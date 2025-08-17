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
    msg['From'] = formataddr((f'Moncler', sender_email))
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
    "Please enter the first name (Juggy):",
    "Please enter the order date (01/11/2024):",
    "Please enter the image url (Must be Moncler image link):",
    "Please enter the item name (Moncler Maya Down Jacket):",
    "Please enter the item size (23):",
    "Please enter the item colour (Black):",
    "Please enter the product price (WITHOUT THE $):",
    "Please enter the estimated delivery date (12/03 and 15/03):",
    "Please enter the customer name (Juggy Resells):",
    "Please enter the street address (123 Test Street):",
    "Please enter the city, state & postcode (New York, NY 10002):",
    "Please enter the country (USA):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o primeiro nome (Juggy):",
    "Por favor, insira a data do pedido (01/11/2024):",
    "Por favor, insira a URL da imagem (Deve ser um link de imagem da Moncler):",
    "Por favor, insira o nome do item (Moncler Maya Down Jacket):",
    "Por favor, insira o tamanho do item (23):",
    "Por favor, insira a cor do item (Preto):",
    "Por favor, insira o preço do produto (SEM O SÍMBOLO $):",
    "Por favor, insira a data estimada de entrega (12/03 e 15/03):",
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira o endereço (123 Test Street):",
    "Por favor, insira a cidade, estado e código postal (New York, NY 10002):",
    "Por favor, insira o país (EUA):",
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
    part1 = random.randint(1000000000000, 9999999999999)  # Random 8-digit number

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
    recipient_email = f'{user_inputs[13]}'
    subject = f"Thank you for your order"

    html_template = f"""
    <html>

        <head></head>

        <body>
            <div alink="#000000" bgcolor="#ffffff" link="#000000" marginheight="0" marginwidth="0" text="#000000"
                vlink="#000000"
                style="background:#ffffff;color:#333333;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:11px;height:100%!important;margin:0px;padding:0px;width:100%!important">
                <table style="border-collapse:collapse;border-spacing:0" border="0" cellpadding="0" cellspacing="0"
                    align="center">
                    <tbody>
                        <tr style="height:0!important;opacity:0;display:none;padding:0;margin:0">
                            <td
                                style="padding:0px;vertical-align:top;max-width:300px;max-height:1px!important;opacity:0;white-space:nowrap;white-space:nowrapper;margin:0px;padding:0px;font-size:1px;line-height:1px;line-height:1px;color:#f6f6f6!important;background-color:#f6f6f6">
                                <span style="display:none!important">View all details</span>
                            </td>
                        </tr>
                        <tr style="height:0!important;opacity:0;display:none;padding:0;margin:0">
                            <td style="padding:0px;vertical-align:top;max-width:300px;max-height:1px!important;opacity:0;white-space:nowrap;white-space:nowrapper;margin:0px;padding:0px;font-size:1px;line-height:1px;line-height:1px;color:#f6f6f6!important;background-color:#f6f6f6"
                                align="center">
                                <span style="display:none!important">
                                    &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C;
                                    &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C;
                                    &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C;
                                    &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C;
                                    &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C;
                                    &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C;
                                    &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C;
                                    &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C;
                                    &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C;
                                    &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C;
                                    &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C;
                                    &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C;
                                    &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C;
                                    &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C;
                                    &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C;
                                    &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C;
                                    &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C;
                                    &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C;
                                    &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C;
                                    &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C; &#x200C;
                                    &#x200C; &#x200C;
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <table align="center" bgcolor="#F8F9FA" border="0" cellpadding="0" cellspacing="0"
                    style="border:0 none;border-collapse:collapse!important;float:none;margin:0 auto!important;width:100%"
                    width="100%">
                    <tbody>
                        <tr>
                            <td align="center" valign="top">
                                <table align="center" bgcolor="#ffffff" border="0" cellpadding="0" cellspacing="0"
                                    style="border:0 none;border-collapse:collapse!important;float:none;margin:0 auto!important;width:100%;max-width:750px"
                                    width="750">
                                    <tbody>
                                        <tr>
                                            <td align="center" valign="top" style="width:750px" width="750">
                                                <table align="center" bgcolor="#ffffff" border="0" cellpadding="0"
                                                    cellspacing="0" class="m_-2061449894373739617deviceWidth"
                                                    style="border:0 none;border-collapse:collapse!important;float:none;margin:0 auto!important;width:100%"
                                                    width="100%">
                                                    <tbody>
                                                        <tr>
                                                            <td align="center" style="background-color:#ffffff;width:100%"
                                                                width="100%" class="m_-2061449894373739617deviceWidth">
                                                                <table align="center" border="0" cellpadding="0" cellspacing="0"
                                                                    class="m_-2061449894373739617deviceWidth"
                                                                    style="border:0 none;border-collapse:collapse!important;float:none;margin:0 auto!important;width:600px"
                                                                    width="600">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td align="center"
                                                                                style="background-color:#ffffff;width:100%"
                                                                                width="100%">
                                                                                <table align="center" border="0" cellpadding="0"
                                                                                    cellspacing="0"
                                                                                    style="border:0 none;border-collapse:collapse!important;float:none;margin:0 auto!important;width:100%"
                                                                                    width="100%">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td align="center"
                                                                                                style="padding:10px 0 10px 0;font-size:14px;line-height:16px;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;color:#363636;text-decoration:none;text-align:center">
                                                                                                If you have problems viewing
                                                                                                this email, <a
                                                                                                    href="https://moncler.com"
                                                                                                    rel="link"
                                                                                                    style="font-size:14px;line-height:16px;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;color:#363636;text-decoration:underline"
                                                                                                    target="_blank">click
                                                                                                    here</a>
                                                                                            </td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                                <table align="center" border="0" cellpadding="0"
                                                                                    cellspacing="0"
                                                                                    class="m_-2061449894373739617deviceWidth"
                                                                                    style="border:0 none;border-collapse:collapse!important;float:none;margin:0 auto!important;width:100%"
                                                                                    width="100%">
                                                                                    <tbody>
                                                                                        <tr
                                                                                            style="font-size:0;line-height:0;border-collapse:collapse">
                                                                                            <td align="center" valign="bottom"
                                                                                                style="padding-top:15px;width:100%"
                                                                                                width="100%">
                                                                                                <table align="center" border="0"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    style="margin:0 auto!important;width:108px"
                                                                                                    valign="bottom" width="108">
                                                                                                    <tbody>
                                                                                                        <tr
                                                                                                            style="font-size:0;line-height:0;border-collapse:collapse">
                                                                                                            <td>
                                                                                                                <a href="https://click.email.moncler.com/?qs=aaa100749ff03ef5e884ea7245c54eda80672a3a5b69621051989a8935382e1ad0861326ecb37eb01fa6f21aa7ae4e1a6f9ccd699e576f9c73fa827ecddb2b94"
                                                                                                                    valign="bottom"
                                                                                                                    style="border:0 none;display:block;margin:0 auto;outline:0;text-decoration:none"
                                                                                                                    aria-label="Visit Moncler"
                                                                                                                    target="_blank">
                                                                                                                    <img src="https://moncler-cdn.thron.com/delivery/public/image/moncler/TRN_HeaderLogo/fm8pkl/std/0x0/TRN_HeaderLogo.png"
                                                                                                                        width="108"
                                                                                                                        style="border:0 none;display:block;outline:0;text-decoration:none"
                                                                                                                        border="0"
                                                                                                                        valign="bottom"
                                                                                                                        alt="Moncler logo">
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
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center" valign="top" style="width:750px" width="750">
                                                <table align="center" bgcolor="#FFFFFF" border="0" cellpadding="0"
                                                    cellspacing="0" class="m_-2061449894373739617deviceWidth"
                                                    style="border:0 none;border-collapse:collapse!important;float:none;margin:0 auto!important;width:100%;background-color:#ffffff"
                                                    width="100%">
                                                    <tbody>
                                                        <tr>
                                                            <td align="center" style="background-color:transparent;width:100%"
                                                                width="100%" class="m_-2061449894373739617deviceWidth">
                                                                <table align="center" border="0" cellpadding="0" cellspacing="0"
                                                                    class="m_-2061449894373739617deviceWidth"
                                                                    style="border:0 none;border-collapse:collapse!important;float:none;margin:0 auto!important;width:600px"
                                                                    width="600">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td align="center" valign="top"
                                                                                style="background-color:transparent;width:100%;padding-left:20px;padding-right:20px"
                                                                                width="100%">
                                                                                <table class="m_-2061449894373739617title"
                                                                                    align="center" cellpadding="0"
                                                                                    cellspacing="0"
                                                                                    style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:100%">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td height="40"
                                                                                                style="font-size:1px"></td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="center">
                                                                                                <h1 style="color:#000000;display:block;font-family:'Futuraefoplight4-regular',Helvetica,Arial,sans-serif;font-size:24px;font-weight:300;letter-spacing:.03em;line-height:28px;margin:0;text-align:center;text-transform:uppercase"
                                                                                                    class="m_-2061449894373739617Maintitle">
                                                                                                    THANK YOU FOR YOUR ORDER
                                                                                                </h1>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td height="40"
                                                                                                style="font-size:1px"></td>
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
                                                <table align="center" bgcolor="#ffffff" border="0" cellpadding="0"
                                                    cellspacing="0" class="m_-2061449894373739617deviceWidth"
                                                    style="border:0 none;border-collapse:collapse!important;float:none;margin:0 auto!important;width:726px"
                                                    width="726">
                                                    <tbody>
                                                        <tr>
                                                            <td align="center" style="background-color:#ffffff;width:100%"
                                                                width="100%" class="m_-2061449894373739617deviceWidth">
                                                                <table align="center" cellpadding="0" cellspacing="0"
                                                                    style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:100%">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td style="padding-left:20px;padding-right:20px">
                                                                                <table align="center" cellpadding="0"
                                                                                    cellspacing="0"
                                                                                    style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:600px"
                                                                                    width="600"
                                                                                    class="m_-2061449894373739617deviceWidth">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td align="center">
                                                                                                <p
                                                                                                    style="color:#000000;display:block;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;letter-spacing:.03em;line-height:20px;margin:0;text-align:center">
                                                                                                    Dear {user_inputs[0]},
                                                                                                    <br><br>Thank you for
                                                                                                    choosing Moncler! <br> Your
                                                                                                    order has been received.
                                                                                                </p>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td height="30"
                                                                                                style="font-size:1px"></td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="center" height="24"
                                                                                                style="font-size:1px"></td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="center">
                                                                                                <p
                                                                                                    style="color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:18px;font-weight:600;letter-spacing:.03em;line-height:24px;margin:0;text-align:center;text-transform:none;padding:0 10px">
                                                                                                    Order
                                                                                                    number<br>{order_num}
                                                                                                </p>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="center" height="8"
                                                                                                style="font-size:1px"></td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="center">
                                                                                                <p
                                                                                                    style="color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:14px;font-weight:300;letter-spacing:.03em;line-height:16px;margin:0;text-align:center;text-transform:none;padding:0 10px">
                                                                                                    Order date: {user_inputs[1]}
                                                                                                </p>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="center" height="32"
                                                                                                style="font-size:1px"></td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="padding-left:20px;padding-right:20px">
                                                                                <table align="center" cellpadding="0"
                                                                                    cellspacing="0"
                                                                                    style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:420px"
                                                                                    class="m_-2061449894373739617deviceWidth">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td align="center"
                                                                                                style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:100%"
                                                                                                width="100%"
                                                                                                class="m_-2061449894373739617deviceWidth">
                                                                                                <a href="https://click.email.moncler.com/?qs=aaa100749ff03ef594227cca55db684898633d62968276289f48b42a248a7a7841b1abb5193d5cbefd932115d7f29fb4430ef73cfe1be7d340759377dedd5991"
                                                                                                    style="color:#ffffff;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:14px;font-weight:400;letter-spacing:.03em;line-height:20px;margin:0;text-align:center;text-decoration:none;text-transform:uppercase"
                                                                                                    target="_blank">
                                                                                                    <table align="center"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        style="margin:0 auto!important;width:100%;background-color:#000"
                                                                                                        width="100%"
                                                                                                        class="m_-2061449894373739617deviceWidth"
                                                                                                        bgcolor="000000">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td
                                                                                                                    style="background-color:#000;color:#ffffff;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:14px;font-weight:400;letter-spacing:.03em;line-height:20px;margin:0;text-align:center;text-decoration:none;text-transform:uppercase;border:1px solid #000;width:100%;padding-top:15px;padding-bottom:15px;padding-left:10px;padding-right:10px">
                                                                                                                    <a href="https://click.email.moncler.com/?qs=aaa100749ff03ef594227cca55db684898633d62968276289f48b42a248a7a7841b1abb5193d5cbefd932115d7f29fb4430ef73cfe1be7d340759377dedd5991"
                                                                                                                        style="color:#ffffff;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:14px;font-weight:400;letter-spacing:.03em;line-height:20px;margin:0;text-align:center;text-decoration:none;text-transform:uppercase"
                                                                                                                        target="_blank">MANAGE
                                                                                                                        ORDER</a>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </a>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td height="45"
                                                                                                style="font-size:1px"></td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="padding-left:20px;padding-right:20px">
                                                                                <table align="center" cellpadding="0"
                                                                                    cellspacing="0"
                                                                                    style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:100%">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td width="100%" align="left"
                                                                                                valign="top">
                                                                                                <p
                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:20px;font-weight:300;line-height:24px;letter-spacing:.03em;text-align:left;margin-bottom:5px;text-transform:uppercase">
                                                                                                    YOUR ITEM(S)</p>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td height="20"
                                                                                                style="font-size:1px"></td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td height="1"
                                                                                                style="border-top:1px solid #e4e4e4;font-size:1px">
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td height="27"
                                                                                                style="font-size:1px"></td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="center"
                                                                                                style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:100%"
                                                                                                width="100%"
                                                                                                class="m_-2061449894373739617deviceWidth">
                                                                                                <table align="center"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:100%">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td width="22%"
                                                                                                                align="left"
                                                                                                                valign="top">
                                                                                                                <a href="{user_inputs[2]}"
                                                                                                                    aria-label="View Le Cedre Bleu Scented Candle 200 g"
                                                                                                                    target="_blank"><img
                                                                                                                        src="{user_inputs[2]}"
                                                                                                                        alt="{user_inputs[3]}"
                                                                                                                        width="100%"
                                                                                                                        style="height:auto;width:100%;outline:0;text-decoration:none;background-color:#000000"
                                                                                                                        border="0"></a>
                                                                                                            </td>
                                                                                                            <td width="3%"
                                                                                                                align="left"
                                                                                                                valign="top">
                                                                                                            </td>
                                                                                                            <td width="75%"
                                                                                                                align="left"
                                                                                                                valign="top">
                                                                                                                <table
                                                                                                                    align="center"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:100%">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td width="75%"
                                                                                                                                align="left"
                                                                                                                                valign="top"
                                                                                                                                class="m_-2061449894373739617columnLeftShip">
                                                                                                                                <p
                                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;line-height:20px;letter-spacing:.03em;text-align:left;margin-bottom:20px">
                                                                                                                                    {user_inputs[3]}
                                                                                                                                </p>
                                                                                                                                <p
                                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;line-height:20px;letter-spacing:.03em;text-align:left;margin-bottom:5px">
                                                                                                                                    Size:
                                                                                                                                    {user_inputs[4]}
                                                                                                                                    <br>
                                                                                                                                    Colour: {user_inputs[5]}
                                                                                                                                    <br>
                                                                                                                                    Quantity:
                                                                                                                                    1
                                                                                                                                </p>
                                                                                                                            </td>
                                                                                                                            <td width="2%"
                                                                                                                                align="left"
                                                                                                                                valign="top">
                                                                                                                            </td>
                                                                                                                            <td width="23%"
                                                                                                                                align="left"
                                                                                                                                valign="top"
                                                                                                                                class="m_-2061449894373739617columnRightShip"
                                                                                                                                style="color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;line-height:20px;letter-spacing:.03em;text-align:right;margin-bottom:20px">
                                                                                                                                <p
                                                                                                                                    style="padding:0;margin:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;line-height:20px;letter-spacing:.03em;text-align:right;text-transform:uppercase">
                                                                                                                                    {user_inputs[12]}{user_inputs[6]}
                                                                                                                                </p>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td class="m_-2061449894373739617height_5"
                                                                                                                height="8"
                                                                                                                colspan="5"
                                                                                                                style="font-size:1px">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td align="center"
                                                                                                                colspan="5"
                                                                                                                style="width:100%">
                                                                                                                <table
                                                                                                                    align="left"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    style="margin:0 auto!important;width:auto">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td
                                                                                                                                style="color:#000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:14px;font-weight:400;letter-spacing:.03em;line-height:20px;margin:0;text-align:center;text-decoration:none;width:100%">
                                                                                                                                <p
                                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:12px;font-weight:600;line-height:14px;letter-spacing:.03em;text-align:left;margin-bottom:5px">
                                                                                                                                    Estimated
                                                                                                                                    delivery
                                                                                                                                    between
                                                                                                                                    {user_inputs[7]}.
                                                                                                                                </p>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td height="20"
                                                                                                                colspan="5"
                                                                                                                style="font-size:1px">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td height="12"
                                                                                                style="font-size:1px"></td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td height="1"
                                                                                                style="border-top:1px solid #e4e4e4;font-size:1px">
                                                                                            </td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="padding-left:20px;padding-right:20px">
                                                                                <table align="center" cellpadding="0"
                                                                                    cellspacing="0"
                                                                                    style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:100%">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td height="30"
                                                                                                style="font-size:1px"></td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="center"
                                                                                                style="width:100%">
                                                                                                <table align="center"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:100%">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td width="58%"
                                                                                                                align="left"
                                                                                                                valign="top">
                                                                                                                <p
                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;line-height:20px;letter-spacing:.03em;text-align:left;margin-bottom:12px">
                                                                                                                    Subtotal</p>
                                                                                                            </td>
                                                                                                            <td width="2%"
                                                                                                                align="left"
                                                                                                                valign="top">
                                                                                                            </td>
                                                                                                            <td width="38%"
                                                                                                                align="right"
                                                                                                                valign="top">
                                                                                                                <p
                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;line-height:20px;letter-spacing:.03em;text-align:right;margin-bottom:12px">
                                                                                                                    {user_inputs[12]} {user_inputs[6]}</p>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td width="58%"
                                                                                                                align="left"
                                                                                                                valign="top">
                                                                                                                <p
                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:600;line-height:20px;letter-spacing:.03em;text-align:left;margin-bottom:12px">
                                                                                                                    Order total
                                                                                                                </p>
                                                                                                            </td>
                                                                                                            <td width="2%"
                                                                                                                align="left"
                                                                                                                valign="top">
                                                                                                            </td>
                                                                                                            <td width="38%"
                                                                                                                align="right"
                                                                                                                valign="top">
                                                                                                                <p
                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:600;line-height:20px;letter-spacing:.03em;text-align:right;margin-bottom:12px">
                                                                                                                    {user_inputs[12]} {user_inputs[6]}</p>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td height="20"
                                                                                                style="font-size:1px"></td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td height="1"
                                                                                                style="border-top:1px solid #e4e4e4;font-size:1px">
                                                                                            </td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="padding-left:20px;padding-right:20px">
                                                                                <table align="center" cellpadding="0"
                                                                                    cellspacing="0"
                                                                                    style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:100%">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td height="30"
                                                                                                style="font-size:1px"></td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="center"
                                                                                                style="width:100%">
                                                                                                <table
                                                                                                    class="m_-2061449894373739617deviceWidth"
                                                                                                    align="center"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:100%">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td class="m_-2061449894373739617block"
                                                                                                                align="center"
                                                                                                                style="width:50%;vertical-align:top"
                                                                                                                valign="top">
                                                                                                                <table
                                                                                                                    class="m_-2061449894373739617deviceWidth"
                                                                                                                    align="center"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:100%">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td align="center"
                                                                                                                                style="width:100%;padding-right:20px">
                                                                                                                                <p
                                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:600;line-height:20px;letter-spacing:.03em;text-align:left;margin-bottom:12px">
                                                                                                                                    Shipping
                                                                                                                                    Address
                                                                                                                                </p>
                                                                                                                                <p
                                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;line-height:20px;letter-spacing:.03em;text-align:left;margin-bottom:4px">
                                                                                                                                    {user_inputs[8]}
                                                                                                                                </p>
                                                                                                                                <p
                                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;line-height:20px;letter-spacing:.03em;text-align:left;margin-bottom:4px">
                                                                                                                                    {user_inputs[9]}
                                                                                                                                </p>
                                                                                                                                <p
                                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;line-height:20px;letter-spacing:.03em;text-align:left;margin-bottom:4px">
                                                                                                                                    {user_inputs[10]}
                                                                                                                                </p>
                                                                                                                                <p
                                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;line-height:20px;letter-spacing:.03em;text-align:left;margin-bottom:4px">
                                                                                                                                    {user_inputs[11]}
                                                                                                                                </p>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td height="30"
                                                                                                                                style="font-size:1px">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                            <td class="m_-2061449894373739617block"
                                                                                                                align="center"
                                                                                                                style="width:50%;vertical-align:top"
                                                                                                                valign="top">
                                                                                                                <table
                                                                                                                    class="m_-2061449894373739617deviceWidth"
                                                                                                                    align="center"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:100%">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td align="center"
                                                                                                                                style="width:100%;padding-right:20px">
                                                                                                                                <p
                                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:600;line-height:20px;letter-spacing:.03em;text-align:left;margin-bottom:12px">
                                                                                                                                    Billing
                                                                                                                                    Address
                                                                                                                                </p>
                                                                                                                                <p
                                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;line-height:20px;letter-spacing:.03em;text-align:left;margin-bottom:4px">
                                                                                                                                    {user_inputs[8]}
                                                                                                                                </p>
                                                                                                                                <p
                                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;line-height:20px;letter-spacing:.03em;text-align:left;margin-bottom:4px">
                                                                                                                                    {user_inputs[9]}
                                                                                                                                </p>
                                                                                                                                <p
                                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;line-height:20px;letter-spacing:.03em;text-align:left;margin-bottom:4px">
                                                                                                                                    {user_inputs[10]}
                                                                                                                                </p>
                                                                                                                                <p
                                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;line-height:20px;letter-spacing:.03em;text-align:left;margin-bottom:4px">
                                                                                                                                    {user_inputs[11]}
                                                                                                                                </p>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td height="30"
                                                                                                                                style="font-size:1px">
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
                                                                            <td style="padding-left:20px;padding-right:20px">
                                                                                <table align="center" cellpadding="0"
                                                                                    cellspacing="0"
                                                                                    style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:100%">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td align="center"
                                                                                                style="width:100%">
                                                                                                <table
                                                                                                    class="m_-2061449894373739617deviceWidth"
                                                                                                    align="center"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:100%">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td class="m_-2061449894373739617hide_on_mobile"
                                                                                                                height="30"
                                                                                                                style="font-size:1px">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr
                                                                                                            class="m_-2061449894373739617main_nav">
                                                                                                            <td align="center"
                                                                                                                style="width:50%;vertical-align:top"
                                                                                                                valign="top">
                                                                                                                <table
                                                                                                                    class="m_-2061449894373739617deviceWidth"
                                                                                                                    align="center"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:100%">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td align="center"
                                                                                                                                style="width:100%;padding-right:20px">
                                                                                                                                <p
                                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:600;line-height:20px;letter-spacing:.03em;text-align:left;margin-bottom:4px">
                                                                                                                                    Delivery
                                                                                                                                    Method
                                                                                                                                </p>
                                                                                                                                <p
                                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;line-height:20px;letter-spacing:.03em;text-align:left;margin-bottom:4px">
                                                                                                                                    Standard
                                                                                                                                </p>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td height="30"
                                                                                                                                style="font-size:1px">
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                            <td align="center"
                                                                                                                style="width:50%;vertical-align:top"
                                                                                                                valign="top">
                                                                                                                <table
                                                                                                                    class="m_-2061449894373739617deviceWidth"
                                                                                                                    align="center"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:100%">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td align="center"
                                                                                                                                style="width:100%">
                                                                                                                                <p
                                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:600;line-height:20px;letter-spacing:.03em;text-align:left;margin-bottom:4px">
                                                                                                                                    Payment
                                                                                                                                    Method
                                                                                                                                </p>
                                                                                                                                <p
                                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;line-height:20px;letter-spacing:.03em;text-align:left;margin-bottom:4px">
                                                                                                                                    Mastercard
                                                                                                                                </p>
                                                                                                                                <p
                                                                                                                                    style="margin:0;padding:0;color:#000000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;line-height:20px;letter-spacing:.03em;text-align:left;margin-bottom:4px">
                                                                                                                                    ****
                                                                                                                                    ****
                                                                                                                                    ****
                                                                                                                                    1414
                                                                                                                                </p>
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr>
                                                                                                                            <td height="30"
                                                                                                                                style="font-size:1px">
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
                                                                                            <td height="1"
                                                                                                style="border-top:1px solid #e4e4e4;font-size:1px">
                                                                                            </td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="padding-left:20px;padding-right:20px">
                                                                                <table align="center" cellpadding="0"
                                                                                    cellspacing="0"
                                                                                    style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:100%">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td height="45"
                                                                                                style="font-size:1px"></td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="center"
                                                                                                style="color:#000000;display:block;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;letter-spacing:.03em;line-height:20px;margin:0;text-align:center">
                                                                                                <table align="center"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    style="border:0;border-collapse:collapse!important;border-spacing:0!important;box-sizing:border-box;margin:0 auto!important;table-layout:auto;width:460px"
                                                                                                    class="m_-2061449894373739617deviceWidth">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td align="center"
                                                                                                                style="color:#000000;display:block;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;letter-spacing:.03em;line-height:20px;margin:0;text-align:center">
                                                                                                                According to the
                                                                                                                payment method
                                                                                                                chosen at
                                                                                                                checkout, the
                                                                                                                payment may
                                                                                                                already have
                                                                                                                been deducted or
                                                                                                                pre-authorized.<br><br>
                                                                                                                To check the
                                                                                                                status of your
                                                                                                                order enter your
                                                                                                                order number
                                                                                                                <a href="https://click.email.moncler.com/?qs=aaa100749ff03ef5002ba4186dabe220ef9831f0bdbfcf76012183bea29f15c763d8160191cf31efce2c8e20565d3d13accab86142a84d73797881ec5598b831"
                                                                                                                    aria-label="Order Status"
                                                                                                                    rel="link"
                                                                                                                    style="border:0 none;color:#000000;outline:0;text-align:center"
                                                                                                                    target="_blank">here</a>.
                                                                                                                If you shopped
                                                                                                                as a registered
                                                                                                                user, you can
                                                                                                                get status
                                                                                                                updates directly
                                                                                                                on
                                                                                                                <a href="https://click.email.moncler.com/?qs=aaa100749ff03ef5b9a655ea6a7f7002a0a65d5efb8f54c0a04d379ecbf45c46bba7273f4f9b7676f13e1f6f882a0cc81cc74ef345254f4a9e7d8ba29a3e6edc"
                                                                                                                    rel="link"
                                                                                                                    style="border:0 none;color:#000000;outline:0;text-align:center"
                                                                                                                    target="_blank">My
                                                                                                                    Moncler</a>.
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td height="20"
                                                                                                                style="font-size:1px">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td align="center"
                                                                                                                style="color:#000000;display:block;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;letter-spacing:.03em;line-height:20px;margin:0;text-align:center">
                                                                                                                Warmly,<br>Moncler
                                                                                                                Team</td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td height="45"
                                                                                                style="font-size:1px"></td>
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
                                            <td align="center" valign="top">
                                                <table align="center" bgcolor="#FFFFFF" border="0" cellpadding="0"
                                                    cellspacing="0" class="m_-2061449894373739617deviceWidth"
                                                    style="border:0 none;border-collapse:collapse!important;float:none;margin:0 auto!important;width:100%;background-color:#ffffff"
                                                    width="100%">
                                                    <tbody>
                                                        <tr>
                                                            <td align="center" style="background-color:transparent;width:100%"
                                                                width="100%" class="m_-2061449894373739617deviceWidth">
                                                                <table align="center" border="0" cellpadding="0" cellspacing="0"
                                                                    class="m_-2061449894373739617deviceWidth"
                                                                    style="border:0 none;border-collapse:collapse!important;float:none;margin:0 auto!important;width:100%"
                                                                    width="100%">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td align="center" valign="top"
                                                                                style="background-color:transparent">
                                                                                <table align="center" border="0" cellpadding="0"
                                                                                    cellspacing="0"
                                                                                    class="m_-2061449894373739617deviceWidth"
                                                                                    style="margin:0 auto!important;width:726px"
                                                                                    width="726">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td align="center" valign="top"
                                                                                                style="padding-left:20px;padding-right:20px">
                                                                                                <table border="0"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    class="m_-2061449894373739617deviceWidth"
                                                                                                    style="width:100%;margin:0 auto!important">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td height="1"
                                                                                                                style="border-top:1px solid #e4e4e4;font-size:1px">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td height="45"
                                                                                                                style="font-size:1px">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td align="center">
                                                                                                                <h2 class="m_-2061449894373739617fontSize18"
                                                                                                                    style="color:#000000;display:block;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:20px;font-weight:300;letter-spacing:.03em;line-height:24px;margin:0;text-align:center;text-transform:uppercase">
                                                                                                                    BROWSE OUR
                                                                                                                    NEW ARRIVALS
                                                                                                                </h2>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td height="34"
                                                                                                                style="font-size:1px">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td align="center"
                                                                                                                style="padding-bottom:60px"
                                                                                                                class="m_-2061449894373739617paddingB_40">
                                                                                                                <table
                                                                                                                    border="0"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    class="m_-2061449894373739617deviceWidth"
                                                                                                                    width="100%"
                                                                                                                    style="margin:0 auto!important">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td style="padding:0 50px 0 50px"
                                                                                                                                align="center">
                                                                                                                                <table
                                                                                                                                    align="center"
                                                                                                                                    border="0"
                                                                                                                                    cellpadding="0"
                                                                                                                                    cellspacing="0"
                                                                                                                                    class="m_-2061449894373739617deviceWidth"
                                                                                                                                    style="margin:0 auto!important;display:table">
                                                                                                                                    <tbody>
                                                                                                                                        <tr>
                                                                                                                                            <td align="center"
                                                                                                                                                style="color:#000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;line-height:20px;font-weight:300;letter-spacing:.1em;padding:0 10px;text-align:center">
                                                                                                                                                <a href="https://click.email.moncler.com/?qs=aaa100749ff03ef52b94eb30b45f450ef784340a59f02c4625b70553e7b94990e39d0030d5c4752094ec90eb337184c6c9f8b8466a58e8316b9087b3a7be18c2"
                                                                                                                                                    style="border:0 none;color:#000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;line-height:20px;font-weight:300;letter-spacing:.1em;outline:0;text-align:center;text-decoration:none"
                                                                                                                                                    rel="link"
                                                                                                                                                    target="_blank">Men</a>
                                                                                                                                            </td>
                                                                                                                                            <td width="20"
                                                                                                                                                style="width:20px;font-size:1px">
                                                                                                                                            </td>
                                                                                                                                            <td align="center"
                                                                                                                                                style="color:#000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;line-height:20px;font-weight:300;letter-spacing:.1em;padding:0 10px;text-align:center">
                                                                                                                                                <a href="https://click.email.moncler.com/?qs=aaa100749ff03ef5a346be2e9c9666f9b4f703c5aba1c3863fe9529d0477fbe658649058fc01d4d53a1398114cdba4a3b684bd5ffcfdecad2f86d9f18497fc05"
                                                                                                                                                    style="border:0 none;color:#000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;line-height:20px;font-weight:300;letter-spacing:.1em;outline:0;text-align:center;text-decoration:none"
                                                                                                                                                    rel="link"
                                                                                                                                                    target="_blank">Women</a>
                                                                                                                                            </td>
                                                                                                                                            <td width="20"
                                                                                                                                                style="width:20px;font-size:1px">
                                                                                                                                            </td>
                                                                                                                                            <td align="center"
                                                                                                                                                style="color:#000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;line-height:20px;font-weight:300;letter-spacing:.1em;padding:0 10px;text-align:center">
                                                                                                                                                <a href="https://click.email.moncler.com/?qs=aaa100749ff03ef58e8b0157a282890b961182ff9df82d8728db92dff6412137b379026a5de3a25bf62047a16c65eec5cf0fdf0ee5c0129253f9e20e677e238f"
                                                                                                                                                    style="border:0 none;color:#000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;line-height:20px;font-weight:300;letter-spacing:.1em;outline:0;text-align:center;text-decoration:none"
                                                                                                                                                    rel="link"
                                                                                                                                                    target="_blank">Children</a>
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
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center" valign="top">
                                                <table align="center" bgcolor="#FFFFFF" border="0" cellpadding="0"
                                                    cellspacing="0" class="m_-2061449894373739617deviceWidth"
                                                    style="border:0 none;border-collapse:collapse!important;float:none;margin:0 auto!important;width:100%;background-color:#ffffff"
                                                    width="100%">
                                                    <tbody>
                                                        <tr>
                                                            <td align="center" style="background-color:transparent;width:100%"
                                                                width="100%" class="m_-2061449894373739617deviceWidth">
                                                                <table align="center" border="0" cellpadding="0" cellspacing="0"
                                                                    class="m_-2061449894373739617deviceWidth"
                                                                    style="border:0 none;border-collapse:collapse!important;float:none;margin:0 auto!important;width:100%"
                                                                    width="100%">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td align="center" valign="top"
                                                                                style="background-color:transparent;padding-left:20px;padding-right:20px">
                                                                                <table align="center" border="0" cellpadding="0"
                                                                                    cellspacing="0"
                                                                                    class="m_-2061449894373739617deviceWidth"
                                                                                    style="margin:0 auto!important;width:686px"
                                                                                    width="686">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td height="1"
                                                                                                style="border-top:1px solid #e4e4e4;font-size:1px">
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td class="m_-2061449894373739617height_30"
                                                                                                height="50"
                                                                                                style="font-size:1px"></td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                                <table align="center" border="0" cellpadding="0"
                                                                                    cellspacing="0"
                                                                                    class="m_-2061449894373739617deviceWidth"
                                                                                    style="margin:0 auto!important;width:600px"
                                                                                    width="600">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td align="center" valign="top"
                                                                                                style="width:20px" width="20">
                                                                                            </td>
                                                                                            <td align="center" valign="top"
                                                                                                class="m_-2061449894373739617footerIcons">
                                                                                                <table border="0"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    class="m_-2061449894373739617deviceWidth"
                                                                                                    style="width:100%;margin:0 auto!important">
                                                                                                    <tbody>
                                                                                                        <tr
                                                                                                            class="m_-2061449894373739617main_nav">
                                                                                                            <td align="center"
                                                                                                                width="25%"
                                                                                                                style="color:#333;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;line-height:20px;font-weight:300;letter-spacing:.03em;text-align:center;text-transform:uppercase">
                                                                                                                <a href="https://click.email.moncler.com/?qs=aaa100749ff03ef55a6d9cdb0cbe3287b07ee378c310d459002b85305ebbb4b1b192b550b88420bf45e14ca45a4dc97196e969a1e574aa71a718e46376b1f6b8"
                                                                                                                    rel="link"
                                                                                                                    style="border:0 none;color:#000000;outline:0;text-align:center;text-decoration:none"
                                                                                                                    target="_blank">OUR
                                                                                                                    SPECIAL
                                                                                                                    SERVICES</a>
                                                                                                            </td>
                                                                                                            <td align="center"
                                                                                                                width="25%"
                                                                                                                style="color:#333;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;line-height:20px;font-weight:300;letter-spacing:.03em;text-align:center;text-transform:uppercase">
                                                                                                                <a href="https://click.email.moncler.com/?qs=aaa100749ff03ef565c7c1221c3ef6e6b5999af095091f50ca1db88dc40fc0c6dbba8ce67eb09f9131061f8d00785de7005c5540c460aaeefde48c97258af66d"
                                                                                                                    rel="link"
                                                                                                                    style="border:0 none;color:#000000;outline:0;text-align:center;text-decoration:none"
                                                                                                                    target="_blank">SHIPPING
                                                                                                                    INFORMATION</a>
                                                                                                            </td>
                                                                                                            <td align="center"
                                                                                                                width="25%"
                                                                                                                style="color:#333;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;line-height:20px;font-weight:300;letter-spacing:.03em;text-align:center;text-transform:uppercase">
                                                                                                                <a href="https://click.email.moncler.com/?qs=aaa100749ff03ef53ad9dec95216d75c3b1c83c19fc304c10226c46ea42ac08bc833a01c3b7ae77de7f1f320ed226ffd7821519943bfd4d219418cef22765d51"
                                                                                                                    rel="link"
                                                                                                                    style="border:0 none;color:#000000;outline:0;text-align:center;text-decoration:none"
                                                                                                                    target="_blank">EXCHANGES
                                                                                                                    AND
                                                                                                                    RETURNS</a>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </td>
                                                                                            <td align="center" valign="top"
                                                                                                style="width:20px" width="20">
                                                                                            </td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                                <table align="center" border="0" cellpadding="0"
                                                                                    cellspacing="0"
                                                                                    class="m_-2061449894373739617deviceWidth"
                                                                                    style="margin:0 auto!important;width:686px"
                                                                                    width="686">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td class="m_-2061449894373739617height_30"
                                                                                                height="50"
                                                                                                style="font-size:1px"></td>
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
                                            <td align="center" valign="top">
                                                <table align="center" bgcolor="#FFFFFF" border="0" cellpadding="0"
                                                    cellspacing="0" class="m_-2061449894373739617deviceWidth"
                                                    style="border:0 none;border-collapse:collapse!important;float:none;margin:0 auto!important;width:100%"
                                                    width="100%">
                                                    <tbody>
                                                        <tr>
                                                            <td align="center" style="background-color:#ffffff;width:100%"
                                                                width="100%" class="m_-2061449894373739617deviceWidth">
                                                                <table align="center" border="0" cellpadding="0" cellspacing="0"
                                                                    class="m_-2061449894373739617deviceWidth"
                                                                    style="border:0 none;border-collapse:collapse!important;float:none;margin:0 auto!important;width:750px"
                                                                    width="750">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td align="center" valign="top"
                                                                                style="background-color:#ffffff;padding-left:20px;padding-right:20px">
                                                                                <table align="center" border="0" cellpadding="0"
                                                                                    cellspacing="0"
                                                                                    class="m_-2061449894373739617deviceWidth"
                                                                                    style="margin:0 auto!important;width:710px"
                                                                                    width="710">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td height="1"
                                                                                                style="border-top:1px solid #e4e4e4;font-size:1px">
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="center" valign="top">
                                                                                                <table border="0"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    class="m_-2061449894373739617deviceWidth"
                                                                                                    style="width:100%;margin:0 auto!important">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td height="48"
                                                                                                                style="font-size:1px">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td align="center">
                                                                                                                <h2 class="m_-2061449894373739617fontSize18"
                                                                                                                    style="color:#000000;display:block;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:16px;font-weight:300;letter-spacing:.03em;line-height:20px;margin:0;text-align:center;text-transform:uppercase">
                                                                                                                    NEED HELP?
                                                                                                                </h2>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td height="16"
                                                                                                                style="font-size:1px">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td align="center">
                                                                                                                <table
                                                                                                                    border="0"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    class="m_-2061449894373739617deviceWidth"
                                                                                                                    style="width:80%;margin:0 auto!important">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td
                                                                                                                                style="color:#000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:14px;font-weight:300;letter-spacing:.03em;padding:0 20px;text-align:center;line-height:16px;text-decoration:none">
                                                                                                                                Our
                                                                                                                                <a href="https://click.email.moncler.com/?qs=aaa100749ff03ef515ab40627c8ff9c57dce2995098f053db55d96a764e8f4a646d417d4e6c7a38ba77b2147782b5e8d29755b2d03a90f882e9b3260427ae72d"
                                                                                                                                    style="color:#000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:14px;font-weight:300;letter-spacing:.03em;padding:0 0 0;text-align:center;line-height:16px;white-space:nowrap"
                                                                                                                                    rel="link"
                                                                                                                                    target="_blank">Client
                                                                                                                                    Service</a>
                                                                                                                                is
                                                                                                                                at
                                                                                                                                your
                                                                                                                                disposal.
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                    </tbody>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td height="15"
                                                                                                                style="font-size:1px">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td align="center"
                                                                                                                style="color:#000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:14px;font-weight:300;letter-spacing:.03em;padding:0 20px;text-align:center">
                                                                                                                <table
                                                                                                                    border="0"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    class="m_-2061449894373739617deviceWidth"
                                                                                                                    style="width:80%;margin:0 auto!important">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td class="m_-2061449894373739617block m_-2061449894373739617deviceWidth"
                                                                                                                                align="center"
                                                                                                                                style="color:#000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:14px;line-height:16px;font-weight:300;letter-spacing:.03em;padding:0 20px;text-align:center">
                                                                                                                                <table
                                                                                                                                    border="0"
                                                                                                                                    cellpadding="0"
                                                                                                                                    cellspacing="0"
                                                                                                                                    style="margin:0 auto!important;display:table">
                                                                                                                                    <tbody>
                                                                                                                                        <tr>
                                                                                                                                            <td height="15"
                                                                                                                                                style="font-size:1px">
                                                                                                                                            </td>
                                                                                                                                        </tr>
                                                                                                                                        <tr>
                                                                                                                                            <td><img src="https://moncler-cdn.thron.com/delivery/public/image/moncler/SocialPhone/fm8pkl/std/0X0/SocialPhone.png"
                                                                                                                                                    width="auto"
                                                                                                                                                    height="15">
                                                                                                                                            </td>
                                                                                                                                            <td><a href="tel:0080010204000"
                                                                                                                                                    style="color:#000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:14px;font-weight:300;letter-spacing:.03em;padding:0 0 0 10px;text-align:center;line-height:16px;text-decoration:none;text-transform:uppercase"
                                                                                                                                                    target="_blank">00
                                                                                                                                                    800
                                                                                                                                                    10204000</a>
                                                                                                                                            </td>
                                                                                                                                        </tr>
                                                                                                                                        <tr>
                                                                                                                                            <td height="10"
                                                                                                                                                style="font-size:1px">
                                                                                                                                            </td>
                                                                                                                                        </tr>
                                                                                                                                    </tbody>
                                                                                                                                </table>
                                                                                                                            </td>
                                                                                                                            <td class="m_-2061449894373739617block m_-2061449894373739617deviceWidth"
                                                                                                                                align="center"
                                                                                                                                style="color:#000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:14px;font-weight:300;letter-spacing:.03em;padding:0 20px;text-align:center">
                                                                                                                                <table
                                                                                                                                    border="0"
                                                                                                                                    cellpadding="0"
                                                                                                                                    cellspacing="0"
                                                                                                                                    style="margin:0 auto!important;display:table">
                                                                                                                                    <tbody>
                                                                                                                                        <tr>
                                                                                                                                            <td height="15"
                                                                                                                                                style="font-size:1px">
                                                                                                                                            </td>
                                                                                                                                        </tr>
                                                                                                                                        <tr>
                                                                                                                                            <td><img src="https://moncler-cdn.thron.com/delivery/public/image/moncler/SocialEmail/fm8pkl/std/0X0/SocialEmail.png"
                                                                                                                                                    width="auto"
                                                                                                                                                    height="15">
                                                                                                                                            </td>
                                                                                                                                            <td><a href="https://click.email.moncler.com/?qs=aaa100749ff03ef5d4f4882259083443b7b28ca79001f102e99a590f39a675583181dda29068d8f0de401c7c3810640bb6c320345cdf755bbd78a37528fe36f8"
                                                                                                                                                    style="color:#000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:14px;font-weight:300;letter-spacing:.03em;padding:0 0 0 10px;text-align:center;line-height:16px;text-decoration:none;text-transform:uppercase"
                                                                                                                                                    target="_blank">EMAIL</a>
                                                                                                                                            </td>
                                                                                                                                        </tr>
                                                                                                                                        <tr>
                                                                                                                                            <td height="10"
                                                                                                                                                style="font-size:1px">
                                                                                                                                            </td>
                                                                                                                                        </tr>
                                                                                                                                    </tbody>
                                                                                                                                </table>
                                                                                                                            </td>
                                                                                                                            <td class="m_-2061449894373739617block m_-2061449894373739617deviceWidth"
                                                                                                                                align="center"
                                                                                                                                style="color:#000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:14px;font-weight:300;letter-spacing:.03em;padding:0 20px;text-align:center">
                                                                                                                                <table
                                                                                                                                    border="0"
                                                                                                                                    cellpadding="0"
                                                                                                                                    cellspacing="0"
                                                                                                                                    style="margin:0 auto!important;display:table">
                                                                                                                                    <tbody>
                                                                                                                                        <tr>
                                                                                                                                            <td height="15"
                                                                                                                                                style="font-size:1px">
                                                                                                                                            </td>
                                                                                                                                        </tr>
                                                                                                                                        <tr>
                                                                                                                                            <td><img src="https://moncler-cdn.thron.com/delivery/public/image/moncler/SocialWhatsapp/fm8pkl/std/0X0/SocialWhatsapp.png"
                                                                                                                                                    width="auto"
                                                                                                                                                    height="15">
                                                                                                                                            </td>
                                                                                                                                            <td><a href="https://click.email.moncler.com/?qs=aaa100749ff03ef5857809114d296254097c7b56bd279928f1a120a4307032bcb14c90f052d686b5ae3014fd492fe8ea992f8a2c99b65f057e7af91ec3cafc45"
                                                                                                                                                    style="color:#000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:14px;font-weight:300;letter-spacing:.03em;padding:0 0 0 10px;text-align:center;line-height:16px;text-decoration:none;text-transform:uppercase"
                                                                                                                                                    target="_blank">WHATSAPP</a>
                                                                                                                                            </td>
                                                                                                                                        </tr>
                                                                                                                                        <tr>
                                                                                                                                            <td height="10"
                                                                                                                                                style="font-size:1px">
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
                                                                                                            <td height="15"
                                                                                                                style="font-size:1px">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td
                                                                                                                style="color:#000;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif;font-size:12px;font-weight:300;letter-spacing:.03em;padding:0 20px;text-align:center;line-height:14px;text-decoration:none">
                                                                                                                Please note this
                                                                                                                is an automatic
                                                                                                                email, do not
                                                                                                                reply to this
                                                                                                                message
                                                                                                                directly.
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td height="48"
                                                                                                                style="font-size:1px">
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                                <table align="center" border="0" cellpadding="0"
                                                                                    cellspacing="0"
                                                                                    class="m_-2061449894373739617deviceWidth"
                                                                                    style="margin:0 auto!important;width:100%"
                                                                                    width="100%">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td height="1"
                                                                                                style="border-top:1px solid #e4e4e4;font-size:1px">
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td height="24" colspan="2"
                                                                                                style="font-size:1px"></td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="center" width="20%"
                                                                                                class="m_-2061449894373739617footerDeviceWidth m_-2061449894373739617footerPadding15">
                                                                                                <table align="center" border="0"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    class="m_-2061449894373739617width_200"
                                                                                                    style="margin:0 auto!important">
                                                                                                    <tbody>
                                                                                                        <tr align="center">
                                                                                                            <td
                                                                                                                style="padding-left:10px;padding-right:5px">
                                                                                                                <a href="https://click.email.moncler.com/?qs=aaa100749ff03ef51fde21fb4e67b2e18d5678b647c2be6cedf4146003f3577414ec9c6b615dc094a22fcfbe6188eee49e014f7197e6476b9cdfe1bc23167443"
                                                                                                                    rel="link"
                                                                                                                    aria-label="Visit Facebook"
                                                                                                                    target="_blank"><img
                                                                                                                        alt="Facebook"
                                                                                                                        border="0"
                                                                                                                        height="16"
                                                                                                                        src="https://moncler-cdn.thron.com/delivery/public/image/moncler/FB-white/fm8pkl/std/20X32/FB-white.png"
                                                                                                                        style="border:0;display:block;outline:0;text-decoration:none"
                                                                                                                        width="10"></a>
                                                                                                            </td>
                                                                                                            <td
                                                                                                                style="padding-left:5px;padding-right:5px">
                                                                                                                <a href="https://click.email.moncler.com/?qs=aaa100749ff03ef567bbb8039452e288ebda75c657c9961289660105fa7228aef05638e5375b00739d733898ac4990341c11405d1010d32dcfb1cb8b4f690f8a"
                                                                                                                    rel="link"
                                                                                                                    aria-label="Visit Twitter"
                                                                                                                    target="_blank"><img
                                                                                                                        alt="Twitter"
                                                                                                                        border="0"
                                                                                                                        height="15"
                                                                                                                        src="https://moncler-cdn.thron.com/delivery/public/image/moncler/TW-white/fm8pkl/std/40X30/TW-white.png"
                                                                                                                        style="border:0;display:block;outline:0;text-decoration:none"
                                                                                                                        width="20"></a>
                                                                                                            </td>
                                                                                                            <td
                                                                                                                style="padding-left:5px;padding-right:5px">
                                                                                                                <a href="https://click.email.moncler.com/?qs=aaa100749ff03ef55c926ee037a7c5c0056b5933773df33cbe49bd0a4dfd9e7d6bdb12149f6f67303e0e02c32f0788dbb31150ed29773ffcd2e951eb97da0d0e"
                                                                                                                    rel="link"
                                                                                                                    aria-label="Visit Instagram"
                                                                                                                    target="_blank"><img
                                                                                                                        alt="Instagram"
                                                                                                                        border="0"
                                                                                                                        height="17"
                                                                                                                        src="https://moncler-cdn.thron.com/delivery/public/image/moncler/instagrambigg/fm8pkl/std/0X0/instagrambigg.png"
                                                                                                                        style="border:0;display:block;outline:0;text-decoration:none"
                                                                                                                        width="17"></a>
                                                                                                            </td>
                                                                                                            <td
                                                                                                                style="padding-left:5px;padding-right:10px">
                                                                                                                <a href="https://click.email.moncler.com/?qs=aaa100749ff03ef595dfd3d451d30fd73503f1b007f20963f6c118663e2ee1e63639de7a09a377a2c5775c14d624654bc01a0aba994fefb469952a34117aee89"
                                                                                                                    rel="link"
                                                                                                                    aria-label="Visit YouTube"
                                                                                                                    target="_blank"><img
                                                                                                                        alt="YouTube"
                                                                                                                        border="0"
                                                                                                                        height="16"
                                                                                                                        src="https://moncler-cdn.thron.com/delivery/public/image/moncler/YT-white/fm8pkl/std/48X32/YT-white.png"
                                                                                                                        style="border:0;display:block;outline:0;text-decoration:none"
                                                                                                                        width="24"></a>
                                                                                                            </td>
                                                                                                            <td
                                                                                                                style="padding-left:5px;padding-right:10px">
                                                                                                                <a href="https://click.email.moncler.com/?qs=aaa100749ff03ef58afa741bdd4d7a1636274b8dc316f5cc9d6d11e46aa4924503af0686e7f235e698e5935ab37af5772711f4827cb7c2268b883f1f189c8620"
                                                                                                                    rel="link"
                                                                                                                    aria-label="Enter Google Play"
                                                                                                                    target="_blank"><img
                                                                                                                        alt="Google Play"
                                                                                                                        border="0"
                                                                                                                        height="19"
                                                                                                                        src="https://moncler-cdn.thron.com/delivery/public/image/moncler/NL_GooglePlay_ENG/fm8pkl/std/0x0/NL_GooglePlay_ENG.png"
                                                                                                                        style="border:0;display:block;outline:0;text-decoration:none;height:19px"></a>
                                                                                                            </td>
                                                                                                            <td
                                                                                                                style="padding-left:5px;padding-right:10px">
                                                                                                                <a href="https://click.email.moncler.com/?qs=aaa100749ff03ef52f6d49673c1157dfcf11463c5cb8312794e38703cfe65e60e13e24c17313943d28933fc7d5bf4cbde97cc45a28f59cc299f87b1d5beea6fa"
                                                                                                                    rel="link"
                                                                                                                    aria-label="Enter Apple Store"
                                                                                                                    target="_blank"><img
                                                                                                                        alt="Apple Store"
                                                                                                                        border="0"
                                                                                                                        height="19"
                                                                                                                        src="https://moncler-cdn.thron.com/delivery/public/image/moncler/NL_Appstore_ENG/fm8pkl/std/0x0/NL_Appstore_ENG.png"
                                                                                                                        style="border:0;display:block;outline:0;text-decoration:none;height:19px"></a>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td height="24" colspan="2"
                                                                                                style="font-size:1px"></td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td height="1" colspan="2"
                                                                                                style="border-top:1px solid #e4e4e4;font-size:1px">
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td height="24" colspan="2"
                                                                                                style="font-size:1px"></td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="center" colspan="2"
                                                                                                width="100%"
                                                                                                class="m_-2061449894373739617footerDeviceWidth">
                                                                                                <p style="border:0 none;color:#000000;font-size:10px;outline:0;text-decoration:none;text-align:center;line-height:20px;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif"
                                                                                                    class="m_-2061449894373739617text_center">
                                                                                                    <a href="https://click.email.moncler.com/?qs=aaa100749ff03ef5d8443600c99676f332f54380f72549fb7d4965ff082ec48d6749827091268bd67e14ed7e4714893197ad07898de372785c9de26ea8ac0496"
                                                                                                        style="border:0 none;color:#000000;font-size:12px;line-height:14px;outline:0;text-decoration:none;white-space:nowrap;text-align:right;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif"
                                                                                                        rel="link"
                                                                                                        target="_blank">Privacy
                                                                                                        Policy</a> <a
                                                                                                        href="https://click.email.moncler.com/?qs=aaa100749ff03ef5bf2d80054e2ff0978f60a956a19ea28e488abf3f1e3d939b304804373297bb5e1407c0b1be8d729dab5a4f1aa53ed4a77b0de1b02dfe75cd"
                                                                                                        style="border:0 none;color:#000000;font-size:12px;line-height:14px;outline:0;text-decoration:none;white-space:nowrap;text-align:right;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif"
                                                                                                        rel="link"
                                                                                                        target="_blank">Terms of
                                                                                                        Sale</a>
                                                                                                </p>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td height="30" colspan="2"
                                                                                                style="font-size:1px"></td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="center" width="100%"
                                                                                                class="m_-2061449894373739617footerDeviceWidth">
                                                                                                <p style="border:0 none;color:#000000;font-size:10px;outline:0;text-decoration:none;text-align:center;line-height:15px;font-family:'Futuraefoplight8-regular',Helvetica,Arial,sans-serif"
                                                                                                    class="m_-2061449894373739617text_center">
                                                                                                </p>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td height="30" colspan="2"
                                                                                                style="font-size:1px"></td>
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
        </body>

        </html>
    """

    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
