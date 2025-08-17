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
    msg['From'] = formataddr(('Apple', sender_email))
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
    "Please enter the order date (20/01/24):",
    "Please enter the image url (jpg, jpeg, png):",
    "Please enter the product name (AirPods Max - Space Grey):",
    "Please enter the product price (WITHOUT THE $):",
    "Please enter the order total (WITHOUT THE $):",
    "Please enter the customer name (Juggy Resells):",
    "Please enter the street address (437 Piper Meadow):",
    "Please enter the suburb/city (North Owenland):",
    "Please enter the postcode (7486):",
    "Please enter the country (Australia):",
    "Please enter the customer email (juggyresells@gmail.com):",
    "Please enter the item quantity (1):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]
prompts_pt = [
    "Por favor, insira a data do pedido (20/01/24):",
    "Por favor, insira a URL da imagem (jpg, jpeg, png):",
    "Por favor, insira o nome do produto (AirPods Max - Cinza Espacial):",
    "Por favor, insira o preço do produto (SEM O SINAL $):",
    "Por favor, insira o total do pedido (SEM O SINAL $):",
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira o endereço (437 Piper Meadow):",
    "Por favor, insira o bairro/cidade (North Owenland):",
    "Por favor, insira o código postal (7486):",
    "Por favor, insira o país (Austrália):",
    "Por favor, insira o e-mail do cliente (juggyresells@gmail.com):",
    "Por favor, insira a quantidade de itens (1):",
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
    part1 = "W"
    part2 = random.randint(1000000000, 9999999999)  # Random 10-digit number

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
    sender_email = EMAIL
    sender_password = PASSWORD
    recipient_email = f'{user_inputs[13]}'
    subject = f"We're processing your order {order_num}" if lang == "en" else f"Estamos processando seu pedido {order_num}"
    html_template = f"""
    <tbody>
    <tr>
        <td align="center">
            <table style="background-color: rgb(255, 255, 255);" cellspacing="0" cellpadding="0" border="0" width="660" align="center" class="main-table" bac>
                <tbody>
                    <tr>
                        <td style="padding-top:32px;" align="left" valign="top" class="apple-logo-td">
                            <img data-unique-identifier="" alt="Apple" width="auto" height="25" border="0"
                                style="outline:none; display:block;" class="header-logo-img"
                                src="https://email.images.apple.com/rover/aos/moe/apple_icon_2x.png">
                        </td>
                    </tr>
                    <tr>
                        <td style="padding-top:75px; padding-bottom:51px;" align="left" valign="top"
                            class="greeting-td">
                            <h1 style="font-family:'SF UI Display Medium',system,-apple-system,-webkit-system-font,'SFNSText','Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif;; font-weight:normal; color:#333333; line-height:47px; font-size:34px; margin-top:0px; margin-left:0px; margin-right:0px; margin-bottom:2px; border-bottom:0px;"
                                class="heading-email">
                                Thank you for your order.
                            </h1>
                            <p style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-size:17px; line-height:24px; color:#333333; padding-top:13px; margin-top:0; margin-left:0; margin-right:0; margin-bottom:0;"
                                class="sub-heading">
                                One or more of your items will be delivered by a courier service.<br>Someone
                                must be present to receive these items.
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding-bottom:14px;" class="order-num-td">
                            <div style="color:#333333; font-weight:normal; font-size:14px; line-height:21px; margin-top:0px; margin-bottom:0px;"
                                class="order-num">
                                <span
                                    style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-weight:600; letter-spacing:0px;">Order
                                    Number:</span> <span
                                    style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; color:#0070C9;">
                                    <a aria-label="Order Number W7394434299"
                                        style="color:#0070c9; font-weight:normal;"
                                        rel="noreferrer nofollow noopener" target="_blank">{order_num}</a>
                                </span>
                            </div>
                            <div style="color:#333333; font-weight:normal; font-size:14px; line-height:21px; margin-top:0px; margin-bottom:0px;"
                                class="order-num">
                                <span
                                    style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-weight:600; letter-spacing:0px;">Ordered
                                    on:</span> <span
                                    style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-weight:normal;">{user_inputs[0]}</span>
                            </div>
                        </td>
                        </tr>
                        <tr>
                        <td align="left" height="1" bgcolor="D6D6D6" valign="top" class="moe-line-col">
                            <div
                                style="background-color:#D6D6D6 !important; font-size:1px !important; height:1px !important;">
                            </div>
                        </td>
                        </tr>
                        <tr>
                        <td align="center" valign="top">
                            <table style="padding-top:43px;" border="0" cellpadding="0" cellspacing="0" width="100%"
                                class="render-lineitems-table">
                                <tbody>
                                    <tr>
                                        <td>
                                            <table style="width:29%;" border="0" cellpadding="0" cellspacing="0"
                                                align="left" class="section-heading-table" width="29%">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-family:'SF UI Display Medium',system,-apple-system,-webkit-system-font,'SFNSText','Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif;; font-weight:500; letter-spacing:0px; color:#333333; font-size:22px; line-height:27px; margin-top:0; margin-left:0; margin-right:0; margin-bottom:0;"
                                                            align="left" valign="top"
                                                            class="section-items-heading-td">
                                                            <h2 style="font-family:'SF UI Display Medium',system,-apple-system,-webkit-system-font,'SFNSText','Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif;; font-weight:500; letter-spacing:0px; color:#333333; font-size:22px; line-height:27px; margin-top:0; margin-left:0; margin-right:0; margin-bottom:0;"
                                                                class="sectionHeading">Items to be Dispatched
                                                            </h2>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                            <table style="width:66.5%;" border="0" cellpadding="0" cellspacing="0"
                                                align="right" width="66.5%" class="product-list-table">
                                                <tbody>
                                                    <tr>
                                                        <td align="left" valign="top" class="pad-lr">
                                                            <div
                                                                style="padding-bottom:3px; font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-weight:600; letter-spacing:0px; font-size:17px; line-height:26px; color:#333333; margin-top:0px; margin-bottom:0px;">
                                                                Shipment 1</div>
                                                            <div
                                                                style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-size:17px; line-height:26px; color:#333333;">
                                                                <span style="font-weight:600">Delivery:</span>
                                                                Today from Store , 2 p.m. - 4 p.m. by Scheduled
                                                                Courier Delivery
                                                            </div>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td align="left" valign="top">
                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                align="left" width="100%">
                                                                <tbody>
                                                                    <tr>
                                                                        <td align="left" valign="top"
                                                                            class="pad-lr">
                                                                            <table
                                                                                style="width:100%; min-width:100%;"
                                                                                border="0" cellpadding="0"
                                                                                cellspacing="0" align="center"
                                                                                width="100%">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td style="height:21px; font-size:21px; line-height:21px; min-width:100%;"
                                                                                            align="left" height="21"
                                                                                            valign="top"
                                                                                            class="gap-30"><img
                                                                                                data-unique-identifier=""
                                                                                                width="1"
                                                                                                height="21"
                                                                                                border="0"
                                                                                                style="display:block; outline:none;"
                                                                                                alt=""
                                                                                                class="gap-30"
                                                                                                src="https://email.images.apple.com/dm/groups/aos/om/global/cmon/spacer.gif">
                                                                                        </td>
                                                                                    </tr>
                                                                                    <tr>
                                                                                        <td style="min-width:100%;"
                                                                                            align="left" height="1"
                                                                                            bgcolor="D6D6D6"
                                                                                            valign="top"
                                                                                            class="moe-line-col">
                                                                                            <div
                                                                                                style="background-color:D6D6D6; font-size:1px !important; height:1px !important;">
                                                                                            </div>
                                                                                        </td>
                                                                                    </tr>
                                                                                    <tr>
                                                                                        <td style="height:28px; font-size:28px; line-height:28px; min-width:100%;"
                                                                                            align="left" height="28"
                                                                                            valign="top"
                                                                                            class="gap-24"><img
                                                                                                data-unique-identifier=""
                                                                                                width="1"
                                                                                                height="28"
                                                                                                border="0"
                                                                                                style="display:block; outline:none;"
                                                                                                alt=""
                                                                                                class="gap-24"
                                                                                                src="https://email.images.apple.com/dm/groups/aos/om/global/cmon/spacer.gif">
                                                                                        </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                            <table cellpadding="0" cellspacing="0" border="0"
                                                                align="left" width="100%" class="line-item-table">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="padding-right:10px;" valign="top"
                                                                            width="96" align="center"
                                                                            class="product-image-td"><img
                                                                                data-unique-identifier=""
                                                                                style="outline:none; display:block;"
                                                                                width="100px" alt="image"
                                                                                class="product-image-img"
                                                                                src="{user_inputs[1]}">
                                                                        </td>
                                                                        <td align="left" valign="top">
                                                                            <table cellpadding="0" cellspacing="0"
                                                                                border="0" align="left" width="100%"
                                                                                class="item-details-table">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-weight:600; letter-spacing:0px; font-size:17px; line-height:26px; color:#333333; margin:0;"
                                                                                            valign="top"
                                                                                            align="left"
                                                                                            class="product-name-td">
                                                                                            {user_inputs[2]}
                                                                                        </td>
                                                                                    </tr>
                                                                                    <tr>
                                                                                        <td style="padding-top:6px; font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-size:17px; line-height:26px; color:#333333;"
                                                                                            align="left"
                                                                                            class="base-price-td">
                                                                                            {user_inputs[12]}{user_inputs[3]}
                                                                                        </td>
                                                                                    </tr>
                                                                                    <tr>
                                                                                        <td style="padding-top:6px;"
                                                                                            class="qty-price-divider"
                                                                                            width="100%">
                                                                                            <table
                                                                                                style="height:1px; font-size:1px; line-height:1px; width:100%;"
                                                                                                height="1"
                                                                                                border="0"
                                                                                                cellpadding="0"
                                                                                                cellspacing="0"
                                                                                                align="center"
                                                                                                width="100%">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td align="left"
                                                                                                            height="1"
                                                                                                            bgcolor="D6D6D6"
                                                                                                            valign="top"
                                                                                                            class="moe-line-col">
                                                                                                            <div
                                                                                                                style="background-color:#D6D6D6 !important; font-size:1px !important; height:1px !important;">
                                                                                                            </div>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                        </td>
                                                                                    </tr>
                                                                                    <tr>
                                                                                        <td style="padding-top:6px;"
                                                                                            class="qty-price-td">
                                                                                            <table cellspacing="0"
                                                                                                border="0"
                                                                                                cellpadding="0"
                                                                                                align="left"
                                                                                                width="45%"
                                                                                                class="product-quantity-table">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-size:17px; line-height:26px; color:#333333;"
                                                                                                            align="left"
                                                                                                            class="product-quantity">
                                                                                                            <nobr>
                                                                                                                Qty
                                                                                                                {user_inputs[11]}
                                                                                                            </nobr>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                            <table cellspacing="0"
                                                                                                border="0"
                                                                                                cellpadding="0"
                                                                                                align="right"
                                                                                                width="50%"
                                                                                                class="total-price-table">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-weight:600; letter-spacing:0px; font-size:17px; line-height:26px; color:#333333; margin:0;"
                                                                                                            align="right"
                                                                                                            class="total-price">
                                                                                                            {user_inputs[12]}{user_inputs[4]}
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
                            <table cellspacing="0" border="0" cellpadding="0" width="100%" align="center">
                                <tbody>
                                    <tr>
                                        <td>
                                            <table style="width:66.5%;" border="0" cellpadding="0" cellspacing="0"
                                                align="right" width="66.5%" class="section-details-table">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-size:17px; line-height:26px; color:#333333;"
                                                            valign="top" align="left" class="section-details-td">
                                                            <table style="width:100%; min-width:100%;" border="0"
                                                                cellpadding="0" cellspacing="0" align="center"
                                                                width="100%">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="height:30px; font-size:30px; line-height:30px; min-width:100%;"
                                                                            align="left" height="30" valign="top"
                                                                            class="gap-21"><img
                                                                                data-unique-identifier="" width="1"
                                                                                height="30" border="0"
                                                                                style="display:block; outline:none;"
                                                                                alt="" class="gap-21"
                                                                                src="https://email.images.apple.com/dm/groups/aos/om/global/cmon/spacer.gif">
                                                                        </td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td style="min-width:100%;" align="left"
                                                                            height="1" bgcolor="D6D6D6" valign="top"
                                                                            class="moe-line-col">
                                                                            <div
                                                                                style="background-color:D6D6D6; font-size:1px !important; height:1px !important;">
                                                                            </div>
                                                                        </td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td style="height:30px; font-size:30px; line-height:30px; min-width:100%;"
                                                                            align="left" height="30" valign="top"
                                                                            class="gap-32"><img
                                                                                data-unique-identifier="" width="1"
                                                                                height="30" border="0"
                                                                                style="display:block; outline:none;"
                                                                                alt="" class="gap-32"
                                                                                src="https://email.images.apple.com/dm/groups/aos/om/global/cmon/spacer.gif">
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                            <h3 style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-weight:600; letter-spacing:0px; font-size:17px; line-height:26px; color:#333333; margin-top:0px; margin-bottom:0px;"
                                                                class="subsec-heading">
                                                                Shipping Address:
                                                            </h3>
                                                            <div style="width:100%; font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-size:17px; line-height:26px; color:#333333;"
                                                                class="gen-txt">
                                                                {user_inputs[5]}
                                                            </div>
                                                            <div style="width:100%; font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-size:17px; line-height:26px; color:#333333;"
                                                                class="gen-txt">
                                                            </div>
                                                            <div style="width:100%; font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-size:17px; line-height:26px; color:#333333;"
                                                                class="gen-txt">
                                                                {user_inputs[6]}
                                                            </div>
                                                            <div style="width:100%; font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-size:17px; line-height:26px; color:#333333;"
                                                                class="gen-txt">
                                                                {user_inputs[7]}
                                                            </div>
                                                            <div style="width:100%; font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-size:17px; line-height:26px; color:#333333;"
                                                                class="gen-txt">
                                                                {user_inputs[8]}
                                                            </div>
                                                            <div style="width:100%; font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-size:17px; line-height:26px; color:#333333;"
                                                                class="gen-txt">
                                                                {user_inputs[9]}
                                                            </div>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table style="width:100%; min-width:100%;" border="0" cellpadding="0" cellspacing="0"
                                align="center" width="100%">
                                <tbody>
                                    <tr>
                                        <td style="height:41px; font-size:41px; line-height:41px; min-width:100%;"
                                            align="left" height="41" valign="top" class="gap-40"><img
                                                data-unique-identifier="" width="1" height="41" border="0"
                                                style="display:block; outline:none;" alt="" class="gap-40"
                                                src="https://email.images.apple.com/dm/groups/aos/om/global/cmon/spacer.gif">
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="min-width:100%;" align="left" height="1" bgcolor="D6D6D6"
                                            valign="top" class="moe-line-col">
                                            <div
                                                style="background-color:D6D6D6; font-size:1px !important; height:1px !important;">
                                            </div>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="height:1px; font-size:1px; line-height:1px; min-width:100%;"
                                            align="left" height="1" valign="top" class="gap-1"><img
                                                data-unique-identifier="" width="1" height="1" border="0"
                                                style="display:block; outline:none;" alt="" class="gap-1"
                                                src="https://email.images.apple.com/dm/groups/aos/om/global/cmon/spacer.gif">
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                        </tr>
                        <tr>
                        <td style="padding-top:43px; padding-bottom:32px;" class="payment-section-td">
                            <table style="width:29%;" border="0" cellpadding="0" cellspacing="0" align="left"
                                class="section-heading-table" width="29%">
                                <tbody>
                                    <tr>
                                        <td style="font-family:'SF UI Display Medium',system,-apple-system,-webkit-system-font,'SFNSText','Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif;; font-weight:500; letter-spacing:0px; color:#333333; font-size:22px; line-height:27px; margin-top:0; margin-left:0; margin-right:0; margin-bottom:0;"
                                            align="left" valign="top" class="section-items-heading-td">
                                            <h2 style="font-family:'SF UI Display Medium',system,-apple-system,-webkit-system-font,'SFNSText','Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif;; font-weight:500; letter-spacing:0px; color:#333333; font-size:22px; line-height:27px; margin-top:0; margin-left:0; margin-right:0; margin-bottom:0;"
                                                class="sectionHeading">Billing and Payment</h2>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table style="width:66.5%;" border="0" cellpadding="0" cellspacing="0" align="right"
                                width="66.5%" class="section-details-table">
                                <tbody>
                                    <tr>
                                        <td style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-size:17px; line-height:26px; color:#333333;"
                                            valign="top" align="left" class="section-details-td">
                                            <h3 style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-weight:600; letter-spacing:0px; font-size:17px; line-height:26px; color:#333333; margin-top:0px; margin-bottom:0px;"
                                                class="subsec-heading">Bill To:</h3>
                                            <div style="width:100%; font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-size:17px; line-height:26px; color:#333333;"
                                                class="gen-txt">
                                                <div style="width:100%;">
                                                    {user_inputs[5]}
                                                </div>
                                                <div style="width:100%;"> </div>
                                                <div style="width:100%; word-wrap:break-word;">
                                                    <span class="moe-break-me">{user_inputs[10]}</span>
                                                </div>
                                            </div>
                                            <h3 style="padding-top:23px; font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-weight:600; letter-spacing:0px; font-size:17px; line-height:26px; color:#333333; margin-top:0px; margin-bottom:0px;"
                                                class="subsec-heading">Billing Address:</h3>
                                            <div style="width:100%; font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-size:17px; line-height:26px; color:#333333;"
                                                class="gen-txt">
                                                <div style="width:100%">{user_inputs[6]}</div>
                                                <div style="width:100%">{user_inputs[7]}</div>
                                                <div style="width:100%">{user_inputs[8]}</div>
                                                <div style="width:100%">{user_inputs[9]}</div>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                        </tr>
                        <tr>
                        <td style="padding-bottom:42px;" align="center" class="amts-section-td">
                            <table style="width:66.5%;" border="0" cellpadding="0" cellspacing="0" align="right"
                                width="66.5%" class="amt-row-table">
                                <tbody>
                                    <tr>
                                        <td align="center">
                                            <table style="width:100%; min-width:100%;" border="0" cellpadding="0"
                                                cellspacing="0" align="center" width="100%">
                                                <tbody>
                                                    <tr>
                                                        <td style="height:1px; font-size:1px; line-height:1px; min-width:100%;"
                                                            align="left" height="1" valign="top" class="gap-1">
                                                            <img data-unique-identifier="" width="1" height="1"
                                                                border="0" style="display:block; outline:none;"
                                                                alt="" class="gap-1"
                                                                src="https://email.images.apple.com/dm/groups/aos/om/global/cmon/spacer.gif">
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="min-width:100%;" align="left" height="1"
                                                            bgcolor="D6D6D6" valign="top" class="moe-line-col">
                                                            <div
                                                                style="background-color:D6D6D6; font-size:1px !important; height:1px !important;">
                                                            </div>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="height:18px; font-size:18px; line-height:18px; min-width:100%;"
                                                            align="left" height="18" valign="top" class="gap-15">
                                                            <img data-unique-identifier="" width="1" height="18"
                                                                border="0" style="display:block; outline:none;"
                                                                alt="" class="gap-15"
                                                                src="https://email.images.apple.com/dm/groups/aos/om/global/cmon/spacer.gif">
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="width:100%; padding-top:4px;" class="amt-row-td">
                                            <table border="0" cellpadding="0" cellspacing="0" align="left"
                                                width="49%" class="amt-label-table">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; color:#333333; font-size:17px; line-height:24px;"
                                                            valign="top" align="left" class="amt-label-td">
                                                            Bag Subtotal
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                            <table border="0" cellpadding="0" cellspacing="0" align="right"
                                                width="49%" class="amt-value-table">
                                                <tbody>
                                                    <tr>
                                                        <td nowrap=""
                                                            style="white-space:nowrap; font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; color:#333333; font-size:17px; line-height:24px;"
                                                            valign="top" align="right" class="amt-value-td">
                                                            <nobr>{user_inputs[12]}{user_inputs[3]}</nobr>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="width:100%; padding-top:4px;" class="amt-row-td">
                                            <table border="0" cellpadding="0" cellspacing="0" align="left"
                                                width="49%" class="amt-label-table">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; color:#339900; font-size:17px; line-height:24px;"
                                                            valign="top" align="left" class="amt-label-td">
                                                            Delivery
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                            <table border="0" cellpadding="0" cellspacing="0" align="right"
                                                width="49%" class="amt-value-table">
                                                <tbody>
                                                    <tr>
                                                        <td nowrap=""
                                                            style="white-space:nowrap; font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; color:#339900; font-size:17px; line-height:24px;"
                                                            valign="top" align="right" class="amt-value-td">
                                                            <nobr>{user_inputs[12]}0.00</nobr>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="width:100%;" class="amt-row-td">
                                            <table style="margin-top:11px;" border="0" cellpadding="0"
                                                cellspacing="0" align="right" width="100%"
                                                class="amt-divider-table">
                                                <tbody>
                                                    <tr>
                                                        <td style="background-color:#D6D6D6;" height="1"
                                                            bgcolor="D6D6D6" valign="top" align="left"
                                                            class="amt-divider"></td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="width:100%; padding-top:4px;" class="amt-row-td">
                                            <table border="0" cellpadding="0" cellspacing="0" align="left"
                                                width="49%" class="amt-label-table">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; color:#333333; font-size:17px; line-height:24px; font-weight:600;"
                                                            valign="top" align="left" class="amt-label-td">
                                                            Order Total
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                            <table border="0" cellpadding="0" cellspacing="0" align="right"
                                                width="49%" class="amt-value-table">
                                                <tbody>
                                                    <tr>
                                                        <td nowrap=""
                                                            style="white-space:nowrap; font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; color:#333333; font-size:17px; line-height:24px; font-weight:600;"
                                                            valign="top" align="right" class="amt-value-td">
                                                            <nobr>{user_inputs[12]}{user_inputs[4]}</nobr>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding-top:16px; font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; color:#666666; font-size:14px; line-height:21px;"
                                            valign="top" align="left" class="note-td"> Your invoice will be sent
                                            via email 2–3 business days after receipt of your order.</td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                        </tr>
                        <tr>
                        <td>
                            <table style="width:100%; min-width:100%;" border="0" cellpadding="0" cellspacing="0"
                                align="center" width="100%">
                                <tbody>
                                    <tr>
                                        <td style="height:1px; font-size:1px; line-height:1px; min-width:100%;"
                                            align="left" height="1" valign="top" class="gap-20"><img
                                                data-unique-identifier="" width="1" height="1" border="0"
                                                style="display:block; outline:none;" alt="" class="gap-20"
                                                src="https://email.images.apple.com/dm/groups/aos/om/global/cmon/spacer.gif">
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="min-width:100%;" align="left" height="1" bgcolor="D6D6D6"
                                            valign="top" class="moe-line-col">
                                            <div
                                                style="background-color:D6D6D6; font-size:1px !important; height:1px !important;">
                                            </div>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="height:43px; font-size:43px; line-height:43px; min-width:100%;"
                                            align="left" height="43" valign="top" class="gap-39"><img
                                                data-unique-identifier="" width="1" height="43" border="0"
                                                style="display:block; outline:none;" alt="" class="gap-39"
                                                src="https://email.images.apple.com/dm/groups/aos/om/global/cmon/spacer.gif">
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table style="padding-bottom:18px;" border="0" cellpadding="0" cellspacing="0"
                                width="100%" class="qa-table">
                                <tbody>
                                    <tr>
                                        <td>
                                            <table style="width:29%;" border="0" cellpadding="0" cellspacing="0"
                                                align="left" class="section-heading-table" width="29%">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-family:'SF UI Display Medium',system,-apple-system,-webkit-system-font,'SFNSText','Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif;; font-weight:500; letter-spacing:0px; color:#333333; font-size:22px; line-height:27px; margin-top:0; margin-left:0; margin-right:0; margin-bottom:0;"
                                                            align="left" valign="top"
                                                            class="section-items-heading-td">
                                                            <h2 style="font-family:'SF UI Display Medium',system,-apple-system,-webkit-system-font,'SFNSText','Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif;; font-weight:500; letter-spacing:0px; color:#333333; font-size:22px; line-height:27px; margin-top:0; margin-left:0; margin-right:0; margin-bottom:0;"
                                                                class="sectionHeading">Questions</h2>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                            <table style="width:66.5%;" border="0" cellpadding="0" cellspacing="0"
                                                align="right" width="66.5%" class="answers-table">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-size:17px; line-height:26px; color:#333333;"
                                                            align="left" valign="top" class="answers-td">
                                                            <h3 style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-weight:600; letter-spacing:0px; font-size:17px; line-height:26px; color:#333333; margin-top:0px; margin-bottom:0px; margin-left:0; margin-right:0;"
                                                                class="answer-h3">When will I get my items?</h3>
                                                            <div style="padding-bottom:23px;" class="answer-para">
                                                                There is a ‘Delivers’ estimate above each item.
                                                                This tells you when your items are expected to
                                                                arrive. Once your items have dispatched, you
                                                                will receive a Dispatch Notification email with
                                                                a delivery reference number. You can also visit
                                                                online <a class="aapl-link" style="color:#0070C9"
                                                                    rel="noreferrer nofollow noopener"
                                                                    target="_blank">Order Status</a> to view the
                                                                most up-to-date status of your order.
                                                                <div style="padding-top:12px;">If you ordered
                                                                    multiple items and have chosen to receive
                                                                    separate shipments, you’ll receive a
                                                                    separate email as each item ships.</div>
                                                            </div>
                                                            <h3 style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-weight:600; letter-spacing:0px; font-size:17px; line-height:26px; color:#333333; margin-top:0px; margin-bottom:0px; margin-left:0; margin-right:0;"
                                                                class="answer-h3">How do I view or change my
                                                                order?</h3>
                                                            <div style="padding-bottom:23px;" class="answer-para">
                                                                Go to <a style="color:#0070C9"
                                                                    rel="noreferrer nofollow noopener"
                                                                    target="_blank">Order Status</a>, then sign
                                                                in to add your order to your Apple ID. You can
                                                                make changes to, return, or cancel eligible
                                                                items there. To learn more about shipping,
                                                                changing, or returning orders, please visit the
                                                                <a class="aapl-link" style="color:#0085cf"
                                                                    href="https://store.apple.com/uk/help/"
                                                                    rel="noreferrer nofollow noopener"
                                                                    target="_blank"> Help</a> page.
                                                                <div style="padding-top:12px;">
                                                                    You can also call Apple Store Customer
                                                                    Service on
                                                                    <nobr>0800 048 0408</nobr>
                                                                    (freephone), Monday–Friday 08:00–20:00,
                                                                    Saturday–Sunday 09:00–18:00. Please have
                                                                    your Order Number available.
                                                                </div>
                                                            </div>
                                                            <h3 style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-weight:600; letter-spacing:0px; font-size:17px; line-height:26px; color:#333333; margin-top:0px; margin-bottom:0px; margin-left:0; margin-right:0;"
                                                                class="answer-h3-faq">
                                                                Recycling Options.
                                                            </h3>
                                                            <div
                                                                style="padding-bottom:23px; font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-size:17px; line-height:26px; color:#333333;">
                                                                You can drop off old devices at an Apple Store
                                                                or local collection point for recycling. <a
                                                                    class="aapl-link" style="color:#0070C9"
                                                                    aria-label="Learn more about other ways to recycle"
                                                                    target="_blank"
                                                                    href="https://www.apple.com/uk/trade-in/"
                                                                    rel="noreferrer nofollow noopener">Learn
                                                                    More ›</a></div>
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
                        style="margin:0; padding-top:19px; padding-bottom:13px; background-color:#F2F2F2; margin-bottom:0px;"
                        border="0" cellpadding="0" bgcolor="F2F2F2" cellspacing="0" align="center" width="100%"
                        class="footer-container-table">
                        <tbody>
                        <tr>
                        <td align="center">
                            <table border="0" cellpadding="0" cellspacing="0" width="660" bgcolor="F2F2F2"
                                align="center" class="footer-section-table">
                                <tbody>
                                    <tr>
                                        <td style="padding-left:16px; padding-right:16px;"
                                            class="footer-copyright-td">
                                            <table
                                                style="padding-bottom:14px; border-bottom-color:#D6D6D6; border-bottom-width:1px; border-bottom-style:solid;"
                                                border="0" cellpadding="0" cellspacing="0" align="center"
                                                width="100%" class="footer-menu-table">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; color:#888888; font-size:12px; line-height:18px;"
                                                            align="center" valign="top" class="footer-menu-td-top">
                                                            <table style="display: inline-table;" border="0"
                                                                cellpadding="0" cellspacing="0" width="auto"
                                                                class="footer-menu-item-table">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; color:#888888; font-size:12px; line-height:18px;"
                                                                            class="footer-menu-item-td">
                                                                            <a color="#888888" style="color:#888888"
                                                                                href="https://store.apple.com/uk"
                                                                                rel="noreferrer nofollow noopener"
                                                                                target="_blank">Shop
                                                                                Online</a><span
                                                                                style="color:#D6D6D6;"
                                                                                color="#D6D6D6" aria-hidden="true"
                                                                                class="hide-line">&nbsp;&nbsp;|&nbsp;&nbsp;</span>
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                            <table style="display: inline-table;" border="0"
                                                                cellpadding="0" cellspacing="0" width="auto"
                                                                class="footer-menu-item-table">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; color:#888888; font-size:12px; line-height:18px;"
                                                                            class="footer-menu-item-td">
                                                                            <a color="#888888" style="color:#888888"
                                                                                href="https://www.apple.com/uk/retail/"
                                                                                rel="noreferrer nofollow noopener"
                                                                                target="_blank">Find a
                                                                                Store</a><span
                                                                                style="color:#D6D6D6;"
                                                                                color="#D6D6D6" aria-hidden="true"
                                                                                class="hide-line">&nbsp;&nbsp;|&nbsp;&nbsp;</span>
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                            <table style="display: inline-table;" border="0"
                                                                cellpadding="0" cellspacing="0" width="auto"
                                                                class="footer-menu-item-table">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; color:#888888; font-size:12px; line-height:18px;"
                                                                            class="footer-menu-item-td">
                                                                            <span
                                                                                style="white-space:nowrap; color:#888888;"
                                                                                class="footer-menu-phone">0800
                                                                                048 0408</span>
                                                                            <span style="color:#D6D6D6;"
                                                                                color="#D6D6D6" aria-hidden="true"
                                                                                class="hide-line">&nbsp;&nbsp;|&nbsp;&nbsp;</span>
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                            <table style="display: inline-table;" border="0"
                                                                cellpadding="0" cellspacing="0" width="auto"
                                                                class="footer-menu-item-table">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; color:#888888; font-size:12px; line-height:18px;"
                                                                            class="footer-menu-item-td">
                                                                            <a color="#888888" style="color:#888888"
                                                                                href="https://store.apple.com/us/go/app"
                                                                                rel="noreferrer nofollow noopener"
                                                                                target="_blank">Get the Apple
                                                                                Store App</a>
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
                                        <td style="padding-left:16px; padding-right:16px;"
                                            class="footer-copyright-td">
                                            <div
                                                style="width:100%; padding-top:20px; font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; color:#888888; font-size:11px; line-height:16px;">
                                                Apple Distribution International Ltd., Hollyhill Industrial
                                                Estate, Hollyhill, Cork, Republic of Ireland.
                                            </div>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding-left:16px; padding-right:16px; font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; color:#888888; font-size:11px; line-height:16px;"
                                            valign="top" align="left" class="footer-copyright-td">
                                            <div style="padding-top:19px;" class="footer-copyright-div">
                                                Copyright © 2025&nbsp;<a
                                                    style="text-decoration:none !important; color:#888888 !important;"
                                                    color="#888888" rel="noopener noreferrer" target="_blank">Apple
                                                    Inc.</a> All rights reserved.
                                            </div>
                                            <div style="padding-top:16px; font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; font-size:11px; line-height:16px;"
                                                class="footer-links-div">
                                                <a style="color:#555555;" target="_blank"
                                                    href="https://www.apple.com/uk/legal/terms/site.html"
                                                    class="footer-links-a" rel="noreferrer nofollow noopener">
                                                    <nobr>Terms of Use</nobr>
                                                </a>
                                                &nbsp; <span aria-hidden="true" color="#D6D6D6">|</span>
                                                &nbsp;
                                                <a style="color:#555555;" target="_blank"
                                                    href="https://www.apple.com/uk/privacy/" class="footer-links-a"
                                                    rel="noreferrer nofollow noopener">
                                                    <nobr>Privacy Policy</nobr>
                                                </a>
                                                &nbsp; <span aria-hidden="true" color="#D6D6D6">|</span>
                                                &nbsp;
                                                <a style="color:#555555;" target="_blank"
                                                    href="https://www.apple.com/uk/shop/browse/open/salespolicies"
                                                    class="footer-links-a" rel="noreferrer nofollow noopener">
                                                    <nobr>Sales and Refunds</nobr>
                                                </a>
                                            </div>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding-left:16px; padding-right:16px; padding-top:10px; font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; color:#6f6f6f; font-size:11px; line-height:16px;"
                                            align="left" class="moe-hide">
                                            <div
                                                style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; color:#888888; font-size:11px; line-height:16px; padding-bottom:5px; padding-top:5px;">
                                                <div style="padding-bottom:5px;"><strong>Apple One (1) Year
                                                        Limited Warranty – (UK and Ireland)</strong></div>
                                                <div><strong>For Apple Branded Products Only</strong></div>
                                            </div>
                                            <div
                                                style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; color:#888888; font-size:11px; line-height:16px;  padding-bottom:7px;font-weight:bold;">
                                                CONSUMER LAW
                                            </div>
                                            <div
                                                style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; color:#888888; font-size:11px; line-height:16px;">
                                                <strong>The Apple One-Year Limited Warranty is a voluntary
                                                    manufacturer’s warranty. It provides rights separate to
                                                    rights provided by consumer law, including but not limited
                                                    to those relating to non-conforming goods.</strong>
                                                <div style="padding-top:7px;">
                                                    <strong>As such, the Apple One-Year Limited warranty
                                                        benefits are in addition to, and not instead of, rights
                                                        provided by consumer law. </strong>
                                                </div>
                                                <div style="padding-top:7px;">
                                                    If a product is defective consumers may, in addition to any
                                                    other rights which they may have under consumer law in the
                                                    UK and Ireland, avail themselves of the rights contained in:
                                                </div>
                                                <div style="padding-top:7px;">
                                                    for products purchased in Ireland: the Sale of Goods Act,
                                                    1893 (in particular Sections 12, 13, 14 and 15), the Sale of
                                                    Goods and Supply of Services Act, 1980 and the European
                                                    Communities (Certain Aspects of the Sale of Consumer Goods
                                                    and Associated Guarantees) Regulations 2003 (S.I. No.
                                                    11/2003);
                                                </div>
                                                <div style="padding-top:7px;">
                                                    for products purchased in the UK: the Sale of Goods Act
                                                    1979.
                                                </div>
                                                <div style="padding-top:7px;">
                                                    <strong>Consumers have the right to choose whether to claim
                                                        service under the Apple One-Year Limited Warranty or
                                                        under their consumer law rights.</strong>
                                                </div>
                                                <div style="padding-top:7px;">
                                                    <strong>Important: The Apple One-Year Limited Warranty terms
                                                        and conditions shall not apply to consumer law
                                                        claims.</strong>
                                                </div>
                                                <div style="padding-top:7px;">
                                                    For further information about consumer law, please visit the
                                                    Apple website (<a class="aapl-link" style="color:#158CFB"
                                                        target="_blank"
                                                        href="https://www.apple.com/legal/warranty/statutoryrights.html"
                                                        rel="noreferrer nofollow noopener">https://www.apple.com/legal/warranty/statutoryrights.html</a>)
                                                    or contact your local consumer organisation.
                                                </div>
                                                <div
                                                    style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;; color:#888888; font-size:11px; line-height:16px;  padding-bottom:3px; padding-top:7px;font-weight:bold;">
                                                    WHAT IS COVERED BY THIS WARRANTY?
                                                </div>
                                                <div style="padding-top:7px;">
                                                    Apple Distribution International Ltd. of Hollyhill
                                                    Industrial Estate Hollyhill, Cork, Republic of Ireland (or
                                                    its successor in title) (<strong>“Apple”</strong>) warrants
                                                    the Apple-branded hardware product and Apple-branded
                                                    accessories contained in the original packaging
                                                    (<strong>“Apple Product“</strong>) against defects in
                                                    materials and workmanship when used in accordance with
                                                    Apple's user manuals, technical specifications and other
                                                    Apple Product published guidelines for a period of ONE (1)
                                                    YEAR from the date of original retail purchase by the
                                                    end-user purchaser (<strong>“Warranty Period“</strong>). You
                                                    will be able to receive the remedies available under the One
                                                    Year Limited Warranty for your Apple product via local Apple
                                                    service facilities in most parts of the world (please refer
                                                    to section “How to obtain warranty services“). In the event
                                                    of any defect in materials and workmanship, you will be able
                                                    to direct your claims to Apple even in situations where you
                                                    purchased the Apple Product from a third party.
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
                        </td>
                        </tr>
                        </tbody>
    """
    
    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
