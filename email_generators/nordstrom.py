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
    msg['From'] = formataddr((f'Nordstrom', sender_email))
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
    "Please enter the order date (03/12/24):",
    "Please enter the street address (123 Test Street):",
    "Please enter the suburb (Test Suburb):",
    "Please enter the image url (.JPG, .PNG):",
    "Please enter the item name (Cologne):",
    "Please enter the item price (WITHOUT THE $):",
    "Please enter the item number (587463):",
    "Please enter the country (USA):",
    "Please enter the item tax (WITHOUT THE $):",
    "Please enter the order total (WITHOUT THE $):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira a data do pedido (03/12/24):",
    "Por favor, insira o endereço (123 Test Street):",
    "Por favor, insira o bairro (Test Suburb):",
    "Por favor, insira a URL da imagem (.JPG, .PNG):",
    "Por favor, insira o nome do item (Colônia):",
    "Por favor, insira o preço do item (SEM O SÍMBOLO $):",
    "Por favor, insira o número do item (587463):",
    "Por favor, insira o país (EUA):",
    "Por favor, insira o imposto do item (SEM O SÍMBOLO $):",
    "Por favor, insira o total do pedido (SEM O SÍMBOLO $):",
    "Por favor, insira a moeda ($/€/£):",
    "Qual endereço de e-mail você quer usar para receber este e-mail (juggyresells@gmail.com):"
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
    part1 = random.randint(10000000, 99999999)  # Random 8-digit number

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

    sender_email = f'{EMAIL}'
    sender_password = f'{PASSWORD}'
    recipient_email = f'{user_inputs[12]}'
    subject = f"Thank you for your order!"

    html_template = f"""
        <div><br /></div>
    <div>
        <div style="line-height: 20px"> </div>
        <table
            style="width: 640px"
            border="0"
            width="640"
            cellspacing="0"
            cellpadding="0"
            align="center"
        >
            <tbody>
            <tr>
                <td align="center" valign="top" width="100%">
                <table
                    style="min-width: 100%"
                    width="100%"
                    cellspacing="0"
                    cellpadding="0"
                >
                    <tbody>
                    <tr>
                        <td>
                        <table border="0" cellspacing="0" cellpadding="0">
                            <tbody>
                            <tr>
                                <td
                                style="width: 640px; background-color: #ffffff"
                                align="left"
                                valign="top"
                                >
                                <table
                                    style="width: 640px"
                                    border="0"
                                    cellspacing="0"
                                    cellpadding="0"
                                >
                                    <tbody>
                                    <tr>
                                        <td align="left" valign="top">
                                        <table
                                            style="width: 640px"
                                            border="0"
                                            cellspacing="0"
                                            cellpadding="0"
                                        >
                                            <tbody>
                                            <tr>
                                                <td align="left" valign="top">
                                                <table
                                                    border="0"
                                                    cellspacing="0"
                                                    cellpadding="0"
                                                >
                                                    <tbody>
                                                    <tr>
                                                        <td
                                                        style="width: 202px"
                                                        align="left"
                                                        valign="top"
                                                        >
                                                        <a
                                                            ><img
                                                            src="https://ecp.yusercontent.com/mail?url=https%3A%2F%2Fimage.eml.nordstrom.com%2Flib%2Ffe3915707564057d721d74%2Fm%2F1%2F98e69c7c-d0e7-4d37-af43-4cc6fb1809c9.gif&amp;t=1560783073&amp;ymreqid=3ee68421-abe6-ad44-1c55-020000015300&amp;sig=WtFXDR1GIYxJ6fhHagDXNw--~C"
                                                            alt="NORDSTROM"
                                                            width="202"
                                                            height="25"
                                                            border="0"
                                                        /></a>
                                                        </td>
                                                    </tr>
                                                    </tbody>
                                                </table>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td
                                                style="padding-top: 25px"
                                                align="left"
                                                valign="bottom"
                                                >
                                                <table
                                                    border="0"
                                                    width="100%"
                                                    cellspacing="0"
                                                    cellpadding="0"
                                                >
                                                    <tbody>
                                                    <tr>
                                                        <td
                                                        align="left"
                                                        valign="bottom"
                                                        >
                                                        <a
                                                            style="
                                                            font-size: 12px;
                                                            font-family: Arial,
                                                                Helvetica,
                                                                sans-serif;
                                                            color: #393939;
                                                            line-height: 12px;
                                                            text-decoration: none;
                                                            font-weight: bold;
                                                            "
                                                            >Designer</a
                                                        >
                                                        </td>
                                                        <td
                                                        style="padding-left: 38px"
                                                        align="left"
                                                        valign="bottom"
                                                        >
                                                        <a
                                                            style="
                                                            font-size: 12px;
                                                            font-family: Arial,
                                                                Helvetica,
                                                                sans-serif;
                                                            color: #393939;
                                                            line-height: 12px;
                                                            text-decoration: none;
                                                            font-weight: bold;
                                                            "
                                                            >Women</a
                                                        >
                                                        </td>
                                                        <td
                                                        style="padding-left: 38px"
                                                        align="left"
                                                        valign="bottom"
                                                        >
                                                        <a
                                                            style="
                                                            font-size: 12px;
                                                            font-family: Arial,
                                                                Helvetica,
                                                                sans-serif;
                                                            color: #393939;
                                                            line-height: 12px;
                                                            text-decoration: none;
                                                            font-weight: bold;
                                                            "
                                                            >Men</a
                                                        >
                                                        </td>
                                                        <td
                                                        style="padding-left: 38px"
                                                        align="left"
                                                        valign="bottom"
                                                        >
                                                        <a
                                                            style="
                                                            font-size: 12px;
                                                            font-family: Arial,
                                                                Helvetica,
                                                                sans-serif;
                                                            color: #393939;
                                                            line-height: 12px;
                                                            text-decoration: none;
                                                            font-weight: bold;
                                                            "
                                                            >Kids</a
                                                        >
                                                        </td>
                                                        <td
                                                        style="padding-left: 38px"
                                                        align="left"
                                                        valign="bottom"
                                                        >
                                                        <a
                                                            style="
                                                            font-size: 12px;
                                                            font-family: Arial,
                                                                Helvetica,
                                                                sans-serif;
                                                            color: #393939;
                                                            line-height: 12px;
                                                            text-decoration: none;
                                                            font-weight: bold;
                                                            "
                                                            >Home &amp; Gifts</a
                                                        >
                                                        </td>
                                                        <td
                                                        style="padding-left: 38px"
                                                        align="left"
                                                        valign="bottom"
                                                        >
                                                        <a
                                                            style="
                                                            font-size: 12px;
                                                            font-family: Arial,
                                                                Helvetica,
                                                                sans-serif;
                                                            color: #393939;
                                                            line-height: 12px;
                                                            text-decoration: none;
                                                            font-weight: bold;
                                                            "
                                                            >Beauty</a
                                                        >
                                                        </td>
                                                        <td
                                                        style="padding-left: 38px"
                                                        align="left"
                                                        valign="bottom"
                                                        >
                                                        <a
                                                            style="
                                                            font-size: 12px;
                                                            font-family: Arial,
                                                                Helvetica,
                                                                sans-serif;
                                                            color: #393939;
                                                            line-height: 12px;
                                                            text-decoration: none;
                                                            font-weight: bold;
                                                            "
                                                            >Sale</a
                                                        >
                                                        </td>
                                                        <td
                                                        style="padding-left: 38px"
                                                        align="right"
                                                        valign="bottom"
                                                        >
                                                        <a
                                                            style="
                                                            font-size: 12px;
                                                            font-family: Arial,
                                                                Helvetica,
                                                                sans-serif;
                                                            color: #393939;
                                                            line-height: 12px;
                                                            text-decoration: none;
                                                            font-weight: bold;
                                                            "
                                                            >What&#39;s Now</a
                                                        >
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
                        <table width="100%" cellspacing="0" cellpadding="0">
                            <tbody>
                            <tr>
                                <td
                                style="
                                    font-size: 8px;
                                    min-height: 8px;
                                    line-height: 8px;
                                "
                                height="8"
                                >
                                 
                                </td>
                            </tr>
                            <tr>
                                <td
                                style="
                                    min-height: 1px;
                                    font-size: 1px;
                                    line-height: 1px;
                                "
                                bgcolor="#d7d7d7"
                                width="100%"
                                height="1"
                                >
                                <img
                                    style="border: 0"
                                    src="https://ecp.yusercontent.com/mail?url=https%3A%2F%2Fimage.eml.nordstrom.com%2Flib%2Ffe3915707564057d721d74%2Fm%2F1%2F4ff34b83-cb67-4357-a2d5-69521764830c.gif&amp;t=1560783073&amp;ymreqid=3ee68421-abe6-ad44-1c55-020000015300&amp;sig=CxPhdvawTzGvcMbvaflKdw--~C"
                                    alt="mail?url=https%3A%2F%2Fimage.eml.nordstrom.com%2Flib%2Ffe3915707564057d721d74%2Fm%2F1%2F4ff34b83-cb67-4357-a2d5-69521764830c.gif&amp;t=1560783073&amp;ymreqid=3ee68421-abe6-ad44-1c55-020000015300&amp;sig=CxPhdvawTzGvcMbvaflKdw--~C"
                                    width="640"
                                    height="1"
                                />
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
        <table
            style="width: 640px"
            border="0"
            width="640"
            cellspacing="0"
            cellpadding="0"
            align="center"
        >
            <tbody>
            <tr>
                <td align="center" valign="top" width="100%">
                <table
                    style="min-width: 100%"
                    width="100%"
                    cellspacing="0"
                    cellpadding="0"
                >
                    <tbody>
                    <tr>
                        <td>
                        <div style="line-height: 48px"> </div>
                        <table
                            style="width: 640px"
                            cellspacing="0"
                            cellpadding="0"
                        >
                            <tbody>
                            <tr>
                                <td align="left" valign="top">
                                <table cellspacing="0" cellpadding="0">
                                    <tbody>
                                    <tr>
                                        <td
                                        style="
                                            font-weight: normal;
                                            padding: 0;
                                            margin: 0;
                                            border: 0;
                                            vertical-align: top;
                                            width: 178px;
                                        "
                                        align="left"
                                        valign="top"
                                        >
                                        <table cellspacing="0" cellpadding="0">
                                            <tbody>
                                            <tr>
                                                <td
                                                style="width: 178px"
                                                align="left"
                                                valign="top"
                                                >
                                                <a
                                                    ><img
                                                    style="border: 0"
                                                    src="https://ecp.yusercontent.com/mail?url=https%3A%2F%2Fimage.eml.nordstrom.com%2Flib%2Ffe3915707564057d721d74%2Fm%2F1%2F4db7cfbc-eb0c-4d3c-8208-98137ae4a1c2.png&amp;t=1560783073&amp;ymreqid=3ee68421-abe6-ad44-1c55-020000015300&amp;sig=ILOaKIlMggC32Shw9PY95A--~C"
                                                    alt="Thanks"
                                                    width="178"
                                                    height="45"
                                                /></a>
                                                </td>
                                            </tr>
                                            </tbody>
                                        </table>
                                        </td>
                                        <td
                                        style="
                                            font-weight: normal;
                                            padding: 0;
                                            margin: 0;
                                            border: 0;
                                            vertical-align: top;
                                        "
                                        align="left"
                                        valign="top"
                                        width="436"
                                        >
                                        <table cellspacing="0" cellpadding="0">
                                            <tbody>
                                            <tr>
                                                <td
                                                style="width: 436px"
                                                align="left"
                                                valign="top"
                                                >
                                                <div style="line-height: 24px">
                                                     
                                                </div>
                                                <div
                                                    style="
                                                    font-size: 19px;
                                                    font-family: Arial, Verdana,
                                                        Geneva, sans-serif;
                                                    color: #000000;
                                                    line-height: 21px;
                                                    "
                                                >
                                                    for shopping with us,
                                                    {user_inputs[0]}!
                                                </div>
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
                <table
                    style="min-width: 100%"
                    width="100%"
                    cellspacing="0"
                    cellpadding="0"
                >
                    <tbody>
                    <tr>
                        <td>
                        <div style="line-height: 27px"> </div>
                        <table
                            style="width: 640px"
                            cellspacing="0"
                            cellpadding="0"
                        >
                            <tbody>
                            <tr>
                                <td align="left" valign="top">
                                <table cellspacing="0" cellpadding="0">
                                    <tbody>
                                    <tr>
                                        <td align="left" valign="top" width="8">
                                        <div
                                            style="
                                            font-size: 13px;
                                            font-family: Arial, Verdana, Geneva,
                                                sans-serif;
                                            color: #000000;
                                            line-height: 19px;
                                            "
                                        >
                                            •
                                        </div>
                                        </td>
                                        <td align="left" valign="top">
                                        <div
                                            style="
                                            font-size: 13px;
                                            font-family: Arial, Verdana, Geneva,
                                                sans-serif;
                                            color: #000000;
                                            line-height: 19px;
                                            "
                                        >
                                            We&#39;ll follow up with another email
                                            once your items have shipped.
                                        </div>
                                        </td>
                                        <td style="width: 20px" valign="top"> </td>
                                    </tr>
                                    <tr>
                                        <td align="left" valign="top" width="8">
                                        <div
                                            style="
                                            font-size: 13px;
                                            font-family: Arial, Verdana, Geneva,
                                                sans-serif;
                                            color: #000000;
                                            line-height: 19px;
                                            "
                                        >
                                            •
                                        </div>
                                        </td>
                                        <td align="left" valign="top">
                                        <div
                                            style="
                                            font-size: 13px;
                                            font-family: Arial, Verdana, Geneva,
                                                sans-serif;
                                            color: #000000;
                                            line-height: 19px;
                                            "
                                        >
                                            We authorized your card for the full
                                            amount of the purchase when you placed
                                            your order. This authorization will fall
                                            off your account in about 7 business
                                            days, depending on your bank.
                                        </div>
                                        </td>
                                        <td style="width: 20px" valign="top"> </td>
                                    </tr>
                                    <tr>
                                        <td align="left" valign="top" width="8">
                                        <div
                                            style="
                                            font-size: 13px;
                                            font-family: Arial, Verdana, Geneva,
                                                sans-serif;
                                            color: #000000;
                                            line-height: 19px;
                                            "
                                        >
                                            •
                                        </div>
                                        </td>
                                        <td align="left" valign="top">
                                        <div
                                            style="
                                            font-size: 13px;
                                            font-family: Arial, Verdana, Geneva,
                                                sans-serif;
                                            color: #000000;
                                            line-height: 19px;
                                            "
                                        >
                                            Your card will be charged the final
                                            amount when your order ships. The final
                                            amount may appear as several charges if
                                            your items ship separately.
                                        </div>
                                        </td>
                                        <td style="width: 20px" valign="top"> </td>
                                    </tr>
                                    <tr>
                                        <td align="left" valign="top" width="8">
                                        <div
                                            style="
                                            font-size: 13px;
                                            font-family: Arial, Verdana, Geneva,
                                                sans-serif;
                                            color: #000000;
                                            line-height: 19px;
                                            "
                                        >
                                            •
                                        </div>
                                        </td>
                                        <td align="left" valign="top">
                                        <div
                                            style="
                                            font-size: 13px;
                                            font-family: Arial, Verdana, Geneva,
                                                sans-serif;
                                            color: #000000;
                                            line-height: 19px;
                                            "
                                        >
                                            We can&#39;t usually change an order
                                            after it&#39;s been placed.
                                        </div>
                                        </td>
                                        <td style="width: 20px" valign="top"> </td>
                                    </tr>
                                    <tr>
                                        <td align="left" valign="top" width="8">
                                        <div
                                            style="
                                            font-size: 13px;
                                            font-family: Arial, Verdana, Geneva,
                                                sans-serif;
                                            color: #000000;
                                            line-height: 19px;
                                            "
                                        >
                                            •
                                        </div>
                                        </td>
                                        <td align="left" valign="top">
                                        <div
                                            style="
                                            font-size: 13px;
                                            font-family: Arial, Verdana, Geneva,
                                                sans-serif;
                                            color: #000000;
                                            line-height: 19px;
                                            "
                                        >
                                            If we&#39;re unable to fulfill your
                                            order for any reason, we&#39;ll let you
                                            know ASAP.
                                        </div>
                                        </td>
                                        <td style="width: 20px" valign="top"> </td>
                                    </tr>
                                    </tbody>
                                </table>
                                </td>
                            </tr>
                            </tbody>
                        </table>
                        <div style="line-height: 27px"> </div>
                        <table cellspacing="0" cellpadding="0">
                            <tbody>
                            <tr>
                                <td align="left">
                                <table border="0" cellspacing="0" cellpadding="0">
                                    <tbody>
                                    <tr>
                                        <td align="center" bgcolor="#ffffff">
                                        <a
                                            style="
                                            font-family: Arial, Helvetica,
                                                sans-serif;
                                            font-size: 13px;
                                            font-weight: normal;
                                            color: #000001;
                                            text-decoration: none;
                                            padding: 15px 40px;
                                            border: 1px solid #000000;
                                            "
                                            >See Order Details</a
                                        >
                                        </td>
                                    </tr>
                                    </tbody>
                                </table>
                                </td>
                            </tr>
                            </tbody>
                        </table>
                        <div style="line-height: 36px"> </div>
                        </td>
                    </tr>
                    </tbody>
                </table>
                <table
                    style="min-width: 100%"
                    width="100%"
                    cellspacing="0"
                    cellpadding="0"
                >
                    <tbody>
                    <tr>
                        <td> </td>
                    </tr>
                    </tbody>
                </table>
                <table
                    style="min-width: 100%"
                    width="100%"
                    cellspacing="0"
                    cellpadding="0"
                >
                    <tbody>
                    <tr>
                        <td>
                        <table width="640" cellspacing="0" cellpadding="0">
                            <tbody>
                            <tr>
                                <td width="0"> </td>
                                <td align="left" valign="top">
                                <table cellspacing="0" cellpadding="0">
                                    <tbody>
                                    <tr>
                                        <td style="line-height: 14px" height="14">
                                        <img
                                            src="https://ecp.yusercontent.com/mail?url=https%3A%2F%2Fimage.eml.nordstrom.com%2Flib%2Ffe3915707564057d721d74%2Fm%2F1%2F4ff34b83-cb67-4357-a2d5-69521764830c.gif&amp;t=1560783073&amp;ymreqid=3ee68421-abe6-ad44-1c55-020000015300&amp;sig=CxPhdvawTzGvcMbvaflKdw--~C"
                                            alt="mail?url=https%3A%2F%2Fimage.eml.nordstrom.com%2Flib%2Ffe3915707564057d721d74%2Fm%2F1%2F4ff34b83-cb67-4357-a2d5-69521764830c.gif&amp;t=1560783073&amp;ymreqid=3ee68421-abe6-ad44-1c55-020000015300&amp;sig=CxPhdvawTzGvcMbvaflKdw--~C"
                                            width="1"
                                            height="1"
                                            border="0"
                                        />
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
                                <td style="line-height: 7px" width="640" height="7">
                                <img
                                    src="https://ecp.yusercontent.com/mail?url=https%3A%2F%2Fimage.eml.nordstrom.com%2Flib%2Ffe3915707564057d721d74%2Fm%2F1%2F4ff34b83-cb67-4357-a2d5-69521764830c.gif&amp;t=1560783073&amp;ymreqid=3ee68421-abe6-ad44-1c55-020000015300&amp;sig=CxPhdvawTzGvcMbvaflKdw--~C"
                                    alt="mail?url=https%3A%2F%2Fimage.eml.nordstrom.com%2Flib%2Ffe3915707564057d721d74%2Fm%2F1%2F4ff34b83-cb67-4357-a2d5-69521764830c.gif&amp;t=1560783073&amp;ymreqid=3ee68421-abe6-ad44-1c55-020000015300&amp;sig=CxPhdvawTzGvcMbvaflKdw--~C"
                                    width="1"
                                    height="1"
                                    border="0"
                                />
                                </td>
                            </tr>
                            </tbody>
                        </table>
                        <table cellspacing="0" cellpadding="0">
                            <tbody>
                            <tr>
                                <td width="0"> </td>
                                <td align="left" valign="top">
                                <table cellspacing="0" cellpadding="0">
                                    <tbody>
                                    <tr>
                                        <td
                                        style="
                                            font-weight: normal;
                                            padding: 0;
                                            margin: 0;
                                            border: 0;
                                            vertical-align: top;
                                        "
                                        align="left"
                                        valign="top"
                                        width="434"
                                        >
                                        <table cellspacing="0" cellpadding="0">
                                            <tbody>
                                            <tr>
                                                <td align="left" valign="top">
                                                <div
                                                    style="
                                                    font-size: 13px;
                                                    font-family: Arial, Verdana,
                                                        Geneva, sans-serif;
                                                    color: #000000;
                                                    line-height: 16px;
                                                    "
                                                >
                                                    <strong>Order number: </strong
                                                    ><a
                                                    style="
                                                        color: #000001;
                                                        line-height: 16px;
                                                        text-decoration: underline;
                                                    "
                                                    >{order_num}</a
                                                    >
                                                </div>
                                                </td>
                                            </tr>
                                            </tbody>
                                        </table>
                                        </td>
                                        <td
                                        style="
                                            font-weight: normal;
                                            padding: 0;
                                            margin: 0;
                                            border: 0;
                                            vertical-align: top;
                                        "
                                        align="left"
                                        valign="top"
                                        width="434"
                                        >
                                        <table cellspacing="0" cellpadding="0">
                                            <tbody>
                                            <tr>
                                                <td align="left" valign="top">
                                                <div
                                                    style="
                                                    font-size: 13px;
                                                    font-family: Arial, Verdana,
                                                        Geneva, sans-serif;
                                                    color: #000000;
                                                    line-height: 16px;
                                                    "
                                                >
                                                    <strong>Order date: </strong
                                                    ><a
                                                    style="
                                                        color: #000001;
                                                        text-decoration: none;
                                                    "
                                                    >{user_inputs[1]}</a
                                                    >
                                                </div>
                                                </td>
                                            </tr>
                                            </tbody>
                                        </table>
                                        </td>
                                        <td
                                        style="
                                            font-weight: normal;
                                            padding: 0;
                                            margin: 0;
                                            border: 0;
                                            vertical-align: top;
                                        "
                                        align="left"
                                        valign="top"
                                        width="434"
                                        >
                                        <table cellspacing="0" cellpadding="0">
                                            <tbody>
                                            <tr>
                                                <td align="left" valign="top">
                                                <div
                                                    style="
                                                    font-size: 13px;
                                                    font-family: Arial, Verdana,
                                                        Geneva, sans-serif;
                                                    color: #000000;
                                                    line-height: 16px;
                                                    "
                                                >
                                                    <strong>Order status: </strong
                                                    >Shipped
                                                </div>
                                                </td>
                                            </tr>
                                            </tbody>
                                        </table>
                                        </td>
                                    </tr>
                                    </tbody>
                                </table>
                                </td>
                                <td align="center" valign="top" width="24"> </td>
                            </tr>
                            </tbody>
                        </table>
                        <div style="line-height: 14px"> </div>
                        <table width="100%" cellspacing="0" cellpadding="0">
                            <tbody>
                            <tr>
                                <td
                                style="line-height: 1px"
                                bgcolor="#afafaf"
                                width="100%"
                                height="1"
                                >
                                <img
                                    src="https://ecp.yusercontent.com/mail?url=https%3A%2F%2Fimage.eml.nordstrom.com%2Flib%2Ffe3915707564057d721d74%2Fm%2F1%2F4ff34b83-cb67-4357-a2d5-69521764830c.gif&amp;t=1560783073&amp;ymreqid=3ee68421-abe6-ad44-1c55-020000015300&amp;sig=CxPhdvawTzGvcMbvaflKdw--~C"
                                    alt="mail?url=https%3A%2F%2Fimage.eml.nordstrom.com%2Flib%2Ffe3915707564057d721d74%2Fm%2F1%2F4ff34b83-cb67-4357-a2d5-69521764830c.gif&amp;t=1560783073&amp;ymreqid=3ee68421-abe6-ad44-1c55-020000015300&amp;sig=CxPhdvawTzGvcMbvaflKdw--~C"
                                    width="1"
                                    height="1"
                                    border="0"
                                />
                                </td>
                            </tr>
                            </tbody>
                        </table>
                        </td>
                    </tr>
                    </tbody>
                </table>
                <table
                    style="min-width: 100%"
                    width="100%"
                    cellspacing="0"
                    cellpadding="0"
                >
                    <tbody>
                    <tr>
                        <td>
                        <table width="100%" cellspacing="0" cellpadding="0">
                            <tbody>
                            <tr>
                                <td style="line-height: 1px" height="1">
                                <img
                                    src="https://ecp.yusercontent.com/mail?url=https%3A%2F%2Fimage.eml.nordstrom.com%2Flib%2Ffe3915707564057d721d74%2Fm%2F1%2F4ff34b83-cb67-4357-a2d5-69521764830c.gif&amp;t=1560783073&amp;ymreqid=3ee68421-abe6-ad44-1c55-020000015300&amp;sig=CxPhdvawTzGvcMbvaflKdw--~C"
                                    alt="mail?url=https%3A%2F%2Fimage.eml.nordstrom.com%2Flib%2Ffe3915707564057d721d74%2Fm%2F1%2F4ff34b83-cb67-4357-a2d5-69521764830c.gif&amp;t=1560783073&amp;ymreqid=3ee68421-abe6-ad44-1c55-020000015300&amp;sig=CxPhdvawTzGvcMbvaflKdw--~C"
                                    width="1"
                                    height="1"
                                    border="0"
                                />
                                </td>
                            </tr>
                            </tbody>
                        </table>
                        <div style="line-height: 12px"> </div>
                        <table
                            style="min-width: 100%"
                            width="100%"
                            cellspacing="0"
                            cellpadding="0"
                        >
                            <tbody>
                            <tr>
                                <td>
                                <table
                                    style="width: 640px"
                                    cellspacing="0"
                                    cellpadding="0"
                                >
                                    <tbody>
                                    <tr>
                                        <td colspan="4">
                                        <div style="line-height: 14px"> </div>
                                        <table
                                            style="min-width: 100%"
                                            width="100%"
                                            cellspacing="0"
                                            cellpadding="0"
                                        >
                                            <tbody>
                                            <tr>
                                                <td>
                                                <table
                                                    border="0"
                                                    cellspacing="0"
                                                    cellpadding="0"
                                                >
                                                    <tbody>
                                                    <tr>
                                                        <td
                                                        style="
                                                            font-size: 13px;
                                                            font-family: Arial,
                                                            Verdana, Geneva,
                                                            sans-serif;
                                                            color: #000000;
                                                            line-height: 24px;
                                                        "
                                                        >
                                                        <strong
                                                            >Shipping to: </strong
                                                        >{user_inputs[0]},
                                                        <a
                                                            >{user_inputs[2]}</a
                                                        >,
                                                        {user_inputs[3]}<span
                                                            >, Free Standard
                                                            Shipping</span
                                                        >
                                                        </td>
                                                    </tr>
                                                    </tbody>
                                                </table>
                                                </td>
                                            </tr>
                                            </tbody>
                                        </table>
                                        <div style="line-height: 21px"> </div>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td
                                        style="padding-bottom: 15px; width: 114px"
                                        align="left"
                                        valign="top"
                                        >
                                        <a
                                            ><img
                                            style="
                                                border: 0;
                                                font-family: Arial, Verdana, Geneva,
                                                sans-serif;
                                                color: #000001;
                                                font-size: 13px;
                                                text-decoration: none;
                                            "
                                            src="{user_inputs[4]}"
                                            alt=""
                                            width="114"
                                            height="114"
                                        /></a>
                                        </td>
                                        <td
                                        style="width: 25px"
                                        align="left"
                                        valign="top"
                                        >
                                         
                                        </td>
                                        <td
                                        style="width: 476px"
                                        align="left"
                                        valign="top"
                                        >
                                        <div>
                                            <a
                                            style="
                                                font-family: Arial, Verdana, Geneva,
                                                sans-serif;
                                                color: #000001;
                                                font-size: 13px;
                                                line-height: 19px;
                                                text-decoration: none;
                                                font-weight: bold;
                                            "
                                            ><span
                                                style="
                                                font-family: Arial, Verdana,
                                                    Geneva, sans-serif;
                                                color: #000001;
                                                font-size: 13px;
                                                line-height: 15px;
                                                text-decoration: none;
                                                font-weight: bold;
                                                "
                                                >{user_inputs[5]}</span
                                            ></a
                                            >
                                        </div>
                                        <div style="line-height: 15px"> </div>
                                        <div
                                            style="
                                            font-size: 13px;
                                            font-family: Arial, Verdana, Geneva,
                                                sans-serif;
                                            color: #000000;
                                            line-height: 19px;
                                            "
                                        >
                                            <span style="text-transform: uppercase"
                                            >{user_inputs[11]}{user_inputs[6]}</span
                                            > 
                                            <div
                                            style="
                                                font-size: 13px;
                                                font-family: Arial, Verdana, Geneva,
                                                sans-serif;
                                                color: #000000;
                                                line-height: 19px;
                                            "
                                            >
                                            Item: <a
                                                style="
                                                color: #000001;
                                                text-decoration: none;
                                                "
                                                >#{user_inputs[7]}</a
                                            >
                                            </div>
                                            <div
                                            style="
                                                font-size: 13px;
                                                font-family: Arial, Verdana, Geneva,
                                                sans-serif;
                                                color: #000000;
                                                line-height: 19px;
                                            "
                                            >
                                            Price:
                                            {user_inputs[11]}{user_inputs[6]}
                                            </div>
                                            <div style="line-height: 20px"> </div>
                                        </div>
                                        </td>
                                        <td
                                        style="width: 25px"
                                        align="left"
                                        valign="top"
                                        >
                                         
                                        </td>
                                    </tr>
                                    </tbody>
                                </table>
                                </td>
                            </tr>
                            </tbody>
                        </table>
                        <div style="line-height: 28px"> </div>
                        <table
                            style="width: 640px"
                            cellspacing="0"
                            cellpadding="0"
                        >
                            <tbody>
                            <tr>
                                <td
                                style="line-height: 1px"
                                bgcolor="#afafaf"
                                width="640"
                                height="1"
                                >
                                <img
                                    src="https://ecp.yusercontent.com/mail?url=https%3A%2F%2Fimage.eml.nordstrom.com%2Flib%2Ffe3915707564057d721d74%2Fm%2F1%2F4ff34b83-cb67-4357-a2d5-69521764830c.gif&amp;t=1560783073&amp;ymreqid=3ee68421-abe6-ad44-1c55-020000015300&amp;sig=CxPhdvawTzGvcMbvaflKdw--~C"
                                    alt="mail?url=https%3A%2F%2Fimage.eml.nordstrom.com%2Flib%2Ffe3915707564057d721d74%2Fm%2F1%2F4ff34b83-cb67-4357-a2d5-69521764830c.gif&amp;t=1560783073&amp;ymreqid=3ee68421-abe6-ad44-1c55-020000015300&amp;sig=CxPhdvawTzGvcMbvaflKdw--~C"
                                    width="1"
                                    height="1"
                                    border="0"
                                />
                                </td>
                            </tr>
                            </tbody>
                        </table>
                        </td>
                    </tr>
                    </tbody>
                </table>
                <table
                    style="min-width: 100%"
                    width="100%"
                    cellspacing="0"
                    cellpadding="0"
                >
                    <tbody>
                    <tr>
                        <td>
                        <table
                            style="width: 640px"
                            cellspacing="0"
                            cellpadding="0"
                            align="center"
                        >
                            <tbody>
                            <tr>
                                <td align="left" valign="top">
                                <div style="line-height: 36px"> </div>
                                <div
                                    style="
                                    font-size: 26px;
                                    font-family: Arial, Verdana, Geneva,
                                        sans-serif;
                                    color: #000000;
                                    line-height: 30px;
                                    "
                                >
                                    Billing Summary
                                </div>
                                <div style="line-height: 28px"> </div>
                                <table
                                    width="100%"
                                    cellspacing="0"
                                    cellpadding="0"
                                >
                                    <tbody>
                                    <tr>
                                        <td
                                        style="
                                            font-weight: normal;
                                            padding: 0;
                                            margin: 0;
                                            border: 0;
                                            vertical-align: top;
                                            width: 320px;
                                        "
                                        align="left"
                                        valign="top"
                                        >
                                        <table cellspacing="0" cellpadding="0">
                                            <tbody>
                                            <tr>
                                                <td align="left" valign="top">
                                                <div
                                                    style="
                                                    font-size: 13px;
                                                    font-family: Arial, Verdana,
                                                        Geneva, sans-serif;
                                                    color: #000000;
                                                    line-height: 20px;
                                                    font-weight: bold;
                                                    "
                                                >
                                                    Billing Address:
                                                </div>
                                                <div
                                                    style="
                                                    font-size: 13px;
                                                    font-family: Arial, Verdana,
                                                        Geneva, sans-serif;
                                                    color: #000000;
                                                    line-height: 20px;
                                                    "
                                                >
                                                    {user_inputs[0]}
                                                </div>
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
                </td>
            </tr>
            </tbody>
        </table>
        </div>
        <div>
        <table
            style="width: 640px"
            border="0"
            width="640"
            cellspacing="0"
            cellpadding="0"
            align="center"
        >
            <tbody>
            <tr>
                <td align="center" valign="top" width="100%">
                <table
                    style="min-width: 100%"
                    width="100%"
                    cellspacing="0"
                    cellpadding="0"
                >
                    <tbody>
                    <tr>
                        <td>
                        <table
                            style="width: 640px"
                            cellspacing="0"
                            cellpadding="0"
                            align="center"
                        >
                            <tbody>
                            <tr>
                                <td align="left" valign="top">
                                <table
                                    width="100%"
                                    cellspacing="0"
                                    cellpadding="0"
                                >
                                    <tbody>
                                    <tr>
                                        <td
                                        style="
                                            font-weight: normal;
                                            padding: 0;
                                            margin: 0;
                                            border: 0;
                                            vertical-align: top;
                                            width: 320px;
                                        "
                                        align="left"
                                        valign="top"
                                        >
                                        <table cellspacing="0" cellpadding="0">
                                            <tbody>
                                            <tr>
                                                <td align="left" valign="top">
                                                <div
                                                    style="
                                                    font-size: 13px;
                                                    font-family: Arial, Verdana,
                                                        Geneva, sans-serif;
                                                    color: #000000;
                                                    line-height: 20px;
                                                    text-decoration: none;
                                                    "
                                                >
                                                    <span>{user_inputs[2]}</span>
                                                </div>
                                                <div
                                                    style="
                                                    font-size: 13px;
                                                    font-family: Arial, Verdana,
                                                        Geneva, sans-serif;
                                                    color: #000000;
                                                    line-height: 20px;
                                                    text-decoration: none;
                                                    "
                                                >
                                                    <span
                                                    >{user_inputs[3]}</span
                                                    >
                                                </div>
                                                <div
                                                    style="
                                                    font-size: 13px;
                                                    font-family: Arial, Verdana,
                                                        Geneva, sans-serif;
                                                    color: #000000;
                                                    line-height: 20px;
                                                    "
                                                >
                                                    <span
                                                    >{user_inputs[8]}</span
                                                    >
                                                </div>
                                                <div style="line-height: 5px">
                                                     
                                                </div>
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
                </td>
            </tr>
            </tbody>
        </table>
        </div>
        <div>
        <table
            style="width: 640px"
            border="0"
            width="640"
            cellspacing="0"
            cellpadding="0"
            align="center"
        >
            <tbody>
            <tr>
                <td align="center" valign="top" width="100%">
                <table
                    style="min-width: 100%"
                    width="100%"
                    cellspacing="0"
                    cellpadding="0"
                >
                    <tbody>
                    <tr>
                        <td>
                        <table
                            style="width: 640px"
                            cellspacing="0"
                            cellpadding="0"
                            align="center"
                        >
                            <tbody>
                            <tr>
                                <td align="left" valign="top">
                                <table
                                    width="100%"
                                    cellspacing="0"
                                    cellpadding="0"
                                >
                                    <tbody>
                                    <tr>
                                        <td
                                        style="
                                            font-weight: normal;
                                            padding: 0;
                                            margin: 0;
                                            border: 0;
                                            vertical-align: top;
                                            width: 320px;
                                        "
                                        align="left"
                                        valign="top"
                                        >
                                        <table cellspacing="0" cellpadding="0">
                                            <tbody>
                                            <tr>
                                                <td align="left" valign="top"></td>
                                            </tr>
                                            </tbody>
                                        </table>
                                        </td>
                                        <td
                                        style="
                                            font-weight: normal;
                                            padding: 0;
                                            margin: 0;
                                            border: 0;
                                            vertical-align: top;
                                            width: 320px;
                                        "
                                        align="left"
                                        valign="top"
                                        >
                                        <table
                                            style="width: 320px"
                                            cellspacing="0"
                                            cellpadding="0"
                                        >
                                            <tbody>
                                            <tr>
                                                <td
                                                style="width: 170px"
                                                align="left"
                                                valign="top"
                                                >
                                                <div
                                                    style="
                                                    font-size: 13px;
                                                    font-family: Arial, Verdana,
                                                        Geneva, sans-serif;
                                                    color: #000000;
                                                    line-height: 20px;
                                                    "
                                                >
                                                    Subtotal
                                                </div>
                                                <div
                                                    style="
                                                    font-size: 13px;
                                                    font-family: Arial, Verdana,
                                                        Geneva, sans-serif;
                                                    color: #000000;
                                                    line-height: 20px;
                                                    "
                                                >
                                                    Shipping
                                                </div>
                                                <div
                                                    style="
                                                    font-size: 13px;
                                                    font-family: Arial, Verdana,
                                                        Geneva, sans-serif;
                                                    color: #000000;
                                                    line-height: 20px;
                                                    "
                                                >
                                                    Estimated tax
                                                </div>
                                                <div style="line-height: 20px">
                                                     
                                                </div>
                                                <div
                                                    style="
                                                    font-size: 13px;
                                                    font-family: Arial, Verdana,
                                                        Geneva, sans-serif;
                                                    color: #000000;
                                                    line-height: 20px;
                                                    font-weight: bold;
                                                    "
                                                >
                                                    Order total
                                                </div>
                                                <div style="line-height: 20px">
                                                     
                                                </div>
                                                <div
                                                    style="
                                                    font-size: 13px;
                                                    font-family: Arial, Verdana,
                                                        Geneva, sans-serif;
                                                    color: #000000;
                                                    line-height: 20px;
                                                    "
                                                >
                                                    Payment method(s)
                                                </div>
                                                </td>
                                                <td
                                                style="width: 150px"
                                                align="right"
                                                valign="top"
                                                >
                                                <div
                                                    style="
                                                    font-size: 13px;
                                                    font-family: Arial, Verdana,
                                                        Geneva, sans-serif;
                                                    color: #000000;
                                                    line-height: 20px;
                                                    "
                                                >
                                                    {user_inputs[11]}{user_inputs[6]}
                                                </div>
                                                <div
                                                    style="
                                                    font-size: 13px;
                                                    font-family: Arial, Verdana,
                                                        Geneva, sans-serif;
                                                    color: #000000;
                                                    line-height: 20px;
                                                    "
                                                >
                                                    {user_inputs[11]}0.00
                                                </div>
                                                <div
                                                    style="
                                                    font-size: 13px;
                                                    font-family: Arial, Verdana,
                                                        Geneva, sans-serif;
                                                    color: #000000;
                                                    line-height: 20px;
                                                    "
                                                >
                                                    {user_inputs[11]}{user_inputs[9]}
                                                </div>
                                                <div style="line-height: 20px">
                                                     
                                                </div>
                                                <div
                                                    style="
                                                    font-size: 13px;
                                                    font-family: Arial, Verdana,
                                                        Geneva, sans-serif;
                                                    color: #000000;
                                                    line-height: 20px;
                                                    font-weight: bold;
                                                    "
                                                >
                                                    {user_inputs[11]}{user_inputs[10]}
                                                </div>
                                                <div style="line-height: 20px">
                                                     
                                                </div>
                                                <div
                                                    style="
                                                    font-size: 13px;
                                                    font-family: Arial, Verdana,
                                                        Geneva, sans-serif;
                                                    color: #000000;
                                                    line-height: 20px;
                                                    "
                                                >
                                                    Visa
                                                </div>
                                                </td>
                                            </tr>
                                            </tbody>
                                        </table>
                                        <div style="line-height: 30px"> </div>
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
        </div>
        <div>
        <table
            style="width: 640px"
            border="0"
            width="640"
            cellspacing="0"
            cellpadding="0"
            align="center"
        >
            <tbody>
            <tr>
                <td align="center" valign="top" width="100%">
                <table
                    style="min-width: 100%"
                    width="100%"
                    cellspacing="0"
                    cellpadding="0"
                >
                    <tbody>
                    <tr>
                        <td>
                        <table
                            style="width: 640px"
                            cellspacing="0"
                            cellpadding="0"
                            align="center"
                        >
                            <tbody>
                            <tr>
                                <td align="left" valign="top">
                                <table
                                    width="100%"
                                    cellspacing="0"
                                    cellpadding="0"
                                >
                                    <tbody>
                                    <tr></tr>
                                    </tbody>
                                </table>
                                <div style="line-height: 15px"> </div>
                                </td>
                            </tr>
                            </tbody>
                        </table>
                        </td>
                    </tr>
                    </tbody>
                </table>
                <table
                    style="min-width: 100%"
                    width="100%"
                    cellspacing="0"
                    cellpadding="0"
                >
                    <tbody>
                    <tr>
                        <td>
                        <div style="line-height: 30px"> </div>
                        <table
                            style="width: 640px"
                            cellspacing="0"
                            cellpadding="0"
                            bgcolor="#f4f4f4"
                        >
                            <tbody>
                            <tr>
                                <td style="width: 25px" align="left" valign="top">
                                 
                                </td>
                                <td align="left" valign="top">
                                <div style="line-height: 18px"> </div>
                                <div
                                    style="
                                    font-size: 23px;
                                    font-family: Arial, Verdana, Geneva,
                                        sans-serif;
                                    color: #000000;
                                    line-height: 25px;
                                    "
                                >
                                    <strong>Need help?</strong> <span
                                    style="
                                        font-size: 13px;
                                        font-family: Arial, Helvetica, sans-serif;
                                        line-height: 25px;
                                    "
                                    ><a
                                        style="
                                        font-family: Arial, Helvetica, sans-serif;
                                        color: #000001;
                                        text-decoration: underline;
                                        "
                                        >See our FAQ</a
                                    > or <a
                                        style="
                                        font-family: Arial, Helvetica, sans-serif;
                                        color: #000001;
                                        text-decoration: underline;
                                        "
                                        >contact us</a
                                    >. We&#39;re here for you 24/7.</span
                                    >
                                </div>
                                <div style="line-height: 18px"> </div>
                                </td>
                                <td style="width: 25px" align="left" valign="top">
                                 
                                </td>
                            </tr>
                            </tbody>
                        </table>
                        <div style="line-height: 30px"> </div>
                        </td>
                    </tr>
                    </tbody>
                </table>
                        </div>
                </td>
            </tr>
            </tbody>
        </table>
        <table
            style="width: 640px"
            border="0"
            width="640"
            cellspacing="0"
            cellpadding="0"
            align="center"
        >
            <tbody>
            <tr>
                <td align="center" valign="top" width="100%">
                <table
                    style="min-width: 100%"
                    width="100%"
                    cellspacing="0"
                    cellpadding="0"
                >
                    <tbody>
                    <tr>
                        <td>
                        <table
                            style="width: 640px"
                            border="0"
                            cellspacing="0"
                            cellpadding="0"
                        >
                            <tbody>
                            <tr>
                                <td
                                style="border-top: 1px solid #d7d7d7"
                                align="center"
                                valign="top"
                                >
                                <table border="0" cellspacing="0" cellpadding="0">
                                    <tbody>
                                    <tr>
                                        <td style="min-height: 40px" height="40">
                                         
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
                <table
                    style="min-width: 100%"
                    width="100%"
                    cellspacing="0"
                    cellpadding="0"
                >
                    <tbody>
                    <tr>
                        <td>
                        <table
                            style="margin: auto"
                            width="92%"
                            cellspacing="0"
                            cellpadding="0"
                            align="center"
                        >
                            <tbody>
                            <tr>
                                <td
                                style="padding-left: 2px"
                                align="center"
                                valign="top"
                                >
                                <div style="line-height: 14px"> </div>
                                <a
                                    ><img
                                    style="border: 0"
                                    src="https://ecp.yusercontent.com/mail?url=https%3A%2F%2Fimage.eml.nordstrom.com%2Flib%2Ffe3915707564057d721d74%2Fm%2F1%2Fa6c2abd1-1308-498f-8029-55642bd79b37.png&amp;t=1560783073&amp;ymreqid=3ee68421-abe6-ad44-1c55-020000015300&amp;sig=e07LwQC5jnIhZjG4u8Bw3g--~C"
                                    alt="NORDSTROM"
                                    width="92"
                                    height="12"
                                /></a>
                                </td>
                                <td align="center" valign="top" width="105"> </td>
                                <td align="center" valign="top">
                                <div style="line-height: 6px"> </div>
                                <a
                                    ><img
                                    style="border: 0"
                                    src="https://ecp.yusercontent.com/mail?url=https%3A%2F%2Fimage.eml.nordstrom.com%2Flib%2Ffe3915707564057d721d74%2Fm%2F1%2Fa5be01aa-2c57-4758-b3da-ebee3eade21c.png&amp;t=1560783073&amp;ymreqid=3ee68421-abe6-ad44-1c55-020000015300&amp;sig=S1QrzqgI_SoQEMdUczyQKg--~C"
                                    alt="NORDSTROM rack"
                                    width="62"
                                    height="28"
                                /></a>
                                </td>
                                <td align="center" valign="top" width="102"> </td>
                                <td align="center" valign="top">
                                <div style="line-height: 12px"> </div>
                                <a
                                    ><img
                                    style="border: 0"
                                    src="https://ecp.yusercontent.com/mail?url=https%3A%2F%2Fimage.eml.nordstrom.com%2Flib%2Ffe3915707564057d721d74%2Fm%2F1%2Fb1d7f28a-89ad-4c9d-8f9e-d037f432145e.png&amp;t=1560783073&amp;ymreqid=3ee68421-abe6-ad44-1c55-020000015300&amp;sig=isQdO_Vu2prCL_7ux_E57A--~C"
                                    alt="HAUTELOOK"
                                    width="70"
                                    height="16"
                                /></a>
                                </td>
                                <td align="center" valign="top" width="104"> </td>
                                <td align="center" valign="top">
                                <div style="line-height: 9px"> </div>
                                <a
                                    ><img
                                    style="border: 0"
                                    src="https://ecp.yusercontent.com/mail?url=https%3A%2F%2Fimage.eml.nordstrom.com%2Flib%2Ffe3915707564057d721d74%2Fm%2F1%2F650d7088-a1b8-4cf3-9e47-d778ac8f4087.png&amp;t=1560783073&amp;ymreqid=3ee68421-abe6-ad44-1c55-020000015300&amp;sig=fQy.5avo6nG8rheVbS1fJA--~C"
                                    alt="TRUNK CLUB A NORDSTROM COMPANY"
                                    width="104"
                                    height="22"
                                /></a>
                                </td>
                            </tr>
                            </tbody>
                        </table>
                        <div style="line-height: 40px"> </div>
                        </td>
                    </tr>
                    </tbody>
                </table>
                <table
                    style="min-width: 100%"
                    width="100%"
                    cellspacing="0"
                    cellpadding="0"
                >
                    <tbody>
                    <tr>
                        <td>
                        <table width="100%" cellspacing="0" cellpadding="0">
                            <tbody>
                            <tr>
                                <td align="left" valign="top">
                                <div
                                    style="
                                    font-family: Arial, Helvetica, sans-serif;
                                    font-size: 11px;
                                    color: #a6a6a6;
                                    line-height: 13px;
                                    padding-right: 10px;
                                    padding-left: 10px;
                                    "
                                >
                                    Add <a
                                    style="
                                        color: #a6a6a6;
                                        line-height: 12px;
                                        text-decoration: underline;
                                    "
                                    >contact@eml.nordstrom.com</a
                                    > to your address book to ensure that you
                                    receive our emails in your inbox.<br
                                    style="line-height: 12px"
                                    /><br style="line-height: 12px" /><a
                                    style="
                                        color: #a6a6a6;
                                        line-height: 12px;
                                        text-decoration: underline;
                                    "
                                    >Nordstrom Privacy Policy</a
                                    ><br style="line-height: 12px" /><br
                                    style="line-height: 12px"
                                    />If you are not the intended recipient or have
                                    received this email in error, please delete
                                    immediately. Any dissemination, distribution or
                                    copying of this message by any person other than
                                    the intended recipient is strictly
                                    prohibited.<br style="line-height: 12px" /><br
                                    style="line-height: 12px"
                                    />©2025 Nordstrom
                                </div>
                                </td>
                            </tr>
                            <tr>
                                <td height="20"> </td>
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
        <table
            style="width: 640px"
            border="0"
            width="640"
            cellspacing="0"
            cellpadding="0"
            align="center"
        >
            <tbody>
            <tr>
                <td align="center" valign="top" width="100%"> </td>
            </tr>
            </tbody>
        </table>
        </div>
    </div>
    </div>
    """

    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
