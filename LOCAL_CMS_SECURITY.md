# 本地 CMS 與資安策略

這個專案採用「本地後台 + GitHub Pages 靜態前台」架構。

## 架構

```text
本地 CMS：http://127.0.0.1:8080/admin/
        ↓
修改 data/site.json、assets/uploads/*
        ↓
執行 build 檢查
        ↓
git commit
        ↓
git push origin main
        ↓
GitHub Actions 產生 dist/
        ↓
GitHub Pages 顯示靜態網站
```

## 啟動本地 CMS

建議先設定管理密碼：

```powershell
$env:NCUT_ADMIN_PASSWORD="請換成你自己的強密碼"
python server.py
```

Windows 上也可以使用啟動腳本，它會先顯示 Microsoft Defender 與 Windows Defender Firewall 狀態，並強制使用 `127.0.0.1`：

```powershell
$env:NCUT_ADMIN_PASSWORD="請換成你自己的強密碼"
.\scripts\start-local-cms.ps1
```

開啟：

```text
http://127.0.0.1:8080/admin/
```

## 後台功能

- 編輯首頁輪播、最新消息、師資、行政人員、內容頁、學生資源、統計數字、快速連結與影音
- 直接編輯完整 `data/site.json`
- 上傳圖片、MP4、PDF 到 `assets/uploads/`
- 儲存內容時自動備份到 `data/backups/`
- 查看 Git 狀態
- 執行 GitHub Pages 靜態 build 檢查
- 建立 commit
- 執行 `git push origin main`

## 資安設計

- `server.py` 預設只綁定 `127.0.0.1`，外部網路無法直接連入。
- GitHub Pages 部署產物不包含 `admin/`、`server.py`、`tools/`、`data/backups/`。
- 管理 API 需要登入後才能使用。
- 管理操作會檢查來源，只接受 localhost / 127.0.0.1。
- Cookie 使用 `HttpOnly` 與 `SameSite=Strict`。
- 後台上傳不允許 SVG，降低上傳可執行內容的風險。

## Microsoft / Windows 防護建議

- 保持 Windows Security 開啟。
- 保持 Microsoft Defender Antivirus 即時保護開啟。
- 保持 Windows Defender Firewall 開啟。
- 不要把 `HOST` 改成 `0.0.0.0`，除非你明確需要區網連線並已設定防火牆規則。
- 建議開啟 Windows Security 的 Ransomware protection / Controlled folder access，再將必要工具加入允許清單。
- 定期執行 Windows Update。

## 發布流程

1. 開啟本地 CMS。
2. 修改內容並儲存。
3. 執行 build 檢查。
4. 建立 commit。
5. Push 到 `origin main`。
6. 到 GitHub Actions 或 Pages 查看部署狀態。
