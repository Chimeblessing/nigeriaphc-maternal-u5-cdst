# app.py - MaternalU5 Early Warning Team
# Connects: WhatsApp Business + poe.com + render.com PostgreSQL + KoboToolbox + Dashboard

from flask import Flask, request, jsonify, render_template_string
import requests
import os
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# ========== CONFIG - Put your keys in render.com Environment Variables ==========
POE_API_KEY = os.getenv("POE_API_KEY")  # your poe.com API key
POE_BOT_NAME = os.getenv("POE_BOT_NAME", "maternalU5") # your bot on poe.com
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
DATABASE_URL = os.getenv("DATABASE_URL")  # from render.com PostgreSQL
KOBO_API_TOKEN = os.getenv("KOBO_API_TOKEN")
KOBO_FORM_ID = os.getenv("KOBO_FORM_ID") # your High & Low risk form

# ========== DATABASE HELPER ==========
def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS triage_logs (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP DEFAULT NOW(),
            state VARCHAR(50),
            lga VARCHAR(100),
            phc_name VARCHAR(100),
            mother_phone VARCHAR(20),
            user_message TEXT,
            poe_response TEXT,
            triage_color VARCHAR(20), -- RED, YELLOW, GREEN, HEAT, FLOOD, TRAUMA
            alert_type VARCHAR(50),
            source VARCHAR(20) DEFAULT 'WhatsApp'
        );
    """)
    conn.commit()
    conn.close()

init_db()

# ========== 1. POE.COM CALL - Gets color signs ==========
def call_poe_api(user_message):
    """
    Sends mother's message to poe.com and gets RED/YELLOW/GREEN classification
    """
    url = "https://api.poe.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {POE_API_KEY}",
        "Content-Type": "application/json"
    }
    # This prompt is what makes poe.com return colors
    system_prompt = """
    You are maternalU5 triage assistant. Classify every message into:
    🔴 RED = emergency: heavy bleeding, cord bleeding, convulsions, can't breathe, trauma physical violence
    🟡 YELLOW = need care within 24h: fever, diarrhea, vomiting, cough, mental trauma, fear
    🟢 GREEN = routine: immunization, family planning, normal
    Also add: HEAT ALERT if mentions hot weather, sun; FLOOD ALERT if mentions water enter house, flood
    Reply format: Start with emoji + COLOR + short Pidgin/English advice + 1-2 follow-up questions. Max 2 questions. Never prescribe dosage, say "CHEW will advise at PHC".
    """
    
    payload = {
        "model": POE_BOT_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=20)
        result = resp.json()
        text = result['choices'][0]['message']['content']
        
        # Extract color from response
        color = "GREEN"
        if "🔴" in text or "RED" in text: color = "RED"
        elif "🟡" in text or "YELLOW" in text: color = "YELLOW"
        if "HEAT" in text: color = "HEAT"
        if "FLOOD" in text: color = "FLOOD"
        
        return text, color
    except Exception as e:
        print(f"Poe API error: {e}")
        return "🟢 GREEN - Thank you, CHEW will advise at PHC.", "GREEN"

# ========== 2. SAVE TO KOBO TOOLBOX (High & Low Risk) ==========
def save_to_kobo(state, lga, phc, color, message, poe_response):
    """
    High Risk = RED, Low Risk = YELLOW/GREEN
    """
    try:
        kobo_url = f"https://kf.kobotoolbox.org/api/v2/assets/{KOBO_FORM_ID}/data/"
        headers = {"Authorization": f"Token {KOBO_API_TOKEN}"}
        
        risk_level = "High" if color == "RED" else "Low"
        payload = {
            "state": state,
            "lga": lga,
            "phc_name": phc,
            "risk_level": risk_level,
            "triage_color": color,
            "user_message": message,
            "ai_response": poe_response,
            "submission_time": datetime.now().isoformat()
        }
        requests.post(kobo_url, headers=headers, json=payload, timeout=10)
    except Exception as e:
        print(f"Kobo error: {e}")

# ========== 3. WHATSAPP WEBHOOK ==========
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # For Meta verification
        return request.args.get('hub.challenge')
    
    data = request.json
    try:
        # Extract message from WhatsApp
        entry = data['entry'][0]['changes'][0]['value']
        if 'messages' not in entry:
            return "ok", 200
            
        msg = entry['messages'][0]
        user_phone = msg['from']
        user_text = msg['text']['body']
        
        # Example: Determine PHC from phone (you can improve this)
        # For now default to Rivers - you will map phone to PHC in DB later
        state = "Rivers"  # or detect from user's profile
        lga = "Obio/Akpor"
        phc = "Rumuokoro PHC"
        
        # Call poe.com to get color
        poe_response, color = call_poe_api(user_text)
        
        # Save to PostgreSQL
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO triage_logs (state, lga, phc_name, mother_phone, user_message, poe_response, triage_color, alert_type)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (state, lga, phc, user_phone, user_text, poe_response, color, color))
        conn.commit()
        conn.close()
        
        # Save to Kobo
        save_to_kobo(state, lga, phc, color, user_text, poe_response)
        
        # Send back to WhatsApp with color signs
        send_whatsapp_message(user_phone, poe_response)
        
    except Exception as e:
        print(f"Webhook error: {e}")
    
    return "ok", 200

def send_whatsapp_message(to_phone, message):
    url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {"body": message}
    }
    requests.post(url, headers=headers, json=payload)

# ========== 4. DASHBOARD - Population Early Warning ==========
@app.route('/dashboard')
def dashboard():
    # Get filter
    state_filter = request.args.get('state', 'All')
    
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if state_filter == "All":
        cur.execute("SELECT * FROM triage_logs ORDER BY created_at DESC LIMIT 100")
    else:
        cur.execute("SELECT * FROM triage_logs WHERE state=%s ORDER BY created_at DESC LIMIT 100", (state_filter,))
    
    logs = cur.fetchall()
    
    # KPIs
    cur.execute("SELECT triage_color, COUNT(*) FROM triage_logs WHERE DATE(created_at)=CURRENT_DATE GROUP BY triage_color")
    kpis = {row['triage_color']: row['count'] for row in cur.fetchall()}
    
    conn.close()
    
    # Simple HTML dashboard - you can move to template later
    html = """
    <html>
    <head><title>maternalU5 Early Warning Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {font-family: Arial; margin:0; background:#f5f7fb}
        .header {background:#1a3a6e; color:white; padding:15px 25px}
        .kpis {display:flex; gap:15px; padding:20px; flex-wrap:wrap}
        .card {background:white; padding:15px; border-radius:10px; flex:1; min-width:150px; box-shadow:0 2px 5px #ddd; text-align:center}
        .red {color:red; font-size:32px; font-weight:bold} .yellow {color:orange; font-size:32px; font-weight:bold} .green {color:green; font-size:32px; font-weight:bold}
        table {width:95%; margin:20px; background:white; border-collapse:collapse}
        th, td {padding:10px; border:1px solid #ddd; text-align:left}
        .badge {padding:4px 8px; border-radius:5px; color:white; font-weight:bold}
        .RED {background:red} .YELLOW {background:orange} .GREEN {background:green} .FLOOD {background:#2a7de1} .HEAT {background:#ff6a00}
    </style>
    </head>
    <body>
        <div class="header">
            <h2>maternalU5 - Population Early Warning Dashboard | MaternalU5 Early Warning Team</h2>
            <div>Filter: <a href="/dashboard?state=All" style="color:white">All</a> | 
            <a href="/dashboard?state=Rivers" style="color:white">Rivers (2 LIVE + 9 PLANNED)</a> | 
            <a href="/dashboard?state=Enugu" style="color:white">Enugu (12 LIVE)</a> | Last updated: {{now}}</div>
        </div>
        <div class="kpis">
            <div class="card"><div>🔴 RED Today</div><div class="red">{{kpis.get('RED',0)}}</div></div>
            <div class="card"><div>🟡 YELLOW Today</div><div class="yellow">{{kpis.get('YELLOW',0)}}</div></div>
            <div class="card"><div>🟢 GREEN Today</div><div class="green">{{kpis.get('GREEN',0)}}</div></div>
            <div class="card"><div>HEAT ALERTS</div><div class="yellow">{{kpis.get('HEAT',0)}}</div></div>
            <div class="card"><div>FLOOD ALERTS</div><div class="red">{{kpis.get('FLOOD',0)}}</div></div>
        </div>
        <table>
            <tr><th>Time</th><th>State</th><th>LGA</th><th>PHC</th><th>Color (from poe.com)</th><th>Message</th><th>Poe Response</th></tr>
            {% for log in logs %}
            <tr>
                <td>{{log.created_at}}</td>
                <td>{{log.state}}</td>
                <td>{{log.lga}}</td>
                <td>{{log.phc_name}}</td>
                <td><span class="badge {{log.triage_color}}">{{log.triage_color}}</span></td>
                <td>{{log.user_message[:80]}}</td>
                <td>{{log.poe_response[:100]}}</td>
            </tr>
            {% endfor %}
        </table>
        <p style="margin:20px">Data source: PostgreSQL + KoboToolbox (High=RED, Low=YELLOW/GREEN) + poe.com colors | Team: MaternalU5 Early Warning Team | 14 LIVE PHCs (12 Enugu + 2 Rivers) + 9 PLANNED = 23 TOTAL</p>
    </body>
    </html>
    """
    from flask import render_template_string
    return render_template_string(html, logs=logs, kpis=kpis, now=datetime.now())

@app.route('/')
def home():
    return "maternalU5 API running - Team MaternalU5 Early Warning Team - Go to /dashboard"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    """
    HOW TO DEPLOY:
    1. Push this file to GitHub
    2. In render.com, connect GitHub repo
    3. Add Environment Variables: POE_API_KEY, WHATSAPP_TOKEN, DATABASE_URL, KOBO_API_TOKEN etc
    4. After deploy, your dashboard link = https://your-app-name.onrender.com/dashboard
    5. Set WhatsApp webhook to https://your-app-name.onrender.com/webhook
    """
