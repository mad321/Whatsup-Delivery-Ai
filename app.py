import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = "MY_SECRET_VERIFY_TOKEN"  # رمز تحكم نختاره للربط مع ميتا
ACCESS_TOKEN = "EAAYuZCFMPNjgBSBACsxqqIZCcHFZBTP0rgqb5ObYDlD3Oq65xN0OxuyxPICS09fY1ZCQOOdKHBQhvcowrKFIKyewkMWffuSa9uEtO2A3ZAkNBZCTXgu2IBaEbfsAGXmPAuHDf8mFZANCU7XVhlMXckLNnI2GTZCkZCyj3p8QqdkdLkOQLmXBr4bQhV7Sdtz4dOBD6WZBSi4n37PmB2y3wZCuFoFZAfn3jRQz1tZAiv8cc4b69HzDk4pITNm4UlALv2tmWcWomZBKaHHWKN6JUbu4YypFrSUJzZC7JLJxrHe"   
PHONE_NUMBER_ID = "1147611041778282"  # معرف الرقم التجريبي

LOCATION_LINK = "https://maps.google.com/?q=24.7136,46.6753"  # ضع رابط موقع المنزل هنا
HOUSE_DETAILS = "مرحباً بك! تفاصيل الموقع كالتالي:\n- العنوان: الرياض\n- رابط الموقع: " + LOCATION_LINK

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Forbidden", 403
    return "Bad Request", 400

@app.route("/webhook", methods=["POST"])
def handle_messages():
    data = request.get_json()
    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        
        if "messages" in value:
            message = value["messages"][0]
            from_number = message["from"]
            send_whatsapp_message(from_number, HOUSE_DETAILS)
    except Exception as e:
        print(f"Error handling message: {e}")

    return jsonify({"status": "success"}), 200

def send_whatsapp_message(recipient, text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {"body": text}
    }
    requests.post(url, json=payload, headers=headers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
