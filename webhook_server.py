# webhook_server.py
from flask import Flask, request, jsonify
import stripe
import json
import os
from config import STRIPE_API_KEY, STRIPE_WEBHOOK_SECRET

app = Flask(__name__)
stripe.api_key = STRIPE_API_KEY

# Path to shared JSON file
ALLOWED_USERS_FILE = "allowed_users.json"

def load_allowed_users():
    """Load allowed users from JSON file"""
    if os.path.exists(ALLOWED_USERS_FILE):
        with open(ALLOWED_USERS_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_allowed_users(users):
    """Save allowed users to JSON file"""
    with open(ALLOWED_USERS_FILE, "w") as f:
        json.dump(list(users), f)

@app.route("/", methods=["GET"])
def home():
    return "✅ The HustleBot Webhook Server is Running"

@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        return f"Invalid payload: {str(e)}", 400
    except stripe.error.SignatureVerificationError as e:
        return f"Invalid signature: {str(e)}", 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        telegram_user_id = session['metadata'].get('telegram_user_id')
        if telegram_user_id:
            try:
                user_id = int(telegram_user_id)

                # Load -> Update -> Save
                allowed_users = load_allowed_users()
                allowed_users.add(user_id)
                save_allowed_users(allowed_users)

                print(f"✅ Access granted for user: {user_id}")
            except ValueError:
                print("❌ Invalid user ID format.")

    return jsonify(success=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
