# main.py
import asyncio
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)
from importlib import import_module
from functools import wraps
import stripe
from config import TOKEN, STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY

RESPONSES = {
    "dm_error": "You can't use this bot in private chat.",
    "no_access": "Please purchase for access!",
    "error_occurred": "An error occurred. Admins have been notified",
}

# 🔹 Shared JSON file
ALLOWED_USERS_FILE = "allowed_users.json"

def load_allowed_users():
    if not os.path.exists(ALLOWED_USERS_FILE):
        return set()  # no file yet → return empty set
    with open(ALLOWED_USERS_FILE, "r") as f:
        try:
            data = f.read().strip()
            if not data:  # file exists but is empty
                return set()
            return set(json.loads(data))
        except json.JSONDecodeError:
            return set()  # corrupted or invalid → reset
        
def save_allowed_users(allowed_users):
    with open(ALLOWED_USERS_FILE, "w") as f:
        json.dump(list(allowed_users), f)

# Load on startup
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

# Helper functions
def has_access(user_id):
    # 🔹 Always re-load so new buyers get access instantly
    global ALLOWED_USER_IDS
    ALLOWED_USER_IDS = load_allowed_users()
    return user_id in ALLOWED_USER_IDS

def requires_start(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if "language" not in context.user_data:
            if update.message:
                await update.message.reply_text("Please use /start first to begin.")
            elif update.callback_query:
                await update.callback_query.answer()
                await update.callback_query.message.reply_text("Please use /start first to begin.")
            return
        return await func(update, context, *args, **kwargs)
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

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("English", callback_data="lang_en"),
            InlineKeyboardButton("Português", callback_data="lang_pt")
        ]
    ]
    lang = context.user_data.get("language", "en")
    await update.message.reply_text(
        TRANSLATIONS["welcome"][lang],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@requires_start
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("language", "en")
    await update.message.reply_text(TRANSLATIONS["help_menu"][lang], parse_mode='Markdown')

@requires_start
async def access_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = context.user_data.get("language", "en")
    if has_access(user_id):
        await update.message.reply_text(TRANSLATIONS["access_granted"][lang])
    else:
        await update.message.reply_text(RESPONSES["no_access"] if lang == "en" else "Por favor, compre para ter acesso!")

@requires_start
async def generate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = context.user_data.get("language", "en")
    if not has_access(user_id):
        await update.message.reply_text(RESPONSES["no_access"] if lang == "en" else "Por favor, compre para ter acesso!")
        return
    await update.message.reply_text(
        TRANSLATIONS["select_store"][lang],
        reply_markup=get_store_keyboard(page=0)
    )

@requires_start
async def payment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'Access Pass'},
                    'unit_amount': 500,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://yourdomain.com/payment-success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://yourdomain.com/payment-cancel',
            metadata={'telegram_user_id': str(user_id)},
        )
        PAYMENT_SESSIONS[session.id] = user_id
        await update.message.reply_text(
            f'Please complete your payment by clicking <a href="{session.url}">this link</a>.',
            parse_mode='HTML'
        )
    except Exception as e:
        await update.message.reply_text(f"Error creating payment session: {str(e)}")

# Callback handlers
async def language_selection_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("_")[1]
    context.user_data["language"] = lang
    await query.edit_message_text(TRANSLATIONS["language_set"][lang])

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if "language" not in context.user_data:
        await query.message.reply_text("Please use /start first to begin.")
        return

    data = query.data
    if data.startswith('store_'):
        store_key = data[6:]
        store_name = store_key.replace('_', ' ').upper()
        try:
            module = import_module(f"email_generators.{store_key}")
        except ModuleNotFoundError:
            await query.edit_message_text("Sorry, this store is not supported yet.")
            return
    elif data.startswith('page_'):
        page = int(data[5:])
        await query.edit_message_reply_markup(reply_markup=get_store_keyboard(page=page))

# Async main
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("access", access_command))
    app.add_handler(CommandHandler("generate", generate_command))
    app.add_handler(CommandHandler("payment", payment_command))
    app.add_handler(CallbackQueryHandler(language_selection_handler, pattern=r'^lang_'))
    app.add_handler(CallbackQueryHandler(button_handler, pattern=r'^(page_|store_)'))

    # Add ConversationHandlers dynamically for each store
    for store in STORE_LIST:
        store_key = store.lower().replace(" ", "_")
        try:
            module = import_module(f"email_generators.{store_key}")
        except ModuleNotFoundError:
            continue

        async def start_receipt_with_lang(update, context, _module=module):
            lang = context.user_data.get("language", "en")
            await _module.start_receipt(update, context, lang=lang)

        async def prompt_handler_with_lang(update, context, _module=module):
            lang = context.user_data.get("language", "en")
            await _module.prompt_handler(update, context, lang=lang)

        async def timeout_callback_with_lang(update, context, _module=module):
            lang = context.user_data.get("language", "en")
            await _module.timeout_callback(update, context, lang=lang)

        handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(start_receipt_with_lang, pattern=f'^store_{store_key}$')],
            states={module.PROMPT_ENUM[f'PROMPT_{i}']: [MessageHandler(filters.TEXT & ~filters.COMMAND, prompt_handler_with_lang)] for i in range(10)},
            fallbacks=[MessageHandler(filters.ALL, timeout_callback_with_lang)],
            conversation_timeout=60
        )
        app.add_handler(handler)

    print("Starting Telegram bot...")
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
