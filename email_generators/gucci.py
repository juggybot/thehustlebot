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
    msg['From'] = formataddr((f'Gucci', sender_email))
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
    "Please enter the item name (Gucci Bag):",
    "Please enter the item style (1234):",
    "Please enter the item colour (Black):",
    "Please enter the item size (US Small):",
    "Please enter the estimated delivery (05/25):",
    "Please enter the item price (WITHOUT THE $ SIGN):",
    "Please enter the customer name (Juggy Resells):",
    "Please enter the street address (123 Test Street):",
    "Please enter the city (Sydney):",
    "Please enter the country (Australia):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o primeiro nome do cliente (Juggy):",
    "Por favor, insira o nome do item (Bolsa Gucci):",
    "Por favor, insira o estilo do item (1234):",
    "Por favor, insira a cor do item (Preto):",
    "Por favor, insira o tamanho do item (US Pequeno):",
    "Por favor, insira a data estimada de entrega (25/05):",
    "Por favor, insira o preço do item (SEM O SÍMBOLO $):",
    "Por favor, insira o nome completo do cliente (Juggy Resells):",
    "Por favor, insira o endereço (123 Test Street):",
    "Por favor, insira a cidade (Sydney):",
    "Por favor, insira o país (Austrália):",
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
    part1 = random.randint(100000000, 999999999)  # Random 9-digit number

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
    subject = f"Thank you for your order {order_num}"

    html_template = f"""
            <div style="margin:0;padding:0;box-sizing:border-box">
        <div><br></div>
        <div>
            <div class="gmail_quote">
                <div
                    style="display:none;font-size:1px;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;font-family:sans-serif">
                    <span style="display:none;font-family:sans-serif">
                        <table cellpadding="0" cellspacing="0" width="100%" style="min-width:100%;font-family:sans-serif">
                            <tbody style="font-family:sans-serif">
                                <tr style="font-family:sans-serif">
                                    <td style="font-family:sans-serif"></td>
                                </tr>
                            </tbody>
                        </table>
                    </span>
                    <span style="display:none;font-family:sans-serif">
                        <table cellpadding="0" cellspacing="0" width="100%" style="min-width:100%;font-family:sans-serif">
                            <tbody style="font-family:sans-serif">
                                <tr style="font-family:sans-serif">
                                    <td style="font-family:sans-serif"><img
                                            src="https://pixel.app.returnpath.net/pixel.gif?r=4cb10d481f91db24e1a7c14cdf5cac9f28c237c9"
                                            width="1" height="1" style="font-family:sans-serif"></td>
                                </tr>
                            </tbody>
                        </table>
                    </span>
                </div>
                <table cellspacing="0" cellpadding="0" border="0" align="center" width="100%" style="width:100%">
                    <tbody>
                        <tr>
                            <td style="font-size:1px;line-height:1px" height="15"> </td>
                        </tr>
                        <tr>
                            <td align="center">
                                <table border="0" cellpadding="0" cellspacing="0" align="center" width="600"
                                    style="width:600px">
                                    <tbody>
                                        <tr>
                                            <td width="5"> </td>
                                            <td style="font-family:Arial,GucciFont,sans-serif;text-align:right"
                                                align="right" dir="ltr">
                                                <a style="font-family:Arial,GucciFont,sans-serif">Web version</a>
                                            </td>
                                            <td width="5"> </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td style="font-size:1px;line-height:1px" height="25"> </td>
                        </tr>
                        <tr>
                            <td style="width:100%" align="center" width="100%">
                                <table border="0" cellpadding="0" cellspacing="0" align="center" width="600"
                                    style="width:600px" bgcolor="#FFFFFF">
                                    <tbody>
                                        <tr>
                                            <td align="center">
                                                <table border="0" cellpadding="0" cellspacing="0" align="center"
                                                    width="100%" style="width:100%" bgcolor="#1B1B1B">
                                                    <tbody>
                                                        <tr>
                                                            <td style="font-size:1px;line-height:1px" height="27"> </td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-size:1px;line-height:1px" height="6"> </td>
                                                        </tr>
                                                        <tr>
                                                            <td align="center">
                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/1/zVT0vvxLgmnLN6sfpn4brg/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPTE0N2NhYWQzZDE2YmUyNjc1MzNjMDhiNjM4MzNmYmYzYmE1YTY2YTUyNDZmZWM0MzhlMmU4ZmYxZjA0NWJiMzIxNGEwNWMzMmI2ZjlkMmM5Y2EyYWU3YzgyZDQzZDBjZmVmMjdhYTcwYmMzZWYyNWMwYzdjY2MyODdkOWUwNjg1"
                                                                    target="_blank">
                                                                    <img style="display:inline"
                                                                        src="http://image.email.gucci.com/lib/fe3815707564047f701279/m/21/ef97f039-197d-4ac3-9963-198dcc0cb609.png"
                                                                        width="280" height="60" alt="Gucci">
                                                                    <div style="display:none">
                                                                        <img src="http://image.email.gucci.com/lib/fe3815707564047f701279/m/21/ef97f039-197d-4ac3-9963-198dcc0cb609.png"
                                                                            width="160" alt="Gucci">
                                                                    </div>
                                                                </a>
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td align="center">
                                                                <table cellpadding="0" cellspacing="0" width="100%"
                                                                    role="presentation" style="min-width:100%">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td>
                                                                                <table border="0" cellpadding="0"
                                                                                    cellspacing="0" align="center"
                                                                                    width="100%" style="width:100%">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td width="15"> </td>
                                                                                            <td width="570" align="center">
                                                                                                <table border="0"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    align="center">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td
                                                                                                                align="center">
                                                                                                                <table
                                                                                                                    border="0"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    align="center">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                                height="15">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td align="center"
                                                                                                                                style="font-family:Arial,GucciFont,sans-serif;font-size:12px;line-height:16px;font-weight:300;letter-spacing:1px;text-align:center">
                                                                                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/2/u7Ix57RaWOydep5EQ7GITA/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPTE0N2NhYWQzZDE2YmUyNjdkNTNjYzE5NjUwMDlmMGUzNGQ3NjhmMGExNWNhMmFjYTJmMmQ4YTdmYTBlMDM2NDJkZGM0NTgzMDMxMmQ4YzA5NzAwYWRmYTg5YmMxNWE4MjJhZWY2YWIxM2JmN2E0MDFlYWE4ZWJmYWIzY2MzN2Ew"
                                                                                                                                    style="text-decoration:none;font-weight:300;font-family:Arial,GucciFont,sans-serif;color:rgb(255,255,255)"
                                                                                                                                    target="_blank">WOMEN</a>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                                height="15">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                            <td
                                                                                                                style="padding:0px;width:20px">
                                                                                                            </td>
                                                                                                            <td
                                                                                                                align="center">
                                                                                                                <table
                                                                                                                    border="0"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    align="center">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                                height="15">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td align="center"
                                                                                                                                style="font-family:Arial,GucciFont,sans-serif;font-size:12px;line-height:16px;font-weight:300;letter-spacing:1px;text-align:center">
                                                                                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/3/qZ0iZwxEGq0Kt9Dh9n9xDA/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPTE0N2NhYWQzZDE2YmUyNjc4MmMzNDBjMGRlOTE1YjhkYTMxNGQ3MjE3MTQ1NzkzN2I0YWM1NmIxYjk1YTkwNWRhNDZkMWQ0MThjOGM3MjJiOWZjZDljNGU1MDg5ODI0MzM0ZDYyMGRkNThjZDA5ZTIyNWUwY2Q0NzljNTA0NjEx"
                                                                                                                                    style="text-decoration:none;font-family:Arial,GucciFont,sans-serif;color:rgb(255,255,255)"
                                                                                                                                    target="_blank">MEN</a>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                                height="15">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                            <td
                                                                                                                style="padding:0px;width:20px">
                                                                                                            </td>
                                                                                                            <td
                                                                                                                align="center">
                                                                                                                <table
                                                                                                                    border="0"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    align="center">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                                height="15">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td align="center"
                                                                                                                                style="font-family:Arial,GucciFont,sans-serif;font-size:12px;line-height:16px;font-weight:300;letter-spacing:1px;text-align:center">
                                                                                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/4/2O2zIEeqlCOnPO3aENOt-Q/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPTE0N2NhYWQzZDE2YmUyNjcwYTBhNzQ4YTdhYTZlN2JkMGQ4NTUwMDY0NTYyNzRjMGJlNWVmMjM1OWZhZGIxZTE0YmY5ZmRjYmI3NGNhODc3YjBlNWI3NzI2YmVlMmZlYmQ2NWE0ODljMDhmZDQ0YzA3ZTA5ZDNlYmJkYjA1M2Ri"
                                                                                                                                    style="text-decoration:none;font-family:Arial,GucciFont,sans-serif;color:rgb(255,255,255)"
                                                                                                                                    target="_blank">CHILDREN</a>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                                height="15">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                            <td
                                                                                                                style="padding:0px;width:20px">
                                                                                                            </td>
                                                                                                            <td
                                                                                                                align="center">
                                                                                                                <table
                                                                                                                    border="0"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    align="center">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                                height="15">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td align="center"
                                                                                                                                style="font-family:Arial,GucciFont,sans-serif;font-size:12px;line-height:16px;font-weight:300;letter-spacing:1px;text-align:center">
                                                                                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/5/oyq61w984-DiJS1Ykf6e7g/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPTE0N2NhYWQzZDE2YmUyNjdkMmQ4ZjBlYTM0ZjgzOWYzM2E3MjIxN2E1NDZmY2RjMTQ1NmFiZGI4ZTc2Nzg1OWE3ZmZlNWE3OGZmNDE5ZjNiMGMwMTJmNGQwMzEzYzU1MDA2OWQyYzlmM2MxN2E4MWE4ZTIwMjdmNmY3NjdlN2E5"
                                                                                                                                    style="text-decoration:none;font-family:Arial,GucciFont,sans-serif;color:rgb(255,255,255)"
                                                                                                                                    target="_blank">GIFTS</a>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                                height="15">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                            <td
                                                                                                                style="padding:0px;width:20px">
                                                                                                            </td>
                                                                                                            <td
                                                                                                                align="center">
                                                                                                                <table
                                                                                                                    border="0"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    align="center">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                                height="15">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td align="center"
                                                                                                                                style="font-family:Arial,GucciFont,sans-serif;font-size:12px;line-height:16px;font-weight:300;letter-spacing:1px;text-align:center">
                                                                                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/6/8QCDuBnN4kUI9CjFzMTZxQ/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPTE0N2NhYWQzZDE2YmUyNjdlMTg2ZTgxNDFiM2Y5NzFjZTVlYWY3Zjc4NjA2OTdiODVkOGQ5YjFmYTM5MWNhMjk2Mjk1MDhiYzdkYjUxOWE5NmZmMTE2NjlmMjA4M2FhODRiZjdkYzAzYTIyMjliZjBhODk3Y2Y4NDZhODU0MWZl"
                                                                                                                                    style="text-decoration:none;font-family:Arial,GucciFont,sans-serif;color:rgb(255,255,255)"
                                                                                                                                    target="_blank">STORIES</a>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                                height="15">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </td>
                                                                                            <td width="15"> </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td colspan="3"
                                                                                                style="font-size:1px;line-height:1px"
                                                                                                height="25"> </td>
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
                                                            <td style="font-size:1px;line-height:1px" height="10"> </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center">
                                                <table border="0" cellpadding="0" cellspacing="0" align="center"
                                                    width="100%" style="width:100%">
                                                    <tbody>
                                                        <tr>
                                                            <td width="40"> </td>
                                                            <td align="center">
                                                                <table border="0" cellpadding="0" cellspacing="0"
                                                                    align="center">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="45"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:16px;line-height:24px;font-weight:300;text-align:center;letter-spacing:1px;color:rgb(27,27,27)"
                                                                                align="center" dir="ltr">
                                                                                Dear {user_inputs[0]},
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="8"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:16px;line-height:24px;font-weight:300;text-align:center;letter-spacing:1px;color:rgb(27,27,27)"
                                                                                align="center" dir="ltr">
                                                                                We&#39;ve received your order and it&#39;s
                                                                                currently being processed.
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="20"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:12px;line-height:24px;letter-spacing:1px;text-align:center;color:rgb(153,153,153)"
                                                                                align="center" dir="ltr">
                                                                                ORDER NUMBER
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:20px;line-height:24px;font-weight:300;text-align:center;letter-spacing:1px;color:rgb(27,27,27)"
                                                                                align="center" dir="ltr">
                                                                                {order_num}
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="20"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:16px;line-height:24px;font-weight:300;text-align:center;letter-spacing:1px;color:rgb(27,27,27)"
                                                                                align="center" dir="ltr">
                                                                                Thank you for your purchase, we hope you
                                                                                enjoyed your experience shopping with us and
                                                                                look forward to assisting you again
                                                                                soon.<br><br>Once your order has shipped, we
                                                                                will send you a separate confirmation email
                                                                                so you can track its journey from our
                                                                                fulfillment center to your door.<br><br>In
                                                                                the meantime, we invite you to <a
                                                                                    style="text-decoration:underline;font-family:Arial,GucciFont,sans-serif;color:rgb(0,0,0)"
                                                                                    href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/7/tUySzZ3j-tcodMINDaIZfQ/aHR0cHM6Ly93d3cuZ3VjY2kuY29tL3VrL2VuX2diL3N0L3doYXQtbmV3P3V0bV9zb3VyY2U9bmRfVUtfTV9uZF9uZF9uZCZnY2k9TWpFME1ETTVPVGt3TURneE1ERTROemN4TVE9PSZ1dG1fbWVkaXVtPWVtYWlsX1NFVCZ1dG1fY2FtcGFpZ249VEVNX29yZGVyX2NvbmZpcm1hdGlvbiZ1dG1fY29udGVudD1jdGE"
                                                                                    target="_blank">explore our latest
                                                                                    collections online.</a>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="20"> </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </td>
                                                            <td width="40"> </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center">
                                                <table border="0" cellpadding="0" cellspacing="0" align="center"
                                                    width="100%" style="width:100%">
                                                    <tbody>
                                                        <tr>
                                                            <td width="40"> </td>
                                                            <td align="center">
                                                                <table border="0" cellpadding="0" cellspacing="0"
                                                                    align="center" width="100%" style="width:100%">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="45"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px;background:0% repeat rgb(0,0,0)"
                                                                                height="1"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="45"> </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </td>
                                                            <td width="40"> </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center">
                                                <table border="0" cellpadding="0" cellspacing="0" align="center"
                                                    width="100%" style="width:100%">
                                                    <tbody>
                                                        <tr>
                                                            <td width="40"> </td>
                                                            <td align="center">
                                                                <table border="0" cellpadding="0" cellspacing="0"
                                                                    align="center" width="520" style="margin:auto">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td style="padding:0px;vertical-align:top"
                                                                                align="center">
                                                                                <table align="center" border="0"
                                                                                    cellpadding="0" cellspacing="0"
                                                                                    style="max-width:520px" width="100%">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td
                                                                                                style="font-size:0px;text-align:center;vertical-align:top">
                                                                                                <div
                                                                                                    style="display:inline-block;vertical-align:top">
                                                                                                    <table align="left"
                                                                                                        border="0"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        width="180">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td
                                                                                                                    align="center">
                                                                                                                    <table
                                                                                                                        border="0"
                                                                                                                        cellpadding="0"
                                                                                                                        cellspacing="0"
                                                                                                                        width="100%"
                                                                                                                        align="left">
                                                                                                                        <tbody>
                                                                                                                            <tr>
                                                                                                                                <td style="font-size:0px;text-align:left"
                                                                                                                                    align="center">
                                                                                                                                    <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/8/21JrQLF7kWH4KdCKtmstMA/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPTE0N2NhYWQzZDE2YmUyNjcwNjE4ZTVkN2UzNmU3ZDQ0ZGRhYTFhYzFhZTcwYzg5ZDg2OGI0NTI0MzhmNWI2YTNkYWM3Y2E5NWY4MmU3ODA2YjI5ZjVkNWU3MWM1YzEzMjNmOGMyMzVkMjQwN2JkNzEzMGRlZGFhMGJjM2Q1ZmNi"
                                                                                                                                        target="_blank">
                                                                                                                                        <img src="https://imageurl.com"
                                                                                                                                            style="display:inline-block;width:160px"
                                                                                                                                            alt="OPHIDIA GG SMALL HANDBAG"
                                                                                                                                            border="0"
                                                                                                                                            width="160">
                                                                                                                                    </a>
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="font-size:1px;line-height:1px"
                                                                                                                                    height="20">
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="font-size:1px;line-height:1px;display:none"
                                                                                                                                    height="15">
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
                                                                                                    style="display:inline-block;vertical-align:top">
                                                                                                    <table align="left"
                                                                                                        border="0"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        width="180">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td
                                                                                                                    align="center">
                                                                                                                    <table
                                                                                                                        border="0"
                                                                                                                        cellpadding="0"
                                                                                                                        cellspacing="0"
                                                                                                                        width="100%"
                                                                                                                        align="left">
                                                                                                                        <tbody>
                                                                                                                            <tr>
                                                                                                                                <td style="font-family:Arial,GucciFont,sans-serif;font-size:26px;line-height:30px;font-weight:300;text-align:left;letter-spacing:1px;color:rgb(27,27,27)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">
                                                                                                                                    {user_inputs[1]}
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="font-size:1px;line-height:1px"
                                                                                                                                    height="15">
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="font-family:Arial,GucciFont,sans-serif;font-size:12px;line-height:20px;text-align:left;color:rgb(173,173,173)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">
                                                                                                                                    <span
                                                                                                                                        style="font-family:Arial,GucciFont,sans-serif">
                                                                                                                                        Style:
                                                                                                                                        {user_inputs[2]}<br>Color:
                                                                                                                                        <span
                                                                                                                                            style="font-family:Arial,GucciFont,sans-serif">{user_inputs[3]}</span>
                                                                                                                                        <br>Size:
                                                                                                                                        {user_inputs[4]}
                                                                                                                                    </span>
                                                                                                                                    <span
                                                                                                                                        style="display:none;font-size:14px;text-align:center;font-family:Arial,GucciFont,sans-serif;line-height:18px!important;color:rgb(173,173,173)">
                                                                                                                                        Style:
                                                                                                                                        000000<br>Color:
                                                                                                                                        <span
                                                                                                                                            style="font-family:Arial,GucciFont,sans-serif">COLOR</span>
                                                                                                                                        <br>Size:
                                                                                                                                        SIZE
                                                                                                                                        |
                                                                                                                                        Qty:
                                                                                                                                        1
                                                                                                                                    </span>
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="font-size:1px;line-height:1px"
                                                                                                                                    height="15">
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="font-family:Arial,GucciFont,sans-serif;font-size:12px;line-height:20px;text-align:left;color:rgb(27,27,27)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">
                                                                                                                                    ESTIMATED
                                                                                                                                    DELIVERY
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="font-family:Arial,GucciFont,sans-serif;font-size:13px;line-height:18px;text-align:left;color:rgb(173,173,173)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">
                                                                                                                                    Estimated
                                                                                                                                    delivery
                                                                                                                                    on
                                                                                                                                    {user_inputs[5]}<br>
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="font-size:1px;line-height:1px"
                                                                                                                                    height="15">
                                                                                                                                </td>
                                                                                                                        </tbody>
                                                                                                                    </table>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                                <div
                                                                                                    style="display:inline-block;vertical-align:top">
                                                                                                    <table align="left"
                                                                                                        border="0"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        width="160">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td
                                                                                                                    align="center">
                                                                                                                    <table
                                                                                                                        border="0"
                                                                                                                        cellpadding="0"
                                                                                                                        cellspacing="0"
                                                                                                                        width="100%"
                                                                                                                        align="left">
                                                                                                                        <tbody>
                                                                                                                            <tr>
                                                                                                                                <td style="font-size:1px;line-height:1px;display:none"
                                                                                                                                    height="15">
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="font-family:Arial,GucciFont,sans-serif;font-size:22px;line-height:30px;font-weight:300;text-align:right;color:rgb(27,27,27)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">
                                                                                                                                    {user_inputs[11]}{user_inputs[6]}
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="font-family:Arial,GucciFont,sans-serif;font-size:12px;line-height:20px;font-weight:300;text-align:right;color:rgb(153,153,153)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">
                                                                                                                                    Qty:
                                                                                                                                    1
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="font-size:1px;line-height:1px"
                                                                                                                                    height="25">
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
                                                            <td width="40"> </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center">
                                                <table border="0" cellpadding="0" cellspacing="0" align="center"
                                                    width="100%" style="width:100%">
                                                    <tbody>
                                                        <tr>
                                                            <td width="40"> </td>
                                                            <td align="center">
                                                                <table border="0" cellpadding="0" cellspacing="0"
                                                                    align="center" width="100%" style="width:100%">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px;background:0% repeat rgb(234,233,233)"
                                                                                height="1"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="25"> </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </td>
                                                            <td width="40"> </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center">
                                                <table border="0" cellpadding="0" cellspacing="0" align="center"
                                                    width="100%" style="width:100%">
                                                    <tbody>
                                                        <tr>
                                                            <td width="40"> </td>
                                                            <td align="center">
                                                                <table border="0" cellpadding="0" cellspacing="0"
                                                                    align="center" width="520" style="margin:auto">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td style="padding:0px;vertical-align:top"
                                                                                align="center">
                                                                                <table align="center" border="0"
                                                                                    cellpadding="0" cellspacing="0"
                                                                                    style="max-width:520px" width="100%">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td
                                                                                                style="font-size:0px;text-align:center;vertical-align:top">
                                                                                                <div
                                                                                                    style="display:inline-block;vertical-align:top">
                                                                                                    <table align="left"
                                                                                                        border="0"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        width="180">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td style="font-size:1px;line-height:1px"
                                                                                                                    align="center">
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                                <div
                                                                                                    style="display:inline-block;vertical-align:top">
                                                                                                    <table align="left"
                                                                                                        border="0"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        width="340">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td
                                                                                                                    align="center">
                                                                                                                    <table
                                                                                                                        border="0"
                                                                                                                        cellpadding="0"
                                                                                                                        cellspacing="0"
                                                                                                                        width="100%"
                                                                                                                        align="center">
                                                                                                                        <tbody>
                                                                                                                            <tr>
                                                                                                                                <td width="200"
                                                                                                                                    style="font-size:1px;line-height:1px;display:none"
                                                                                                                                    height="15">
                                                                                                                                </td>
                                                                                                                                <td width="140"
                                                                                                                                    style="font-size:1px;line-height:1px;display:none"
                                                                                                                                    height="15">
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td width="200"
                                                                                                                                    style="font-family:Arial,GucciFont,sans-serif;font-size:12px;line-height:20px;text-align:left;color:rgb(124,124,124)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">
                                                                                                                                    Subtotal
                                                                                                                                </td>
                                                                                                                                <td width="140"
                                                                                                                                    style="font-family:Arial,GucciFont,sans-serif;font-size:12px;line-height:20px;text-align:right;color:rgb(124,124,124)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">
                                                                                                                                    {user_inputs[11]}{user_inputs[6]}
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td width="200"
                                                                                                                                    style="font-family:Arial,GucciFont,sans-serif;font-size:12px;line-height:20px;text-align:left;color:rgb(124,124,124)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">
                                                                                                                                    Shipping
                                                                                                                                    -
                                                                                                                                    DHL-Express
                                                                                                                                </td>
                                                                                                                                <td width="140"
                                                                                                                                    style="font-family:Arial,GucciFont,sans-serif;font-size:12px;line-height:20px;text-align:right;color:rgb(124,124,124)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">
                                                                                                                                    Free
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td colspan="2"
                                                                                                                                    style="font-size:1px;line-height:1px"
                                                                                                                                    height="15">
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td width="200"
                                                                                                                                    style="font-family:Arial,GucciFont,sans-serif;font-size:22px;line-height:30px;font-weight:300;text-align:left;color:rgb(27,27,27)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">
                                                                                                                                    Total
                                                                                                                                </td>
                                                                                                                                <td width="140"
                                                                                                                                    style="font-family:Arial,GucciFont,sans-serif;font-size:22px;line-height:30px;font-weight:300;text-align:right;color:rgb(27,27,27)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">
                                                                                                                                    {user_inputs[11]}{user_inputs[6]}
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td width="200"
                                                                                                                                    style="font-family:Arial,GucciFont,sans-serif;font-size:12px;line-height:20px;text-align:left;color:rgb(124,124,124)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">

                                                                                                                                </td>
                                                                                                                                <td width="140"
                                                                                                                                    style="font-family:Arial,GucciFont,sans-serif;font-size:12px;line-height:20px;text-align:right;color:rgb(124,124,124)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">

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
                                                            <td width="40"> </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center">
                                                <table border="0" cellpadding="0" cellspacing="0" align="center"
                                                    width="100%" style="width:100%">
                                                    <tbody>
                                                        <tr>
                                                            <td width="40"> </td>
                                                            <td align="center">
                                                                <table border="0" cellpadding="0" cellspacing="0"
                                                                    align="center" width="100%" style="width:100%">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="45"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px;background:0% repeat rgb(0,0,0)"
                                                                                height="1"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="45"> </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </td>
                                                            <td width="40"> </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center">
                                                <table border="0" cellpadding="0" cellspacing="0" align="center"
                                                    width="100%" style="width:100%">
                                                    <tbody>
                                                        <tr>
                                                            <td width="40"> </td>
                                                            <td align="center">
                                                                <table border="0" cellpadding="0" cellspacing="0"
                                                                    align="center" width="520" style="margin:auto">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td style="padding:0px;vertical-align:top"
                                                                                align="center">
                                                                                <table align="center" border="0"
                                                                                    cellpadding="0" cellspacing="0"
                                                                                    style="max-width:520px" width="100%">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td style="font-size:0px;text-align:center;vertical-align:top"
                                                                                                dir="ltr">
                                                                                                <div
                                                                                                    style="display:inline-block;vertical-align:top">
                                                                                                    <table align="left"
                                                                                                        border="0"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        width="260">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td
                                                                                                                    align="center">
                                                                                                                    <table
                                                                                                                        border="0"
                                                                                                                        cellpadding="0"
                                                                                                                        cellspacing="0"
                                                                                                                        width="100%"
                                                                                                                        align="center">
                                                                                                                        <tbody>
                                                                                                                            <tr>
                                                                                                                                <td style="font-family:Arial,GucciFont,sans-serif;font-size:26px;line-height:35px;font-weight:300;text-align:left;letter-spacing:1px;color:rgb(27,27,27)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">
                                                                                                                                    SHIPPING
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="font-family:Arial,GucciFont,sans-serif;font-size:11px;line-height:16px;letter-spacing:1px;text-align:left;color:rgb(153,153,153)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">
                                                                                                                                    DHL-Express<br>
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="font-size:1px;line-height:1px"
                                                                                                                                    height="20">
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
                                                                                                    style="display:inline-block;vertical-align:top">
                                                                                                    <table align="left"
                                                                                                        border="0"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        width="260">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td
                                                                                                                    align="center">
                                                                                                                    <table
                                                                                                                        border="0"
                                                                                                                        cellpadding="0"
                                                                                                                        cellspacing="0"
                                                                                                                        width="100%"
                                                                                                                        align="center">
                                                                                                                        <tbody>
                                                                                                                            <tr>
                                                                                                                                <td style="font-family:Arial,GucciFont,sans-serif;font-size:14px;line-height:20px;font-weight:300;text-align:right;letter-spacing:1px;color:rgb(27,27,27)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">
                                                                                                                                    {user_inputs[7]}<br>{user_inputs[8]}<br>{user_inputs[9]}<br>{user_inputs[10]}<br>
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
                                                            <td width="40"> </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center">
                                                <table border="0" cellpadding="0" cellspacing="0" align="center"
                                                    width="100%" style="width:100%">
                                                    <tbody>
                                                        <tr>
                                                            <td width="40"> </td>
                                                            <td align="center">
                                                                <table border="0" cellpadding="0" cellspacing="0"
                                                                    align="center" width="100%" style="width:100%">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="45"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px;background:0% repeat rgb(234,233,233)"
                                                                                height="1"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="45"> </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </td>
                                                            <td width="40"> </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center">
                                                <table border="0" cellpadding="0" cellspacing="0" align="center"
                                                    width="100%" style="width:100%">
                                                    <tbody>
                                                        <tr>
                                                            <td width="40"> </td>
                                                            <td align="center">
                                                                <table border="0" cellpadding="0" cellspacing="0"
                                                                    align="center" width="520" style="margin:auto">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td style="padding:0px;vertical-align:top"
                                                                                align="center" dir="ltr">
                                                                                <table align="center" border="0"
                                                                                    cellpadding="0" cellspacing="0"
                                                                                    style="max-width:520px" width="100%">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td
                                                                                                style="font-size:0px;text-align:center;vertical-align:top">
                                                                                                <div
                                                                                                    style="display:inline-block;vertical-align:top">
                                                                                                    <table align="left"
                                                                                                        border="0"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        width="260">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td
                                                                                                                    align="center">
                                                                                                                    <table
                                                                                                                        border="0"
                                                                                                                        cellpadding="0"
                                                                                                                        cellspacing="0"
                                                                                                                        width="100%"
                                                                                                                        align="center">
                                                                                                                        <tbody>
                                                                                                                            <tr>
                                                                                                                                <td style="font-family:Arial,GucciFont,sans-serif;font-size:26px;line-height:35px;font-weight:300;letter-spacing:1px;text-align:left;color:rgb(27,27,27)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">
                                                                                                                                    PACKAGING
                                                                                                                                    &amp;
                                                                                                                                    GIFTING
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="font-family:Arial,GucciFont,sans-serif;font-size:11px;line-height:16px;letter-spacing:1px;font-weight:300;text-align:left;color:rgb(27,27,27)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">
                                                                                                                                    We
                                                                                                                                    will
                                                                                                                                    do
                                                                                                                                    our
                                                                                                                                    best
                                                                                                                                    to
                                                                                                                                    meet
                                                                                                                                    your
                                                                                                                                    packaging
                                                                                                                                    preference.
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
                                                                                                    style="display:inline-block;vertical-align:top">
                                                                                                    <table align="left"
                                                                                                        border="0"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        width="260">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td
                                                                                                                    align="center">
                                                                                                                    <table
                                                                                                                        border="0"
                                                                                                                        cellpadding="0"
                                                                                                                        cellspacing="0"
                                                                                                                        width="100%"
                                                                                                                        align="center">
                                                                                                                        <tbody>
                                                                                                                            <tr>
                                                                                                                                <td style="font-size:1px;line-height:1px"
                                                                                                                                    height="20">
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="font-size:0px;text-align:right"
                                                                                                                                    align="center">
                                                                                                                                    <img style="display:inline-block;width:150px"
                                                                                                                                        border="0"
                                                                                                                                        width="150">
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
                                                            <td width="40"> </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center">
                                                <table border="0" cellpadding="0" cellspacing="0" align="center"
                                                    width="100%" style="width:100%">
                                                    <tbody>
                                                        <tr>
                                                            <td width="40"> </td>
                                                            <td align="center">
                                                                <table border="0" cellpadding="0" cellspacing="0"
                                                                    align="center" width="100%" style="width:100%">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="45"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px;background:0% repeat rgb(234,233,233)"
                                                                                height="1"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="45"> </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </td>
                                                            <td width="40"> </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center">
                                                <table border="0" cellpadding="0" cellspacing="0" align="center"
                                                    width="100%" style="width:100%">
                                                    <tbody>
                                                        <tr>
                                                            <td width="40"> </td>
                                                            <td align="center">
                                                                <table border="0" cellpadding="0" cellspacing="0"
                                                                    align="center" width="520" style="margin:auto">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td style="padding:0px;vertical-align:top"
                                                                                align="center">
                                                                                <table align="center" border="0"
                                                                                    cellpadding="0" cellspacing="0"
                                                                                    style="max-width:520px" width="100%">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td style="font-size:0px;text-align:center;vertical-align:top"
                                                                                                dir="ltr">
                                                                                                <div
                                                                                                    style="display:inline-block;vertical-align:top">
                                                                                                    <table align="left"
                                                                                                        border="0"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        width="260">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td
                                                                                                                    align="center">
                                                                                                                    <table
                                                                                                                        border="0"
                                                                                                                        cellpadding="0"
                                                                                                                        cellspacing="0"
                                                                                                                        width="100%"
                                                                                                                        align="center">
                                                                                                                        <tbody>
                                                                                                                            <tr>
                                                                                                                                <td style="font-family:Arial,GucciFont,sans-serif;font-size:26px;line-height:35px;font-weight:300;text-align:left;letter-spacing:1px;color:rgb(27,27,27)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">
                                                                                                                                    PAYMENT
                                                                                                                                    &amp;
                                                                                                                                    BILLING
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="font-family:Arial,GucciFont,sans-serif;font-size:11px;line-height:16px;letter-spacing:1px;text-align:left;color:rgb(153,153,153)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">
                                                                                                                                    You
                                                                                                                                    will
                                                                                                                                    be
                                                                                                                                    charged
                                                                                                                                    at
                                                                                                                                    the
                                                                                                                                    time
                                                                                                                                    of
                                                                                                                                    shipment
                                                                                                                                    with
                                                                                                                                    the
                                                                                                                                    following
                                                                                                                                    exceptions:<br>Made
                                                                                                                                    to
                                                                                                                                    Order,
                                                                                                                                    personalised
                                                                                                                                    items
                                                                                                                                    and
                                                                                                                                    cash
                                                                                                                                    in
                                                                                                                                    store
                                                                                                                                    -
                                                                                                                                    You
                                                                                                                                    will
                                                                                                                                    be
                                                                                                                                    charged
                                                                                                                                    at
                                                                                                                                    time
                                                                                                                                    of
                                                                                                                                    purchase
                                                                                                                                    <br>Wire
                                                                                                                                    transfer
                                                                                                                                    -
                                                                                                                                    Your
                                                                                                                                    order
                                                                                                                                    will
                                                                                                                                    be
                                                                                                                                    prepared
                                                                                                                                    for
                                                                                                                                    shipment
                                                                                                                                    after
                                                                                                                                    we
                                                                                                                                    have
                                                                                                                                    processed
                                                                                                                                    your
                                                                                                                                    payment
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                            <tr>
                                                                                                                                <td style="font-size:1px;line-height:1px"
                                                                                                                                    height="15">
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
                                                                                                    style="display:inline-block;vertical-align:top">
                                                                                                    <table align="left"
                                                                                                        border="0"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        width="260">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td
                                                                                                                    align="center">
                                                                                                                    <table
                                                                                                                        border="0"
                                                                                                                        cellpadding="0"
                                                                                                                        cellspacing="0"
                                                                                                                        width="100%"
                                                                                                                        align="center">
                                                                                                                        <tbody>
                                                                                                                            <tr>
                                                                                                                                <td style="font-family:Arial,GucciFont,sans-serif;font-size:14px;line-height:20px;font-weight:300;text-align:right;letter-spacing:1px;color:rgb(27,27,27)"
                                                                                                                                    align="center"
                                                                                                                                    dir="ltr">
                                                                                                                                    MasterCard
                                                                                                                                    ************4800<br><br>
                                                                                                                                    {user_inputs[7]}<br>{user_inputs[8]}<br>{user_inputs[9]}<br>{user_inputs[10]}<br><a
                                                                                                                                        href="tel:%%=v(@billToPhone)=%%"
                                                                                                                                        style="font-family:Arial,GucciFont,sans-serif;text-decoration:none!important;color:rgb(0,0,0)"
                                                                                                                                        target="_blank"></a>
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
                                                            <td width="40"> </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center">
                                                <table border="0" cellpadding="0" cellspacing="0" align="center"
                                                    width="100%" style="width:100%">
                                                    <tbody>
                                                        <tr>
                                                            <td width="40"> </td>
                                                            <td align="center">
                                                                <table border="0" cellpadding="0" cellspacing="0"
                                                                    align="center" width="100%" style="width:100%">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="45"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px;background:0% repeat rgb(234,233,233)"
                                                                                height="1"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="45"> </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </td>
                                                            <td width="40"> </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center">
                                                <table border="0" cellpadding="0" cellspacing="0" align="center"
                                                    width="100%" style="width:100%">
                                                    <tbody>
                                                        <tr>
                                                            <td width="40"> </td>
                                                            <td align="center">
                                                                <table border="0" cellpadding="0" cellspacing="0"
                                                                    align="center" width="100%" style="width:100%">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td width="520" style="width:520px">
                                                                                <table border="0" cellspacing="0"
                                                                                    cellpadding="0" width="520">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td valign="top" width="520"
                                                                                                style="width:520px;text-align:left;font-family:Arial,GucciFont,sans-serif;font-size:26px;line-height:35px;font-weight:300;letter-spacing:1px;color:rgb(27,27,27)"
                                                                                                align="left">
                                                                                                ORDER TRACKING MADE EASY
                                                                                            </td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                            <td>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td width="520" height="25px"
                                                                                style="height:25px;width:520px"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td width="520"
                                                                                style="width:520px;text-align:left;font-family:Arial,GucciFont,sans-serif;font-size:14px;line-height:20px;font-weight:300;letter-spacing:1px;color:rgb(27,27,27)"
                                                                                align="left">
                                                                                Scan the QR code and register or sign in to
                                                                                your MY GUCCI account to keep track of your
                                                                                orders and returns with the Gucci App.
                                                                            </td>
                                                                            <td>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td width="520" height="25px"
                                                                                style="height:25px;width:520px"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td width="520"
                                                                                style="width:520px;text-align:center"
                                                                                align="center"><img
                                                                                    style="width:140px;height:140px;margin:auto"
                                                                                    alt="Gucci App Download" border="0"
                                                                                    width="140" height="140"></td>
                                                                            <td>
                                                                            </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                                <div style="display:none">
                                                                    <table border="0" cellpadding="0" cellspacing="0"
                                                                        align="center" width="100%" style="width:100%">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td width="10%" style="width:10%"> </td>
                                                                                <td width="80%"
                                                                                    style="width:80%;text-align:center;font-family:Arial,GucciFont,sans-serif;font-size:26px;line-height:35px;font-weight:300;letter-spacing:1px;color:rgb(27,27,27)"
                                                                                    align="center">ORDER TRACKING MADE EASY
                                                                                </td>
                                                                                <td>
                                                                                </td>
                                                                                <td width="10%" style="width:10%"> </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td width="10%" height="25px"
                                                                                    style="width:10%;height:25px"> </td>
                                                                                <td width="10%" height="25px"
                                                                                    style="width:10%;height:25px"> </td>
                                                                                <td width="10%" height="25px"
                                                                                    style="width:10%;height:25px"> </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td width="10%" style="width:10%"> </td>
                                                                                <td width="80%"
                                                                                    style="width:80%;font-family:Arial,GucciFont,sans-serif;font-size:14px;line-height:20px;font-weight:300;text-align:center;letter-spacing:1px;color:rgb(27,27,27)"
                                                                                    align="left">Tap and register or sign in
                                                                                    to your MY GUCCI account to keep track
                                                                                    of your orders and returns with the
                                                                                    Gucci App.</td>
                                                                                <td>
                                                                                </td>
                                                                                <td width="10%" style="width:10%"> </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td width="10%" height="50px"
                                                                                    style="width:10%;height:50px"> </td>
                                                                                <td width="10%" height="50px"
                                                                                    style="width:10%;height:50px"> </td>
                                                                                <td width="10%" height="50px"
                                                                                    style="width:10%;height:50px"> </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td width="10%" style="width:10%"> </td>
                                                                                <td width="80%"
                                                                                    style="width:80%;font-family:Arial,GucciFont,sans-serif;font-size:14px;line-height:24px;font-weight:300;text-align:center;letter-spacing:1px;color:rgb(0,0,0)"
                                                                                    align="center">
                                                                                    <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/9/M0N7k_m5Nv0cka3zVq3g8Q/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPWMzMDczMDU1MmY3ZjM3NjU2Y2NiYTBiYzcxMTY0NjQ5MzlmNDVlZDVkMmE0ZTY1MzE4ZjE3MDRiNTk1YmEzYWZmZDIzODQzMjhhODgzNWU2NjE2MTE0MjlkYzdlMmVlNzVhMmJlZTQwYjAwMTQ1NzQ5NDM1YzM2MzEwZjM3MTY0"
                                                                                        style="font-family:Arial,GucciFont,sans-serif"
                                                                                        target="_blank">
                                                                                        <img src="https://image.email.gucci.com/lib/fe3815707564047f701279/m/9/712ab88f-5c4b-43af-b88b-ece138a0d90d.png"
                                                                                            style="display:inline-block;width:60px;height:60px;border-radius:15px;border:1px solid rgb(27,27,27);font-family:Arial,GucciFont,sans-serif"
                                                                                            border="0" width="60"
                                                                                            alt="Gucci App">
                                                                                    </a>
                                                                                </td>
                                                                                <td>
                                                                                </td>
                                                                                <td width="10%" style="width:10%"> </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </div>
                                                            </td>
                                                            <td width="40"> </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center">
                                                <table border="0" cellpadding="0" cellspacing="0" align="center"
                                                    width="100%" style="width:100%">
                                                    <tbody>
                                                        <tr>
                                                            <td width="40"> </td>
                                                            <td align="center">
                                                                <table border="0" cellpadding="0" cellspacing="0"
                                                                    align="center" width="100%" style="width:100%">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="45"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px;background:0% repeat rgb(234,233,233)"
                                                                                height="1"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="45"> </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </td>
                                                            <td width="40"> </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center">
                                                <table border="0" cellpadding="0" cellspacing="0" align="center"
                                                    width="100%" style="width:100%">
                                                    <tbody>
                                                        <tr>
                                                            <td width="40"> </td>
                                                            <td align="center">
                                                                <table border="0" cellpadding="0" cellspacing="0"
                                                                    align="center">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:14px;line-height:20px;font-weight:300;text-align:center;letter-spacing:1px;color:rgb(75,75,75)"
                                                                                align="center">
                                                                                Items are subject to availability. If we are
                                                                                unable to fulfill your order, our Client
                                                                                Advisors will notify you as soon as possible
                                                                                and are available to assist you with
                                                                                alternative options you may like. Please
                                                                                note, Gucci online purchases will require an
                                                                                adult signature upon delivery. <a
                                                                                    href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/10/3Ba5Lw23KLel87M8vPe6OQ/aHR0cHM6Ly93d3cuZ3VjY2kuY29tL2RvY3VtZW50cy90Yy8yMDIxMDUxMy9UZXJtc0FuZENvbmRpdGlvbnNfZW5fVUsuMjAyMTA1MTMucGRmP3V0bV9zb3VyY2U9bmRfVUtfTV9uZF9uZF9uZCZnY2k9TWpFME1ETTVPVGt3TURneE1ERTROemN4TVE9PSZ1dG1fbWVkaXVtPWVtYWlsX1NFVCZ1dG1fY2FtcGFpZ249VEVNX29yZGVyX2NvbmZpcm1hdGlvbiZ1dG1fY29udGVudD1nZHBy"
                                                                                    style="font-family:Arial,GucciFont,sans-serif;text-decoration:none!important;color:rgb(0,0,0)"
                                                                                    target="_blank">Terms and Conditions of
                                                                                    sale</a>.
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="20"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:14px;line-height:20px;font-weight:300;text-align:center;letter-spacing:1px;color:rgb(75,75,75)"
                                                                                align="center" dir="ltr">
                                                                                NEED TO RETURN AN ITEM?<br>
                                                                                If you would like to return an item, notify
                                                                                us within 14 days from the date of delivery.
                                                                                You will then have 14 days from the
                                                                                notification date to return your order.
                                                                                Items must remain in their original
                                                                                condition with all labels attached and
                                                                                intact. Please note, Made to Order and
                                                                                personalized items are final sale.
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="20"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:14px;line-height:20px;font-weight:300;text-align:center;letter-spacing:1px;color:rgb(75,75,75)"
                                                                                align="center" dir="ltr">
                                                                                OUR GUARANTEE<br>
                                                                                At Gucci, we take pride in the craftsmanship
                                                                                and quality of our products. If an item does
                                                                                not meet these standards, please let us
                                                                                know. We will do our best to rectify the
                                                                                situation with a repair or exchange, free of
                                                                                charge.
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="20"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:14px;line-height:20px;font-weight:300;text-align:center;letter-spacing:1px;color:rgb(75,75,75)"
                                                                                align="center" dir="ltr">
                                                                                THIRD-PARTY RESOLUTION<br>
                                                                                If you are still having issues with your
                                                                                order, you may request a third-party
                                                                                resolution at <a
                                                                                    href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/11/yhkomg-WJ8rJWX3eY38V5g/aHR0cDovL2VjLmV1cm9wYS5ldS9vZHI"
                                                                                    style="font-family:Arial,GucciFont,sans-serif;text-decoration:none!important;color:rgb(0,0,0)"
                                                                                    target="_blank">http://ec.europa.eu/odr.</a>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-size:1px;line-height:1px"
                                                                                height="45"> </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </td>
                                                            <td width="40"> </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center">
                                                <table cellpadding="0" cellspacing="0" width="100%" role="presentation"
                                                    style="min-width:100%">
                                                    <tbody>
                                                        <tr>
                                                            <td>
                                                                <table border="0" cellpadding="0" cellspacing="0"
                                                                    align="center" width="100%" style="width:100%"
                                                                    bgcolor="#E7E7E7">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td width="40"> </td>
                                                                            <td align="center">
                                                                                <table border="0" cellpadding="0"
                                                                                    cellspacing="0" align="center">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                height="45"> </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:26px;line-height:29px;font-weight:300;text-align:center;letter-spacing:0.5px;color:rgb(27,27,27)"
                                                                                                align="center" dir="ltr">
                                                                                                For additional assistance
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                height="10"> </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                height="10"> </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:16px;line-height:25px;font-weight:300;text-align:center;letter-spacing:0.5px;color:rgb(75,75,75)"
                                                                                                align="center" dir="ltr">
                                                                                                <span
                                                                                                    style="font-family:Arial,GucciFont,sans-serif"><a
                                                                                                        style="font-weight:300;font-family:Arial,GucciFont,sans-serif;color:rgb(0,0,0)"
                                                                                                        href="https://www.gucci.com/au/en_au/st/contact-us?location=US"
                                                                                                        target="_blank">Contact
                                                                                                        Us</a><br><a
                                                                                                        style="font-weight:300;font-family:Arial,GucciFont,sans-serif;text-decoration:none!important;color:rgb(0,0,0)"
                                                                                                        href="mailto:assistance@onlineshopping.gucci.com"
                                                                                                        target="_blank">assistance@onlineshopping.gucci.com</a></span>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="display:none;font-size:1px;line-height:1px"
                                                                                                height="25"> </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="display:none"
                                                                                                align="center">
                                                                                                <table border="0"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    align="center">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td width="20">
                                                                                                            </td>
                                                                                                            <td width="240"
                                                                                                                style="font-family:Arial,GucciFont,sans-serif;font-size:12px;line-height:20px;font-weight:300;text-align:center;color:rgb(27,27,27)"
                                                                                                                align="center"
                                                                                                                dir="ltr">
                                                                                                                <a href="tel:+44%202074951445"
                                                                                                                    style="display:block;text-decoration:none;padding-top:10px;padding-bottom:10px;border-top-width:1px;border-top-style:solid;border-bottom-width:1px;border-bottom-style:solid;border-left-width:1px;border-left-style:solid;font-family:Arial,GucciFont,sans-serif;border-top-color:rgb(27,27,27);border-bottom-color:rgb(27,27,27);border-left-color:rgb(27,27,27);color:rgb(27,27,27)"
                                                                                                                    target="_blank">
                                                                                                                    PHONE
                                                                                                                </a>
                                                                                                            </td>
                                                                                                            <td width="240"
                                                                                                                style="font-family:Arial,GucciFont,sans-serif;font-size:12px;line-height:20px;font-weight:300;text-align:center;color:rgb(27,27,27)"
                                                                                                                align="center"
                                                                                                                dir="ltr">
                                                                                                                <a href="mailto:assistance@uk-onlineshopping.gucci.com"
                                                                                                                    style="display:block;text-decoration:none;padding-top:10px;padding-bottom:10px;border-width:1px;border-style:solid;font-family:Arial,GucciFont,sans-serif;border-color:rgb(27,27,27);color:rgb(27,27,27)"
                                                                                                                    target="_blank">
                                                                                                                    MAIL
                                                                                                                </a>
                                                                                                            </td>
                                                                                                            <td width="20">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                height="45"> </td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                            <td width="40"> </td>
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
                                            <td align="center">
                                                <table cellpadding="0" cellspacing="0" width="100%" role="presentation"
                                                    style="min-width:100%">
                                                    <tbody>
                                                        <tr>
                                                            <td>
                                                                <table border="0" cellpadding="0" cellspacing="0"
                                                                    align="center" width="100%" style="width:100%">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td style="display:none" align="center">
                                                                                <table border="0" cellpadding="0"
                                                                                    cellspacing="0" align="center"
                                                                                    width="100%" style="width:100%">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td width="40"> </td>
                                                                                            <td align="center">
                                                                                                <table border="0"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    align="center">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                height="50">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:16px;line-height:16px;text-align:center;letter-spacing:1px;color:rgb(27,27,27)"
                                                                                                                align="center"
                                                                                                                dir="ltr">
                                                                                                                Discover
                                                                                                                more:
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                height="30">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:16px;line-height:16px;font-weight:300;text-align:center;letter-spacing:1px;color:rgb(27,27,27)"
                                                                                                                align="center"
                                                                                                                dir="ltr">
                                                                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/12/6HSZe8okjLrLXZWR6ZDt2w/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPTE0N2NhYWQzZDE2YmUyNjdkNTNjYzE5NjUwMDlmMGUzNGQ3NjhmMGExNWNhMmFjYTJmMmQ4YTdmYTBlMDM2NDJkZGM0NTgzMDMxMmQ4YzA5NzAwYWRmYTg5YmMxNWE4MjJhZWY2YWIxM2JmN2E0MDFlYWE4ZWJmYWIzY2MzN2Ew"
                                                                                                                    style="display:block;text-decoration:none;font-family:Arial,GucciFont,sans-serif;color:rgb(27,27,27)"
                                                                                                                    target="_blank">
                                                                                                                    WOMEN
                                                                                                                </a>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                height="30">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:16px;line-height:16px;font-weight:300;text-align:center;letter-spacing:1px;color:rgb(27,27,27)"
                                                                                                                align="center"
                                                                                                                dir="ltr">
                                                                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/13/CKnZxR0cLwWtu0ChQaONLQ/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPTE0N2NhYWQzZDE2YmUyNjc4MmMzNDBjMGRlOTE1YjhkYTMxNGQ3MjE3MTQ1NzkzN2I0YWM1NmIxYjk1YTkwNWRhNDZkMWQ0MThjOGM3MjJiOWZjZDljNGU1MDg5ODI0MzM0ZDYyMGRkNThjZDA5ZTIyNWUwY2Q0NzljNTA0NjEx"
                                                                                                                    style="display:block;text-decoration:none;font-family:Arial,GucciFont,sans-serif;color:rgb(27,27,27)"
                                                                                                                    target="_blank">
                                                                                                                    MEN
                                                                                                                </a>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                height="30">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:16px;line-height:16px;font-weight:300;text-align:center;letter-spacing:1px;color:rgb(27,27,27)"
                                                                                                                align="center"
                                                                                                                dir="ltr">
                                                                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/14/571f0y4KG1Syz4ayQJsS9g/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPTE0N2NhYWQzZDE2YmUyNjcwYTBhNzQ4YTdhYTZlN2JkMGQ4NTUwMDY0NTYyNzRjMGJlNWVmMjM1OWZhZGIxZTE0YmY5ZmRjYmI3NGNhODc3YjBlNWI3NzI2YmVlMmZlYmQ2NWE0ODljMDhmZDQ0YzA3ZTA5ZDNlYmJkYjA1M2Ri"
                                                                                                                    style="display:block;text-decoration:none;font-family:Arial,GucciFont,sans-serif;color:rgb(27,27,27)"
                                                                                                                    target="_blank">
                                                                                                                    CHILDREN
                                                                                                                </a>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                height="30">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:16px;line-height:16px;font-weight:300;text-align:center;letter-spacing:1px;color:rgb(27,27,27)"
                                                                                                                align="center"
                                                                                                                dir="ltr">
                                                                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/15/ZV2deLJ8hiTgGpJOHstuKw/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPTE0N2NhYWQzZDE2YmUyNjdkMmQ4ZjBlYTM0ZjgzOWYzM2E3MjIxN2E1NDZmY2RjMTQ1NmFiZGI4ZTc2Nzg1OWE3ZmZlNWE3OGZmNDE5ZjNiMGMwMTJmNGQwMzEzYzU1MDA2OWQyYzlmM2MxN2E4MWE4ZTIwMjdmNmY3NjdlN2E5"
                                                                                                                    style="display:block;text-decoration:none;font-family:Arial,GucciFont,sans-serif;color:rgb(27,27,27)"
                                                                                                                    target="_blank">
                                                                                                                    GIFTS
                                                                                                                </a>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                height="30">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:16px;line-height:16px;font-weight:300;text-align:center;letter-spacing:1px;color:rgb(27,27,27)"
                                                                                                                align="center"
                                                                                                                dir="ltr">
                                                                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/16/V6Zj3TxOmqSySA9bidunew/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPTE0N2NhYWQzZDE2YmUyNjdlMTg2ZTgxNDFiM2Y5NzFjZTVlYWY3Zjc4NjA2OTdiODVkOGQ5YjFmYTM5MWNhMjk2Mjk1MDhiYzdkYjUxOWE5NmZmMTE2NjlmMjA4M2FhODRiZjdkYzAzYTIyMjliZjBhODk3Y2Y4NDZhODU0MWZl"
                                                                                                                    style="display:block;text-decoration:none;font-family:Arial,GucciFont,sans-serif;color:rgb(27,27,27)"
                                                                                                                    target="_blank">
                                                                                                                    STORIES
                                                                                                                </a>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                height="50">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </td>
                                                                                            <td width="40"> </td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td align="center">
                                                                                <table border="0" cellpadding="0"
                                                                                    cellspacing="0" align="center"
                                                                                    width="100%" style="width:100%"
                                                                                    bgcolor="#1B1B1B">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                height="25"> </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="center">
                                                                                                <table border="0"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    align="center"
                                                                                                    width="100%"
                                                                                                    style="width:100%">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td width="15">
                                                                                                            </td>
                                                                                                            <td width="570"
                                                                                                                align="center">
                                                                                                                <table
                                                                                                                    border="0"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    align="center">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td align="center"
                                                                                                                                style="font-family:Arial,GucciFont,sans-serif;font-size:11px;line-height:16px;font-weight:300;letter-spacing:1px;text-align:center"
                                                                                                                                dir="ltr">
                                                                                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/17/nrtaOXgbCV1kHufNzIbP1A/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPWMzMDczMDU1MmY3ZjM3NjU4MTdlZTQ4YzQzMjE0YTAyZTQ4MTU1MTFhNmYyYmRlZTNmZjNkYWI5MDNjMDhmMDNiYjYwOWU5ZmM4YjZlODJkYWRmZjcxNGJkM2I2MWMyODdmNjM5ZjczOTg5MjI5NGVjOGQ5NjMwYzdkYmMwMDFh"
                                                                                                                                    style="text-decoration:none;font-weight:300;font-family:Arial,GucciFont,sans-serif;color:rgb(229,223,217)"
                                                                                                                                    target="_blank">
                                                                                                                                    My
                                                                                                                                    Account</a>
                                                                                                                            </td>
                                                                                                                            <td
                                                                                                                                style="padding:0px;width:20px">
                                                                                                                            </td>
                                                                                                                            <td align="center"
                                                                                                                                style="font-family:Arial,GucciFont,sans-serif;font-size:11px;line-height:16px;font-weight:300;letter-spacing:1px;text-align:center"
                                                                                                                                dir="ltr">
                                                                                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/18/GlL_O8KACxhd_JPtq0fMbw/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPWMzMDczMDU1MmY3ZjM3NjVkODJmMmJmZTQyN2JjNWQ1NTcyMWQ0OWQwNWNlNGY2NGMxNGE1N2VhNjE2ZGY5ODZlOWYwOWE3ZWRhODY3MDJhYTEyOTk1Y2VkNTA3ZWFiYTk2M2UyZjNjMDZjZDRkZjg4YmM1ZmQ1NzE0Njk4ODRi"
                                                                                                                                    style="text-decoration:none;font-weight:300;font-family:Arial,GucciFont,sans-serif;color:rgb(229,223,217)"
                                                                                                                                    target="_blank">FAQs</a>
                                                                                                                            </td>
                                                                                                                            <td
                                                                                                                                style="padding:0px;width:20px">
                                                                                                                            </td>
                                                                                                                            <td align="center"
                                                                                                                                style="font-family:Arial,GucciFont,sans-serif;font-size:11px;line-height:16px;font-weight:300;letter-spacing:1px;text-align:center"
                                                                                                                                dir="ltr">
                                                                                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/19/TShu7IR2vu4URXWIEUkwLg/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPWMzMDczMDU1MmY3ZjM3NjU3YzQ0YzVjOTE2MDVlNDNjZWE3NTU3ZTVkNWIwZTg4ZDFlNTFmY2ExMTVhZTYxYjczMzk3ODRmZDdlNWU4OTY5NjA3NzQ2NjQ5Njc1MjM2MWM4NDRiNGZlMTgzYjQ1NTI0YzVhMTNiNjQxZGVjYmYz"
                                                                                                                                    style="text-decoration:none;font-weight:300;font-family:Arial,GucciFont,sans-serif;color:rgb(229,223,217)"
                                                                                                                                    target="_blank">Returns
                                                                                                                                    &amp;
                                                                                                                                    Exchanges</a>
                                                                                                                            </td>
                                                                                                                            <td
                                                                                                                                style="padding:0px;width:20px">
                                                                                                                            </td>
                                                                                                                            <td align="center"
                                                                                                                                style="font-family:Arial,GucciFont,sans-serif;font-size:11px;line-height:16px;font-weight:300;letter-spacing:1px;text-align:center"
                                                                                                                                dir="ltr">
                                                                                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/20/awYoILaZ4eJAjhAmAYZaOA/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPWMzMDczMDU1MmY3ZjM3NjU3Zjg5ZDVkNTU1MjNlMjEwNGNlYjYxODA3MzNjOTU5MmNkZWM0ZDcyMTQyMDVlNDIzNGEwZjYzMjdhNTg4ZTBmYjljMmE4YjgyMWUyNWYwMzJmYzcxZDdiYmMxOTQ2YTg5MTBhMjYwYmE3N2I5M2Iw"
                                                                                                                                    style="text-decoration:none;font-weight:300;font-family:Arial,GucciFont,sans-serif;color:rgb(229,223,217)"
                                                                                                                                    target="_blank">
                                                                                                                                    Store
                                                                                                                                    Locator</a>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                            <td width="15">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="display:none"
                                                                                                align="center">
                                                                                                <table border="0"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    align="center"
                                                                                                    width="100%"
                                                                                                    style="width:100%">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td width="40">
                                                                                                            </td>
                                                                                                            <td
                                                                                                                align="center">
                                                                                                                <table
                                                                                                                    border="0"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    align="center">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                                height="25">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:16px;line-height:16px;font-weight:300;text-align:center;letter-spacing:1px"
                                                                                                                                align="center"
                                                                                                                                dir="ltr">
                                                                                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/21/W8I2api4NQdkP1ABjtDCvQ/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPWMzMDczMDU1MmY3ZjM3NjU4MTdlZTQ4YzQzMjE0YTAyZTQ4MTU1MTFhNmYyYmRlZTNmZjNkYWI5MDNjMDhmMDNiYjYwOWU5ZmM4YjZlODJkYWRmZjcxNGJkM2I2MWMyODdmNjM5ZjczOTg5MjI5NGVjOGQ5NjMwYzdkYmMwMDFh"
                                                                                                                                    style="display:block;text-decoration:none;font-weight:300;font-family:Arial,GucciFont,sans-serif;color:rgb(229,223,217)"
                                                                                                                                    target="_blank">My
                                                                                                                                    Account</a>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                                height="30">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:16px;line-height:16px;font-weight:300;text-align:center;letter-spacing:1px"
                                                                                                                                align="center"
                                                                                                                                dir="ltr">
                                                                                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/22/R4yX-idIa20CBjOHMJUExg/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPWMzMDczMDU1MmY3ZjM3NjVkODJmMmJmZTQyN2JjNWQ1NTcyMWQ0OWQwNWNlNGY2NGMxNGE1N2VhNjE2ZGY5ODZlOWYwOWE3ZWRhODY3MDJhYTEyOTk1Y2VkNTA3ZWFiYTk2M2UyZjNjMDZjZDRkZjg4YmM1ZmQ1NzE0Njk4ODRi"
                                                                                                                                    style="display:block;text-decoration:none;font-weight:300;font-family:Arial,GucciFont,sans-serif;color:rgb(229,223,217)"
                                                                                                                                    target="_blank">FAQs</a>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                                height="30">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:16px;line-height:16px;font-weight:300;text-align:center;letter-spacing:1px"
                                                                                                                                align="center"
                                                                                                                                dir="ltr">
                                                                                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/23/QaLny_g4iSxb987z8DY77g/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPWMzMDczMDU1MmY3ZjM3NjU3YzQ0YzVjOTE2MDVlNDNjZWE3NTU3ZTVkNWIwZTg4ZDFlNTFmY2ExMTVhZTYxYjczMzk3ODRmZDdlNWU4OTY5NjA3NzQ2NjQ5Njc1MjM2MWM4NDRiNGZlMTgzYjQ1NTI0YzVhMTNiNjQxZGVjYmYz"
                                                                                                                                    style="display:block;text-decoration:none;font-weight:300;font-family:Arial,GucciFont,sans-serif;color:rgb(229,223,217)"
                                                                                                                                    target="_blank">Returns
                                                                                                                                    &amp;
                                                                                                                                    Exchanges</a>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                                height="30">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td style="max-width:480px;font-family:Arial,GucciFont,sans-serif;font-size:16px;line-height:16px;font-weight:300;text-align:center;letter-spacing:1px"
                                                                                                                                align="center"
                                                                                                                                dir="ltr">
                                                                                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/24/6GSWuRUC-0zQMOoNJoQ37Q/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPWMzMDczMDU1MmY3ZjM3NjU3Zjg5ZDVkNTU1MjNlMjEwNGNlYjYxODA3MzNjOTU5MmNkZWM0ZDcyMTQyMDVlNDIzNGEwZjYzMjdhNTg4ZTBmYjljMmE4YjgyMWUyNWYwMzJmYzcxZDdiYmMxOTQ2YTg5MTBhMjYwYmE3N2I5M2Iw"
                                                                                                                                    style="display:block;text-decoration:none;font-weight:300;font-family:Arial,GucciFont,sans-serif;color:rgb(229,223,217)"
                                                                                                                                    target="_blank">Store
                                                                                                                                    Locator</a>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                                height="5">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                            <td width="40">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                height="25"> </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="center">
                                                                                                <table border="0"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    align="center"
                                                                                                    width="100%"
                                                                                                    style="width:100%">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td width="40">
                                                                                                            </td>
                                                                                                            <td
                                                                                                                align="center">
                                                                                                                <table
                                                                                                                    border="0"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    align="center"
                                                                                                                    width="100%"
                                                                                                                    style="width:100%">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td style="font-size:1px;line-height:1px;background:0% repeat rgb(88,86,84)"
                                                                                                                                height="1">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                            <td width="40">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="display:none"
                                                                                                align="center">
                                                                                                <table
                                                                                                    style="text-align:center"
                                                                                                    border="0"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    align="center">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td style="font-size:1px;line-height:1px;background:0% repeat rgb(88,86,84);width:30px!important"
                                                                                                                width="30"
                                                                                                                height="1">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                height="50"> </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="center">
                                                                                                <table border="0"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    align="center"
                                                                                                    width="100%"
                                                                                                    style="width:100%">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td width="40">
                                                                                                            </td>
                                                                                                            <td
                                                                                                                align="center">
                                                                                                                <table
                                                                                                                    border="0"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    align="center"
                                                                                                                    width="520"
                                                                                                                    style="margin:auto">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td style="padding:0px;vertical-align:top"
                                                                                                                                align="center">
                                                                                                                                <table
                                                                                                                                    align="center"
                                                                                                                                    border="0"
                                                                                                                                    cellpadding="0"
                                                                                                                                    cellspacing="0"
                                                                                                                                    style="max-width:520px"
                                                                                                                                    width="100%">
                                                                                                                                    <tbody>
                                                                                                                                        <tr>
                                                                                                                                            <td
                                                                                                                                                style="font-size:0px;text-align:center;vertical-align:top">
                                                                                                                                                <div
                                                                                                                                                    style="display:inline-block;vertical-align:top">
                                                                                                                                                    <table
                                                                                                                                                        align="left"
                                                                                                                                                        border="0"
                                                                                                                                                        cellpadding="0"
                                                                                                                                                        cellspacing="0"
                                                                                                                                                        width="260">
                                                                                                                                                        <tbody>
                                                                                                                                                            <tr>
                                                                                                                                                                <td style="border-right-width:1px;border-right-style:solid;border-right-color:rgb(108,105,103)"
                                                                                                                                                                    align="center">
                                                                                                                                                                    <table
                                                                                                                                                                        border="0"
                                                                                                                                                                        cellpadding="0"
                                                                                                                                                                        cellspacing="0"
                                                                                                                                                                        width="100%"
                                                                                                                                                                        align="center">
                                                                                                                                                                        <tbody>
                                                                                                                                                                            <tr>
                                                                                                                                                                                <td style="font-size:1px;line-height:1px"
                                                                                                                                                                                    height="15">
                                                                                                                                                                                </td>
                                                                                                                                                                            </tr>
                                                                                                                                                                            <tr>
                                                                                                                                                                                <td style="font-family:Arial,GucciFont,sans-serif;font-size:13px;line-height:20px;text-transform:uppercase;text-align:center;letter-spacing:1px;color:rgb(229,223,217)"
                                                                                                                                                                                    align="center"
                                                                                                                                                                                    dir="ltr">
                                                                                                                                                                                    Download
                                                                                                                                                                                    the
                                                                                                                                                                                    Gucci
                                                                                                                                                                                    App
                                                                                                                                                                                </td>
                                                                                                                                                                            </tr>
                                                                                                                                                                            <tr>
                                                                                                                                                                                <td style="font-size:1px;line-height:1px"
                                                                                                                                                                                    height="15">
                                                                                                                                                                                </td>
                                                                                                                                                                            </tr>
                                                                                                                                                                            <tr>
                                                                                                                                                                                <td style="font-size:0px;text-align:center"
                                                                                                                                                                                    align="center">
                                                                                                                                                                                    <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/25/yW_N-1laPF9b8CmPIdBgyw/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPWMzMDczMDU1MmY3ZjM3NjU5NGU1NmQ5MDE0MjBjODgwM2RmYWRkZmNkMjMwYmNkZTQ1MDY4YjQxNzNkMzA1NTMzYTM2M2FkOWZmNTdkNWFjZTFlNzYzYWQzNWJmNTcyMmZlNjAwNjc3MTAxODI5YTM3Mjc2NDNkNDMxNzYxMDQ0"
                                                                                                                                                                                        target="_blank">
                                                                                                                                                                                        <img src="http://image.email.gucci.com/lib/fe3815707564047f701279/m/21/dd1fa6a4-84e0-4fbd-8eaf-822d97c7f854.png"
                                                                                                                                                                                            style="display:inline-block;width:30px"
                                                                                                                                                                                            alt="-"
                                                                                                                                                                                            border="0"
                                                                                                                                                                                            width="30">
                                                                                                                                                                                    </a>
                                                                                                                                                                                </td>
                                                                                                                                                                            </tr>
                                                                                                                                                                            <tr>
                                                                                                                                                                                <td style="font-size:1px;line-height:1px"
                                                                                                                                                                                    height="20">
                                                                                                                                                                                </td>
                                                                                                                                                                            </tr>
                                                                                                                                                                            <tr>
                                                                                                                                                                                <td style="font-size:1px;line-height:1px;display:none"
                                                                                                                                                                                    height="10">
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
                                                                                                                                                    style="display:inline-block;vertical-align:top">
                                                                                                                                                    <table
                                                                                                                                                        align="left"
                                                                                                                                                        border="0"
                                                                                                                                                        cellpadding="0"
                                                                                                                                                        cellspacing="0"
                                                                                                                                                        width="260">
                                                                                                                                                        <tbody>
                                                                                                                                                            <tr>
                                                                                                                                                                <td
                                                                                                                                                                    align="center">
                                                                                                                                                                    <table
                                                                                                                                                                        border="0"
                                                                                                                                                                        cellpadding="0"
                                                                                                                                                                        cellspacing="0"
                                                                                                                                                                        width="100%"
                                                                                                                                                                        align="center">
                                                                                                                                                                        <tbody>
                                                                                                                                                                            <tr>
                                                                                                                                                                                <td style="font-size:1px;line-height:1px"
                                                                                                                                                                                    height="15">
                                                                                                                                                                                </td>
                                                                                                                                                                            </tr>
                                                                                                                                                                            <tr>
                                                                                                                                                                                <td style="font-family:Arial,GucciFont,sans-serif;font-size:13px;line-height:20px;text-transform:uppercase;text-align:center;letter-spacing:1px;color:rgb(229,223,217)"
                                                                                                                                                                                    align="center"
                                                                                                                                                                                    dir="ltr">
                                                                                                                                                                                    Follow
                                                                                                                                                                                    us
                                                                                                                                                                                    on
                                                                                                                                                                                </td>
                                                                                                                                                                            </tr>
                                                                                                                                                                            <tr>
                                                                                                                                                                                <td style="font-size:1px;line-height:1px"
                                                                                                                                                                                    height="15">
                                                                                                                                                                                </td>
                                                                                                                                                                            </tr>
                                                                                                                                                                            <tr>
                                                                                                                                                                                <td
                                                                                                                                                                                    align="center">
                                                                                                                                                                                    <table
                                                                                                                                                                                        border="0"
                                                                                                                                                                                        cellpadding="0"
                                                                                                                                                                                        cellspacing="0"
                                                                                                                                                                                        align="center">
                                                                                                                                                                                        <tbody>
                                                                                                                                                                                            <tr>
                                                                                                                                                                                                <td
                                                                                                                                                                                                    align="center">
                                                                                                                                                                                                    <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/26/DxPutSlF1ulMzACIrhllug/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPWMzMDczMDU1MmY3ZjM3NjU3YzlmZjBjM2MyNDA3NThiYmZkMzNiYjU0MmNhNWE4MTE1YTE5NGNlNzgwMTdmNDM3YmQyMzJjOTllN2VmNjhjNjMwZGE3MWRhM2VmYTc3MmFhOWYzYzQzZmU1Yjc0ZThhNWZiNGFhOTA1NjU2NjA2"
                                                                                                                                                                                                        target="_blank">
                                                                                                                                                                                                        <img src="http://image.email.gucci.com/lib/fe3815707564047f701279/m/21/2fce7590-ab30-41fd-b063-2a1e142d7507.png"
                                                                                                                                                                                                            style="width:30px"
                                                                                                                                                                                                            alt="Instagram"
                                                                                                                                                                                                            border="0"
                                                                                                                                                                                                            width="30">
                                                                                                                                                                                                    </a>
                                                                                                                                                                                                </td>
                                                                                                                                                                                                <td style="width:30px"
                                                                                                                                                                                                    width="30"
                                                                                                                                                                                                    align="center">
                                                                                                                                                                                                </td>
                                                                                                                                                                                                <td
                                                                                                                                                                                                    align="center">
                                                                                                                                                                                                    <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/27/9yWcJ27iGOFbp8mzltkVRw/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPWMzMDczMDU1MmY3ZjM3NjUxODhmM2UzNjZjMDE3NTlmNjZlNmZhNGRkNzExMTAzNzBmNDJmNThjNzUxYTI5MDI0NzI0OThjOGZjOTU2MTk5YzliM2UxNzljYjUzYzIyYjJjMzMzYzhkMjM2ZWZmMWZhMjA1MTNlMzViN2Q0MGU4"
                                                                                                                                                                                                        target="_blank">
                                                                                                                                                                                                        <img src="http://image.email.gucci.com/lib/fe3815707564047f701279/m/21/dbb35acf-2550-41fd-a272-11fe9600fa45.png"
                                                                                                                                                                                                            style="width:30px"
                                                                                                                                                                                                            alt="Facebook"
                                                                                                                                                                                                            border="0"
                                                                                                                                                                                                            width="30">
                                                                                                                                                                                                    </a>
                                                                                                                                                                                                </td>
                                                                                                                                                                                                <td style="width:30px"
                                                                                                                                                                                                    width="30"
                                                                                                                                                                                                    align="center">
                                                                                                                                                                                                </td>
                                                                                                                                                                                                <td
                                                                                                                                                                                                    align="center">
                                                                                                                                                                                                    <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/28/TLu6_krR_n7ixxf2QLQhUw/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPWMzMDczMDU1MmY3ZjM3NjVmNDNkNTQ0MGU2NGE0NTcyMDgwZmMyM2I0Y2YzYTZjOGExYjhmZDAwM2Y5YThmZGE2Yzc5OTU3MDFhMDM0N2ZlNTE4MDUyMmM3MWU5YmViZWM4ZGQyOTVkYTJkYTE0OWM3OGYzMTcwZDVkZmVjYTBi"
                                                                                                                                                                                                        target="_blank">
                                                                                                                                                                                                        <img src="http://image.email.gucci.com/lib/fe3815707564047f701279/m/21/9c83157d-c44a-4c41-9e6b-6712005e6dff.png"
                                                                                                                                                                                                            style="width:30px"
                                                                                                                                                                                                            alt="Twitter"
                                                                                                                                                                                                            border="0"
                                                                                                                                                                                                            width="30">
                                                                                                                                                                                                    </a>
                                                                                                                                                                                                </td>
                                                                                                                                                                                                <td style="width:30px"
                                                                                                                                                                                                    width="30"
                                                                                                                                                                                                    align="center">
                                                                                                                                                                                                </td>
                                                                                                                                                                                                <td
                                                                                                                                                                                                    align="center">
                                                                                                                                                                                                    <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/29/XqO9HEWakx7yFSEfgY8aMQ/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPWMzMDczMDU1MmY3ZjM3NjViNTk2NmZkYjk5ZDNhMjFlNzViYmM2YjBlMzI1MjY1ZmU2ODMxOGIzMjkwYmY0YzcxYTc1ZDcxZjgyYzQzNTc1ZjE0NGMyYTM0NmU1Nzg3MzgyZGQwOTYxM2U3Y2ZjNmEyNjhmODc4NWIxOTk0MTVh"
                                                                                                                                                                                                        target="_blank">
                                                                                                                                                                                                        <img src="http://image.email.gucci.com/lib/fe3815707564047f701279/m/21/6cb8fbf2-5aca-41eb-b2fd-0d287c36861f.png"
                                                                                                                                                                                                            style="width:30px"
                                                                                                                                                                                                            alt="YouTube"
                                                                                                                                                                                                            border="0"
                                                                                                                                                                                                            width="30">
                                                                                                                                                                                                    </a>
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
                                                                                                            <td width="40">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="center">
                                                                                                <table border="0"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    align="center"
                                                                                                    width="100%"
                                                                                                    style="width:100%">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td width="40">
                                                                                                            </td>
                                                                                                            <td
                                                                                                                align="center">
                                                                                                                <table
                                                                                                                    border="0"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    align="center">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                                height="50">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td style="font-family:Arial,GucciFont,sans-serif;font-size:12px;line-height:16px;text-align:center;letter-spacing:1px;color:rgb(113,113,113)"
                                                                                                                                align="center">
                                                                                                                                ©
                                                                                                                                2025
                                                                                                                                Guccio
                                                                                                                                Gucci
                                                                                                                                S.p.A.
                                                                                                                                -
                                                                                                                                All
                                                                                                                                rights
                                                                                                                                reserved.
                                                                                                                                SIAE
                                                                                                                                LICENCE
                                                                                                                                #
                                                                                                                                2294/I/1936
                                                                                                                                and
                                                                                                                                5647/I/1936
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td style="font-size:1px;line-height:1px"
                                                                                                                                height="20">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                            <td width="40">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="center">
                                                                                                <table border="0"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    align="center"
                                                                                                    width="100%" bgcolor=""
                                                                                                    style="width:100%">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td style="width:40px"
                                                                                                                width="40">
                                                                                                            </td>
                                                                                                            <td
                                                                                                                align="center">
                                                                                                                <table
                                                                                                                    border="0"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    align="center">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td align="center"
                                                                                                                                style="font-family:Arial,GucciFont,sans-serif;font-size:9px;line-height:14px;text-decoration:none;letter-spacing:1px;color:rgb(229,223,217)">
                                                                                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/30/nu2YaT9ZT9u83V6TjmhS1A/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPWMzMDczMDU1MmY3ZjM3NjUyMjAzMjBlNDE5OTk3MjEyZTM4NDZlOTQ1NmM4Yzc1NWE3OTJjNTRlYTBiNzk0NGYxZjU4NDhiOGU4NWUwYjZkZThlOTk3ZTZiZDMxYzgxMjNmZTJmNWRiNzhjMDI3ZTNkN2MyMWRiZDFlNDdlOTdl"
                                                                                                                                    style="font-family:Arial,GucciFont,sans-serif;font-size:9px;line-height:14px;text-decoration:none;letter-spacing:0.7px;color:rgb(229,223,217)"
                                                                                                                                    target="_blank"><u
                                                                                                                                        style="font-family:Arial,GucciFont,sans-serif">Unsubscribe</u></a>
                                                                                                                                |
                                                                                                                                <a href="https://smymr.mjt.lu/lnk/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/31/rUY9I-ikcOjQ4_YqczDGZg/aHR0cHM6Ly9jbGljay5lbWFpbC5ndWNjaS5jb20vP3FzPWMzMDczMDU1MmY3ZjM3NjVjM2I3Y2EyNDBjNjAxODVhOGU0OThkZjc4N2ExMjIzYTMxNTU4NTU1YWQxMjYzNTVmN2UyNzAyMmI5NjVlZDFkOGRkMDE1NTljNzlmYzFmZmQ5ZDg0YjRlNDkxOTExZmI2Y2I1YzFjMWYwNmFmMTY3"
                                                                                                                                    style="font-family:Arial,GucciFont,sans-serif;font-size:9px;line-height:14px;text-decoration:underline;letter-spacing:0.7px;color:rgb(229,223,217)"
                                                                                                                                    target="_blank"><u
                                                                                                                                        style="font-family:Arial,GucciFont,sans-serif">Privacy
                                                                                                                                        Policy</u></a>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td style="height:25px"
                                                                                                                                height="25">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                            <td style="width:40px"
                                                                                                                width="40">
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
                        </tr>
                        <tr>
                            <td style="font-size:1px;line-height:1px" height="30"> </td>
                        </tr>
                    </tbody>
                </table>
                <img src="https://click.email.gucci.com/open.aspx?ffcb10-fec61c767666077e-fe5713757c65067b7c15-fe3815707564047f701279-ff971577-fe2916727c620575731672-fef11076716c0c&amp;d=100197&amp;bmt=0"
                    width="1" height="1" alt="">


                <br><img
                    src="https://smymr.mjt.lu/oo/EAAABWBny5cAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwSMqmexZMghTIa82l_B8HEv8wAlFbo/7d4d7bef/e.gif"
                    height="1" width="1" alt="" border="0" style="height:1px;width:1px;border:0px">
            </div>
        </div>
    </div>


    </div>
    </div>
    """

    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
