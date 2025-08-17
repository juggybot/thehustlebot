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
    msg['From'] = formataddr((f'GOAT', sender_email))
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
    "Please enter the image url  (jpg, jpeg, png):",
    "Please enter the product name (AIR JORDAN 4 RETRO - 11):",
    "Please enter the brand (AIR JORDAN):",
    "Please enter the shoe condition (NEW/USED):",
    "Please enter the box condition (GOOD CONDITION/DAMAGED BOX):",
    "Please enter the product price (WITHOUT THE $):",
    "Please enter the shipping price (WITHOUT THE $ SIGN):",
    "Please enter the tax cost (WITHOUT THE $ SIGN):",
    "Please enter the order total (WITHOUT THE $ SIGN):",
    "Please enter the customer name (PAW PA):",
    "Please enter the street address (1962 TEST STREET):",
    "Please enter the suburb (LAKE COOPER):",
    "Please enter the postcode (6173):",
    "Please enter the country (AUSTRALIA):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira a URL da imagem (jpg, jpeg, png):",
    "Por favor, insira o nome do produto (AIR JORDAN 4 RETRO - 11):",
    "Por favor, insira a marca (AIR JORDAN):",
    "Por favor, insira a condição do tênis (NOVO/USADO):",
    "Por favor, insira a condição da caixa (BOA CONDIÇÃO/CAIXA DANIFICADA):",
    "Por favor, insira o preço do produto (SEM O $):",
    "Por favor, insira o valor do frete (SEM O SÍMBOLO $):",
    "Por favor, insira o valor do imposto (SEM O SÍMBOLO $):",
    "Por favor, insira o total do pedido (SEM O SÍMBOLO $):",
    "Por favor, insira o nome do cliente (PAW PA):",
    "Por favor, insira o endereço (1962 TEST STREET):",
    "Por favor, insira o bairro (LAKE COOPER):",
    "Por favor, insira o CEP (6173):",
    "Por favor, insira o país (AUSTRÁLIA):",
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
    part1 = random.randint(10000000, 99999999)  # Random 9-digit number

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
    recipient_email = f'{user_inputs[15]}'
    subject = f"Your GOAT order #{order_num}"

    # Format input into HTML template
    html_template = f"""
    <div marginwidth="0" marginheight="0"
        style="margin: 0px; padding: 0px; width: 100% !important; background-color: white;">
        <meta charset="UTF-8">
        <u></u> <img src="https://mandrillapp.com/track/open.php?u=30012989&amp;id=7dbad82ebcc9496eb17ac2e2cd1ea824" alt=""
            width="1" height="1" />
    </div>
    <div bgcolor="#ffffff" marginwidth="0" marginheight="0" style="height: auto; padding: 0px; margin: 0px;">
        <table style="font-size: 0em;" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#ffffff"
            align="center">
            <tbody>
                <tr>
                    <td width="100%" valign="top" bgcolor="#ffffff" align="center">
                        <div
                            style="display: none; font-size: 0px; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; color: rgb(0, 0, 0);">
                            You ordered the Air Jordan 4 Retro 'Military Black'
                        </div>
                        <table style="max-width: 600px; border: 1px solid rgb(0, 0, 0);" width="100%" cellspacing="0"
                            cellpadding="0" border="0" align="center">
                            <tbody>
                                <tr>
                                    <td width="100%" align="center">
                                        <table width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#ffffff"
                                            align="center">
                                            <tbody>
                                                <tr>
                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                </tr>
                                                <tr>
                                                    <td width="100%" align="center">
                                                        <table width="100%" cellspacing="0" cellpadding="0" border="0"
                                                            align="center">
                                                            <tbody>
                                                                <tr>
                                                                    <td style="padding-left: 40px; font-family: Helvetica, Arial, sans-serif, normal; letter-spacing: 3px; font-size: 50px;"
                                                                        width="50%" align="left">
                                                                        <a href="https://goat.app.link/?$deeplink_path=&amp;urlString=airgoat://&amp;$desktop_url=http://goat.com/?channel=Email&amp;campaign=buyer-order-confirmation&amp;utm_source=Email&amp;utm_medium=Transactional&amp;utm_campaign=buyer-order-confirmation&amp;utm_term=59941266"
                                                                            style="font-family: Helvetica, Arial, sans-serif, normal;"
                                                                            target="_blank">
                                                                            <img src="https://email-assets.goat.com/GOAT/2022/Transactional/Evergreen/GOATLogo2022.png"
                                                                                style="max-width: 40px; display: block; font-family: Helvetica, Arial, sans-serif, normal; color: rgb(0, 0, 0);"
                                                                                alt="GOAT" width="40" height="9"
                                                                                border="0" />
                                                                        </a>
                                                                    </td>
                                                                    <td style="padding-right: 40px;" width="50%"
                                                                        align="right">
                                                                        <a href="https://goat.app.link/?$deeplink_path=&amp;urlString=airgoat://&amp;$desktop_url=http://goat.com/?channel=Email&amp;campaign=buyer-order-confirmation&amp;utm_source=Email&amp;utm_medium=Transactional&amp;utm_campaign=buyer-order-confirmation&amp;utm_term=59941266"
                                                                            style="
                                                                                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif, normal;
                                                                                letter-spacing: 2.3px;
                                                                                font-size: 10px;
                                                                                line-height: 24px;
                                                                                font-weight: 500;
                                                                                text-transform: uppercase;
                                                                                text-decoration: underline;
                                                                                color: rgb(0, 0, 0);
                                                                            " target="_blank">
                                                                            shop
                                                                        </a>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                </tr>
                                                <tr>
                                                    <td style="border-top-width: 1px; border-top-style: solid; border-top-color: rgb(0, 0, 0);"
                                                        width="100%" height="1"></td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 27.5px 0px;" width="100%"></td>
                                                </tr>
                                                <tr>
                                                    <td style="
                                                            font-family: Georgia, Helvetica, Arial, sans-serif, normal;
                                                            font-size: 22px;
                                                            font-weight: 100;
                                                            letter-spacing: 0.3px;
                                                            line-height: 25px;
                                                            padding: 0px 10%;
                                                            color: rgb(0, 0, 0);
                                                        " width="100%" valign="middle" align="center">
                                                        Thank you for your order
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                </tr>
                                                <tr>
                                                    <td style="
                                                            font-family: Helvetica, Arial, sans-serif, normal;
                                                            font-size: 12px;
                                                            font-weight: 400;
                                                            letter-spacing: 0.4px;
                                                            line-height: 18px;
                                                            padding: 0px 10%;
                                                            color: rgb(0, 0, 0);
                                                        " width="100%" valign="middle" align="center">
                                                        Your order is being sent to GOAT for authentication by our
                                                        specialists. Once your item has been authenticated, we&#39;ll send
                                                        you a confirmation email with a link to
                                                        track your package.
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 17.5px 0px;" width="100%"></td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 0px 40px;" width="100%" align="center">
                                                        <table style="border: 1px solid rgb(0, 0, 0);" width="100%"
                                                            cellspacing="0" cellpadding="0" border="0" align="center">
                                                            <tbody>
                                                                <tr>
                                                                    <td style="
                                                                            padding: 20px 0px;
                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                            font-size: 14px;
                                                                            text-decoration: underline;
                                                                            font-weight: 500;
                                                                            letter-spacing: 2px;
                                                                            line-height: 24px;
                                                                            text-transform: uppercase;
                                                                            color: rgb(0, 0, 0);
                                                                        " width="100%" align="center">
                                                                        <a href="https://goat.app.link/?$desktop_deepview=&amp;$deeplink_path=&amp;orders/313881082/&amp;urlString=airgoat://orders/313881082&amp;$fallback_url=https://goat.com/manage-order/313881082"
                                                                            style="
                                                                                text-decoration: underline;
                                                                                font-weight: 500;
                                                                                letter-spacing: 2px;
                                                                                line-height: 24px;
                                                                                font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                color: rgb(0, 0, 0);
                                                                            " target="_blank">
                                                                            Order #{order_num}
                                                                        </a>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="border-top-width: 1px; border-top-style: solid; border-top-color: rgb(0, 0, 0);"
                                                                        width="100%" height="1"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 0px 60px;" width="100%"
                                                                        align="center">
                                                                        <img src="{user_inputs[0]}"
                                                                            style="display: block; width: 100%; max-width: 383px;"
                                                                            width="383" />
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="
                                                                                            padding: 0px 5px 0px 20px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            color: rgb(182, 182, 182);
                                                                                        " width="25%" align="left">
                                                                                        <a
                                                                                            style="text-decoration: none; font-family: 'Helvetica Neue', Helvetica, sans-serif, normal; color: rgb(0, 0, 0);">
                                                                                            DH6927 111‌ </a>
                                                                                    </td>
                                                                                    <td style="
                                                                                            padding: 0px 10px 0px 5px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 500;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(0, 0, 0);
                                                                                        " width="75%" align="left">
                                                                                        {user_inputs[1]}
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                    <td style="font-size: 0px; overflow: hidden; display: none;"
                                                                        width="100%" align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="
                                                                                            padding: 0px 20px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            color: rgb(182, 182, 182);
                                                                                        " width="100%" align="left">
                                                                                        <a
                                                                                            style="font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;">
                                                                                            205759 610 </a>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="padding: 2.5px 0px;"
                                                                                        width="100%"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="
                                                                                            padding: 0px 20px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 500;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            color: rgb(0, 0, 0);
                                                                                        " width="100%" align="left">
                                                                                        Cars x Classic Clog &#39;Lightning
                                                                                        McQueen&#39; – Size US 11 M
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 15px 0px;" width="100%"></td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 20px 0px;" width="100%"></td>
                                                </tr>
                                                <tr>
                                                    <td style="
                                                            padding: 0px 40px 15px;
                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                            font-size: 14px;
                                                            font-weight: 500;
                                                            letter-spacing: 2.3px;
                                                            line-height: 24px;
                                                            text-transform: uppercase;
                                                            color: rgb(0, 0, 0);
                                                        " width="100%" align="left">
                                                        item summary
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 0px 40px;" width="100%" align="center">
                                                        <table style="border: 1px solid rgb(0, 0, 0);" width="100%"
                                                            cellspacing="0" cellpadding="0" border="0" align="center">
                                                            <tbody>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="
                                                                                            padding: 0px 5px 0px 20px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(182, 182, 182);
                                                                                        " width="35%" align="left">
                                                                                        brand name
                                                                                    </td>
                                                                                    <td style="
                                                                                            padding: 0px 5px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(0, 0, 0);
                                                                                        " width="65%" align="left">
                                                                                        {user_inputs[2]}
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                    <td style="font-size: 0px; overflow: hidden; display: none;"
                                                                        width="100%" align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="
                                                                                            padding: 0px 20px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(182, 182, 182);
                                                                                        " width="100%" align="left">
                                                                                        box size
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="padding: 2.5px 0px;"
                                                                                        width="100%"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="
                                                                                            padding: 0px 20px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(0, 0, 0);
                                                                                        " width="100%" align="left">
                                                                                        11
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="border-top-width: 1px; border-top-style: solid; border-top-color: rgb(182, 182, 182);"
                                                                        width="100%" height="1"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="
                                                                                            padding: 0px 5px 0px 20px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(182, 182, 182);
                                                                                        " width="35%" align="left">
                                                                                        shoe condition
                                                                                    </td>
                                                                                    <td style="
                                                                                            padding: 0px 5px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(0, 0, 0);
                                                                                        " width="65%" align="left">
                                                                                        {user_inputs[3]}
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                    <td style="font-size: 0px; overflow: hidden; display: none;"
                                                                        width="100%" align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="
                                                                                            padding: 0px 20px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(182, 182, 182);
                                                                                        " width="100%" align="left">
                                                                                        shoe condition
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="padding: 2.5px 0px;"
                                                                                        width="100%"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="
                                                                                            padding: 0px 20px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(0, 0, 0);
                                                                                        " width="100%" align="left">
                                                                                        New
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="border-top-width: 1px; border-top-style: solid; border-top-color: rgb(182, 182, 182);"
                                                                        width="100%" height="1"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="
                                                                                            padding: 0px 5px 0px 20px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(182, 182, 182);
                                                                                        " width="35%" align="left">
                                                                                        box condition
                                                                                    </td>
                                                                                    <td style="
                                                                                            padding: 0px 5px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(0, 0, 0);
                                                                                        " width="65%" align="left">
                                                                                        {user_inputs[4]}
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                    <td style="font-size: 0px; overflow: hidden; display: none;"
                                                                        width="100%" align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="
                                                                                            padding: 0px 20px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(182, 182, 182);
                                                                                        " width="100%" align="left">
                                                                                        box condition
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="padding: 2.5px 0px;"
                                                                                        width="100%"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="
                                                                                            padding: 0px 20px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(0, 0, 0);
                                                                                        " width="100%" align="left">
                                                                                        Good Condition
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="border-top-width: 1px; border-top-style: solid; border-top-color: rgb(182, 182, 182);"
                                                                        width="100%" height="1"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="
                                                                                            padding: 0px 5px 0px 20px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(182, 182, 182);
                                                                                        " width="35%" align="left">
                                                                                        return policy
                                                                                    </td>
                                                                                    <td width="65%" align="left">
                                                                                        <a href="https://www.goat.com/returns?channel=Email&amp;campaign=buyer-order-confirmation&amp;utm_source=Email&amp;utm_medium=Transactional&amp;utm_campaign=buyer-order-confirmation&amp;utm_term=59941266"
                                                                                            style="
                                                                                                padding: 0px 10px 0px 5px;
                                                                                                font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                                font-size: 12px;
                                                                                                font-weight: 400;
                                                                                                letter-spacing: 2px;
                                                                                                line-height: 18px;
                                                                                                text-transform: uppercase;
                                                                                                text-decoration: underline;
                                                                                                color: rgb(0, 0, 0);
                                                                                            " target="_blank">
                                                                                            returnable for site credit
                                                                                        </a>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                    <td style="font-size: 0px; overflow: hidden; display: none;"
                                                                        width="100%" align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="
                                                                                            padding: 0px 20px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(182, 182, 182);
                                                                                        " width="100%" align="left">
                                                                                        return policy
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="padding: 2.5px 0px;"
                                                                                        width="100%"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="
                                                                                            padding: 0px 20px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(0, 0, 0);
                                                                                        " width="100%" align="left">
                                                                                        <a href="https://www.goat.com/returns?channel=Email&amp;campaign=buyer-order-confirmation&amp;utm_source=Email&amp;utm_medium=Transactional&amp;utm_campaign=buyer-order-confirmation&amp;utm_term=59941266"
                                                                                            style="
                                                                                                font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                                font-size: 12px;
                                                                                                font-weight: 400;
                                                                                                letter-spacing: 1.8px;
                                                                                                line-height: 18px;
                                                                                                text-transform: uppercase;
                                                                                                text-decoration: underline;
                                                                                                color: rgb(0, 0, 0);
                                                                                            " target="_blank">
                                                                                            returnable for site credit
                                                                                        </a>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 20px 0px;" width="100%"></td>
                                                </tr>
                                                <tr>
                                                    <td style="
                                                            padding: 0px 40px 15px;
                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                            font-size: 14px;
                                                            font-weight: 500;
                                                            letter-spacing: 2.3px;
                                                            line-height: 24px;
                                                            text-transform: uppercase;
                                                            color: rgb(0, 0, 0);
                                                        " width="100%" align="left">
                                                        order summary
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 0px 40px;" width="100%" align="center">
                                                        <table style="border: 1px solid rgb(0, 0, 0);" width="100%"
                                                            cellspacing="0" cellpadding="0" border="0" align="center">
                                                            <tbody>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="
                                                                                            padding: 0px 5px 0px 20px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(182, 182, 182);
                                                                                        " width="65%" align="left">
                                                                                        subtotal
                                                                                    </td>
                                                                                    <td style="
                                                                                            padding: 0px 15px 0px 5px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(0, 0, 0);
                                                                                        " width="35%" align="right">
                                                                                        {user_inputs[14]}{user_inputs[5]}
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="border-top-width: 1px; border-top-style: solid; border-top-color: rgb(182, 182, 182);"
                                                                        width="100%" height="1"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="
                                                                                            padding: 0px 5px 0px 20px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(182, 182, 182);
                                                                                        " width="65%" align="left">
                                                                                        shipping
                                                                                    </td>
                                                                                    <td style="
                                                                                            padding: 0px 15px 0px 5px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(0, 0, 0);
                                                                                        " width="35%" align="right">
                                                                                        {user_inputs[14]}{user_inputs[6]}
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="border-top-width: 1px; border-top-style: solid; border-top-color: rgb(182, 182, 182);"
                                                                        width="100%" height="1"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 7.5px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="
                                                                                            padding: 0px 5px 0px 20px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(182, 182, 182);
                                                                                        " width="65%" align="left">
                                                                                        verification
                                                                                    </td>
                                                                                    <td style="
                                                                                            padding: 0px 15px 0px 5px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(0, 0, 0);
                                                                                        " width="35%" align="right">
                                                                                        free
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="border-top-width: 1px; border-top-style: solid; border-top-color: rgb(182, 182, 182);"
                                                                        width="100%" height="1"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="
                                                                                            padding: 0px 5px 0px 20px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(182, 182, 182);
                                                                                        " width="65%" align="left">
                                                                                        tax
                                                                                    </td>
                                                                                    <td style="
                                                                                            padding: 0px 15px 0px 5px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(0, 0, 0);
                                                                                        " width="35%" align="right">
                                                                                        {user_inputs[14]}{user_inputs[7]}
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="border-top-width: 1px; border-top-style: solid; border-top-color: rgb(0, 0, 0);"
                                                                        width="100%" height="0"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td width="100%" align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="
                                                                                            padding: 0px 5px 0px 20px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 500;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(0, 0, 0);
                                                                                        " width="65%" align="left">
                                                                                        total paid
                                                                                    </td>
                                                                                    <td style="
                                                                                            padding: 0px 15px 0px 5px;
                                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 500;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 18px;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(0, 0, 0);
                                                                                        " width="35%" align="right">
                                                                                        {user_inputs[14]}{user_inputs[8]}
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 5px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="
                                                                            padding: 0px 20px;
                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                            font-size: 12px;
                                                                            font-weight: 400;
                                                                            letter-spacing: 2px;
                                                                            line-height: 18px;
                                                                            text-transform: uppercase;
                                                                            color: rgb(0, 0, 0);
                                                                        " width="100%" align="left">
                                                                        PayPal
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                </tr>
                                                <tr>
                                                    <td style="
                                                            padding: 0px 45px;
                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                            font-size: 12px;
                                                            font-weight: 300;
                                                            letter-spacing: 0.8px;
                                                            line-height: 16px;
                                                            text-align: center;
                                                            color: rgb(0, 0, 0);
                                                        " width="100%" align="left">
                                                        No additional tax should be charged upon arrival.
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 20px 0px;" width="100%"></td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 20px 0px;" width="100%"></td>
                                                </tr>
                                                <tr>
                                                    <td style="
                                                            padding: 0px 40px 15px;
                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                            font-size: 14px;
                                                            font-weight: 500;
                                                            letter-spacing: 2.3px;
                                                            line-height: 24px;
                                                            text-transform: uppercase;
                                                            color: rgb(0, 0, 0);
                                                        " width="100%" align="left">
                                                        shipping address
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 0px 40px; text-decoration: none; color: rgb(0, 0, 0);"
                                                        width="100%" align="center">
                                                        <table style="border: 1px solid rgb(0, 0, 0);" width="100%"
                                                            cellspacing="0" cellpadding="0" border="0" align="center">
                                                            <tbody>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="
                                                                            padding: 0px 5px 0px 20px;
                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                            font-size: 12px;
                                                                            font-weight: 500;
                                                                            letter-spacing: 2px;
                                                                            line-height: 18px;
                                                                            text-transform: uppercase;
                                                                            color: rgb(0, 0, 0);
                                                                        " width="100%" align="left">
                                                                        {user_inputs[9]}
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="
                                                                            padding: 0px 5px 0px 20px;
                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                            font-size: 12px;
                                                                            font-weight: 400;
                                                                            letter-spacing: 2px;
                                                                            line-height: 18px;
                                                                            text-transform: uppercase;
                                                                            color: rgb(0, 0, 0);
                                                                        " width="100%" align="left">
                                                                        <a
                                                                            style="text-decoration: none; font-family: 'Helvetica Neue', Helvetica, sans-serif, normal; color: rgb(0, 0, 0);">
                                                                            {user_inputs[10]} </a>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="
                                                                            padding: 0px 5px 0px 20px;
                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                            font-size: 12px;
                                                                            font-weight: 400;
                                                                            letter-spacing: 2px;
                                                                            line-height: 18px;
                                                                            text-transform: uppercase;
                                                                            color: rgb(0, 0, 0);
                                                                        " width="100%" align="left">
                                                                        <a
                                                                            style="text-decoration: none; font-family: 'Helvetica Neue', Helvetica, sans-serif, normal; color: rgb(0, 0, 0);">
                                                                        </a>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="
                                                                            padding: 0px 5px 0px 20px;
                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                            font-size: 12px;
                                                                            font-weight: 400;
                                                                            letter-spacing: 2px;
                                                                            line-height: 18px;
                                                                            text-transform: uppercase;
                                                                            color: rgb(0, 0, 0);
                                                                        " width="100%" align="left">
                                                                        <a
                                                                            style="text-decoration: none; font-family: 'Helvetica Neue', Helvetica, sans-serif, normal; color: rgb(0, 0, 0);">
                                                                            {user_inputs[11]} </a>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="
                                                                            padding: 0px 5px 0px 20px;
                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                            font-size: 12px;
                                                                            font-weight: 400;
                                                                            letter-spacing: 2px;
                                                                            line-height: 18px;
                                                                            text-transform: uppercase;
                                                                            color: rgb(0, 0, 0);
                                                                        " width="100%" align="left">
                                                                        <a
                                                                            style="text-decoration: none; font-family: 'Helvetica Neue', Helvetica, sans-serif, normal; color: rgb(0, 0, 0);">
                                                                            {user_inputs[12]} </a>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="
                                                                            padding: 0px 5px 0px 20px;
                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                            font-size: 12px;
                                                                            font-weight: 400;
                                                                            letter-spacing: 2px;
                                                                            line-height: 18px;
                                                                            text-transform: uppercase;
                                                                            color: rgb(0, 0, 0);
                                                                        " width="100%" align="left">
                                                                        <a
                                                                            style="text-decoration: none; font-family: 'Helvetica Neue', Helvetica, sans-serif, normal; color: rgb(0, 0, 0);">
                                                                            {user_inputs[13]} </a>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 10px 0px;" width="100%"></td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 20px 0px;" width="100%"></td>
                                                </tr>
                                                <tr>
                                                    <td width="100%" align="center">
                                                        <table width="100%" cellspacing="0" cellpadding="0" border="0"
                                                            align="center">
                                                            <tbody>
                                                                <tr>
                                                                    <td align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="padding: 0px 25px;"
                                                                                        width="100%" align="center">
                                                                                        <div align="center">
                                                                                            <a href="https://goat.app.link/?$desktop_deepview=&amp;$deeplink_path=&amp;orders/313881082/&amp;urlString=airgoat://orders/313881082&amp;$fallback_url=https://goat.com/manage-order/313881082"
                                                                                                style="
                                                                                                    border: 1px solid rgb(0, 0, 0);
                                                                                                    border-radius: 2px;
                                                                                                    display: block;
                                                                                                    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif, normal;
                                                                                                    font-size: 12px;
                                                                                                    letter-spacing: 2.3px;
                                                                                                    font-weight: 500;
                                                                                                    line-height: 60px;
                                                                                                    text-align: center;
                                                                                                    text-decoration: none;
                                                                                                    width: 320px;
                                                                                                    text-transform: uppercase;
                                                                                                    background-color: rgb(255, 255, 255);
                                                                                                    color: rgb(0, 0, 0);
                                                                                                " target="_blank">
                                                                                                view order status
                                                                                            </a>
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
                                                <tr>
                                                    <td style="padding: 20px 0px;" width="100%"></td>
                                                </tr>
                                                <tr>
                                                    <td width="100%" align="center">
                                                        <table style="background-color: rgb(239, 239, 239);" width="100%"
                                                            cellspacing="0" cellpadding="0" border="0" align="center">
                                                            <tbody>
                                                                <tr>
                                                                    <td style="padding: 20px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="
                                                                            padding: 0px 40px 15px;
                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                            font-size: 14px;
                                                                            font-weight: 500;
                                                                            letter-spacing: 2px;
                                                                            line-height: 24px;
                                                                            text-transform: uppercase;
                                                                            color: rgb(0, 0, 0);
                                                                        " width="100%" align="left">
                                                                        Top Questions
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 0px 40px;" width="100%"
                                                                        align="center">
                                                                        <table
                                                                            style="border: 1px solid rgb(0, 0, 0); background-color: rgb(255, 255, 255);"
                                                                            width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="padding: 10px 0px;"
                                                                                        width="100%"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td width="100%" align="center">
                                                                                        <span
                                                                                            style="text-decoration: none;">
                                                                                            <table width="100%"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                align="center">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td style="
                                                                                                                padding: 0px 5px 0px 20px;
                                                                                                                font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                                                font-size: 14px;
                                                                                                                font-weight: 400;
                                                                                                                letter-spacing: 1px;
                                                                                                                line-height: 20px;
                                                                                                                color: rgb(0, 0, 0);
                                                                                                            " width="85%"
                                                                                                            align="left">
                                                                                                            <a href="https://goat.zendesk.com/hc/en-us/articles/115004608267-When-will-I-receive-my-order-"
                                                                                                                style="
                                                                                                                    text-decoration: none;
                                                                                                                    font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                                                    color: rgb(0, 0, 0);
                                                                                                                "
                                                                                                                target="_blank">
                                                                                                                When will I
                                                                                                                receive my
                                                                                                                order?
                                                                                                            </a>
                                                                                                        </td>
                                                                                                        <td style="
                                                                                                                padding: 0px 15px 0px 5px;
                                                                                                                font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                                                font-size: 14px;
                                                                                                                font-weight: 700;
                                                                                                                letter-spacing: 1px;
                                                                                                                line-height: 20px;
                                                                                                                text-transform: uppercase;
                                                                                                                color: rgb(0, 0, 0);
                                                                                                            " width="15%"
                                                                                                            align="right">
                                                                                                            <a href="https://goat.zendesk.com/hc/en-us/articles/115004608267-When-will-I-receive-my-order-"
                                                                                                                style="font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;"
                                                                                                                target="_blank">
                                                                                                                <img src="https://sneakers-email-assets.s3.amazonaws.com/Transactional/Core%20Assets/arrow.png"
                                                                                                                    style="font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;"
                                                                                                                    width="5"
                                                                                                                    height="10" />
                                                                                                            </a>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                        </span>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="padding: 10px 0px;"
                                                                                        width="100%"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="border-top-width: 1px; border-top-style: solid; border-top-color: rgb(182, 182, 182);"
                                                                                        width="100%" height="1"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="padding: 10px 0px;"
                                                                                        width="100%"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td width="100%" align="center">
                                                                                        <span
                                                                                            style="text-decoration: none;">
                                                                                            <table width="100%"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                align="center">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td style="
                                                                                                                padding: 0px 5px 0px 20px;
                                                                                                                font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                                                font-size: 14px;
                                                                                                                font-weight: 400;
                                                                                                                letter-spacing: 1px;
                                                                                                                line-height: 20px;
                                                                                                                color: rgb(0, 0, 0);
                                                                                                            " width="85%"
                                                                                                            align="left">
                                                                                                            <a href="https://goat.zendesk.com/hc/en-us/articles/360021670172-Does-GOAT-Charge-Sales-Tax-"
                                                                                                                style="
                                                                                                                    text-decoration: none;
                                                                                                                    font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                                                    color: rgb(0, 0, 0);
                                                                                                                "
                                                                                                                target="_blank">
                                                                                                                Why was I
                                                                                                                charged
                                                                                                                sales tax?
                                                                                                            </a>
                                                                                                        </td>
                                                                                                        <td style="
                                                                                                                padding: 0px 15px 0px 5px;
                                                                                                                font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                                                font-size: 14px;
                                                                                                                font-weight: 700;
                                                                                                                letter-spacing: 1px;
                                                                                                                line-height: 20px;
                                                                                                                text-transform: uppercase;
                                                                                                                color: rgb(0, 0, 0);
                                                                                                            " width="15%"
                                                                                                            align="right">
                                                                                                            <a href="https://goat.zendesk.com/hc/en-us/articles/360021670172-Does-GOAT-Charge-Sales-Tax-"
                                                                                                                style="font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;"
                                                                                                                target="_blank">
                                                                                                                <img src="https://sneakers-email-assets.s3.amazonaws.com/Transactional/Core%20Assets/arrow.png"
                                                                                                                    style="font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;"
                                                                                                                    width="5"
                                                                                                                    height="10" />
                                                                                                            </a>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                        </span>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="padding: 10px 0px;"
                                                                                        width="100%"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="border-top-width: 1px; border-top-style: solid; border-top-color: rgb(182, 182, 182);"
                                                                                        width="100%" height="1"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="padding: 10px 0px;"
                                                                                        width="100%"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td width="100%" align="center">
                                                                                        <span
                                                                                            style="text-decoration: none;">
                                                                                            <table width="100%"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                align="center">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td style="
                                                                                                                padding: 0px 5px 0px 20px;
                                                                                                                font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                                                font-size: 14px;
                                                                                                                font-weight: 400;
                                                                                                                letter-spacing: 1px;
                                                                                                                line-height: 20px;
                                                                                                                color: rgb(0, 0, 0);
                                                                                                            " width="85%"
                                                                                                            align="left">
                                                                                                            <a href="https://goat.zendesk.com/hc/en-us/articles/115004608087-Can-I-cancel-my-order-"
                                                                                                                style="
                                                                                                                    text-decoration: none;
                                                                                                                    font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                                                    color: rgb(0, 0, 0);
                                                                                                                "
                                                                                                                target="_blank">
                                                                                                                Can I cancel
                                                                                                                my order?
                                                                                                            </a>
                                                                                                        </td>
                                                                                                        <td style="
                                                                                                                padding: 0px 15px 0px 5px;
                                                                                                                font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                                                font-size: 14px;
                                                                                                                font-weight: 700;
                                                                                                                letter-spacing: 1px;
                                                                                                                line-height: 20px;
                                                                                                                text-transform: uppercase;
                                                                                                                color: rgb(0, 0, 0);
                                                                                                            " width="15%"
                                                                                                            align="right">
                                                                                                            <a href="https://goat.zendesk.com/hc/en-us/articles/115004608087-Can-I-cancel-my-order-"
                                                                                                                style="font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;"
                                                                                                                target="_blank">
                                                                                                                <img src="https://sneakers-email-assets.s3.amazonaws.com/Transactional/Core%20Assets/arrow.png"
                                                                                                                    style="font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;"
                                                                                                                    width="5"
                                                                                                                    height="10" />
                                                                                                            </a>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                        </span>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="padding: 10px 0px;"
                                                                                        width="100%"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="border-top-width: 1px; border-top-style: solid; border-top-color: rgb(182, 182, 182);"
                                                                                        width="100%" height="1"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="padding: 10px 0px;"
                                                                                        width="100%"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td width="100%" align="center">
                                                                                        <span
                                                                                            style="text-decoration: none;">
                                                                                            <table width="100%"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                align="center">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td style="
                                                                                                                padding: 0px 5px 0px 20px;
                                                                                                                font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                                                font-size: 14px;
                                                                                                                font-weight: 400;
                                                                                                                letter-spacing: 1px;
                                                                                                                line-height: 20px;
                                                                                                                color: rgb(0, 0, 0);
                                                                                                            " width="85%"
                                                                                                            align="left">
                                                                                                            <a href="https://goat.zendesk.com/hc/en-us/articles/360001395651-How-do-I-update-my-shipping-address-"
                                                                                                                style="
                                                                                                                    text-decoration: none;
                                                                                                                    font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                                                    color: rgb(0, 0, 0);
                                                                                                                "
                                                                                                                target="_blank">
                                                                                                                How do I
                                                                                                                update my
                                                                                                                shipping
                                                                                                                address?
                                                                                                            </a>
                                                                                                        </td>
                                                                                                        <td style="
                                                                                                                padding: 0px 15px 0px 5px;
                                                                                                                font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                                                font-size: 14px;
                                                                                                                font-weight: 700;
                                                                                                                letter-spacing: 1px;
                                                                                                                line-height: 20px;
                                                                                                                text-transform: uppercase;
                                                                                                                color: rgb(0, 0, 0);
                                                                                                            " width="15%"
                                                                                                            align="right">
                                                                                                            <a href="https://goat.zendesk.com/hc/en-us/articles/360001395651-How-do-I-update-my-shipping-address-"
                                                                                                                style="font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;"
                                                                                                                target="_blank">
                                                                                                                <img src="https://sneakers-email-assets.s3.amazonaws.com/Transactional/Core%20Assets/arrow.png"
                                                                                                                    style="font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;"
                                                                                                                    width="5"
                                                                                                                    height="10" />
                                                                                                            </a>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                        </span>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="padding: 10px 0px;"
                                                                                        width="100%"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="border-top-width: 1px; border-top-style: solid; border-top-color: rgb(182, 182, 182);"
                                                                                        width="100%" height="1"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="padding: 10px 0px;"
                                                                                        width="100%"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td width="100%" align="center">
                                                                                        <span
                                                                                            style="text-decoration: none;">
                                                                                            <table width="100%"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                align="center">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td style="
                                                                                                                padding: 0px 5px 0px 20px;
                                                                                                                font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                                                font-size: 14px;
                                                                                                                font-weight: 400;
                                                                                                                letter-spacing: 1px;
                                                                                                                line-height: 20px;
                                                                                                                color: rgb(0, 0, 0);
                                                                                                            " width="85%"
                                                                                                            align="left">
                                                                                                            <a href="https://goat.zendesk.com/hc/en-us/articles/115004770408-Do-you-accept-returns-"
                                                                                                                style="
                                                                                                                    text-decoration: none;
                                                                                                                    font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                                                    color: rgb(0, 0, 0);
                                                                                                                "
                                                                                                                target="_blank">
                                                                                                                Will I be
                                                                                                                able to
                                                                                                                return this
                                                                                                                item?
                                                                                                            </a>
                                                                                                        </td>
                                                                                                        <td style="
                                                                                                                padding: 0px 15px 0px 5px;
                                                                                                                font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                                                font-size: 14px;
                                                                                                                font-weight: 700;
                                                                                                                letter-spacing: 1px;
                                                                                                                line-height: 20px;
                                                                                                                text-transform: uppercase;
                                                                                                                color: rgb(0, 0, 0);
                                                                                                            " width="15%"
                                                                                                            align="right">
                                                                                                            <a href="https://goat.zendesk.com/hc/en-us/articles/115004770408-Do-you-accept-returns-"
                                                                                                                style="font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;"
                                                                                                                target="_blank">
                                                                                                                <img src="https://sneakers-email-assets.s3.amazonaws.com/Transactional/Core%20Assets/arrow.png"
                                                                                                                    style="font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;"
                                                                                                                    width="5"
                                                                                                                    height="10" />
                                                                                                            </a>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                        </span>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="padding: 10px 0px;"
                                                                                        width="100%"></td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 20px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="
                                                                            padding: 0px 40px;
                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                            font-size: 12px;
                                                                            font-weight: 400;
                                                                            letter-spacing: 2px;
                                                                            line-height: 22px;
                                                                            text-transform: uppercase;
                                                                            color: rgb(0, 0, 0);
                                                                        " width="100%" align="center">
                                                                        Have more questions?
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="
                                                                            padding: 0px 40px;
                                                                            font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                            font-size: 12px;
                                                                            font-weight: 400;
                                                                            letter-spacing: 2px;
                                                                            line-height: 18px;
                                                                            text-transform: uppercase;
                                                                            color: rgb(0, 0, 0);
                                                                        " width="100%" align="center">
                                                                        <a href="https://www.goat.com/faq?channel=Email&amp;campaign=buyer-order-confirmation&amp;utm_source=Email&amp;utm_medium=Transactional&amp;utm_campaign=buyer-order-confirmation&amp;utm_term=59941266"
                                                                            style="
                                                                                font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                font-size: 12px;
                                                                                font-weight: 400;
                                                                                letter-spacing: 2px;
                                                                                line-height: 22px;
                                                                                text-transform: uppercase;
                                                                                text-decoration: underline;
                                                                                color: rgb(0, 0, 0);
                                                                            " target="_blank">
                                                                            Visit our FAQ
                                                                        </a>
                                                                        or
                                                                        <a href="https://goat.zendesk.com/hc/en-us/requests/new"
                                                                            style="
                                                                                font-family: 'Helvetica Neue', Helvetica, sans-serif, normal;
                                                                                font-size: 12px;
                                                                                font-weight: 400;
                                                                                letter-spacing: 2px;
                                                                                line-height: 22px;
                                                                                text-transform: uppercase;
                                                                                text-decoration: underline;
                                                                                color: rgb(0, 0, 0);
                                                                            " target="_blank">
                                                                            submit a request
                                                                        </a>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 20px 0px;" width="100%"></td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="background-color: rgb(0, 0, 0);" width="100%" align="center">
                                                        <table style="max-width: 600px;" width="100%" cellspacing="0"
                                                            cellpadding="0" border="0" align="center">
                                                            <tbody>
                                                                <tr>
                                                                    <td style="padding: 20px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 0px 40px;" width="100%"
                                                                        align="center">
                                                                        <table
                                                                            style="max-width: 600px; border: 1px solid rgb(255, 255, 255);"
                                                                            width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="padding: 50px 0px;"
                                                                                        width="100%"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="
                                                                                            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 600;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 24px;
                                                                                            padding: 0px 10%;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(255, 255, 255);
                                                                                        " width="100%" valign="middle"
                                                                                        align="center">
                                                                                        tip
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="padding: 15px 0px;"
                                                                                        width="100%"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="
                                                                                            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif, normal;
                                                                                            font-size: 12px;
                                                                                            font-weight: 400;
                                                                                            letter-spacing: 2px;
                                                                                            line-height: 22px;
                                                                                            padding: 0px 20%;
                                                                                            text-transform: uppercase;
                                                                                            color: rgb(255, 255, 255);
                                                                                        " width="100%" valign="middle"
                                                                                        align="center">
                                                                                        follow the progress of your order in
                                                                                        our app
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td style="padding: 20px 0px;"
                                                                                        width="100%"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td width="100%" align="center">
                                                                                        <table style="max-width: 600px;"
                                                                                            width="100%" cellspacing="0"
                                                                                            cellpadding="0" border="0"
                                                                                            align="center">
                                                                                            <tbody>
                                                                                                <tr>
                                                                                                    <td valign="top"
                                                                                                        align="center">
                                                                                                        <table width="100%"
                                                                                                            cellspacing="0"
                                                                                                            cellpadding="0"
                                                                                                            border="0"
                                                                                                            align="center">
                                                                                                            <tbody>
                                                                                                                <tr>
                                                                                                                    <td style="padding: 0px 15px;"
                                                                                                                        align="center">
                                                                                                                        <div>
                                                                                                                            <a href="https://goat.app.link/?$deeplink_path=home/&amp;urlString=airgoat://home&amp;$desktop_url=https://www.goat.com/app?channel=Email&amp;campaign=buyer-order-confirmation&amp;utm_source=Email&amp;utm_medium=Transactional&amp;utm_campaign=buyer-order-confirmation&amp;utm_content=&amp;utm_term=59941266"
                                                                                                                                style="
                                                                                                                                    border: 1px solid rgb(255, 255, 255);
                                                                                                                                    border-radius: 1px;
                                                                                                                                    display: inline-block;
                                                                                                                                    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif, normal;
                                                                                                                                    font-size: 12px;
                                                                                                                                    letter-spacing: 2.3px;
                                                                                                                                    font-weight: 500;
                                                                                                                                    line-height: 60px;
                                                                                                                                    text-align: center;
                                                                                                                                    text-decoration: none;
                                                                                                                                    width: 100%;
                                                                                                                                    max-width: 320px;
                                                                                                                                    text-transform: uppercase;
                                                                                                                                    background-color: rgb(0, 0, 0);
                                                                                                                                    color: rgb(255, 255, 255);
                                                                                                                                "
                                                                                                                                target="_blank">
                                                                                                                                download
                                                                                                                                goat
                                                                                                                                app
                                                                                                                            </a>
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
                                                                                <tr>
                                                                                    <td style="padding: 50px 0px;"
                                                                                        width="100%"></td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 20px 0px;" width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="background-color: rgb(0, 0, 0);" width="100%"
                                                                        align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td width="100%" align="center">
                                                                                        <a href="https://goat.zendesk.com/hc/en-us/requests/new"
                                                                                            style="
                                                                                                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif, normal;
                                                                                                letter-spacing: 1px;
                                                                                                font-size: 10px;
                                                                                                line-height: 15px;
                                                                                                font-weight: 400;
                                                                                                text-decoration: underline;
                                                                                                text-transform: uppercase;
                                                                                                color: rgb(255, 255, 255);
                                                                                            " target="_blank">
                                                                                            Contact Support
                                                                                        </a>
                                                                                        <span style="
                                                                                                text-decoration: none;
                                                                                                font-size: 11px;
                                                                                                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif, normal;
                                                                                                font-weight: 500;
                                                                                                line-height: 0px;
                                                                                                color: rgb(255, 255, 255);
                                                                                            ">
                                                                                            |
                                                                                        </span>
                                                                                        <a href="https://goat.app.link/?$deeplink_path=home/&amp;urlString=airgoat://home&amp;$desktop_url=https://www.goat.com/app?channel=Email&amp;campaign=buyer-order-confirmation&amp;utm_source=Email&amp;utm_medium=Transactional&amp;utm_campaign=buyer-order-confirmation&amp;utm_content=&amp;utm_term=59941266"
                                                                                            style="
                                                                                                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif, normal;
                                                                                                letter-spacing: 1px;
                                                                                                font-size: 10px;
                                                                                                line-height: 15px;
                                                                                                font-weight: 400;
                                                                                                text-decoration: underline;
                                                                                                text-transform: uppercase;
                                                                                                color: rgb(255, 255, 255);
                                                                                            " target="_blank">
                                                                                            download goat app
                                                                                        </a>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 12.5px 0px; background-color: rgb(0, 0, 0);"
                                                                        width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="background-color: rgb(0, 0, 0);" width="100%"
                                                                        align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td width="100%" align="center">
                                                                                        <a href="https://www.instagram.com/goat"
                                                                                            target="_blank">
                                                                                            <img src="https://sneakers-email-assets.s3.amazonaws.com/Transactional/Core%20Assets/INSTAGRAM_White.png"
                                                                                                style="display: inline-block; width: 100%; max-width: 30px;"
                                                                                                width="30" height="30" />
                                                                                        </a>
                                                                                        <a href="https://www.facebook.com/goatapp"
                                                                                            target="_blank">
                                                                                            <img src="https://sneakers-email-assets.s3.amazonaws.com/Transactional/Core%20Assets/FACEBOOK_White.png"
                                                                                                style="display: inline-block; width: 100%; max-width: 30px; padding: 0px 10px;"
                                                                                                width="30" height="30" />
                                                                                        </a>
                                                                                        <a href="https://www.twitter.com/goatapp"
                                                                                            target="_blank">
                                                                                            <img src="https://sneakers-email-assets.s3.amazonaws.com/Transactional/Core%20Assets/TWITTER_White.png"
                                                                                                style="display: inline-block; width: 100%; max-width: 30px;"
                                                                                                width="30" height="30" />
                                                                                        </a>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 12.5px 0px; background-color: rgb(0, 0, 0);"
                                                                        width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="background-color: rgb(0, 0, 0);" width="100%"
                                                                        align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                                            border="0" align="center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="
                                                                                            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif, normal;
                                                                                            letter-spacing: 0.5px;
                                                                                            font-size: 10px;
                                                                                            line-height: 18px;
                                                                                            font-weight: 300;
                                                                                            color: rgb(255, 255, 255);
                                                                                        " width="100%" valign="top"
                                                                                        align="center">
                                                                                        © 2025 1661, Inc. All Rights
                                                                                        Reserved
                                                                                        <span style="
                                                                                                letter-spacing: 0.5px;
                                                                                                font-size: 10px;
                                                                                                font-weight: 300;
                                                                                                text-decoration: none;
                                                                                                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif, normal;
                                                                                                color: rgb(255, 255, 255);
                                                                                            ">
                                                                                            |
                                                                                        </span>
                                                                                        <a href="https://www.goat.com/terms?channel=Email&amp;campaign=buyer-order-confirmation&amp;utm_source=Email&amp;utm_medium=Transactional&amp;utm_campaign=buyer-order-confirmation&amp;utm_term=59941266"
                                                                                            style="text-decoration: underline; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif, normal; color: rgb(255, 255, 255);"
                                                                                            target="_blank">
                                                                                            Terms
                                                                                        </a>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="background-color: rgb(0, 0, 0);" width="100%"
                                                                        align="center">
                                                                        <span style="
                                                                                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif, normal;
                                                                                font-size: 10px;
                                                                                font-weight: 300;
                                                                                letter-spacing: 0.5px;
                                                                                padding: 0px 3%;
                                                                                line-height: 18px;
                                                                                text-decoration: none;
                                                                                background-color: rgb(0, 0, 0);
                                                                                color: rgb(255, 255, 255);
                                                                            ">
                                                                            P.O. Box 91258, Los Angeles, CA 90009-1258
                                                                        </span>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 2.5px 0px; background-color: rgb(0, 0, 0);"
                                                                        width="100%"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding: 2.5px 0px; background-color: rgb(0, 0, 0);"
                                                                        width="100%"></td>
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
                                    <td style="padding: 20px 0px; background-color: rgb(0, 0, 0);" width="100%"></td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
            </tbody>
        </table>
        <img src="https://mandrillapp.com/track/open.php?u=30012989&amp;id=7dbad82ebcc9496eb17ac2e2cd1ea824" alt=""
            width="1" height="1" />
    </div>
    </blockquote>
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
