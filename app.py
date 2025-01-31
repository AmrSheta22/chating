from twilio.rest import Client
import time
from flask import Flask, render_template, request, jsonify

# Twilio credentials (replace with your actual credentials)
TWILIO_ACCOUNT_SID = "AC33e442b377fd63f21d97b017490e19ed"
TWILIO_AUTH_TOKEN = "77cd0f2a3020a68e5a5838c7f17266e7"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

# The specific number you want to allow
ALLOWED_SENDER = "whatsapp:+201282662987"


app = Flask(__name__)
# Initialize Twilio Client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

last_message = {"sid": None, "body": ""}

def get_latest_message():
    """Fetch the latest WhatsApp message from Twilio"""
    messages = client.messages.list(limit=5)  # Fetch recent messages
    for msg in messages:
        if msg.from_ == ALLOWED_SENDER and msg.direction == "inbound":
            return {"sid": msg.sid, "body": msg.body}
    return {"sid": None, "body": "No new messages"}

@app.route("/")
def index():
    """Serve the frontend HTML"""
    return render_template("index.html")

@app.route("/get_message", methods=["GET"])
def get_message():
    """API to fetch the latest message"""
    global last_message
    latest_msg = get_latest_message()
    
    if latest_msg["sid"] != last_message["sid"]:
        last_message = latest_msg  # Update last message
    
    return jsonify(last_message)

@app.route("/send_message", methods=["POST"])
def send_message():
    """API to send a reply"""
    data = request.get_json()
    reply_text = data.get("reply", "")

    if not reply_text:
        return jsonify({"status": "error", "message": "Reply text is empty"}), 400

    message = client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        to=ALLOWED_SENDER,
        body=reply_text
    )

    return jsonify({"status": "success", "message_sid": message.sid})

if __name__ == "__main__":
    app.run(debug=True)
