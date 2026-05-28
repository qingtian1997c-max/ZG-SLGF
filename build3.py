import json, openpyxl

wb = openpyxl.load_workbook("specs.xlsx", data_only=True)
ws = wb.active
specs = []
cats_order = []

# Map Excel spec code to PDF filename
code_to_file = {
    "SLT 197-2026": "SLT-197-2026.pdf",
    "SLT 290-2024": "SLT-290-2024.pdf",
    "SLT 386-2025": "SLT-386-2025.pdf",
    "SLT 447-2026": "SLT-447-2026.pdf",
    "SLT 504-2026": "SLT-504-2026.pdf",
    "SL/T 530-2026": "SLT-530-2026.pdf",
    "SLT 612-2026": "SLT-612-2026.pdf",
    "SLT 631.5-2025": "SLT-631.5-2025.pdf",
    "SLT 631.6-2025": "SLT-631.6-2025.pdf",
    "SLT 631.7-2025": "SLT-631.7-2025.pdf",
    "SLT 654-2026": "SLT-654-2026.pdf",
    "SLT 706-2026": "SLT-706-2026.pdf",
    "SLT 851-2025": "SLT-851-2025.pdf",
    "SLT 860-2026": "SLT-860-2026.pdf",
    "SLT 861-2026": "SLT-861-2026.pdf",
    "SLT 862-2026": "SLT-862-2026.pdf",
    "SLT 863-2026": "SLT-863-2026.pdf",
    "SLT 864-2026": "SLT-864-2026.pdf",
    "SLT 865-2026": "SLT-865-2026.pdf",
    "SLT 866-2026": "SLT-866-2026.pdf",
    "SLT 867-2026": "SLT-867-2026.pdf",
    "SLT 868-2026": "SLT-868-2026.pdf",
    "SLT 869-2026": "SLT-869-2026.pdf",
    "SLT 870-2026": "SLT-870-2026.pdf",
}

# Which files are already in the repo (generates raw link)
# SLT 290-2024 is >100MB, needs GitHub Release
needs_release = {"SLT 290-2024"}

BASE_RAW = "https://slgf-pdf.qingtian1997c.workers.dev/"
BASE_RELEASE = "https://github.com/qingtian1997c-max/ZG-SLGF/releases/download/v1.0/"

for row in ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=True):
    seq, code, name, date = row
    code = str(code).strip().replace("  ", " ")
    name = str(name).strip().replace("  ", " ")
    date_str = str(date).strip()
    
    n = name
    if "测量" in n: cat = "勘测测量"
    elif "规划" in n or "设计" in n or "边坡" in n or "使用年限" in n: cat = "规划设计"
    elif "水土保持" in n: cat = "水土保持"
    elif "水文" in n: cat = "水文水资源"
    elif "施工质量" in n or "质量管理" in n or "金属结构" in n or "发电机组" in n or "电气装置" in n: cat = "施工质量"
    elif "安全监测" in n: cat = "安全监测"
    elif "自动化" in n or "无人机" in n or "激光雷达" in n or "数字孪生" in n or "数据分类" in n or "可视化" in n or "模型集成" in n: cat = "数字水利"
    elif "水库调度" in n or "调水工程" in n or "调度管理" in n: cat = "水库调度"
    elif "用水权" in n: cat = "用水权"
    elif "水下" in n or "修复" in n: cat = "维护修复"
    elif "灌溉" in n: cat = "灌溉"
    elif "小水电" in n: cat = "小水电"
    elif "移民" in n: cat = "规划设计"
    else: cat = "其他"
    
    if cat not in cats_order:
        cats_order.append(cat)
    
    filename = code_to_file.get(code, "")
    if filename:
        if code in needs_release:
            file_url = BASE_RELEASE + filename
        else:
            file_url = BASE_RAW + filename
    else:
        file_url = ""
    
    specs.append({
        "id": seq, "code": code, "name": name,
        "date": date_str, "cat": cat, "file": file_url, "size": ""
    })

specs_json = json.dumps(specs, ensure_ascii=False)
cats_json = json.dumps(cats_order, ensure_ascii=False)

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>水利规范文件检索</title>
<style>
  :root {
    --bg: #f0f4f8;
    --card-bg: #ffffff;
    --primary: #1a73e8;
    --primary-light: #e8f0fe;
    --text: #202124;
    --text-secondary: #5f6368;
    --border: #e0e4e8;
    --tag-bg: #e8eaed;
    --tag-active: #1a73e8;
    --tag-active-text: #ffffff;
    --shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
    --shadow-hover: 0 4px 12px rgba(0,0,0,0.1);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    min-height: 100vh;
  }
  header {
    background: linear-gradient(135deg, #1a56db 0%, #1a73e8 100%);
    color: #fff;
    padding: 32px 24px;
    text-align: center;
  }
  header h1 { font-size: 28px; font-weight: 600; margin-bottom: 6px; }
  header p { font-size: 14px; opacity: 0.85; }
  .container { max-width: 960px; margin: 0 auto; padding: 24px 20px; }
  .search-wrap { position: relative; margin-bottom: 20px; }
  .search-wrap input {
    width: 100%; padding: 14px 20px 14px 52px; font-size: 16px;
    border: 2px solid var(--border); border-radius: 12px;
    background: var(--card-bg); outline: none;
    transition: border-color 0.2s, box-shadow 0.2s; box-shadow: var(--shadow);
  }
  .search-wrap input:focus { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(26,115,232,0.15); }
  .search-wrap .icon { position: absolute; left: 18px; top: 50%; transform: translateY(-50%); font-size: 20px; color: var(--text-secondary); pointer-events: none; }
  .stats { font-size: 13px; color: var(--text-secondary); margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; }
  .tags { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 24px; }
  .tag {
    padding: 7px 16px; border-radius: 20px; font-size: 14px; cursor: pointer;
    border: 1px solid var(--border); background: var(--card-bg);
    color: var(--text-secondary); transition: all 0.2s; user-select: none; white-space: nowrap;
  }
  .tag:hover { border-color: var(--primary); color: var(--primary); }
  .tag.active { background: var(--tag-active); color: var(--tag-active-text); border-color: var(--tag-active); }
  .tag .count { font-size: 11px; margin-left: 2px; opacity: 0.7; }
  .card-list { display: flex; flex-direction: column; gap: 12px; }
  .card {
    background: var(--card-bg); border-radius: 12px; padding: 20px 24px;
    box-shadow: var(--shadow); border: 1px solid var(--border);
    transition: box-shadow 0.2s, transform 0.15s; cursor: pointer;
  }
  .card:hover { box-shadow: var(--shadow-hover); transform: translateY(-1px); }
  .card-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; }
  .card-code { font-size: 15px; font-weight: 700; color: var(--primary); white-space: nowrap; }
  .card-name { font-size: 15px; font-weight: 500; color: var(--text); flex: 1; }
  .card-cat { display: inline-block; padding: 2px 10px; border-radius: 10px; font-size: 12px; background: var(--primary-light); color: var(--primary); white-space: nowrap; }
  .card-date { font-size: 12px; color: var(--text-secondary); margin-top: 8px; }
  .card-actions { display: none; margin-top: 14px; padding-top: 14px; border-top: 1px solid var(--border); gap: 10px; flex-wrap: wrap; }
  .card.expanded .card-actions { display: flex; }
  .btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 18px; border-radius: 8px; font-size: 13px; font-weight: 500; text-decoration: none; cursor: pointer; border: 1px solid var(--border); background: var(--card-bg); color: var(--text); transition: all 0.15s; }
  .btn:hover { background: var(--primary-light); border-color: var(--primary); color: var(--primary); }
  .btn.primary { background: var(--primary); color: #fff; border-color: var(--primary); }
  .btn.primary:hover { background: #1557b0; }
  .btn:disabled { opacity: 0.4; pointer-events: none; }
  .expand-hint { font-size: 12px; color: var(--text-secondary); margin-top: 6px; }
  .empty { text-align: center; padding: 60px 20px; color: var(--text-secondary); }
  .empty .emoji { font-size: 48px; margin-bottom: 12px; }
  .empty p { font-size: 15px; }
  footer { text-align: center; padding: 32px 20px; font-size: 13px; color: var(--text-secondary); }
  @media (max-width: 600px) {
    header h1 { font-size: 22px; }
    .card-header { flex-direction: column; gap: 4px; }
    .card-code { font-size: 14px; }
    .card-name { font-size: 14px; }
  }
</style>
</head>
<body>
<header>
  <h1>水利规范文件检索</h1>
  <p>涵盖勘测、设计、施工、数字水利等领域 \u00b7 共 """ + str(len(specs)) + """ 部现行规范</p>
</header>
<div class="container">
  <div class="search-wrap">
    <span class="icon">搜索</span>
    <input type="text" id="search" placeholder="输入关键词搜索规范，如：测量、质量验收、数字孪生..." autocomplete="off">
  </div>
  <div class="stats">
    <span id="result-count">共 """ + str(len(specs)) + """ 部规范</span>
    <span style="cursor:pointer;color:var(--primary)" onclick="clearAll()">清除筛选</span>
  </div>
  <div class="tags" id="tags"></div>
  <div class="card-list" id="card-list"></div>
  <div class="empty" id="empty" style="display:none">
    <div class="emoji">无</div>
    <p>没有找到匹配的规范，试试其他关键词</p>
  </div>
</div>
<footer>
  <p>点击规范卡片展开查看详情 \u00b7 数据更新时间 2026.05</p>
</footer>
<script>
const specs = """ + specs_json + """;
const categories = """ + cats_json + """;
let activeCat = null;
let query = '';
function renderTags() {
  const tagsEl = document.getElementById('tags');
  let html = '<span class="tag' + (activeCat === null ? ' active' : '') + '" onclick="filterByCat(null)">全部<span class="count">' + specs.length + '</span></span>';
  categories.forEach(cat => {
    const count = specs.filter(s => s.cat === cat).length;
    html += '<span class="tag' + (activeCat === cat ? ' active' : '') + '" onclick="filterByCat(\"' + cat + '\")">' + cat + '<span class="count"> ' + count + '</span></span>';
  });
  tagsEl.innerHTML = html;
}
function filterByCat(cat) {
  activeCat = cat;
  query = document.getElementById('search').value.trim().toLowerCase();
  renderTags();
  renderCards();
}
function renderCards() {
  const listEl = document.getElementById('card-list');
  const emptyEl = document.getElementById('empty');
  const countEl = document.getElementById('result-count');
  let filtered = specs;
  if (activeCat !== null) { filtered = filtered.filter(s => s.cat === activeCat); }
  if (query) { filtered = filtered.filter(s => s.code.toLowerCase().includes(query) || s.name.includes(query)); }
  countEl.textContent = filtered.length === specs.length ? '\u5171 ' + specs.length + ' \u90e8\u89c4\u8303' : '\u627e\u5230 ' + filtered.length + ' \u90e8\u89c4\u8303';
  if (filtered.length === 0) { listEl.innerHTML = ''; emptyEl.style.display = 'block'; return; }
  emptyEl.style.display = 'none';
  let html = '';
  filtered.forEach(s => {
    html += '<div class="card" id="card-' + s.id + '" onclick="toggleCard(' + s.id + ')">';
    html += '<div class="card-header">';
    html += '<span class="card-code">' + s.code + '</span>';
    html += '<span class="card-name">' + s.name + '</span>';
    html += '<span class="card-cat">' + s.cat + '</span>';
    html += '</div>';
    html += '<div class="card-date">\u5b9e\u65bd\u65f6\u95f4\uff1a' + s.date + '</div>';
    html += '<div class="card-actions">';
    if (s.file) {
      html += '<a class="btn primary" href="viewer.html?file=' + encodeURIComponent(s.file) + '" target="_blank" onclick="event.stopPropagation()">\u5728\u7ebf\u6d4f\u89c8</a>';
      html += '<a class="btn" href="viewer.html?file=' + encodeURIComponent(s.file) + '" download onclick="event.stopPropagation()">\u4e0b\u8f7d PDF</a>';
    } else {
      html += '<span class="btn" disabled title="PDF \u6682\u672a\u4e0a\u4f20">\u5728\u7ebf\u6d4f\u89c8\uff08\u6682\u672a\u4e0a\u4f20\uff09</span>';
      html += '<span class="btn" disabled title="PDF \u6682\u672a\u4e0a\u4f20">\u4e0b\u8f7d\uff08\u6682\u672a\u4e0a\u4f20\uff09</span>';
    }
    html += '</div>';
    html += '<div class="expand-hint">\u70b9\u51fb\u5c55\u5f00\u67e5\u770b\u8be6\u60c5</div>';
    html += '</div>';
  });
  listEl.innerHTML = html;
}
function toggleCard(id) {
  document.getElementById('card-' + id).classList.toggle('expanded');
}
function clearAll() {
  activeCat = null;
  document.getElementById('search').value = '';
  query = '';
  renderTags();
  renderCards();
}
document.getElementById('search').addEventListener('input', function(e) {
  query = e.target.value.trim().toLowerCase();
  renderCards();
});
renderTags();
renderCards();
</script>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Done! " + str(len(specs)) + " specs, " + str(sum(1 for s in specs if s['file'])) + " with links.")