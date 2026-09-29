import sqlite3
import threading
import time
from flask import Flask, request, jsonify, render_template_string, Response

app = Flask(__name__)
DB_FILE = "crew_logbook.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS routes (route_pair TEXT PRIMARY KEY, minutes INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS flights (id INTEGER PRIMARY KEY AUTOINCREMENT, flight_date TEXT, origin TEXT, destination TEXT, minutes INTEGER)''')
    default_routes = [
        ("THR-MHD", 75), ("MHD-THR", 80), ("THR-SYZ", 80), ("SYZ-THR", 80),
        ("THR-KIH", 105), ("KIH-THR", 105), ("THR-BND", 105), ("BND-THR", 110),
        ("MHD-BGW", 140), ("BGW-MHD", 135), ("THR-NJF", 110), ("NJF-THR", 105)
    ]
    c.executemany("INSERT OR IGNORE INTO routes (route_pair, minutes) VALUES (?, ?)", default_routes)
    conn.commit()
    conn.close()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AvaFix Flight Log</title>
  <style>
    :root { --bg: #070b14; --card: #0f172a; --border: #1e293b; --primary: #38bdf8; --accent: #f59e0b; --text: #f8fafc; --muted: #94a3b8; --danger: #ef4444; }
    * { box-sizing: border-box; margin:0; padding:0; }
    body { background: var(--bg); color: var(--text); font-family: -apple-system, Tahoma, sans-serif; padding-bottom: 50px; }
    header { background: #111e38; padding: 14px; text-align: center; border-bottom: 1px solid var(--border); }
    .brand { font-size: 1.15rem; font-weight: bold; color: var(--primary); }
    .container { max-width: 500px; margin: auto; padding: 12px; display: flex; flex-direction: column; gap: 14px; }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 14px; }
    .card-title { color: var(--primary); font-size: 0.95rem; font-weight: bold; margin-bottom: 12px; }
    .stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 6px; }
    .stat-box { background: #080e1a; border: 1px solid #1a2744; border-radius: 8px; padding: 10px; text-align: center; }
    .stat-label { font-size: 0.75rem; color: var(--muted); margin-bottom: 4px; }
    .stat-val { font-size: 1.1rem; font-weight: bold; font-family: monospace; color: var(--accent); }
    .form-group { display: flex; flex-direction: column; gap: 4px; margin-bottom: 10px; }
    label { font-size: 0.78rem; color: var(--muted); }
    input { background: #070d19; border: 1px solid #1a2744; color: #fff; padding: 10px; border-radius: 8px; font-size: 0.9rem; width: 100%; outline: none; }
    input:focus { border-color: var(--primary); }
    .route-row { display: grid; grid-template-columns: 1fr auto 1fr; gap: 8px; align-items: center; }
    .btn { background: var(--primary); color: #00121d; border: none; border-radius: 8px; padding: 11px; font-weight: bold; font-size: 0.9rem; width: 100%; cursor: pointer; }
    .btn-secondary { background: #1e293b; color: #cbd5e1; border: 1px solid #334155; }
    .flight-row { background: #070d19; border: 1px solid #1a2744; border-radius: 8px; padding: 10px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center; }
    .flight-route { font-family: monospace; font-weight: bold; color: #fff; }
    .flight-time { font-family: monospace; color: var(--accent); font-weight: bold; }
  </style>
</head>
<body>
<header>
  <div class="brand">✈️ AvaFix Flight Log</div>
  <div style="font-size:0.7rem; color:var(--muted); margin-top:2px;">نسخه اختصاصی کرو پروازی</div>
</header>
<div class="container">
  <div class="card">
    <div class="card-title">📊 وضعیت ساعات پرواز</div>
    <div class="stats-grid">
      <div class="stat-box"><div class="stat-label">ساعت ماه جاری</div><div id="monthHours" class="stat-val">۰۰:۰۰</div></div>
      <div class="stat-box"><div class="stat-label">لگ‌های ماه جاری</div><div id="monthLegs" class="stat-val" style="color:var(--primary);">۰</div></div>
      <div class="stat-box"><div class="stat-label">کل ساعت ثبت شده</div><div id="totalHours" class="stat-val">۰۰:۰۰</div></div>
      <div class="stat-box"><div class="stat-label">کل پروازها</div><div id="totalLegs" class="stat-val" style="color:var(--primary);">۰</div></div>
    </div>
  </div>
  <div class="card">
    <div class="card-title">📝 ثبت لگ پروازی جدید</div>
    <div class="form-group"><label>تاریخ پرواز (شمسی)</label><input id="dateInput" type="text" placeholder="۱۴۰۵/۰۷/۰۷"></div>
    <div class="route-row">
      <div class="form-group"><label>مبدأ</label><input id="origInput" type="text" placeholder="THR" maxlength="4" style="text-transform:uppercase;"></div>
      <span style="color:var(--primary); font-size:1.2rem;">➜</span>
      <div class="form-group"><label>مقصد</label><input id="destInput" type="text" placeholder="MHD" maxlength="4" style="text-transform:uppercase;"></div>
    </div>
    <div class="form-group"><label>مدت پرواز (ساعت:دقیقه یا دقیقه)</label><input id="durationInput" type="text" placeholder="مثال: 01:20 یا 80"></div>
    <button onclick="saveFlight()" class="btn">✈️ ذخیره در دیتابیس گوشی</button>
  </div>
  <div class="card">
    <div class="card-title">📑 خروجی اکسل</div>
    <div style="display:flex; gap:8px;">
      <input id="filterMonth" type="text" placeholder="ماه، مثال: ۱۴۰۵/۰۷">
      <button onclick="downloadCSV()" class="btn btn-secondary" style="width: auto; white-space:nowrap;">📥 دریافت اکسل</button>
    </div>
  </div>
  <div class="card"><div class="card-title">📜 پروازهای اخیر</div><div id="flightsList"></div></div>
</div>
<script>
  function formatMinutes(m){ return String(Math.floor(m/60)).padStart(2,'0') + ':' + String(m%60).padStart(2,'0'); }
  async function checkRoute(){
    const o=document.getElementById("origInput").value.trim().toUpperCase(), d=document.getElementById("destInput").value.trim().toUpperCase();
    if(o.length>=3 && d.length>=3){
      const res = await fetch(`/api/get_route_time?orig=${o}&dest=${d}`);
      const data = await res.json();
      if(data.minutes) document.getElementById("durationInput").value = formatMinutes(data.minutes);
    }
  }
  document.getElementById("origInput").addEventListener("input", checkRoute);
  document.getElementById("destInput").addEventListener("input", checkRoute);
  async function loadData(){
    const res = await fetch('/api/get_data');
    const data = await res.json();
    document.getElementById("totalHours").textContent = formatMinutes(data.stats.total_minutes);
    document.getElementById("totalLegs").textContent = data.stats.total_flights;
    document.getElementById("monthHours").textContent = formatMinutes(data.stats.month_minutes);
    document.getElementById("monthLegs").textContent = data.stats.month_flights;
    const list = document.getElementById("flightsList"); list.innerHTML = "";
    data.flights.forEach(f => {
      const row = document.createElement("div"); row.className = "flight-row";
      row.innerHTML = `<div><span style="font-size:0.75rem; color:var(--muted);">${f.date}</span><br><span class="flight-route">${f.origin} ✈️ ${f.destination}</span></div><div style="text-align:left;"><span class="flight-time">${formatMinutes(f.minutes)}</span><br><button onclick="deleteFlight(${f.id})" style="background:none; border:none; color:var(--danger); font-size:0.75rem; cursor:pointer;">حذف</button></div>`;
      list.appendChild(row);
    });
  }
  async function saveFlight(){
    const date=document.getElementById("dateInput").value.trim(), origin=document.getElementById("origInput").value.trim().toUpperCase(), destination=document.getElementById("destInput").value.trim().toUpperCase(), duration=document.getElementById("durationInput").value.trim();
    if(!date||!origin||!destination||!duration) return alert("تمامی فیلدها را کامل کنید");
    await fetch('/api/add_flight', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({date, origin, destination, duration})});
    document.getElementById("origInput").value=""; document.getElementById("destInput").value=""; document.getElementById("durationInput").value="";
    loadData();
  }
  async function deleteFlight(id){ if(confirm("حذف شود؟")){ await fetch(`/api/delete_flight?id=${id}`); loadData(); } }
  function downloadCSV(){ const m=document.getElementById("filterMonth").value.trim(); window.location.href=`/api/export_csv?month=${encodeURIComponent(m)}`; }
  document.getElementById("dateInput").value = new Intl.DateTimeFormat("fa-IR-u-ca-persian", {year:"numeric",month:"2-digit",day:"2-digit"}).format(new Date()).replace(/-/g,"/");
  loadData();
</script>
</body>
</html>
"""

@app.route("/")
def home(): return render_template_string(HTML_TEMPLATE)

@app.route("/api/get_route_time")
def get_route_time():
    orig, dest = request.args.get("orig", "").upper(), request.args.get("dest", "").upper()
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("SELECT minutes FROM routes WHERE route_pair = ?", (f"{orig}-{dest}",))
    row = c.fetchone(); conn.close()
    return jsonify({"minutes": row[0] if row else None})

@app.route("/api/add_flight", methods=["POST"])
def add_flight():
    data = request.json
    date, orig, dest, dur = data.get("date"), data.get("origin").upper(), data.get("destination").upper(), str(data.get("duration")).replace(".", ":")
    mins = int(dur.split(":")[0])*60 + int(dur.split(":")[1]) if ":" in dur else int(dur)
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("INSERT INTO flights (flight_date, origin, destination, minutes) VALUES (?, ?, ?, ?)", (date, orig, dest, mins))
    c.execute("INSERT OR IGNORE INTO routes (route_pair, minutes) VALUES (?, ?)", (f"{orig}-{dest}", mins))
    conn.commit(); conn.close()
    return jsonify({"status": "success"})

@app.route("/api/delete_flight")
def delete_flight():
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("DELETE FROM flights WHERE id = ?", (request.args.get("id"),))
    conn.commit(); conn.close()
    return jsonify({"status": "success"})

@app.route("/api/get_data")
def get_data():
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    c.execute("SELECT id, flight_date, origin, destination, minutes FROM flights ORDER BY id DESC")
    flights = [{"id": r[0], "date": r[1], "origin": r[2], "destination": r[3], "minutes": r[4]} for r in c.fetchall()]
    conn.close()
    cur_m = flights[0]["date"][:7] if flights else ""
    m_list = [f for f in flights if f["date"].startswith(cur_m)]
    return jsonify({
        "flights": flights[:15],
        "stats": {
            "total_minutes": sum(f["minutes"] for f in flights),
            "total_flights": len(flights),
            "month_minutes": sum(f["minutes"] for f in m_list),
            "month_flights": len(m_list)
        }
    })

@app.route("/api/export_csv")
def export_csv():
    m = request.args.get("month", "").strip()
    conn = sqlite3.connect(DB_FILE); c = conn.cursor()
    rows = c.execute("SELECT flight_date, origin, destination, minutes FROM flights WHERE flight_date LIKE ? ORDER BY id ASC", (f"{m}%",)).fetchall() if m else c.execute("SELECT flight_date, origin, destination, minutes FROM flights ORDER BY id ASC").fetchall()
    conn.close()
    csv_data = "\uFEFFDate,Origin,Destination,Minutes,Block_Time\\n" + "\\n".join([f"{r[0]},{r[1]},{r[2]},{r[3]},{r[3]//60:02d}:{r[3]%60:02d}" for r in rows])
    return Response(csv_data, mimetype="text/csv", headers={"Content-disposition": f"attachment; filename=Crew_Log.csv"})

if __name__ == "__main__":
    init_db()
    threading.Thread(target=lambda: app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False), daemon=True).start()
    
    # کنترل باز شدن در اندروید WebView
    try:
        from jnius import autoclass
        from android.runnable import run_on_ui_thread
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        
        @run_on_ui_thread
        def create_webview():
            activity = PythonActivity.mActivity
            webview = WebView(activity)
            webview.getSettings().setJavaScriptEnabled(True)
            webview.getSettings().setDomStorageEnabled(True)
            webview.setWebViewClient(WebViewClient())
            webview.loadUrl('http://127.0.0.1:5000')
            activity.setContentView(webview)
            
        create_webview()
        while True:
            time.sleep(1)
    except Exception:
        # برای تست محلی در دسکتاپ یا ترمینال
        app.run(host="0.0.0.0", port=5000)
