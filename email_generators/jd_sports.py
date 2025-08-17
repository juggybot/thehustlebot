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
    msg['From'] = formataddr((f'JD Sports', sender_email))
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
    "Please enter the order date (03/01/25):",
    "Please enter the expected date (12/04):",
    "Please enter the delivery address (0839 Adams Mews):",
    "Please enter the customer name (Juggy Resells):",
    "Please enter the suburb (East Jeffreyhaven):",
    "Please enter the postcode (50769):",
    "Please enter the image url (jpg, jpeg, png):",
    "Please enter the product brand (Adidas):",
    "Please enter the product name (Originals Samba OG):",
    "Please enter the product size (9.5 US):",
    "Please enter the product price (WITHOUT THE $ SIGN):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira a data do pedido (01/03/25):",
    "Por favor, insira a data prevista (12/04):",
    "Por favor, insira o endereço de entrega (0839 Adams Mews):",
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira o bairro (East Jeffreyhaven):",
    "Por favor, insira o código postal (50769):",
    "Por favor, insira a URL da imagem (jpg, jpeg, png):",
    "Por favor, insira a marca do produto (Adidas):",
    "Por favor, insira o nome do produto (Originals Samba OG):",
    "Por favor, insira o tamanho do produto (9.5 US):",
    "Por favor, insira o preço do produto (SEM O SÍMBOLO $):",
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
    part1 = random.randint(100000000, 999999999)  # Random 8-digit number

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
    subject = f"Thanks For Your Order, It's Been Confirmed! ✔"

    # Format input into HTML template
    html_template = f"""
        <div style="margin: 0px; padding: 0px">
        <div style="width: 600px; max-width: 100%; margin: 0px auto; padding: 0px" class="m_8750190790095149799width100pc">
            <div>
                <table border="0" cellpadding="0" cellspacing="0" width="600" class="m_8750190790095149799width100pc">
                    <tbody>
                        <tr>
                            <td>
                                <table border="0" cellpadding="0" cellspacing="0" style="padding: 0px; vertical-align: top"
                                    width="100%">
                                    <tbody>
                                        <tr>
                                            <td align="center" style="
                            padding: 0px;
                            font-size: 11px;
                            text-transform: uppercase;
                            ">
                                                <a href="https://reporting.jdsports.co.uk/cgi-bin/rr/nobook:9410011,nosent:3187429,nosrep:59862479,nored:xwsrnePwTlhxG_C5j_Vc1HEtKDaSGrIc-bERlsx2uUU=/http://www.jdsports.co.uk/?utm_source=RedEye&amp;utm_medium=Email&amp;utm_campaign=&amp;utm_content=&amp;id_hash="
                                                    style="text-decoration: none" title="JD Sports" target="_blank"><img
                                                        alt="JD Sports" border="0"
                                                        src="https://reporting.jdsports.co.uk/images/180906/img_r1_c17.jpg"
                                                        style="display: block" width="80" /></a>
                                            </td>
                                            <td align="center" style="
                            padding: 0px;
                            font-size: 11px;
                            text-transform: uppercase;
                            ">
                                                <a href="https://reporting.jdsports.co.uk/cgi-bin/rr/nobook:9410012,nosent:3187429,nosrep:59862479,nored:xR5RaCYN0pHhkzdSlkfqqWHAmWpQ0YG95va2pB3ZKIm03kFjIdeJ3e2HtYax3fKh/https://www.jdsports.co.uk/men/?facet:new=latest&amp;utm_source=RedEye&amp;utm_medium=Email&amp;utm_campaign=&amp;utm_content=&amp;id_hash="
                                                    target="_blank"><img
                                                        src="https://jdsports-client-resources.co.uk/jdsports-client-resources/img/2022/0212/email/uk-header_02.jpg"
                                                        style="border: medium" width="100%" /></a>
                                            </td>
                                            <td align="center" style="
                            padding: 0px;
                            font-size: 11px;
                            text-transform: uppercase;
                            ">
                                                <a href="https://reporting.jdsports.co.uk/cgi-bin/rr/nobook:9410013,nosent:3187429,nosrep:59862479,nored:xR5RaCYN0pHhkzdSlkfqqRke3TmEu3jD5fOzY4wy4s2l28eEKatu_SK1ae0tW02E/https://www.jdsports.co.uk/women/?facet:new=latest&amp;utm_source=RedEye&amp;utm_medium=Email&amp;utm_campaign=&amp;utm_content=&amp;id_hash="
                                                    target="_blank"><img
                                                        src="https://jdsports-client-resources.co.uk/jdsports-client-resources/img/2022/0212/email/uk-header_03.jpg"
                                                        style="border: medium" width="100%" /></a>
                                            </td>
                                            <td align="center" style="
                            padding: 0px;
                            font-size: 11px;
                            text-transform: uppercase;
                            ">
                                                <a href="https://reporting.jdsports.co.uk/cgi-bin/rr/nobook:9410014,nosent:3187429,nosrep:59862479,nored:xR5RaCYN0pHhkzdSlkfqqYWqxi47vR6UDwwX3FbbGrxUqwbVvFpUtoC5ZPNmwXAD/https://www.jdsports.co.uk/kids/?facet:new=latest&amp;utm_source=RedEye&amp;utm_medium=Email&amp;utm_campaign=&amp;utm_content=&amp;id_hash="
                                                    target="_blank"><img
                                                        src="https://jdsports-client-resources.co.uk/jdsports-client-resources/img/2022/0212/email/uk-header_04.jpg"
                                                        style="border: medium" width="100%" /></a>
                                            </td>
                                            <td align="center" style="
                            padding: 0px;
                            font-size: 11px;
                            text-transform: uppercase;
                            ">
                                                <a href="https://reporting.jdsports.co.uk/cgi-bin/rr/nobook:9410015,nosent:3187429,nosrep:59862479,nored:xR5RaCYN0pHhkzdSlkfqqRfJ_hQ-moIgSLP6vw7PuZg=/https://www.jdsports.co.uk/brands/?utm_source=RedEye&amp;utm_medium=Email&amp;utm_campaign=&amp;utm_content=&amp;id_hash="
                                                    target="_blank"><img
                                                        src="https://jdsports-client-resources.co.uk/jdsports-client-resources/img/2022/0212/email/uk-header_05.jpg"
                                                        style="border: medium" width="100%" /></a>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td style="background: repeat rgb(0, 0, 0); padding: 45px 0px"
                                id="m_8750190790095149799spacing">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                    <tbody>
                                        <tr>
                                            <td style="width: 12%"></td>
                                            <td>
                                                <h1 style="color: rgb(255, 255, 255)">
                                                    YOUR ORDER CONFIRMATION
                                                </h1>
                                                <h4 style="color: rgb(255, 255, 255)">
                                                    Thanks for your order.
                                                </h4>
                                            </td>
                                            <td style="width: 12%" align="left" valign="bottom">
                                                <img src="https://jdsports-client-resources.co.uk/jdsports-client-resources/img/2020/1009/email/shopping-bag2.png"
                                                    style="
                                width: 60%;
                                display: block;
                                margin: 0px 10px 0px 0px;
                            " />
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <table width="100%" border="0" align="center" cellspacing="0" cellpadding="0" style="
                        font-family: Lato, Arial, sans-serif;
                        font-size: 12px;
                        line-height: 16px;
                        border-collapse: collapse;
                        color: rgb(0, 0, 0);
                    ">
                                    <tbody style="font-family: Lato, Arial, sans-serif">
                                        <tr style="font-family: Lato, Arial, sans-serif">
                                            <td style="
                            background: repeat rgb(242, 242, 242);
                            padding: 14px 0px;
                            font-family: Lato, Arial, sans-serif;
                            ">
                                                <table border="0" cellpadding="0" cellspacing="0" width="100%"
                                                    style="font-family: Lato, Arial, sans-serif">
                                                    <tbody style="font-family: Lato, Arial, sans-serif">
                                                        <tr style="font-family: Lato, Arial, sans-serif">
                                                            <td style="
                                    width: 8%;
                                    font-family: Lato, Arial, sans-serif;
                                    "></td>
                                                            <td style="font-family: Lato, Arial, sans-serif">
                                                                <div style="font-family: Lato, Arial, sans-serif">
                                                                    YOUR ORDER NUMBER:
                                                                    <span
                                                                        style="font-family: Lato, Arial, sans-serif">{order_num}</span>
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
                            <td style="
                    background: repeat rgb(255, 255, 255);
                    text-align: left;
                    padding: 40px 0px 0px;
                    ">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                    <tbody>
                                        <tr>
                                            <td style="width: 12%"></td>
                                            <td>
                                                <div class="m_8750190790095149799normaltext">
                                                    <p>
                                                        Hey {user_inputs[0]},<br /><br />
                                                        Thanks for shopping with us, Your order has been
                                                        confirmed! Once it’s been dispatched, we&#39;ll send
                                                        you another email so you know it’s on the way. If you
                                                        have placed an order to be delivered to store, we will
                                                        let you know once its arrived. Please don’t travel to
                                                        store before you’ve received an email or a text to say
                                                        it’s ready to collect.
                                                    </p>
                                                    <p>
                                                        If there&#39;s any issues we&#39;ll let you know
                                                        ASAP<br /><br />
                                                        Please note that if purchasing more than one item then
                                                        your order may be split into separate deliveries.
                                                    </p>
                                                    <p>
                                                        Track your parcel
                                                        <a href="https://reporting.jdsports.co.uk/cgi-bin/rr/nobook:9410016,nosent:3187429,nosrep:59862479,nored:xwsrnePwTlhxG_C5j_Vc1C0SUSNnJ9pCXMXSQNT6LH0=/http://www.jdsports.co.uk/track-my-order?utm_source=RedEye&amp;utm_medium=Email&amp;utm_campaign=API_Transactional&amp;utm_content=transorderconfuk&amp;id_hash="
                                                            style="text-decoration: underline"
                                                            target="_blank">here</a><br /><br />
                                                        One or more items in your order may be delivered
                                                        direct from the brand.
                                                    </p>
                                                    <p></p>
                                                    <p>
                                                        Not quite right? Return your order online or instore.
                                                        <u><a href="https://reporting.jdsports.co.uk/cgi-bin/rr/nobook:9410017,nosent:3187429,nosrep:59862479,nored:xR5RaCYN0pHhkzdSlkfqqTy4qnE71StR3j3i3n-jtl9Toh3_Fy-WXaXCB0duoE_5/https://www.jdsports.co.uk/page/delivery-returns?utm_source=RedEye&amp;utm_medium=Email&amp;utm_campaign=API_Transactional&amp;utm_content=transorderconfuk&amp;id_hash="
                                                                target="_blank">Find out more</a></u>
                                                    </p>
                                                    <p></p>
                                                    <p></p>
                                                </div>
                                            </td>
                                            <td style="width: 12%"></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>

                        <tr>
                            <td style="
                    background: repeat rgb(255, 255, 255);
                    text-align: left;
                    padding: 20px 0px 10px;
                    ">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                    <tbody>
                                        <tr>
                                            <td style="width: 12%"></td>
                                            <td>
                                                <table style="
                                width: 100%;
                                border-spacing: 0px;
                                table-layout: fixed;
                                border-collapse: collapse;
                            " cellpadding="0" cellspacing="0">
                                                    <tbody>
                                                        <tr>
                                                            <td style="
                                    border: 2px solid rgb(183, 183, 183);
                                    width: 50%;
                                    padding: 20px;
                                    margin: 0px;
                                    vertical-align: top;
                                    " align="top" class="m_8750190790095149799responsive-td">
                                                                <h5 style="
                                        font-weight: normal;
                                        min-height: 20px;
                                        margin-bottom: 10px;
                                        color: rgb(0, 0, 0);
                                    ">
                                                                    When?
                                                                </h5>
                                                                <h5 style="
                                        line-height: 22px;
                                        margin: 0px;
                                        padding: 0px;
                                        font-weight: normal;
                                        color: rgb(0, 0, 0);
                                    ">
                                                                    Next Day Delivery - EVRi<br />
                                                                    Ordered: {user_inputs[1]}<br />Expected on
                                                                    or after
                                                                    {user_inputs[2]}
                                                                </h5>
                                                            </td>
                                                            <td style="width: 3%"></td>
                                                            <td style="
                                    border: 2px solid rgb(183, 183, 183);
                                    width: 50%;
                                    padding: 20px;
                                    margin: 0px;
                                    vertical-align: top;
                                    " align="top" class="m_8750190790095149799responsive-td">
                                                                <h5 style="
                                        font-weight: normal;
                                        min-height: 20px;
                                        margin-bottom: 10px;
                                        color: rgb(0, 0, 0);
                                    ">
                                                                    Delivery Address
                                                                </h5>
                                                                <h5 style="
                                        line-height: 22px;
                                        margin: 0px;
                                        padding: 0px;
                                        font-weight: normal;
                                        color: rgb(0, 0, 0);
                                    " dir="auto">
                                                                    {user_inputs[3]}
                                                                    <br />{user_inputs[4]}
                                                                    <br />{user_inputs[5]}
                                                                </h5>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                            <td style="width: 12%"></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>

                        <tr>
                            <td style="
                    background: repeat rgb(255, 255, 255);
                    text-align: left;
                    padding: 0px 0px 10px;
                    ">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                    <tbody>
                                        <tr>
                                            <td style="width: 12%"></td>
                                            <td>
                                                <table border="0" cellpadding="0" cellspacing="0" width="100%"
                                                    style="background: repeat rgb(0, 0, 0)">
                                                    <tbody>
                                                        <tr>
                                                            <td style="
                                    padding: 10px 20px;
                                    margin: 0px;
                                    vertical-align: top;
                                    color: rgb(255, 255, 255);
                                    " align="top"></td>
                                                        </tr>
                                                        <tr>
                                                            <td style="
                                    padding: 10px 20px;
                                    margin: 0px;
                                    vertical-align: top;
                                    color: rgb(255, 255, 255);
                                    " align="top">
                                                                Payment Method
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td style="
                                    padding: 10px 20px;
                                    margin: 0px;
                                    vertical-align: top;
                                    color: rgb(255, 255, 255);
                                    " align="top">
                                                                APPLE PAY<br />
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td style="
                                    padding: 10px 20px;
                                    margin: 0px;
                                    vertical-align: top;
                                    color: rgb(255, 255, 255);
                                    " align="top"></td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                            <td style="width: 12%"></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 20px 0px 10px; text-align: center">
                                <h2>YOUR ORDER SUMMARY</h2>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding-bottom: 10px">
                                <table id="m_8750190790095149799carousel_container" align="center" border="0"
                                    cellpadding="0" cellspacing="0" role="presentation" style="width: 600px">
                                    <tbody>
                                        <tr>
                                            <td align="center" valign="top">
                                                <input checked id="m_8750190790095149799webkitnocheck" name="webkit"
                                                    style="display: none; max-height: 0" type="checkbox" />

                                                <div>
                                                    <table width="100%" border="0" align="center" cellspacing="0"
                                                        cellpadding="0" style="
                                font-family: Arial, Helvetica, sans-serif;
                                font-size: 12px;
                                line-height: 16px;
                                border-collapse: collapse;
                                color: rgb(0, 0, 0);
                                ">
                                                        <tbody style="font-family: Arial, Helvetica, sans-serif">
                                                            <tr style="font-family: Arial, Helvetica, sans-serif">
                                                                <td id="m_8750190790095149799carousel_fallback" style="
                                        font-family: Arial, Helvetica, sans-serif;
                                    "></td>
                                                            </tr>
                                                            <tr style="font-family: Arial, Helvetica, sans-serif">
                                                                <td style="
                                        padding-top: 2px;
                                        font-size: 2px;
                                        line-height: 2px;
                                        font-family: Arial, Helvetica, sans-serif;
                                    "></td>
                                                            </tr>
                                                            <tr style="font-family: Arial, Helvetica, sans-serif">
                                                                <td align="center" style="
                                        font-family: Arial, Helvetica, sans-serif;
                                    ">
                                                                    <table align="center" bgcolor="#F2F2F2" border="0"
                                                                        cellpadding="0" cellspacing="0"
                                                                        class="m_8750190790095149799width100pc"
                                                                        role="presentation" style="
                                        font-family: GothamMedium, Arial, Helvetica,
                                            sans-serif;
                                        font-size: 13px;
                                        line-height: 20px;
                                        border-collapse: collapse;
                                        width: 600px;
                                        color: rgb(0, 0, 0);
                                        " width="600">
                                                                        <tbody style="
                                            font-family: GothamMedium, Arial,
                                            Helvetica, sans-serif;
                                        ">
                                                                            <tr style="
                                            font-family: GothamMedium, Arial,
                                                Helvetica, sans-serif;
                                            ">
                                                                                <td align="center" style="
                                                font-family: GothamMedium, Arial,
                                                Helvetica, sans-serif;
                                            ">
                                                                                    <table align="left" bgcolor="#F2F2F2"
                                                                                        border="0" cellpadding="0"
                                                                                        cellspacing="0"
                                                                                        class="m_8750190790095149799stack-column"
                                                                                        style="
                                                font-size: 13px;
                                                line-height: 18px;
                                                font-family: GothamMedium, Arial,
                                                    Helvetica, sans-serif;
                                                border-collapse: collapse;
                                                width: 300px;
                                                color: rgb(255, 255, 255);
                                                " width="300">
                                                                                        <tbody style="
                                                    font-family: GothamMedium, Arial,
                                                    Helvetica, sans-serif;
                                                ">
                                                                                            <tr style="
                                                    font-family: GothamMedium, Arial,
                                                        Helvetica, sans-serif;
                                                    ">
                                                                                                <td align="center"
                                                                                                    valign="top" style="
                                                        padding: 10px;
                                                        font-family: GothamMedium,
                                                        Arial, Helvetica, sans-serif;
                                                    ">
                                                                                                    <a href="https://reporting.jdsports.co.uk/cgi-bin/rr/nobook:9410018,nosent:3187429,nosrep:59862479,nored:ULKye1AUzGceVjHgbH_Brh807J-_xF81oooTjE2k4c0=/https://www.jdsports.co.uk/product/grey-nike-tech-fleece-joggers-junior/19574900/?utm_source=RedEye&amp;utm_medium=Email&amp;utm_campaign=API_Transactional&amp;utm_content=transorderconfuk&amp;id_hash="
                                                                                                        target="_blank"
                                                                                                        style="
                                                        font-family: GothamMedium,
                                                            Arial, Helvetica,
                                                            sans-serif;
                                                        "><img src="{user_inputs[6]}" style="
                                                            display: block;
                                                            font-family: GothamMedium,
                                                            Arial, Helvetica,
                                                            sans-serif;
                                                        " width="220" border="0" /></a>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>

                                                                                    <table align="left" bgcolor="#F2F2F2"
                                                                                        border="0" cellpadding="0"
                                                                                        cellspacing="0"
                                                                                        class="m_8750190790095149799stack-column"
                                                                                        role="presentation" style="
                                                font-size: 13px;
                                                line-height: 18px;
                                                font-family: GothamMedium, Arial,
                                                    Helvetica, sans-serif;
                                                border-collapse: collapse;
                                                width: 300px;
                                                color: rgb(0, 0, 0);
                                                " width="300">
                                                                                        <tbody style="
                                                    font-family: GothamMedium, Arial,
                                                    Helvetica, sans-serif;
                                                ">
                                                                                            <tr style="
                                                    font-family: GothamMedium, Arial,
                                                        Helvetica, sans-serif;
                                                    ">
                                                                                                <td align="left"
                                                                                                    class="m_8750190790095149799product"
                                                                                                    style="
                                                        font-family: GothamMedium,
                                                        Arial, Helvetica, sans-serif;
                                                        font-size: 14px;
                                                        line-height: 24px;
                                                        padding: 10px 15px 25px;
                                                        color: rgb(0, 0, 0);
                                                    ">
                                                                                                    {user_inputs[7]}
                                                                                                    <br />
                                                                                                    {user_inputs[8]}
                                                                                                    <br />
                                                                                                    Qty -
                                                                                                    1
                                                                                                    <br />
                                                                                                    Size - {user_inputs[9]}
                                                                                                </td>
                                                                                            </tr>

                                                                                            <tr style="
                                                    font-family: GothamMedium, Arial,
                                                        Helvetica, sans-serif;
                                                    ">
                                                                                                <td class="m_8750190790095149799product"
                                                                                                    align="left" style="
                                                        padding: 5px 15px 25px;
                                                        font-family: GothamMedium,
                                                        Arial, Helvetica, sans-serif;
                                                    ">
                                                                                                    <strong style="
                                                        font-family: GothamMedium,
                                                            Arial, Helvetica,
                                                            sans-serif;
                                                        ">{user_inputs[11]}{user_inputs[10]}</strong>
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
            </div>
        </div>
    </div>
    """

    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
