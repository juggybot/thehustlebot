# webhook_server.py
from flask import Flask, request, jsonify
import stripe
from config import STRIPE_API_KEY, STRIPE_WEBHOOK_SECRET
from main import ALLOWED_USER_IDS  # import from your bot file or use a DB

app = Flask(__name__)
stripe.api_key = STRIPE_API_KEY

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
                ALLOWED_USER_IDS.add(user_id)
                print(f"✅ Access granted for user: {user_id}")
            except ValueError:
                print("❌ Invalid user ID format.")

    return jsonify(success=True)
