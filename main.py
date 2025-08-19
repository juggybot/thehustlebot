# bot_server.py
import os
import json
import stripe
from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ConversationHandler, ContextTypes
)
from importlib import import_module
from functools import wraps
from config import TOKEN, STRIPE_API_KEY, STRIPE_WEBHOOK_SECRET

# ------------------ Flask Setup ------------------
app = Flask(__name__)

# ------------------ Stripe Setup ------------------
stripe.api_key = STRIPE_API_KEY
ALLOWED_USERS_FILE = "allowed_users.json"

def load_allowed_users():
    if os.path.exists(ALLOWED_USERS_FILE):
        with open(ALLOWED_USERS_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_allowed_users(users):
    with open(ALLOWED_USERS_FILE, "w") as f:
        json.dump(list(users), f)

ALLOWED_USER_IDS = load_allowed_users()
PAYMENT_SESSIONS = {}

STORE_LIST = ["AMAZON", "APPLE", "ARCTERYX", "BALENCIAGA"]  # truncated for brevity

TRANSLATIONS = {
    "language_set": {"en": "Language set to English.", "pt": "Idioma definido para Português."},
    "welcome": {"en": "Welcome! English or Portuguese?", "pt": "Bem-vindo! Inglês ou Português?"},
    "help_menu": {"en": "/access - check access\n/generate - generate receipt", "pt": "/access - verificar acesso\n/generate - gerar recibo"},
    "access_granted": {"en": "You have access!", "pt": "Você tem acesso!"},
    "select_store": {"en": "Select a store:", "pt": "Selecione uma loja:"}
}

# ------------------ Helper Functions ------------------
def has_access(user_id):
    global ALLOWED_USER_IDS
    ALLOWED_USER_IDS = load_allowed_users()
    return user_id in ALLOWED_USER_IDS

def requires_start(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if "language" not in context.user_data:
            if update.message:
                await update.message.reply_text("Please use /start first.")
            elif update.callback_query:
                await update.callback_query.answer()
                await update.callback_query.message.reply_text("Please use /start first.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def get_store_keyboard(page=0, items_per_page=10):
    start = page * items_per_page
    end = min(start + items_per_page, len(STORE_LIST))
    keyboard = [[InlineKeyboardButton(store, callback_data=f'store_{store.lower()}')] for store in STORE_LIST[start:end]]
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("Previous", callback_data=f'page_{page-1}'))
    if end < len(STORE_LIST):
        nav_buttons.append(InlineKeyboardButton("Next", callback_data=f'page_{page+1}'))
    if nav_buttons:
        keyboard.append(nav_buttons)
    return InlineKeyboardMarkup(keyboard)

# ------------------ Telegram Handlers ------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("English", callback_data="lang_en"),
                 InlineKeyboardButton("Português", callback_data="lang_pt")]]
    lang = context.user_data.get("language", "en")
    await update.message.reply_text(TRANSLATIONS["welcome"][lang], reply_markup=InlineKeyboardMarkup(keyboard))

@requires_start
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("language", "en")
    await update.message.reply_text(TRANSLATIONS["help_menu"][lang])

@requires_start
async def access_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = context.user_data.get("language", "en")
    if has_access(user_id):
        await update.message.reply_text(TRANSLATIONS["access_granted"][lang])
    else:
        await update.message.reply_text("Please purchase!" if lang=="en" else "Por favor, compre!")

@requires_start
async def generate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = context.user_data.get("language", "en")
    if not has_access(user_id):
        await update.message.reply_text("Please purchase!" if lang=="en" else "Por favor, compre!")
        return
    await update.message.reply_text(TRANSLATIONS["select_store"][lang], reply_markup=get_store_keyboard())

async def payment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{'price_data': {'currency':'usd','product_data':{'name':'Access Pass'},'unit_amount':500},'quantity':1}],
        mode='payment',
        success_url='https://yourdomain.com/payment-success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='https://yourdomain.com/payment-cancel',
        metadata={'telegram_user_id': str(user_id)}
    )
    PAYMENT_SESSIONS[session.id] = user_id
    await update.message.reply_text(f'Please complete your payment: {session.url}')

async def language_selection_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("_")[1]
    context.user_data["language"] = lang
    await query.edit_message_text(TRANSLATIONS["language_set"][lang])

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith('store_'):
        await query.edit_message_text(f"You selected: {data[6:].upper()}")
    elif data.startswith('page_'):
        page = int(data[5:])
        await query.edit_message_reply_markup(reply_markup=get_store_keyboard(page=page))

# ------------------ Flask Routes ------------------
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("access", access_command))
application.add_handler(CommandHandler("generate", generate_command))
application.add_handler(CommandHandler("payment", payment_command))
application.add_handler(CallbackQueryHandler(language_selection_handler, pattern=r'^lang_'))
application.add_handler(CallbackQueryHandler(button_handler, pattern=r'^(page_|store_)'))

@app.route("/", methods=["GET"])
def home():
    return "✅ HustleBot running"

@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot=application.bot)
    application.create_task(application.process_update(update))
    return jsonify({"ok": True})

@app.route("/stripe-webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except Exception as e:
        return f"Invalid webhook: {e}", 400
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        telegram_user_id = session['metadata'].get('telegram_user_id')
        if telegram_user_id:
            user_id = int(telegram_user_id)
            allowed_users = load_allowed_users()
            allowed_users.add(user_id)
            save_allowed_users(allowed_users)
            print(f"✅ Access granted for user {user_id}")
    return jsonify(success=True)

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
