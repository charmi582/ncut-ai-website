from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, urldefrag
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from pathlib import Path
import json
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "official-pages.json"
BASE = "https://n063.ncut.edu.tw/"
SEEDS = [
    BASE,
    "https://n063.ncut.edu.tw/p/412-1063-2370.php?Lang=zh-tw",
    "https://n063.ncut.edu.tw/p/412-1063-2371.php?Lang=zh-tw",
    "https://n063.ncut.edu.tw/p/412-1063-2410.php?Lang=zh-tw",
    "https://n063.ncut.edu.tw/p/412-1063-2380.php?Lang=zh-tw",
    "https://n063.ncut.edu.tw/p/412-1063-8062.php?Lang=zh-tw",
    "https://n063.ncut.edu.tw/p/412-1063-8200.php?Lang=zh-tw",
    "https://n063.ncut.edu.tw/p/412-1063-85.php?Lang=zh-tw",
    "https://n063.ncut.edu.tw/app/index.php?Action=mobileloadmod&Type=mobile_rcg_mstr&Nbr=726",
    "https://n063.ncut.edu.tw/app/index.php?Action=mobileloadmod&Type=mobile_rcg_mstr&Nbr=730",
]

NOISE = {
    ":::", "Menu", "OK", "Cancel", "Close (Esc)", "Share", "Toggle fullscreen",
    "Zoom in/out", "Previous (arrow left)", "Next (arrow right)", "回到頂部",
    "繁體", "English", "本功能需使用支援JavaScript之瀏覽器才能正常操作",
    "字體大小調整", "小", "中", "大", "跳到主要內容區"
}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.links = []
        self.images = []
        self.skip = 0
        self.title = ""
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag in ("script", "style", "noscript"):
            self.skip += 1
        if tag == "title":
            self.in_title = True
        if tag == "a" and data.get("href"):
            self.links.append({
                "href": data.get("href", ""),
                "label": data.get("title") or data.get("aria-label") or ""
            })
        if tag == "img" and data.get("src"):
            self.images.append({
                "src": data.get("src", ""),
                "alt": data.get("alt", "")
            })

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self.skip:
            self.skip -= 1
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        text = " ".join(data.split())
        if not text:
            return
        if self.in_title:
            self.title += text
        if self.skip or text in NOISE:
            return
        self.text.append(text)


def fetch(url):
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8", "replace")


def normalize(base_url, href):
    absolute = urldefrag(urljoin(base_url, href))[0]
    parsed = urlparse(absolute)
    if parsed.scheme not in ("http", "https", "mailto"):
        return ""
    return absolute


def should_crawl(url):
    parsed = urlparse(url)
    if parsed.netloc not in ("n063.ncut.edu.tw", "ai.ncut.edu.tw"):
        return False
    if "1063" not in url:
        return False
    if any(url.lower().endswith(ext) for ext in (".pdf", ".jpg", ".png", ".gif", ".doc", ".docx", ".xls", ".xlsx")):
        return False
    return True


def title_from_text(parser, url):
    for item in parser.text:
        if item not in NOISE and len(item) > 1:
            return item[:80]
    return parser.title or url


def crawl():
    queue = list(dict.fromkeys(SEEDS))
    seen = set()
    pages = []
    resources = {}

    while queue and len(seen) < 90:
        url = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)
        try:
            html = fetch(url)
        except (HTTPError, URLError, TimeoutError, ValueError) as error:
            pages.append({"url": url, "title": "讀取失敗", "error": str(error), "text": [], "links": [], "images": []})
            continue

        parser = PageParser()
        parser.feed(html)
        links = []
        for link in parser.links:
            href = normalize(url, link["href"])
            if not href:
                continue
            label = " ".join((link["label"] or "").split())
            links.append({"href": href, "label": label})
            if should_crawl(href) and href not in seen and href not in queue:
                queue.append(href)
            if not should_crawl(href):
                resources[href] = label or href

        pages.append({
            "id": len(pages),
            "url": url,
            "title": title_from_text(parser, url),
            "text": parser.text[:260],
            "links": links[:120],
            "images": [
                {"src": normalize(url, image["src"]), "alt": image["alt"]}
                for image in parser.images[:30]
                if normalize(url, image["src"])
            ]
        })
        time.sleep(0.08)

    return {
        "generatedAt": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source": BASE,
        "pageCount": len(pages),
        "resourceCount": len(resources),
        "pages": pages,
        "resources": [{"href": href, "label": label} for href, label in sorted(resources.items())]
    }


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = crawl()
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT} pages={payload['pageCount']} resources={payload['resourceCount']}")
