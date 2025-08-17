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
    msg['From'] = formataddr((f'Farfetch', sender_email))
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
    "Please enter the street address (123 Main Street):",
    "Please enter the suburb & city (Sydney, Sydney):",
    "Please enter the postcode (2000):",
    "Please enter the country (Australia):",
    "Please enter the image url (jpg, jpeg, png):",
    "Please enter the delivery dates (15/03 and 20/03)"
    "Please enter the product name (Apple AirPods Pro (2nd Generation)):",
    "Please enter the product colour (Black):",
    "Please enter the product size (EU 42):",
    "Please enter the product price (WITHOUT THE $ SIGN):",
    "Please enter the delivery cost (WITHOUT THE $ SIGN):",
    "Please enter the tax cost (WITHOUT THE $ SIGN):",
    "Please enter the order total (WITHOUT THE $ SIGN):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira o endereço (123 Main Street):",
    "Por favor, insira o bairro e cidade (Sydney, Sydney):",
    "Por favor, insira o código postal (2000):",
    "Por favor, insira o país (Austrália):",
    "Por favor, insira a URL da imagem (jpg, jpeg, png):",
    "Por favor, insira as datas de entrega (15/03 e 20/03):",
    "Por favor, insira o nome do produto (Apple AirPods Pro (2ª Geração)):",
    "Por favor, insira a cor do produto (Preto):",
    "Por favor, insira o tamanho do produto (EU 42):",
    "Por favor, insira o preço do produto (SEM O SINAL $):",
    "Por favor, insira o custo de entrega (SEM O SINAL $):",
    "Por favor, insira o valor do imposto (SEM O SINAL $):",
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
    recipient_email = f'{user_inputs[15]}'
    subject = f"Thanks for your order. Here's what you can expect now"

    # Format input into HTML template
    html_template = f"""
            <html>

        <head></head>

        <body>
            <div dir="ltr">
                <div width="100%"
                    style="width:100%;min-width:100%;margin:0;padding:0;box-sizing:border-box;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;Margin:0">
                    <table cellpadding="0" cellspacing="0" border="0" height="100%" width="100%"
                        class="m_8214844979060577330body"
                        style="border-spacing:0;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;height:100%;width:100%;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;border-collapse:collapse"
                        valign="top" align="left">
                        <tbody>
                            <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                valign="top" align="left">
                                <td align="center" valign="top"
                                    style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;text-align:center;margin:0 auto;Margin:0 auto;float:none">
                                    <center style="width:100%;min-width:576px">
                                        <table align="center" class="m_8214844979060577330container"
                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:center;width:576px;margin:0 auto;Margin:0 auto;float:none"
                                            width="576" valign="top">
                                            <tbody>
                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                    valign="top" align="left">
                                                    <td style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                        valign="top" align="left">
                                                        <table
                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                            width="100%" valign="top" align="left">
                                                            <tbody>
                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                    valign="top" align="left">
                                                                    <th class="m_8214844979060577330header m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:560px;padding-right:16px;padding-left:16px;padding-top:35px"
                                                                        valign="top" align="left">
                                                                        <table
                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                            width="100%" valign="top" align="left">
                                                                            <tbody>
                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                    valign="top" align="left">
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                        valign="top" align="left">
                                                                                        <div style="display:none">
                                                                                            YOU&#x2019;VE MADE A GREAT CHOICE
                                                                                            <span
                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0">
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C; &#x200C;
                                                                                                &#x200C; &#x200C;
                                                                                            </span>
                                                                                        </div>
                                                                                        <table
                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                            width="100%" valign="top"
                                                                                            align="left">
                                                                                            <tbody>
                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                    valign="top" align="left">
                                                                                                    <th class="m_8214844979060577330header-logo m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;height:90px;padding-bottom:0;margin:0 auto;width:100%;padding-left:0;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <center
                                                                                                                            style="width:100%;min-width:none">
                                                                                                                            <a href="https://email.farfetch.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTCQGzaeo8O8Rzcqudh3df5d4uoWKG1Sm6GduWo9n5RDols8rgzgH4O0fo8VXtpKX%3DYABWWAY&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmfJHJMslcpD7sCeaoatYQClSZZkef8ZkpbId1JXS24xc4gxON1asXDYOPfRX4tvRezTgJfy7CC-w.&amp;_di_=l0fsreriei95b6vp8dprdf0nua2lt61t5ejao6h93175svj8rlvg"
                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;color:#222222;text-decoration:underline;text-decoration-color:#222222"
                                                                                                                                target="_blank">
                                                                                                                                <img class="m_8214844979060577330global-logo"
                                                                                                                                    align="middle"
                                                                                                                                    src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/images_header/farfetch_logo_global_default@4x.png"
                                                                                                                                    width="286"
                                                                                                                                    height="80"
                                                                                                                                    alt="farfetch logo"
                                                                                                                                    style="outline:none;text-decoration:none;width:auto;max-width:100%;clear:both;display:block;border:none;margin:0 auto;Margin:0 auto;float:none;text-align:center">
                                                                                                                                <div
                                                                                                                                    style="display:none">

                                                                                                                                </div>
                                                                                                                                <div
                                                                                                                                    style="display:none">

                                                                                                                                </div>
                                                                                                                            </a>
                                                                                                                        </center>
                                                                                                                    </th>
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                        <table
                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                            width="100%" valign="top"
                                                                                            align="left">
                                                                                            <tbody>
                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                    valign="top" align="left">
                                                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-top:48px;padding-bottom:0;margin:0 auto;width:100%;padding-left:0;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <h1
                                                                                                                            style="margin:0;Margin:0;font-family:'NimbusSansExtD-Bold','Helvetica Neue Bold','Arial Bold',sans-serif;font-weight:700;font-size:26px;line-height:26px;text-transform:uppercase;text-align:center">
                                                                                                                            YOU&#x2019;VE
                                                                                                                            MADE
                                                                                                                            A
                                                                                                                            GREAT
                                                                                                                            CHOICE
                                                                                                                        </h1>
                                                                                                                    </th>
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                        <table
                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                            width="100%" valign="top"
                                                                                            align="left">
                                                                                            <tbody>
                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                    valign="top" align="left">
                                                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-top:24px;padding-bottom:0;margin:0 auto;width:100%;padding-left:0;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <p
                                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;text-align:center;direction:ltr">
                                                                                                                            Order
                                                                                                                            number:<span
                                                                                                                                style="font-size:16px;line-height:22px;margin:0;Margin:0;font-family:'FarfetchBasis-Bold','Helvetica Neue',Arial,sans-serif;font-weight:700;text-align:left">
                                                                                                                                {order_num}</span>
                                                                                                                        </p>
                                                                                                                    </th>
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                        <table
                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                            width="100%" valign="top"
                                                                                            align="left">
                                                                                            <tbody>
                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                    valign="top" align="left">
                                                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-top:12px;padding-bottom:0;margin:0 auto;width:100%;padding-left:0;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <p
                                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;text-align:center">
                                                                                                                            <a href="https://email.farfetch.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTCQGzaeo8O8Rzcqudh3df5d4uoWKG1Sm6GduWo9n5RDols8rgzgH4O0fo8VXtpKX%3DYABWWCY&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmfJHJMslcpD7sCeaoatYQClSZZkef8ZkpbId1JXS24xc4gxON1asXDYOPfRX4tvRezTgJfy7CC-w.&amp;_di_=fd9rsm5fhr8rvvhsdngd2ilrbnsispvjd4hs22orf16atkcg9mu0"
                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;color:#222222;text-decoration:underline;text-decoration-color:#222222"
                                                                                                                                target="_blank">View
                                                                                                                                account</a>
                                                                                                                        </p>
                                                                                                                    </th>
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                    </th>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </th>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <table align="center" class="m_8214844979060577330container"
                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:center;width:576px;margin:0 auto;Margin:0 auto;float:none"
                                            width="576" valign="top">
                                            <tbody>
                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                    valign="top" align="left">
                                                    <td style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                        valign="top" align="left">
                                                        <table
                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                            width="100%" valign="top" align="left">
                                                            <tbody>
                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                    valign="top" align="left">
                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;margin:0 auto;width:560px;padding-right:16px;padding-left:16px;padding-top:48px;padding-bottom:24px"
                                                                        valign="top" align="left">
                                                                        <table
                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                            width="100%" valign="top" align="left">
                                                                            <tbody>
                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                    valign="top" align="left">
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                        valign="top" align="left">
                                                                                        <p
                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px">
                                                                                            Hi {user_inputs[0]},
                                                                                        </p>
                                                                                        <br>
                                                                                        <p
                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px">
                                                                                            Thanks for shopping at
                                                                                            FARFETCH.<br><br>We've received your
                                                                                            order and will process it shortly,
                                                                                            this can take up to two business
                                                                                            days.
                                                                                        </p>
                                                                                        <br>
                                                                                        <p
                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px">
                                                                                            Once we've sent your order, you'll
                                                                                            receive an email with the tracking
                                                                                            number. If you've placed your order
                                                                                            using our F90 or Same Day delivery
                                                                                            services and have any questions,
                                                                                            please contact our Customer Service
                                                                                            team.
                                                                                        </p>
                                                                                        <br>
                                                                                        <p
                                                                                            style="font-size:16px;line-height:22px;margin:0;Margin:0;font-family:'FarfetchBasis-Bold','Helvetica Neue',Arial,sans-serif;font-weight:700;text-align:left">
                                                                                            Shopped items from multiple
                                                                                            locations?
                                                                                        </p>
                                                                                        <br>
                                                                                        <p
                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0">
                                                                                            We've got it covered. We'll confirm
                                                                                            when each item has been sent
                                                                                            &#x2014; you may receive more than
                                                                                            one package.
                                                                                        </p>
                                                                                        <br>
                                                                                        <p
                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px">
                                                                                            We hope you love your new find.</p>
                                                                                        <br>
                                                                                        <p
                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0">
                                                                                            FARFETCH</p>
                                                                                    </th>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </th>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <table align="center" class="m_8214844979060577330container"
                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:center;width:576px;margin:0 auto;Margin:0 auto;float:none"
                                            width="576" valign="top">
                                            <tbody>
                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                    valign="top" align="left">
                                                    <td style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                        valign="top" align="left">
                                                        <table
                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                            width="100%" valign="top" align="left">
                                                            <tbody>
                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                    valign="top" align="left">
                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;margin:0 auto;width:560px;padding-right:16px;padding-left:16px;padding-top:48px;padding-bottom:24px"
                                                                        valign="top" align="left">
                                                                        <table
                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                            width="100%" valign="top" align="left">
                                                                            <tbody>
                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                    valign="top" align="left">
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                        valign="top" align="left">
                                                                                        <h3
                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:19px;line-height:26px;Margin-bottom:24px;margin-bottom:24px">
                                                                                            Your delivery information
                                                                                        </h3>
                                                                                        <p
                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0">
                                                                                            {user_inputs[0]}
                                                                                            <br>{user_inputs[1]}
                                                                                            <br>{user_inputs[2]}
                                                                                            <br>{user_inputs[3]}
                                                                                            <br>{user_inputs[4]}
                                                                                            <br>
                                                                                        </p>
                                                                                    </th>
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                        valign="top" align="left"></th>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </th>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <table align="center" class="m_8214844979060577330container"
                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:center;width:576px;margin:0 auto;Margin:0 auto;float:none"
                                            width="576" valign="top">
                                            <tbody>
                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                    valign="top" align="left">
                                                    <td style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                        valign="top" align="left">
                                                        <table
                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                            width="100%" valign="top" align="left">
                                                            <tbody>
                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                    valign="top" align="left">
                                                                    <th class="m_8214844979060577330banner m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;margin:0 auto;width:560px;padding-right:16px;padding-left:16px;padding-top:24px;padding-bottom:24px"
                                                                        valign="top" align="left">
                                                                        <table
                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                            width="100%" valign="top" align="left">
                                                                            <tbody>
                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                    valign="top" align="left">
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                        valign="top" align="left">
                                                                                        <table
                                                                                            class="m_8214844979060577330title m_8214844979060577330collapse"
                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;padding-bottom:6px;display:table"
                                                                                            width="100%" valign="top"
                                                                                            align="left">
                                                                                            <tbody>
                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                    valign="top" align="left">
                                                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:100%;padding-left:0;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <img border="0"
                                                                                                                            src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/images_banners/IconClimateConciousLight@4x.png"
                                                                                                                            class="m_8214844979060577330light-mode-image"
                                                                                                                            width="20"
                                                                                                                            height="20"
                                                                                                                            alt="Positively Farfetch environment leaf icon"
                                                                                                                            style="outline:none;text-decoration:none;width:auto;max-width:100%;clear:both;display:block;float:left;text-align:left;Margin-right:6px;margin-right:6px">
                                                                                                                        <span
                                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;display:none">
                                                                                                                            <img border="0"
                                                                                                                                src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/images_banners/IconClimateConciousDark@4x.png"
                                                                                                                                width="20"
                                                                                                                                height="20"
                                                                                                                                class="m_8214844979060577330dark-mode-image"
                                                                                                                                alt="Delivery truck icon"
                                                                                                                                style="outline:none;text-decoration:none;width:auto;max-width:100%;clear:both;display:block;float:left;text-align:left;Margin-right:6px;margin-right:6px">
                                                                                                                        </span>
                                                                                                                        <span
                                                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Bold','Helvetica Neue',Arial,sans-serif;font-weight:700;text-align:left;font-size:16px;line-height:22px">
                                                                                                                            Positively
                                                                                                                            FARFETCH
                                                                                                                        </span>
                                                                                                                    </th>
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                        <table
                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                            width="100%" valign="top"
                                                                                            align="left">
                                                                                            <tbody>
                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                    valign="top" align="left">
                                                                                                    <th class="m_8214844979060577330body m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:100%;padding-left:0;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <p
                                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0">
                                                                                                                            We're
                                                                                                                            on a
                                                                                                                            mission
                                                                                                                            to
                                                                                                                            become
                                                                                                                            the
                                                                                                                            global
                                                                                                                            platform
                                                                                                                            for
                                                                                                                            good
                                                                                                                            in
                                                                                                                            luxury
                                                                                                                            fashion
                                                                                                                            &#x2013;
                                                                                                                            empowering
                                                                                                                            everyone
                                                                                                                            to
                                                                                                                            choose,
                                                                                                                            act
                                                                                                                            and
                                                                                                                            think
                                                                                                                            positively.
                                                                                                                            <a href="https://email.farfetch.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTCQGzaeo8O8Rzcqudh3df5d4uoWKG1Sm6GduWo9n5RDols8rgzgH4O0fo8VXtpKX%3DCAWTSYAY&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmfJHJMslcpD7sCeaoatYQClSZZkef8ZkpbId1JXS24xc4gxON1asXDYOPfRX4tvRezTgJfy7CC-w.&amp;_di_=22fdr8rlqvmt3ntviel3rn20hepi3pkcp19fk5envkfmjmuhuqe0"
                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;color:#222222;text-decoration:underline;text-decoration-color:#222222"
                                                                                                                                target="_blank">Discover
                                                                                                                                more
                                                                                                                                about
                                                                                                                                Positively
                                                                                                                                FARFETCH</a>
                                                                                                                        </p>
                                                                                                                    </th>
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                    </th>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </th>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <table align="center" class="m_8214844979060577330container"
                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:center;width:576px;margin:0 auto;Margin:0 auto;float:none"
                                            width="576" valign="top">
                                            <tbody>
                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                    valign="top" align="left">
                                                    <td style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                        valign="top" align="left">
                                                        <table
                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                            width="100%" valign="top" align="left">
                                                            <tbody>
                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                    valign="top" align="left">
                                                                    <th class="m_8214844979060577330order-items-container m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;margin:0 auto;width:560px;padding-right:16px;padding-left:16px;padding-top:48px;padding-bottom:24px"
                                                                        valign="top" align="left">
                                                                        <table
                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                            width="100%" valign="top" align="left">
                                                                            <tbody>
                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                    valign="top" align="left">
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                        valign="top" align="left">
                                                                                        <table
                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                            width="100%" valign="top"
                                                                                            align="left">
                                                                                            <tbody>
                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                    valign="top" align="left">
                                                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:100%;padding-left:0;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <h3
                                                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:19px;line-height:26px">
                                                                                                                            Your
                                                                                                                            order
                                                                                                                            summary
                                                                                                                        </h3>
                                                                                                                    </th>
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                        <table
                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                            width="100%" valign="top"
                                                                                            align="left">
                                                                                            <tbody>
                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                    valign="top" align="left">
                                                                                                    <th class="m_8214844979060577330small-4 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-right:8px;padding-bottom:0;margin:0 auto;width:33.33333%;padding-left:0;padding-top:24px"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <a href="{user_inputs[5]}"
                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;color:#222222;text-decoration:underline;text-decoration-color:#222222"
                                                                                                            target="_blank">
                                                                                                            <img src="1"
                                                                                                                width="92"
                                                                                                                height="110"
                                                                                                                style="outline:none;text-decoration:none;width:auto;max-width:100%;clear:both;display:block;border:none;margin:0 auto;Margin:0 auto;float:none;text-align:center">
                                                                                                        </a>
                                                                                                    </th>
                                                                                                    <th class="m_8214844979060577330item-content m_8214844979060577330small-7 m_8214844979060577330columns"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-right:8px;padding-bottom:0;padding-left:8px;vertical-align:bottom;margin:0 auto;width:58.33333%;padding-top:24px"
                                                                                                        valign="bottom"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;Margin-bottom:12px;margin-bottom:12px;padding:0;width:100%;display:table"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:100%;padding-left:0;padding-right:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <table
                                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                                            width="100%"
                                                                                                                            valign="top"
                                                                                                                            align="left">
                                                                                                                            <tbody>
                                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                                    valign="top"
                                                                                                                                    align="left">
                                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                                        valign="top"
                                                                                                                                        align="left">
                                                                                                                                        <p
                                                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0">
                                                                                                                                            Delivery
                                                                                                                                            between
                                                                                                                                            <span
                                                                                                                                                style="font-size:16px;line-height:22px;margin:0;Margin:0;font-family:'FarfetchBasis-Bold','Helvetica Neue',Arial,sans-serif;font-weight:700;text-align:left">{user_inputs[6]}</span>

                                                                                                                                        </p>
                                                                                                                                    </th>
                                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                                                                        valign="top"
                                                                                                                                        align="left">
                                                                                                                                    </th>
                                                                                                                                </tr>
                                                                                                                            </tbody>
                                                                                                                        </table>
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th class="m_8214844979060577330item-brand m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:100%;padding-left:0;padding-right:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <table
                                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                                            width="100%"
                                                                                                                            valign="top"
                                                                                                                            align="left">
                                                                                                                            <tbody>
                                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                                    valign="top"
                                                                                                                                    align="left">
                                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                                        valign="top"
                                                                                                                                        align="left">
                                                                                                                                        <p
                                                                                                                                            style="font-size:16px;line-height:22px;margin:0;Margin:0;font-family:'FarfetchBasis-Bold','Helvetica Neue',Arial,sans-serif;font-weight:700;text-align:left">
                                                                                                                                            {user_inputs[7]}
                                                                                                                                        </p>
                                                                                                                                    </th>
                                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                                                                        valign="top"
                                                                                                                                        align="left">
                                                                                                                                    </th>
                                                                                                                                </tr>
                                                                                                                            </tbody>
                                                                                                                        </table>
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:100%;padding-left:0;padding-right:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <table
                                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                                            width="100%"
                                                                                                                            valign="top"
                                                                                                                            align="left">
                                                                                                                            <tbody>
                                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                                    valign="top"
                                                                                                                                    align="left">
                                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                                        valign="top"
                                                                                                                                        align="left">
                                                                                                                                        <p
                                                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0">
                                                                                                                                            {user_inputs[8]}
                                                                                                                                        </p>
                                                                                                                                    </th>
                                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                                                                        valign="top"
                                                                                                                                        align="left">
                                                                                                                                    </th>
                                                                                                                                </tr>
                                                                                                                            </tbody>
                                                                                                                        </table>
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;Margin-bottom:12px;margin-bottom:12px;padding:0;width:100%;display:table"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:100%;padding-left:0;padding-right:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <table
                                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                                            width="100%"
                                                                                                                            valign="top"
                                                                                                                            align="left">
                                                                                                                            <tbody>
                                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                                    valign="top"
                                                                                                                                    align="left">
                                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                                        valign="top"
                                                                                                                                        align="left">
                                                                                                                                        <p
                                                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0">
                                                                                                                                            {user_inputs[9]}
                                                                                                                                        </p>
                                                                                                                                    </th>
                                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                                                                        valign="top"
                                                                                                                                        align="left">
                                                                                                                                    </th>
                                                                                                                                </tr>
                                                                                                                            </tbody>
                                                                                                                        </table>
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                    <th class="m_8214844979060577330item-price m_8214844979060577330small-12 m_8214844979060577330columns"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;padding-left:8px;vertical-align:bottom;margin:0 auto;width:100%;padding-right:0"
                                                                                                        valign="bottom"
                                                                                                        align="left">
                                                                                                        <p
                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;text-align:right;white-space:nowrap">
                                                                                                            {user_inputs[14]}{user_inputs[10]}</p>
                                                                                                    </th>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                        <table
                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                            width="100%" valign="top"
                                                                                            align="left">
                                                                                            <tbody>
                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                    valign="top" align="left">
                                                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:100%;padding-left:0;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <hr
                                                                                                                            style="border:0;padding:0;margin:0;Margin:0;border-top:1px solid #727272;color:#727272;background:#727272;Margin-top:24px;margin-top:24px">
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                    </th>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </th>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <table align="center" class="m_8214844979060577330container"
                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:center;width:576px;margin:0 auto;Margin:0 auto;float:none"
                                            width="576" valign="top">
                                            <tbody>
                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                    valign="top" align="left">
                                                    <td style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                        valign="top" align="left">
                                                        <table
                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                            width="100%" valign="top" align="left">
                                                            <tbody>
                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                    valign="top" align="left">
                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:560px;padding-right:16px;padding-left:16px"
                                                                        valign="top" align="left">
                                                                        <table
                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                            width="100%" valign="top" align="left">
                                                                            <tbody>
                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                    valign="top" align="left">
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                        valign="top" align="left">
                                                                                        <table
                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                            width="100%" valign="top"
                                                                                            align="left">
                                                                                            <tbody>
                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                    valign="top" align="left">
                                                                                                    <th class="m_8214844979060577330small-6 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-right:8px;padding-bottom:0;margin:0 auto;width:50%;padding-left:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <p
                                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;Margin-bottom:24px;margin-bottom:24px">
                                                                                                                            Sub-total
                                                                                                                        </p>
                                                                                                                        <p
                                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;Margin-bottom:12px;margin-bottom:12px">
                                                                                                                            Delivery
                                                                                                                        </p>
                                                                                                                        <p
                                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;Margin-bottom:12px;margin-bottom:12px">
                                                                                                                            Taxes
                                                                                                                        </p>
                                                                                                                        <p
                                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;Margin-bottom:12px;margin-bottom:12px">
                                                                                                                            Credit
                                                                                                                        </p>
                                                                                                                        <p
                                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0">
                                                                                                                            Promotions
                                                                                                                        </p>
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                    <th class="m_8214844979060577330small-6 m_8214844979060577330columns"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;padding-left:8px;margin:0 auto;width:50%;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <p
                                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;Margin-bottom:24px;margin-bottom:24px;text-align:right">
                                                                                                                            {user_inputs[14]}{user_inputs[10]}
                                                                                                                        </p>
                                                                                                                        <p
                                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;Margin-bottom:12px;margin-bottom:12px;text-align:right">
                                                                                                                            {user_inputs[14]}{user_inputs[11]}
                                                                                                                        </p>
                                                                                                                        <p
                                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;Margin-bottom:12px;margin-bottom:12px;text-align:right">
                                                                                                                            {user_inputs[14]}{user_inputs[12]}
                                                                                                                        </p>
                                                                                                                        <p
                                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;Margin-bottom:12px;margin-bottom:12px;text-align:right">
                                                                                                                            -
                                                                                                                            {user_inputs[14]}0.00
                                                                                                                        </p>
                                                                                                                        <p
                                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;text-align:right">
                                                                                                                            -
                                                                                                                            {user_inputs[14]}0.00
                                                                                                                        </p>
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                    </th>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </th>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                        <table
                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                            width="100%" valign="top" align="left">
                                                            <tbody>
                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                    valign="top" align="left">
                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:560px;padding-right:16px;padding-left:16px"
                                                                        valign="top" align="left">
                                                                        <table
                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                            width="100%" valign="top" align="left">
                                                                            <tbody>
                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                    valign="top" align="left">
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                        valign="top" align="left">
                                                                                        <hr
                                                                                            style="border:0;padding:0;margin:0;Margin:0;border-top:1px solid #727272;color:#727272;background:#727272;Margin-top:24px;margin-top:24px">
                                                                                    </th>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </th>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                        <table
                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                            width="100%" valign="top" align="left">
                                                            <tbody>
                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                    valign="top" align="left">
                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:560px;padding-right:16px;padding-left:16px"
                                                                        valign="top" align="left">
                                                                        <table
                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                            width="100%" valign="top" align="left">
                                                                            <tbody>
                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                    valign="top" align="left">
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                        valign="top" align="left">
                                                                                        <table
                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                            width="100%" valign="top"
                                                                                            align="left">
                                                                                            <tbody>
                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                    valign="top" align="left">
                                                                                                    <th class="m_8214844979060577330small-6 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-right:8px;padding-bottom:0;margin:0 auto;width:50%;padding-left:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <p
                                                                                                                            style="font-size:16px;line-height:22px;margin:0;Margin:0;font-family:'FarfetchBasis-Bold','Helvetica Neue',Arial,sans-serif;font-weight:700;text-align:left;Margin-bottom:12px;margin-bottom:12px;Margin-top:24px;margin-top:24px">
                                                                                                                            Total
                                                                                                                        </p>
                                                                                                                        <p
                                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;Margin-bottom:24px;margin-bottom:24px">
                                                                                                                            Payment
                                                                                                                            method
                                                                                                                        </p>
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                    <th class="m_8214844979060577330small-6 m_8214844979060577330columns"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;padding-left:8px;margin:0 auto;width:50%;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <p
                                                                                                                            style="font-size:16px;line-height:22px;margin:0;Margin:0;font-family:'FarfetchBasis-Bold','Helvetica Neue',Arial,sans-serif;font-weight:700;Margin-bottom:12px;margin-bottom:12px;Margin-top:24px;margin-top:24px;text-align:right">
                                                                                                                            {user_inputs[14]}{user_inputs[13]}
                                                                                                                        </p>
                                                                                                                        <p
                                                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;Margin-bottom:24px;margin-bottom:24px;text-align:right">
                                                                                                                            CreditCard
                                                                                                                        </p>
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                    </th>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </th>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                        <table
                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                            width="100%" valign="top" align="left">
                                                            <tbody>
                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                    valign="top" align="left">
                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:560px;padding-right:16px;padding-left:16px"
                                                                        valign="top" align="left">
                                                                        <table
                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                            width="100%" valign="top" align="left">
                                                                            <tbody>
                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                    valign="top" align="left">
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                        valign="top" align="left">
                                                                                        <hr
                                                                                            style="border:0;padding:0;margin:0;Margin:0;border-top:1px solid #727272;color:#727272;background:#727272;Margin-top:24px;margin-top:24px">
                                                                                    </th>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </th>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <table align="center" class="m_8214844979060577330container"
                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:center;width:576px;margin:0 auto;Margin:0 auto;float:none"
                                            width="576" valign="top">
                                            <tbody>
                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                    valign="top" align="left">
                                                    <td style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                        valign="top" align="left">
                                                        <table
                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                            width="100%" valign="top" align="left">
                                                            <tbody>
                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                    valign="top" align="left">
                                                                    <th class="m_8214844979060577330banner m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;margin:0 auto;width:560px;padding-right:16px;padding-left:16px;padding-top:24px;padding-bottom:24px"
                                                                        valign="top" align="left">
                                                                        <table
                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                            width="100%" valign="top" align="left">
                                                                            <tbody>
                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                    valign="top" align="left">
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                        valign="top" align="left">
                                                                                        <p
                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0">
                                                                                            Excited to get your FARFETCH order?
                                                                                            We recommend you're at your selected
                                                                                            address at the time of delivery. If
                                                                                            you choose an alternative delivery
                                                                                            method through our courier, like
                                                                                            leaving your package in a safe
                                                                                            place, we won't be able to help if
                                                                                            your package is lost or
                                                                                            damaged.<br><br>If you have an
                                                                                            account with our courier, check your
                                                                                            delivery preferences, as these are
                                                                                            applied to your FARFETCH deliveries.
                                                                                            For more information, <a
                                                                                                href="https://email.farfetch.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTCQGzaeo8O8Rzcqudh3df5d4uoWKG1Sm6GduWo9n5RDols8rgzgH4O0fo8VXtpKX%3DCWYDYSTY&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmfJHJMslcpD7sCeaoatYQClSZZkef8ZkpbId1JXS24xc4gxON1asXDYOPfRX4tvRezTgJfy7CC-w.&amp;_di_=v2a01athrmehh958n598p59f7m9nsif2j4e3b04sfhv07g45or1g"
                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;color:#222222;text-decoration:underline;text-decoration-color:#222222"
                                                                                                target="_blank">visit our Terms
                                                                                                &amp; Conditions</a></p>
                                                                                        <hr
                                                                                            style="border:0;padding:0;margin:0;Margin:0;border-top:1px solid #727272;color:#727272;background:#727272;Margin-top:24px;margin-top:24px">
                                                                                    </th>
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                        valign="top" align="left"></th>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </th>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <table align="center" class="m_8214844979060577330container"
                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:center;width:576px;margin:0 auto;Margin:0 auto;float:none"
                                            width="576" valign="top">
                                            <tbody>
                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                    valign="top" align="left">
                                                    <td style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                        valign="top" align="left">
                                                        <table
                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                            width="100%" valign="top" align="left">
                                                            <tbody>
                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                    valign="top" align="left">
                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;margin:0 auto;width:560px;padding-right:16px;padding-left:16px;padding-top:48px;padding-bottom:48px"
                                                                        valign="top" align="left">
                                                                        <table
                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                            width="100%" valign="top" align="left">
                                                                            <tbody>
                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                    valign="top" align="left">
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                        valign="top" align="left">
                                                                                        <table
                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                            width="100%" valign="top"
                                                                                            align="left">
                                                                                            <tbody>
                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                    valign="top" align="left">
                                                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:100%;padding-left:0;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <h2
                                                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:24px;line-height:30px;text-align:center">
                                                                                                                            Loved
                                                                                                                            that?
                                                                                                                            Why
                                                                                                                            not
                                                                                                                            try
                                                                                                                            these
                                                                                                                        </h2>
                                                                                                                    </th>
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                        <table
                                                                                            class="m_8214844979060577330collapse"
                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                            width="100%" valign="top"
                                                                                            align="left">
                                                                                            <tbody>
                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                    valign="top" align="left">
                                                                                                    <th class="m_8214844979060577330small-6 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;text-align:center;margin:0 auto;width:25%;padding-left:0;padding-top:24px;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="center">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <center
                                                                                                                            style="width:100%;min-width:none">
                                                                                                                            <a href="https://email.farfetch.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTCQGzaeo8O8Rzcqudh3df5d4uoWKG1Sm6GduWo9n5RDols8rgzgH4O0fo8VXtpKX%3DCWTWTBAY&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmfJHJMslcpD7sCeaoatYQClSZZkef8ZkpbId1JXS24xbQ7dVWwL2WS7IVzMzifs7adj0_7xspiCxTdBM1A1o5ohUEBSJlOnjylXoSF_pNJ8LGZ4NKCG83haPogy2zVN1d0kkIsCv2rHiT_fsGb8juIznZ006wmHLtWRJjfDcrIuMxgcgGwMHX7UjNeYXlwEbdwQ0bgclENCVW_op23GzpukFux41bEYGDjUzBd8OJCSOIb32vmW6jpCNGXBuZShsxOM-tk0Emdvl_Ng61T8KPNlvzUG4oMXuAEvj8AhXJlFbRyVoAK_TkpEayU7HDhNv0hf4ENJ-X42kZ_j5HfNAACu2rQUPBF0u2X93GijCeuAOElF9PJEeJPKitEYnTo4EiD9OqTbVYnQWvCiZuxh6pW8-httnCYSNLLqEm-STiEQjyC9lHYB3irM-U12tqNAmqOn2KOg3pXaVnnmnL2rCs_fhqg9BsjrLbFRBLhJ4_VnBQwrbUW-tw3EvaOa5Ya3o-Qakt6W0MProerQJfbLRtw7-ny2OaIQ0rDNW2e3dDtgHja_-x8HLoIKY_b5ECAozuWHANcjd_ErdsBB0XTPMKRepvykXyEbqZFE5FRCRirtf8uG1uNp322Dlo3DNAAzFIlxs87HIEiczp8o1RWxqGu8B2IcvVTKezJFRzl_xG9mqDQQelT3IhMwSUZ9eCOXg6vnxNB71GLzuJy-kQ8MqAWvCXk7aJ0am0PJEouJwNAZ2NZl9--CYdC291x.&amp;_di_=rbqtvkast4sep7vmo4t89rh2gg181jiehu674a8cl8clknpke6mg"
                                                                                                                                align="center"
                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;color:#222222;text-decoration:underline;text-decoration-color:#222222"
                                                                                                                                target="_blank">
                                                                                                                                <img border="0"
                                                                                                                                    src="https://service-ofr.farfetch.net/v1/10000/products/543f9cbd0a58fe1b18c78f4951903ca1e226032e2811c243cd10ff1a1dbe3f97/cdn/0?campaignName=THANK_YOU_FOR_PLACING_YOUR_ORDER&amp;clientName=Responsys_op&amp;dateTime=2023-10-20T15:03:39Z&amp;strategyName=email_op_orderconfirmation_a&amp;userIdentifier=3e01a2a3bfae41bb505d88fd2be04b1c93943c7cc26aa151bfec95a785ab3998&amp;userType=emailHash&amp;countryCode=GB&amp;ProductId=18394987&amp;ffref=pp_recom&amp;rtype=inspire_email_op_orderconfirmation_a"
                                                                                                                                    width="82"
                                                                                                                                    height="110"
                                                                                                                                    alt=""
                                                                                                                                    style="outline:none;text-decoration:none;width:auto;max-width:100%;clear:both;display:block;border:none;padding-bottom:24px;margin:0 auto;Margin:0 auto;float:none;text-align:center">
                                                                                                                                <img border="0"
                                                                                                                                    src="https://service-ofr.farfetch.net/v1/10000/products/543f9cbd0a58fe1b18c78f4951903ca1e226032e2811c243cd10ff1a1dbe3f97/brand/0?campaignName=THANK_YOU_FOR_PLACING_YOUR_ORDER&amp;clientName=Responsys_op&amp;dateTime=2023-10-20T15:03:39Z&amp;strategyName=email_op_orderconfirmation_a&amp;userIdentifier=3e01a2a3bfae41bb505d88fd2be04b1c93943c7cc26aa151bfec95a785ab3998&amp;userType=emailHash&amp;countryCode=GB&amp;ProductId=18394987&amp;ffref=pp_recom&amp;rtype=inspire_email_op_orderconfirmation_a"
                                                                                                                                    width="136"
                                                                                                                                    height="14"
                                                                                                                                    alt=""
                                                                                                                                    style="outline:none;text-decoration:none;width:auto;max-width:100%;clear:both;display:block;border:none;margin:0 auto;Margin:0 auto;float:none;text-align:center">
                                                                                                                            </a>
                                                                                                                        </center>
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                    <th class="m_8214844979060577330small-6 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;text-align:center;margin:0 auto;width:25%;padding-left:0;padding-top:24px;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="center">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <center
                                                                                                                            style="width:100%;min-width:none">
                                                                                                                            <a href="https://email.farfetch.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTCQGzaeo8O8Rzcqudh3df5d4uoWKG1Sm6GduWo9n5RDols8rgzgH4O0fo8VXtpKX%3DCWTWTBAY&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmfJHJMslcpD7sCeaoatYQClSZZkef8ZkpbId1JXS24xbQ7dVWwL2WS7IVzMzifs7adj0_7xspiCxTdBM1A1o5ohUEBSJlOnjylXoSF_pNJ8LGZ4NKCG83haPogy2zVN1d0kkIsCv2rHiT_fsGb8juIznZ006wmHLtWRJjfDcrIuMxgcgGwMHX7UjNeYXlwEbdwQ0bgclENCVW_op23Gzpub5piRDsQhKmrtEBL92zTzYaOMgmba93roAmmpjvqrzkGKeJ1sUx8561nKzS4M8iMvK-Do-IBpqezV-B112wRDHWmXO4nt2eIYiwmFJ3TO4m8u03iNjj4dUeDFB-izctCQpUjHYHUxekqHn57F02ZKYwGO3ZgbiOYFV0C8gjuwR0j66Cj16npahNRZ2I1cqN5CtckdnNNGLW6IiY-iQ97_8HheXI95PgDPiXm4ItNQBkbFunul8BCzFSqTVjoI_cd0V2xeWV8UeghkjAT2_eBdIHssi_nuCmWzcJPXFu_4nuysv8DESBv51h7swp0fOzsKnvuSWVytHvNgryhVd3MbZ-crajB6D_lnmUicVU34II7urvMTNYMQoq64lytSDlHFNE_BbKnnjto8OnMnfsKkl-NPRY3QgOmgMSzNZYJXYy50POIO_Ph4RZzrmjZDeXtONBmzANpmNeDp0JdkutHamsq0yo2ZxP-9Fd5nndJU0Aq6Tkf0pCOpuzIDyVbtH1OA5eq0fAVj00J5iwWdlDO0qYWiFCACD8Yu9xy.&amp;_di_=lp89v1fqnafba9jk8qo1603941e322g1qiv80socgtq9qtjl91rg"
                                                                                                                                align="center"
                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;color:#222222;text-decoration:underline;text-decoration-color:#222222"
                                                                                                                                target="_blank">
                                                                                                                                <img border="0"
                                                                                                                                    src="https://service-ofr.farfetch.net/v1/10000/products/543f9cbd0a58fe1b18c78f4951903ca1e226032e2811c243cd10ff1a1dbe3f97/cdn/1?campaignName=THANK_YOU_FOR_PLACING_YOUR_ORDER&amp;clientName=Responsys_op&amp;dateTime=2023-10-20T15:03:39Z&amp;strategyName=email_op_orderconfirmation_a&amp;userIdentifier=3e01a2a3bfae41bb505d88fd2be04b1c93943c7cc26aa151bfec95a785ab3998&amp;userType=emailHash&amp;countryCode=GB&amp;ProductId=18394987&amp;ffref=pp_recom&amp;rtype=inspire_email_op_orderconfirmation_a"
                                                                                                                                    width="82"
                                                                                                                                    height="110"
                                                                                                                                    alt=""
                                                                                                                                    style="outline:none;text-decoration:none;width:auto;max-width:100%;clear:both;display:block;border:none;padding-bottom:24px;margin:0 auto;Margin:0 auto;float:none;text-align:center">
                                                                                                                                <img border="0"
                                                                                                                                    src="https://service-ofr.farfetch.net/v1/10000/products/543f9cbd0a58fe1b18c78f4951903ca1e226032e2811c243cd10ff1a1dbe3f97/brand/1?campaignName=THANK_YOU_FOR_PLACING_YOUR_ORDER&amp;clientName=Responsys_op&amp;dateTime=2023-10-20T15:03:39Z&amp;strategyName=email_op_orderconfirmation_a&amp;userIdentifier=3e01a2a3bfae41bb505d88fd2be04b1c93943c7cc26aa151bfec95a785ab3998&amp;userType=emailHash&amp;countryCode=GB&amp;ProductId=18394987&amp;ffref=pp_recom&amp;rtype=inspire_email_op_orderconfirmation_a"
                                                                                                                                    width="136"
                                                                                                                                    height="14"
                                                                                                                                    alt=""
                                                                                                                                    style="outline:none;text-decoration:none;width:auto;max-width:100%;clear:both;display:block;border:none;margin:0 auto;Margin:0 auto;float:none;text-align:center">
                                                                                                                            </a>
                                                                                                                        </center>
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                    <th class="m_8214844979060577330small-6 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;text-align:center;margin:0 auto;width:25%;padding-left:0;padding-top:24px;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="center">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <center
                                                                                                                            style="width:100%;min-width:none">
                                                                                                                            <a href="https://email.farfetch.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTCQGzaeo8O8Rzcqudh3df5d4uoWKG1Sm6GduWo9n5RDols8rgzgH4O0fo8VXtpKX%3DCWTWTBAY&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmfJHJMslcpD7sCeaoatYQClSZZkef8ZkpbId1JXS24xbQ7dVWwL2WS7IVzMzifs7adj0_7xspiCxTdBM1A1o5ohUEBSJlOnjylXoSF_pNJ8LGZ4NKCG83haPogy2zVN1d0kkIsCv2rHiT_fsGb8juIznZ006wmHLtWRJjfDcrIuMxgcgGwMHX7UjNeYXlwEbdwQ0bgclENCVW_op23Gzpu3F42mhHwrDORiZMMPa_PYnKYhvj1O2Q0PSXqgzGBhh4l4ne5veXNOFDNgoXcMDIdE6Myqd3MLDKi0F1vT-GonS67HG3OCesAdr_-abOV_sJBNkzG_1reCQFGZv97ZrOisGheTzD5MIfdIUDgS2-CsDr9G8LQjLnEqtWXqKkxJu8W2WsMsyDuzmbYQXGRxENSI0MGWFgP8ERQNGHpa5Sv-7s99Ekb_daHkZzB41KQdIMvedTNPozyhSoYBzcoN-CbbWv_1c-MSZg_bHFuxQqDvWaIdWgvrZgRoPMtWGWl05umcX9U9kvOeRO_Jzfd5UrLUMkvl8yGExkl85zWERkcnnYqARihGehJrzfevA0b3cTSoMi223jIYJlrAXszytZg0_PJy9MAQY1L3R--ZYWDJ75x1oSK0MR_sVGvQEKd2pZ6dW544D5OP7JULJcl9dNwQaXTqf-af_J1zZEvRYv2x2yg3XRMlD4AJFsEiv0XDaP9H36ahr1dqsWFMidJz8Rl6I9n3vF0ZUc02YzoRXur-3UAKf3E-NbP3CoJ.&amp;_di_=dk02ciot8nf5419fatun6pg90rhi3gr7frmn51k36k10ltnv6bf0"
                                                                                                                                align="center"
                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;color:#222222;text-decoration:underline;text-decoration-color:#222222"
                                                                                                                                target="_blank">
                                                                                                                                <img border="0"
                                                                                                                                    src="https://service-ofr.farfetch.net/v1/10000/products/543f9cbd0a58fe1b18c78f4951903ca1e226032e2811c243cd10ff1a1dbe3f97/cdn/2?campaignName=THANK_YOU_FOR_PLACING_YOUR_ORDER&amp;clientName=Responsys_op&amp;dateTime=2023-10-20T15:03:39Z&amp;strategyName=email_op_orderconfirmation_a&amp;userIdentifier=3e01a2a3bfae41bb505d88fd2be04b1c93943c7cc26aa151bfec95a785ab3998&amp;userType=emailHash&amp;countryCode=GB&amp;ProductId=18394987&amp;ffref=pp_recom&amp;rtype=inspire_email_op_orderconfirmation_a"
                                                                                                                                    width="82"
                                                                                                                                    height="110"
                                                                                                                                    alt=""
                                                                                                                                    style="outline:none;text-decoration:none;width:auto;max-width:100%;clear:both;display:block;border:none;padding-bottom:24px;margin:0 auto;Margin:0 auto;float:none;text-align:center">
                                                                                                                                <img border="0"
                                                                                                                                    src="https://service-ofr.farfetch.net/v1/10000/products/543f9cbd0a58fe1b18c78f4951903ca1e226032e2811c243cd10ff1a1dbe3f97/brand/2?campaignName=THANK_YOU_FOR_PLACING_YOUR_ORDER&amp;clientName=Responsys_op&amp;dateTime=2023-10-20T15:03:39Z&amp;strategyName=email_op_orderconfirmation_a&amp;userIdentifier=3e01a2a3bfae41bb505d88fd2be04b1c93943c7cc26aa151bfec95a785ab3998&amp;userType=emailHash&amp;countryCode=GB&amp;ProductId=18394987&amp;ffref=pp_recom&amp;rtype=inspire_email_op_orderconfirmation_a"
                                                                                                                                    width="136"
                                                                                                                                    height="14"
                                                                                                                                    alt=""
                                                                                                                                    style="outline:none;text-decoration:none;width:auto;max-width:100%;clear:both;display:block;border:none;margin:0 auto;Margin:0 auto;float:none;text-align:center">
                                                                                                                            </a>
                                                                                                                        </center>
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                    <th class="m_8214844979060577330small-6 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;text-align:center;margin:0 auto;width:25%;padding-left:0;padding-top:24px;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="center">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <center
                                                                                                                            style="width:100%;min-width:none">
                                                                                                                            <a href="https://email.farfetch.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTCQGzaeo8O8Rzcqudh3df5d4uoWKG1Sm6GduWo9n5RDols8rgzgH4O0fo8VXtpKX%3DCWTWTBAY&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmfJHJMslcpD7sCeaoatYQClSZZkef8ZkpbId1JXS24xbQ7dVWwL2WS7IVzMzifs7adj0_7xspiCxTdBM1A1o5ohUEBSJlOnjylXoSF_pNJ8LGZ4NKCG83haPogy2zVN1d0kkIsCv2rHiT_fsGb8juIznZ006wmHLtWRJjfDcrIuMxgcgGwMHX7UjNeYXlwEbdwQ0bgclENCVW_op23GzpuviZapCJAwEWcvN3wvi3VMEPoPPIKdOHpCNnQJzhwU1h2x5nM5aWYoV1Xbrq9dOGCIOF8OHFwdBljFtgmlhViluAXA9Qqp51Vtgs6bdPKcHxFQ3UOA9N5U1W4S1wg65VTBZL5DWtsxCWUtjvLkuzMNowsxyIF6lZ7P-84bj80SUkoJlXEtLVvom81RbCBtqiiyOWCx4VuJy-LmbrsuwGBf1xmsqIUGpt_dzNWp2G2e5vIlQOgUGYNryvnrnvl_p4gPVvZtxDwrFeildc-8umQrGocDZ3Ti6Nx23GkHU44pcCGofzsg-WPOuSUabw3_86FakebbU_LK8GCiHLQDIPmzvrjX2uCm5OdB6GO61JLTZAHkBhEYBhcopRTn7NtvVGkU9xJgeZEfkT0fWikSsTTBPmVDiIBRAEgg4HoSrhJBL8-KZ43EYRJ9UJbh8bQB1IjcsQv3jWfecLMIQlXajfe5bz8js6_a5ryOsb2OLR8MnciJo_7vlRQCvb999Y2dFnH85H9-3M_jxjnLmm2HnOK-5cqkUMwwq17nwjF.&amp;_di_=i8ffgmlqq4avp315kmk34bo6j8hf8jnj4j5kadsa9jijg1i01nu0"
                                                                                                                                align="center"
                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;color:#222222;text-decoration:underline;text-decoration-color:#222222"
                                                                                                                                target="_blank">
                                                                                                                                <img border="0"
                                                                                                                                    src="https://service-ofr.farfetch.net/v1/10000/products/543f9cbd0a58fe1b18c78f4951903ca1e226032e2811c243cd10ff1a1dbe3f97/cdn/3?campaignName=THANK_YOU_FOR_PLACING_YOUR_ORDER&amp;clientName=Responsys_op&amp;dateTime=2023-10-20T15:03:39Z&amp;strategyName=email_op_orderconfirmation_a&amp;userIdentifier=3e01a2a3bfae41bb505d88fd2be04b1c93943c7cc26aa151bfec95a785ab3998&amp;userType=emailHash&amp;countryCode=GB&amp;ProductId=18394987&amp;ffref=pp_recom&amp;rtype=inspire_email_op_orderconfirmation_a"
                                                                                                                                    width="82"
                                                                                                                                    height="110"
                                                                                                                                    alt=""
                                                                                                                                    style="outline:none;text-decoration:none;width:auto;max-width:100%;clear:both;display:block;border:none;padding-bottom:24px;margin:0 auto;Margin:0 auto;float:none;text-align:center">
                                                                                                                                <img border="0"
                                                                                                                                    src="https://service-ofr.farfetch.net/v1/10000/products/543f9cbd0a58fe1b18c78f4951903ca1e226032e2811c243cd10ff1a1dbe3f97/brand/3?campaignName=THANK_YOU_FOR_PLACING_YOUR_ORDER&amp;clientName=Responsys_op&amp;dateTime=2023-10-20T15:03:39Z&amp;strategyName=email_op_orderconfirmation_a&amp;userIdentifier=3e01a2a3bfae41bb505d88fd2be04b1c93943c7cc26aa151bfec95a785ab3998&amp;userType=emailHash&amp;countryCode=GB&amp;ProductId=18394987&amp;ffref=pp_recom&amp;rtype=inspire_email_op_orderconfirmation_a"
                                                                                                                                    width="136"
                                                                                                                                    height="14"
                                                                                                                                    alt=""
                                                                                                                                    style="outline:none;text-decoration:none;width:auto;max-width:100%;clear:both;display:block;border:none;margin:0 auto;Margin:0 auto;float:none;text-align:center">
                                                                                                                            </a>
                                                                                                                        </center>
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                    </th>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </th>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <table align="center" class="m_8214844979060577330container"
                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:center;width:576px;margin:0 auto;Margin:0 auto;float:none"
                                            width="576" valign="top">
                                            <tbody>
                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                    valign="top" align="left">
                                                    <td style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                        valign="top" align="left">
                                                        <table
                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;Margin-bottom:24px;margin-bottom:24px;padding:0;width:100%;display:table"
                                                            width="100%" valign="top" align="left">
                                                            <tbody>
                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                    valign="top" align="left">
                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:560px;padding-right:16px;padding-left:16px"
                                                                        valign="top" align="left">
                                                                        <table
                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                            width="100%" valign="top" align="left">
                                                                            <tbody>
                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                    valign="top" align="left">
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                        valign="top" align="left">
                                                                                        <h2
                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:24px;line-height:30px">
                                                                                            What happens next?
                                                                                        </h2>
                                                                                    </th>
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                        valign="top" align="left"></th>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </th>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                        <table class="m_8214844979060577330next-steps-item"
                                                            style="border-spacing:0;border-collapse:collapse;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding-top:24px;Margin-bottom:24px;margin-bottom:24px;padding:0;width:100%;display:table"
                                                            width="100%" valign="top" align="left">
                                                            <tbody>
                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                    valign="top" align="left">
                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:560px;padding-right:16px;padding-left:16px"
                                                                        valign="top" align="left">
                                                                        <table
                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                            width="100%" valign="top" align="left">
                                                                            <tbody>
                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                    valign="top" align="left">
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                        valign="top" align="left">
                                                                                        <img src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/icons/light/clock.png"
                                                                                            class="m_8214844979060577330light-mode-image"
                                                                                            alt="Step 1 - Timing" width="24"
                                                                                            height="24"
                                                                                            style="outline:none;text-decoration:none;width:auto;max-width:100%;clear:both;float:left;text-align:left;display:inline-block">
                                                                                        <span
                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;display:none">
                                                                                            <img src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/icons/dark/clock.png"
                                                                                                class="m_8214844979060577330dark-mode-image"
                                                                                                alt="Step 1 - Timing" width="24"
                                                                                                height="24"
                                                                                                style="outline:none;text-decoration:none;width:auto;max-width:100%;clear:both;float:left;text-align:left;display:inline-block">
                                                                                        </span>
                                                                                        <p
                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;Margin-left:12px;margin-left:12px;vertical-align:top;max-width:93%;display:inline-block">
                                                                                            Your order's placed and usually
                                                                                            takes two business days to be
                                                                                            confirmed
                                                                                        </p>
                                                                                    </th>
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                        valign="top" align="left"></th>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </th>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                        <table class="m_8214844979060577330next-steps-item"
                                                            style="border-spacing:0;border-collapse:collapse;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding-top:24px;Margin-bottom:24px;margin-bottom:24px;padding:0;width:100%;display:table"
                                                            width="100%" valign="top" align="left">
                                                            <tbody>
                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                    valign="top" align="left">
                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:560px;padding-right:16px;padding-left:16px"
                                                                        valign="top" align="left">
                                                                        <table
                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                            width="100%" valign="top" align="left">
                                                                            <tbody>
                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                    valign="top" align="left">
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                        valign="top" align="left">
                                                                                        <img src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/icons/light/heart.png"
                                                                                            class="m_8214844979060577330light-mode-image"
                                                                                            alt="Step 2 - Care" width="24"
                                                                                            height="24"
                                                                                            style="outline:none;text-decoration:none;width:auto;max-width:100%;clear:both;float:left;text-align:left;display:inline-block">
                                                                                        <span
                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;display:none">
                                                                                            <img src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/icons/dark/heart.png"
                                                                                                class="m_8214844979060577330dark-mode-image"
                                                                                                alt="Step 2 - Care" width="24"
                                                                                                height="24"
                                                                                                style="outline:none;text-decoration:none;width:auto;max-width:100%;clear:both;float:left;text-align:left;display:inline-block">
                                                                                        </span>
                                                                                        <p
                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;Margin-left:12px;margin-left:12px;vertical-align:top;max-width:93%;display:inline-block">
                                                                                            It's then carefully packaged by our
                                                                                            partner brand or boutique
                                                                                        </p>
                                                                                    </th>
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                        valign="top" align="left"></th>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </th>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                        <table class="m_8214844979060577330next-steps-item"
                                                            style="border-spacing:0;border-collapse:collapse;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding-top:24px;Margin-bottom:24px;margin-bottom:24px;padding:0;width:100%;display:table"
                                                            width="100%" valign="top" align="left">
                                                            <tbody>
                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                    valign="top" align="left">
                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:560px;padding-right:16px;padding-left:16px"
                                                                        valign="top" align="left">
                                                                        <table
                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                            width="100%" valign="top" align="left">
                                                                            <tbody>
                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                    valign="top" align="left">
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                        valign="top" align="left">
                                                                                        <img src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/icons/light/box-progress.png"
                                                                                            class="m_8214844979060577330light-mode-image"
                                                                                            alt="Step 3 - Progress" width="24"
                                                                                            height="24"
                                                                                            style="outline:none;text-decoration:none;width:auto;max-width:100%;clear:both;float:left;text-align:left;display:inline-block">
                                                                                        <span
                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;display:none">
                                                                                            <img src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/icons/dark/box-progress.png"
                                                                                                class="m_8214844979060577330dark-mode-image"
                                                                                                alt="Step 3 - Progress"
                                                                                                width="24" height="24"
                                                                                                style="outline:none;text-decoration:none;width:auto;max-width:100%;clear:both;float:left;text-align:left;display:inline-block">
                                                                                        </span>
                                                                                        <p
                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;Margin-left:12px;margin-left:12px;vertical-align:top;max-width:93%;display:inline-block">
                                                                                            You'll receive an email confirming
                                                                                            your estimated delivery date when
                                                                                            it's on its way
                                                                                        </p>
                                                                                    </th>
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                        valign="top" align="left"></th>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </th>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                        <table class="m_8214844979060577330next-steps-item"
                                                            style="border-spacing:0;border-collapse:collapse;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding-top:24px;Margin-bottom:24px;margin-bottom:24px;padding:0;width:100%;display:table"
                                                            width="100%" valign="top" align="left">
                                                            <tbody>
                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                    valign="top" align="left">
                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:560px;padding-right:16px;padding-left:16px"
                                                                        valign="top" align="left">
                                                                        <table
                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                            width="100%" valign="top" align="left">
                                                                            <tbody>
                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                    valign="top" align="left">
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                        valign="top" align="left">
                                                                                        <img src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/icons/light/box-return.png"
                                                                                            class="m_8214844979060577330light-mode-image"
                                                                                            alt="Step 4 - Return" width="24"
                                                                                            height="24"
                                                                                            style="outline:none;text-decoration:none;width:auto;max-width:100%;clear:both;float:left;text-align:left;display:inline-block">
                                                                                        <span
                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;display:none">
                                                                                            <img src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/icons/dark/box-return.png"
                                                                                                class="m_8214844979060577330dark-mode-image"
                                                                                                alt="Step 4 - Return" width="24"
                                                                                                height="24"
                                                                                                style="outline:none;text-decoration:none;width:auto;max-width:100%;clear:both;float:left;text-align:left;display:inline-block">
                                                                                        </span>
                                                                                        <p
                                                                                            style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;Margin-left:12px;margin-left:12px;vertical-align:top;max-width:93%;display:inline-block">
                                                                                            No problem, we offer free returns
                                                                                            within 14 days, or more depending on
                                                                                            your Access tier
                                                                                        </p>
                                                                                    </th>
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                        valign="top" align="left"></th>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </th>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <table align="center" class="m_8214844979060577330container"
                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:center;width:576px;margin:0 auto;Margin:0 auto;float:none"
                                            width="576" valign="top">
                                            <tbody>
                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                    valign="top" align="left">
                                                    <td style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                        valign="top" align="left">
                                                        <table
                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                            width="100%" valign="top" align="left">
                                                            <tbody>
                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                    valign="top" align="left">
                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;margin:0 auto;width:560px;padding-right:16px;padding-left:16px;padding-top:48px;padding-bottom:48px"
                                                                        valign="top" align="left">
                                                                        <table
                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                            width="100%" valign="top" align="left">
                                                                            <tbody>
                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                    valign="top" align="left">
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                        valign="top" align="left">
                                                                                        <table
                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                            width="100%" valign="top"
                                                                                            align="left">
                                                                                            <tbody>
                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                    valign="top" align="left">
                                                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:100%;padding-left:0;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <h2
                                                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:24px;line-height:30px;Margin-bottom:12px;margin-bottom:12px;text-align:center">
                                                                                                                            Need
                                                                                                                            help?
                                                                                                                        </h2>
                                                                                                                        <p class="m_8214844979060577330help-contacts-message"
                                                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:14px;line-height:18px;Margin-bottom:48px;margin-bottom:48px;text-align:center">
                                                                                                                            Contact
                                                                                                                            our
                                                                                                                            global
                                                                                                                            Customer
                                                                                                                            Service
                                                                                                                            team.<br
                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:14px;line-height:18px">Remember
                                                                                                                            we&#x2019;ll
                                                                                                                            need
                                                                                                                            your
                                                                                                                            order
                                                                                                                            number.
                                                                                                                        </p>
                                                                                                                    </th>
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                        <table
                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                            width="100%" valign="top"
                                                                                            align="left">
                                                                                            <tbody>
                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                    valign="top" align="left">
                                                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-right:8px;padding-bottom:0;margin:0 auto;width:33.33333%;padding-left:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <center
                                                                                                                            style="width:100%;min-width:none">
                                                                                                                            <img class="m_8214844979060577330light-mode-image"
                                                                                                                                src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/images_help/IconMailLight@4x.png"
                                                                                                                                width="24"
                                                                                                                                height="24"
                                                                                                                                alt="email icon"
                                                                                                                                align="middle"
                                                                                                                                style="outline:none;text-decoration:none;max-width:100%;clear:both;display:block;margin:0 auto;Margin:0 auto;float:none;text-align:center;width:24px;height:24px">
                                                                                                                            <span
                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;text-align:-webkit-center;display:none"
                                                                                                                                align="center">
                                                                                                                                <img class="m_8214844979060577330dark-mode-image"
                                                                                                                                    src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/images_help/IconMailDark@4x.png"
                                                                                                                                    width="24"
                                                                                                                                    height="24"
                                                                                                                                    alt="email icon"
                                                                                                                                    style="outline:none;text-decoration:none;max-width:100%;clear:both;display:block;width:24px;height:24px">
                                                                                                                            </span>
                                                                                                                        </center>
                                                                                                                        <p
                                                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Bold','Helvetica Neue',Arial,sans-serif;font-weight:700;font-size:11px;line-height:14px;Margin-top:12px;margin-top:12px;Margin-bottom:6px;margin-bottom:6px;text-align:center">
                                                                                                                            Email
                                                                                                                            us
                                                                                                                        </p>
                                                                                                                        <p
                                                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:11px;line-height:14px;text-align:center">
                                                                                                                            <a href="https://email.farfetch.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTCQGzaeo8O8Rzcqudh3df5d4uoWKG1Sm6GduWo9n5RDols8rgzgH4O0fo8VXtpKX%3DYABWBWY&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmfJHJMslcpD7sCeaoatYQClSZZkef8ZkpbId1JXS24xc4gxON1asXDYOPfRX4tvRezTgJfy7CC-w.&amp;_di_=hec56vgqdlac7jaagljgj1f5ts95tfit9bkq5g6m8lkvdsi3t320"
                                                                                                                                style="margin:0;Margin:0;color:#222222;text-decoration:underline;text-decoration-color:#222222;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px"
                                                                                                                                target="_blank">
                                                                                                                                Send
                                                                                                                                us
                                                                                                                                an
                                                                                                                                email
                                                                                                                            </a>
                                                                                                                        </p>
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns"
                                                                                                        dir="ltr"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-right:8px;padding-bottom:0;padding-left:8px;margin:0 auto;width:33.33333%"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <table
                                                                                                                            class="m_8214844979060577330hide-for-large"
                                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;display:none;overflow:hidden;max-height:0;font-size:0;line-height:0;width:100%"
                                                                                                                            width="100%"
                                                                                                                            valign="top"
                                                                                                                            align="left">
                                                                                                                            <tbody>
                                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                                    valign="top"
                                                                                                                                    align="left">
                                                                                                                                    <td height="24"
                                                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;margin:0;Margin:0;font-size:24px;line-height:24px"
                                                                                                                                        valign="top"
                                                                                                                                        align="left">
                                                                                                                                    </td>
                                                                                                                                </tr>
                                                                                                                            </tbody>
                                                                                                                        </table>
                                                                                                                        <center
                                                                                                                            style="width:100%;min-width:none">
                                                                                                                            <img class="m_8214844979060577330light-mode-image"
                                                                                                                                src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/images_help/IconPhoneLight@4x.png"
                                                                                                                                width="24"
                                                                                                                                height="24"
                                                                                                                                alt="phone icon"
                                                                                                                                align="middle"
                                                                                                                                style="outline:none;text-decoration:none;max-width:100%;clear:both;display:block;margin:0 auto;Margin:0 auto;float:none;text-align:center;width:24px;height:24px">
                                                                                                                            <span
                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;text-align:-webkit-center;display:none"
                                                                                                                                align="center">
                                                                                                                                <img class="m_8214844979060577330dark-mode-image"
                                                                                                                                    src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/images_help/IconPhoneDark@4x.png"
                                                                                                                                    width="24"
                                                                                                                                    height="24"
                                                                                                                                    alt="phone icon"
                                                                                                                                    style="outline:none;text-decoration:none;max-width:100%;clear:both;display:block;width:24px;height:24px">
                                                                                                                            </span>
                                                                                                                        </center>
                                                                                                                        <p
                                                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Bold','Helvetica Neue',Arial,sans-serif;font-weight:700;font-size:11px;line-height:14px;Margin-top:12px;margin-top:12px;Margin-bottom:6px;margin-bottom:6px;text-align:center">
                                                                                                                            Call
                                                                                                                            us
                                                                                                                        </p>
                                                                                                                        <p
                                                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:11px;line-height:14px;text-align:center">
                                                                                                                            <span
                                                                                                                                style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px;margin-right:0.25rem">
                                                                                                                                US
                                                                                                                            </span>
                                                                                                                            <a href="tel:+16467913768"
                                                                                                                                style="margin:0;Margin:0;color:#222222;text-decoration:underline;text-decoration-color:#222222;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px"
                                                                                                                                target="_blank">&#x200E;+1
                                                                                                                                646
                                                                                                                                791
                                                                                                                                3768</a><br
                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px">
                                                                                                                            <span
                                                                                                                                style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px;margin-right:0.25rem">
                                                                                                                                CA
                                                                                                                            </span>
                                                                                                                            <a href="tel:+12267804061"
                                                                                                                                style="margin:0;Margin:0;color:#222222;text-decoration:underline;text-decoration-color:#222222;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px"
                                                                                                                                target="_blank">&#x200E;+1
                                                                                                                                226
                                                                                                                                780
                                                                                                                                4061</a><br
                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px">
                                                                                                                            <span
                                                                                                                                style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px;margin-right:0.25rem">
                                                                                                                                AU
                                                                                                                                and
                                                                                                                                NZ
                                                                                                                            </span>
                                                                                                                            <a href="tel:+61488839167"
                                                                                                                                style="margin:0;Margin:0;color:#222222;text-decoration:underline;text-decoration-color:#222222;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px"
                                                                                                                                target="_blank">&#x200E;+61
                                                                                                                                488
                                                                                                                                839
                                                                                                                                167</a><br
                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px">
                                                                                                                            <span
                                                                                                                                style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px">
                                                                                                                                UK
                                                                                                                                and
                                                                                                                                rest
                                                                                                                                of
                                                                                                                                world
                                                                                                                            </span><br
                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px">
                                                                                                                            <a href="tel:+4402039622362"
                                                                                                                                style="margin:0;Margin:0;color:#222222;text-decoration:underline;text-decoration-color:#222222;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px"
                                                                                                                                target="_blank">&#x200E;+44
                                                                                                                                (0)
                                                                                                                                20
                                                                                                                                3962
                                                                                                                                2362</a>
                                                                                                                        </p>
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;padding-left:8px;margin:0 auto;width:33.33333%;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <table
                                                                                                                            class="m_8214844979060577330hide-for-large"
                                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;display:none;overflow:hidden;max-height:0;font-size:0;line-height:0;width:100%"
                                                                                                                            width="100%"
                                                                                                                            valign="top"
                                                                                                                            align="left">
                                                                                                                            <tbody>
                                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                                    valign="top"
                                                                                                                                    align="left">
                                                                                                                                    <td height="24"
                                                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;margin:0;Margin:0;font-size:24px;line-height:24px"
                                                                                                                                        valign="top"
                                                                                                                                        align="left">
                                                                                                                                    </td>
                                                                                                                                </tr>
                                                                                                                            </tbody>
                                                                                                                        </table>
                                                                                                                        <center
                                                                                                                            style="width:100%;min-width:none">
                                                                                                                            <img class="m_8214844979060577330light-mode-image"
                                                                                                                                src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/images_help/IconQuestionMarkCircleLight@4x.png"
                                                                                                                                width="24"
                                                                                                                                height="24"
                                                                                                                                alt="faq icon"
                                                                                                                                align="middle"
                                                                                                                                style="outline:none;text-decoration:none;max-width:100%;clear:both;display:block;margin:0 auto;Margin:0 auto;float:none;text-align:center;width:24px;height:24px">
                                                                                                                            <span
                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;text-align:-webkit-center;display:none"
                                                                                                                                align="center">
                                                                                                                                <img class="m_8214844979060577330dark-mode-image"
                                                                                                                                    src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/images_help/IconQuestionMarkCircleDark@4x.png"
                                                                                                                                    width="24"
                                                                                                                                    height="24"
                                                                                                                                    alt="faq icon"
                                                                                                                                    style="outline:none;text-decoration:none;max-width:100%;clear:both;display:block;width:24px;height:24px">
                                                                                                                            </span>
                                                                                                                        </center>
                                                                                                                        <p
                                                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Bold','Helvetica Neue',Arial,sans-serif;font-weight:700;font-size:11px;line-height:14px;Margin-top:12px;margin-top:12px;Margin-bottom:6px;margin-bottom:6px;text-align:center">
                                                                                                                            FAQs
                                                                                                                        </p>
                                                                                                                        <p
                                                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:11px;line-height:14px;text-align:center">
                                                                                                                            <a href="https://email.farfetch.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTCQGzaeo8O8Rzcqudh3df5d4uoWKG1Sm6GduWo9n5RDols8rgzgH4O0fo8VXtpKX%3DYABWYRY&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmfJHJMslcpD7sCeaoatYQClSZZkef8ZkpbId1JXS24xc4gxON1asXDYOPfRX4tvRezTgJfy7CC-w.&amp;_di_=buh60kbf59nbe33oo3ind5q5h0lfi40ug72oems8mbjvqjs7k550"
                                                                                                                                style="margin:0;Margin:0;color:#222222;text-decoration:underline;text-decoration-color:#222222;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px"
                                                                                                                                target="_blank">
                                                                                                                                Find
                                                                                                                                the
                                                                                                                                answers
                                                                                                                                you
                                                                                                                                need
                                                                                                                                in
                                                                                                                                our
                                                                                                                                FAQs
                                                                                                                            </a>
                                                                                                                        </p>
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                    </th>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </th>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <table align="center" class="m_8214844979060577330container"
                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:center;width:576px;margin:0 auto;Margin:0 auto;float:none"
                                            width="576" valign="top">
                                            <tbody>
                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                    valign="top" align="left">
                                                    <td style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                        valign="top" align="left">
                                                        <table
                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                            width="100%" valign="top" align="left">
                                                            <tbody>
                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                    valign="top" align="left">
                                                                    <th class="m_8214844979060577330footer m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;margin:0 auto;width:560px;padding-right:16px;padding-left:16px;padding-top:36px;padding-bottom:36px"
                                                                        valign="top" align="left">
                                                                        <table
                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                            width="100%" valign="top" align="left">
                                                                            <tbody>
                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                    valign="top" align="left">
                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                        valign="top" align="left">
                                                                                        <table
                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                            width="100%" valign="top"
                                                                                            align="left">
                                                                                            <tbody>
                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                    valign="top" align="left">
                                                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;padding-top:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;width:100%;padding-left:0;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <center
                                                                                                                            style="width:100%;min-width:none">
                                                                                                                            <table
                                                                                                                                align="center"
                                                                                                                                class="m_8214844979060577330menu"
                                                                                                                                style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:center;margin:0 auto;Margin:0 auto;float:none;width:auto"
                                                                                                                                valign="top">
                                                                                                                                <tbody>
                                                                                                                                    <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:center"
                                                                                                                                        valign="top"
                                                                                                                                        align="center">
                                                                                                                                        <td style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                                            valign="top"
                                                                                                                                            align="left">
                                                                                                                                            <table
                                                                                                                                                style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                                                                width="100%"
                                                                                                                                                valign="top"
                                                                                                                                                align="left">
                                                                                                                                                <tbody>
                                                                                                                                                    <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:center"
                                                                                                                                                        valign="top"
                                                                                                                                                        align="center">
                                                                                                                                                        <th style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;text-align:center;margin:0 auto;Margin:0 auto;float:none;padding-top:0;padding-right:12px;padding-bottom:0;padding-left:12px;text-decoration:none"
                                                                                                                                                            valign="top"
                                                                                                                                                            align="center">
                                                                                                                                                            <a href="https://email.farfetch.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTCQGzaeo8O8Rzcqudh3df5d4uoWKG1Sm6GduWo9n5RDols8rgzgH4O0fo8VXtpKX%3DYABWAWY&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmfJHJMslcpD7sCeaoatYQClSZZkef8ZkpbId1JXS24xc4gxON1asXDYOPfRX4tvRezTgJfy7CC-w.&amp;_di_=94gfsnpch0al1desbbusjgidng1nffhi19gvekc6kl754lrfmgbg"
                                                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;text-decoration:underline;text-decoration-color:#222222;color:#222222"
                                                                                                                                                                target="_blank">
                                                                                                                                                                <img src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/images_footer/IconInstagramLight@4x.png"
                                                                                                                                                                    width="24"
                                                                                                                                                                    height="24"
                                                                                                                                                                    class="m_8214844979060577330light-mode-image"
                                                                                                                                                                    alt="instagram icon"
                                                                                                                                                                    style="outline:none;text-decoration:none;max-width:100%;clear:both;display:block;border:none;width:24px;height:24px">
                                                                                                                                                                <div
                                                                                                                                                                    style="display:none">

                                                                                                                                                                </div>
                                                                                                                                                            </a>
                                                                                                                                                        </th>
                                                                                                                                                        <th style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;text-align:center;margin:0 auto;Margin:0 auto;float:none;padding-top:0;padding-right:12px;padding-bottom:0;padding-left:12px;text-decoration:none"
                                                                                                                                                            valign="top"
                                                                                                                                                            align="center">
                                                                                                                                                            <a href="https://email.farfetch.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTCQGzaeo8O8Rzcqudh3df5d4uoWKG1Sm6GduWo9n5RDols8rgzgH4O0fo8VXtpKX%3DYABWAAY&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmfJHJMslcpD7sCeaoatYQClSZZkef8ZkpbId1JXS24xc4gxON1asXDYOPfRX4tvRezTgJfy7CC-w.&amp;_di_=gnehjm6hrfrgo5ghamtgb0irlcov08bh7tfu2qarr0nq1baokdm0"
                                                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;text-decoration:underline;text-decoration-color:#222222;color:#222222"
                                                                                                                                                                target="_blank">
                                                                                                                                                                <img src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/images_footer/IconFacebookLight@4x.png"
                                                                                                                                                                    width="24"
                                                                                                                                                                    height="24"
                                                                                                                                                                    class="m_8214844979060577330light-mode-image"
                                                                                                                                                                    alt="facebook icon"
                                                                                                                                                                    style="outline:none;text-decoration:none;max-width:100%;clear:both;display:block;border:none;width:24px;height:24px">
                                                                                                                                                                <div
                                                                                                                                                                    style="display:none">

                                                                                                                                                                </div>
                                                                                                                                                            </a>
                                                                                                                                                        </th>
                                                                                                                                                        <th style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;text-align:center;margin:0 auto;Margin:0 auto;float:none;padding-top:0;padding-right:12px;padding-bottom:0;padding-left:12px;text-decoration:none"
                                                                                                                                                            valign="top"
                                                                                                                                                            align="center">
                                                                                                                                                            <a href="https://email.farfetch.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTCQGzaeo8O8Rzcqudh3df5d4uoWKG1Sm6GduWo9n5RDols8rgzgH4O0fo8VXtpKX%3DYABWBRY&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmfJHJMslcpD7sCeaoatYQClSZZkef8ZkpbId1JXS24xc4gxON1asXDYOPfRX4tvRezTgJfy7CC-w.&amp;_di_=29c2e9bvapaqb5pf8ipe8s8nahhl9ditpcrojo66r72edvkgk8b0"
                                                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;text-decoration:underline;text-decoration-color:#222222;color:#222222"
                                                                                                                                                                target="_blank">
                                                                                                                                                                <img src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/images_footer/IconTwitterLight@4x.png"
                                                                                                                                                                    width="24"
                                                                                                                                                                    height="24"
                                                                                                                                                                    class="m_8214844979060577330light-mode-image"
                                                                                                                                                                    alt="twitter icon"
                                                                                                                                                                    style="outline:none;text-decoration:none;max-width:100%;clear:both;display:block;border:none;width:24px;height:24px">
                                                                                                                                                                <div
                                                                                                                                                                    style="display:none">

                                                                                                                                                                </div>
                                                                                                                                                            </a>
                                                                                                                                                        </th>
                                                                                                                                                        <th style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;text-align:center;margin:0 auto;Margin:0 auto;float:none;padding-top:0;padding-right:12px;padding-bottom:0;padding-left:12px;text-decoration:none"
                                                                                                                                                            valign="top"
                                                                                                                                                            align="center">
                                                                                                                                                            <a href="https://email.farfetch.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTCQGzaeo8O8Rzcqudh3df5d4uoWKG1Sm6GduWo9n5RDols8rgzgH4O0fo8VXtpKX%3DYABWBTY&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmfJHJMslcpD7sCeaoatYQClSZZkef8ZkpbId1JXS24xc4gxON1asXDYOPfRX4tvRezTgJfy7CC-w.&amp;_di_=at7dh5ma6elv157rvcurvi3a1377slrklhnqm2g4en50h5k34rdg"
                                                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;text-decoration:underline;text-decoration-color:#222222;color:#222222"
                                                                                                                                                                target="_blank">
                                                                                                                                                                <img src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/images_footer/IconPinterestLight@4x.png"
                                                                                                                                                                    width="24"
                                                                                                                                                                    height="24"
                                                                                                                                                                    class="m_8214844979060577330light-mode-image"
                                                                                                                                                                    alt="pinterest icon"
                                                                                                                                                                    style="outline:none;text-decoration:none;max-width:100%;clear:both;display:block;border:none;width:24px;height:24px">
                                                                                                                                                                <div
                                                                                                                                                                    style="display:none">

                                                                                                                                                                </div>
                                                                                                                                                            </a>
                                                                                                                                                        </th>
                                                                                                                                                        <th style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;text-align:center;margin:0 auto;Margin:0 auto;float:none;padding-top:0;padding-right:12px;padding-bottom:0;padding-left:12px;text-decoration:none"
                                                                                                                                                            valign="top"
                                                                                                                                                            align="center">
                                                                                                                                                            <a href="https://email.farfetch.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTCQGzaeo8O8Rzcqudh3df5d4uoWKG1Sm6GduWo9n5RDols8rgzgH4O0fo8VXtpKX%3DCWBWSYCY&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmfJHJMslcpD7sCeaoatYQClSZZkef8ZkpbId1JXS24xc4gxON1asXDYOPfRX4tvRezTgJfy7CC-w.&amp;_di_=nrqdgp3um938a26q3gi8crb1isu5mqbl65csb19psodbpp08df1g"
                                                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:16px;line-height:22px;margin:0;Margin:0;text-decoration:underline;text-decoration-color:#222222;color:#222222"
                                                                                                                                                                target="_blank">
                                                                                                                                                                <img src="https://static.cdn.responsys.net/i5/responsysimages/farfetch/contentlibrary/ff_transactional_emails/resources/images_footer/IconYoutubeLight@4x.png"
                                                                                                                                                                    width="24"
                                                                                                                                                                    height="24"
                                                                                                                                                                    class="m_8214844979060577330light-mode-image"
                                                                                                                                                                    alt="youtube icon"
                                                                                                                                                                    style="outline:none;text-decoration:none;max-width:100%;clear:both;display:block;border:none;width:24px;height:24px">
                                                                                                                                                                <div
                                                                                                                                                                    style="display:none">

                                                                                                                                                                </div>
                                                                                                                                                            </a>
                                                                                                                                                        </th>
                                                                                                                                                    </tr>
                                                                                                                                                </tbody>
                                                                                                                                            </table>
                                                                                                                                        </td>
                                                                                                                                    </tr>
                                                                                                                                </tbody>
                                                                                                                            </table>
                                                                                                                        </center>
                                                                                                                    </th>
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                        <table
                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                            width="100%" valign="top"
                                                                                            align="left">
                                                                                            <tbody>
                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                    valign="top" align="left">
                                                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;padding-top:24px;width:100%;padding-left:0;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <p
                                                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:11px;line-height:14px;text-align:center">
                                                                                                                            FARFETCH
                                                                                                                            App
                                                                                                                            for
                                                                                                                            <a href="https://email.farfetch.com/pub/acc?_ri_=X0Gzc2X%3DAQjkPkSTCQGzaeo8O8Rzcqudh3df5d4uoWKG1Sm6GduWo9n5RDols8rgzgH4O0fo8VXtpKX%3DYABWARY&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmfJHJMslcpD7sCeaoatYQClSZZkef8ZkpbId1JXS24xc4gxON1asXDYOPfRX4tvRezTgJfy7CC-w.&amp;_di_=6l1um4mfmobo1ffbprpb0508s050n1paikv5j8pm1u8vhc9q55a0"
                                                                                                                                style="margin:0;Margin:0;color:#222222;text-decoration:underline;text-decoration-color:#222222;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px"
                                                                                                                                target="_blank">iOS</a>
                                                                                                                            and
                                                                                                                            <a href="https://email.farfetch.com/pub/acc?_ri_=X0Gzc2X%3DAQjkPkSTCQGzaeo8O8Rzcqudh3df5d4uoWKG1Sm6GduWo9n5RDols8rgzgH4O0fo8VXtpKX%3DYABWATY&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmfJHJMslcpD7sCeaoatYQClSZZkef8ZkpbId1JXS24xc4gxON1asXDYOPfRX4tvRezTgJfy7CC-w.&amp;_di_=srdl6dr3ueai2v79l3htcsbah05d839pukqgasomkong7v7t60q0"
                                                                                                                                style="margin:0;Margin:0;color:#222222;text-decoration:underline;text-decoration-color:#222222;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px"
                                                                                                                                target="_blank">Android</a>
                                                                                                                        </p>
                                                                                                                    </th>
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                        <table
                                                                                            class="m_8214844979060577330footer-preferences"
                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                            width="100%" valign="top"
                                                                                            align="left">
                                                                                            <tbody>
                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                    valign="top" align="left">
                                                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-right:8px;padding-bottom:0;margin:0 auto;padding-top:36px;width:33.33333%;padding-left:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <p
                                                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:11px;line-height:14px;text-align:center">
                                                                                                                            <a href="https://email.farfetch.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTCQGzaeo8O8Rzcqudh3df5d4uoWKG1Sm6GduWo9n5RDols8rgzgH4O0fo8VXtpKX%3DWDTABAWY&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmfJHJMslcpD7sCeaoatYQClSZZkef8ZkpbId1JXS24xc4gxON1asXDYOPfRX4tvRezTgJfy7CC-w.&amp;_di_=52qkc9sjt64ai44g8057a6663967g7309nub6iva1jeoe9attmq0"
                                                                                                                                style="margin:0;Margin:0;color:#222222;text-decoration-color:#222222;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px;text-decoration:none"
                                                                                                                                target="_blank">
                                                                                                                                Email
                                                                                                                                preferences
                                                                                                                            </a>
                                                                                                                        </p>
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-right:8px;padding-bottom:0;padding-left:8px;margin:0 auto;padding-top:36px;width:33.33333%"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <p
                                                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:11px;line-height:14px;text-align:center">
                                                                                                                            <a href="https://email.farfetch.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTCQGzaeo8O8Rzcqudh3df5d4uoWKG1Sm6GduWo9n5RDols8rgzgH4O0fo8VXtpKX%3DYABWWCY&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmfJHJMslcpD7sCeaoatYQClSZZkef8ZkpbId1JXS24xc4gxON1asXDYOPfRX4tvRezTgJfy7CC-w.&amp;_di_=fd9rsm5fhr8rvvhsdngd2ilrbnsispvjd4hs22orf16atkcg9mu0"
                                                                                                                                style="margin:0;Margin:0;color:#222222;text-decoration-color:#222222;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px;text-decoration:none"
                                                                                                                                target="_blank">
                                                                                                                                My
                                                                                                                                account
                                                                                                                            </a>
                                                                                                                        </p>
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;padding-left:8px;margin:0 auto;padding-top:36px;width:33.33333%;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <p
                                                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:11px;line-height:14px;text-align:center">
                                                                                                                            <a href="https://email.farfetch.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTCQGzaeo8O8Rzcqudh3df5d4uoWKG1Sm6GduWo9n5RDols8rgzgH4O0fo8VXtpKX%3DYABWBWY&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmfJHJMslcpD7sCeaoatYQClSZZkef8ZkpbId1JXS24xc4gxON1asXDYOPfRX4tvRezTgJfy7CC-w.&amp;_di_=hec56vgqdlac7jaagljgj1f5ts95tfit9bkq5g6m8lkvdsi3t320"
                                                                                                                                style="margin:0;Margin:0;color:#222222;text-decoration-color:#222222;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px;text-decoration:none"
                                                                                                                                target="_blank">
                                                                                                                                Contact
                                                                                                                                us
                                                                                                                            </a>
                                                                                                                        </p>
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                        <table
                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;padding:0;width:100%;display:table"
                                                                                            width="100%" valign="top"
                                                                                            align="left">
                                                                                            <tbody>
                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                    valign="top" align="left">
                                                                                                    <th class="m_8214844979060577330small-12 m_8214844979060577330columns m_8214844979060577330first"
                                                                                                        style="word-wrap:break-word;border-collapse:collapse;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;Margin:0;padding-bottom:0;margin:0 auto;padding-top:36px;width:100%;padding-left:0;padding-right:0"
                                                                                                        valign="top"
                                                                                                        align="left">
                                                                                                        <table
                                                                                                            style="border-spacing:0;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;width:100%"
                                                                                                            width="100%"
                                                                                                            valign="top"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr style="padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left"
                                                                                                                    valign="top"
                                                                                                                    align="left">
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                        <p
                                                                                                                            style="margin:0;Margin:0;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:center;font-size:9px;line-height:16px">
                                                                                                                            FARFETCH
                                                                                                                            Europe
                                                                                                                            Trading
                                                                                                                            B.V.,
                                                                                                                            Joop
                                                                                                                            Geesinkweg
                                                                                                                            701,
                                                                                                                            1114AB
                                                                                                                            Amsterdam-Duivendrecht,
                                                                                                                            Netherlands<br
                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px">Company
                                                                                                                            no.
                                                                                                                            45279195<br
                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px">Please
                                                                                                                            note
                                                                                                                            this
                                                                                                                            is
                                                                                                                            our
                                                                                                                            registered
                                                                                                                            office
                                                                                                                            and
                                                                                                                            returns
                                                                                                                            cannot
                                                                                                                            be
                                                                                                                            accepted
                                                                                                                            here.<br
                                                                                                                                style="font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;text-align:left;font-size:11px;line-height:14px">&#xA9;
                                                                                                                            2025
                                                                                                                            FARFETCH
                                                                                                                            Europe
                                                                                                                            Trading
                                                                                                                            B.V.
                                                                                                                        </p>
                                                                                                                    </th>
                                                                                                                    <th style="word-wrap:break-word;border-collapse:collapse;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0;vertical-align:top;text-align:left;font-family:'FarfetchBasis-Regular','Helvetica Neue',Arial,sans-serif;font-weight:400;font-size:16px;line-height:22px;margin:0;Margin:0;width:0;padding:0"
                                                                                                                        valign="top"
                                                                                                                        align="left">
                                                                                                                    </th>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </th>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                    </th>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </th>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </center>
                                </td>
                            </tr>
                        </tbody>
                    </table>
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
