# 交接說明 — NCUT AI 系網 RPage 改版（給接手的 Claude）

> 用法：請先讀完這份，再讀同資料夾的其他檔案。所有成品都在 `rpage-skin/` 內。
> 使用者是勤益科大 AI 系學生，**擁有系網 RPage 網站管理者（最高）權限**。

## 一句話目標
把現有系網 https://ai.ncut.edu.tw/（RPage 平台、PHP server-render）的前端「重新上妝」成
`~/Downloads/ncut_ai_redesign_mock.html` 的藍＋金乾淨現代風格。**不換平台、不動後台架構**，
只用 RPage 的「頭部 CSS / 頭部 HTML / 自訂 HTML 模組」三個欄位注入。

本案決定不另建新站，改在現有 RPage 上做前端改版（保留平台、不動後台架構、可隨時還原）。

## 平台事實（已驗證，不要重查）
- 這版 RPage 是 **PHP 多頁面（MPA）**，子頁網址 `/p/412-1063-XXXX.php?Lang=zh-tw`，同源。
- 真實 DOM 的穩定 class（寫 override CSS 的命脈，2026-06 抓自首頁）：
  - 導覽：`.mnavbar.mn-collapse` → `ul.nav.navbar-nav > li > a`、`.mlogo`
  - 模組外殼：`.module.module-xxx.md_style1` → `.mouter` → `header.mt > h2.mt-title` + `section.mb`
  - 最新消息：`.module-complex` → `ul.nav.nav-tabs` + `.tab-content > .tab-pane#cmb_251_0..4`，
    每則 `.d-item.v-it.col-sm-12 > .mbox > .d-txt > .mtitle > a`
  - 獲獎輪播：`.module-adv` → `.owl-carousel` → `figure.figBS > img.madv-img` + `.bn-txt`
  - 頁尾：`.o-footer` → `.o-footer__main`（內含 inline `font-family:微軟正黑體` 與 inline 顏色，需 `!important` 壓）
- **RPage 原生有首頁背景影片功能**：DOM 裡有空的 `<div class="fpbgvideo"></div>`（槽存在、未設定影片）。

## 檔案與貼上位置
| 檔案 | 貼到 RPage 後台 | 作用 |
|---|---|---|
| `override.css` | 首頁 → 頭部 CSS | 全站上妝（導覽／消息／獲獎牆統一／頁尾深藍）|
| `transitions.css` | **首頁＋內頁**頭部 CSS | 子頁面淡入淡出轉場（CSS View Transitions，純 CSS）|
| `header.html` | 首頁 → 頭部 HTML | 載字體（Space Grotesk + Noto Sans TC）+ 補 meta |
| `hero-module.html` | 自訂 HTML 模組（放首頁最上方）| mock 招牌 Hero（靜態藍金版）|
| `enhance.js` | 頭部 HTML（選用）| 捲動淡入 |

## 週日現場操作順序（風險低→高，每步可單獨回退＝清空欄位）
0. **先備份再修改**：照 `backup-原始/備份步驟.md`，把每個要動的欄位現有內容複製存檔、前台整頁截圖。
   還原 = 貼回原始內容或清空欄位。內容資料（公告/圖片/頁面）全程不動，最壞只是跑版、不會掉資料。
1. **先確認三個欄位有沒有對此帳號開放**：頭部 CSS、頭部 HTML、自訂 HTML 模組。
   有些計網中心會鎖，鎖了就整件事卡住——這是唯一的硬關卡，先驗。
2. 貼 `override.css` 看整體上妝 → 用 F12 比對：沒生效的區塊，抓它實際 class 修對應 selector。
3. 貼 `transitions.css` 到**首頁與內頁兩欄**（只貼首頁，子頁不會有轉場）。
4. 貼 `header.html`（字體）。
5. 加 `hero-module.html` 自訂模組。
6. 選用 `enhance.js`。

## 已知限制（誠實告知使用者，別承諾做不到的）
- URL 仍是 `/p/412-1063-XXXX.php`，平台寫死，改不掉（不影響外觀）。
- 沒有 server 端響應式圖片（srcset 多尺寸），手機載原圖。
- 是「覆蓋」而非「擁有」markup：RPage 改版後 class 若變，CSS 要跟著修 → selector 綁穩定結構、JS 寫防禦性。
- 轉場（View Transitions）：Chrome/Edge 126+、Safari 18.2+ 有；Firefox 目前無 → 自動降級成瞬間切換，不會壞。

## 尚未決定 / 待使用者回覆
1. **影片背景 Hero**：使用者想把開頭藍金畫面換成影片背景（其自建站 `.hero-video` 即滿版影片）。
   RPage 原生 `fpbgvideo` 可能後台就能開；否則用自訂 HTML 放滿版 `<video muted autoplay loop playsinline>` + 深色遮罩 + 手機 poster + reduced-motion。
   **待確認**：影片來源用 (A) 自己的 mp4 檔，還是 (B) YouTube iframe。確定後做「影片背景版 hero」。
2. **教學特色六宮格、文字版獲獎成果牆**：mock 有、但需另外做自訂 HTML 模組（DOM 無結構化資料，CSS 變不出來）。尚未製作。

## 參考檔
- 設計目標：`~/Downloads/ncut_ai_redesign_mock.html`
- 使用者自建站（僅供抽取內容/風格參考）：`~/Desktop/web/ncut-ai-website/`
