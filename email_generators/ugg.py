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
    msg['From'] = formataddr((f'UGG', sender_email))
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
    "Please enter the image url (jpg, jpeg, png):",
    "Please enter the item name (Men's Classic Short Boot):",
    "Please enter the size (11):",
    "Please enter the product total (WITHOUT THE $):",
    "Please enter the customer name (Juggy Resells):",
    "Please enter the street address (81 Hayley Road):",
    "Please enter the suburb, country & postcode (West Andrew, Australia 7604):",
    "Please enter the shipping cost (WITHOUT THE $ SIGN):",
    "Please enter the tax total (WITHOUT THE $ SIGN):",
    "Please enter the order total (WITHOUT THE $ SIGN):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira a URL da imagem (jpg, jpeg, png):",
    "Por favor, insira o nome do item (Botina Clássica Masculina):",
    "Por favor, insira o tamanho (11):",
    "Por favor, insira o total do produto (SEM O SÍMBOLO $):",
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira o endereço (81 Hayley Road):",
    "Por favor, insira o bairro, país e código postal (West Andrew, Austrália 7604):",
    "Por favor, insira o custo de envio (SEM O SÍMBOLO $):",
    "Por favor, insira o total do imposto (SEM O SÍMBOLO $):",
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
    part1 = "NA"
    part2 = random.randint(10000000, 99999999)  # Random 8-digit number

    # Combine the parts into order number
    order_number = f"{part1}{part2}"
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
    recipient_email = f'{user_inputs[11]}'
    subject = f"Order {order_num} has been confirmed"

    html_template = f"""
        <div>
        <div class="gmail_quote">
            <u></u>
            <div marginwidth="0" marginheight="0"
                style="margin-top:0px;margin-bottom:0px;padding-top:0px;padding-bottom:0px;width:100%!important">
                <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center" bgcolor="#ffffff">
                    <tbody>
                        <tr>
                            <td valign="top" align="center">
                                <table width="600" cellpadding="0" cellspacing="0" align="center" style="width:600px"
                                    bgcolor="#ffffff">
                                    <tbody>
                                        <tr>
                                            <td align="center" valign="top"
                                                style="font-family:sans-serif;font-size:1px;line-height:1px;display:none;color:rgb(255,255,255)">
                                                Your items are in the works.</td>
                                        </tr>
                                        <tr>
                                            <td>
                                                <div style="display:none;max-height:0px;overflow:hidden">͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌
                                                    ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌
                                                    ͏ ‌ ͏ ‌ ͏ ‌ </div>
                                                <div style="display:none;max-height:0px;overflow:hidden">͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌
                                                    ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌ ͏ ‌
                                                    ͏ ‌ ͏ ‌ ͏ ‌ </div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td valign="top" align="center"
                                                style="min-width:600px;font-family:'Proxima Nova',Arial,sans-serif;color:rgb(0,0,1)">
                                                <table width="100%" cellpadding="0" cellspacing="0"
                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                    <tbody style="font-family:'Proxima Nova',Arial,sans-serif">
                                                        <tr style="font-family:'Proxima Nova',Arial,sans-serif">
                                                            <td align="center" valign="top"
                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                <table width="100%" cellpadding="0" cellspacing="0"
                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                    <tbody
                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                        <tr
                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                            <td
                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                <div
                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                    <table width="100%" cellpadding="0"
                                                                                        cellspacing="0" bgcolor="#ffffff"
                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                        <tbody
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <tr
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <td align="center"
                                                                                                    valign="top"
                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                    <table width="600"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        bgcolor="#ffffff"
                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                        <tbody
                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            <tr
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <td height="20"
                                                                                                                    style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                            <tr
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <td align="center"
                                                                                                                    valign="top"
                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                    <table
                                                                                                                        width="100%"
                                                                                                                        cellpadding="0"
                                                                                                                        cellspacing="0"
                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                        <tbody
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <tr
                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                <td width="20"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                </td>
                                                                                                                                <td align="center"
                                                                                                                                    valign="top"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                    <table
                                                                                                                                        width="100%"
                                                                                                                                        cellpadding="0"
                                                                                                                                        cellspacing="0"
                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                        <tbody
                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            <tr
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <td align="center"
                                                                                                                                                    valign="top"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                    <a href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/fae5660c?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxY2Y3ZmMxOWNiNzAwMDNmZTRlIiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvP3V0bV9zb3VyY2U9VVNfVHJhbnNhY3Rpb25hbCZ1dG1fbWVkaXVtPWVtYWlsJnV0bV9jYW1wYWlnbj1VX1RYTkxfT1JERVJfQ09ORklSTUFUSU9OX0VOLUNBJmhtYWlsPWRkYWIyODk4NGNiZDBmNjExNjdlNWU3M2I3NWI2NWU1MjFiMDNkNmE3NTY4OWNjMWY1MTMyODQ1YTA4MTg2OTkmYnhpZD02NTc3MWUwZThhMDFhMTE3MTEwMTYzZjgifQ&amp;jwtS=i1cSXVWqt64iyvNViEdAaAkhWmnNwyz2wr3Ggvm-OQ4"
                                                                                                                                                        target="_blank"
                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif"><img
                                                                                                                                                            src="https://images.usw2.cordial.com/1663/204x100/ugg_logo.png"
                                                                                                                                                            width="109"
                                                                                                                                                            border="0"
                                                                                                                                                            style="display: block; height: auto; max-width: 109px; font-family: 'Proxima Nova', Arial, sans-serif;"
                                                                                                                                                            alt="UGG"></a>
                                                                                                                                                </td>
                                                                                                                                            </tr>
                                                                                                                                        </tbody>
                                                                                                                                    </table>
                                                                                                                                </td>
                                                                                                                                <td width="20"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                        </tbody>
                                                                                                                    </table>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                            <tr
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <td height="20"
                                                                                                                    style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </div>
                                                                                <div
                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                    <table width="100%" cellpadding="0"
                                                                                        cellspacing="0" bgcolor="#ffffff"
                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                        <tbody
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <tr
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <td align="center"
                                                                                                    valign="top"
                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                    <table width="600"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif;background-color:rgb(255,255,255)">
                                                                                                        <tbody
                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            <tr
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <td height="20"
                                                                                                                    style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </div>
                                                                                <div
                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                    <table width="100%" cellpadding="0"
                                                                                        cellspacing="0" bgcolor="#ffffff"
                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                        <tbody
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <tr
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <td align="center"
                                                                                                    valign="top"
                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                    <table width="600"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        bgcolor="#FFFFFF"
                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                        <tbody
                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            <tr
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <td height="10"
                                                                                                                    style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                            <tr
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <td align="center"
                                                                                                                    valign="top"
                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                    <table
                                                                                                                        width="100%"
                                                                                                                        cellpadding="0"
                                                                                                                        cellspacing="0"
                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                        <tbody
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <tr
                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                <td width="40"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                </td>
                                                                                                                                <td align="center"
                                                                                                                                    valign="top"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                    <table
                                                                                                                                        width="100%"
                                                                                                                                        cellpadding="0"
                                                                                                                                        cellspacing="0"
                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                        <tbody
                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            <tr
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <td align="center"
                                                                                                                                                    valign="top"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif;font-size:48px;line-height:48px;font-weight:700;color:rgb(0,0,1)">
                                                                                                                                                    <a style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif"
                                                                                                                                                        href="#m_5921561251109312795_?utm_source=US_Transactional&amp;utm_medium=email&amp;utm_campaign=U_TXNL_ORDER_CONFIRMATION_EN-CA&amp;hmail=ddab28984cbd0f61167e5e73b75b65e521b03d6a75689cc1f5132845a0818699&amp;bxid=65771e0e8a01a117110163f8"><span
                                                                                                                                                            style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif;color:rgb(0,0,1)">Thank
                                                                                                                                                            you
                                                                                                                                                            for
                                                                                                                                                            your
                                                                                                                                                            order</span></a>
                                                                                                                                                </td>
                                                                                                                                            </tr>
                                                                                                                                            <tr
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <td height="14"
                                                                                                                                                    style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                </td>
                                                                                                                                            </tr>
                                                                                                                                            <tr
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <td align="center"
                                                                                                                                                    valign="top"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif;font-size:16px;line-height:20px;font-weight:400;color:rgb(0,0,1)">
                                                                                                                                                    <span
                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">Due
                                                                                                                                                        to
                                                                                                                                                        increased
                                                                                                                                                        holiday
                                                                                                                                                        volume,
                                                                                                                                                        orders
                                                                                                                                                        may
                                                                                                                                                        take
                                                                                                                                                        up
                                                                                                                                                        to
                                                                                                                                                        48
                                                                                                                                                        hours
                                                                                                                                                        to
                                                                                                                                                        process</span>.<br><br>Once
                                                                                                                                                    your
                                                                                                                                                    items
                                                                                                                                                    are
                                                                                                                                                    ready
                                                                                                                                                    to
                                                                                                                                                    ship,
                                                                                                                                                    you&#39;ll
                                                                                                                                                    receive
                                                                                                                                                    a
                                                                                                                                                    confirmation
                                                                                                                                                    email
                                                                                                                                                    with
                                                                                                                                                    a
                                                                                                                                                    tracking
                                                                                                                                                    number
                                                                                                                                                    to
                                                                                                                                                    view
                                                                                                                                                    details
                                                                                                                                                    and
                                                                                                                                                    update
                                                                                                                                                    delivery
                                                                                                                                                    preferences
                                                                                                                                                    directly
                                                                                                                                                    with
                                                                                                                                                    the
                                                                                                                                                    carrier.
                                                                                                                                                </td>
                                                                                                                                            </tr>
                                                                                                                                            <tr
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <td height="10"
                                                                                                                                                    style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                </td>
                                                                                                                                            </tr>
                                                                                                                                            <tr
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <td align="center"
                                                                                                                                                    valign="top"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif;font-size:18px;line-height:28px;font-weight:400;text-decoration:none;color:rgb(0,0,1)">
                                                                                                                                                </td>
                                                                                                                                            </tr>
                                                                                                                                        </tbody>
                                                                                                                                    </table>
                                                                                                                                </td>
                                                                                                                                <td width="40"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                        </tbody>
                                                                                                                    </table>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                            <tr
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <td height="10"
                                                                                                                    style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </div>
                                                                                <div
                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                    <table width="100%" cellpadding="0"
                                                                                        cellspacing="0" bgcolor="#ffffff"
                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                        <tbody
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <tr
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <td align="center"
                                                                                                    valign="top"
                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                    <table width="600"
                                                                                                        bgcolor="#FFFFFF"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                        <tbody
                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            <tr
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <td height="10"
                                                                                                                    style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                            <tr
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <td align="center"
                                                                                                                    valign="top"
                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                    <table
                                                                                                                        width="100%"
                                                                                                                        cellpadding="0"
                                                                                                                        cellspacing="0"
                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                        <tbody
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <tr
                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                <td width="40"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                </td>
                                                                                                                                <td align="center"
                                                                                                                                    valign="top"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                    <table
                                                                                                                                        width="100%"
                                                                                                                                        cellpadding="0"
                                                                                                                                        cellspacing="0"
                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                        <tbody
                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            <tr
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <td align="center"
                                                                                                                                                    valign="top"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif;font-size:24px;line-height:24px;font-weight:700;color:rgb(0,0,1)">
                                                                                                                                                    Order
                                                                                                                                                    Confirmation:
                                                                                                                                                </td>
                                                                                                                                            </tr>
                                                                                                                                        </tbody>
                                                                                                                                    </table>
                                                                                                                                </td>
                                                                                                                                <td width="40"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                        </tbody>
                                                                                                                    </table>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                            <tr
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <td height="10"
                                                                                                                    style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </div>
                                                                                <div
                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                    <table width="100%" cellpadding="0"
                                                                                        cellspacing="0" bgcolor="#ffffff"
                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                        <tbody
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <tr
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <td align="center"
                                                                                                    valign="top"
                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                    <table width="600"
                                                                                                        bgcolor="#FFFFFF"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                        <tbody
                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            <tr
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <td align="center"
                                                                                                                    valign="top"
                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                    <table
                                                                                                                        width="100%"
                                                                                                                        cellpadding="0"
                                                                                                                        cellspacing="0"
                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                        <tbody
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <tr
                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                <td width="40"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                </td>
                                                                                                                                <td align="center"
                                                                                                                                    valign="top"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                    <table
                                                                                                                                        width="100%"
                                                                                                                                        cellpadding="0"
                                                                                                                                        cellspacing="0"
                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                        <tbody
                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            <tr
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <td align="center"
                                                                                                                                                    valign="top"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif;font-size:16px;line-height:16px;font-weight:700;color:rgb(0,0,1)">
                                                                                                                                                    Order
                                                                                                                                                    #{order_num}
                                                                                                                                                </td>
                                                                                                                                            </tr>
                                                                                                                                        </tbody>
                                                                                                                                    </table>
                                                                                                                                </td>
                                                                                                                                <td width="40"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                        </tbody>
                                                                                                                    </table>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                            <tr
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <td height="10"
                                                                                                                    style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </div>
                                                                                <div
                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                    <table width="100%" cellpadding="0"
                                                                                        cellspacing="0" bgcolor="#ffffff"
                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                        <tbody
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <tr
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <td align="center"
                                                                                                    valign="top"
                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                    <table width="600"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif;background-color:rgb(255,255,255)">
                                                                                                        <tbody
                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            <tr
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <td height="20"
                                                                                                                    style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </div>
                                                                                <div
                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                    <table width="100%" cellpadding="0"
                                                                                        cellspacing="0" bgcolor="#ffffff"
                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                        <tbody
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <tr
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <td align="center"
                                                                                                    valign="top"
                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                    <table width="600"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        bgcolor="#eeeeee"
                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                        <tbody
                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            <tr
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <td align="center"
                                                                                                                    valign="top"
                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                    <table
                                                                                                                        width="100%"
                                                                                                                        cellpadding="0"
                                                                                                                        cellspacing="0"
                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                        <tbody
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <tr
                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                <td width="5"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                </td>
                                                                                                                                <td align="center"
                                                                                                                                    valign="top"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                    <table
                                                                                                                                        width="100%"
                                                                                                                                        cellpadding="0"
                                                                                                                                        cellspacing="0"
                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                        <tbody
                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            <tr
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <td align="center"
                                                                                                                                                    valign="top"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                    <table
                                                                                                                                                        width="100%"
                                                                                                                                                        cellpadding="0"
                                                                                                                                                        cellspacing="0"
                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                        <tbody
                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                            <tr
                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                <td height="10"
                                                                                                                                                                    style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                </td>
                                                                                                                                                            </tr>
                                                                                                                                                            <tr
                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                <td align="center"
                                                                                                                                                                    valign="top"
                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif;font-size:16px;line-height:16px;font-weight:700;color:rgb(0,0,1)">
                                                                                                                                                                    <span
                                                                                                                                                                        style="font-weight:bold;text-transform:capitalize;font-family:'Proxima Nova',Arial,sans-serif">Shipping
                                                                                                                                                                        Soon:</span>
                                                                                                                                                                </td>
                                                                                                                                                            </tr>
                                                                                                                                                        </tbody>
                                                                                                                                                    </table>
                                                                                                                                                </td>
                                                                                                                                            </tr>
                                                                                                                                        </tbody>
                                                                                                                                    </table>
                                                                                                                                </td>
                                                                                                                                <td width="5"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
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
                                                                                    <table width="100%" cellpadding="0"
                                                                                        cellspacing="0" bgcolor="#ffffff"
                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                        <tbody
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <tr
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <td align="center"
                                                                                                    valign="top"
                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                    <table width="600"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        style="width:600px;font-family:'Proxima Nova',Arial,sans-serif"
                                                                                                        bgcolor="#eeeeee">
                                                                                                        <tbody
                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            <tr
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <td align="center"
                                                                                                                    valign="top"
                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                    <table
                                                                                                                        width="100%"
                                                                                                                        cellpadding="0"
                                                                                                                        cellspacing="0"
                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                        <tbody
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <tr
                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                <td width="5"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                </td>
                                                                                                                                <td align="center"
                                                                                                                                    valign="top"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                    <table
                                                                                                                                        width="100%"
                                                                                                                                        cellpadding="0"
                                                                                                                                        cellspacing="0"
                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                        <tbody
                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            <tr
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <td align="center"
                                                                                                                                                    valign="top"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                    <table
                                                                                                                                                        width="100%"
                                                                                                                                                        cellpadding="0"
                                                                                                                                                        cellspacing="0"
                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                        <tbody
                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                            <tr
                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                            </tr>
                                                                                                                                                            <tr
                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                <td width=""
                                                                                                                                                                    align="center"
                                                                                                                                                                    valign="middle"
                                                                                                                                                                    style="width:25%;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                    <table
                                                                                                                                                                        cellpadding="0"
                                                                                                                                                                        cellspacing="0"
                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                        <tbody
                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            <tr
                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                <td align="center"
                                                                                                                                                                                    valign="top"
                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                    <img src="{user_inputs[0]}"
                                                                                                                                                                                        width="150"
                                                                                                                                                                                        border="0"
                                                                                                                                                                                        style="display: block; height: auto; font-family: 'Proxima Nova', Arial, sans-serif;"
                                                                                                                                                                                        alt="{user_inputs[1]}">
                                                                                                                                                                                </td>
                                                                                                                                                                            </tr>
                                                                                                                                                                        </tbody>
                                                                                                                                                                    </table>
                                                                                                                                                                </td>
                                                                                                                                                            </tr>
                                                                                                                                                            <tr
                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                <td align="left"
                                                                                                                                                                    valign="top"
                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                    <table
                                                                                                                                                                        width="100%"
                                                                                                                                                                        cellpadding="0"
                                                                                                                                                                        cellspacing="0"
                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                        <tbody
                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            <tr
                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                <td width="16"
                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                </td>
                                                                                                                                                                                <td align="center"
                                                                                                                                                                                    valign="top"
                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                    <table
                                                                                                                                                                                        width="100%"
                                                                                                                                                                                        cellpadding="0"
                                                                                                                                                                                        cellspacing="0"
                                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                        <tbody
                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            <tr
                                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                                <td align="center"
                                                                                                                                                                                                    valign="top"
                                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif;font-size:16px;line-height:20px;font-weight:400;color:rgb(0,0,1)">
                                                                                                                                                                                                    <table
                                                                                                                                                                                                        cellpadding="0"
                                                                                                                                                                                                        cellspacing="0"
                                                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                                        <tbody
                                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                                            <tr
                                                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                                                <td valign="top"
                                                                                                                                                                                                                    align="center"
                                                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                                                    <p
                                                                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                                                        <span
                                                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">{user_inputs[1]}
                                                                                                                                                                                                                            </span><br>Qty:
                                                                                                                                                                                                                        <span
                                                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">1</span>
                                                                                                                                                                                                                        Size:
                                                                                                                                                                                                                        <span
                                                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">{user_inputs[2]}</span>
                                                                                                                                                                                                                        Product
                                                                                                                                                                                                                        Total:
                                                                                                                                                                                                                        <span
                                                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">{user_inputs[10]}{user_inputs[3]}</span>
                                                                                                                                                                                                                    </p>
                                                                                                                                                                                                                </td>
                                                                                                                                                                                                            </tr>
                                                                                                                                                                                                        </tbody>
                                                                                                                                                                                                        <tbody
                                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                                            <tr
                                                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                                                <td height="20"
                                                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
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
                                                                                                                                </td>
                                                                                                                                <td width="5"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
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
                                                                                    <table width="100%" cellpadding="0"
                                                                                        cellspacing="0" bgcolor="#ffffff"
                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                        <tbody
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <tr
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <td height="10"
                                                                                                    style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                </td>
                                                                                            </tr>
                                                                                            <tr
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <td align="center"
                                                                                                    valign="top"
                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                    <table width="600"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        style="width:600px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                        <tbody
                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            <tr
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <td height="10"
                                                                                                                    style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                            <tr
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <td align="center"
                                                                                                                    valign="top"
                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                    <table
                                                                                                                        width="100%"
                                                                                                                        cellpadding="0"
                                                                                                                        cellspacing="0"
                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                        <tbody
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <tr
                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                <td width="5"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                </td>
                                                                                                                                <td align="center"
                                                                                                                                    valign="top"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                    <table
                                                                                                                                        width="100%"
                                                                                                                                        cellpadding="0"
                                                                                                                                        cellspacing="0"
                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                        <tbody
                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            <tr
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <td align="center"
                                                                                                                                                    valign="top"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                    <table
                                                                                                                                                        width="100%"
                                                                                                                                                        cellpadding="0"
                                                                                                                                                        cellspacing="0"
                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                        <tbody
                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                            <tr
                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                <td align="left"
                                                                                                                                                                    valign="top"
                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                    <table
                                                                                                                                                                        width="100%"
                                                                                                                                                                        cellpadding="0"
                                                                                                                                                                        cellspacing="0"
                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                        <tbody
                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            <tr
                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                <td width="16"
                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                </td>
                                                                                                                                                                                <td align="center"
                                                                                                                                                                                    valign="top"
                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                    <table
                                                                                                                                                                                        width="100%"
                                                                                                                                                                                        cellpadding="0"
                                                                                                                                                                                        cellspacing="0"
                                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                        <tbody
                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            <tr
                                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                                <td align="center"
                                                                                                                                                                                                    valign="top"
                                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif;font-size:16px;line-height:20px;font-weight:400;color:rgb(0,0,1)">
                                                                                                                                                                                                    <span
                                                                                                                                                                                                        style="font-weight:bold;font-size:16px;line-height:16px;text-transform:capitalize;font-family:'Proxima Nova',Arial,sans-serif">Shipping
                                                                                                                                                                                                        Address:</span><br>{user_inputs[4]}<br><a
                                                                                                                                                                                                        href="https://www.google.com/maps/"
                                                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">{user_inputs[5]}</a><br><a
                                                                                                                                                                                                        href="https://www.google.com/maps/"
                                                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">{user_inputs[6]}</a>
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
                                                                                                                                <td width="5"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
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
                                                                                <div
                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                    <table width="100%" cellpadding="0"
                                                                                        cellspacing="0" bgcolor="#ffffff"
                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                        <tbody
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <tr
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <td align="center"
                                                                                                    valign="top"
                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                    <table width="600"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif;background-color:rgb(255,255,255)">
                                                                                                        <tbody
                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            <tr
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <td height="20"
                                                                                                                    style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </div>
                                                                                <div
                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                    <table width="100%" cellpadding="0"
                                                                                        cellspacing="0" bgcolor="#ffffff"
                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                        <tbody
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <tr
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <td align="center"
                                                                                                    valign="top"
                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                    <table width="600"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        bgcolor="#ffffff"
                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                        <tbody
                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            <tr
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <td align="center"
                                                                                                                    valign="top"
                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                    <table
                                                                                                                        width="100%"
                                                                                                                        cellpadding="0"
                                                                                                                        cellspacing="0"
                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                        <tbody
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <tr
                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                <td width="5"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                </td>
                                                                                                                                <td align="center"
                                                                                                                                    valign="top"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                    <table
                                                                                                                                        width="100%"
                                                                                                                                        cellpadding="0"
                                                                                                                                        cellspacing="0"
                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                        <tbody
                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            <tr
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <td align="center"
                                                                                                                                                    valign="top"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                    <table
                                                                                                                                                        width="100%"
                                                                                                                                                        cellpadding="0"
                                                                                                                                                        cellspacing="0"
                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                        <tbody
                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                            <tr
                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                <td height="10"
                                                                                                                                                                    style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                </td>
                                                                                                                                                            </tr>
                                                                                                                                                            <tr
                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                <td align="center"
                                                                                                                                                                    valign="top"
                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif;font-size:16px;line-height:20px;font-weight:400;text-transform:capitalize;color:rgb(0,0,1)">
                                                                                                                                                                    <span
                                                                                                                                                                        style="font-weight:bold;text-transform:capitalize;font-family:'Proxima Nova',Arial,sans-serif">Order
                                                                                                                                                                        Summary:</span><br>Sales
                                                                                                                                                                    Subtotal:
                                                                                                                                                                    {user_inputs[10]}{user_inputs[3]}<br>Product
                                                                                                                                                                    Discount:
                                                                                                                                                                    {user_inputs[10]}0.00<br>Gift
                                                                                                                                                                    Wrap:
                                                                                                                                                                    {user_inputs[10]}0.00<br>Shipping:
                                                                                                                                                                    {user_inputs[10]}{user_inputs[7]}<br>Ship
                                                                                                                                                                    Discount:
                                                                                                                                                                    {user_inputs[10]}0.00<br>Tax:
                                                                                                                                                                    {user_inputs[10]}{user_inputs[8]}<br><br><span
                                                                                                                                                                        style="font-weight:bold;text-transform:capitalize;font-family:'Proxima Nova',Arial,sans-serif">Total:
                                                                                                                                                                        {user_inputs[10]}{user_inputs[9]}</span>
                                                                                                                                                                </td>
                                                                                                                                                            </tr>
                                                                                                                                                            <tr
                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                <td height="10"
                                                                                                                                                                    style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                </td>
                                                                                                                                                            </tr>
                                                                                                                                                        </tbody>
                                                                                                                                                    </table>
                                                                                                                                                </td>
                                                                                                                                            </tr>
                                                                                                                                        </tbody>
                                                                                                                                    </table>
                                                                                                                                </td>
                                                                                                                                <td width="5"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
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
                                                <table width="100%" cellpadding="0" cellspacing="0"
                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                    <tbody style="font-family:'Proxima Nova',Arial,sans-serif">
                                                        <tr style="font-family:'Proxima Nova',Arial,sans-serif">
                                                            <td align="center" valign="top"
                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                <table width="100%" cellpadding="0" cellspacing="0"
                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                    <tbody
                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                        <tr
                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                            <td align="center" valign="top"
                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                <table width="100%" cellpadding="0"
                                                                                    cellspacing="0" bgcolor="#ffffff"
                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                    <tbody
                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                        <tr
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <td height="20"
                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <td align="center" valign="top"
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <table width="600"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                    <tbody
                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                        <tr
                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            <td align="center"
                                                                                                                valign="top"
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <table
                                                                                                                    width="100%"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                    <tbody
                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                        <tr
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <td height="10"
                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif;background-color:rgb(0,0,0)">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <td height="20"
                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <td align="center"
                                                                                                                                valign="top"
                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                <a href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/439a7734?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxY2Y3ZmMxOWNiNzAwMDNmZTUwIiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvY2FcL3VnZy1yZXdhcmRzLmh0bWw_dXRtX3NvdXJjZT1VU19UcmFuc2FjdGlvbmFsJnV0bV9tZWRpdW09ZW1haWwmdXRtX2NhbXBhaWduPVVfVFhOTF9PUkRFUl9DT05GSVJNQVRJT05fRU4tQ0EmaG1haWw9ZGRhYjI4OTg0Y2JkMGY2MTE2N2U1ZTczYjc1YjY1ZTUyMWIwM2Q2YTc1Njg5Y2MxZjUxMzI4NDVhMDgxODY5OSZieGlkPTY1NzcxZTBlOGEwMWExMTcxMTAxNjNmOCJ9&amp;jwtS=msJAdoCMjUiaSip8QIvh3Z-r8loKZp-g_jS3LkJgxcA"
                                                                                                                                    target="_blank"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif"><img
                                                                                                                                        src="https://images.usw2.cordial.com/1663/123x86/ugg_rewards_header_2022.png"
                                                                                                                                        width="123"
                                                                                                                                        border="0"
                                                                                                                                        style="display: block; height: auto; font-family: 'Proxima Nova', Arial, sans-serif;"
                                                                                                                                        alt="UGG Rewards"></a>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <td height="20"
                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr
                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            <td align="center"
                                                                                                                valign="top"
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <table
                                                                                                                    width="100%"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                    <tbody
                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                        <tr
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <td width="67"
                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            </td>
                                                                                                                            <td align="center"
                                                                                                                                valign="top"
                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                <table
                                                                                                                                    width="100%"
                                                                                                                                    cellpadding="0"
                                                                                                                                    cellspacing="0"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                    <tbody
                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                        <tr
                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            <td align="center"
                                                                                                                                                valign="top"
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <table
                                                                                                                                                    width="466"
                                                                                                                                                    cellpadding="0"
                                                                                                                                                    cellspacing="0"
                                                                                                                                                    style="width:466px;max-width:466px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                    <tbody
                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                        <tr
                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                            <td align="center"
                                                                                                                                                                valign="top"
                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                <table
                                                                                                                                                                    width="28.755364806867%"
                                                                                                                                                                    cellpadding="0"
                                                                                                                                                                    cellspacing="0"
                                                                                                                                                                    align="left"
                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                    <tbody
                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                        <tr
                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            <td align="center"
                                                                                                                                                                                valign="top"
                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                <a href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/b13d87b1?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxY2Y3ZmMxOWNiNzAwMDNmZTUxIiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvY2FcL3VnZy1yZXdhcmRzLmh0bWw_dXRtX3NvdXJjZT1VU19UcmFuc2FjdGlvbmFsJnV0bV9tZWRpdW09ZW1haWwmdXRtX2NhbXBhaWduPVVfVFhOTF9PUkRFUl9DT05GSVJNQVRJT05fRU4tQ0EmaG1haWw9ZGRhYjI4OTg0Y2JkMGY2MTE2N2U1ZTczYjc1YjY1ZTUyMWIwM2Q2YTc1Njg5Y2MxZjUxMzI4NDVhMDgxODY5OSZieGlkPTY1NzcxZTBlOGEwMWExMTcxMTAxNjNmOCJ9&amp;jwtS=q5IVi5cFmi7A4oeooEIGSXPkND2yB7ddNUxVfJ184Nc"
                                                                                                                                                                                    target="_blank"
                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif"><img
                                                                                                                                                                                        src="https://images.usw2.cordial.com/1663/134x56/ugg_rewards_1_earlyAccess_2022.png"
                                                                                                                                                                                        width="134"
                                                                                                                                                                                        border="0"
                                                                                                                                                                                        style="display: block; height: auto; max-width: none; font-family: 'Proxima Nova', Arial, sans-serif;"
                                                                                                                                                                                        alt=""></a>
                                                                                                                                                                            </td>
                                                                                                                                                                        </tr>
                                                                                                                                                                        <tr
                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            <td height="10"
                                                                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            </td>
                                                                                                                                                                        </tr>
                                                                                                                                                                        <tr
                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            <td align="center"
                                                                                                                                                                                valign="top"
                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif;font-size:14px;line-height:20px;font-weight:700;color:rgb(0,0,1)">
                                                                                                                                                                                <a style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif"
                                                                                                                                                                                    href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/cbf3d0d6?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxY2Y3ZmMxOWNiNzAwMDNmZTUyIiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvY2FcL3VnZy1yZXdhcmRzLmh0bWw_dXRtX3NvdXJjZT1VU19UcmFuc2FjdGlvbmFsJnV0bV9tZWRpdW09ZW1haWwmdXRtX2NhbXBhaWduPVVfVFhOTF9PUkRFUl9DT05GSVJNQVRJT05fRU4tQ0EmaG1haWw9ZGRhYjI4OTg0Y2JkMGY2MTE2N2U1ZTczYjc1YjY1ZTUyMWIwM2Q2YTc1Njg5Y2MxZjUxMzI4NDVhMDgxODY5OSZieGlkPTY1NzcxZTBlOGEwMWExMTcxMTAxNjNmOCJ9&amp;jwtS=Tn6pPmhJPnDVjDKVI2GYb4wJHixtB7FiSIQsIKuhYSQ"
                                                                                                                                                                                    target="_blank"><span
                                                                                                                                                                                        style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif;color:rgb(0,0,1)">Early
                                                                                                                                                                                        Shopping<br>Access</span></a>
                                                                                                                                                                            </td>
                                                                                                                                                                        </tr>
                                                                                                                                                                    </tbody>
                                                                                                                                                                </table>
                                                                                                                                                                <table
                                                                                                                                                                    width="32"
                                                                                                                                                                    cellpadding="0"
                                                                                                                                                                    cellspacing="0"
                                                                                                                                                                    align="left"
                                                                                                                                                                    style="width:32px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                    <tbody
                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                        <tr
                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            <td height="32"
                                                                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            </td>
                                                                                                                                                                        </tr>
                                                                                                                                                                    </tbody>
                                                                                                                                                                </table>
                                                                                                                                                                <table
                                                                                                                                                                    width="28.755364806867%"
                                                                                                                                                                    cellpadding="0"
                                                                                                                                                                    cellspacing="0"
                                                                                                                                                                    align="left"
                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                    <tbody
                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                        <tr
                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            <td align="center"
                                                                                                                                                                                valign="top"
                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                <a href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/b2e8182f?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxY2Y3ZmMxOWNiNzAwMDNmZTUzIiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvY2FcL3VnZy1yZXdhcmRzLmh0bWw_dXRtX3NvdXJjZT1VU19UcmFuc2FjdGlvbmFsJnV0bV9tZWRpdW09ZW1haWwmdXRtX2NhbXBhaWduPVVfVFhOTF9PUkRFUl9DT05GSVJNQVRJT05fRU4tQ0EmaG1haWw9ZGRhYjI4OTg0Y2JkMGY2MTE2N2U1ZTczYjc1YjY1ZTUyMWIwM2Q2YTc1Njg5Y2MxZjUxMzI4NDVhMDgxODY5OSZieGlkPTY1NzcxZTBlOGEwMWExMTcxMTAxNjNmOCJ9&amp;jwtS=pW2M4dh1t8hG0d4uAImjJpvia5R9WSvbfOx8BpfCoBA"
                                                                                                                                                                                    target="_blank"
                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif"><img
                                                                                                                                                                                        src="https://images.usw2.cordial.com/1663/134x56/ugg_rewards_2_shippingPerks_2022.png"
                                                                                                                                                                                        width="134"
                                                                                                                                                                                        border="0"
                                                                                                                                                                                        style="display: block; height: auto; max-width: none; font-family: 'Proxima Nova', Arial, sans-serif;"
                                                                                                                                                                                        alt=""></a>
                                                                                                                                                                            </td>
                                                                                                                                                                        </tr>
                                                                                                                                                                        <tr
                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            <td height="10"
                                                                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            </td>
                                                                                                                                                                        </tr>
                                                                                                                                                                        <tr
                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            <td align="center"
                                                                                                                                                                                valign="top"
                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif;font-size:14px;line-height:20px;font-weight:700;color:rgb(0,0,1)">
                                                                                                                                                                                <a style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif"
                                                                                                                                                                                    href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/5e092752?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxY2Y3ZmMxOWNiNzAwMDNmZTU0IiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvY2FcL3VnZy1yZXdhcmRzLmh0bWw_dXRtX3NvdXJjZT1VU19UcmFuc2FjdGlvbmFsJnV0bV9tZWRpdW09ZW1haWwmdXRtX2NhbXBhaWduPVVfVFhOTF9PUkRFUl9DT05GSVJNQVRJT05fRU4tQ0EmaG1haWw9ZGRhYjI4OTg0Y2JkMGY2MTE2N2U1ZTczYjc1YjY1ZTUyMWIwM2Q2YTc1Njg5Y2MxZjUxMzI4NDVhMDgxODY5OSZieGlkPTY1NzcxZTBlOGEwMWExMTcxMTAxNjNmOCJ9&amp;jwtS=oiK8oydMfMdgYYqyr41u4lZb6ed_uPQMtrcmI2aTAUw"
                                                                                                                                                                                    target="_blank"><span
                                                                                                                                                                                        style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif;color:rgb(0,0,1)">Shipping
                                                                                                                                                                                        Perks</span></a>
                                                                                                                                                                            </td>
                                                                                                                                                                        </tr>
                                                                                                                                                                    </tbody>
                                                                                                                                                                </table>
                                                                                                                                                                <table
                                                                                                                                                                    width="32"
                                                                                                                                                                    cellpadding="0"
                                                                                                                                                                    cellspacing="0"
                                                                                                                                                                    align="left"
                                                                                                                                                                    style="width:32px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                    <tbody
                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                        <tr
                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            <td height="32"
                                                                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            </td>
                                                                                                                                                                        </tr>
                                                                                                                                                                    </tbody>
                                                                                                                                                                </table>
                                                                                                                                                                <table
                                                                                                                                                                    width="28.755364806867%"
                                                                                                                                                                    cellpadding="0"
                                                                                                                                                                    cellspacing="0"
                                                                                                                                                                    align="left"
                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                    <tbody
                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                        <tr
                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            <td align="center"
                                                                                                                                                                                valign="top"
                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                <a href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/8b9d054d?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxY2Y3ZmMxOWNiNzAwMDNmZTU1IiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvY2FcL3VnZy1yZXdhcmRzLmh0bWw_dXRtX3NvdXJjZT1VU19UcmFuc2FjdGlvbmFsJnV0bV9tZWRpdW09ZW1haWwmdXRtX2NhbXBhaWduPVVfVFhOTF9PUkRFUl9DT05GSVJNQVRJT05fRU4tQ0EmaG1haWw9ZGRhYjI4OTg0Y2JkMGY2MTE2N2U1ZTczYjc1YjY1ZTUyMWIwM2Q2YTc1Njg5Y2MxZjUxMzI4NDVhMDgxODY5OSZieGlkPTY1NzcxZTBlOGEwMWExMTcxMTAxNjNmOCJ9&amp;jwtS=jtCdk3iP73Xs79KymkL7a5pL09FWSAejWdjM0uUO4bA"
                                                                                                                                                                                    target="_blank"
                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif"><img
                                                                                                                                                                                        src="https://images.usw2.cordial.com/1663/268x112/ugg_rewards_3_birthdayBonus_CA.png"
                                                                                                                                                                                        width="134"
                                                                                                                                                                                        border="0"
                                                                                                                                                                                        style="display: block; height: auto; max-width: none; font-family: 'Proxima Nova', Arial, sans-serif;"
                                                                                                                                                                                        alt=""></a>
                                                                                                                                                                            </td>
                                                                                                                                                                        </tr>
                                                                                                                                                                        <tr
                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            <td height="10"
                                                                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            </td>
                                                                                                                                                                        </tr>
                                                                                                                                                                        <tr
                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            <td align="center"
                                                                                                                                                                                valign="top"
                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif;font-size:14px;line-height:20px;font-weight:700;color:rgb(0,0,1)">
                                                                                                                                                                                <a style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif"
                                                                                                                                                                                    href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/747e8463?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxY2Y3ZmMxOWNiNzAwMDNmZTU2IiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvY2FcL3VnZy1yZXdhcmRzLmh0bWw_dXRtX3NvdXJjZT1VU19UcmFuc2FjdGlvbmFsJnV0bV9tZWRpdW09ZW1haWwmdXRtX2NhbXBhaWduPVVfVFhOTF9PUkRFUl9DT05GSVJNQVRJT05fRU4tQ0EmaG1haWw9ZGRhYjI4OTg0Y2JkMGY2MTE2N2U1ZTczYjc1YjY1ZTUyMWIwM2Q2YTc1Njg5Y2MxZjUxMzI4NDVhMDgxODY5OSZieGlkPTY1NzcxZTBlOGEwMWExMTcxMTAxNjNmOCJ9&amp;jwtS=zpIofuMbmMp4QDjZWQnEP1mH_5yLv75RouY7VXNM_co"
                                                                                                                                                                                    target="_blank"><span
                                                                                                                                                                                        style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif;color:rgb(0,0,1)">And
                                                                                                                                                                                        So
                                                                                                                                                                                        Much
                                                                                                                                                                                        More</span></a>
                                                                                                                                                                            </td>
                                                                                                                                                                        </tr>
                                                                                                                                                                        <tr
                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            <td height="20"
                                                                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
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
                                                                                                                            <td width="67"
                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr
                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            <td align="center"
                                                                                                                valign="top"
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <table
                                                                                                                    width="100%"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                    <tbody
                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                        <tr
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <td align="center"
                                                                                                                                valign="top"
                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                <table
                                                                                                                                    width="100%"
                                                                                                                                    cellspacing="0"
                                                                                                                                    cellpadding="0"
                                                                                                                                    border="0"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                    <tbody
                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                        <tr
                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            <td align="center"
                                                                                                                                                valign="top"
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <table
                                                                                                                                                    cellspacing="0"
                                                                                                                                                    cellpadding="0"
                                                                                                                                                    border="0"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                    <tbody
                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                        <tr
                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                            <td align="center"
                                                                                                                                                                style="width:131px;border-radius:initial;box-sizing:border-box;font-family:'Proxima Nova',Arial,sans-serif;background-color:rgb(255,255,255)">
                                                                                                                                                                <a style="padding:10px 12px;border:2px solid rgb(0,0,0);border-radius:initial;font-family:'Proxima Nova',Arial,sans-serif;font-size:18px;line-height:20px;font-weight:700;display:block;text-decoration:none;color:rgb(0,0,1)"
                                                                                                                                                                    href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/09b15ad6?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxY2Y3ZmMxOWNiNzAwMDNmZTU3IiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvbG9naW4jcmVnaXN0ZXI_dXRtX3NvdXJjZT1VU19UcmFuc2FjdGlvbmFsJnV0bV9tZWRpdW09ZW1haWwmdXRtX2NhbXBhaWduPVVfVFhOTF9PUkRFUl9DT05GSVJNQVRJT05fRU4tQ0EmaG1haWw9ZGRhYjI4OTg0Y2JkMGY2MTE2N2U1ZTczYjc1YjY1ZTUyMWIwM2Q2YTc1Njg5Y2MxZjUxMzI4NDVhMDgxODY5OSZieGlkPTY1NzcxZTBlOGEwMWExMTcxMTAxNjNmOCJ9&amp;jwtS=OwggpBbn6iwIwsAl7FUpG9xH_IqQ9Q2d-0oUycnXY_g"
                                                                                                                                                                    target="_blank"><span
                                                                                                                                                                        style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif;color:rgb(0,0,1)">JOIN
                                                                                                                                                                        NOW</span></a>
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
                                                                                        <tr
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <td height="24"
                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            </td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                                <table width="100%" cellpadding="0"
                                                                                    cellspacing="0"
                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                    <tbody
                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                        <tr
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <td align="center" valign="top"
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <table width="600"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    bgcolor="#ffffff"
                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                    <tbody
                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                        <tr
                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            <td width="20"
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            </td>
                                                                                                            <td align="center"
                                                                                                                valign="top"
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <table
                                                                                                                    width="100%"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    bgcolor="#000000"
                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                    <tbody
                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                        <tr
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <td height="20"
                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <td align="center"
                                                                                                                                valign="top"
                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif;font-size:16px;line-height:20px;font-weight:700;color:rgb(255,255,254)">
                                                                                                                                <a style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif"
                                                                                                                                    href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/7fe6a613?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxY2Y3ZmMxOWNiNzAwMDNmZTU4IiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvY2FcL3NoaXBwaW5nLWluZm9ybWF0aW9uLmh0bWw_dXRtX3NvdXJjZT1VU19UcmFuc2FjdGlvbmFsJnV0bV9tZWRpdW09ZW1haWwmdXRtX2NhbXBhaWduPVVfVFhOTF9PUkRFUl9DT05GSVJNQVRJT05fRU4tQ0EmaG1haWw9ZGRhYjI4OTg0Y2JkMGY2MTE2N2U1ZTczYjc1YjY1ZTUyMWIwM2Q2YTc1Njg5Y2MxZjUxMzI4NDVhMDgxODY5OSZieGlkPTY1NzcxZTBlOGEwMWExMTcxMTAxNjNmOCJ9&amp;jwtS=V_PGlTZX_CiXWnfbK9-YhNDIXTRAA7C3u4Dnw4cYC0g"
                                                                                                                                    target="_blank"><span
                                                                                                                                        style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif;color:rgb(255,255,254)">STANDARD
                                                                                                                                        SHIPPING
                                                                                                                                        {user_inputs[10]}10
                                                                                                                                        OR
                                                                                                                                        FREE
                                                                                                                                        ON
                                                                                                                                        ORDERS
                                                                                                                                        {user_inputs[10]}195+*<br>EXPEDITED
                                                                                                                                        SHIPPING
                                                                                                                                        {user_inputs[10]}20*</span></a>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <td height="20"
                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                            <td width="20"
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                                <table width="100%" cellpadding="0"
                                                                                    cellspacing="0" bgcolor="#ffffff"
                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                    <tbody
                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                        <tr
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <td height="20"
                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <td align="center" valign="top"
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <table width="600"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                    <tbody
                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                        <tr
                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            <td width="50"
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            </td>
                                                                                                            <td align="center"
                                                                                                                valign="top"
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <table
                                                                                                                    width="100%"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                    <tbody
                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                        <tr
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <td align="center"
                                                                                                                                valign="top"
                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                <table
                                                                                                                                    width="504"
                                                                                                                                    cellpadding="0"
                                                                                                                                    cellspacing="0"
                                                                                                                                    style="max-width:504px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                    <tbody
                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                        <tr
                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            <td align="center"
                                                                                                                                                valign="top"
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <table
                                                                                                                                                    width="232"
                                                                                                                                                    cellpadding="0"
                                                                                                                                                    cellspacing="0"
                                                                                                                                                    align="left"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                    <tbody
                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                        <tr
                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                            <td align="center"
                                                                                                                                                                valign="top"
                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                <table
                                                                                                                                                                    cellpadding="0"
                                                                                                                                                                    cellspacing="0"
                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                    <tbody
                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                        <tr
                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            <td align="center"
                                                                                                                                                                                valign="top"
                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                <table
                                                                                                                                                                                    width="96"
                                                                                                                                                                                    cellpadding="0"
                                                                                                                                                                                    cellspacing="0"
                                                                                                                                                                                    align="left"
                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                    <tbody
                                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                        <tr
                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            <td align="center"
                                                                                                                                                                                                valign="top"
                                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                                <a href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/141c118f?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxY2Y3ZmMxOWNiNzAwMDNmZTU5IiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvY2FcL2FmdGVycGF5LWZhcS5odG1sP3V0bV9zb3VyY2U9VVNfVHJhbnNhY3Rpb25hbCZ1dG1fbWVkaXVtPWVtYWlsJnV0bV9jYW1wYWlnbj1VX1RYTkxfT1JERVJfQ09ORklSTUFUSU9OX0VOLUNBJmhtYWlsPWRkYWIyODk4NGNiZDBmNjExNjdlNWU3M2I3NWI2NWU1MjFiMDNkNmE3NTY4OWNjMWY1MTMyODQ1YTA4MTg2OTkmYnhpZD02NTc3MWUwZThhMDFhMTE3MTEwMTYzZjgifQ&amp;jwtS=uiBgqAxwz-r9A4_yaP7eqUAg3fFKCMHsHM_lPptcm20"
                                                                                                                                                                                                    target="_blank"
                                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif"><img
                                                                                                                                                                                                        src="https://images.usw2.cordial.com/1663/95x63/ugg_icons_1_afterpay.png"
                                                                                                                                                                                                        width="95"
                                                                                                                                                                                                        border="0"
                                                                                                                                                                                                        style="display: block; height: auto; max-width: none; font-family: 'Proxima Nova', Arial, sans-serif;"
                                                                                                                                                                                                        alt=""></a>
                                                                                                                                                                                            </td>
                                                                                                                                                                                        </tr>
                                                                                                                                                                                        <tr
                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            <td height="10"
                                                                                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            </td>
                                                                                                                                                                                        </tr>
                                                                                                                                                                                        <tr
                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            <td align="center"
                                                                                                                                                                                                valign="top"
                                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif;font-size:14px;line-height:20px;font-weight:700;color:rgb(0,0,1)">
                                                                                                                                                                                                <a style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif"
                                                                                                                                                                                                    href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/118768b3?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxY2Y3ZmMxOWNiNzAwMDNmZTVhIiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvY2FcL2FmdGVycGF5LWZhcS5odG1sP3V0bV9zb3VyY2U9VVNfVHJhbnNhY3Rpb25hbCZ1dG1fbWVkaXVtPWVtYWlsJnV0bV9jYW1wYWlnbj1VX1RYTkxfT1JERVJfQ09ORklSTUFUSU9OX0VOLUNBJmhtYWlsPWRkYWIyODk4NGNiZDBmNjExNjdlNWU3M2I3NWI2NWU1MjFiMDNkNmE3NTY4OWNjMWY1MTMyODQ1YTA4MTg2OTkmYnhpZD02NTc3MWUwZThhMDFhMTE3MTEwMTYzZjgifQ&amp;jwtS=nJox7syuQ9cJ07px0tCpjk8_QSD_hr6T_zUj4bww0PQ"
                                                                                                                                                                                                    target="_blank"><span
                                                                                                                                                                                                        style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif;color:rgb(0,0,1)">Buy
                                                                                                                                                                                                        Now,<br>Pay
                                                                                                                                                                                                        Later
                                                                                                                                                                                                        With<br>Afterpay</span></a>
                                                                                                                                                                                            </td>
                                                                                                                                                                                        </tr>
                                                                                                                                                                                    </tbody>
                                                                                                                                                                                </table>
                                                                                                                                                                                <table
                                                                                                                                                                                    width="40"
                                                                                                                                                                                    height="40"
                                                                                                                                                                                    cellpadding="0"
                                                                                                                                                                                    cellspacing="0"
                                                                                                                                                                                    align="left"
                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                    <tbody
                                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                        <tr
                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            <td width="40"
                                                                                                                                                                                                height="40"
                                                                                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            </td>
                                                                                                                                                                                        </tr>
                                                                                                                                                                                    </tbody>
                                                                                                                                                                                </table>
                                                                                                                                                                                <table
                                                                                                                                                                                    width="96"
                                                                                                                                                                                    cellpadding="0"
                                                                                                                                                                                    cellspacing="0"
                                                                                                                                                                                    align="left"
                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                    <tbody
                                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                        <tr
                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            <td align="center"
                                                                                                                                                                                                valign="top"
                                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                                <a href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/9df26724?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxZDA3ZmMxOWNiNzAwMDNmZTViIiwibGlua1VybCI6Imh0dHBzOlwvXC91Z2ctY2EuYXR0bi50dlwvcFwvRUV2XC9sYW5kaW5nLXBhZ2U_dXRtX3NvdXJjZT1VU19UcmFuc2FjdGlvbmFsJnV0bV9tZWRpdW09ZW1haWwmdXRtX2NhbXBhaWduPVVfVFhOTF9PUkRFUl9DT05GSVJNQVRJT05fRU4tQ0EmaG1haWw9ZGRhYjI4OTg0Y2JkMGY2MTE2N2U1ZTczYjc1YjY1ZTUyMWIwM2Q2YTc1Njg5Y2MxZjUxMzI4NDVhMDgxODY5OSZieGlkPTY1NzcxZTBlOGEwMWExMTcxMTAxNjNmOCJ9&amp;jwtS=gwcYbBQOZDH-1nEf6CgM2u9hvXuKiyGY3GZMpBupuvY"
                                                                                                                                                                                                    target="_blank"
                                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif"><img
                                                                                                                                                                                                        src="https://images.usw2.cordial.com/1663/95x63/ugg_icons_2_textOffers.png"
                                                                                                                                                                                                        width="95"
                                                                                                                                                                                                        border="0"
                                                                                                                                                                                                        style="display: block; height: auto; max-width: none; font-family: 'Proxima Nova', Arial, sans-serif;"
                                                                                                                                                                                                        alt=""></a>
                                                                                                                                                                                            </td>
                                                                                                                                                                                        </tr>
                                                                                                                                                                                        <tr
                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            <td height="10"
                                                                                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            </td>
                                                                                                                                                                                        </tr>
                                                                                                                                                                                        <tr
                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            <td align="center"
                                                                                                                                                                                                valign="top"
                                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif;font-size:14px;line-height:20px;font-weight:700;color:rgb(0,0,1)">
                                                                                                                                                                                                <a style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif"
                                                                                                                                                                                                    href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/e5a8bd12?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxZDA3ZmMxOWNiNzAwMDNmZTVjIiwibGlua1VybCI6Imh0dHBzOlwvXC91Z2ctY2EuYXR0bi50dlwvcFwvRUV2XC9sYW5kaW5nLXBhZ2U_dXRtX3NvdXJjZT1VU19UcmFuc2FjdGlvbmFsJnV0bV9tZWRpdW09ZW1haWwmdXRtX2NhbXBhaWduPVVfVFhOTF9PUkRFUl9DT05GSVJNQVRJT05fRU4tQ0EmaG1haWw9ZGRhYjI4OTg0Y2JkMGY2MTE2N2U1ZTczYjc1YjY1ZTUyMWIwM2Q2YTc1Njg5Y2MxZjUxMzI4NDVhMDgxODY5OSZieGlkPTY1NzcxZTBlOGEwMWExMTcxMTAxNjNmOCJ9&amp;jwtS=Q23YM4H-Ii0Jo-xb4Ds_NRABMkyRODhbpSnl6BRLMlk"
                                                                                                                                                                                                    target="_blank"><span
                                                                                                                                                                                                        style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif;color:rgb(0,0,1)">Sign
                                                                                                                                                                                                        Up
                                                                                                                                                                                                        For
                                                                                                                                                                                                        Text
                                                                                                                                                                                                        Offers</span></a>
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
                                                                                                                                                    width="272"
                                                                                                                                                    cellpadding="0"
                                                                                                                                                    cellspacing="0"
                                                                                                                                                    align="left"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                    <tbody
                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                        <tr
                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                            <td align="center"
                                                                                                                                                                valign="top"
                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                <table
                                                                                                                                                                    cellpadding="0"
                                                                                                                                                                    cellspacing="0"
                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                    <tbody
                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                        <tr
                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                            <td align="center"
                                                                                                                                                                                valign="top"
                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                <table
                                                                                                                                                                                    width="40"
                                                                                                                                                                                    height="40"
                                                                                                                                                                                    cellpadding="0"
                                                                                                                                                                                    cellspacing="0"
                                                                                                                                                                                    align="left"
                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                    <tbody
                                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                        <tr
                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            <td width="40"
                                                                                                                                                                                                height="40"
                                                                                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            </td>
                                                                                                                                                                                        </tr>
                                                                                                                                                                                    </tbody>
                                                                                                                                                                                </table>
                                                                                                                                                                                <table
                                                                                                                                                                                    width="96"
                                                                                                                                                                                    cellpadding="0"
                                                                                                                                                                                    cellspacing="0"
                                                                                                                                                                                    align="left"
                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                    <tbody
                                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                        <tr
                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            <td align="center"
                                                                                                                                                                                                valign="top"
                                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                                <a href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/a58fb3ae?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxZDA3ZmMxOWNiNzAwMDNmZTVkIiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvcHJvbW9zLWNvdXBvbnMtZGlzY291bnRzXC8_dXRtX3NvdXJjZT1VU19UcmFuc2FjdGlvbmFsJnV0bV9tZWRpdW09ZW1haWwmdXRtX2NhbXBhaWduPVVfVFhOTF9PUkRFUl9DT05GSVJNQVRJT05fRU4tQ0EmaG1haWw9ZGRhYjI4OTg0Y2JkMGY2MTE2N2U1ZTczYjc1YjY1ZTUyMWIwM2Q2YTc1Njg5Y2MxZjUxMzI4NDVhMDgxODY5OSZieGlkPTY1NzcxZTBlOGEwMWExMTcxMTAxNjNmOCJ9&amp;jwtS=tURAXFj92_KGbQpa758dLajtQ_PMAtgz6_10qx449s4"
                                                                                                                                                                                                    target="_blank"
                                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif"><img
                                                                                                                                                                                                        src="https://images.usw2.cordial.com/1663/95x63/ugg_icons_3_discount.png"
                                                                                                                                                                                                        width="95"
                                                                                                                                                                                                        border="0"
                                                                                                                                                                                                        style="display: block; height: auto; max-width: none; font-family: 'Proxima Nova', Arial, sans-serif;"
                                                                                                                                                                                                        alt=""></a>
                                                                                                                                                                                            </td>
                                                                                                                                                                                        </tr>
                                                                                                                                                                                        <tr
                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            <td height="10"
                                                                                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            </td>
                                                                                                                                                                                        </tr>
                                                                                                                                                                                        <tr
                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            <td align="center"
                                                                                                                                                                                                valign="top"
                                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif;font-size:14px;line-height:20px;font-weight:700;color:rgb(0,0,1)">
                                                                                                                                                                                                <a style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif"
                                                                                                                                                                                                    href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/231ec74f?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxZDA3ZmMxOWNiNzAwMDNmZTVlIiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvcHJvbW9zLWNvdXBvbnMtZGlzY291bnRzXC8_dXRtX3NvdXJjZT1VU19UcmFuc2FjdGlvbmFsJnV0bV9tZWRpdW09ZW1haWwmdXRtX2NhbXBhaWduPVVfVFhOTF9PUkRFUl9DT05GSVJNQVRJT05fRU4tQ0EmaG1haWw9ZGRhYjI4OTg0Y2JkMGY2MTE2N2U1ZTczYjc1YjY1ZTUyMWIwM2Q2YTc1Njg5Y2MxZjUxMzI4NDVhMDgxODY5OSZieGlkPTY1NzcxZTBlOGEwMWExMTcxMTAxNjNmOCJ9&amp;jwtS=6RaEYgBvyjegi7jWtuQBn6cEV7vl8BfC5W4bWCFHe7A"
                                                                                                                                                                                                    target="_blank"><span
                                                                                                                                                                                                        style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif;color:rgb(0,0,1)">Student
                                                                                                                                                                                                        Discount</span></a>
                                                                                                                                                                                            </td>
                                                                                                                                                                                        </tr>
                                                                                                                                                                                    </tbody>
                                                                                                                                                                                </table>
                                                                                                                                                                                <table
                                                                                                                                                                                    width="40"
                                                                                                                                                                                    height="40"
                                                                                                                                                                                    cellpadding="0"
                                                                                                                                                                                    cellspacing="0"
                                                                                                                                                                                    align="left"
                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                    <tbody
                                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                        <tr
                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            <td width="40"
                                                                                                                                                                                                height="40"
                                                                                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            </td>
                                                                                                                                                                                        </tr>
                                                                                                                                                                                    </tbody>
                                                                                                                                                                                </table>
                                                                                                                                                                                <table
                                                                                                                                                                                    width="96"
                                                                                                                                                                                    cellpadding="0"
                                                                                                                                                                                    cellspacing="0"
                                                                                                                                                                                    align="left"
                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                    <tbody
                                                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                        <tr
                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            <td align="center"
                                                                                                                                                                                                valign="top"
                                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                                <a href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/5cb1facf?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxZDA3ZmMxOWNiNzAwMDNmZTVmIiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvY2FcL3N0b3Jlcy5odG1sP3V0bV9zb3VyY2U9VVNfVHJhbnNhY3Rpb25hbCZ1dG1fbWVkaXVtPWVtYWlsJnV0bV9jYW1wYWlnbj1VX1RYTkxfT1JERVJfQ09ORklSTUFUSU9OX0VOLUNBJmhtYWlsPWRkYWIyODk4NGNiZDBmNjExNjdlNWU3M2I3NWI2NWU1MjFiMDNkNmE3NTY4OWNjMWY1MTMyODQ1YTA4MTg2OTkmYnhpZD02NTc3MWUwZThhMDFhMTE3MTEwMTYzZjgifQ&amp;jwtS=q00nhlkyq5k6HK9uAon15_ggSFWUvMctosIZJgBia4Y"
                                                                                                                                                                                                    target="_blank"
                                                                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif"><img
                                                                                                                                                                                                        src="https://images.usw2.cordial.com/1663/95x63/ugg_icons_4_storeNearYou.png"
                                                                                                                                                                                                        width="95"
                                                                                                                                                                                                        border="0"
                                                                                                                                                                                                        style="display: block; height: auto; max-width: none; font-family: 'Proxima Nova', Arial, sans-serif;"
                                                                                                                                                                                                        alt=""></a>
                                                                                                                                                                                            </td>
                                                                                                                                                                                        </tr>
                                                                                                                                                                                        <tr
                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            <td height="10"
                                                                                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            </td>
                                                                                                                                                                                        </tr>
                                                                                                                                                                                        <tr
                                                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                                                            <td align="center"
                                                                                                                                                                                                valign="top"
                                                                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif;font-size:14px;line-height:20px;font-weight:700;color:rgb(0,0,1)">
                                                                                                                                                                                                <a style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif"
                                                                                                                                                                                                    href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/5a78b090?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxZDA3ZmMxOWNiNzAwMDNmZTYwIiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvY2FcL3N0b3Jlcy5odG1sP3V0bV9zb3VyY2U9VVNfVHJhbnNhY3Rpb25hbCZ1dG1fbWVkaXVtPWVtYWlsJnV0bV9jYW1wYWlnbj1VX1RYTkxfT1JERVJfQ09ORklSTUFUSU9OX0VOLUNBJmhtYWlsPWRkYWIyODk4NGNiZDBmNjExNjdlNWU3M2I3NWI2NWU1MjFiMDNkNmE3NTY4OWNjMWY1MTMyODQ1YTA4MTg2OTkmYnhpZD02NTc3MWUwZThhMDFhMTE3MTEwMTYzZjgifQ&amp;jwtS=nT_VbdnvvQh04xtDAS6hL6cOIesdkH-V-8RpJaNBcZA"
                                                                                                                                                                                                    target="_blank"><span
                                                                                                                                                                                                        style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif;color:rgb(0,0,1)">Find
                                                                                                                                                                                                        A
                                                                                                                                                                                                        Store
                                                                                                                                                                                                        Near
                                                                                                                                                                                                        You</span></a>
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
                                                                                                            </td>
                                                                                                            <td width="50"
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <td height="10"
                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            </td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                                <table width="100%" cellpadding="0"
                                                                                    cellspacing="0" bgcolor="#ffffff"
                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                    <tbody
                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                        <tr
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <td height="20"
                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <td align="center" valign="top"
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <table width="600"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                    <tbody
                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                        <tr
                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            <td align="center"
                                                                                                                valign="top"
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <table
                                                                                                                    width="100%"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                    <tbody
                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                        <tr
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <td align="center"
                                                                                                                                valign="top"
                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                <table
                                                                                                                                    width="100%"
                                                                                                                                    cellspacing="0"
                                                                                                                                    cellpadding="0"
                                                                                                                                    border="0"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                    <tbody
                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                        <tr
                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            <td height="1"
                                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif;background-color:rgb(0,0,0)">
                                                                                                                                            </td>
                                                                                                                                        </tr>
                                                                                                                                        <tr
                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            <td align="center"
                                                                                                                                                valign="top"
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <table
                                                                                                                                                    cellspacing="0"
                                                                                                                                                    cellpadding="0"
                                                                                                                                                    border="0"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                    <tbody
                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                        <tr
                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                            <td align="center"
                                                                                                                                                                style="width:600px;border-radius:initial;box-sizing:border-box;font-family:'Proxima Nova',Arial,sans-serif;background-color:rgb(255,255,255)">
                                                                                                                                                                <a style="padding:18px 12px;border:1px solid rgb(255,255,255);border-radius:initial;font-family:'Proxima Nova',Arial,sans-serif;font-size:14px;line-height:15px;font-weight:700;display:block;text-decoration:none;color:rgb(0,0,1)"
                                                                                                                                                                    href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/29e62286?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxZDA3ZmMxOWNiNzAwMDNmZTYxIiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvY2FcL3dvbWVuLW5ldy1hcnJpdmFsc1wvP3V0bV9zb3VyY2U9VVNfVHJhbnNhY3Rpb25hbCZ1dG1fbWVkaXVtPWVtYWlsJnV0bV9jYW1wYWlnbj1VX1RYTkxfT1JERVJfQ09ORklSTUFUSU9OX0VOLUNBJmhtYWlsPWRkYWIyODk4NGNiZDBmNjExNjdlNWU3M2I3NWI2NWU1MjFiMDNkNmE3NTY4OWNjMWY1MTMyODQ1YTA4MTg2OTkmYnhpZD02NTc3MWUwZThhMDFhMTE3MTEwMTYzZjgifQ&amp;jwtS=41b8BOTnfavDJIzGxJC4MtubFwlgpPEkiRn1gi9HoKg"
                                                                                                                                                                    target="_blank"><span
                                                                                                                                                                        style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif;color:rgb(0,0,1)">SHOP
                                                                                                                                                                        WOMEN</span></a>
                                                                                                                                                            </td>
                                                                                                                                                        </tr>
                                                                                                                                                    </tbody>
                                                                                                                                                </table>
                                                                                                                                            </td>
                                                                                                                                        </tr>
                                                                                                                                        <tr
                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            <td height="1"
                                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif;background-color:rgb(0,0,0)">
                                                                                                                                            </td>
                                                                                                                                        </tr>
                                                                                                                                        <tr
                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            <td align="center"
                                                                                                                                                valign="top"
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <table
                                                                                                                                                    cellspacing="0"
                                                                                                                                                    cellpadding="0"
                                                                                                                                                    border="0"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                    <tbody
                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                        <tr
                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                            <td align="center"
                                                                                                                                                                style="width:600px;border-radius:initial;box-sizing:border-box;font-family:'Proxima Nova',Arial,sans-serif;background-color:rgb(255,255,255)">
                                                                                                                                                                <a style="padding:18px 12px;border:1px solid rgb(255,255,255);border-radius:initial;font-family:'Proxima Nova',Arial,sans-serif;font-size:14px;line-height:15px;font-weight:700;display:block;text-decoration:none;color:rgb(0,0,1)"
                                                                                                                                                                    href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/081915f2?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxZDA3ZmMxOWNiNzAwMDNmZTYyIiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvY2FcL21lbi1uZXctYXJyaXZhbHNcLz91dG1fc291cmNlPVVTX1RyYW5zYWN0aW9uYWwmdXRtX21lZGl1bT1lbWFpbCZ1dG1fY2FtcGFpZ249VV9UWE5MX09SREVSX0NPTkZJUk1BVElPTl9FTi1DQSZobWFpbD1kZGFiMjg5ODRjYmQwZjYxMTY3ZTVlNzNiNzViNjVlNTIxYjAzZDZhNzU2ODljYzFmNTEzMjg0NWEwODE4Njk5JmJ4aWQ9NjU3NzFlMGU4YTAxYTExNzExMDE2M2Y4In0&amp;jwtS=jsEiIJjqUmmsVo7d2GNRkn4yNh5g27lzMIenOGdcU6M"
                                                                                                                                                                    target="_blank"><span
                                                                                                                                                                        style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif;color:rgb(0,0,1)">SHOP
                                                                                                                                                                        MEN</span></a>
                                                                                                                                                            </td>
                                                                                                                                                        </tr>
                                                                                                                                                    </tbody>
                                                                                                                                                </table>
                                                                                                                                            </td>
                                                                                                                                        </tr>
                                                                                                                                        <tr
                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            <td height="1"
                                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif;background-color:rgb(0,0,0)">
                                                                                                                                            </td>
                                                                                                                                        </tr>
                                                                                                                                        <tr
                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            <td align="center"
                                                                                                                                                valign="top"
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <table
                                                                                                                                                    cellspacing="0"
                                                                                                                                                    cellpadding="0"
                                                                                                                                                    border="0"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                    <tbody
                                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                        <tr
                                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                            <td align="center"
                                                                                                                                                                style="width:600px;border-radius:initial;box-sizing:border-box;font-family:'Proxima Nova',Arial,sans-serif;background-color:rgb(255,255,255)">
                                                                                                                                                                <a style="padding:18px 12px;border:1px solid rgb(255,255,255);border-radius:initial;font-family:'Proxima Nova',Arial,sans-serif;font-size:14px;line-height:15px;font-weight:700;display:block;text-decoration:none;color:rgb(0,0,1)"
                                                                                                                                                                    href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/9e8c7b3b?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxZDA3ZmMxOWNiNzAwMDNmZTYzIiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvY2FcL2tpZHMtbmV3LWFycml2YWxzXC8_dXRtX3NvdXJjZT1VU19UcmFuc2FjdGlvbmFsJnV0bV9tZWRpdW09ZW1haWwmdXRtX2NhbXBhaWduPVVfVFhOTF9PUkRFUl9DT05GSVJNQVRJT05fRU4tQ0EmaG1haWw9ZGRhYjI4OTg0Y2JkMGY2MTE2N2U1ZTczYjc1YjY1ZTUyMWIwM2Q2YTc1Njg5Y2MxZjUxMzI4NDVhMDgxODY5OSZieGlkPTY1NzcxZTBlOGEwMWExMTcxMTAxNjNmOCJ9&amp;jwtS=OKm5YFimtsQHBnI5Ar0gKZ6NCOFNM1jcUzqH6fpLERA"
                                                                                                                                                                    target="_blank"><span
                                                                                                                                                                        style="text-decoration:none;font-family:'Proxima Nova',Arial,sans-serif;color:rgb(0,0,1)">SHOP
                                                                                                                                                                        KIDS</span></a>
                                                                                                                                                            </td>
                                                                                                                                                        </tr>
                                                                                                                                                    </tbody>
                                                                                                                                                </table>
                                                                                                                                            </td>
                                                                                                                                        </tr>
                                                                                                                                        <tr
                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            <td height="1"
                                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif;background-color:rgb(0,0,0)">
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
                                                                                        <tr
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <td height="20"
                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            </td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                                <table width="100%" cellpadding="0"
                                                                                    cellspacing="0" bgcolor="#ffffff"
                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                    <tbody
                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                        <tr
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <td height="10"
                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <td align="center" valign="top"
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <table width="600"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                    <tbody
                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                        <tr
                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            <td width="20"
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            </td>
                                                                                                            <td align="center"
                                                                                                                valign="top"
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <table
                                                                                                                    width="100%"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                    <tbody
                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                        <tr
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <td align="center"
                                                                                                                                valign="top"
                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                <table
                                                                                                                                    cellpadding="0"
                                                                                                                                    cellspacing="0"
                                                                                                                                    style="max-width:340px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                    <tbody
                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                        <tr
                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            <td width="11.764705882353%"
                                                                                                                                                align="left"
                                                                                                                                                valign="top"
                                                                                                                                                bgcolor=""
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <a href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/704aaa5b?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxZDA3ZmMxOWNiNzAwMDNmZTY0IiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvYmxvZz91dG1fc291cmNlPVVTX1RyYW5zYWN0aW9uYWwmdXRtX21lZGl1bT1lbWFpbCZ1dG1fY2FtcGFpZ249VV9UWE5MX09SREVSX0NPTkZJUk1BVElPTl9FTi1DQSZobWFpbD1kZGFiMjg5ODRjYmQwZjYxMTY3ZTVlNzNiNzViNjVlNTIxYjAzZDZhNzU2ODljYzFmNTEzMjg0NWEwODE4Njk5JmJ4aWQ9NjU3NzFlMGU4YTAxYTExNzExMDE2M2Y4In0&amp;jwtS=hEXFmvqf_B1gJd8M7OEQY0H7QkUGVx7RFthyJwKXkbs"
                                                                                                                                                    target="_blank"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif"><img
                                                                                                                                                        src="https://images.usw2.cordial.com/1663/40x40/ugg_social_1_blog_2022.png"
                                                                                                                                                        width="40"
                                                                                                                                                        border="0"
                                                                                                                                                        style="display: block; height: auto; font-family: 'Proxima Nova', Arial, sans-serif;"
                                                                                                                                                        alt="Blog"></a>
                                                                                                                                            </td>
                                                                                                                                            <td width="2.9411764705882%"
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            </td>
                                                                                                                                            <td width="11.764705882353%"
                                                                                                                                                align="left"
                                                                                                                                                valign="top"
                                                                                                                                                bgcolor=""
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <a href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/e5f78b6c?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxZDA3ZmMxOWNiNzAwMDNmZTY1IiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cuZmFjZWJvb2suY29tXC9VR0dcLz91dG1fc291cmNlPVVTX1RyYW5zYWN0aW9uYWwmdXRtX21lZGl1bT1lbWFpbCZ1dG1fY2FtcGFpZ249VV9UWE5MX09SREVSX0NPTkZJUk1BVElPTl9FTi1DQSZobWFpbD1kZGFiMjg5ODRjYmQwZjYxMTY3ZTVlNzNiNzViNjVlNTIxYjAzZDZhNzU2ODljYzFmNTEzMjg0NWEwODE4Njk5JmJ4aWQ9NjU3NzFlMGU4YTAxYTExNzExMDE2M2Y4In0&amp;jwtS=-QFEuLe1T1C7L0eO3EWLiRb7aFvesH25b27s0pKAVSw"
                                                                                                                                                    target="_blank"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif"><img
                                                                                                                                                        src="https://images.usw2.cordial.com/1663/40x40/ugg_social_2_fb_2022.png"
                                                                                                                                                        width="40"
                                                                                                                                                        border="0"
                                                                                                                                                        style="display: block; height: auto; font-family: 'Proxima Nova', Arial, sans-serif;"
                                                                                                                                                        alt="Facebook"></a>
                                                                                                                                            </td>
                                                                                                                                            <td width="2.9411764705882%"
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            </td>
                                                                                                                                            <td width="11.764705882353%"
                                                                                                                                                align="left"
                                                                                                                                                valign="top"
                                                                                                                                                bgcolor=""
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <a href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/7ab1d137?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxZDA3ZmMxOWNiNzAwMDNmZTY2IiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cuaW5zdGFncmFtLmNvbVwvdWdnXC8_dXRtX3NvdXJjZT1VU19UcmFuc2FjdGlvbmFsJnV0bV9tZWRpdW09ZW1haWwmdXRtX2NhbXBhaWduPVVfVFhOTF9PUkRFUl9DT05GSVJNQVRJT05fRU4tQ0EmaG1haWw9ZGRhYjI4OTg0Y2JkMGY2MTE2N2U1ZTczYjc1YjY1ZTUyMWIwM2Q2YTc1Njg5Y2MxZjUxMzI4NDVhMDgxODY5OSZieGlkPTY1NzcxZTBlOGEwMWExMTcxMTAxNjNmOCJ9&amp;jwtS=a_i6-Cm-V-aAK3y1eOhCYfvowPcvGgQVWGLKS0QWPPg"
                                                                                                                                                    target="_blank"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif"><img
                                                                                                                                                        src="https://images.usw2.cordial.com/1663/40x40/ugg_social_3_inst_2022.png"
                                                                                                                                                        width="40"
                                                                                                                                                        border="0"
                                                                                                                                                        style="display: block; height: auto; font-family: 'Proxima Nova', Arial, sans-serif;"
                                                                                                                                                        alt="Instagram"></a>
                                                                                                                                            </td>
                                                                                                                                            <td width="2.9411764705882%"
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            </td>
                                                                                                                                            <td width="11.764705882353%"
                                                                                                                                                align="left"
                                                                                                                                                valign="top"
                                                                                                                                                bgcolor=""
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <a href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/3c1fb942?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxZDA3ZmMxOWNiNzAwMDNmZTY3IiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cucGludGVyZXN0LmNvbVwvdWdnXC8_dXRtX3NvdXJjZT1VU19UcmFuc2FjdGlvbmFsJnV0bV9tZWRpdW09ZW1haWwmdXRtX2NhbXBhaWduPVVfVFhOTF9PUkRFUl9DT05GSVJNQVRJT05fRU4tQ0EmaG1haWw9ZGRhYjI4OTg0Y2JkMGY2MTE2N2U1ZTczYjc1YjY1ZTUyMWIwM2Q2YTc1Njg5Y2MxZjUxMzI4NDVhMDgxODY5OSZieGlkPTY1NzcxZTBlOGEwMWExMTcxMTAxNjNmOCJ9&amp;jwtS=qaBtixyv0dWYJXSXMfsXctJbD1PHtMr4qc02DV5rOOk"
                                                                                                                                                    target="_blank"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif"><img
                                                                                                                                                        src="https://images.usw2.cordial.com/1663/40x40/ugg_social_4_pi_2022.png"
                                                                                                                                                        width="40"
                                                                                                                                                        border="0"
                                                                                                                                                        style="display: block; height: auto; font-family: 'Proxima Nova', Arial, sans-serif;"
                                                                                                                                                        alt="Pinterest"></a>
                                                                                                                                            </td>
                                                                                                                                            <td width="2.9411764705882%"
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            </td>
                                                                                                                                            <td width="11.764705882353%"
                                                                                                                                                align="left"
                                                                                                                                                valign="top"
                                                                                                                                                bgcolor=""
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <a href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/986353f2?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxZDA3ZmMxOWNiNzAwMDNmZTY4IiwibGlua1VybCI6Imh0dHBzOlwvXC90d2l0dGVyLmNvbVwvdWdnP3V0bV9zb3VyY2U9VVNfVHJhbnNhY3Rpb25hbCZ1dG1fbWVkaXVtPWVtYWlsJnV0bV9jYW1wYWlnbj1VX1RYTkxfT1JERVJfQ09ORklSTUFUSU9OX0VOLUNBJmhtYWlsPWRkYWIyODk4NGNiZDBmNjExNjdlNWU3M2I3NWI2NWU1MjFiMDNkNmE3NTY4OWNjMWY1MTMyODQ1YTA4MTg2OTkmYnhpZD02NTc3MWUwZThhMDFhMTE3MTEwMTYzZjgifQ&amp;jwtS=zRo8OX65xRUoeJdXe-8YzylZlLfdWszmJMJfZ7xo3OI"
                                                                                                                                                    target="_blank"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif"><img
                                                                                                                                                        src="https://images.usw2.cordial.com/1663/40x40/ugg_social_5_tw_2022.png"
                                                                                                                                                        width="40"
                                                                                                                                                        border="0"
                                                                                                                                                        style="display: block; height: auto; font-family: 'Proxima Nova', Arial, sans-serif;"
                                                                                                                                                        alt="Twitter"></a>
                                                                                                                                            </td>
                                                                                                                                            <td width="2.9411764705882%"
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            </td>
                                                                                                                                            <td width="11.764705882353%"
                                                                                                                                                align="left"
                                                                                                                                                valign="top"
                                                                                                                                                bgcolor=""
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <a href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/64182523?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxZDA3ZmMxOWNiNzAwMDNmZTY5IiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cuc25hcGNoYXQuY29tXC9hZGRcL3VnZ29mZmljaWFsP3V0bV9zb3VyY2U9VVNfVHJhbnNhY3Rpb25hbCZ1dG1fbWVkaXVtPWVtYWlsJnV0bV9jYW1wYWlnbj1VX1RYTkxfT1JERVJfQ09ORklSTUFUSU9OX0VOLUNBJmhtYWlsPWRkYWIyODk4NGNiZDBmNjExNjdlNWU3M2I3NWI2NWU1MjFiMDNkNmE3NTY4OWNjMWY1MTMyODQ1YTA4MTg2OTkmYnhpZD02NTc3MWUwZThhMDFhMTE3MTEwMTYzZjgifQ&amp;jwtS=2rCD8tpHpBtrFljaSDGaorsviiTA6GdsWgb8PrDfVFU"
                                                                                                                                                    target="_blank"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif"><img
                                                                                                                                                        src="https://images.usw2.cordial.com/1663/40x40/ugg_social_6_sn_2022.png"
                                                                                                                                                        width="40"
                                                                                                                                                        border="0"
                                                                                                                                                        style="display: block; height: auto; font-family: 'Proxima Nova', Arial, sans-serif;"
                                                                                                                                                        alt="Snapchat"></a>
                                                                                                                                            </td>
                                                                                                                                            <td width="2.9411764705882%"
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                            </td>
                                                                                                                                            <td width="11.764705882353%"
                                                                                                                                                align="left"
                                                                                                                                                valign="top"
                                                                                                                                                bgcolor=""
                                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                                <a href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/48b280a4?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxZDA3ZmMxOWNiNzAwMDNmZTZhIiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cueW91dHViZS5jb21cL2NcL3VnZz91dG1fc291cmNlPVVTX1RyYW5zYWN0aW9uYWwmdXRtX21lZGl1bT1lbWFpbCZ1dG1fY2FtcGFpZ249VV9UWE5MX09SREVSX0NPTkZJUk1BVElPTl9FTi1DQSZobWFpbD1kZGFiMjg5ODRjYmQwZjYxMTY3ZTVlNzNiNzViNjVlNTIxYjAzZDZhNzU2ODljYzFmNTEzMjg0NWEwODE4Njk5JmJ4aWQ9NjU3NzFlMGU4YTAxYTExNzExMDE2M2Y4In0&amp;jwtS=hg3FRPDhwmX7O1LnakvOxJYBJjRRrxXKAM2J6SyKukM"
                                                                                                                                                    target="_blank"
                                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif"><img
                                                                                                                                                        src="https://images.usw2.cordial.com/1663/40x40/ugg_social_7_yt_2022.png"
                                                                                                                                                        width="40"
                                                                                                                                                        border="0"
                                                                                                                                                        style="display: block; height: auto; font-family: 'Proxima Nova', Arial, sans-serif;"
                                                                                                                                                        alt="YouTube"></a>
                                                                                                                                            </td>
                                                                                                                                        </tr>
                                                                                                                                    </tbody>
                                                                                                                                </table>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                            <td width="20"
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <td height="10"
                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            </td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                                <div style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                    <table width="100%" cellpadding="0" cellspacing="0"
                                                                        bgcolor="#ffffff"
                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                        <tbody
                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                            <tr
                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                <td align="center" valign="top"
                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                    <table width="600" cellpadding="0"
                                                                                        cellspacing="0" bgcolor="#ffffff"
                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                        <tbody
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <tr
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <td height="10"
                                                                                                    style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                </td>
                                                                                            </tr>
                                                                                            <tr
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <td align="center"
                                                                                                    valign="top"
                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                    <table width="100%"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                        <tbody
                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            <tr
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <td width="75"
                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                </td>
                                                                                                                <td align="center"
                                                                                                                    valign="top"
                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                    <table
                                                                                                                        width="100%"
                                                                                                                        cellpadding="0"
                                                                                                                        cellspacing="0"
                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                        <tbody
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <tr
                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                <td align="center"
                                                                                                                                    valign="top"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif;font-size:11px;line-height:15px;font-weight:400;color:rgb(0,0,1)">
                                                                                                                                    *We
                                                                                                                                    charge
                                                                                                                                    a
                                                                                                                                    flat
                                                                                                                                    shipping
                                                                                                                                    rate
                                                                                                                                    of
                                                                                                                                    {user_inputs[10]}10
                                                                                                                                    per
                                                                                                                                    orders
                                                                                                                                    placed
                                                                                                                                    on<span
                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                                    </span><a
                                                                                                                                        href="http://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/45e486d7?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxZDA3ZmMxOWNiNzAwMDNmZTZiIiwibGlua1VybCI6Imh0dHA6XC9cL3VnZy5jb21cL2NhP3V0bV9zb3VyY2U9VVNfVHJhbnNhY3Rpb25hbCZ1dG1fbWVkaXVtPWVtYWlsJnV0bV9jYW1wYWlnbj1VX1RYTkxfT1JERVJfQ09ORklSTUFUSU9OX0VOLUNBJmhtYWlsPWRkYWIyODk4NGNiZDBmNjExNjdlNWU3M2I3NWI2NWU1MjFiMDNkNmE3NTY4OWNjMWY1MTMyODQ1YTA4MTg2OTkmYnhpZD02NTc3MWUwZThhMDFhMTE3MTEwMTYzZjgifQ&amp;jwtS=HM3aKJm997RBkyPzoRJfG_of7o4GJxAMqRQI0p-Djh0"
                                                                                                                                        target="_blank"
                                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">ugg.com</a>.
                                                                                                                                    Please
                                                                                                                                    expect
                                                                                                                                    your
                                                                                                                                    delivery
                                                                                                                                    in
                                                                                                                                    2-4
                                                                                                                                    business
                                                                                                                                    days.
                                                                                                                                    In
                                                                                                                                    some
                                                                                                                                    rural
                                                                                                                                    areas
                                                                                                                                    an
                                                                                                                                    extra
                                                                                                                                    3
                                                                                                                                    business
                                                                                                                                    days
                                                                                                                                    may
                                                                                                                                    be
                                                                                                                                    needed
                                                                                                                                    for
                                                                                                                                    delivery.<br><br>This
                                                                                                                                    product
                                                                                                                                    contains
                                                                                                                                    real
                                                                                                                                    fur
                                                                                                                                    from
                                                                                                                                    sheep
                                                                                                                                    or
                                                                                                                                    lamb
                                                                                                                                    originating
                                                                                                                                    in
                                                                                                                                    Australia,
                                                                                                                                    the
                                                                                                                                    European
                                                                                                                                    Union
                                                                                                                                    or
                                                                                                                                    the
                                                                                                                                    United
                                                                                                                                    States.
                                                                                                                                    The
                                                                                                                                    fur
                                                                                                                                    has
                                                                                                                                    been
                                                                                                                                    artificially
                                                                                                                                    dyed
                                                                                                                                    and
                                                                                                                                    treated.
                                                                                                                                    This
                                                                                                                                    product
                                                                                                                                    is
                                                                                                                                    made
                                                                                                                                    in
                                                                                                                                    China.
                                                                                                                                    RN#
                                                                                                                                    88276.<br><br>UGG.com<br><br>We
                                                                                                                                    only
                                                                                                                                    send
                                                                                                                                    emails
                                                                                                                                    to
                                                                                                                                    individuals
                                                                                                                                    who
                                                                                                                                    have
                                                                                                                                    registered
                                                                                                                                    at
                                                                                                                                    our
                                                                                                                                    site:
                                                                                                                                    <a style="text-decoration:underline;font-family:'Proxima Nova',Arial,sans-serif"
                                                                                                                                        href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/eaf5dbc7?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxZDA3ZmMxOWNiNzAwMDNmZTZjIiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvY2E_dXRtX3NvdXJjZT1VU19UcmFuc2FjdGlvbmFsJnV0bV9tZWRpdW09ZW1haWwmdXRtX2NhbXBhaWduPVVfVFhOTF9PUkRFUl9DT05GSVJNQVRJT05fRU4tQ0EmaG1haWw9ZGRhYjI4OTg0Y2JkMGY2MTE2N2U1ZTczYjc1YjY1ZTUyMWIwM2Q2YTc1Njg5Y2MxZjUxMzI4NDVhMDgxODY5OSZieGlkPTY1NzcxZTBlOGEwMWExMTcxMTAxNjNmOCJ9&amp;jwtS=q_C7vQIPwniObPdFr5GgrhnKuUkBjRSw1yma2dXpE-I"
                                                                                                                                        target="_blank"><span
                                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">www.ugg.com</span></a>.
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                        </tbody>
                                                                                                                    </table>
                                                                                                                </td>
                                                                                                                <td width="75"
                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                            <tr
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <td height="10"
                                                                                                    style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </div>
                                                                <table width="100%" cellpadding="0" cellspacing="0"
                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                    <tbody
                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                        <tr
                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                            <td align="center" valign="top"
                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                <table width="100%" cellpadding="0"
                                                                                    cellspacing="0" bgcolor="#ffffff"
                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                    <tbody
                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                        <tr
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <td height="10"
                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <td align="center" valign="top"
                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                <table width="600"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                    <tbody
                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                        <tr
                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            <td width="20"
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            </td>
                                                                                                            <td align="center"
                                                                                                                valign="top"
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                <table
                                                                                                                    width="100%"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                    <tbody
                                                                                                                        style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                        <tr
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <td align="center"
                                                                                                                                valign="top"
                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif;font-size:10px;line-height:15px;font-weight:400;color:rgb(0,0,1)">
                                                                                                                                <strong
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">1.888.432.8530</strong><br><a
                                                                                                                                    href="https://www.google.com/maps/search/250+Coromar+Drive,+Goleta,+CA+93117?entry=gmail&amp;source=g"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif">250
                                                                                                                                    Coromar
                                                                                                                                    Drive,
                                                                                                                                    Goleta,
                                                                                                                                    CA
                                                                                                                                    93117</a>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <td height="10"
                                                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr
                                                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                                            <td align="center"
                                                                                                                                valign="top"
                                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif;font-size:10px;line-height:15px;font-weight:400;color:rgb(0,0,1)">
                                                                                                                                <a href="https://e.emails.ugg.com/c2/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/5566740e?jwtH=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9&amp;jwtP=eyJpYXQiOjE3MDIzMDUzNDAsImNkIjoiLmVtYWlscy51Z2cuY29tIiwiY2UiOjg2NDAwLCJ0ayI6InVnZyIsIm10bElEIjoiNjU3NmMxZDA3ZmMxOWNiNzAwMDNmZTZkIiwibGlua1VybCI6Imh0dHBzOlwvXC93d3cudWdnLmNvbVwvY2FcL3ByaXZhY3ktcG9saWN5Lmh0bWw_dXRtX3NvdXJjZT1VU19UcmFuc2FjdGlvbmFsJnV0bV9tZWRpdW09ZW1haWwmdXRtX2NhbXBhaWduPVVfVFhOTF9PUkRFUl9DT05GSVJNQVRJT05fRU4tQ0EmaG1haWw9ZGRhYjI4OTg0Y2JkMGY2MTE2N2U1ZTczYjc1YjY1ZTUyMWIwM2Q2YTc1Njg5Y2MxZjUxMzI4NDVhMDgxODY5OSZieGlkPTY1NzcxZTBlOGEwMWExMTcxMTAxNjNmOCJ9&amp;jwtS=2F1Z4MtTQl_cdQM7p9B148W9x4jv6U6cI5rOmbD2W00"
                                                                                                                                    target="_blank"
                                                                                                                                    style="font-family:'Proxima Nova',Arial,sans-serif"><span
                                                                                                                                        style="text-decoration:underline;display:inline-block;font-family:'Proxima Nova',Arial,sans-serif;color:rgb(0,0,1)">Privacy
                                                                                                                                        Policy</span></a>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                            <td width="20"
                                                                                                                style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr
                                                                                            style="font-family:'Proxima Nova',Arial,sans-serif">
                                                                                            <td height="30"
                                                                                                style="line-height:1px;font-size:1px;font-family:'Proxima Nova',Arial,sans-serif">
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
                                        <tr>
                                            <td>
                                                <div
                                                    style="display:none;white-space:nowrap;font-style:normal;font-variant-caps:normal;font-weight:normal;font-stretch:normal;font-size:15px;font-family:courier;font-size-adjust:none;font-kerning:auto;font-variant-alternates:normal;font-variant-ligatures:normal;font-variant-numeric:normal;font-variant-east-asian:normal;font-feature-settings:normal;line-height:0">
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <img src="https://e.emails.ugg.com/o/p/1663:d46c7e394834ee577317d55ca43a3196:d231211:65771e0e8a01a117110163f8:1702305340427/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MDIzMDUzNDB9.wI9p_1eRwMo_PjrVF_yXAapxOyfB43oyZJpcG_XzXPw"
                    height="1" width="1">
                <img border="0" width="1" height="1" alt=""
                    src="http://track.sp.crdl.io/q/b_ZNAu7kujuya1fT5BEetw~~/AAAABAA~/RgRnWaM9PlcHY29yZGlhbEIKZXM9HndlRwuC4VIWdGFybG9uaWtpdGE5QGdtYWlsLmNvbVgEAAAAUw~~">
            </div>
        </div>
    </div>
    """

    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
