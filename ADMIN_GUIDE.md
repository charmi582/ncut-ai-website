# 國立勤益科技大學人工智慧應用工程系網站操作說明

本網站採用「靜態前台 + JSON 資料 + Python 後台 API」架構。前台接近台大首頁的做法：HTML 頁面完整輸出，CSS 與少量 JavaScript 負責輪播、選單、分類、搜尋與互動；後台提供表單給系辦助理維護內容。

## 啟動網站

在 PowerShell 執行：

```powershell
cd D:\web
python server.py
```

預設網址：

- 前台：http://localhost:8080/
- 後台：http://localhost:8080/admin/

預設後台密碼為 `ncutai`。正式上線時請改用環境變數設定：

```powershell
$env:NCUT_ADMIN_PASSWORD="請改成正式密碼"
python server.py
```

## 後台可維護內容

後台登入後可用表單維護：

- 首頁主視覺
- 首頁統計數字、快速入口、首頁特色、系所影片
- 最新消息
- 師資陣容
- 內容頁面：系所沿革、教學宗旨、發展方向、課程與就業、專業實驗室、學生專區、專班資訊等
- 學生專區入口：學分計畫、課程地圖、實務專題、畢業門檻、核心證照、校外實習、課程抵免、系學會、系友會
- 專班資源：產學攜手合作專班、海外青年技術訓練班
- 課程與職涯模組
- 專業實驗室

一般助理請優先使用表單區塊；「進階：完整 JSON」保留給技術人員批次修改。

## 備份與還原

每次後台儲存前，系統會自動將原本的資料備份到：

```text
D:\web\data\backups
```

檔名格式：

```text
site-YYYYMMDD-HHMMSS.json
```

系統保留最近 30 份備份。

如需還原，停止伺服器後，把備份檔覆蓋回：

```text
D:\web\data\site.json
```

再重新啟動 `python server.py`。

## 官方資訊庫

官方資訊庫位於：

```text
http://localhost:8080/official.html
```

它整理原系網匯入的公開頁面、公告、圖片與外部連結，並提供分類與搜尋。這一區可作為正式頁面改寫前的完整資料來源，避免漏掉原站內容。

文件與資源索引位於：

```text
http://localhost:8080/resources.html
```

它集中列出 PDF、DOC、XLS、外部系統與常用連結。

## 重新匯入官方資料

如需重新抓取原系網資料，可執行：

```powershell
cd D:\web
python tools\import_ncut.py
```

匯入結果會更新：

```text
D:\web\data\official-pages.json
```

## 主要檔案

- `index.html`：首頁
- `page.html`：一般內容頁
- `faculty.html`：師資頁
- `news.html`：最新消息頁
- `official.html`：官方資訊庫
- `resources.html`：文件與資源索引
- `admin/`：後台介面
- `data/site.json`：主要網站資料
- `data/official-pages.json`：原系網匯入資料
- `server.py`：本機後台伺服器

## 部署建議

若只是校內展示，可直接在系辦電腦或校內伺服器執行 `python server.py`。

若要正式上線，建議：

- 使用正式網域與 HTTPS
- 設定 `NCUT_ADMIN_PASSWORD`
- 將 `D:\web\data` 納入定期備份
- 由校方資訊單位協助設定反向代理，例如 IIS、Nginx 或 Apache
- 後台只允許校內 IP 或 VPN 存取
