# GitHub Pages 靜態部署

這個專案的前台可以部署成 GitHub Pages 靜態網站。後台管理介面需要 `server.py` 提供 `/api/*`，因此不會被放進 Pages 部署產物。

## 已整理的部署方式

- GitHub Actions workflow：`.github/workflows/pages.yml`
- 靜態建置腳本：`scripts/build-pages.mjs`
- 部署輸出資料夾：`dist/`
- Pages artifact 只包含前台需要的 HTML、CSS、JS、`assets/`、`data/`、`robots.txt`、`sitemap.xml`、`manifest.webmanifest`
- 不部署：`admin/`、`server.py`、`tools/`、`rpage-skin/`、`data/backups/`

## 啟用 GitHub Pages

1. 將專案推送到 GitHub。
2. 到 repository 的 `Settings` -> `Pages`。
3. `Build and deployment` 的 `Source` 選擇 `GitHub Actions`。
4. 推送到 `main` 後，workflow 會自動部署。

## 本機檢查

```powershell
node scripts/build-pages.mjs
python -m http.server 8080 -d dist
```

開啟：

```text
http://localhost:8080/
```

## 重要限制

- GitHub Pages 上的前台可正常讀取 `data/site.json` 和 `data/official-pages.json`。
- `/admin/` 不會部署，因為登入、讀取與儲存內容需要 Python API。
- 若要修改網站內容，可以使用本地 CMS：`python server.py` 後開啟 `http://127.0.0.1:8080/admin/`。
- 若未使用 `https://ai.ncut.edu.tw/` 作為自訂網域，請記得調整 `sitemap.xml` 和 `robots.txt` 內的正式網址。

更多本地後台與資安設定請看 `LOCAL_CMS_SECURITY.md`。
