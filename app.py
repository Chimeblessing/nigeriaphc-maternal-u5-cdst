import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "maternalU5_verify_123")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")

@app.route("/", methods=["GET"])
def home():
    return "MaternalU5 WhatsApp Bot is Running!", 200

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        if data and data.get("object") == "whatsapp_business_account":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    if messages:
                        for msg in messages:
                            from_number = msg.get("from")
                            text = msg.get("text", {}).get("body", "")
                            if from_number and text:
                                send_reply(from_number, f"Hello! Received: {text}. MaternalU5 Triage v1.3 is working for PHC!")
    except Exception as e:
        print(f"Error: {e}")
    return jsonify({"status": "ok"}), 200

def send_reply(to, text):
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
        print("Missing token or phone ID")
        return
    url = f"https://graph.facebook.com/v20.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": text}}
    try:
        r = requests.post(url, headers=headers, json=payload)
        print(f"Sent: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Send error: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
