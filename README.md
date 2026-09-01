# 系網管理員說明

這個專案是「本地 CMS 後台 + GitHub Pages 靜態前台」架構。管理員平常在本機後台修改資料，確認無誤後 push 到 GitHub，GitHub Actions 會自動重新部署靜態網站。

## 架構概念

```text
管理員電腦
  本地 CMS：server.py + admin/
        ↓
  修改 data/site.json 與 assets/uploads/
        ↓
  git commit / git push origin main
        ↓
GitHub
  GitHub Actions 執行 scripts/build-pages.mjs
        ↓
  產生 dist/ 靜態網站
        ↓
GitHub Pages
  對外公開前台網頁
```

## 前台如何運作

前台是純靜態網站，可以部署在 GitHub Pages。

主要檔案：

- `index.html`：首頁
- `news.html`：最新消息頁
- `faculty.html`：師資列表
- `faculty-detail.html`：教師詳細頁
- `page.html`：一般內容頁
- `student-resource.html`：學生資源詳細頁
- `resources.html`：資源索引
- `campus-links.html`：校內連結
- `awards.html`：獲獎資訊
- `script.js`：前台資料載入與畫面渲染
- `styles.css`：前台樣式
- `data/site.json`：主要內容資料
- `data/official-pages.json`：舊站或官方頁面資料
- `assets/`：圖片、影片、圖示等素材

前台沒有資料庫，也不需要 Python 後端。瀏覽器會透過 `script.js` 讀取：

```text
./data/site.json
./data/official-pages.json
```

因此 GitHub Pages 可以正常顯示前台內容。

## 後端如何運作

後端只給管理員在本機使用，不會部署到 GitHub Pages。

主要檔案：

- `server.py`：本地 CMS 後端
- `admin/index.html`：後台介面
- `admin/admin.js`：後台操作邏輯
- `admin/admin.css`：後台樣式
- `scripts/start-local-cms.ps1`：Windows 啟動腳本

`server.py` 預設只綁定：

```text
127.0.0.1
```

也就是只有本機可以開啟。管理 API 包含：

- `/api/login`：登入本地 CMS
- `/api/status`：檢查登入與本地狀態
- `/api/site`：讀取或儲存 `data/site.json`
- `/api/assets`：列出素材
- `/api/assets/upload`：上傳素材到 `assets/uploads/`
- `/api/git/status`：查看 Git 狀態
- `/api/build`：執行 GitHub Pages 靜態 build
- `/api/git/commit`：建立 commit
- `/api/git/push`：push 到 `origin main`

## 啟動本地 CMS

在 PowerShell 執行：

```powershell
cd D:\web\ncut-ai-website
$env:NCUT_ADMIN_PASSWORD="請改成管理員自己的強密碼"
.\scripts\start-local-cms.ps1
```

開啟後台：

```text
http://127.0.0.1:8080/admin/
```

開啟前台預覽：

```text
http://127.0.0.1:8080/
```

## 管理員日常更新流程

1. 啟動本地 CMS。
2. 登入後台。
3. 修改最新消息、首頁輪播、教師資料、學生資源或素材。
4. 按「儲存內容」。
5. 開前台預覽確認畫面。
6. 按「執行 build」確認靜態部署包可正常產生。
7. 建立 commit。
8. 執行 `git push origin main`。
9. 到 GitHub Actions 或 GitHub Pages 檢查部署結果。

## GitHub Pages 部署方式

GitHub Pages 使用 GitHub Actions 部署。

相關檔案：

- `.github/workflows/pages.yml`
- `scripts/build-pages.mjs`

當 `main` 分支有新的 push 時，GitHub Actions 會：

1. checkout 專案
2. 使用 Node.js
3. 執行 `node scripts/build-pages.mjs`
4. 上傳 `dist/` 作為 Pages artifact
5. 部署到 GitHub Pages

目前測試網址：

```text
https://ncutaiweb.github.io/ncut-ai-website/
```

## 什麼會被部署

GitHub Pages 只部署 `dist/` 內的靜態前台。

會部署：

- HTML 前台頁面
- `script.js`
- `styles.css`
- `data/site.json`
- `data/official-pages.json`
- `assets/`
- `manifest.webmanifest`
- `robots.txt`
- `sitemap.xml`

不會部署：

- `admin/`
- `server.py`
- `tools/`
- `data/backups/`
- `scripts/`
- `CODEX_LOCAL_CMS_RULES.md`
- 本地測試檔案

## 內容資料位置

大部分網站內容都在：

```text
data/site.json
```

常見資料區塊：

- `identity`：網站名稱、logo、SEO 相關設定
- `contact`：聯絡資訊
- `hero`：首頁輪播
- `metrics`：首頁統計數字
- `quickLinks`：快速連結
- `pages`：一般內容頁
- `faculty`：教師資料
- `staff`：行政人員
- `news`：最新消息
- `videos`：影音
- `studentResources`：學生資源
- `campusLinks`：校內連結
- `awardSlides`：獲獎資訊

## 素材管理

新上傳素材建議放在：

```text
assets/uploads/
```

前台引用路徑應使用相對路徑：

```text
./assets/uploads/example.jpg
```

不要使用本機磁碟路徑：

```text
D:\web\ncut-ai-website\assets\example.jpg
file:///D:/web/ncut-ai-website/assets/example.jpg
```

## 測試與檢查

每次修改後建議執行：

```powershell
python -m py_compile server.py
node --check script.js
node --check admin\admin.js
node scripts\build-pages.mjs
git diff --check
```

確認 Git 狀態：

```powershell
git status --short --branch
```

## 資安注意事項

- 本地 CMS 只應在管理員電腦執行。
- 不要將 `HOST` 改成 `0.0.0.0`，除非已評估區網風險。
- 不要把密碼、token、GitHub PAT、API key 寫入專案。
- 建議保持 Windows Security、Microsoft Defender Antivirus、Windows Defender Firewall 開啟。
- `data/backups/` 不應 commit。
- `dist/` 不應 commit。

## 給 Codex 的維護規則

如果未來要請 Codex 協助新增消息、修改教師資料或正式發布，請先要求 Codex 閱讀：

```text
CODEX_LOCAL_CMS_RULES.md
```

範例指令：

```text
請先讀取 CODEX_LOCAL_CMS_RULES.md，然後幫我新增一則最新消息。
```

```text
請先讀取 CODEX_LOCAL_CMS_RULES.md，然後幫我修改某某老師的資訊。
```
