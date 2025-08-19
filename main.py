# bot_server.py
import os
import json
import stripe
from flask import Flask, request, jsonify
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
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

# ------------------ Telegram Setup ------------------
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, update_queue=None, use_context=True)

# ------------------ Bot Data ------------------
ALLOWED_USER_IDS = load_allowed_users()
PAYMENT_SESSIONS = {}

STORE_LIST = [
    "AMAZON", "APPLE", "ARCTERYX", "BALENCIAGA", "BEST BUY", "CANADA GOOSE",
    "CARTIER", "CHANEL", "DENIM TEARS", "DIOR", "DYSON", "EBAY", "FARFETCH",
    "FOOTLOCKER", "GLUE", "GOAT", "GRAILED", "GUCCI", "JD SPORTS", "LEGIT APP",
    "LEGO", "LOUIS VUITTON", "MONCLER", "MYER", "NIKE", "NORDSTROM", "NORTH FACE",
    "PANDORA", "PRADA", "RALPH LAUREN", "SAKS FIFTH AVENUE", "SAMSUNG", "SEPHORA",
    "SP5DER", "STANLEY", "STOCKX", "TARGET", "TRAPSTAR", "UGG", "VINTED", "ZALANDO"
]

TRANSLATIONS = {
    "language_set": {
        "en": "Language set to English.\nYou can now use /help or /generate.",
        "pt": "Idioma definido para Português.\nAgora você pode usar /help ou /generate."
    },
    "welcome": {
        "en": "Welcome to The Hustle Bot! Would you like to continue in English or Portuguese?",
        "pt": "Bem-vindo ao The Hustle Bot! Você gostaria de continuar em Inglês ou Português?"
    },
    "help_menu": {
        "en": "*HELP MENU*\n/access - Use this command to check if you have access!\n/generate - Use this command to start generating your receipt!\nProvided by The Hustle Bot",
        "pt": "*MENU DE AJUDA*\n/access - Use este comando para verificar se você tem acesso!\n/generate - Use este comando para começar a gerar seu recibo!\nFornecido por The Hustle Bot"
    },
    "access_granted": {
        "en": "YOU HAVE ACCESS\nUse /generate to get started!\nProvided by The Hustle Bot",
        "pt": "VOCÊ TEM ACESSO\nUse /generate para começar!\nFornecido por The Hustle Bot"
    },
    "select_store": {
        "en": "Please select a store to generate your receipt!",
        "pt": "Por favor, selecione uma loja para gerar seu recibo!"
    },
}

# ------------------ Helper Functions ------------------
def has_access(user_id):
    global ALLOWED_USER_IDS
    ALLOWED_USER_IDS = load_allowed_users()
    return user_id in ALLOWED_USER_IDS

def requires_start(func):
    @wraps(func)
    def wrapper(update, context, *args, **kwargs):
        if "language" not in getattr(context, 'user_data', {}):
            if hasattr(update, 'message') and update.message:
                update.message.reply_text("Please use /start first to begin.")
            elif hasattr(update, 'callback_query') and update.callback_query:
                update.callback_query.answer()
                update.callback_query.message.reply_text("Please use /start first to begin.")
            return
        return func(update, context, *args, **kwargs)
    return wrapper

def get_store_keyboard(page=0, items_per_page=10):
    start = page * items_per_page
    end = min(start + items_per_page, len(STORE_LIST))
    keyboard = [
        [InlineKeyboardButton(store, callback_data=f'store_{store.lower().replace(" ", "_")}')]
        for store in STORE_LIST[start:end]
    ]
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("Previous", callback_data=f'page_{page-1}'))
    if end < len(STORE_LIST):
        nav_buttons.append(InlineKeyboardButton("Next", callback_data=f'page_{page+1}'))
    if nav_buttons:
        keyboard.append(nav_buttons)
    return InlineKeyboardMarkup(keyboard)

# ------------------ Telegram Handlers ------------------
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("English", callback_data="lang_en"),
         InlineKeyboardButton("Português", callback_data="lang_pt")]
    ]
    lang = getattr(context, 'user_data', {}).get("language", "en")
    update.message.reply_text(TRANSLATIONS["welcome"][lang], reply_markup=InlineKeyboardMarkup(keyboard))

@requires_start
def help_command(update, context):
    lang = context.user_data.get("language", "en")
    update.message.reply_text(TRANSLATIONS["help_menu"][lang], parse_mode='Markdown')

@requires_start
def access_command(update, context):
    user_id = update.effective_user.id
    lang = context.user_data.get("language", "en")
    if has_access(user_id):
        update.message.reply_text(TRANSLATIONS["access_granted"][lang])
    else:
        update.message.reply_text("Please purchase for access!" if lang=="en" else "Por favor, compre para ter acesso!")

@requires_start
def generate_command(update, context):
    user_id = update.effective_user.id
    lang = context.user_data.get("language", "en")
    if not has_access(user_id):
        update.message.reply_text("Please purchase for access!" if lang=="en" else "Por favor, compre para ter acesso!")
        return
    update.message.reply_text(TRANSLATIONS["select_store"][lang], reply_markup=get_store_keyboard(page=0))

@requires_start
def payment_command(update, context):
    user_id = update.effective_user.id
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {'currency':'usd', 'product_data': {'name':'Access Pass'}, 'unit_amount':500},
            'quantity':1,
        }],
        mode='payment',
        success_url='https://yourdomain.com/payment-success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='https://yourdomain.com/payment-cancel',
        metadata={'telegram_user_id': str(user_id)}
    )
    PAYMENT_SESSIONS[session.id] = user_id
    update.message.reply_text(f'Please complete your payment: {session.url}')

def language_selection_handler(update, context):
    query = update.callback_query
    query.answer()
    lang = query.data.split("_")[1]
    context.user_data["language"] = lang
    query.edit_message_text(TRANSLATIONS["language_set"][lang])

def button_handler(update, context):
    query = update.callback_query
    query.answer()
    data = query.data
    if data.startswith('store_'):
        store_key = data[6:]
        try:
            module = import_module(f"email_generators.{store_key}")
        except ModuleNotFoundError:
            query.edit_message_text("Sorry, this store is not supported yet.")
            return
    elif data.startswith('page_'):
        page = int(data[5:])
        query.edit_message_reply_markup(reply_markup=get_store_keyboard(page=page))

# ------------------ Dispatcher Registration ------------------
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(CommandHandler("access", access_command))
dispatcher.add_handler(CommandHandler("generate", generate_command))
dispatcher.add_handler(CommandHandler("payment", payment_command))
dispatcher.add_handler(CallbackQueryHandler(language_selection_handler, pattern=r'^lang_'))
dispatcher.add_handler(CallbackQueryHandler(button_handler, pattern=r'^(page_|store_)'))

# ------------------ Flask Routes ------------------
@app.route("/", methods=["GET"])
def home():
    return "✅ The HustleBot Server is Running"

@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    dispatcher.process_update(update)
    return jsonify({"ok": True})

@app.route("/stripe-webhook", methods=["POST"])
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
            user_id = int(telegram_user_id)
            allowed_users = load_allowed_users()
            allowed_users.add(user_id)
            save_allowed_users(allowed_users)
            print(f"✅ Access granted for user: {user_id}")
    return jsonify(success=True)

# ------------------ Run ------------------
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
