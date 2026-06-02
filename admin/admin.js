let data;

const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const esc = (value = "") => String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));

const listFields = new Set([
  "duties",
  "sections.0.body",
  "sections.0.items",
  "children",
  "focus",
  "courses",
  "outcomes",
  "themes",
  "training"
]);

boot();

async function boot() {
  bindStaticEvents();
  const status = await fetch("../api/status").then((r) => r.json()).catch(() => ({ authenticated: false }));
  if (status.authenticated) await loadEditor();
}

function bindStaticEvents() {
  $("[data-login]")?.addEventListener("submit", login);
  $("[data-save]")?.addEventListener("click", save);
  $("[data-admin-search]")?.addEventListener("input", filterAdminItems);
  $("[data-build-prompt]")?.addEventListener("click", buildAssistantPrompt);
  $("[data-copy-prompt]")?.addEventListener("click", copyAssistantPrompt);
  $("[data-clear-prompt]")?.addEventListener("click", () => {
    $("[data-assistant-input]").value = "";
    $("[data-assistant-output]").value = "";
  });

  document.addEventListener("click", (event) => {
    const nav = event.target.closest("[data-admin-target]");
    if (nav) setActiveAdminPanel(nav.dataset.adminTarget);

    const remove = event.target.closest("[data-remove]");
    if (remove) {
      removePath(remove.dataset.remove);
      renderAll();
    }
  });

  document.addEventListener("input", (event) => {
    const field = event.target.closest("[data-path]");
    if (!field || !data) return;
    setPath(field.dataset.path, field.dataset.kind === "list" ? toList(field.value) : field.value);
    syncJson();
  });

  bindAddButtons();
}

function bindAddButtons() {
  $("[data-add-hero]")?.addEventListener("click", () => {
    data.hero ||= [];
    data.hero.push({
      kicker: "NCUT AI",
      title: "新增主視覺標題",
      text: "請輸入主視覺說明文字。",
      image: data.identity?.defaultImage || data.identity?.logo || "",
      position: "center center",
      video: "",
      primary: { label: "了解更多", href: "./" },
      secondary: { label: "相關資訊", href: "./" }
    });
    renderAll();
  });
  $("[data-add-news]")?.addEventListener("click", () => {
    data.news ||= [];
    data.news.unshift({ date: today(), category: "系所公告", title: "新增公告標題", summary: "", href: "", image: data.identity?.defaultImage || "" });
    renderAll();
  });
  $("[data-add-faculty]")?.addEventListener("click", () => {
    data.faculty ||= [];
    data.faculty.push({ name: "新增教師", enName: "", role: "專任教師", email: "", phone: "", photo: data.identity?.logo || "", education: "", expertise: "", office: "", lab: "" });
    renderAll();
  });
  $("[data-add-staff]")?.addEventListener("click", () => {
    data.staff ||= [];
    data.staff.push({ name: "新增行政人員", role: "行政人員", email: "", phone: "", duties: [] });
    renderAll();
  });
  $("[data-add-page]")?.addEventListener("click", () => {
    data.pages ||= [];
    data.pages.push({ slug: `page-${Date.now()}`, group: "新增頁面", title: "新增內容頁面", summary: "", image: "", sections: [{ heading: "段落標題", body: ["段落文字"], items: [] }], links: [] });
    renderAll();
  });
  $("[data-add-student-resource]")?.addEventListener("click", () => {
    data.studentResources ||= [];
    data.studentResources.push({ title: "新增學生資源", category: "學生資源", summary: "", href: "", children: [] });
    renderAll();
  });
  $("[data-add-special-program]")?.addEventListener("click", () => {
    data.specialPrograms ||= [];
    data.specialPrograms.push({ slug: `program-${Date.now()}`, title: "新增專班資訊", summary: "", links: [] });
    renderAll();
  });
  $("[data-add-metric]")?.addEventListener("click", () => {
    data.metrics ||= [];
    data.metrics.push({ value: "NEW", label: "新增數據說明" });
    renderAll();
  });
  $("[data-add-quick-link]")?.addEventListener("click", () => {
    data.quickLinks ||= [];
    data.quickLinks.push({ kicker: "Link", label: "新增快速入口", href: "./" });
    renderAll();
  });
  $("[data-add-home-feature]")?.addEventListener("click", () => {
    data.homeFeatures ||= [];
    data.homeFeatures.push({ title: "新增教學特色", text: "" });
    renderAll();
  });
  $("[data-add-video]")?.addEventListener("click", () => {
    data.videos ||= [];
    data.videos.push({ title: "新增影音", embed: "" });
    renderAll();
  });
}

async function login(event) {
  event.preventDefault();
  const password = new FormData(event.currentTarget).get("password");
  const response = await fetch("../api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password })
  });
  if (!response.ok) {
    setStatus("密碼錯誤，請重新輸入。", true);
    return;
  }
  await loadEditor();
}

async function loadEditor() {
  data = await fetch("../api/site", { cache: "no-store" }).then((r) => r.json());
  $("[data-login]")?.classList.add("hidden");
  $("[data-editor]")?.classList.remove("hidden");
  renderAll();
  setStatus("資料已載入。");
}

async function save() {
  try {
    const jsonText = $("[data-json-editor]")?.value;
    if (jsonText?.trim()) data = JSON.parse(jsonText);
  } catch (error) {
    setStatus(`JSON 格式錯誤：${error.message}`, true);
    return;
  }

  const response = await fetch("../api/site", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  const result = await response.json().catch(() => ({}));
  if (!response.ok || !result.ok) {
    setStatus(result.message || "儲存失敗，請檢查資料格式。", true);
    return;
  }
  setStatus(`已儲存。備份檔：${result.backup || "已建立"}`);
}

function renderAll() {
  renderOverview();
  renderHero();
  renderHomeBlocks();
  renderNews();
  renderFaculty();
  renderStaff();
  renderPages();
  renderStudentResources();
  renderSpecialPrograms();
  syncJson();
}

function renderOverview() {
  const stats = [
    ["主視覺", data.hero?.length || 0, "圖片、影片與招生輪播"],
    ["最新消息", data.news?.length || 0, "公告、活動、學生資訊"],
    ["師資", data.faculty?.length || 0, "教師個人頁與專長"],
    ["內容頁", data.pages?.length || 0, "系所介紹與課程資訊"],
    ["學生資源", data.studentResources?.length || 0, "課程、專題與畢業門檻"],
    ["校內連結", data.campusLinks?.length || 0, "校務系統與常用平台"]
  ];
  $("[data-admin-overview]").innerHTML = stats.map(([label, value, hint]) => `
    <article class="stat-card">
      <span>${label}</span>
      <strong>${value}</strong>
      <small>${hint}</small>
    </article>
  `).join("");
  setText("[data-count-hero]", `${data.hero?.length || 0} 項`);
  setText("[data-count-news]", `${data.news?.length || 0} 則`);
  setText("[data-count-faculty]", `${data.faculty?.length || 0} 位`);
  setText("[data-count-pages]", `${data.pages?.length || 0} 頁`);
}

function renderHero() {
  $("[data-hero-editor]").innerHTML = (data.hero || []).map((item, i) => itemCard("主視覺", i, `hero.${i}`, [
    input("標籤", `hero.${i}.kicker`, item.kicker),
    input("標題", `hero.${i}.title`, item.title),
    textarea("說明", `hero.${i}.text`, item.text),
    input("圖片 URL", `hero.${i}.image`, item.image),
    input("圖片位置", `hero.${i}.position`, item.position || "center center"),
    input("影片 Embed URL", `hero.${i}.video`, item.video || ""),
    input("主按鈕文字", `hero.${i}.primary.label`, item.primary?.label || ""),
    input("主按鈕連結", `hero.${i}.primary.href`, item.primary?.href || ""),
    input("次按鈕文字", `hero.${i}.secondary.label`, item.secondary?.label || ""),
    input("次按鈕連結", `hero.${i}.secondary.href`, item.secondary?.href || "")
  ], item.title)).join("");
}

function renderHomeBlocks() {
  $("[data-metrics-editor]").innerHTML = blockTitle("首頁數據") + (data.metrics || []).map((item, i) => itemCard("數據", i, `metrics.${i}`, [
    input("數值", `metrics.${i}.value`, item.value),
    input("說明", `metrics.${i}.label`, item.label)
  ], item.value)).join("");

  $("[data-quick-links-editor]").innerHTML = blockTitle("快速入口") + (data.quickLinks || []).map((item, i) => itemCard("入口", i, `quickLinks.${i}`, [
    input("英文標籤", `quickLinks.${i}.kicker`, item.kicker),
    input("標題", `quickLinks.${i}.label`, item.label),
    input("連結", `quickLinks.${i}.href`, item.href)
  ], item.label)).join("");

  $("[data-home-features-editor]").innerHTML = blockTitle("教學特色") + (data.homeFeatures || []).map((item, i) => itemCard("特色", i, `homeFeatures.${i}`, [
    input("標題", `homeFeatures.${i}.title`, item.title),
    textarea("說明", `homeFeatures.${i}.text`, item.text)
  ], item.title)).join("");

  $("[data-videos-editor]").innerHTML = blockTitle("影音") + (data.videos || []).map((item, i) => itemCard("影音", i, `videos.${i}`, [
    input("標題", `videos.${i}.title`, item.title),
    input("YouTube Embed URL", `videos.${i}.embed`, item.embed)
  ], item.title)).join("");
}

function renderNews() {
  $("[data-news-editor]").innerHTML = (data.news || []).map((item, i) => itemCard("公告", i, `news.${i}`, [
    input("日期", `news.${i}.date`, item.date, "date"),
    input("分類", `news.${i}.category`, item.category),
    input("標題", `news.${i}.title`, item.title),
    textarea("摘要", `news.${i}.summary`, item.summary),
    input("連結", `news.${i}.href`, item.href || ""),
    input("圖片 URL", `news.${i}.image`, item.image || "")
  ], item.title)).join("");
}

function renderFaculty() {
  $("[data-faculty-editor]").innerHTML = (data.faculty || []).map((item, i) => itemCard("教師", i, `faculty.${i}`, [
    input("姓名", `faculty.${i}.name`, item.name),
    input("英文姓名", `faculty.${i}.enName`, item.enName),
    input("職稱", `faculty.${i}.role`, item.role),
    input("Email", `faculty.${i}.email`, item.email),
    input("電話", `faculty.${i}.phone`, item.phone),
    input("照片 URL", `faculty.${i}.photo`, item.photo),
    input("辦公室 / 研究室", `faculty.${i}.office`, item.office || ""),
    input("實驗室", `faculty.${i}.lab`, item.lab || ""),
    textarea("學歷", `faculty.${i}.education`, item.education || ""),
    textarea("專長", `faculty.${i}.expertise`, item.expertise || "")
  ], item.name)).join("");
}

function renderStaff() {
  $("[data-staff-editor]").innerHTML = (data.staff || []).map((item, i) => itemCard("行政", i, `staff.${i}`, [
    input("姓名", `staff.${i}.name`, item.name),
    input("職稱", `staff.${i}.role`, item.role),
    input("Email", `staff.${i}.email`, item.email),
    input("電話", `staff.${i}.phone`, item.phone),
    textarea("業務項目，每行一項", `staff.${i}.duties`, fromList(item.duties), "list")
  ], item.name)).join("");
}

function renderPages() {
  $("[data-pages-editor]").innerHTML = (data.pages || []).map((item, i) => itemCard("頁面", i, `pages.${i}`, [
    input("Slug", `pages.${i}.slug`, item.slug),
    input("群組", `pages.${i}.group`, item.group),
    input("標題", `pages.${i}.title`, item.title),
    textarea("摘要", `pages.${i}.summary`, item.summary),
    input("主圖 URL", `pages.${i}.image`, item.image || ""),
    input("第一段標題", `pages.${i}.sections.0.heading`, item.sections?.[0]?.heading || ""),
    textarea("第一段內容，每行一段", `pages.${i}.sections.0.body`, fromList(item.sections?.[0]?.body), "list")
  ], item.title)).join("");
}

function renderStudentResources() {
  $("[data-student-resources-editor]").innerHTML = blockTitle("學生資源") + (data.studentResources || []).map((item, i) => itemCard("資源", i, `studentResources.${i}`, [
    input("標題", `studentResources.${i}.title`, item.title),
    input("分類", `studentResources.${i}.category`, item.category),
    textarea("摘要", `studentResources.${i}.summary`, item.summary),
    input("連結", `studentResources.${i}.href`, item.href || "")
  ], item.title)).join("");
}

function renderSpecialPrograms() {
  $("[data-special-programs-editor]").innerHTML = blockTitle("專班資訊") + (data.specialPrograms || []).map((item, i) => itemCard("專班", i, `specialPrograms.${i}`, [
    input("Slug", `specialPrograms.${i}.slug`, item.slug),
    input("標題", `specialPrograms.${i}.title`, item.title),
    textarea("摘要", `specialPrograms.${i}.summary`, item.summary)
  ], item.title)).join("");
}

function itemCard(type, index, path, fields, title = "") {
  return `
    <article class="item">
      <div class="item-head">
        <h3>${type} ${index + 1}${title ? `｜${esc(title)}` : ""}</h3>
        <button class="danger" type="button" data-remove="${path}">刪除</button>
      </div>
      <div class="grid">${fields.join("")}</div>
    </article>`;
}

function blockTitle(text) {
  return `<h3 class="editor-subtitle">${text}</h3>`;
}

function input(label, path, value = "", type = "text") {
  return `<label>${label}<input type="${type}" data-path="${path}" value="${esc(value)}"></label>`;
}

function textarea(label, path, value = "", kind = "") {
  return `<label>${label}<textarea data-path="${path}" ${kind ? `data-kind="${kind}"` : ""}>${esc(value)}</textarea></label>`;
}

function setActiveAdminPanel(name) {
  $$("[data-admin-target]").forEach((button) => button.classList.toggle("is-active", button.dataset.adminTarget === name));
  $$("[data-admin-panel]").forEach((panel) => panel.classList.toggle("is-focused", panel.dataset.adminPanel === name));
  document.querySelector(`[data-admin-panel="${CSS.escape(name)}"]`)?.scrollIntoView({ behavior: "smooth", block: "start" });
}

function filterAdminItems() {
  const query = ($("[data-admin-search]")?.value || "").trim().toLowerCase();
  $$(".item").forEach((item) => {
    item.hidden = query && !item.textContent.toLowerCase().includes(query);
  });
}

function buildAssistantPrompt() {
  const type = $("[data-assistant-type]").value;
  const inputText = $("[data-assistant-input]").value.trim();
  const prompt = [
    "請協助維護國立勤益科技大學人工智慧應用工程系網站資料。",
    `任務類型：${type}`,
    "請先判斷資料應寫入 data/site.json 的哪個區塊，保留既有資料，不要刪除未提到的內容。",
    "輸出要求：",
    "1. 整理成可直接貼入 JSON 的結構。",
    "2. 日期統一使用 YYYY-MM-DD。",
    "3. 圖片、PDF、外部系統連結請保留完整 URL。",
    "4. 若資料不足，請列出缺少欄位，不要自行編造。",
    "",
    "原始資料：",
    inputText || "請在這裡貼上要處理的公告、師資、圖片或連結資料。"
  ].join("\n");
  $("[data-assistant-output]").value = prompt;
  setStatus("已產生代理人指令。");
}

async function copyAssistantPrompt() {
  const output = $("[data-assistant-output]");
  if (!output.value.trim()) {
    setStatus("目前沒有可複製的指令。", true);
    return;
  }
  try {
    await navigator.clipboard.writeText(output.value);
  } catch {
    output.select();
    document.execCommand("copy");
  }
  setStatus("代理人指令已複製。");
}

function setPath(path, value) {
  const parts = path.split(".");
  let ref = data;
  for (let i = 0; i < parts.length - 1; i += 1) {
    const key = normalizeKey(parts[i]);
    const nextKey = normalizeKey(parts[i + 1]);
    if (ref[key] == null) ref[key] = typeof nextKey === "number" ? [] : {};
    ref = ref[key];
  }
  ref[normalizeKey(parts.at(-1))] = value;
}

function removePath(path) {
  const parts = path.split(".");
  let ref = data;
  for (let i = 0; i < parts.length - 1; i += 1) ref = ref?.[normalizeKey(parts[i])];
  const key = normalizeKey(parts.at(-1));
  if (Array.isArray(ref)) ref.splice(key, 1);
  else if (ref && key in ref) delete ref[key];
  syncJson();
}

function normalizeKey(key) {
  return /^\d+$/.test(key) ? Number(key) : key;
}

function toList(value) {
  return value.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
}

function fromList(value) {
  return Array.isArray(value) ? value.join("\n") : (value || "");
}

function syncJson() {
  const editor = $("[data-json-editor]");
  if (editor) editor.value = JSON.stringify(data, null, 2);
}

function setStatus(message, isError = false) {
  const status = $("[data-status]");
  if (!status) return;
  status.textContent = message;
  status.classList.toggle("is-error", isError);
}

function setText(selector, text) {
  const node = $(selector);
  if (node) node.textContent = text;
}

function today() {
  return new Date().toISOString().slice(0, 10);
}
