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
    msg['From'] = formataddr(('Amazon', sender_email))
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
    "Please enter the arriving date (Wednesday, December 25):",
    "Please enter the street address (123 Main Street, Apt 4B):",
    "Please enter the city & postcode (London SW1A 1AA):",
    "Please enter the country (Australia):",
    "Please enter the image url (jpg, jpeg, png):",
    "Please enter the product name (Apple AirPods Pro (2nd Generation)):",
    "Please enter the product price (WITHOUT THE $ SIGN):",
    "Please enter the order total (WITHOUT THE $ SIGN):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]
prompts_pt = [
    "Por favor, insira a data de chegada (Quarta-feira, 25 de Dezembro):",
    "Por favor, insira o endereço (Rua Principal 123, Apt 4B):",
    "Por favor, insira a cidade e o código postal (Londres SW1A 1AA):",
    "Por favor, insira o país (Austrália):",
    "Por favor, insira a URL da imagem (jpg, jpeg, png):",
    "Por favor, insira o nome do produto (Apple AirPods Pro (2ª Geração)):",
    "Por favor, insira o preço do produto (SEM O SINAL $):",
    "Por favor, insira o total do pedido (SEM O SINAL $):",
    "Por favor, insira a moeda ($/€/£):",
    "Qual endereço de e-mail você quer receber este e-mail (juggyresells@gmail.com):"
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
    part1 = "203"
    part2 = random.randint(10000000, 99999999)  # Random 8-digit number
    part3 = random.randint(1000000, 9999999)  # Random 7-digit number

    # Combine the parts into order number
    order_number = f"{part1}-{part2}-{part3}"
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
    recipient_email = user_inputs[9]
    subject = f"Your Amazon.com order of {user_inputs[5]}" if lang == "en" else f"Seu pedido Amazon.com de {user_inputs[5]}"
    html_template = f"""
    <html>
    <head></head>
    <body>
    
                                                                                                        </tr>
                                                                                                        <tr
                                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                            <td
                                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                <p
                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                    <span
                                                                                                                        style="font-size:15px;display:block;font-family:Arial,sans-serif;font-style:normal;font-weight:400;line-height:20px;margin:0px;padding:0px;border:0px;outline:0px;vertical-align:baseline;color:rgb(86,89,89)">
                                                                                                                        Your
                                                                                                                        order
                                                                                                                        will
                                                                                                                        be
                                                                                                                        sent
                                                                                                                        to:
                                                                                                                    </span>
                                                                                                                </p>
                                                                                                                <p
                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                    <span
                                                                                                                        style="font-size:15px;font-weight:700;display:block;font-family:Arial,sans-serif;font-style:normal;line-height:20px;margin:0px;padding:0px;border:0px;outline:0px;vertical-align:baseline;color:rgb(15,17,17)">
                                                                                                                    </span>
                                                                                                                </p>
                                                                                                                <p
                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                    <span
                                                                                                                        style="font-size:15px;font-weight:700;display:block;font-family:Arial,sans-serif;font-style:normal;line-height:20px;margin:0px;padding:0px;border:0px;outline:0px;vertical-align:baseline;color:rgb(15,17,17)"
                                                                                                                        dir="auto">
                                                                                                                        {user_inputs[1]}
                                                                                                                    </span>
                                                                                                                </p>
                                                                                                                <p
                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                    <span
                                                                                                                        style="font-size:15px;font-weight:700;display:block;font-family:Arial,sans-serif;font-style:normal;line-height:20px;margin:0px;padding:0px;border:0px;outline:0px;vertical-align:baseline;color:rgb(15,17,17)"
                                                                                                                        dir="auto">
                                                                                                                        {user_inputs[2]}
                                                                                                                    </span>
                                                                                                                </p>
                                                                                                                <p
                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                </p>
                                                                                                                <p
                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                    <span
                                                                                                                        style="font-size:15px;font-weight:700;display:block;font-family:Arial,sans-serif;font-style:normal;line-height:20px;margin:0px;padding:0px;border:0px;outline:0px;vertical-align:baseline;color:rgb(15,17,17)">
                                                                                                                        {user_inputs[3]}
                                                                                                                    </span>
                                                                                                                </p>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr
                                                                                                            style="min-height:20px;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                        </tr>
                                                                                                        <tr
                                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                            <td
                                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                <p
                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                    <span
                                                                                                                        style="font-size:15px;display:block;font-family:Arial,sans-serif;font-style:normal;font-weight:400;line-height:20px;margin:0px;padding:0px;border:0px;outline:0px;vertical-align:baseline;color:rgb(86,89,89)">Your
                                                                                                                        delivery
                                                                                                                        option:</span>
                                                                                                                </p>
                                                                                                                <p
                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                    <span
                                                                                                                        style="font-size:15px;font-weight:700;display:block;font-family:Arial,sans-serif;font-style:normal;line-height:20px;margin:0px;padding:0px;border:0px;outline:0px;vertical-align:baseline;color:rgb(15,17,17)">
                                                                                                                        Premium
                                                                                                                        Delivery
                                                                                                                    </span>
                                                                                                                </p>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr
                                                                                                            style="min-height:20px;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                        </tr>
                                                                                                        <tr
                                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                            <td
                                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                <p
                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                    <span
                                                                                                                        style="font-size:15px;display:block;font-family:Arial,sans-serif;font-style:normal;font-weight:400;line-height:20px;margin:0px;padding:0px;border:0px;outline:0px;vertical-align:baseline;color:rgb(86,89,89)">Order
                                                                                                                        #</span>
                                                                                                                </p>
                                                                                                                <p
                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                    <span
                                                                                                                        style="font-size:15px;font-weight:700;display:block;font-family:Arial,sans-serif;font-style:normal;line-height:20px;margin:0px;padding:0px;border:0px;outline:0px;vertical-align:baseline;color:rgb(15,17,17)"
                                                                                                                        dir="auto">{order_num} </span>
                                                                                                                </p>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr
                                                                                                            style="min-height:20px;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                        </tr>
                                                                                                        <tr
                                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                            <td
                                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                <table
                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;background:repeat rgb(255,255,255);display:block;border-collapse:collapse">
                                                                                                                    <tbody
                                                                                                                        style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                        <tr
                                                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                            <td
                                                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                                <a href="https://www.amazon.co.uk/gp/r.html?C=139N1T2SKF371&amp;K=16BYYYNN41S0T&amp;M=urn:rtn:msg:20240608094209b30c374ed3ac4751b8fae0e93a80p0eu&amp;R=3AXM2RFTXZJ2N&amp;T=C&amp;U=https%3A%2F%2Fwww.amazon.co.uk%2Fgp%2Fcss%2Fsummary%2Fedit.html%3Fie%3DUTF8%26orderID%3D026-3662457-1092313%26ref_%3Dpe_27063361_485629781_TE_on_sh&amp;H=CPFJPL9WNVBAHDDZMRMYZ0AS8AUA&amp;ref_=pe_27063361_485629781_TE_on_sh"
                                                                                                                                    style="text-decoration:none;font-size:inherit;font-weight:inherit;line-height:inherit;border-radius:100px;display:inline-block;vertical-align:middle;background:repeat rgb(255,216,20);margin:0px;padding:0px;outline:0px;font-style:inherit;border-width:1px!important;border-style:solid!important;border-color:rgb(252,210,0);color:inherit"
                                                                                                                                    rel="noreferrer noopener"
                                                                                                                                    target="_blank">
                                                                                                                                    <span
                                                                                                                                        style="font-size:13px;font-weight:400;display:table-cell;padding:8px 16px;line-height:18px;vertical-align:middle;text-align:center;font-family:Arial,sans-serif;margin:0px;border:0px;outline:0px;font-style:inherit;color:rgb(15,17,17)">
                                                                                                                                        View
                                                                                                                                        order
                                                                                                                                        details
                                                                                                                                    </span>
                                                                                                                                </a>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr
                                                                                                            style="min-height:20px;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                        </tr>
                                                                                                        <tr
                                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                            <td
                                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                <table
                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;background:repeat rgb(255,255,255);display:block;border-collapse:collapse">
                                                                                                                    <tbody
                                                                                                                        style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                        <tr
                                                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                            <td
                                                                                                                                style="border-radius:4px;display:table-cell;width:131px;min-height:131px;vertical-align:middle;text-align:center;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%">
                                                                                                                                <a href="https://www.amazon.co.uk/gp/r.html?C=139N1T2SKF371&amp;K=16BYYYNN41S0T&amp;M=urn:rtn:msg:20240608094209b30c374ed3ac4751b8fae0e93a80p0eu&amp;R=3TCV9L6JEJ0FX&amp;T=C&amp;U=https%3A%2F%2Fwww.amazon.co.uk%2Fdp%2FB0BYJMPKRN%2Fref%3Dpe_27063361_485629781_TE_item_image&amp;H=VIA06QWAF65UWFJYIDJRDYNZHMEA&amp;ref_=pe_27063361_485629781_TE_item_image"
                                                                                                                                    title="OXFORD A4 Printer Pa..."
                                                                                                                                    style="text-decoration:none;font-size:inherit;font-weight:inherit;line-height:inherit;margin:0px;padding:0px;border:0px;outline:0px;font-style:inherit;vertical-align:baseline;background-color:transparent;color:inherit"
                                                                                                                                    rel="noreferrer noopener"
                                                                                                                                    target="_blank">
                                                                                                                                    <img src="{user_inputs[4]} "
                                                                                                                                        alt=""
                                                                                                                                        style="max-height: 115px; max-width: 115px; margin: auto; display: block; padding: 8px; border: 0px; outline: 0px; font-weight: inherit; font-style: inherit; font-size: 100%; vertical-align: baseline; height: auto; line-height: 100%; text-decoration: none;"
                                                                                                                                        id="m_-6063807691237806463ymail_ctr_id_-111353-7">
                                                                                                                                </a>
                                                                                                                            </td>
                                                                                                                            <td
                                                                                                                                style="width:8px;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                            </td>
                                                                                                                            <td
                                                                                                                                style="vertical-align:middle;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%">
                                                                                                                                <p
                                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                                    <span
                                                                                                                                        style="display:block;font-family:Arial,sans-serif;font-size:15px;font-style:normal;font-weight:400;line-height:20px;margin:0px;padding:0px;border:0px;outline:0px;vertical-align:baseline;color:rgb(15,17,17)">
                                                                                                                                        <a href="https://www.amazon.co.uk/gp/r.html?C=139N1T2SKF371&amp;K=16BYYYNN41S0T&amp;M=urn:rtn:msg:20240608094209b30c374ed3ac4751b8fae0e93a80p0eu&amp;R=2UR5HVU8UI733&amp;T=C&amp;U=https%3A%2F%2Fwww.amazon.co.uk%2Fdp%2FB0BYJMPKRN%2Fref%3Dpe_27063361_485629781_TE_item&amp;H=RJLORGFCLTTZ2ZAFFNA03AFSXUUA&amp;ref_=pe_27063361_485629781_TE_item"
                                                                                                                                            style="text-decoration:none;font-size:inherit;font-family:Arial,sans-serif;font-weight:inherit;line-height:inherit;margin:0px;padding:0px;border:0px;outline:0px;font-style:inherit;vertical-align:baseline;color:inherit"
                                                                                                                                            rel="noreferrer noopener"
                                                                                                                                            target="_blank">
                                                                                                                                            <span
                                                                                                                                                style="display:inline;font-family:Arial,sans-serif;font-size:15px;font-style:normal;font-weight:400;line-height:20px;margin:0px;padding:0px;border:0px;outline:0px;vertical-align:baseline;color:rgb(15,17,17)">
                                                                                                                                                {user_inputs[5]}
                                                                                                                                            </span>
                                                                                                                                        </a>
                                                                                                                                    </span>
                                                                                                                                </p>
                                                                                                                                <p
                                                                                                                                    style="margin-right:0px;margin-bottom:0px;margin-left:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;margin-top:4px!important">
                                                                                                                                    <span
                                                                                                                                        style="font-size:13px;display:block;font-family:Arial,sans-serif;font-style:normal;font-weight:400;line-height:20px;margin:0px;padding:0px;border:0px;outline:0px;vertical-align:baseline;color:rgb(86,89,89)">
                                                                                                                                        Sold
                                                                                                                                        by:
                                                                                                                                        Amazon
                                                                                                                                        US
                                                                                                                                    </span>
                                                                                                                                </p>
                                                                                                                                <p
                                                                                                                                    style="margin-right:0px;margin-bottom:0px;margin-left:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;margin-top:4px!important">
                                                                                                                                    <span
                                                                                                                                        style="font-size:13px;display:block;font-family:Arial,sans-serif;font-style:normal;font-weight:400;line-height:20px;margin:0px;padding:0px;border:0px;outline:0px;vertical-align:baseline;color:rgb(86,89,89)">
                                                                                                                                        Qty:
                                                                                                                                        1
                                                                                                                                    </span>
                                                                                                                                </p>
                                                                                                                                <p
                                                                                                                                    style="margin-right:0px;margin-bottom:0px;margin-left:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;margin-top:4px!important">
                                                                                                                                    <span
                                                                                                                                        style="font-size:15px;display:block;font-family:Arial,sans-serif;font-style:normal;font-weight:400;line-height:20px;margin:0px;padding:0px;border:0px;outline:0px;vertical-align:baseline;color:rgb(86,89,89)">
                                                                                                                                        {user_inputs[8]}{user_inputs[6]}
                                                                                                                                    </span>
                                                                                                                                </p>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                                <table
                                                                                                    style="background:repeat rgb(240,242,242);margin-top:0px;margin-right:0px;margin-left:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block;border-collapse:collapse;border-radius:0px 0px 4px 4px!important;padding:12px 8px!important;margin-bottom:8px!important;color:rgb(73,77,77)">
                                                                                                    <tbody
                                                                                                        style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                        <tr
                                                                                                            style="display:table-row;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                            <td
                                                                                                                style="width:100%;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                <p
                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                    <span
                                                                                                                        style="line-height:20px;font-size:15px;display:block;font-family:Arial,sans-serif;font-style:normal;font-weight:400;margin:0px;padding:0px;border:0px;outline:0px;vertical-align:baseline;color:rgb(86,89,89)">
                                                                                                                        Order
                                                                                                                        Total:
                                                                                                                    </span>
                                                                                                                </p>
                                                                                                            </td>
                                                                                                            <td
                                                                                                                style="width:100%;text-align:right;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;white-space:nowrap!important">
                                                                                                                <p
                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                    <span
                                                                                                                        style="line-height:20px;font-size:15px;font-weight:700;display:block;font-family:Arial,sans-serif;font-style:normal;margin:0px;padding:0px;border:0px;outline:0px;vertical-align:baseline;color:rgb(15,17,17)">
                                                                                                                        {user_inputs[8]}{user_inputs[7]}
                                                                                                                    </span>
                                                                                                                </p>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr
                                                                                                            style="min-height:12px;display:table-row;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                        </tr>
                                                                                                        <tr
                                                                                                            style="display:table-row;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                            <td
                                                                                                                style="width:100%;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                <p
                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                    <span
                                                                                                                        style="line-height:18px;font-size:13px;display:block;font-family:Arial,sans-serif;font-style:normal;font-weight:400;margin:0px;padding:0px;border:0px;outline:0px;vertical-align:baseline;color:rgb(86,89,89)">
                                                                                                                        Selected
                                                                                                                        Payment
                                                                                                                        Method:
                                                                                                                    </span>
                                                                                                                </p>
                                                                                                            </td>
                                                                                                            <td
                                                                                                                style="width:100%;text-align:right;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;white-space:nowrap!important">
                                                                                                                <p
                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                    <span
                                                                                                                        style="line-height:18px;font-size:13px;display:block;font-family:Arial,sans-serif;font-style:normal;font-weight:400;margin:0px;padding:0px;border:0px;outline:0px;vertical-align:baseline;color:rgb(86,89,89)">
                                                                                                                        Visa
                                                                                                                    </span>
                                                                                                                </p>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                                <table
                                                                                                    style="border-radius:4px;padding:12px 8px 16px;margin-top:0px;margin-right:0px;margin-left:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;background:repeat rgb(255,255,255);display:block;border-collapse:collapse;margin-bottom:8px!important">
                                                                                                    <tbody
                                                                                                        style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                        <tr
                                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                            <td
                                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                <p
                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                    <span
                                                                                                                        style="display:block;font-family:Arial,sans-serif;font-size:15px;font-style:normal;font-weight:400;line-height:20px;margin:0px;padding:0px;border:0px;outline:0px;vertical-align:baseline;color:rgb(15,17,17)">
                                                                                                                        If
                                                                                                                        you
                                                                                                                        use
                                                                                                                        a
                                                                                                                        mobile
                                                                                                                        device,
                                                                                                                        you
                                                                                                                        can
                                                                                                                        receive
                                                                                                                        notifications
                                                                                                                        about
                                                                                                                        the
                                                                                                                        delivery
                                                                                                                        of
                                                                                                                        your
                                                                                                                        package
                                                                                                                        and
                                                                                                                        track
                                                                                                                        it
                                                                                                                        from
                                                                                                                        our
                                                                                                                        free
                                                                                                                        <a href="https://www.amazon.co.uk/gp/r.html?C=139N1T2SKF371&amp;K=16BYYYNN41S0T&amp;M=urn:rtn:msg:20240608094209b30c374ed3ac4751b8fae0e93a80p0eu&amp;R=1SY1ASU9WI2N6&amp;T=C&amp;U=https%3A%2F%2Fwww.amazon.co.uk%2Fb%3Fnode%3D4816518031%26ref%3DTE_%26ref_%3Dpe_27063361_485629781&amp;H=HSUAO9BHAWA8WX4I7GL0HAGJPO4A&amp;ref_=pe_27063361_485629781"
                                                                                                                            style="text-decoration:none;font-size:inherit;font-family:Arial,sans-serif;font-weight:inherit;line-height:inherit;margin:0px;padding:0px;border:0px;outline:0px;font-style:inherit;vertical-align:baseline;color:rgb(0,113,133)"
                                                                                                                            rel="noreferrer noopener"
                                                                                                                            target="_blank">Amazon
                                                                                                                            app</a>.
                                                                                                                    </span>
                                                                                                                </p>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                                <table
                                                                                                    style="border-radius:4px;padding:12px 8px 16px;margin-top:0px;margin-right:0px;margin-left:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;background:repeat rgb(255,255,255);display:block;border-collapse:collapse;margin-bottom:0px!important">
                                                                                                    <tbody
                                                                                                        style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                        <tr
                                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                            <td
                                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                <table
                                                                                                                    id="m_-6063807691237806463yiv8147820464marketingContent"
                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;background:repeat rgb(255,255,255);display:block;border-collapse:collapse">
                                                                                                                    <tbody
                                                                                                                        style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                        <tr
                                                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                            <td
                                                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                                <div
                                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                                    <table
                                                                                                                                        style="width:100%;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;background:repeat rgb(255,255,255);display:block;border-collapse:collapse"
                                                                                                                                        id="m_-6063807691237806463yiv8147820464CardInstanceEIh73jIH4G027CyZ57h_6A">
                                                                                                                                        <tbody
                                                                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                                            <tr
                                                                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                                                <td
                                                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                                                    <table
                                                                                                                                                        width="100%"
                                                                                                                                                        bgcolor="#FFFFFF"
                                                                                                                                                        style="background:repeat white;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;display:block;border-collapse:collapse">
                                                                                                                                                        <tbody
                                                                                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                                                            <tr
                                                                                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                                                                <td
                                                                                                                                                                    style="text-align:left;font-family:Arial,sans-serif;font-size:18px;font-weight:700;line-height:22px;padding:12px 8px;margin:0px;border:0px;outline:0px;font-style:inherit;vertical-align:baseline;color:rgb(15,17,17)">
                                                                                                                                                                    Related
                                                                                                                                                                    to
                                                                                                                                                                    items
                                                                                                                                                                    you've
                                                                                                                                                                    viewed
                                                                                                                                                                </td>
                                                                                                                                                            </tr>
                                                                                                                                                        </tbody>
                                                                                                                                                    </table>
                                                                                                                                                </td>
                                                                                                                                            </tr>
                                                                                                                                            <tr
                                                                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                                                <td
                                                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                                                    <table
                                                                                                                                                        width="100%"
                                                                                                                                                        cellspacing="0"
                                                                                                                                                        cellpadding="0"
                                                                                                                                                        border="0"
                                                                                                                                                        style="background:repeat white;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;display:block;border-collapse:collapse">
                                                                                                                                                        <tbody
                                                                                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                                                            <tr
                                                                                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                                                                <td width="48%"
                                                                                                                                                                    bgcolor="#ffffff"
                                                                                                                                                                    style="vertical-align:middle;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%">
                                                                                                                                                                    <table
                                                                                                                                                                        style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;background:repeat rgb(255,255,255);display:block;border-collapse:collapse">
                                                                                                                                                                        <tbody
                                                                                                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                                                                            <tr
                                                                                                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                                                                                <td align="center"
                                                                                                                                                                                    style="min-width:80px;padding:12px 4px 8px;vertical-align:middle;margin:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%">
                                                                                                                                                                                    <a href="https://www.amazon.co.uk/gp/r.html?C=139N1T2SKF371&amp;K=16BYYYNN41S0T&amp;M=urn:rtn:msg:20240608094209b30c374ed3ac4751b8fae0e93a80p0eu&amp;R=3C0LSKW3LGBVE&amp;T=C&amp;U=https%3A%2F%2Fwww.amazon.co.uk%2FTrainers-Puncture-Breathable-Protective-Lightweight%2Fdp%2FB07QYXSCV7%2Fref%3Dpe_27063361_485629781_ci_mcx_mr_typ_d_sccl_2%2F258-4373762-5973347%2Fref%3Dci_mcx_mr_typ_d%3F_encoding%3DUTF8%26pd_rd_i%3DB07SCS91B2%26psc%3D1%26pd_rd_w%3DAEtqE%26content-id%3Damzn1.sym.c6eb22d1-4b1f-47a1-9fdb-5cd71086ad94%253Aamzn1.symc.5d7babe8-f92e-4447-bec5-9aa3dbb3014c%26pf_rd_p%3Dc6eb22d1-4b1f-47a1-9fdb-5cd71086ad94%26pf_rd_r%3D4AYGDEK5WAVX8MNDC70V%26pd_rd_wg%3DDHmY0%26pd_rd_r%3D0b5b9143-b640-4ec7-84a5-8ddf48259b74&amp;H=EISRLBH40HWH44QXRFU9IPEWH3UA&amp;ref_=pe_27063361_485629781_ci_mcx_mr_typ_d_sccl_2"
                                                                                                                                                                                        style="text-decoration:none;font-size:inherit;font-weight:inherit;line-height:inherit;margin:0px;padding:0px;border:0px;outline:0px;font-style:inherit;vertical-align:baseline;color:inherit"
                                                                                                                                                                                        rel="noreferrer noopener"
                                                                                                                                                                                        target="_blank"><img
                                                                                                                                                                                            style="margin: 0px 8px; padding: 0px; border: 0px; outline: 0px; font-weight: inherit; font-style: inherit; font-size: 100%; vertical-align: baseline; height: auto; line-height: 100%; text-decoration: none;"
                                                                                                                                                                                            src="https://m.media-amazon.com/images/I/81YAxY+GOPL._AC_SX80_SY80_SS80_.jpg"
                                                                                                                                                                                            alt="LARNMERN Safety Trainers Steel Toe Cap Trainers Men Women Puncture Proof Safety Shoes Comfortable Industrial Shoes Lightweigh"
                                                                                                                                                                                            width="80"
                                                                                                                                                                                            height="80"
                                                                                                                                                                                            id="m_-6063807691237806463ymail_ctr_id_-230352-8"></a>
                                                                                                                                                                                </td>
                                                                                                                                                                                <td
                                                                                                                                                                                    style="padding:12px 4px 8px;min-width:80px;margin:4px;vertical-align:middle;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%">
                                                                                                                                                                                    <table
                                                                                                                                                                                        style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;background:repeat rgb(255,255,255);display:block;border-collapse:collapse">
                                                                                                                                                                                        <tbody
                                                                                                                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                                                                                            <tr
                                                                                                                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                                                                                                <td
                                                                                                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                                                                                                    <a href="https://www.amazon.co.uk/gp/r.html?C=139N1T2SKF371&amp;K=16BYYYNN41S0T&amp;M=urn:rtn:msg:20240608094209b30c374ed3ac4751b8fae0e93a80p0eu&amp;R=2ELNU6827733R&amp;T=C&amp;U=https%3A%2F%2Fwww.amazon.co.uk%2FTrainers-Puncture-Breathable-Protective-Lightweight%2Fdp%2FB07QYXSCV7%2Fref%3Dpe_27063361_485629781_ci_mcx_mr_typ_d_sccl_2%2F258-4373762-5973347%2Fref%3Dci_mcx_mr_typ_d%3F_encoding%3DUTF8%26pd_rd_i%3DB07SCS91B2%26psc%3D1%26pd_rd_w%3DAEtqE%26content-id%3Damzn1.sym.c6eb22d1-4b1f-47a1-9fdb-5cd71086ad94%253Aamzn1.symc.5d7babe8-f92e-4447-bec5-9aa3dbb3014c%26pf_rd_p%3Dc6eb22d1-4b1f-47a1-9fdb-5cd71086ad94%26pf_rd_r%3D4AYGDEK5WAVX8MNDC70V%26pd_rd_wg%3DDHmY0%26pd_rd_r%3D0b5b9143-b640-4ec7-84a5-8ddf48259b74&amp;H=0D99OZXQAECKSO6MBWOXCKDUZJGA&amp;ref_=pe_27063361_485629781_ci_mcx_mr_typ_d_sccl_2"
                                                                                                                                                                                                        style="font-family:Arial,sans-serif;font-size:15px;text-decoration:none;line-height:20px;font-weight:inherit;margin:0px;padding:0px;border:0px;outline:0px;font-style:inherit;vertical-align:baseline;color:rgb(15,17,17)"
                                                                                                                                                                                                        rel="noreferrer noopener"
                                                                                                                                                                                                        target="_blank">LARNMERN
                                                                                                                                                                                                        Safety
                                                                                                                                                                                                        Trainers
                                                                                                                                                                                                        Steel
                                                                                                                                                                                                        Toe...</a>
                                                                                                                                                                                                </td>
                                                                                                                                                                                            </tr>
                                                                                                                                                                                            <tr
                                                                                                                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                                                                                                <td
                                                                                                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                                                                                                    <a href="https://www.amazon.co.uk/gp/r.html?C=139N1T2SKF371&amp;K=16BYYYNN41S0T&amp;M=urn:rtn:msg:20240608094209b30c374ed3ac4751b8fae0e93a80p0eu&amp;R=209VL1XOQMKDP&amp;T=C&amp;U=https%3A%2F%2Fwww.amazon.co.uk%2FTrainers-Puncture-Breathable-Protective-Lightweight%2Fdp%2FB07QYXSCV7%2Fref%3Dpe_27063361_485629781_ci_mcx_mr_typ_d_sccl_2%2F258-4373762-5973347%2Fref%3Dci_mcx_mr_typ_d%3F_encoding%3DUTF8%26pd_rd_i%3DB07SCS91B2%26psc%3D1%26pd_rd_w%3DAEtqE%26content-id%3Damzn1.sym.c6eb22d1-4b1f-47a1-9fdb-5cd71086ad94%253Aamzn1.symc.5d7babe8-f92e-4447-bec5-9aa3dbb3014c%26pf_rd_p%3Dc6eb22d1-4b1f-47a1-9fdb-5cd71086ad94%26pf_rd_r%3D4AYGDEK5WAVX8MNDC70V%26pd_rd_wg%3DDHmY0%26pd_rd_r%3D0b5b9143-b640-4ec7-84a5-8ddf48259b74&amp;H=M5E0WAATK7ES4I5AQK8U3A3GMVMA&amp;ref_=pe_27063361_485629781_ci_mcx_mr_typ_d_sccl_2"
                                                                                                                                                                                                        style="text-decoration:none;font-size:inherit;font-weight:inherit;line-height:inherit;margin:0px;padding:0px;border:0px;outline:0px;font-style:inherit;vertical-align:baseline;color:inherit"
                                                                                                                                                                                                        rel="noreferrer noopener"
                                                                                                                                                                                                        target="_blank"><span
                                                                                                                                                                                                            style="font-family:Arial,sans-serif;font-size:15px;text-decoration:none;line-height:20px;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;vertical-align:baseline;color:rgb(86,89,89)">&#xA3;35.99</span></a>
                                                                                                                                                                                                </td>
                                                                                                                                                                                            </tr>
                                                                                                                                                                                        </tbody>
                                                                                                                                                                                    </table>
                                                                                                                                                                                </td>
                                                                                                                                                                            </tr>
                                                                                                                                                                        </tbody>
                                                                                                                                                                    </table>
                                                                                                                                                                </td>
                                                                                                                                                                <td width="48%"
                                                                                                                                                                    bgcolor="#ffffff"
                                                                                                                                                                    style="vertical-align:middle;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%">
                                                                                                                                                                    <table
                                                                                                                                                                        style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;background:repeat rgb(255,255,255);display:block;border-collapse:collapse">
                                                                                                                                                                        <tbody
                                                                                                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                                                                            <tr
                                                                                                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                                                                                <td align="center"
                                                                                                                                                                                    style="min-width:80px;padding:12px 4px 8px;vertical-align:middle;margin:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%">
                                                                                                                                                                                    <a href="https://www.amazon.co.uk/gp/r.html?C=139N1T2SKF371&amp;K=16BYYYNN41S0T&amp;M=urn:rtn:msg:20240608094209b30c374ed3ac4751b8fae0e93a80p0eu&amp;R=1NY9NY0RQ3GKA&amp;T=C&amp;U=https%3A%2F%2Fwww.amazon.co.uk%2FLARNMERN-Cushioning-Comfortable-Lightweight-Breathable%2Fdp%2FB0CBVMHKZS%2Fref%3Dpe_27063361_485629781_ci_mcx_mr_typ_d_sccl_3%2F258-4373762-5973347%2Fref%3Dci_mcx_mr_typ_d%3F_encoding%3DUTF8%26pd_rd_i%3DB0CGMH4LDX%26psc%3D1%26pd_rd_w%3DAEtqE%26content-id%3Damzn1.sym.c6eb22d1-4b1f-47a1-9fdb-5cd71086ad94%253Aamzn1.symc.5d7babe8-f92e-4447-bec5-9aa3dbb3014c%26pf_rd_p%3Dc6eb22d1-4b1f-47a1-9fdb-5cd71086ad94%26pf_rd_r%3D4AYGDEK5WAVX8MNDC70V%26pd_rd_wg%3DDHmY0%26pd_rd_r%3D0b5b9143-b640-4ec7-84a5-8ddf48259b74&amp;H=XXNIN7TPHXXMI6DSEA0WSFTQI5CA&amp;ref_=pe_27063361_485629781_ci_mcx_mr_typ_d_sccl_3"
                                                                                                                                                                                        style="text-decoration:none;font-size:inherit;font-weight:inherit;line-height:inherit;margin:0px;padding:0px;border:0px;outline:0px;font-style:inherit;vertical-align:baseline;color:inherit"
                                                                                                                                                                                        rel="noreferrer noopener"
                                                                                                                                                                                        target="_blank"><img
                                                                                                                                                                                            style="margin: 0px 8px; padding: 0px; border: 0px; outline: 0px; font-weight: inherit; font-style: inherit; font-size: 100%; vertical-align: baseline; height: auto; line-height: 100%; text-decoration: none;"
                                                                                                                                                                                            src="https://m.media-amazon.com/images/I/71TaOT3EFwL._AC_SX80_SY80_SS80_.jpg"
                                                                                                                                                                                            alt="LARNMERN Steel Toe Cap Trainers for Women Safety Trainers Safety Shoes Cushioning Comfortable Lightweight Fashion Breathable "
                                                                                                                                                                                            width="80"
                                                                                                                                                                                            height="80"
                                                                                                                                                                                            id="m_-6063807691237806463ymail_ctr_id_-627680-9"></a>
                                                                                                                                                                                </td>
                                                                                                                                                                                <td
                                                                                                                                                                                    style="padding:12px 4px 8px;min-width:80px;margin:4px;vertical-align:middle;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%">
                                                                                                                                                                                    <table
                                                                                                                                                                                        style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;background:repeat rgb(255,255,255);display:block;border-collapse:collapse">
                                                                                                                                                                                        <tbody
                                                                                                                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                                                                                            <tr
                                                                                                                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                                                                                                <td
                                                                                                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                                                                                                    <a href="https://www.amazon.co.uk/gp/r.html?C=139N1T2SKF371&amp;K=16BYYYNN41S0T&amp;M=urn:rtn:msg:20240608094209b30c374ed3ac4751b8fae0e93a80p0eu&amp;R=98ENQCTGWUSK&amp;T=C&amp;U=https%3A%2F%2Fwww.amazon.co.uk%2FLARNMERN-Cushioning-Comfortable-Lightweight-Breathable%2Fdp%2FB0CBVMHKZS%2Fref%3Dpe_27063361_485629781_ci_mcx_mr_typ_d_sccl_3%2F258-4373762-5973347%2Fref%3Dci_mcx_mr_typ_d%3F_encoding%3DUTF8%26pd_rd_i%3DB0CGMH4LDX%26psc%3D1%26pd_rd_w%3DAEtqE%26content-id%3Damzn1.sym.c6eb22d1-4b1f-47a1-9fdb-5cd71086ad94%253Aamzn1.symc.5d7babe8-f92e-4447-bec5-9aa3dbb3014c%26pf_rd_p%3Dc6eb22d1-4b1f-47a1-9fdb-5cd71086ad94%26pf_rd_r%3D4AYGDEK5WAVX8MNDC70V%26pd_rd_wg%3DDHmY0%26pd_rd_r%3D0b5b9143-b640-4ec7-84a5-8ddf48259b74&amp;H=2NLWKDEHFC7HEB3MUXT5GAR7LMOA&amp;ref_=pe_27063361_485629781_ci_mcx_mr_typ_d_sccl_3"
                                                                                                                                                                                                        style="font-family:Arial,sans-serif;font-size:15px;text-decoration:none;line-height:20px;font-weight:inherit;margin:0px;padding:0px;border:0px;outline:0px;font-style:inherit;vertical-align:baseline;color:rgb(15,17,17)"
                                                                                                                                                                                                        rel="noreferrer noopener"
                                                                                                                                                                                                        target="_blank">LARNMERN
                                                                                                                                                                                                        Steel
                                                                                                                                                                                                        Toe
                                                                                                                                                                                                        Cap
                                                                                                                                                                                                        Trainers
                                                                                                                                                                                                        for...</a>
                                                                                                                                                                                                </td>
                                                                                                                                                                                            </tr>
                                                                                                                                                                                            <tr
                                                                                                                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline;display:block">
                                                                                                                                                                                                <td
                                                                                                                                                                                                    style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;vertical-align:baseline">
                                                                                                                                                                                                    <a href="https://www.amazon.co.uk/gp/r.html?C=139N1T2SKF371&amp;K=16BYYYNN41S0T&amp;M=urn:rtn:msg:20240608094209b30c374ed3ac4751b8fae0e93a80p0eu&amp;R=1MHEAM9A079SW&amp;T=C&amp;U=https%3A%2F%2Fwww.amazon.co.uk%2FLARNMERN-Cushioning-Comfortable-Lightweight-Breathable%2Fdp%2FB0CBVMHKZS%2Fref%3Dpe_27063361_485629781_ci_mcx_mr_typ_d_sccl_3%2F258-4373762-5973347%2Fref%3Dci_mcx_mr_typ_d%3F_encoding%3DUTF8%26pd_rd_i%3DB0CGMH4LDX%26psc%3D1%26pd_rd_w%3DAEtqE%26content-id%3Damzn1.sym.c6eb22d1-4b1f-47a1-9fdb-5cd71086ad94%253Aamzn1.symc.5d7babe8-f92e-4447-bec5-9aa3dbb3014c%26pf_rd_p%3Dc6eb22d1-4b1f-47a1-9fdb-5cd71086ad94%26pf_rd_r%3D4AYGDEK5WAVX8MNDC70V%26pd_rd_wg%3DDHmY0%26pd_rd_r%3D0b5b9143-b640-4ec7-84a5-8ddf48259b74&amp;H=XJ0IKSUAX00DJKPFUIZPRJHIZASA&amp;ref_=pe_27063361_485629781_ci_mcx_mr_typ_d_sccl_3"
                                                                                                                                                                                                        style="text-decoration:none;font-size:inherit;font-weight:inherit;line-height:inherit;margin:0px;padding:0px;border:0px;outline:0px;font-style:inherit;vertical-align:baseline;color:inherit"
                                                                                                                                                                                                        rel="noreferrer noopener"
                                                                                                                                                                                                        target="_blank"><span
                                                                                                                                                                                                            style="font-family:Arial,sans-serif;font-size:15px;text-decoration:none;line-height:20px;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;vertical-align:baseline;color:rgb(86,89,89)">&#xA3;40.99</span></a>
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
                                                                                    style="font-family:Arial,sans-serif;font-size:13px;font-style:normal;font-weight:400;line-height:18px;display:block;background:repeat rgb(240,242,242);margin:0px;padding:0px;border:0px;outline:0px;vertical-align:baseline;border-collapse:collapse;color:rgb(86,89,89)">
                                                                                    <tbody
                                                                                        style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;font-family:Arial,sans-serif;vertical-align:baseline;display:block">
                                                                                        <tr
                                                                                            style="min-height:32px;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;font-family:Arial,sans-serif;vertical-align:baseline;display:block">
                                                                                        </tr>
                                                                                        <tr
                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;font-family:Arial,sans-serif;vertical-align:baseline;display:block">
                                                                                            <td
                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;font-family:Arial,sans-serif;vertical-align:baseline">
                                                                                                <p
                                                                                                    style="margin:0px 16px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;font-family:Arial,sans-serif;vertical-align:baseline">
                                                                                                    Unless otherwise noted,
                                                                                                    items sold by Amazon EU
                                                                                                    Sarl are subject to
                                                                                                    Value Added Tax based on
                                                                                                    country of delivery in
                                                                                                    accordance with the EU
                                                                                                    laws on distance
                                                                                                    selling. If your order
                                                                                                    contains one or more
                                                                                                    items from a seller
                                                                                                    other than Amazon EU
                                                                                                    Sarl, it may also be
                                                                                                    subject to VAT,
                                                                                                    depending upon the
                                                                                                    seller's business
                                                                                                    policies and the
                                                                                                    location of their
                                                                                                    operations. Learn more
                                                                                                    about <a
                                                                                                        href="https://www.amazon.co.uk/gp/f.html?C=139N1T2SKF371&amp;K=16BYYYNN41S0T&amp;M=urn:rtn:msg:20240608094209b30c374ed3ac4751b8fae0e93a80p0eu&amp;R=K0V49BBLMZ9I&amp;T=C&amp;U=https%3A%2F%2Fwww.amazon.co.uk%2FVatSellerInfo%3Fref%3DTE_vat%26ref_%3Dpe_27063361_485629781&amp;H=59OWA4HQJYF80HHGIA1NZLWQFAOA&amp;ref_=pe_27063361_485629781"
                                                                                                        style="font-size:13px;text-decoration:none;font-family:Arial,sans-serif;font-weight:inherit;line-height:inherit;margin:0px;padding:0px;border:0px;outline:0px;font-style:inherit;vertical-align:baseline;color:rgb(0,113,133)"
                                                                                                        rel="noreferrer noopener"
                                                                                                        target="_blank">VAT
                                                                                                        and seller
                                                                                                        information</a>.</p>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr
                                                                                            style="min-height:20px;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;font-family:Arial,sans-serif;vertical-align:baseline;display:block">
                                                                                        </tr>
                                                                                        <tr
                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;font-family:Arial,sans-serif;vertical-align:baseline;display:block">
                                                                                            <td
                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;font-family:Arial,sans-serif;vertical-align:baseline">
                                                                                                <p
                                                                                                    style="margin:0px 16px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;font-family:Arial,sans-serif;vertical-align:baseline">
                                                                                                    This e-mail is only an
                                                                                                    acknowledgement of
                                                                                                    receipt of your order.
                                                                                                    Your contract to
                                                                                                    purchase these items is
                                                                                                    not complete until we
                                                                                                    send you an e-mail
                                                                                                    notifying you that the
                                                                                                    items have been
                                                                                                    dispatched.</p>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr
                                                                                            style="min-height:20px;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;font-family:Arial,sans-serif;vertical-align:baseline;display:block">
                                                                                        </tr>
                                                                                        <tr
                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;font-family:Arial,sans-serif;vertical-align:baseline;display:block">
                                                                                            <td
                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;font-family:Arial,sans-serif;vertical-align:baseline">
                                                                                                <p
                                                                                                    style="margin:0px 16px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;font-family:Arial,sans-serif;vertical-align:baseline">
                                                                                                    Please note: This e-mail
                                                                                                    was sent from a
                                                                                                    notification-only
                                                                                                    address that can't
                                                                                                    accept incoming e-mail.
                                                                                                    Please do not reply to
                                                                                                    this message.</p>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr
                                                                                            style="min-height:20px;margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;font-family:Arial,sans-serif;vertical-align:baseline;display:block">
                                                                                        </tr>
                                                                                        <tr
                                                                                            style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;font-family:Arial,sans-serif;vertical-align:baseline;display:block">
                                                                                            <td
                                                                                                style="margin:0px;padding:0px;border:0px;outline:0px;font-weight:inherit;font-style:inherit;font-size:100%;font-family:Arial,sans-serif;vertical-align:baseline">
                                                                                                <a href="https://www.amazon.co.uk/gp/r.html?C=139N1T2SKF371&amp;K=16BYYYNN41S0T&amp;M=urn:rtn:msg:20240608094209b30c374ed3ac4751b8fae0e93a80p0eu&amp;R=N6PPLLJ29Z9T&amp;T=C&amp;U=https%3A%2F%2Fwww.amazon.co.uk%2Fref%3Dpe_27063361_485629781_TE_cn&amp;H=AEBLP9WZKCSDICMXLWB6ZNJFMR0A&amp;ref_=pe_27063361_485629781_TE_cn"
                                                                                                    title="Visit Amazon.co.uk"
                                                                                                    style="font-size:13px;text-decoration:none;font-family:Arial,sans-serif;font-weight:inherit;line-height:inherit;margin:0px;padding:0px;border:0px;outline:0px;font-style:inherit;vertical-align:baseline;color:rgb(0,113,133)"
                                                                                                    rel="noreferrer noopener"
                                                                                                    target="_blank"> <img
                                                                                                        alt="Amazon.co.uk"
                                                                                                        src="https://m.media-amazon.com/images/G/01/outbound/OutboundTemplates/Smile_Logo_Light._BG240,242,242_.png"
                                                                                                        height="43"
                                                                                                        style="width: 86px; min-height: 43px; display: block; margin: 0px; padding: 0px; border: 0px; outline: 0px; font-weight: inherit; font-style: inherit; font-size: 100%; font-family: Arial, sans-serif; vertical-align: baseline; line-height: 100%; text-decoration: none;"
                                                                                                        id="m_-6063807691237806463ymail_ctr_id_-325584-10">
                                                                                                </a> </td>
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
                        </div>
                    </div>
                </blockquote>
            </div>
        </div>
    </body>
    </html>
    """
    
    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
