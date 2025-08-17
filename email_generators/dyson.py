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
    msg['From'] = formataddr((f'Dyson', sender_email))
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
    "Please enter the customer name (Juggy Resells):",
    "Please enter the city & suburb (Manchester, Greater Manchester):",
    "Please enter the country & postcode (United Kingdom, SW1A 1AA):",
    "Please enter the image url (.jpg, .png, .jpeg):",
    "Please enter the item name (Dyson V15 Detect Absolute vacuum):",
    "Please enter the item price (WITHOUT THE $):",
    "Please enter the postage price (WITHOUT THE $):",
    "Please enter the tax amount (WITHOUT THE $):",
    "Please enter the order total (WITHOUT THE $):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira a cidade e o bairro (Manchester, Greater Manchester):",
    "Por favor, insira o país e o código postal (Reino Unido, SW1A 1AA):",
    "Por favor, insira a URL da imagem (.jpg, .png, .jpeg):",
    "Por favor, insira o nome do item (Aspirador Dyson V15 Detect Absolute):",
    "Por favor, insira o preço do item (SEM O $):",
    "Por favor, insira o valor do frete (SEM O $):",
    "Por favor, insira o valor do imposto (SEM O $):",
    "Por favor, insira o total do pedido (SEM O $):",
    "Por favor, insira a moeda ($/€/£):",
    "Qual endereço de e-mail você deseja receber este e-mail (juggyresells@gmail.com):"
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
    # Generate random order number
    part1 = random.randint(1000000000, 9999999999)  # Random 10-digit number

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
    subject = f"Order #{order_num} confirmed"
    html_template = f"""
    <html>
    <head></head>
    <body>
        <div dir="ltr">
            <table align="center" border="0" cellpadding="0" cellspacing="0" style="
                border-collapse: collapse;
                background: rgb(0, 0, 0);
                width: 1330.67px;
                ">
                <tbody>
                <tr>
                    <td style="border-collapse: collapse">
                        <div style="margin: 0px auto; max-width: 640px">
                            <table align="center" border="0" cellpadding="0" cellspacing="0"
                            style="border-collapse: collapse; width: 640px">
                            <tbody>
                                <tr>
                                    <td style="
                                        border-collapse: collapse;
                                        direction: ltr;
                                        font-size: 0px;
                                        padding: 0px;
                                        text-align: center;
                                        ">
                                        <div style="margin: 0px auto; max-width: 640px">
                                        <table align="center" border="0" cellpadding="0" cellspacing="0"
                                            style="border-collapse: collapse; width: 640px">
                                            <tbody>
                                                <tr>
                                                    <td style="
                                                    border-collapse: collapse;
                                                    direction: ltr;
                                                    padding: 20px 5px 3px;
                                                    ">
                                                    <div style="
                                                        max-width: 100%;
                                                        width: 630px;
                                                        line-height: 0;
                                                        text-align: left;
                                                        display: inline-block;
                                                        direction: ltr;
                                                        ">
                                                        <div style="
                                                            max-width: 32%;
                                                            width: 201.597px;
                                                            direction: ltr;
                                                            display: inline-block;
                                                            vertical-align: top;
                                                            ">
                                                            <table border="0" cellpadding="0"
                                                                cellspacing="0" width="100%"
                                                                style="border-collapse: collapse">
                                                                <tbody>
                                                                <tr>
                                                                    <td style="
                                                                        border-collapse: collapse;
                                                                        vertical-align: top;
                                                                        padding: 0px 0px 0px 15px;
                                                                        ">
                                                                        <table border="0"
                                                                            cellpadding="0"
                                                                            cellspacing="0" width="100%"
                                                                            style="border-collapse: collapse">
                                                                            <tbody>
                                                                            <tr>
                                                                                <td align="left"
                                                                                    style="
                                                                                    border-collapse: collapse;
                                                                                    padding: 0px 0px 10px;
                                                                                    word-break: break-word;
                                                                                    ">
                                                                                    <table
                                                                                        border="0"
                                                                                        cellpadding="0"
                                                                                        cellspacing="0"
                                                                                        style="
                                                                                        border-collapse: collapse;
                                                                                        border-spacing: 0px;
                                                                                        ">
                                                                                        <tbody>
                                                                                        <tr>
                                                                                            <td style="
                                                                                                border-collapse: collapse;
                                                                                                width: 70px;
                                                                                                ">
                                                                                                <a href="https://www.dyson.com/"
                                                                                                    target="_blank"><img
                                                                                                    alt=""
                                                                                                    height="27"
                                                                                                    src="https://dyson-h.assetsadobe2.com/is/image//content/dam/dyson/oe-team-email-assets/mjml-master-template-assets/dyson-logo-header-light-x2.png?scl=1&amp;fmt=png-alpha"
                                                                                                    width="70"
                                                                                                    class="gmail-CToWUd"
                                                                                                    style="
                                                                                                    border: 0px;
                                                                                                    height: 27px;
                                                                                                    line-height: 13px;
                                                                                                    outline: none;
                                                                                                    text-decoration-line: none;
                                                                                                    display: block;
                                                                                                    width: 70px;
                                                                                                    font-size: 13px;
                                                                                                    "></a>
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
                                                        </div>
                                                    </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                            </table>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" style="
                border-collapse: collapse;
                background: rgb(251, 251, 251);
                width: 1330.67px;
                ">
                <tbody>
                <tr>
                    <td style="border-collapse: collapse">
                        <div style="margin: 0px auto; max-width: 640px">
                            <table align="center" border="0" cellpadding="0" cellspacing="0"
                            style="border-collapse: collapse; width: 640px">
                            <tbody>
                                <tr>
                                    <td style="
                                        border-collapse: collapse;
                                        direction: ltr;
                                        font-size: 0px;
                                        padding: 0px;
                                        text-align: center;
                                        ">
                                        <div style="margin: 0px auto; max-width: 640px">
                                        <table align="center" border="0" cellpadding="0" cellspacing="0"
                                            style="border-collapse: collapse; width: 640px">
                                            <tbody>
                                                <tr>
                                                    <td style="
                                                    border-collapse: collapse;
                                                    direction: ltr;
                                                    padding: 15px 5px 0px;
                                                    ">
                                                    <div style="
                                                        max-width: 100%;
                                                        width: 630px;
                                                        text-align: left;
                                                        direction: ltr;
                                                        display: inline-block;
                                                        vertical-align: top;
                                                        ">
                                                        <table border="0" cellpadding="0" cellspacing="0"
                                                            width="100%" style="border-collapse: collapse">
                                                            <tbody>
                                                                <tr>
                                                                <td style="
                                                                    border-collapse: collapse;
                                                                    vertical-align: top;
                                                                    padding: 0px 15px 5px;
                                                                    ">
                                                                    <table border="0" cellpadding="0"
                                                                        cellspacing="0" width="100%"
                                                                        style="border-collapse: collapse">
                                                                        <tbody>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px 0px 10px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <div style="
                                                                                    font-family: DysonFutura,
                                                                                    Arial, Helvetica,
                                                                                    sans-serif;
                                                                                    font-size: 14px;
                                                                                    line-height: 18px;
                                                                                    color: rgb(51, 51, 51);
                                                                                    ">
                                                                                    Order number:
                                                                                    {order_num}
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                            </table>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" style="
                border-collapse: collapse;
                background-image: initial;
                background-position: initial;
                background-size: initial;
                background-repeat: initial;
                background-origin: initial;
                background-clip: initial;
                width: 1330.67px;
                ">
                <tbody>
                <tr>
                    <td style="border-collapse: collapse">
                        <div style="margin: 0px auto; max-width: 640px">
                            <table align="center" border="0" cellpadding="0" cellspacing="0"
                            style="border-collapse: collapse; width: 640px">
                            <tbody>
                                <tr>
                                    <td style="
                                        border-collapse: collapse;
                                        direction: ltr;
                                        font-size: 0px;
                                        padding: 0px;
                                        text-align: center;
                                        ">
                                        <div style="margin: 0px auto; max-width: 640px">
                                        <table align="center" border="0" cellpadding="0" cellspacing="0"
                                            style="border-collapse: collapse; width: 640px">
                                            <tbody>
                                                <tr>
                                                    <td style="
                                                    border-collapse: collapse;
                                                    direction: ltr;
                                                    padding: 30px 5px 0px;
                                                    ">
                                                    <div style="
                                                        max-width: 460px;
                                                        width: 460px;
                                                        text-align: left;
                                                        direction: ltr;
                                                        display: inline-block;
                                                        vertical-align: top;
                                                        ">
                                                        <table border="0" cellpadding="0" cellspacing="0"
                                                            width="100%" style="border-collapse: collapse">
                                                            <tbody>
                                                                <tr>
                                                                <td style="
                                                                    border-collapse: collapse;
                                                                    vertical-align: top;
                                                                    padding: 0px 15px 20px;
                                                                    ">
                                                                    <table border="0" cellpadding="0"
                                                                        cellspacing="0" width="100%"
                                                                        style="border-collapse: collapse">
                                                                        <tbody>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px 0px 20px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <div style="
                                                                                    font-family: DysonFutura,
                                                                                    Arial, Helvetica,
                                                                                    sans-serif;
                                                                                    font-size: 24px;
                                                                                    line-height: 30px;
                                                                                    color: rgb(51, 51, 51);
                                                                                    ">
                                                                                    Thank you! Your
                                                                                    order has been
                                                                                    placed
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px 0px 10px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <div style="
                                                                                    font-family: DysonFutura,
                                                                                    Arial, Helvetica,
                                                                                    sans-serif;
                                                                                    font-size: 14px;
                                                                                    line-height: 18px;
                                                                                    color: rgb(51, 51, 51);
                                                                                    ">
                                                                                    Please see your
                                                                                    order details
                                                                                    below. Your
                                                                                    order has been
                                                                                    placed and is
                                                                                    currently
                                                                                    processing. If
                                                                                    you have any
                                                                                    questions
                                                                                    regarding your
                                                                                    order, please
                                                                                    use the
                                                                                    &#x2018;Contact
                                                                                    us&#x2019;
                                                                                    button at the
                                                                                    bottom of
                                                                                    this email.
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                            </table>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" style="
                border-collapse: collapse;
                background: rgb(251, 251, 251);
                width: 1330.67px;
                ">
                <tbody>
                <tr>
                    <td style="border-collapse: collapse">
                        <div style="margin: 0px auto; max-width: 640px">
                            <table align="center" border="0" cellpadding="0" cellspacing="0"
                            style="border-collapse: collapse; width: 640px">
                            <tbody>
                                <tr>
                                    <td style="
                                        border-collapse: collapse;
                                        direction: ltr;
                                        font-size: 0px;
                                        padding: 0px;
                                        text-align: center;
                                        ">
                                        <div style="margin: 0px auto; max-width: 640px">
                                        <table align="center" border="0" cellpadding="0" cellspacing="0"
                                            style="border-collapse: collapse; width: 640px">
                                            <tbody>
                                                <tr>
                                                    <td style="
                                                    border-collapse: collapse;
                                                    direction: ltr;
                                                    padding: 30px 5px 0px;
                                                    ">
                                                    <div style="
                                                        max-width: 50%;
                                                        width: 315px;
                                                        text-align: left;
                                                        direction: ltr;
                                                        display: inline-block;
                                                        vertical-align: top;
                                                        ">
                                                        <table border="0" cellpadding="0" cellspacing="0"
                                                            width="100%" style="border-collapse: collapse">
                                                            <tbody>
                                                                <tr>
                                                                <td style="
                                                                    border-collapse: collapse;
                                                                    vertical-align: top;
                                                                    padding: 0px 15px 20px;
                                                                    ">
                                                                    <table border="0" cellpadding="0"
                                                                        cellspacing="0" width="100%"
                                                                        style="border-collapse: collapse">
                                                                        <tbody>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px 0px 10px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <div style="
                                                                                    font-family: DysonFutura,
                                                                                    Arial, Helvetica,
                                                                                    sans-serif;
                                                                                    font-size: 18px;
                                                                                    line-height: 24px;
                                                                                    color: rgb(51, 51, 51);
                                                                                    ">
                                                                                    Delivery address
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px 0px 10px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <div style="
                                                                                    font-family: DysonFutura,
                                                                                    Arial, Helvetica,
                                                                                    sans-serif;
                                                                                    font-size: 14px;
                                                                                    line-height: 18px;
                                                                                    color: rgb(51, 51, 51);
                                                                                    ">
                                                                                    <span style="
                                                                                        font-size: 10pt;
                                                                                        font-family: Arial;
                                                                                        ">{user_inputs[0]}
                                                                                    </span>
                                                                                </div>
                                                                                <div style="
                                                                                    line-height: 18px;
                                                                                    color: rgb(51, 51, 51);
                                                                                    ">
                                                                                    <font
                                                                                        face="Arial">
                                                                                    <span style="
                                                                                        font-size: 13.3333px;
                                                                                        "></span>
                                                                                    </font>
                                                                                </div>
                                                                                <div style="
                                                                                    line-height: 18px;
                                                                                    color: rgb(51, 51, 51);
                                                                                    ">
                                                                                    <span style="
                                                                                        font-family: Arial;
                                                                                        font-size: 10pt;
                                                                                        ">{user_inputs[1]}</span>
                                                                                </div>
                                                                                <div style="
                                                                                    line-height: 18px;
                                                                                    color: rgb(51, 51, 51);
                                                                                    ">
                                                                                    <font
                                                                                        face="Arial">
                                                                                    <span style="
                                                                                        font-size: 13.3333px;
                                                                                        "></span>
                                                                                    </font>
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                    <div style="
                                                        max-width: 50%;
                                                        width: 315px;
                                                        text-align: left;
                                                        direction: ltr;
                                                        display: inline-block;
                                                        vertical-align: top;
                                                        ">
                                                        <table border="0" cellpadding="0" cellspacing="0"
                                                            width="100%" style="border-collapse: collapse">
                                                            <tbody>
                                                                <tr>
                                                                <td style="
                                                                    border-collapse: collapse;
                                                                    vertical-align: top;
                                                                    padding: 0px 15px 20px;
                                                                    ">
                                                                    <table border="0" cellpadding="0"
                                                                        cellspacing="0" width="100%"
                                                                        style="border-collapse: collapse">
                                                                        <tbody>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px 0px 10px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <div style="
                                                                                    font-family: DysonFutura,
                                                                                    Arial, Helvetica,
                                                                                    sans-serif;
                                                                                    font-size: 18px;
                                                                                    line-height: 24px;
                                                                                    color: rgb(51, 51, 51);
                                                                                    ">
                                                                                    Billing address
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px 0px 10px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <div style="
                                                                                    font-family: DysonFutura,
                                                                                    Arial, Helvetica,
                                                                                    sans-serif;
                                                                                    font-size: 14px;
                                                                                    line-height: 18px;
                                                                                    color: rgb(51, 51, 51);
                                                                                    ">
                                                                                    <div
                                                                                        style="line-height: 18px">
                                                                                        <span style="
                                                                                        font-family: Arial;
                                                                                        font-size: 13.3333px;
                                                                                        ">{user_inputs[0]} </span><span style="
                                                                                        font-family: Arial;
                                                                                        font-size: 10pt;
                                                                                        ">
                                                                                        </span>
                                                                                    </div>
                                                                                    <div style="
                                                                                        font-family: Arial,
                                                                                        Helvetica, sans-serif;
                                                                                        font-size: 0px;
                                                                                        line-height: 18px;
                                                                                        ">
                                                                                        <span style="
                                                                                        font-family: Arial;
                                                                                        font-size: 13.3333px;
                                                                                        "></span>
                                                                                    </div>
                                                                                    <div style="
                                                                                        font-family: Arial,
                                                                                        Helvetica, sans-serif;
                                                                                        font-size: 0px;
                                                                                        line-height: 18px;
                                                                                        ">
                                                                                        <span style="
                                                                                        font-family: Arial;
                                                                                        font-size: 13.3333px;
                                                                                        ">{user_inputs[1]}</span>
                                                                                    </div>
                                                                                    <div style="
                                                                                        font-family: Arial,
                                                                                        Helvetica, sans-serif;
                                                                                        font-size: 0px;
                                                                                        line-height: 18px;
                                                                                        ">
                                                                                        <span style="
                                                                                        font-family: Arial;
                                                                                        font-size: 13.3333px;
                                                                                        ">{user_inputs[2]}</span>
                                                                                        \
                                                                                    </div>
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                            </table>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" style="
                border-collapse: collapse;
                background-image: initial;
                background-position: initial;
                background-size: initial;
                background-repeat: initial;
                background-origin: initial;
                background-clip: initial;
                width: 1330.67px;
                ">
                <tbody>
                <tr>
                    <td style="border-collapse: collapse">
                        <div style="margin: 0px auto; max-width: 640px">
                            <table align="center" border="0" cellpadding="0" cellspacing="0"
                            style="border-collapse: collapse; width: 640px">
                            <tbody>
                                <tr>
                                    <td style="
                                        border-collapse: collapse;
                                        direction: ltr;
                                        font-size: 0px;
                                        padding: 0px;
                                        text-align: center;
                                        ">
                                        <div style="margin: 0px auto; max-width: 640px">
                                        <table align="center" border="0" cellpadding="0" cellspacing="0"
                                            style="border-collapse: collapse; width: 640px">
                                            <tbody>
                                                <tr>
                                                    <td style="
                                                    border-collapse: collapse;
                                                    direction: ltr;
                                                    padding: 30px 5px 0px;
                                                    ">
                                                    <div style="
                                                        max-width: 100%;
                                                        width: 630px;
                                                        text-align: left;
                                                        direction: ltr;
                                                        display: inline-block;
                                                        vertical-align: top;
                                                        ">
                                                        <table border="0" cellpadding="0" cellspacing="0"
                                                            width="100%" style="border-collapse: collapse">
                                                            <tbody>
                                                                <tr>
                                                                <td style="
                                                                    border-collapse: collapse;
                                                                    vertical-align: top;
                                                                    padding: 0px 15px 20px;
                                                                    ">
                                                                    <table border="0" cellpadding="0"
                                                                        cellspacing="0" width="100%"
                                                                        style="border-collapse: collapse">
                                                                        <tbody>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <div style="
                                                                                    font-family: DysonFutura,
                                                                                    Arial, Helvetica,
                                                                                    sans-serif;
                                                                                    font-size: 21px;
                                                                                    line-height: 27px;
                                                                                    color: rgb(51, 51, 51);
                                                                                    ">
                                                                                    Your order
                                                                                    details
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                            </table>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" style="
                border-collapse: collapse;
                background-image: initial;
                background-position: initial;
                background-size: initial;
                background-repeat: initial;
                background-origin: initial;
                background-clip: initial;
                width: 1330.67px;
                ">
                <tbody>
                <tr>
                    <td style="border-collapse: collapse">
                        <div style="margin: 0px auto; max-width: 640px">
                            <table align="center" border="0" cellpadding="0" cellspacing="0"
                            style="border-collapse: collapse; width: 640px">
                            <tbody>
                                <tr>
                                    <td style="
                                        border-collapse: collapse;
                                        direction: ltr;
                                        font-size: 0px;
                                        padding: 5px 15px 0px;
                                        text-align: center;
                                        ">
                                        <div style="
                                        background: rgb(251, 251, 251);
                                        margin: 0px auto;
                                        max-width: 610px;
                                        ">
                                        <table align="center" border="0" cellpadding="0" cellspacing="0" style="
                                            border-collapse: collapse;
                                            background-image: initial;
                                            background-position: initial;
                                            background-size: initial;
                                            background-repeat: initial;
                                            background-origin: initial;
                                            background-clip: initial;
                                            width: 610px;
                                            ">
                                            <tbody>
                                                <tr>
                                                    <td style="
                                                    border-collapse: collapse;
                                                    direction: ltr;
                                                    padding: 30px 5px 0px;
                                                    ">
                                                    <div style="
                                                        max-width: 100%;
                                                        width: 600px;
                                                        line-height: 0;
                                                        text-align: left;
                                                        display: inline-block;
                                                        direction: ltr;
                                                        ">
                                                        <div style="
                                                            direction: ltr;
                                                            display: inline-block;
                                                            vertical-align: top;
                                                            width: 240px;
                                                            ">
                                                            <table border="0" cellpadding="0"
                                                                cellspacing="0" width="100%"
                                                                style="border-collapse: collapse">
                                                                <tbody>
                                                                <tr>
                                                                    <td style="
                                                                        border-collapse: collapse;
                                                                        vertical-align: top;
                                                                        padding: 0px;
                                                                        ">
                                                                        <table border="0"
                                                                            cellpadding="0"
                                                                            cellspacing="0" width="100%"
                                                                            style="border-collapse: collapse">
                                                                            <tbody>
                                                                            <tr>
                                                                                <td align="left"
                                                                                    style="
                                                                                    border-collapse: collapse;
                                                                                    padding: 0px;
                                                                                    word-break: break-word;
                                                                                    ">
                                                                                    <table
                                                                                        border="0"
                                                                                        cellpadding="0"
                                                                                        cellspacing="0"
                                                                                        style="
                                                                                        border-collapse: collapse;
                                                                                        border-spacing: 0px;
                                                                                        ">
                                                                                        <tbody>
                                                                                        <tr>
                                                                                            <td style="
                                                                                                border-collapse: collapse;
                                                                                                width: 235px;
                                                                                                "></td>
                                                                                        </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                    <img src="{user_inputs[3]}"
                                                                                        alt="image.png"
                                                                                        width="230"
                                                                                        class="gmail-CToWUd gmail-a6T"
                                                                                        tabindex="0"
                                                                                        style="
                                                                                        cursor: pointer;
                                                                                        outline: 0px;
                                                                                        margin-right: 0px;
                                                                                        ">
                                                                                    <div dir="ltr"
                                                                                        style="opacity: 0.01">
                                                                                        <div id="m_-1562170312633499073:219"
                                                                                        title="&#x41F;&#x43E;&#x438;&#x441;&#x43A; &#x432;&#x438;&#x440;&#x443;&#x441;&#x43E;&#x432;&#x2026;"
                                                                                        role="button"
                                                                                        aria-label="&#x421;&#x43A;&#x430;&#x447;&#x430;&#x442;&#x44C; &#x444;&#x430;&#x439;&#x43B; image.png">
                                                                                        <div>
                                                                                            <div>
                                                                                            </div>
                                                                                        </div>
                                                                                        </div>
                                                                                        <div id="m_-1562170312633499073:21a"
                                                                                        title="&#x414;&#x43E;&#x431;&#x430;&#x432;&#x438;&#x442;&#x44C; &#x43D;&#x430; &#x414;&#x438;&#x441;&#x43A;"
                                                                                        role="button"
                                                                                        aria-label="&#x414;&#x43E;&#x431;&#x430;&#x432;&#x438;&#x442;&#x44C; &#x444;&#x430;&#x439;&#x43B; &quot;image.png&quot; &#x43D;&#x430; &#x414;&#x438;&#x441;&#x43A;">
                                                                                        <div>
                                                                                            <div>
                                                                                                <div>
                                                                                                    <div>
                                                                                                    </div>
                                                                                                    <div>
                                                                                                    </div>
                                                                                                </div>
                                                                                            </div>
                                                                                        </div>
                                                                                        </div>
                                                                                        <div id="m_-1562170312633499073:21c"
                                                                                        role="button"
                                                                                        aria-label="&#x421;&#x43E;&#x445;&#x440;&#x430;&#x43D;&#x438;&#x442;&#x44C; &#x43A;&#x43E;&#x43F;&#x438;&#x44E; &#x432; &#x424;&#x43E;&#x442;&#x43E;">
                                                                                        <div>
                                                                                            <div>
                                                                                            </div>
                                                                                        </div>
                                                                                        </div>
                                                                                    </div>
                                                                                    <br>
                                                                                </td>
                                                                            </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                </tbody>
                                                            </table>
                                                        </div>
                                                        <div style="
                                                            direction: ltr;
                                                            display: inline-block;
                                                            vertical-align: top;
                                                            width: 360px;
                                                            ">
                                                            <table border="0" cellpadding="0"
                                                                cellspacing="0" width="100%"
                                                                style="border-collapse: collapse">
                                                                <tbody>
                                                                <tr>
                                                                    <td style="
                                                                        border-collapse: collapse;
                                                                        vertical-align: top;
                                                                        padding: 0px 15px 20px;
                                                                        ">
                                                                        <table border="0"
                                                                            cellpadding="0"
                                                                            cellspacing="0" width="100%"
                                                                            style="border-collapse: collapse">
                                                                            <tbody>
                                                                            <tr>
                                                                                <td align="left"
                                                                                    style="
                                                                                    border-collapse: collapse;
                                                                                    padding: 0px 0px 10px;
                                                                                    word-break: break-word;
                                                                                    ">
                                                                                    <div style="
                                                                                        font-family: DysonFutura,
                                                                                        Arial, Helvetica,
                                                                                        sans-serif;
                                                                                        font-size: 14px;
                                                                                        line-height: 18px;
                                                                                        color: rgb(51, 51, 51);
                                                                                        ">
                                                                                        {user_inputs[4]}
                                                                                    </div>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td align="left"
                                                                                    style="
                                                                                    border-collapse: collapse;
                                                                                    padding: 0px 0px 10px;
                                                                                    word-break: break-word;
                                                                                    ">
                                                                                    <div style="
                                                                                        font-family: DysonFutura,
                                                                                        Arial, Helvetica,
                                                                                        sans-serif;
                                                                                        font-size: 14px;
                                                                                        line-height: 18px;
                                                                                        color: rgb(153, 153, 153);
                                                                                        ">
                                                                                        Qty:
                                                                                        1
                                                                                    </div>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td align="left"
                                                                                    style="
                                                                                    border-collapse: collapse;
                                                                                    padding: 0px 0px 10px;
                                                                                    word-break: break-word;
                                                                                    ">
                                                                                    <div style="
                                                                                        font-family: DysonFutura,
                                                                                        Arial, Helvetica,
                                                                                        sans-serif;
                                                                                        font-size: 14px;
                                                                                        line-height: 18px;
                                                                                        color: rgb(51, 51, 51);
                                                                                        ">
                                                                                        Price:
                                                                                        {user_inputs[9]}
                                                                                        {user_inputs[5]}
                                                                                    </div>
                                                                                </td>
                                                                            </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                </tbody>
                                                            </table>
                                                        </div>
                                                    </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                            </table>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" style="
                border-collapse: collapse;
                background-image: initial;
                background-position: initial;
                background-size: initial;
                background-repeat: initial;
                background-origin: initial;
                background-clip: initial;
                width: 1330.67px;
                ">
                <tbody>
                <tr>
                    <td style="border-collapse: collapse">
                        <div style="margin: 0px auto; max-width: 640px">
                            <table align="center" border="0" cellpadding="0" cellspacing="0"
                            style="border-collapse: collapse; width: 640px">
                            <tbody>
                                <tr>
                                    <td style="
                                        border-collapse: collapse;
                                        direction: ltr;
                                        font-size: 0px;
                                        padding: 0px;
                                        text-align: center;
                                        ">
                                        <div style="margin: 0px auto; max-width: 640px">
                                        <table align="center" border="0" cellpadding="0" cellspacing="0"
                                            style="border-collapse: collapse; width: 640px">
                                            <tbody>
                                                <tr>
                                                    <td style="
                                                    border-collapse: collapse;
                                                    direction: ltr;
                                                    padding: 30px 5px 0px;
                                                    ">
                                                    <div style="
                                                        max-width: 100%;
                                                        width: 630px;
                                                        text-align: left;
                                                        direction: ltr;
                                                        display: inline-block;
                                                        vertical-align: top;
                                                        ">
                                                        <table border="0" cellpadding="0" cellspacing="0"
                                                            width="100%" style="border-collapse: collapse">
                                                            <tbody>
                                                                <tr>
                                                                <td style="
                                                                    border-collapse: collapse;
                                                                    vertical-align: top;
                                                                    padding: 0px 15px 20px;
                                                                    ">
                                                                    <table border="0" cellpadding="0"
                                                                        cellspacing="0" width="100%"
                                                                        style="border-collapse: collapse">
                                                                        <tbody>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px 0px 10px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <div style="
                                                                                    font-family: DysonFutura,
                                                                                    Arial, Helvetica,
                                                                                    sans-serif;
                                                                                    font-size: 11px;
                                                                                    line-height: 15px;
                                                                                    color: rgb(153, 153, 153);
                                                                                    ">
                                                                                    Payment will be
                                                                                    taken when the
                                                                                    order is
                                                                                    shipped.
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px 0px 10px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <div style="
                                                                                    font-family: DysonFutura,
                                                                                    Arial, Helvetica,
                                                                                    sans-serif;
                                                                                    font-size: 11px;
                                                                                    line-height: 15px;
                                                                                    color: rgb(153, 153, 153);
                                                                                    ">
                                                                                    PayPal payment
                                                                                    will be taken
                                                                                    at the time of
                                                                                    purchase.
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        </div>
                                        <div style="margin: 0px auto; max-width: 640px">
                                        <table align="center" border="0" cellpadding="0" cellspacing="0"
                                            style="border-collapse: collapse; width: 640px">
                                            <tbody>
                                                <tr>
                                                    <td style="
                                                    border-collapse: collapse;
                                                    direction: ltr;
                                                    padding: 10px 5px 0px;
                                                    ">
                                                    <div style="
                                                        max-width: 100%;
                                                        width: 630px;
                                                        line-height: 0;
                                                        text-align: left;
                                                        display: inline-block;
                                                        direction: ltr;
                                                        ">
                                                        <div style="
                                                            max-width: 50%;
                                                            width: 315px;
                                                            direction: ltr;
                                                            display: inline-block;
                                                            vertical-align: top;
                                                            ">
                                                            <table border="0" cellpadding="0"
                                                                cellspacing="0" width="100%"
                                                                style="border-collapse: collapse">
                                                                <tbody>
                                                                <tr>
                                                                    <td style="
                                                                        border-collapse: collapse;
                                                                        vertical-align: top;
                                                                        padding: 0px 15px 20px;
                                                                        ">
                                                                        <table border="0"
                                                                            cellpadding="0"
                                                                            cellspacing="0" width="100%"
                                                                            style="border-collapse: collapse">
                                                                            <tbody>
                                                                            <tr>
                                                                                <td align="left"
                                                                                    style="
                                                                                    border-collapse: collapse;
                                                                                    padding: 0px 0px 10px;
                                                                                    word-break: break-word;
                                                                                    ">
                                                                                    <div style="
                                                                                        font-family: DysonFutura,
                                                                                        Arial, Helvetica,
                                                                                        sans-serif;
                                                                                        font-size: 14px;
                                                                                        line-height: 18px;
                                                                                        color: rgb(153, 153, 153);
                                                                                        ">
                                                                                        Delivery:
                                                                                    </div>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="
                                                                                    border-collapse: collapse;
                                                                                    "></td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td align="left"
                                                                                    style="
                                                                                    border-collapse: collapse;
                                                                                    padding: 0px 0px 10px;
                                                                                    word-break: break-word;
                                                                                    ">
                                                                                    <div style="
                                                                                        font-family: DysonFutura,
                                                                                        Arial, Helvetica,
                                                                                        sans-serif;
                                                                                        font-size: 14px;
                                                                                        line-height: 18px;
                                                                                        color: rgb(153, 153, 153);
                                                                                        ">
                                                                                        Subtotal:
                                                                                    </div>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td align="left"
                                                                                    style="
                                                                                    border-collapse: collapse;
                                                                                    padding: 0px 0px 10px;
                                                                                    word-break: break-word;
                                                                                    ">
                                                                                    <div style="
                                                                                        font-family: DysonFutura,
                                                                                        Arial, Helvetica,
                                                                                        sans-serif;
                                                                                        font-size: 14px;
                                                                                        line-height: 18px;
                                                                                        color: rgb(153, 153, 153);
                                                                                        ">
                                                                                        Tax:
                                                                                    </div>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td align="left"
                                                                                    style="
                                                                                    border-collapse: collapse;
                                                                                    padding: 10px 0px;
                                                                                    word-break: break-word;
                                                                                    ">
                                                                                    <div style="
                                                                                        font-family: DysonFutura,
                                                                                        Arial, Helvetica,
                                                                                        sans-serif;
                                                                                        font-size: 18px;
                                                                                        line-height: 24px;
                                                                                        color: rgb(51, 51, 51);
                                                                                        ">
                                                                                        Order total
                                                                                        (inc. Tax):
                                                                                    </div>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td align="left"
                                                                                    style="
                                                                                    border-collapse: collapse;
                                                                                    padding: 0px 0px 10px;
                                                                                    word-break: break-word;
                                                                                    ">
                                                                                    <div style="
                                                                                        font-family: DysonFutura,
                                                                                        Arial, Helvetica,
                                                                                        sans-serif;
                                                                                        font-size: 14px;
                                                                                        line-height: 18px;
                                                                                        color: rgb(0, 102, 204);
                                                                                        ">
                                                                                        Discount:
                                                                                    </div>
                                                                                </td>
                                                                            </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                </tbody>
                                                            </table>
                                                        </div>
                                                        <div style="
                                                            max-width: 50%;
                                                            width: 315px;
                                                            direction: ltr;
                                                            display: inline-block;
                                                            vertical-align: top;
                                                            ">
                                                            <table border="0" cellpadding="0"
                                                                cellspacing="0" width="100%"
                                                                style="border-collapse: collapse">
                                                                <tbody>
                                                                <tr>
                                                                    <td style="
                                                                        border-collapse: collapse;
                                                                        vertical-align: top;
                                                                        padding: 0px 15px 20px;
                                                                        ">
                                                                        <table border="0"
                                                                            cellpadding="0"
                                                                            cellspacing="0" width="100%"
                                                                            style="border-collapse: collapse">
                                                                            <tbody>
                                                                            <tr>
                                                                                <td align="right"
                                                                                    style="
                                                                                    border-collapse: collapse;
                                                                                    padding: 0px 0px 10px;
                                                                                    word-break: break-word;
                                                                                    ">
                                                                                    <div style="
                                                                                        font-family: DysonFutura,
                                                                                        Arial, Helvetica,
                                                                                        sans-serif;
                                                                                        font-size: 14px;
                                                                                        line-height: 18px;
                                                                                        color: rgb(153, 153, 153);
                                                                                        ">
                                                                                        {user_inputs[9]}
                                                                                        {user_inputs[6]}
                                                                                    </div>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td align="right"
                                                                                    style="
                                                                                    border-collapse: collapse;
                                                                                    padding: 0px 0px 10px;
                                                                                    word-break: break-word;
                                                                                    ">
                                                                                    <div style="
                                                                                        font-family: DysonFutura,
                                                                                        Arial, Helvetica,
                                                                                        sans-serif;
                                                                                        font-size: 14px;
                                                                                        line-height: 18px;
                                                                                        color: rgb(153, 153, 153);
                                                                                        ">
                                                                                        {user_inputs[9]}
                                                                                        {user_inputs[5]}
                                                                                    </div>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td align="right"
                                                                                    style="
                                                                                    border-collapse: collapse;
                                                                                    padding: 0px 0px 10px;
                                                                                    word-break: break-word;
                                                                                    ">
                                                                                    <div style="
                                                                                        font-family: DysonFutura,
                                                                                        Arial, Helvetica,
                                                                                        sans-serif;
                                                                                        font-size: 14px;
                                                                                        line-height: 18px;
                                                                                        color: rgb(153, 153, 153);
                                                                                        ">
                                                                                        {user_inputs[9]}
                                                                                        {user_inputs[7]}
                                                                                    </div>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td align="right"
                                                                                    style="
                                                                                    border-collapse: collapse;
                                                                                    padding: 10px 0px;
                                                                                    word-break: break-word;
                                                                                    ">
                                                                                    <div style="
                                                                                        font-family: DysonFutura,
                                                                                        Arial, Helvetica,
                                                                                        sans-serif;
                                                                                        font-size: 18px;
                                                                                        line-height: 24px;
                                                                                        color: rgb(51, 51, 51);
                                                                                        ">
                                                                                        {user_inputs[9]}
                                                                                        {user_inputs[8]}
                                                                                    </div>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td align="right"
                                                                                    style="
                                                                                    border-collapse: collapse;
                                                                                    padding: 0px 0px 10px;
                                                                                    word-break: break-word;
                                                                                    ">
                                                                                    <div style="
                                                                                        font-family: DysonFutura,
                                                                                        Arial, Helvetica,
                                                                                        sans-serif;
                                                                                        font-size: 14px;
                                                                                        line-height: 18px;
                                                                                        color: rgb(0, 102, 204);
                                                                                        ">
                                                                                        {user_inputs[9]}
                                                                                        0.00
                                                                                    </div>
                                                                                </td>
                                                                            </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                </tbody>
                                                            </table>
                                                        </div>
                                                    </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                            </table>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" style="
                border-collapse: collapse;
                background-image: initial;
                background-position: initial;
                background-size: initial;
                background-repeat: initial;
                background-origin: initial;
                background-clip: initial;
                width: 1330.67px;
                ">
                <tbody>
                <tr>
                    <td style="border-collapse: collapse">
                        <div style="margin: 0px auto; max-width: 640px">
                            <table align="center" border="0" cellpadding="0" cellspacing="0"
                            style="border-collapse: collapse; width: 640px">
                            <tbody>
                                <tr>
                                    <td style="
                                        border-collapse: collapse;
                                        direction: ltr;
                                        font-size: 0px;
                                        padding: 0px;
                                        text-align: center;
                                        ">
                                        <div style="margin: 0px auto; max-width: 640px">
                                        <table align="center" border="0" cellpadding="0" cellspacing="0"
                                            style="border-collapse: collapse; width: 640px">
                                            <tbody>
                                                <tr>
                                                    <td style="
                                                    border-collapse: collapse;
                                                    direction: ltr;
                                                    padding: 0px 5px;
                                                    ">
                                                    <div style="
                                                        max-width: 100%;
                                                        width: 630px;
                                                        text-align: left;
                                                        direction: ltr;
                                                        display: inline-block;
                                                        vertical-align: top;
                                                        ">
                                                        <table border="0" cellpadding="0" cellspacing="0"
                                                            width="100%" style="border-collapse: collapse">
                                                            <tbody>
                                                                <tr>
                                                                <td style="
                                                                    border-collapse: collapse;
                                                                    vertical-align: top;
                                                                    padding: 0px 15px 20px;
                                                                    ">
                                                                    <table border="0" cellpadding="0"
                                                                        cellspacing="0" width="100%"
                                                                        style="border-collapse: collapse">
                                                                        <tbody>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px 0px 10px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <div style="
                                                                                    font-family: DysonFutura,
                                                                                    Arial, Helvetica,
                                                                                    sans-serif;
                                                                                    font-size: 11px;
                                                                                    line-height: 15px;
                                                                                    color: rgb(51, 51, 51);
                                                                                    ">
                                                                                    Once an order
                                                                                    has been placed,
                                                                                    it cannot be
                                                                                    amended. Dyson
                                                                                    gladly accepts
                                                                                    returns in
                                                                                    accordance to
                                                                                    the
                                                                                    <a href="https://www.dyson.com/inside-dyson/terms/returns-policy.html"
                                                                                        target="_blank"
                                                                                        style="
                                                                                        color: rgb(102, 102, 102);
                                                                                        ">Dyson Store Returns
                                                                                    Policy</a>.
                                                                                    Please visit our
                                                                                    <a href="https://www.dyson.com/inside-dyson/terms/returns-policy.html"
                                                                                        target="_blank"
                                                                                        style="
                                                                                        color: rgb(102, 102, 102);
                                                                                        ">returns page</a>
                                                                                    for more
                                                                                    information or
                                                                                    to
                                                                                    begin the return
                                                                                    process.
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px 0px 10px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <div style="
                                                                                    font-family: DysonFutura,
                                                                                    Arial, Helvetica,
                                                                                    sans-serif;
                                                                                    font-size: 11px;
                                                                                    line-height: 15px;
                                                                                    color: rgb(51, 51, 51);
                                                                                    ">
                                                                                    Refurbished
                                                                                    machines as well
                                                                                    as tools, parts
                                                                                    and
                                                                                    accessories will
                                                                                    ship
                                                                                    separately and
                                                                                    will be
                                                                                    delivered within
                                                                                    5-7 business
                                                                                    days.
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px 0px 10px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <div style="
                                                                                    font-family: DysonFutura,
                                                                                    Arial, Helvetica,
                                                                                    sans-serif;
                                                                                    font-size: 11px;
                                                                                    line-height: 15px;
                                                                                    color: rgb(51, 51, 51);
                                                                                    ">
                                                                                    Get the most out
                                                                                    of your
                                                                                    machine by
                                                                                    signing up for
                                                                                    maintenance
                                                                                    reminders and
                                                                                    special offers
                                                                                    when you update
                                                                                    your preferences
                                                                                    on
                                                                                    <a href="https://www.dyson.com/your-dyson.html"
                                                                                        target="_blank"
                                                                                        style="
                                                                                        color: rgb(102, 102, 102);
                                                                                        ">My Dyson</a>.
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px 0px 10px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <div style="
                                                                                    font-family: DysonFutura,
                                                                                    Arial, Helvetica,
                                                                                    sans-serif;
                                                                                    font-size: 11px;
                                                                                    line-height: 15px;
                                                                                    color: rgb(51, 51, 51);
                                                                                    ">
                                                                                    Discover
                                                                                    maintenance
                                                                                    guides,
                                                                                    how-to videos
                                                                                    and more by
                                                                                    visiting the
                                                                                    <a href="https://www.dyson.com/support/journey/overview.html"
                                                                                        target="_blank"
                                                                                        style="
                                                                                        color: rgb(102, 102, 102);
                                                                                        ">Dyson Support Page</a>.
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                            </table>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" style="
                border-collapse: collapse;
                background: rgb(25, 29, 32);
                width: 1330.67px;
                ">
                <tbody>
                <tr>
                    <td style="border-collapse: collapse">
                        <div style="margin: 0px auto; max-width: 640px">
                            <table align="center" border="0" cellpadding="0" cellspacing="0"
                            style="border-collapse: collapse; width: 640px">
                            <tbody>
                                <tr>
                                    <td style="
                                        border-collapse: collapse;
                                        direction: ltr;
                                        font-size: 0px;
                                        padding: 0px;
                                        text-align: center;
                                        ">
                                        <div style="margin: 0px auto; max-width: 640px">
                                        <table align="center" border="0" cellpadding="0" cellspacing="0"
                                            style="border-collapse: collapse; width: 640px">
                                            <tbody>
                                                <tr>
                                                    <td style="
                                                    border-collapse: collapse;
                                                    direction: ltr;
                                                    padding: 30px 5px 0px;
                                                    ">
                                                    <div style="
                                                        max-width: 70px;
                                                        width: 70px;
                                                        text-align: left;
                                                        direction: ltr;
                                                        display: inline-block;
                                                        vertical-align: top;
                                                        ">
                                                        <table border="0" cellpadding="0" cellspacing="0"
                                                            width="100%" style="border-collapse: collapse">
                                                            <tbody>
                                                                <tr>
                                                                <td style="
                                                                    border-collapse: collapse;
                                                                    vertical-align: top;
                                                                    padding: 0px 0px 20px 15px;
                                                                    ">
                                                                    <table border="0" cellpadding="0"
                                                                        cellspacing="0" width="100%"
                                                                        style="border-collapse: collapse">
                                                                        <tbody>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <table border="0"
                                                                                    cellpadding="0"
                                                                                    cellspacing="0"
                                                                                    style="
                                                                                    border-collapse: collapse;
                                                                                    border-spacing: 0px;
                                                                                    ">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                        <td style="
                                                                                            border-collapse: collapse;
                                                                                            width: 48px;
                                                                                            ">
                                                                                            <img height="auto"
                                                                                                src="https://dyson-h.assetsadobe2.com/is/image/content/dam/dyson/oe-team-email-assets/transactional-email-assets/support.png?scl=1&amp;fmt=png-alpha"
                                                                                                width="48"
                                                                                                class="gmail-CToWUd"
                                                                                                style="
                                                                                                border: 0px;
                                                                                                height: auto;
                                                                                                line-height: 13px;
                                                                                                outline: none;
                                                                                                display: block;
                                                                                                width: 48px;
                                                                                                font-size: 13px;
                                                                                                ">
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
                                                    </div>
                                                    <div style="
                                                        max-width: 460px;
                                                        width: 460px;
                                                        text-align: left;
                                                        direction: ltr;
                                                        display: inline-block;
                                                        vertical-align: top;
                                                        ">
                                                        <table border="0" cellpadding="0" cellspacing="0"
                                                            width="100%" style="border-collapse: collapse">
                                                            <tbody>
                                                                <tr>
                                                                <td style="
                                                                    border-collapse: collapse;
                                                                    vertical-align: top;
                                                                    padding: 0px 15px 20px;
                                                                    ">
                                                                    <table border="0" cellpadding="0"
                                                                        cellspacing="0" width="100%"
                                                                        style="border-collapse: collapse">
                                                                        <tbody>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px 0px 10px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <div style="
                                                                                    font-family: DysonFutura,
                                                                                    Arial, Helvetica,
                                                                                    sans-serif;
                                                                                    font-size: 18px;
                                                                                    line-height: 24px;
                                                                                    color: rgb(255, 255, 255);
                                                                                    ">
                                                                                    What happens
                                                                                    next
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px 0px 10px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <div style="
                                                                                    font-family: DysonFutura,
                                                                                    Arial, Helvetica,
                                                                                    sans-serif;
                                                                                    font-size: 14px;
                                                                                    line-height: 18px;
                                                                                    color: rgb(255, 255, 255);
                                                                                    ">
                                                                                    We will send you
                                                                                    another email
                                                                                    when your order
                                                                                    has been
                                                                                    shipped.
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                            </table>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" style="
                border-collapse: collapse;
                background: rgb(243, 243, 243);
                width: 1330.67px;
                ">
                <tbody>
                <tr>
                    <td style="border-collapse: collapse">
                        <div style="margin: 0px auto; max-width: 640px">
                            <table align="center" border="0" cellpadding="0" cellspacing="0"
                            style="border-collapse: collapse; width: 640px">
                            <tbody>
                                <tr>
                                    <td style="
                                        border-collapse: collapse;
                                        direction: ltr;
                                        font-size: 0px;
                                        padding: 0px;
                                        text-align: center;
                                        ">
                                        <div style="margin: 0px auto; max-width: 640px">
                                        <table align="center" border="0" cellpadding="0" cellspacing="0"
                                            style="border-collapse: collapse; width: 640px">
                                            <tbody>
                                                <tr>
                                                    <td style="
                                                    border-collapse: collapse;
                                                    direction: ltr;
                                                    padding: 30px 5px 0px;
                                                    ">
                                                    <div style="
                                                        max-width: 460px;
                                                        width: 460px;
                                                        text-align: left;
                                                        direction: ltr;
                                                        display: inline-block;
                                                        vertical-align: top;
                                                        ">
                                                        <table border="0" cellpadding="0" cellspacing="0"
                                                            width="100%" style="border-collapse: collapse">
                                                            <tbody>
                                                                <tr>
                                                                <td style="
                                                                    border-collapse: collapse;
                                                                    vertical-align: top;
                                                                    padding: 0px 15px 20px;
                                                                    ">
                                                                    <table border="0" cellpadding="0"
                                                                        cellspacing="0" width="100%"
                                                                        style="border-collapse: collapse">
                                                                        <tbody>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px 0px 10px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <div style="
                                                                                    font-family: DysonFutura,
                                                                                    Arial, Helvetica,
                                                                                    sans-serif;
                                                                                    font-size: 21px;
                                                                                    line-height: 27px;
                                                                                    color: rgb(51, 51, 51);
                                                                                    ">
                                                                                    Contacting us is
                                                                                    easy
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px 0px 10px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <div style="
                                                                                    font-family: DysonFutura,
                                                                                    Arial, Helvetica,
                                                                                    sans-serif;
                                                                                    font-size: 14px;
                                                                                    line-height: 18px;
                                                                                    color: rgb(51, 51, 51);
                                                                                    ">
                                                                                    If you have any
                                                                                    questions
                                                                                    about your
                                                                                    order, a Dyson
                                                                                    Expert is on
                                                                                    hand to help.
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        </div>
                                        <div style="margin: 0px auto; max-width: 640px">
                                        <table align="center" border="0" cellpadding="0" cellspacing="0"
                                            style="border-collapse: collapse; width: 640px">
                                            <tbody>
                                                <tr>
                                                    <td style="
                                                    border-collapse: collapse;
                                                    direction: ltr;
                                                    padding: 0px 5px 10px;
                                                    ">
                                                    <div style="
                                                        max-width: 33.3333%;
                                                        width: 210px;
                                                        text-align: left;
                                                        direction: ltr;
                                                        display: inline-block;
                                                        vertical-align: top;
                                                        ">
                                                        <table border="0" cellpadding="0" cellspacing="0"
                                                            width="100%" style="border-collapse: collapse">
                                                            <tbody>
                                                                <tr>
                                                                <td style="
                                                                    border-collapse: collapse;
                                                                    vertical-align: top;
                                                                    padding: 0px 15px 20px;
                                                                    ">
                                                                    <table border="0" cellpadding="0"
                                                                        cellspacing="0" width="100%"
                                                                        style="border-collapse: collapse">
                                                                        <tbody>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px 0px 15px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <table border="0"
                                                                                    cellpadding="0"
                                                                                    cellspacing="0"
                                                                                    style="
                                                                                    border-collapse: collapse;
                                                                                    width: 210px;
                                                                                    border-spacing: 0px;
                                                                                    ">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                        <td align="center"
                                                                                            bgcolor="#333333"
                                                                                            valign="middle"
                                                                                            style="
                                                                                            border-collapse: collapse;
                                                                                            border: none;
                                                                                            border-radius: 0px;
                                                                                            background: rgb(
                                                                                            51,
                                                                                            51,
                                                                                            51
                                                                                            );
                                                                                            ">
                                                                                            <a href="https://www.dyson.com/support/contact-us"
                                                                                                target="_blank"
                                                                                                style="
                                                                                                color: rgb(
                                                                                                255,
                                                                                                255,
                                                                                                255
                                                                                                );
                                                                                                display: inline-block;
                                                                                                width: 180px;
                                                                                                background-image: initial;
                                                                                                background-position: initial;
                                                                                                background-size: initial;
                                                                                                background-repeat: initial;
                                                                                                background-origin: initial;
                                                                                                background-clip: initial;
                                                                                                font-family: DysonFutura,
                                                                                                Arial, Helvetica,
                                                                                                sans-serif;
                                                                                                font-size: 14px;
                                                                                                line-height: 18px;
                                                                                                margin: 0px;
                                                                                                text-decoration-line: none;
                                                                                                padding: 13px 10px;
                                                                                                border-radius: 0px;
                                                                                                ">Contact us</a>
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
                                                    </div>
                                                    <div style="
                                                        max-width: 33.3333%;
                                                        width: 210px;
                                                        text-align: left;
                                                        direction: ltr;
                                                        display: inline-block;
                                                        vertical-align: top;
                                                        "></div>
                                                    <div style="
                                                        max-width: 33.3333%;
                                                        width: 210px;
                                                        text-align: left;
                                                        direction: ltr;
                                                        display: inline-block;
                                                        vertical-align: top;
                                                        "></div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                            </table>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" style="
                border-collapse: collapse;
                background-image: initial;
                background-position: initial;
                background-size: initial;
                background-repeat: initial;
                background-origin: initial;
                background-clip: initial;
                width: 1330.67px;
                ">
                <tbody>
                <tr>
                    <td style="border-collapse: collapse">
                        <div style="margin: 0px auto; max-width: 640px">
                            <table align="center" border="0" cellpadding="0" cellspacing="0"
                            style="border-collapse: collapse; width: 640px">
                            <tbody>
                                <tr>
                                    <td style="
                                        border-collapse: collapse;
                                        direction: ltr;
                                        font-size: 0px;
                                        padding: 0px;
                                        text-align: center;
                                        ">
                                        <div style="margin: 0px auto; max-width: 640px">
                                        <table align="center" border="0" cellpadding="0" cellspacing="0"
                                            style="border-collapse: collapse; width: 640px">
                                            <tbody>
                                                <tr>
                                                    <td style="
                                                    border-collapse: collapse;
                                                    direction: ltr;
                                                    padding: 25px 5px 0px;
                                                    ">
                                                    <div style="
                                                        max-width: 100%;
                                                        width: 630px;
                                                        line-height: 0;
                                                        text-align: left;
                                                        display: inline-block;
                                                        direction: ltr;
                                                        ">
                                                        <div style="
                                                            max-width: 28%;
                                                            width: 176.389px;
                                                            direction: ltr;
                                                            display: inline-block;
                                                            vertical-align: top;
                                                            ">
                                                            <table border="0" cellpadding="0"
                                                                cellspacing="0" width="100%"
                                                                style="border-collapse: collapse">
                                                                <tbody>
                                                                <tr>
                                                                    <td style="
                                                                        border-collapse: collapse;
                                                                        vertical-align: top;
                                                                        padding: 0px 15px;
                                                                        ">
                                                                        <table border="0"
                                                                            cellpadding="0"
                                                                            cellspacing="0" width="100%"
                                                                            style="border-collapse: collapse">
                                                                            <tbody>
                                                                            <tr>
                                                                                <td align="left"
                                                                                    style="
                                                                                    border-collapse: collapse;
                                                                                    padding: 0px 0px 10px;
                                                                                    word-break: break-word;
                                                                                    ">
                                                                                    <table
                                                                                        border="0"
                                                                                        cellpadding="0"
                                                                                        cellspacing="0"
                                                                                        style="
                                                                                        border-collapse: collapse;
                                                                                        border-spacing: 0px;
                                                                                        ">
                                                                                        <tbody>
                                                                                        <tr>
                                                                                            <td style="
                                                                                                border-collapse: collapse;
                                                                                                width: 55px;
                                                                                                ">
                                                                                                <a href="https://www.dyson.com/"
                                                                                                    target="_blank"><img
                                                                                                    alt=""
                                                                                                    height="21"
                                                                                                    src="https://dyson-h.assetsadobe2.com/is/image//content/dam/dyson/oe-team-email-assets/mjml-master-template-assets/dyson-logo-footer-dark-x2.png?scl=1&amp;fmt=png-alpha"
                                                                                                    width="55"
                                                                                                    class="gmail-CToWUd"
                                                                                                    style="
                                                                                                    border: 0px;
                                                                                                    height: 21px;
                                                                                                    line-height: 13px;
                                                                                                    outline: none;
                                                                                                    text-decoration-line: none;
                                                                                                    display: block;
                                                                                                    width: 55px;
                                                                                                    font-size: 13px;
                                                                                                    "></a>
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
                                                        </div>
                                                    </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        </div>
                                        <div style="margin: 0px auto; max-width: 640px">
                                        <table align="center" border="0" cellpadding="0" cellspacing="0"
                                            style="border-collapse: collapse; width: 640px">
                                            <tbody>
                                                <tr>
                                                    <td style="
                                                    border-collapse: collapse;
                                                    direction: ltr;
                                                    padding: 3px 5px 0px;
                                                    ">
                                                    <div style="
                                                        max-width: 100%;
                                                        width: 630px;
                                                        text-align: left;
                                                        direction: ltr;
                                                        display: inline-block;
                                                        vertical-align: top;
                                                        ">
                                                        <table border="0" cellpadding="0" cellspacing="0"
                                                            width="100%" style="border-collapse: collapse">
                                                            <tbody>
                                                                <tr>
                                                                <td style="
                                                                    border-collapse: collapse;
                                                                    vertical-align: top;
                                                                    padding: 0px 15px 20px;
                                                                    ">
                                                                    <table border="0" cellpadding="0"
                                                                        cellspacing="0" width="100%"
                                                                        style="border-collapse: collapse">
                                                                        <tbody>
                                                                            <tr>
                                                                            <td align="center"
                                                                                style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <p style="
                                                                                    margin: 0px auto;
                                                                                    border-top: 1px solid
                                                                                    rgb(217, 217, 217);
                                                                                    font-size: 1px;
                                                                                    width: 600px;
                                                                                    "></p>
                                                                            </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        </div>
                                        <div style="margin: 0px auto; max-width: 640px">
                                        <table align="center" border="0" cellpadding="0" cellspacing="0"
                                            style="border-collapse: collapse; width: 640px">
                                            <tbody>
                                                <tr>
                                                    <td style="
                                                    border-collapse: collapse;
                                                    direction: ltr;
                                                    padding: 0px 5px 40px;
                                                    ">
                                                    <div style="
                                                        max-width: 100%;
                                                        width: 630px;
                                                        text-align: left;
                                                        direction: ltr;
                                                        display: inline-block;
                                                        vertical-align: top;
                                                        ">
                                                        <table border="0" cellpadding="0" cellspacing="0"
                                                            width="100%" style="border-collapse: collapse">
                                                            <tbody>
                                                                <tr>
                                                                <td style="
                                                                    border-collapse: collapse;
                                                                    vertical-align: top;
                                                                    padding: 0px 15px 10px;
                                                                    ">
                                                                    <table border="0" cellpadding="0"
                                                                        cellspacing="0" width="100%"
                                                                        style="border-collapse: collapse">
                                                                        <tbody>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px 0px 10px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <div style="
                                                                                    font-family: DysonFutura,
                                                                                    Arial, Helvetica,
                                                                                    sans-serif;
                                                                                    font-size: 11px;
                                                                                    line-height: 15px;
                                                                                    color: rgb(153, 153, 153);
                                                                                    ">
                                                                                    You've received
                                                                                    this email
                                                                                    because you
                                                                                    recently
                                                                                    purchased
                                                                                    a Dyson machine.
                                                                                    Unless
                                                                                    requested, you
                                                                                    have not been
                                                                                    added to any
                                                                                    marketing list.
                                                                                    We explain how
                                                                                    we use your
                                                                                    personal
                                                                                    information in
                                                                                    our
                                                                                    <a href="https://privacy.dyson.com/homepage.aspx"
                                                                                        target="_blank"
                                                                                        style="
                                                                                        color: rgb(153, 153, 153);
                                                                                        ">Privacy policy</a>. If you think you have
                                                                                    received this
                                                                                    email in error,
                                                                                    please contact
                                                                                    us.
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                                </tr>
                                                                <tr>
                                                                <td style="
                                                                    border-collapse: collapse;
                                                                    vertical-align: top;
                                                                    padding: 0px 15px 20px;
                                                                    ">
                                                                    <table border="0" cellpadding="0"
                                                                        cellspacing="0" width="100%"
                                                                        style="border-collapse: collapse">
                                                                        <tbody>
                                                                            <tr>
                                                                            <td align="left" style="
                                                                                border-collapse: collapse;
                                                                                padding: 0px 0px 10px;
                                                                                word-break: break-word;
                                                                                ">
                                                                                <div style="
                                                                                    font-family: DysonFutura,
                                                                                    Arial, Helvetica,
                                                                                    sans-serif;
                                                                                    font-size: 11px;
                                                                                    line-height: 15px;
                                                                                    color: rgb(153, 153, 153);
                                                                                    ">
                                                                                    Dyson Inc. 1330
                                                                                    West Fulton
                                                                                    Street, 5th
                                                                                    Floor, Chicago,
                                                                                    Illinois 60607.
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                            </table>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    
    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
