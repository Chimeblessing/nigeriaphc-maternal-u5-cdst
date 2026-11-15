# app.py - MaternalU5 - Correct figures
# LIVE: 14 (12 Enugu + 2 Rivers) | PLANNED: 23 Rivers per LOI - separate

from flask import Flask, request, render_template
import requests, os, psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

app = Flask(__name__)

POE_API_KEY = os.getenv("POE_API_KEY")
POE_BOT_NAME = os.getenv("POE_BOT_NAME", "maternalU5")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
DATABASE_URL = os.getenv("DATABASE_URL")
KOBO_API_TOKEN = os.getenv("KOBO_API_TOKEN")
KOBO_FORM_ID = os.getenv("KOBO_FORM_ID")

def get_db():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_db(); cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS triage_logs (
        id SERIAL PRIMARY KEY, created_at TIMESTAMP DEFAULT NOW(),
        state VARCHAR(50), lga VARCHAR(100), phc_name VARCHAR(100),
        mother_phone VARCHAR(20), user_message TEXT, poe_response TEXT,
        triage_color VARCHAR(20), alert_type VARCHAR(50), source VARCHAR(20) DEFAULT 'WhatsApp'
    );""")
    conn.commit(); conn.close()
init_db()

def call_poe_api(msg):
    url="https://api.poe.com/v1/chat/completions"
    headers={"Authorization":f"Bearer {POE_API_KEY}","Content-Type":"application/json"}
    system_prompt="Classify: RED emergency, YELLOW 24h care, GREEN routine, plus HEAT/FLOOD. Reply: emoji + COLOR + Pidgin/English advice + max 2 questions. No dosage."
    try:
        r=requests.post(url,headers=headers,json={"model":POE_BOT_NAME,"messages":[{"role":"system","content":system_prompt},{"role":"user","content":msg}]},timeout=20)
        text=r.json()['choices'][0]['message']['content']
        color="GREEN"
        if "🔴" in text or "RED" in text: color="RED"
        elif "🟡" in text or "YELLOW" in text: color="YELLOW"
        if "HEAT" in text: color="HEAT"
        if "FLOOD" in text: color="FLOOD"
        return text,color
    except:
        return "🟢 GREEN - CHEW will advise at PHC","GREEN"

def save_to_kobo(state,lga,phc,color,msg,resp):
    try:
        url=f"https://kf.kobotoolbox.org/api/v2/assets/{KOBO_FORM_ID}/data/"
        headers={"Authorization":f"Token {KOBO_API_TOKEN}"}
        risk="High" if color=="RED" else "Low"
        requests.post(url,headers=headers,json={"state":state,"lga":lga,"phc_name":phc,"risk_level":risk,"triage_color":color,"user_message":msg,"ai_response":resp},timeout=10)
    except: pass

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method=='GET': return request.args.get('hub.challenge')
    data=request.json
    try:
        val=data['entry'][0]['changes'][0]['value']
        if 'messages' not in val: return "ok",200
        m=val['messages'][0]; phone=m['from']; text=m['text']['body']
        state="Rivers"; lga="Obio/Akpor"; phc="Rumuokoro PHC" # map phone to PHC in future
        poe_resp,color=call_poe_api(text)
        conn=get_db(); cur=conn.cursor()
        cur.execute("INSERT INTO triage_logs (state,lga,phc_name,mother_phone,user_message,poe_response,triage_color,alert_type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(state,lga,phc,phone,text,poe_resp,color,color))
        conn.commit(); conn.close()
        save_to_kobo(state,lga,phc,color,text,poe_resp)
        # send WhatsApp back
        requests.post(f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_ID}/messages",headers={"Authorization":f"Bearer {WHATSAPP_TOKEN}","Content-Type":"application/json"},json={"messaging_product":"whatsapp","to":phone,"type":"text","text":{"body":poe_resp}})
    except Exception as e: print(e)
    return "ok",200

@app.route('/dashboard')
def dashboard():
    state_filter=request.args.get('state','All')
    conn=get_db(); cur=conn.cursor(cursor_factory=RealDictCursor)
    if state_filter=='All':
        cur.execute("SELECT * FROM triage_logs ORDER BY created_at DESC LIMIT 100")
    else:
        cur.execute("SELECT * FROM triage_logs WHERE state=%s ORDER BY created_at DESC LIMIT 100",(state_filter,))
    logs=cur.fetchall()
    cur.execute("SELECT triage_color, COUNT(*) FROM triage_logs WHERE DATE(created_at)=CURRENT_DATE GROUP BY triage_color")
    kpis={r['triage_color']:r['count'] for r in cur.fetchall()}
    conn.close()
    return render_template('dashboard.html', logs=logs, kpis=kpis, now=datetime.now())

@app.route('/')
def home(): return "maternalU5 API running - LIVE 14 PHCs (12 Enugu + 2 Rivers) | PLANNED 23 Rivers per LOI"

if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
