# NCUT AI 系網 — RPage 改版套件

把現有 RPage 系網（https://ai.ncut.edu.tw/）的前端「重新上妝」成 `ncut_ai_redesign_mock.html` 的藍＋金乾淨風格。
**不動後台架構、不換平台**，只用 RPage 提供的「自訂 CSS / 自訂 HTML / 自訂模組」三個欄位。

## 檔案與貼上位置

| 檔案 | 貼到 RPage 後台哪裡 | 作用 |
|---|---|---|
| `header.html` | 頁面管理 →（首頁）→ **頭部 HTML** | 載入字體 + 補 meta（原本是「請填寫網站簡述」佔位字）|
| `override.css` | 頁面管理 →（首頁）→ **頭部 CSS** | 全站重新上妝（顏色／字體／導覽／消息／獲獎牆／頁尾）|
| `hero-module.html` | 模組管理 → 新增 **自訂 HTML 模組** → 放首頁最上方 | mock 的招牌 Hero（CSS 變不出來，要靠它）|
| `enhance.js` | 頭部 HTML 欄位（用 `<script>` 包）| 選用，捲動淡入 |

> 若後台只有一個「頭部程式碼」欄位，就把 `header.html` + `<style>override.css 內容</style>` 一起貼。

## 套用後能看到的改變（不碰後台結構）
- 整站藍＋金配色、Space Grotesk + Noto Sans TC 字體層級
- 頂部導覽 → sticky 白色 bar、招生訊息變實心 pill
- 模組標題 → 金色 eyebrow + 大標
- 最新消息 → 底線分頁 + 乾淨列表（空縮圖自動收掉）
- **獲獎輪播亂尺寸圖 → `object-fit:cover` 統一成整齊金頂卡片**（最有感的一塊）
- 頁尾 → 深藍版

## 已知限制（誠實說）
- **URL 仍是 `/p/412-1063-xxxx.php`** —— 平台引擎寫死，改不掉（不影響外觀）。
- **沒有 server 端響應式圖片**（台大那種 srcset 多尺寸）—— 手機會載原圖。
- **你是在「覆蓋」而非「擁有」markup**：RPage 哪天改版、class 變了，CSS 可能要跟著修。
  → 所以 selector 盡量綁穩定結構 class，JS 寫成抓不到就略過。

## 上線前要做的兩件事
1. **確認後台有開這幾個欄位**（頭部 CSS / 頭部 HTML / 自訂模組）。有些學校計網中心會鎖，即使你是網站管理者也看不到。
2. **比對真實 class**：套上去若某塊沒生效，按 F12 看那塊實際的 class，把 `override.css` 對應 selector 改成你站上的值。本套件的 selector 是依 2026-06 抓到的首頁 DOM 寫的（`.module-adv`、`.d-item.v-it`、`.o-footer` 等）。

## 建議上線順序（風險由低到高）
1. 先只貼 `override.css` 看整體上妝 → 2. 加 `header.html` 字體 → 3. 加 `hero-module.html` → 4. 選用 `enhance.js`。
每一步都能單獨回退（清空該欄位即可），系辦的日常編輯流程完全不受影響。
