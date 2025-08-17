import random
from config import EMAIL, PASSWORD
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from email.utils import formataddr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(sender_email, sender_password, recipient_email, subject, html_content):
    msg = MIMEMultipart()
    msg['From'] = formataddr((f'DIOR', sender_email))
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

# Generic multi-step input handler for any store
PROMPT_STATES = [f"PROMPT_{i}" for i in range(10)]
PROMPT_ENUM = {name: idx for idx, name in enumerate(PROMPT_STATES)}

prompts_en = [
    "Please enter the customer first name (Juggy):",
    "Please enter the image url (MUST BE FROM DIOR SITE):",
    "Please enter the product name (Dior Shoes):",
    "Please enter the product price (WITHOUT THE $ SIGN):",
    "Please enter the tax cost (WITHOUT THE $ SIGN):",
    "Please enter the order total (WITHOUT THE $ SIGN):",
    "Please enter the street address (123 Test Street):",
    "Please enter the suburb & postcode (Sydney, 2000):",
    "Please enter the country (Australia):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o primeiro nome do cliente (Juggy):",
    "Por favor, insira a URL da imagem (DEVE SER DO SITE DA DIOR):",
    "Por favor, insira o nome do produto (Sapatos Dior):",
    "Por favor, insira o preço do produto (SEM O SÍMBOLO $):",
    "Por favor, insira o valor do imposto (SEM O SÍMBOLO $):",
    "Por favor, insira o total do pedido (SEM O SÍMBOLO $):",
    "Por favor, insira o endereço (Rua Exemplo, 123):",
    "Por favor, insira o bairro e o CEP (São Paulo, 01000-000):",
    "Por favor, insira o país (Brasil):",
    "Por favor, insira a moeda ($/€/£):",
    "Qual endereço de e-mail deve receber este e-mail (juggyresells@gmail.com):"
]

RECEIPT_START = {
    "en": "Let's start your receipt generation!\n",
    "pt": "Vamos começar a geração do seu recibo!\n"
}
RECEIPT_DONE = {
    "en": "Receipt generated! Check your email...",
    "pt": "Recibo gerado! Verifique seu e-mail..."
}

def generate_order_number():
    part1 = random.randint(111111111, 999999999)  # Random 10-digit number

    # Combine the parts into order number
    order_number = f"{part1}"
    return order_number

async def start_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE, lang="en"):
    context.user_data['user_inputs'] = []
    msg = None
    if hasattr(update, 'message') and update.message: 
        msg = update.message
    elif hasattr(update, 'callback_query') and update.callback_query and update.callback_query.message:
        msg = update.callback_query.message
    prompts = prompts_pt if lang == "pt" else prompts_en
    if msg:
        await msg.reply_text(RECEIPT_START[lang] + prompts[0])
    return PROMPT_ENUM['PROMPT_0']

async def prompt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, lang="en"):
    user_inputs = context.user_data['user_inputs']
    user_inputs.append(update.message.text)
    prompts = prompts_pt if lang == "pt" else prompts_en
    if len(user_inputs) < len(prompts):
        await update.message.reply_text(prompts[len(user_inputs)])
        return PROMPT_ENUM[f'PROMPT_{len(user_inputs)}']
    # Final step: generate and send email
    await update.message.reply_text(RECEIPT_DONE[lang])
    order_num = generate_order_number()
    sender_email = EMAIL
    sender_password = PASSWORD
    recipient_email = f'{user_inputs[10]}'
    subject = f"Your order confirmation"
    html_template = f"""
            <html>

        <head>
            <meta charset="utf-8">
        </head>

        <body class="body" style="color: #000000">
            <table cellspacing="0" cellpadding="0" style="
                table-layout: fixed;
                border: 0;
                width: 100%;
                border-collapse: collapse;
                margin: 0 auto;
            ">
                <tbody>
                    <tr>
                        <td align="center">
                            <table cellspacing="0" cellpadding="0" style="width: 100%">
                                <tbody>
                                    <tr>
                                        <td>
                                            <table align="center" style="
                                width: 100%;
                                max-width: 600px;
                                padding: 32px 0;
                                text-align: center;
                                border: 0;
                                margin: 0 auto;
                            ">
                                                <tbody>
                                                    <tr>
                                                        <td>
                                                            <a href="https://www.dior.com/en_gb/beauty"><img width="106"
                                                                    height="31" alt="Logo Dior"
                                                                    src="https://www.dior.com/on/demandware.static/Sites-dior_gb-Site/-/default/dwcb8d8440/images/email/logo-dior.png"></a>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table cellspacing="0" cellpadding="0">
                                <tbody>
                                    <tr>
                                        <td>
                                            <table cellspacing="0" cellpadding="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="border: 0; text-align: center">
                                                            <div style="
                                        width: 100%;
                                        max-width: 600px;
                                        margin: 0 auto;
                                    ">
                                                                <img style="width: 100%"
                                                                    src="https://www.dior.com/on/demandware.static/Sites-dior_gb-Site/-/default/dw2cacc2e6/images/email/order-confirmation/order-confirmation-promo.jpg"
                                                                    alt="Thank you for the order"
                                                                    title="Thank you for the order">
                                                            </div>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table cellspacing="0" cellpadding="0" style="
                        width: 100%;
                        max-width: 600px;
                        padding: 32px 0 64px;
                        margin: 0 auto;
                        border-bottom: solid 1px #e5e5e5;
                    ">
                                <tbody>
                                    <tr>
                                        <td>
                                            <table style="
                                width: 100%;
                                max-width: 520px;
                                margin: 0 auto;
                                padding: 0 40px;
                            ">
                                                <tbody>
                                                    <tr>
                                                        <td>
                                                            <font
                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                style="
                                        font-family: 'CenturyGothic', 'Helvetica Neue',
                                        Helvetica, Arial, sans-serif;
                                    ">
                                                                <p style="
                                        margin: 0 0 16px;
                                        text-transform: uppercase;
                                        font-weight: 700;
                                        font-size: 16px;
                                        line-height: 24px;
                                        text-align: center;
                                        ">
                                                                    Thank you for your purchase
                                                                </p>
                                                                <p style="
                                        margin: 0 0 8px;
                                        font-weight: 400;
                                        font-size: 13px;
                                        line-height: 20px;
                                        text-align: center;
                                        ">
                                                                    Mr.
                                                                    {user_inputs[0]}
                                                                </p>
                                                                <p style="
                                        margin: 0 0 16px;
                                        font-weight: 400;
                                        font-size: 13px;
                                        line-height: 20px;
                                        text-align: center;
                                        ">
                                                                    This email confirms that your order:
                                                                    <b>{order_num}</b>
                                                                    is currently being processed.
                                                                </p>
                                                                <p style="
                                        color: #757575;
                                        margin: 0 0 16px;
                                        font-weight: 400;
                                        font-size: 13px;
                                        line-height: 20px;
                                        text-align: center;
                                        ">
                                                                    We'll notify you by email when your order has
                                                                    shipped. Your payment card will be charged once
                                                                    your order has been dispatched.
                                                                </p>
                                                                <p style="
                                        margin: 0;
                                        font-weight: 400;
                                        font-size: 13px;
                                        line-height: 20px;
                                        text-align: center;
                                        ">
                                                                    The Dior Online Boutique
                                                                </p>
                                                            </font>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table cellspacing="0" cellpadding="0" style="width: 100%; max-width: 600px; margin: 0 auto">
                                <tbody>
                                    <tr>
                                        <td style="padding: 64px 40px 24px">
                                            <table style="width: 100%">
                                                <tbody>
                                                    <tr>
                                                        <td style="padding: 0">
                                                            <font
                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                style="
                                        font-family: 'CenturyGothic', 'Helvetica Neue',
                                        Helvetica, Arial, sans-serif;
                                    ">
                                                                <span style="
                                        margin: 0;
                                        font-weight: 400;
                                        font-size: 13px;
                                        line-height: 20px;
                                        text-align: left;
                                        ">
                                                                    Order details:
                                                                    <b>{order_num}</b>
                                                                </span>
                                                            </font>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0 40px 24px">
                                            <table style="
                                width: 100%;
                                max-width: 520px;
                                border-bottom: solid 1px #e5e5e5;
                            ">
                                                <tbody>
                                                    <tr>
                                                        <td style="width: 60px; padding: 0 0 24px">
                                                            <img src="{user_inputs[1]}" alt="{user_inputs[2]}" width="100%" style="min-width: 120px; width: 100%">
                                                        </td>
                                                        <td align="left" style="padding: 0 20px 24px">
                                                            <font
                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                style="
                                        font-family: 'CenturyGothic', 'Helvetica Neue',
                                        Helvetica, Arial, sans-serif;
                                    ">
                                                                <p style="
                                        margin: 0 0 8px;
                                        font-weight: 700;
                                        font-size: 13px;
                                        line-height: 20px;
                                        ">
                                                                    {user_inputs[2]}
                                                                </p>
                                                            </font>
                                                        </td>
                                                        <td align="right" style="width: 80px; padding: 0 0 24px">
                                                            <font
                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                style="
                                        font-family: 'CenturyGothic', 'Helvetica Neue',
                                        Helvetica, Arial, sans-serif;
                                    ">
                                                                <p style="
                                        margin: 0;
                                        font-weight: 400;
                                        font-size: 13px;
                                        line-height: 20px;
                                        color: #757575;
                                        ">
                                                                    Qty: 1
                                                                </p>
                                                                <p style="
                                        margin: 0;
                                        font-weight: 700;
                                        font-size: 13px;
                                        line-height: 20px;
                                        ">
                                                                    {user_inputs[9]} {user_inputs[3]}
                                                                </p>
                                                            </font>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table cellspacing="0" cellpadding="0" style="width: 100%; max-width: 600px; margin: 0 auto">
                                <tbody>
                                    <tr>
                                        <td align="center" style="padding: 24px 40px 56px">
                                            <table style="
                                width: 100%;
                                max-width: 520px;
                                border: 0;
                                margin: 0 auto;
                                padding: 0;
                            ">
                                                <tbody></tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table cellspacing="0" cellpadding="0" style="
                        width: 100%;
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #f7f7f7;
                    ">
                                <tbody>
                                    <tr>
                                        <td align="center" style="padding: 32px 40px">
                                            <table style="width: 100%; max-width: 520px; margin: 0 auto">
                                                <tbody>
                                                    <!-- TO DO Promo section -->
                                                    <tr>
                                                        <td style="padding: 12px 0 0">
                                                            <table cellspacing="0" cellpadding="0"
                                                                style="width: 100%; border: 0; margin: 0 auto">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="padding: 0 0 12px">
                                                                            <font
                                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                style="
                                                font-family: 'CenturyGothic',
                                                'Helvetica Neue', Helvetica, Arial,
                                                sans-serif;
                                            ">
                                                                                <p style="
                                                margin: 0;
                                                font-weight: 400;
                                                font-size: 13px;
                                                line-height: 20px;
                                                ">
                                                                                    Subtotal
                                                                                </p>
                                                                            </font>
                                                                        </td>
                                                                        <td width="150" align="right" style="padding: 0 0 12px">
                                                                            <font
                                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                style="
                                                font-family: 'CenturyGothic',
                                                'Helvetica Neue', Helvetica, Arial,
                                                sans-serif;
                                            ">
                                                                                <p style="
                                                margin: 0;
                                                font-weight: 700;
                                                font-size: 13px;
                                                line-height: 20px;
                                                ">
                                                                                    {user_inputs[9]}
                                                                                    {user_inputs[3]}
                                                                                </p>
                                                                            </font>
                                                                        </td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td style="padding: 0 0 12px">
                                                                            <font
                                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                style="
                                                font-family: 'CenturyGothic',
                                                'Helvetica Neue', Helvetica, Arial,
                                                sans-serif;
                                            ">
                                                                                <p style="
                                                margin: 0;
                                                font-weight: 400;
                                                font-size: 13px;
                                                line-height: 20px;
                                                ">
                                                                                    DPD Next Day Delivery
                                                                                </p>
                                                                            </font>
                                                                        </td>
                                                                        <td width="150" align="right" style="padding: 0 0 12px">
                                                                            <font
                                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                style="
                                                font-family: 'CenturyGothic',
                                                'Helvetica Neue', Helvetica, Arial,
                                                sans-serif;
                                            ">
                                                                                <p style="
                                                margin: 0;
                                                font-weight: 700;
                                                font-size: 13px;
                                                line-height: 20px;
                                                ">
                                                                                    Free
                                                                                </p>
                                                                            </font>
                                                                        </td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td style="padding: 0 0 12px">
                                                                            <font
                                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                style="
                                                font-family: 'CenturyGothic',
                                                'Helvetica Neue', Helvetica, Arial,
                                                sans-serif;
                                            ">
                                                                                <p style="
                                                margin: 0;
                                                font-weight: 400;
                                                font-size: 13px;
                                                line-height: 20px;
                                                ">
                                                                                    Taxes
                                                                                </p>
                                                                            </font>
                                                                        </td>
                                                                        <td width="150" align="right" style="padding: 0 0 12px">
                                                                            <font
                                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                style="
                                                font-family: 'CenturyGothic',
                                                'Helvetica Neue', Helvetica, Arial,
                                                sans-serif;
                                            ">
                                                                                <p style="
                                                margin: 0;
                                                font-weight: 700;
                                                font-size: 13px;
                                                line-height: 20px;
                                                ">
                                                                                    {user_inputs[9]} {user_inputs[4]}
                                                                                </p>
                                                                            </font>
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>
                                                            <table cellspacing="0" cellpadding="0" style="
                                        width: 100%;
                                        border-top: solid 1px #e5e5e5;
                                        margin: 0 auto;
                                        padding: 12px 0 0;
                                    ">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="padding: 12px 0 0">
                                                                            <font
                                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                style="
                                                font-family: 'CenturyGothic',
                                                'Helvetica Neue', Helvetica, Arial,
                                                sans-serif;
                                            ">
                                                                                <p style="
                                                margin: 0 0 4px;
                                                text-transform: uppercase;
                                                font-weight: 700;
                                                font-size: 13px;
                                                line-height: 20px;
                                                ">
                                                                                    Total
                                                                                </p>
                                                                                <p style="
                                                margin: 0;
                                                font-weight: 400;
                                                font-size: 10px;
                                                line-height: 16px;
                                                color: #757575;
                                                ">
                                                                                    Total calculated after shipping method
                                                                                    and taxes
                                                                                </p>
                                                                            </font>
                                                                        </td>
                                                                        <td width="150" align="right" style="padding: 0 0 12px">
                                                                            <font
                                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                style="
                                                font-family: 'CenturyGothic',
                                                'Helvetica Neue', Helvetica, Arial,
                                                sans-serif;
                                            ">
                                                                                <p style="
                                                margin: 0;
                                                font-weight: 700;
                                                font-size: 13px;
                                                line-height: 20px;
                                                ">
                                                                                    {user_inputs[9]} {user_inputs[5]}
                                                                                </p>
                                                                            </font>
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table cellspacing="0" cellpadding="0" style="
                        width: 100%;
                        max-width: 600px;
                        margin: 0 auto;
                        border-bottom: solid 1px #e5e5e5;
                    ">
                                <tbody>
                                    <tr>
                                        <td style="padding: 64px 40px 52px">
                                            <table style="width: 100%; max-width: 520px; margin: 0 auto">
                                                <tbody>
                                                    <tr>
                                                        <td style="padding: 0 0 24px">
                                                            <font
                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                style="
                                        font-family: 'CenturyGothic', 'Helvetica Neue',
                                        Helvetica, Arial, sans-serif;
                                    ">
                                                                <p style="
                                        margin: 0;
                                        text-transform: uppercase;
                                        font-weight: 400;
                                        font-size: 13px;
                                        line-height: 20px;
                                        ">
                                                                    More about your order
                                                                </p>
                                                            </font>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                            <table style="width: 100%; max-width: 520px; margin: 0 auto">
                                                <tbody>
                                                    <tr>
                                                        <td style="padding: 0 0 12px">
                                                            <font
                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                style="
                                        font-family: 'CenturyGothic', 'Helvetica Neue',
                                        Helvetica, Arial, sans-serif;
                                    ">
                                                                <p style="
                                        margin: 0;
                                        font-weight: 700;
                                        font-size: 13px;
                                        line-height: 20px;
                                        ">
                                                                    Delivery address :
                                                                </p>
                                                                <p style="
                                        margin: 0;
                                        font-weight: 400;
                                        font-size: 13px;
                                        line-height: 20px;
                                        color: #757575;
                                        ">
                                                                    {user_inputs[6]}
                                                                    <br>
                                                                    {user_inputs[7]}
                                                                    <br>
                                                                    {user_inputs[8]}

                                                                </p>
                                                            </font>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                            <table style="width: 100%; max-width: 520px; margin: 0 auto">
                                                <tbody>
                                                    <tr>
                                                        <td style="padding: 0 0 12px">
                                                            <font
                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                style="
                                        font-family: 'CenturyGothic', 'Helvetica Neue',
                                        Helvetica, Arial, sans-serif;
                                    ">
                                                                <p style="
                                        margin: 0;
                                        font-weight: 700;
                                        font-size: 13px;
                                        line-height: 20px;
                                        ">
                                                                    Billing address :
                                                                </p>
                                                                <p style="
                                        margin: 0;
                                        font-weight: 400;
                                        font-size: 13px;
                                        line-height: 20px;
                                        color: #757575;
                                        ">
                                                                    {user_inputs[6]}
                                                                    <br>
                                                                    {user_inputs[7]}
                                                                    <br>
                                                                    {user_inputs[8]}
                                                                </p>
                                                            </font>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table cellpadding="0" cellspacing="0" style="
                        width: 100%;
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 0 20px;
                        border-bottom: solid 1px #e5e5e5;
                    ">
                                <tbody>
                                    <tr>
                                        <td style="padding: 64px 0">
                                            <table align="center" style="width: 100%; max-width: 560px; margin: 0 auto"
                                                valign="center">
                                                <tbody>
                                                    <tr>
                                                        <td style="padding: 0 0 16px">
                                                            <table align="center" style="margin: 0 auto" valign="center">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="padding: 0 18px 0">
                                                                            <img alt="Cart icon" height="20"
                                                                                src="https://www.dior.com/on/demandware.static/Sites-dior_gb-Site/-/default/dwa9f04a31/images/email/icons/cart.png"
                                                                                width="20">
                                                                        </td>
                                                                        <td style="padding: 0">
                                                                            <font
                                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                style="
                                                font-family: 'CenturyGothic',
                                                'Helvetica Neue', Helvetica, Arial,
                                                sans-serif;
                                            ">
                                                                                <span style="
                                                font-weight: 700;
                                                font-size: 13px;
                                                line-height: 20px;
                                                text-transform: uppercase;
                                                vertical-align: middle;
                                                ">
                                                                                    NEED ADVICE, HAVE A QUESTION ?
                                                                                </span>
                                                                            </font>
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td align="center">
                                                            <p style="
                                        margin: 0;
                                        font-weight: 400;
                                        font-size: 13px;
                                        line-height: 20px;
                                    ">
                                                                <font
                                                                    face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                    style="
                                        font-family: 'CenturyGothic', 'Helvetica Neue',
                                            Helvetica, Arial, sans-serif;
                                        ">
                                                                    You can contact the Dior Customer Service team
                                                                    by phone at +44 (0)20 7216 02 16 Monday to
                                                                    Friday 10am to 6pm or via email by filling in
                                                                    the &#x2018;Contact us&#x2019; form
                                                                    <a href="https://www.dior.com/en_gb/beauty/contact-parfum"
                                                                        style="
                                            color: #000000;
                                            font-weight: 400;
                                            font-size: 13px;
                                            line-height: 20px;
                                            text-decoration: underline;
                                        ">here</a>.
                                                                </font>
                                                            </p>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table cellspacing="0" cellpadding="0" style="
                        width: 100%;
                        max-width: 600px;
                        padding: 0 20px;
                        margin: 0 auto;
                        border-bottom: solid 1px #e5e5e5;
                    ">
                                <tbody>
                                    <tr>
                                        <td style="padding: 64px 0">
                                            <table valign="center" align="center"
                                                style="width: 100%; max-width: 560px; margin: 0 auto">
                                                <tbody>
                                                    <tr>
                                                        <td style="padding: 0 0 16px">
                                                            <table valign="center" align="center" style="margin: 0 auto">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="padding: 0 18px 0">
                                                                            <img width="20" height="20" alt="Cart icon"
                                                                                src="https://www.dior.com/on/demandware.static/Sites-dior_gb-Site/-/default/dwa9f04a31/images/email/icons/cart.png">
                                                                        </td>
                                                                        <td style="padding: 0">
                                                                            <font
                                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                style="
                                                font-family: 'CenturyGothic',
                                                'Helvetica Neue', Helvetica, Arial,
                                                sans-serif;
                                            ">
                                                                                <span style="
                                                font-weight: 700;
                                                font-size: 13px;
                                                line-height: 20px;
                                                text-transform: uppercase;
                                                vertical-align: middle;
                                                ">
                                                                                    Cancel or Refund
                                                                                </span>
                                                                            </font>
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td align="center">
                                                            <p style="
                                        margin: 0 0 8px;
                                        font-weight: 400;
                                        font-size: 13px;
                                        line-height: 20px;
                                    ">
                                                                <font
                                                                    face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                    style="
                                        font-family: 'CenturyGothic', 'Helvetica Neue',
                                            Helvetica, Arial, sans-serif;
                                        ">
                                                                    For assistance, please contact the
                                                                    <a href="https://www.dior.com/en_gb/beauty/contact-parfum"
                                                                        style="
                                            color: #000000;
                                            font-weight: 400;
                                            font-size: 13px;
                                            line-height: 20px;
                                            text-decoration: underline;
                                        ">
                                                                        Dior Customer Service
                                                                    </a>
                                                                </font>
                                                            </p>
                                                            <p style="
                                        margin: 0;
                                        font-weight: 400;
                                        font-size: 13px;
                                        line-height: 20px;
                                    ">
                                                                <font
                                                                    face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                    style="
                                        font-family: 'CenturyGothic', 'Helvetica Neue',
                                            Helvetica, Arial, sans-serif;
                                        ">
                                                                    <a href="https://www.dior.com/en_gb/beauty/folder?fid=legal-terms"
                                                                        style="
                                            color: #000000;
                                            font-weight: 400;
                                            font-size: 13px;
                                            line-height: 20px;
                                            text-decoration: underline;
                                        ">
                                                                        View the General Terms and Conditions of Sale
                                                                    </a>
                                                                </font>
                                                            </p>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table cellspacing="0" cellpadding="0" style="
                        width: 100%;
                        max-width: 600px;
                        padding: 0 20px;
                        margin: 0 auto;
                        border-bottom: solid 1px #e5e5e5;
                    " align="center">
                                <tbody>
                                    <tr>
                                        <td style="padding: 32px 0">
                                            <table style="
                                width: 100%;
                                max-width: 560px;
                                text-align: center;
                                border: 0;
                            " align="center">
                                                <tbody>
                                                    <tr>
                                                        <td>
                                                            <table style="
                                        width: 100%;
                                        padding: 0;
                                        text-align: center;
                                        border: 0;
                                        margin: 0 auto;
                                    " align="center">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="padding: 0 0 18px 0">
                                                                            <p style="
                                                margin: 0;
                                                text-transform: uppercase;
                                                font-weight: 700;
                                                font-size: 13px;
                                                line-height: 20px;
                                                text-align: center;
                                            ">
                                                                                <font
                                                                                    face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                    style="
                                                font-family: 'CenturyGothic',
                                                    'Helvetica Neue', Helvetica, Arial,
                                                    sans-serif;
                                                ">EXPLORE MORE
                                                                                </font>
                                                                            </p>
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="border: 0">
                                                            <table style="
                                        padding: 0;
                                        text-align: center;
                                        border: 0;
                                        margin: 0 auto;
                                    ">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="padding: 0 6px">
                                                                            <font
                                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                style="
                                                font-family: 'CenturyGothic',
                                                'Helvetica Neue', Helvetica, Arial,
                                                sans-serif;
                                            "><a href="https://www.dior.com/en_gb/beauty/womens-fragrance" style="
                                                color: #000000;
                                                font-weight: 400;
                                                font-size: 13px;
                                                line-height: 20px;
                                                text-transform: uppercase;
                                                text-decoration: none;
                                                ">Fragrance</a>
                                                                            </font>
                                                                        </td>
                                                                        <td style="padding: 0 6px">
                                                                            <font
                                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                style="
                                                font-family: 'CenturyGothic',
                                                'Helvetica Neue', Helvetica, Arial,
                                                sans-serif;
                                            "><a href="https://www.dior.com/en_gb/beauty/makeup" style="
                                                color: #000000;
                                                font-weight: 400;
                                                font-size: 13px;
                                                line-height: 20px;
                                                text-transform: uppercase;
                                                text-decoration: none;
                                                ">Makeup</a>
                                                                            </font>
                                                                        </td>
                                                                        <td style="padding: 0 6px">
                                                                            <font
                                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                style="
                                                font-family: 'CenturyGothic',
                                                'Helvetica Neue', Helvetica, Arial,
                                                sans-serif;
                                            "><a href="https://www.dior.com/en_gb/beauty/skincare-2" style="
                                                color: #000000;
                                                font-weight: 400;
                                                font-size: 13px;
                                                line-height: 20px;
                                                text-transform: uppercase;
                                                text-decoration: none;
                                                ">Skincare</a>
                                                                            </font>
                                                                        </td>
                                                                        <td style="padding: 0 6px">
                                                                            <font
                                                                                face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                style="
                                                font-family: 'CenturyGothic',
                                                'Helvetica Neue', Helvetica, Arial,
                                                sans-serif;
                                            "><a href="https://www.dior.com/en_gb/beauty/other/gifts" style="
                                                color: #000000;
                                                font-weight: 400;
                                                font-size: 13px;
                                                line-height: 20px;
                                                text-transform: uppercase;
                                                text-decoration: none;
                                                ">Gift</a>
                                                                            </font>
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table cellspacing="0" cellpadding="0" style="
                        width: 100%;
                        max-width: 600px;
                        padding: 0 20px;
                        margin: 0 auto;
                        border-bottom: solid 1px #e5e5e5;
                    ">
                                <tbody>
                                    <tr>
                                        <td style="padding: 32px 0">
                                            <table align="center" style="
                                width: 100%;
                                max-width: 560px;
                                text-align: center;
                                margin: 0 auto;
                            ">
                                                <tbody>
                                                    <tr>
                                                        <td>
                                                            <table style="
                                        width: 100%;
                                        padding: 0;
                                        text-align: center;
                                        border: 0;
                                        margin: 0;
                                    ">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="padding: 0 0 18px 0">
                                                                            <p style="
                                                margin: 0;
                                                text-transform: uppercase;
                                                font-weight: 700;
                                                font-size: 13px;
                                                line-height: 20px;
                                                text-align: center;
                                            ">
                                                                                <font
                                                                                    face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                    style="
                                                font-family: 'CenturyGothic',
                                                    'Helvetica Neue', Helvetica, Arial,
                                                    sans-serif;
                                                ">Our exclusive e-boutique services</font>
                                                                            </p>
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>
                                                            <table style="
                                        width: 100%;
                                        padding: 0;
                                        text-align: center;
                                        border: 0;
                                        margin: 0 auto;
                                    ">
                                                                <tbody>
                                                                    <tr>
                                                                        <td>
                                                                            <p style="
                                                margin: 0 0 4px;
                                                font-size: 0;
                                                line-height: 0;
                                            ">
                                                                                <img width="20" height="20" alt="Delivery icon"
                                                                                    src="https://www.dior.com/on/demandware.static/Sites-dior_gb-Site/-/default/dw97645abc/images/email/services/delivery.png">
                                                                            </p>
                                                                        </td>
                                                                        <td>
                                                                            <p style="
                                                margin: 0 0 4px;
                                                font-size: 0;
                                                line-height: 0;
                                            ">
                                                                                <img width="20" height="20" alt="Voyage icon"
                                                                                    src="https://www.dior.com/on/demandware.static/Sites-dior_gb-Site/-/default/dw74d29430/images/email/services/voyage.png">
                                                                            </p>
                                                                        </td>
                                                                        <td>
                                                                            <p style="
                                                margin: 0 0 4px;
                                                font-size: 0;
                                                line-height: 0;
                                            ">
                                                                                <img width="20" height="20" alt="Team icon"
                                                                                    src="https://www.dior.com/on/demandware.static/Sites-dior_gb-Site/-/default/dwa4e7bd51/images/email/services/team.png">
                                                                            </p>
                                                                        </td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td style="padding: 0 6px">
                                                                            <p style="
                                                color: #000000;
                                                font-weight: 400;
                                                font-size: 10px;
                                                line-height: 16px;
                                                margin: 0;
                                            ">
                                                                                <font
                                                                                    face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                    style="
                                                font-family: 'CenturyGothic',
                                                    'Helvetica Neue', Helvetica, Arial,
                                                    sans-serif;
                                                ">Free Delivery <br>
                                                                                    &amp; Return</font>
                                                                            </p>
                                                                        </td>
                                                                        <td style="padding: 0 6px">
                                                                            <p style="
                                                color: #000000;
                                                font-weight: 400;
                                                font-size: 10px;
                                                line-height: 16px;
                                                margin: 0;
                                            ">
                                                                                <font
                                                                                    face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                    style="
                                                font-family: 'CenturyGothic',
                                                    'Helvetica Neue', Helvetica, Arial,
                                                    sans-serif;
                                                ">Complimentary <br>
                                                                                    Travel Size</font>
                                                                            </p>
                                                                        </td>
                                                                        <td style="padding: 0 6px">
                                                                            <p style="
                                                color: #000000;
                                                font-weight: 400;
                                                font-size: 10px;
                                                line-height: 16px;
                                                margin: 0;
                                            ">
                                                                                <font
                                                                                    face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                    style="
                                                font-family: 'CenturyGothic',
                                                    'Helvetica Neue', Helvetica, Arial,
                                                    sans-serif;
                                                ">Art of <br>
                                                                                    Gifting</font>
                                                                            </p>
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table cellspacing="0" cellpadding="0" style="
                        width: 100%;
                        max-width: 600px;
                        padding: 0 20px;
                        margin: 0 auto;
                    ">
                                <tbody>
                                    <tr>
                                        <td style="padding: 32px 0 0">
                                            <table align="center" style="
                                width: 100%;
                                max-width: 520px;
                                text-align: center;
                                border: 0;
                                margin: 0 auto;
                                border-bottom: solid 1px #e5e5e5;
                            ">
                                                <tbody>
                                                    <tr>
                                                        <td>
                                                            <table valign="center" style="margin: 0 auto">
                                                                <tbody>
                                                                    <tr>
                                                                        <td valign="center" style="padding: 0 5px 32px">
                                                                            <p style="
                                                color: #000000;
                                                font-weight: 700;
                                                font-size: 13px;
                                                line-height: 20px;
                                                text-transform: uppercase;
                                                margin: 0;
                                            ">
                                                                                <font
                                                                                    face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                    style="
                                                font-family: 'CenturyGothic',
                                                    'Helvetica Neue', Helvetica, Arial,
                                                    sans-serif;
                                                ">Follow us
                                                                                </font>
                                                                            </p>
                                                                        </td>
                                                                        <td valign="center" style="padding: 0 5px 32px">
                                                                            <a href="https://www.facebook.com/Dior/"
                                                                                title="Facebook" style="
                                                text-decoration: none;
                                                padding: 5px;
                                            "><img width="20" height="20" alt="Facebook icon"
                                                                                    src="https://www.dior.com/on/demandware.static/Sites-dior_gb-Site/-/default/dw2d06f9d6/images/email/social/facebook.png"></a>
                                                                        </td>
                                                                        <td valign="center" style="padding: 0 5px 32px">
                                                                            <a href="https://www.instagram.com/dior/"
                                                                                title="Instagram" style="
                                                text-decoration: none;
                                                padding: 5px;
                                            "><img width="20" height="20" alt="Instagram icon"
                                                                                    src="https://www.dior.com/on/demandware.static/Sites-dior_gb-Site/-/default/dwb8bde51a/images/email/social/instagram.png"></a>
                                                                        </td>
                                                                        <td valign="center" style="padding: 0 5px 32px">
                                                                            <a href="https://www.youtube.com/dior/"
                                                                                title="YouTube" style="
                                                text-decoration: none;
                                                padding: 5px;
                                            "><img width="20" height="20" alt="Youtube icon"
                                                                                    src="https://www.dior.com/on/demandware.static/Sites-dior_gb-Site/-/default/dw75b6588c/images/email/social/youtube.png"></a>
                                                                        </td>
                                                                        <td valign="center" style="padding: 0 5px 32px">
                                                                            <a href="https://twitter.com/DIOR" title="Twitter"
                                                                                style="
                                                text-decoration: none;
                                                padding: 5px;
                                            "><img width="20" height="20" alt="Twitter icon"
                                                                                    src="https://www.dior.com/on/demandware.static/Sites-dior_gb-Site/-/default/dw8398848d/images/email/social/twitter.png"></a>
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table cellspacing="0" cellpadding="0" style="
                        width: 100%;
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 0 0 32px;
                    ">
                                <tbody>
                                    <tr>
                                        <td style="padding: 0 40px">
                                            <table align="left" style="
                                width: 100%;
                                max-width: 520px;
                                padding: 32px 0 20px;
                                margin: 0 auto;
                            ">
                                                <tbody>
                                                    <tr>
                                                        <td>
                                                            <p href="/" style="
                                        color: #000000;
                                        font-weight: 400;
                                        font-size: 10px;
                                        line-height: 18px;
                                        margin: 0;
                                    ">
                                                                <font
                                                                    face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                    style="
                                        font-family: 'CenturyGothic', 'Helvetica Neue',
                                            Helvetica, Arial, sans-serif;
                                        ">
                                                                    <a href="https://www.dior.com/en_gb/beauty/contact-parfum"
                                                                        style="
                                            color: #000000;
                                            text-decoration: underline;
                                        ">Contact us</a>
                                                                    <span style="margin: 0 5px">-</span>
                                                                    <a href="https://www.dior.com/en_gb/beauty/folder?fid=legal-terms"
                                                                        style="
                                            color: #000000;
                                            text-decoration: underline;
                                        ">Legal terms</a>
                                                                    <span style="margin: 0 5px">-</span>
                                                                    <a href="https://www.dior.com/en_gb/beauty/folder?fid=personal-data"
                                                                        style="
                                            color: #000000;
                                            text-decoration: underline;
                                        ">Privacy policy</a>
                                                                </font>
                                                            </p>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0 40px">
                                            <table cellspacing="0" cellpadding="0" style="
                                width: 100%;
                                max-width: 600px;
                                margin: 0 auto;
                                padding: 0 0 32px;
                            ">
                                                <tbody>
                                                    <tr>
                                                        <td>
                                                            <table style="
                                        width: 100%;
                                        max-width: 520px;
                                        margin: 0 auto;
                                    ">
                                                                <tbody>
                                                                    <tr>
                                                                        <td>
                                                                            <p style="
                                                color: #757575;
                                                font-weight: 400;
                                                font-size: 10px;
                                                line-height: 18px;
                                                margin: 0;
                                            ">
                                                                                <font
                                                                                    face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                    style="
                                                font-family: 'CenturyGothic',
                                                    'Helvetica Neue', Helvetica, Arial,
                                                    sans-serif;
                                                ">To be removed from future emailings,
                                                                                    please click
                                                                                    <a href="https://www.dior.com/on/demandware.store/Sites-dior_gb-Site/en_GB/Newsletter-Unsubscribe?token=p8L0dPJxhucPDfstnAiGNe5Aditj%2f7gz8ekuVuI4223H5QPcxkOojhZjZ6gu0KI3"
                                                                                        style="
                                                    color: #757575;
                                                    font-weight: 400;
                                                    font-size: 10px;
                                                    line-height: 18px;
                                                    text-decoration: underline;
                                                ">here</a>.
                                                                                </font>
                                                                            </p>
                                                                            <p style="
                                                color: #757575;
                                                font-weight: 400;
                                                font-size: 10px;
                                                line-height: 18px;
                                                margin: 0;
                                            ">
                                                                                <font
                                                                                    face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                    style="
                                                font-family: 'CenturyGothic',
                                                    'Helvetica Neue', Helvetica, Arial,
                                                    sans-serif;
                                                ">At Parfums Christian Dior, we take your
                                                                                    choices and the confidentiality of your
                                                                                    data seriously.</font>
                                                                            </p>
                                                                            <p style="
                                                color: #757575;
                                                font-weight: 400;
                                                font-size: 10px;
                                                line-height: 18px;
                                                margin: 0;
                                            ">
                                                                                <font
                                                                                    face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                    style="
                                                font-family: 'CenturyGothic',
                                                    'Helvetica Neue', Helvetica, Arial,
                                                    sans-serif;
                                                ">Please consult our privacy policy on
                                                                                    dior.com for all information concerning
                                                                                    the use of your personal data by Parfums
                                                                                    Christian Dior.</font>
                                                                            </p>
                                                                            <p style="
                                                color: #757575;
                                                font-weight: 400;
                                                font-size: 10px;
                                                line-height: 18px;
                                                margin: 0;
                                            ">
                                                                                <font
                                                                                    face="'CenturyGothic','Helvetica Neue',Helvetica,Arial,sans-serif"
                                                                                    style="
                                                font-family: 'CenturyGothic',
                                                    'Helvetica Neue', Helvetica, Arial,
                                                    sans-serif;
                                                ">In accordance with the applicable laws
                                                                                    and regulations, you have the right to
                                                                                    consult, modify and delete any data that
                                                                                    concerns you. You are also able to
                                                                                    request to no longer receive
                                                                                    personalised communications about our
                                                                                    products and services. You are able to
                                                                                    exercise this right at any time by
                                                                                    sending us an email to the following
                                                                                    address: contact@dior.com, or by
                                                                                    contacting our customer services
                                                                                    department at +44 (0)20 7216 02 16.
                                                                                </font>
                                                                            </p>
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
        </body>
        </html>
    """
    
    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
