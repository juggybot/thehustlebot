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
    msg['From'] = formataddr((f'Foot Locker', sender_email))
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
    "Please enter the order date (July 19, 2024):",
    "Please enter the customer name (Juggy Resells):",
    "Please enter the street address (10 Test Street):",
    "Please enter the suburb (North Owenland):",
    "Please enter the state & postcode (NSW 2000):",
    "Please enter the image url (MUST BE FROM FOOTLOCKER SITE):",
    "Please enter the product name (Nike Dunk Low):",
    "Please enter the product size (37,5):",
    "Please enter the product price (WITHOUT THE $ SIGN):",
    "Please enter the shipping price (WITHOUT THE $ SIGN):",
    "Please enter the tax type (GST/VAT/SALES TAX):",
    "Please enter the tax amount (WITHOUT THE $ SIGN):",
    "Please enter the order total (WITHOUT THE $ SIGN):",
    "Please enter the currency (AUD/EUR/USD):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira a data do pedido (19 de julho de 2024):",
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira o endereço (10 Test Street):",
    "Por favor, insira o bairro (North Owenland):",
    "Por favor, insira o estado e CEP (NSW 2000):",
    "Por favor, insira a URL da imagem (DEVE SER DO SITE DA FOOTLOCKER):",
    "Por favor, insira o nome do produto (Nike Dunk Low):",
    "Por favor, insira o tamanho do produto (37,5):",
    "Por favor, insira o preço do produto (SEM O SINAL $):",
    "Por favor, insira o valor do frete (SEM O SINAL $):",
    "Por favor, insira o tipo de imposto (GST/VAT/SALES TAX):",
    "Por favor, insira o valor do imposto (SEM O SINAL $):",
    "Por favor, insira o total do pedido (SEM O SINAL $):",
    "Por favor, insira a moeda (AUD/EUR/USD):",
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
    part1 = random.randint(11111111111111111111, 99999999999999999999)  # Random 10-digit number

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
    recipient_email = f'{user_inputs[14]}'
    subject = f"Get ready – your Foot Locker order is on its way"
    html_template = f"""
        <div style="margin:0;padding:0">
        <table id="m_-7397014659233970794wrapper-table" width="100%" cellspacing="0" cellpadding="0" border="0"
            style="border-collapse:collapse;margin:0;padding:0">
            <tbody>
                <tr>
                    <td align="center" style="border-collapse:collapse">
                        <table id="m_-7397014659233970794content-table" width="600" align="center" cellspacing="0"
                            cellpadding="0" border="0" style="border-collapse:collapse">
                            <tbody>
                                <tr>
                                    <td id="m_-7397014659233970794content-cell" align="center"
                                        style="border-collapse:collapse">
                                        <table class="m_-7397014659233970794row" bgcolor="#ffffff"
                                            id="m_-7397014659233970794widget_3a5468cdfc6a48ef69ab1bf3f67db855" width="600"
                                            align="center" cellspacing="0" cellpadding="0" border="0"
                                            style="border-collapse:collapse">
                                            <tbody>
                                                <tr>
                                                    <td class="m_-7397014659233970794widget_top_bottom_padding"
                                                        style="border-collapse:collapse;padding-top:40px;padding-bottom:10px">
                                                        <table class="m_-7397014659233970794col-12" width="600"
                                                            align="center" cellspacing="0" cellpadding="0" border="0"
                                                            style="border-collapse:collapse;border-left:1px;border-right:1px">
                                                            <tbody>
                                                                <tr>
                                                                    <td style="border-collapse:collapse">
                                                                        <table class="m_-7397014659233970794block-content"
                                                                            width="100%" align="center" cellspacing="0"
                                                                            cellpadding="0" border="0"
                                                                            style="border-collapse:collapse;width:100%;text-align:center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center"
                                                                                        class="m_-7397014659233970794image-widget-content"
                                                                                        style="border-collapse:collapse;padding-left:0px;padding-right:0px;line-height:1px;font-size:1px">
                                                                                        <a href=""
                                                                                            target="_blank"><img
                                                                                                class="m_-7397014659233970794mobile-width"
                                                                                                src="https://partner-images.bluecore.com/footlocker/FL_Logo.png"
                                                                                                alt="Foot Locker Logo"
                                                                                                border="0"
                                                                                                style="display:block;height:auto;line-height:100%;text-decoration:none;outline:none;border:0 none;font-size:initial"
                                                                                                width="180"
                                                                                                height="auto"></a></td>
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
                                        <table bgcolor="#ffffff" class="m_-7397014659233970794row"
                                            id="m_-7397014659233970794widget_029695f8243620828df4d4edc05eef89" width="600"
                                            align="center" cellspacing="0" cellpadding="0" border="0"
                                            style="border-collapse:collapse">
                                            <tbody>
                                                <tr>
                                                    <td class="m_-7397014659233970794widget_top_bottom_padding"
                                                        style="border-collapse:collapse;padding-top:20px;padding-bottom:20px">
                                                        <table class="m_-7397014659233970794col-12" width="600" align="left"
                                                            cellspacing="0" cellpadding="0" border="0"
                                                            style="border-collapse:collapse;border-left:1px;border-right:1px">
                                                            <tbody>
                                                                <tr>
                                                                    <td style="border-collapse:collapse">
                                                                        <table class="m_-7397014659233970794block-content"
                                                                            width="100%" align="center" cellspacing="0"
                                                                            cellpadding="0" border="0"
                                                                            style="border-collapse:collapse;width:100%;text-align:center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center"
                                                                                        style="border-collapse:collapse;font-size:14px;line-height:24px;letter-spacing:0.0em;text-transform:none;padding-left:0px;padding-right:0px">
                                                                                        <p style="margin:0!important"></p>
                                                                                        <p style="margin:0!important;color:#0e1111;text-align:center"
                                                                                            align="center"><span
                                                                                                style="font-family:&#39;Roboto Regular&#39;,Arial,Helvetica,sans-serif;color:#0e1111">
                                                                                                Order: {order_num}
                                                                                            </span> <br><span
                                                                                                style="font-family:&#39;Roboto Regular&#39;,Arial,Helvetica,sans-serif;color:#757575">
                                                                                                Purchase date: {user_inputs[0]}
                                                                                            </span></p>
                                                                                        <p style="margin:0!important"></p>
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
                                        <table bgcolor="#ffffff" class="m_-7397014659233970794row"
                                            id="m_-7397014659233970794widget_ecf454aa46c6ed486983175fd6bb8628" width="600"
                                            align="center" cellspacing="0" cellpadding="0" border="0"
                                            style="border-collapse:collapse">
                                            <tbody>
                                                <tr>
                                                    <td class="m_-7397014659233970794widget_top_bottom_padding"
                                                        style="border-collapse:collapse;padding-top:10px;padding-bottom:10px">
                                                        <table class="m_-7397014659233970794col-12" width="600" align="left"
                                                            cellspacing="0" cellpadding="0" border="0"
                                                            style="border-collapse:collapse;border-left:1px;border-right:1px">
                                                            <tbody>
                                                                <tr>
                                                                    <td style="border-collapse:collapse">
                                                                        <table class="m_-7397014659233970794block-content"
                                                                            width="100%" align="center" cellspacing="0"
                                                                            cellpadding="0" border="0"
                                                                            style="border-collapse:collapse;width:100%;text-align:center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center"
                                                                                        style="border-collapse:collapse;font-size:23px;line-height:24px;letter-spacing:0.0em;text-transform:none;padding-left:0px;padding-right:0px">
                                                                                        <h1
                                                                                            style="text-align:center;color:#0e1111;font-size:20px;margin:0">
                                                                                            <span
                                                                                                style="font-family:&#39;Footlocker Classic - Header Regular&#39;,Arial,Helvetica,sans-serif"><b><span
                                                                                                        style="color:#0e1111">We’re
                                                                                                        working on your
                                                                                                        order
                                                                                                        now</span></b></span>
                                                                                        </h1>
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
                                        <table bgcolor="#ffffff" class="m_-7397014659233970794row"
                                            id="m_-7397014659233970794widget_30501f3658045bd1d85b910f80f473b1" width="600"
                                            align="center" cellspacing="0" cellpadding="0" border="0"
                                            style="border-collapse:collapse">
                                            <tbody>
                                                <tr>
                                                    <td class="m_-7397014659233970794widget_top_bottom_padding"
                                                        style="border-collapse:collapse;padding-top:0px;padding-bottom:20px">
                                                        <table class="m_-7397014659233970794col-12" width="600" align="left"
                                                            cellspacing="0" cellpadding="0" border="0"
                                                            style="border-collapse:collapse;border-left:1px;border-right:1px">
                                                            <tbody>
                                                                <tr>
                                                                    <td style="border-collapse:collapse">
                                                                        <table class="m_-7397014659233970794block-content"
                                                                            width="100%" align="center" cellspacing="0"
                                                                            cellpadding="0" border="0"
                                                                            style="border-collapse:collapse;width:100%;text-align:center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center"
                                                                                        style="border-collapse:collapse;font-size:16px;line-height:20px;letter-spacing:0.0em;text-transform:none;padding-left:0px;padding-right:0px">
                                                                                        <p style="margin:0!important;text-align:center;color:#0e1111"
                                                                                            align="center"><span
                                                                                                style="font-family:&#39;Footlocker Standard - Body  Regular&#39;,Arial,Helvetica,sans-serif;color:#0e1111"
                                                                                                role="text">Thank you for
                                                                                                shopping with us</span></p>
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
                                        <table class="m_-7397014659233970794row"
                                            id="m_-7397014659233970794widget_78d81cbb58c335338f39c4a1eaa9b3e7"
                                            bgcolor="#ffffff" width="600" align="center" cellspacing="0" cellpadding="0"
                                            border="0" style="border-collapse:collapse">
                                            <tbody>
                                                <tr>
                                                    <td class="m_-7397014659233970794widget_top_bottom_padding"
                                                        style="border-collapse:collapse;padding-top:10px;padding-bottom:40px">
                                                        <table class="m_-7397014659233970794col-12" width="600"
                                                            align="center" cellspacing="0" cellpadding="0" border="0"
                                                            style="border-collapse:collapse;border-left:1px;border-right:1px">
                                                            <tbody>
                                                                <tr>
                                                                    <td class="m_-7397014659233970794button-container"
                                                                        align="center"
                                                                        style="border-collapse:collapse;padding-left:0px;padding-right:0px">
                                                                        <table
                                                                            class="m_-7397014659233970794text-button-content"
                                                                            align="center" cellspacing="0" cellpadding="0"
                                                                            border="0" style="border-collapse:initial">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" valign="middle"
                                                                                        style="border-collapse:collapse;background-color:#0e1111;color:#ffffff;letter-spacing:0.05em;line-height:18px;border-radius:2px"
                                                                                        bgcolor="#0E1111">
                                                                                        <a href="https://trk.bc.footlocker.com.au/ss/c/hVHNotmYA35oKI7Og-SINmL9PFqZICMffvOK7iWqlUas0XfibKgO_BhuIIefXvntTxapAiv_S8_KxaHdaOK-9Q/3xz/IjRlaBFTTBGAlFfnOfvaOA/h1/nVRCq27m0L2d5ZSf6Ca0TFqg0BaAuto3l1uC-hJwouU"
                                                                                            style="display:block;color:#ffffff;text-decoration:none;font-family:&#39;Footlocker Classic - Header Regular&#39;,Arial,Helvetica,sans-serif;font-size:16px;line-height:18px;border-top:13px solid #0e1111;border-bottom:13px solid #0e1111;border-left:78px solid #0e1111;border-right:78px solid #0e1111;border-radius:2px"
                                                                                            target="_blank">CHECK ORDER
                                                                                            STATUS</a>
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
                                        <span>
                                            <table border="0" role="presentation" cellpadding="0" cellspacing="0"
                                                width="100%" style="border-collapse:collapse">
                                                <tbody>
                                                    <tr style="page-break-before:always">
                                                        <td align="center" valign="top" width="100%" cellpadding="0"
                                                            style="background-color:#f5f5f5;font-size:16px;line-height:16px;border-collapse:collapse"
                                                            bgcolor="#F5F5F5">
                                                            <table cellpadding="10" role="presentation" cellspacing="0"
                                                                width="100%" style="border-collapse:collapse">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="border-collapse:collapse">
                                                                            <table class="m_-7397014659233970794fluid-row"
                                                                                role="presentation" width="100%"
                                                                                align="center" cellspacing="0"
                                                                                cellpadding="0" border="0" bgcolor="#f5f5f5"
                                                                                style="border-collapse:collapse;padding-top:10px;padding-bottom:20px">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td
                                                                                            style="border-collapse:collapse">
                                                                                            <table
                                                                                                class="m_-7397014659233970794col-12"
                                                                                                role="presentation"
                                                                                                width="560" align="center"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                style="border-collapse:collapse;border-left:1px;border-right:1px">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td
                                                                                                            style="border-collapse:collapse;padding-top:32px;padding-bottom:0px">
                                                                                                            <table
                                                                                                                class="m_-7397014659233970794block-content"
                                                                                                                role="presentation"
                                                                                                                align="center"
                                                                                                                cellspacing="0"
                                                                                                                cellpadding="0"
                                                                                                                border="0"
                                                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                                                width="100%">
                                                                                                                <tbody>
                                                                                                                    <tr>
                                                                                                                        <td style="border-collapse:collapse;text-align:center"
                                                                                                                            align="center">
                                                                                                                            <h2
                                                                                                                                style="font-family:&#39;Roboto Bold&#39;,Arial,Helvetica,sans-serif;color:#0e1111;font-size:18px;line-height:22px;letter-spacing:0.5px;margin:0">
                                                                                                                                <span
                                                                                                                                    style="font-family:&#39;Roboto Bold&#39;,Arial,Helvetica,sans-serif;color:#0e1111;font-size:18px;line-height:22px;letter-spacing:0.5px"><b><span
                                                                                                                                            style="font-family:&#39;Roboto Bold&#39;,Arial,Helvetica,sans-serif;color:#0e1111">Delivery</span></b></span>
                                                                                                                            </h2>
                                                                                                                        </td>
                                                                                                                    </tr>
                                                                                                                </tbody>
                                                                                                            </table>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                            <table
                                                                                                class="m_-7397014659233970794row-spacer"
                                                                                                role="presentation"
                                                                                                width="100%" align="center"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                style="border-collapse:collapse">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td height="0"
                                                                                                            style="border-collapse:collapse">
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                            <table
                                                                                                class="m_-7397014659233970794col-12"
                                                                                                width="560"
                                                                                                role="presentation"
                                                                                                align="center"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                style="border-collapse:collapse;border-left:1px;border-right:1px">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td
                                                                                                            style="border-collapse:collapse;padding-top:16px;padding-bottom:0px">
                                                                                                            <table
                                                                                                                class="m_-7397014659233970794block-content"
                                                                                                                role="presentation"
                                                                                                                align="center"
                                                                                                                cellspacing="0"
                                                                                                                cellpadding="0"
                                                                                                                border="0"
                                                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                                                width="100%">
                                                                                                                <tbody>
                                                                                                                    <tr>
                                                                                                                        <td style="border-collapse:collapse;text-align:center"
                                                                                                                            align="center">
                                                                                                                            <span><b><span
                                                                                                                                        style="font-family:&#39;Roboto Bold&#39;,Arial,Helvetica,sans-serif;color:#0e1111"><img
                                                                                                                                            width="320"
                                                                                                                                            alt="Package status – Processing"
                                                                                                                                            src="https://partner-images.bluecore.com/footlocker/Delivery.png"
                                                                                                                                            style="border:0 none;height:auto;line-height:100%;text-decoration:none;outline:none;display:inline-block"
                                                                                                                                            height="auto"></span></b></span>
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
                                                                            <table class="m_-7397014659233970794fluid-row"
                                                                                role="presentation" width="100%"
                                                                                align="center" cellspacing="0"
                                                                                cellpadding="0" border="0" bgcolor="#f5f5f5"
                                                                                style="border-collapse:collapse;padding-top:10px;padding-bottom:20px">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td
                                                                                            style="border-collapse:collapse">
                                                                                            <table
                                                                                                class="m_-7397014659233970794row-spacer"
                                                                                                role="presentation"
                                                                                                width="100%" align="center"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                style="border-collapse:collapse">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td height="24"
                                                                                                            style="border-collapse:collapse">
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                            <table
                                                                                                class="m_-7397014659233970794col-12"
                                                                                                role="presentation"
                                                                                                width="560" align="center"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                style="border-collapse:collapse;border-left:1px;border-right:1px">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td
                                                                                                            style="border-collapse:collapse;padding-top:0px;padding-bottom:0px">
                                                                                                            <table
                                                                                                                class="m_-7397014659233970794block-content"
                                                                                                                role="presentation"
                                                                                                                align="center"
                                                                                                                cellspacing="0"
                                                                                                                cellpadding="0"
                                                                                                                border="0"
                                                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                                                width="100%">
                                                                                                                <tbody>
                                                                                                                    <tr>
                                                                                                                        <td style="border-collapse:collapse;text-align:left"
                                                                                                                            align="left">
                                                                                                                            <h3
                                                                                                                                style="font-family:&#39;Roboto Medium&#39;,Arial,Helvetica,sans-serif;color:#515151;font-size:12px;line-height:16px;text-transform:uppercase;letter-spacing:0.08em;margin:0">
                                                                                                                                <span
                                                                                                                                    style="font-family:&#39;Roboto Medium&#39;,Arial,Helvetica,sans-serif;color:#515151;font-size:12px;line-height:16px;text-transform:uppercase;letter-spacing:0.08em"><b>SHIPPING
                                                                                                                                        TO:</b></span>
                                                                                                                            </h3>
                                                                                                                        </td>
                                                                                                                    </tr>
                                                                                                                </tbody>
                                                                                                            </table>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                            <table
                                                                                                class="m_-7397014659233970794row-spacer"
                                                                                                role="presentation"
                                                                                                width="100%" align="center"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                style="border-collapse:collapse">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td height="12"
                                                                                                            style="border-collapse:collapse">
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                            <table
                                                                                                class="m_-7397014659233970794col-12"
                                                                                                role="presentation"
                                                                                                width="560" align="center"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                style="border-collapse:collapse;border-left:1px;border-right:1px;border-radius:5px"
                                                                                                bgcolor="#ffffff">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td
                                                                                                            style="border-collapse:collapse;padding-top:12px;padding-bottom:12px;border-bottom:1px solid #dddddd">
                                                                                                            <table
                                                                                                                class="m_-7397014659233970794block-content"
                                                                                                                role="presentation"
                                                                                                                align="center"
                                                                                                                cellspacing="0"
                                                                                                                cellpadding="0"
                                                                                                                border="0"
                                                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                                                width="100%">
                                                                                                                <tbody>
                                                                                                                    <tr>
                                                                                                                        <td style="border-collapse:collapse;text-align:left;padding-left:16px;padding-right:0px"
                                                                                                                            width="20"
                                                                                                                            align="left">
                                                                                                                            <img alt="Location"
                                                                                                                                width="20"
                                                                                                                                style="border:0 none;height:auto;line-height:100%;text-decoration:none;outline:none;vertical-align:middle;display:inline-block"
                                                                                                                                src="https://partner-images.bluecore.com/eastbay_teamsales_us/location-fill.png"
                                                                                                                                height="auto">
                                                                                                                        </td>
                                                                                                                        <td style="border-collapse:collapse;text-align:left;padding-left:5px;padding-right:16px"
                                                                                                                            align="left">
                                                                                                                            <span
                                                                                                                                style="font-family:&#39;Roboto Regular&#39;,Arial,Helvetica,sans-serif;color:#0e1111;vertical-align:middle;font-size:14px;margin-left:0px">
                                                                                                                                {user_inputs[1]}</span>
                                                                                                                        </td>
                                                                                                                    </tr>
                                                                                                                </tbody>
                                                                                                            </table>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                    <tr>
                                                                                                        <td
                                                                                                            style="border-collapse:collapse;padding-top:12px;padding-bottom:12px">
                                                                                                            <table
                                                                                                                class="m_-7397014659233970794block-content"
                                                                                                                role="presentation"
                                                                                                                align="center"
                                                                                                                cellspacing="0"
                                                                                                                cellpadding="0"
                                                                                                                border="0"
                                                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                                                width="100%">
                                                                                                                <tbody>
                                                                                                                    <tr>
                                                                                                                        <td style="border-collapse:collapse;text-align:left;padding-left:16px;padding-right:16px"
                                                                                                                            align="left">
                                                                                                                            <span
                                                                                                                                style="font-family:&#39;Roboto&#39;,Arial,Helvetica,sans-serif;color:#0e1111;vertical-align:middle;font-size:14px;line-height:20px;font-weight:400">
                                                                                                                                {user_inputs[2]}
                                                                                                                                ,
                                                                                                                                {user_inputs[3]},
                                                                                                                                {user_inputs[4]}</span>
                                                                                                                        </td>
                                                                                                                    </tr>
                                                                                                                </tbody>
                                                                                                            </table>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                            <table
                                                                                                class="m_-7397014659233970794row-spacer"
                                                                                                role="presentation"
                                                                                                width="100%" align="center"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                style="border-collapse:collapse">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td height="32"
                                                                                                            style="border-collapse:collapse">
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                            <table
                                                                                                class="m_-7397014659233970794col-12"
                                                                                                width="560"
                                                                                                role="presentation"
                                                                                                align="center"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                style="border-collapse:collapse;border-radius:4px;border-left:1px;border-right:1px"
                                                                                                bgcolor="#ffffff">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td
                                                                                                            style="border-collapse:collapse;padding-top:12px;padding-bottom:12px;padding-left:16px;padding-right:16px">
                                                                                                            <table
                                                                                                                class="m_-7397014659233970794block-content"
                                                                                                                role="presentation"
                                                                                                                align="center"
                                                                                                                cellspacing="0"
                                                                                                                cellpadding="0"
                                                                                                                border="0"
                                                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                                                width="100%">
                                                                                                                <tbody>
                                                                                                                    <tr>
                                                                                                                        <td style="border-collapse:collapse;text-align:left"
                                                                                                                            align="left">
                                                                                                                            <span
                                                                                                                                style="font-family:&#39;Roboto&#39;,Arial,Helvetica,sans-serif;color:#0e1111;font-size:14px;line-height:20px;font-weight:400">You’ll
                                                                                                                                get
                                                                                                                                a
                                                                                                                                tracking
                                                                                                                                number
                                                                                                                                as
                                                                                                                                each
                                                                                                                                package
                                                                                                                                ships.</span>
                                                                                                                        </td>
                                                                                                                    </tr>
                                                                                                                </tbody>
                                                                                                            </table>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                            <table
                                                                                                class="m_-7397014659233970794row-spacer"
                                                                                                role="presentation"
                                                                                                width="100%" align="center"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                style="border-collapse:collapse">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td height="32"
                                                                                                            style="border-collapse:collapse">
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                        </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                            <table class="m_-7397014659233970794fluid-row"
                                                                                width="560" role="presentation"
                                                                                align="center" cellspacing="0"
                                                                                cellpadding="0" border="0" bgcolor="#f5f5f5"
                                                                                style="border-collapse:collapse">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td
                                                                                            style="border-collapse:collapse">
                                                                                            <table
                                                                                                class="m_-7397014659233970794col-3"
                                                                                                width="100"
                                                                                                role="presentation"
                                                                                                height="114" align="left"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                style="border-collapse:collapse;border-left:1px;border-right:1px;background:#ffffff;padding:10px;border-radius:5px">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td
                                                                                                            style="border-collapse:collapse">
                                                                                                            <table
                                                                                                                class="m_-7397014659233970794block-content"
                                                                                                                role="presentation"
                                                                                                                align="center"
                                                                                                                cellspacing="0"
                                                                                                                cellpadding="0"
                                                                                                                border="0"
                                                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                                                width="100%">
                                                                                                                <tbody>
                                                                                                                    <tr>
                                                                                                                        <td align="left"
                                                                                                                            style="border-collapse:collapse;font-family:&#39;Roboto Regular&#39;,Arial,Helvetica,sans-serif">
                                                                                                                            <a href=""
                                                                                                                                target="_blank">
                                                                                                                                <img width="68"
                                                                                                                                    alt=""
                                                                                                                                    src="{user_inputs[5]}"
                                                                                                                                    style="display:block;height:auto;line-height:100%;text-decoration:none;outline:none;border:0 none;margin:0 auto"
                                                                                                                                    height="auto">
                                                                                                                            </a>
                                                                                                                        </td>
                                                                                                                    </tr>
                                                                                                                </tbody>
                                                                                                            </table>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                            <table
                                                                                                class="m_-7397014659233970794col-9"
                                                                                                width="456"
                                                                                                role="presentation"
                                                                                                align="right"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                style="border-collapse:collapse;border-left:1px;border-right:1px">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td
                                                                                                            style="border-collapse:collapse">
                                                                                                            <table
                                                                                                                class="m_-7397014659233970794block-content"
                                                                                                                role="presentation"
                                                                                                                align="center"
                                                                                                                cellspacing="0"
                                                                                                                cellpadding="0"
                                                                                                                border="0"
                                                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                                                width="100%">
                                                                                                                <tbody>
                                                                                                                    <tr>
                                                                                                                        <td align="left"
                                                                                                                            style="border-collapse:collapse;font-family:&#39;Roboto Regular&#39;,Arial,Helvetica,sans-serif;color:#0e1111;font-size:16px;line-height:20px;padding-top:12px;padding-bottom:4px;padding-left:16px">
                                                                                                                            <a href="https://trk.bc.footlocker.com.au/ss/c/hVHNotmYA35oKI7Og-SINmL9PFqZICMffvOK7iWqlUbFEKseeGoTQs4_pyX3FhPm_G2Tfphae1qgtFLFZM3Ejw/3xz/IjRlaBFTTBGAlFfnOfvaOA/h3/rvWVZV-lFqyuoKnNRZOm0vrOJ7ML6cSv26rMV79PT5A"
                                                                                                                                style="font-family:&#39;Roboto Regular&#39;,Arial,Helvetica,sans-serif;color:#0e1111;font-size:16px;line-height:20px;text-decoration:none"
                                                                                                                                target="_blank">{user_inputs[6]}
                                                                                                                            </a>
                                                                                                                        </td>
                                                                                                                    </tr>
                                                                                                                </tbody>
                                                                                                            </table>
                                                                                                            <table
                                                                                                                class="m_-7397014659233970794block-content"
                                                                                                                role="presentation"
                                                                                                                align="center"
                                                                                                                cellspacing="0"
                                                                                                                cellpadding="0"
                                                                                                                border="0"
                                                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                                                width="100%">
                                                                                                                <tbody>
                                                                                                                    <tr>
                                                                                                                        <td align="left"
                                                                                                                            style="border-collapse:collapse;font-family:&#39;Roboto Regular&#39;,Arial,Helvetica,sans-serif;color:#0e1111;font-size:12px;line-height:16px;padding-top:4px;padding-bottom:4px;padding-left:16px">
                                                                                                                            Size
                                                                                                                            <span
                                                                                                                                style="font-family:&#39;Roboto Regular&#39;,Arial,Helvetica,sans-serif;color:#515151">
                                                                                                                                {user_inputs[7]}</span>
                                                                                                                        </td>
                                                                                                                    </tr>
                                                                                                                </tbody>
                                                                                                            </table>
                                                                                                            <table
                                                                                                                class="m_-7397014659233970794block-content"
                                                                                                                role="presentation"
                                                                                                                align="center"
                                                                                                                cellspacing="0"
                                                                                                                cellpadding="0"
                                                                                                                border="0"
                                                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                                                width="100%">
                                                                                                                <tbody>
                                                                                                                    <tr>
                                                                                                                        <td align="left"
                                                                                                                            style="border-collapse:collapse;font-family:&#39;Roboto Regular&#39;,Arial,Helvetica,sans-serif;color:#0e1111;font-size:12px;line-height:16px;padding-top:4px;padding-bottom:4px;padding-left:16px">
                                                                                                                            Qty
                                                                                                                            <span
                                                                                                                                style="font-family:&#39;Roboto Regular&#39;,Arial,Helvetica,sans-serif;color:#515151">
                                                                                                                                1</span>
                                                                                                                        </td>
                                                                                                                    </tr>
                                                                                                                </tbody>
                                                                                                            </table>
                                                                                                            <table
                                                                                                                class="m_-7397014659233970794block-content"
                                                                                                                role="presentation"
                                                                                                                align="center"
                                                                                                                cellspacing="0"
                                                                                                                cellpadding="0"
                                                                                                                border="0"
                                                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                                                width="100%">
                                                                                                                <tbody>
                                                                                                                    <tr>
                                                                                                                        <td align="left"
                                                                                                                            style="border-collapse:collapse;padding-top:4px;padding-bottom:12px;padding-left:16px">
                                                                                                                            <span
                                                                                                                                style="font-family:&#39;Robotomono Regular&#39;,Arial,Helvetica,sans-serif;color:#0e1111;font-size:12px;line-height:16px">{user_inputs[13]}
                                                                                                                                {user_inputs[8]}</span>
                                                                                                                        </td>
                                                                                                                    </tr>
                                                                                                                </tbody>
                                                                                                            </table>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                            <table
                                                                                                class="m_-7397014659233970794row-spacer"
                                                                                                width="100%"
                                                                                                role="presentation"
                                                                                                align="center"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                style="border-collapse:collapse">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td height="12"
                                                                                                            style="border-collapse:collapse">
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                            <table
                                                                                                class="m_-7397014659233970794col-12"
                                                                                                width="560" align="center"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                style="border-collapse:collapse;border-left:1px;border-right:1px;border-radius:5px"
                                                                                                bgcolor="#ffffff">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td
                                                                                                            style="border-collapse:collapse;padding-top:12px;padding-bottom:12px">
                                                                                                            <table
                                                                                                                class="m_-7397014659233970794block-content"
                                                                                                                align="center"
                                                                                                                cellspacing="0"
                                                                                                                cellpadding="0"
                                                                                                                border="0"
                                                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                                                width="100%">
                                                                                                                <tbody>
                                                                                                                    <tr>
                                                                                                                        <td style="border-collapse:collapse;text-align:left;padding-right:16px;padding-left:16px;font-family:&#39;Roboto Regular&#39;,Arial,Helvetica,sans-serif;color:#0e1111;font-size:14px;line-height:20px"
                                                                                                                            align="left">
                                                                                                                            <span
                                                                                                                                style="color:#0e1111">Arrives
                                                                                                                                in
                                                                                                                                5-7
                                                                                                                                Working
                                                                                                                                Days</span>
                                                                                                                            <br><span
                                                                                                                                style="font-size:12px;font-style:italic;color:#757575">(after
                                                                                                                                your
                                                                                                                                order
                                                                                                                                ships)</span>
                                                                                                                        </td>
                                                                                                                    </tr>
                                                                                                                </tbody>
                                                                                                            </table>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                            <table
                                                                                                class="m_-7397014659233970794row-spacer"
                                                                                                width="100%" align="center"
                                                                                                role="presentation"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                style="border-collapse:collapse">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td height="24"
                                                                                                            style="border-collapse:collapse">
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
                                                            <table cellpadding="1" cellspacing="0" width="100%"
                                                                role="presentation" style="border-collapse:collapse">
                                                                <tbody>
                                                                    <tr>
                                                                        <td height="1"
                                                                            style="border-collapse:collapse;border-bottom:1px solid #dddddd">
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </span> <span> </span>
                                        <table bgcolor="#F5F5F5" class="m_-7397014659233970794row"
                                            id="m_-7397014659233970794widget_65654a443646b6e28d255bcf97e1a956" width="600"
                                            align="center" cellspacing="0" cellpadding="0" border="0"
                                            style="border-collapse:collapse">
                                            <tbody>
                                                <tr>
                                                    <td class="m_-7397014659233970794widget_top_bottom_padding"
                                                        style="border-collapse:collapse;padding-top:32px;padding-bottom:24px">
                                                        <table class="m_-7397014659233970794col-12" width="600" align="left"
                                                            cellspacing="0" cellpadding="0" border="0"
                                                            style="border-collapse:collapse;border-left:1px;border-right:1px">
                                                            <tbody>
                                                                <tr>
                                                                    <td style="border-collapse:collapse">
                                                                        <table class="m_-7397014659233970794block-content"
                                                                            width="100%" align="center" cellspacing="0"
                                                                            cellpadding="0" border="0"
                                                                            style="border-collapse:collapse;width:100%;text-align:center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center"
                                                                                        style="border-collapse:collapse;font-size:16px;line-height:18px;letter-spacing:0.0em;text-transform:none;padding-left:16px;padding-right:16px">
                                                                                        <h2
                                                                                            style="color:#0e1111;text-align:left;font-size:16px;margin:0">
                                                                                            <b><span
                                                                                                    style="font-family:&#39;Roboto Bold&#39;,Arial,Helvetica,sans-serif;color:#0e1111">Order
                                                                                                    summary</span></b></h2>
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
                                        <span>
                                            <table class="m_-7397014659233970794fluid-row" role="presentation" width="600"
                                                align="center" cellspacing="0" cellpadding="0" border="0" bgcolor="#f5f5f5"
                                                style="border-collapse:collapse">
                                                <tbody>
                                                    <tr>
                                                        <td class="m_-7397014659233970794mobile-hide" width="10"
                                                            style="border-collapse:collapse"> </td>
                                                        <td class="m_-7397014659233970794desktop-hide" width="4"
                                                            style="border-collapse:collapse;display:none;padding:0;max-height:0;overflow:hidden;float:left;font-size:0;line-height:0">
                                                             </td>
                                                        <td style="border-collapse:collapse">
                                                            <table class="m_-7397014659233970794col-12" width="576"
                                                                align="left" role="presentation" cellspacing="0"
                                                                cellpadding="0" border="0"
                                                                style="border-collapse:collapse;border-left:1px;border-right:1px">
                                                                <tbody>
                                                                    <tr>
                                                                        <td width="50%"
                                                                            style="border-collapse:collapse;width:50%">
                                                                            <table
                                                                                class="m_-7397014659233970794block-content"
                                                                                role="presentation" align="center"
                                                                                cellspacing="0" cellpadding="0" border="0"
                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                width="100%">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td align="left"
                                                                                            style="border-collapse:collapse;font-family:&#39;Roboto Medium&#39;,Arial,Helvetica,sans-serif;color:#515151;font-size:12px;line-height:20px;padding-left:6px;padding-top:0px;padding-bottom:5px;letter-spacing:.08em">
                                                                                            SUBTOTAL <br> <span
                                                                                                style="font-family:&#39;Roboto Regular&#39;,Arial,Helvetica,sans-serif;color:#515151;padding-left:0px;padding-top:0px;padding-bottom:0px;letter-spacing:.08em">(1
                                                                                                item)</span> </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                        <td width="50%"
                                                                            style="border-collapse:collapse;width:50%">
                                                                            <table
                                                                                class="m_-7397014659233970794block-content"
                                                                                role="presentation" align="center"
                                                                                cellspacing="0" cellpadding="0" border="0"
                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                width="100%">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td align="right"
                                                                                            style="border-collapse:collapse;font-family:&#39;Robotomono Regular&#39;,Arial,Helvetica,sans-serif;color:#515151;font-size:12px;line-height:20px;padding-right:6px;padding-top:0px;padding-bottom:5px;height:40px"
                                                                                            height="40"> {user_inputs[13]} {user_inputs[8]}<br>
                                                                                        </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td width="50%"
                                                                            style="border-collapse:collapse;width:50%">
                                                                            <table
                                                                                class="m_-7397014659233970794block-content"
                                                                                role="presentation" align="center"
                                                                                cellspacing="0" cellpadding="0" border="0"
                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                width="100%">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td align="left"
                                                                                            style="border-collapse:collapse;font-family:&#39;Roboto Medium&#39;,Arial,Helvetica,sans-serif;color:#515151;font-size:12px;line-height:20px;padding-left:6px;letter-spacing:.08em;padding-top:10px;padding-bottom:10px">
                                                                                            SHIPPING </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                        <td width="50%"
                                                                            style="border-collapse:collapse;width:50%">
                                                                            <table
                                                                                class="m_-7397014659233970794block-content"
                                                                                role="presentation" align="center"
                                                                                cellspacing="0" cellpadding="0" border="0"
                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                width="100%">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td align="right"
                                                                                            style="border-collapse:collapse;font-family:&#39;Robotomono Regular&#39;,Arial,Helvetica,sans-serif;color:#515151;font-size:12px;line-height:20px;padding-right:6px;padding-top:10px;padding-bottom:10px">
                                                                                            {user_inputs[13]} {user_inputs[9]} </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td width="50%"
                                                                            style="border-collapse:collapse;width:50%">
                                                                            <table
                                                                                class="m_-7397014659233970794block-content"
                                                                                align="center" role="presentation"
                                                                                cellspacing="0" cellpadding="0" border="0"
                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                width="100%">
                                                                                <tbody>
                                                                                    <tr> </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                        <td width="50%"
                                                                            style="border-collapse:collapse;width:50%">
                                                                            <table
                                                                                class="m_-7397014659233970794block-content"
                                                                                align="center" role="presentation"
                                                                                cellspacing="0" cellpadding="0" border="0"
                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                width="100%">
                                                                                <tbody>
                                                                                    <tr> </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td width="50%"
                                                                            style="border-collapse:collapse;width:50%">
                                                                            <table
                                                                                class="m_-7397014659233970794block-content"
                                                                                align="center" role="presentation"
                                                                                cellspacing="0" cellpadding="0" border="0"
                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                width="100%">
                                                                                <tbody>
                                                                                    <tr> </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                        <td width="50%"
                                                                            style="border-collapse:collapse;width:50%">
                                                                            <table
                                                                                class="m_-7397014659233970794block-content"
                                                                                align="center" role="presentation"
                                                                                cellspacing="0" cellpadding="0" border="0"
                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                width="100%">
                                                                                <tbody>
                                                                                    <tr> </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td width="50%"
                                                                            style="border-collapse:collapse;width:50%">
                                                                            <table
                                                                                class="m_-7397014659233970794block-content"
                                                                                align="center" role="presentation"
                                                                                cellspacing="0" cellpadding="0" border="0"
                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                width="100%">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td align="left"
                                                                                            style="border-collapse:collapse;font-family:&#39;Roboto Medium&#39;,Arial,Helvetica,sans-serif;color:#515151;font-size:12px;line-height:20px;padding-left:6px;letter-spacing:.08em;padding-top:10px;padding-bottom:10px">
                                                                                            {user_inputs[10]} </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                        <td width="50%"
                                                                            style="border-collapse:collapse;width:50%">
                                                                            <table
                                                                                class="m_-7397014659233970794block-content"
                                                                                align="center" role="presentation"
                                                                                cellspacing="0" cellpadding="0" border="0"
                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                width="100%">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td align="right"
                                                                                            style="border-collapse:collapse;font-family:&#39;Robotomono Regular&#39;,Arial,Helvetica,sans-serif;color:#515151;font-size:12px;line-height:20px;padding-right:6px;padding-top:10px;padding-bottom:10px">
                                                                                            {user_inputs[13]} {user_inputs[11]} </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td width="50%"
                                                                            style="border-collapse:collapse;width:50%">
                                                                            <table
                                                                                class="m_-7397014659233970794block-content"
                                                                                align="center" role="presentation"
                                                                                cellspacing="0" cellpadding="0" border="0"
                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                width="100%">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td align="left"
                                                                                            style="border-collapse:collapse;font-family:&#39;Roboto Medium&#39;,Arial,Helvetica,sans-serif;color:#515151;font-size:12px;line-height:20px;padding-left:6px;letter-spacing:.08em;padding-top:10px;padding-bottom:10px">
                                                                                            <span
                                                                                                style="font-size:12px">TOTAL</span>
                                                                                        </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                        <td width="50%"
                                                                            style="border-collapse:collapse;width:50%">
                                                                            <table
                                                                                class="m_-7397014659233970794block-content"
                                                                                align="center" role="presentation"
                                                                                cellspacing="0" cellpadding="0" border="0"
                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                width="100%">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td align="right"
                                                                                            style="border-collapse:collapse;font-family:&#39;Robotomono Regular&#39;,Arial,Helvetica,sans-serif;color:#515151;font-size:12px;line-height:20px;padding-right:6px;padding-top:10px;padding-bottom:10px">
                                                                                            <span style="font-size:12px">{user_inputs[13]}
                                                                                                {user_inputs[12]} </span>
                                                                                        </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                        <td class="m_-7397014659233970794mobile-hide" width="10"
                                                            style="border-collapse:collapse"> </td>
                                                        <td class="m_-7397014659233970794desktop-hide" width="4"
                                                            style="border-collapse:collapse;display:none;padding:0;max-height:0;overflow:hidden;float:left;font-size:0;line-height:0">
                                                             </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </span>
                                        <table class="m_-7397014659233970794row-spacer" bgcolor="#f5f5f5"
                                            id="m_-7397014659233970794widget_c3419d1f4c281107ee9b12a11da58443" width="600"
                                            align="center" cellspacing="0" cellpadding="0" border="0"
                                            style="border-collapse:collapse">
                                            <tbody>
                                                <tr>
                                                    <td class="m_-7397014659233970794widget_bottom_padding m_-7397014659233970794widget_top_padding"
                                                        align="center"
                                                        style="border-collapse:collapse;padding-right:20px;padding-left:20px;padding-bottom:20px;padding-top:20px">
                                                        <table width="100%" align="center" cellspacing="0" cellpadding="0"
                                                            border="0" style="border-collapse:collapse">
                                                            <tbody>
                                                                <tr>
                                                                    <td height="1"
                                                                        style="border-collapse:collapse;border-bottom:1px solid #dddddd;line-height:1px;font-size:1px">
                                                                         </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <span>
                                            <table class="m_-7397014659233970794fluid-row" role="presentation" width="600"
                                                align="center" cellspacing="0" cellpadding="0" border="0" bgcolor="#f5f5f5"
                                                style="border-collapse:collapse">
                                                <tbody>
                                                    <tr>
                                                        <td class="m_-7397014659233970794mobile-hide" width="10"
                                                            style="border-collapse:collapse"> </td>
                                                        <td style="border-collapse:collapse">
                                                            <table class="m_-7397014659233970794col-3" role="presentation"
                                                                width="120" align="left" cellspacing="0" cellpadding="0"
                                                                border="0"
                                                                style="border-collapse:collapse;border-left:1px;border-right:1px">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="border-collapse:collapse">
                                                                            <table
                                                                                class="m_-7397014659233970794block-content"
                                                                                role="presentation" align="center"
                                                                                cellspacing="0" cellpadding="0" border="0"
                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                width="100%">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td align="left"
                                                                                            style="border-collapse:collapse;font-family:&#39;Roboto Bold&#39;,Arial,Helvetica,sans-serif;color:#515151;font-size:12px;line-height:20px;padding-left:10px;letter-spacing:.08em">
                                                                                            PAYMENT </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                            <table class="m_-7397014659233970794col-9" width="400"
                                                                role="presentation" align="right" cellspacing="0"
                                                                cellpadding="0" border="0"
                                                                style="border-collapse:collapse;border-left:1px;border-right:1px">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="border-collapse:collapse">
                                                                            <table
                                                                                class="m_-7397014659233970794block-content"
                                                                                role="presentation" align="center"
                                                                                cellspacing="0" cellpadding="0" border="0"
                                                                                style="border-collapse:collapse;width:100%;text-align:center"
                                                                                width="100%">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td align="right"
                                                                                            style="border-collapse:collapse;font-family:&#39;Roboto Regular&#39;,Arial,Helvetica,sans-serif;color:#515151;font-size:14px;line-height:28px;padding-right:10px;padding-bottom:8px">
                                                                                            <img width="40"
                                                                                                style="border:0 none;height:auto;line-height:100%;text-decoration:none;outline:none;vertical-align:middle;display:inline-block"
                                                                                                src="https://partner-images.bluecore.com/eastbay_teamsales_us/ic_afterpay.png"
                                                                                                alt="AFTERPAY"
                                                                                                height="auto">
                                                                                        </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                        <td class="m_-7397014659233970794mobile-hide"
                                                                            width="10" style="border-collapse:collapse"> 
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </span>
                                        <table class="m_-7397014659233970794row-spacer" bgcolor="#f5f5f5" width="600"
                                            align="center" cellspacing="0" cellpadding="0" border="0"
                                            style="border-collapse:collapse">
                                            <tbody>
                                                <tr>
                                                    <td height="30"
                                                        style="border-collapse:collapse;line-height:1px;font-size:1px"> 
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <table class="m_-7397014659233970794row-spacer" bgcolor="#f5f5f5"
                                            id="m_-7397014659233970794widget_a71f226c1548e97baafb152f43767ca8" width="600"
                                            align="center" cellspacing="0" cellpadding="0" border="0"
                                            style="border-collapse:collapse">
                                            <tbody>
                                                <tr>
                                                    <td class="m_-7397014659233970794widget_bottom_padding m_-7397014659233970794widget_top_padding"
                                                        align="center"
                                                        style="border-collapse:collapse;padding-right:0px;padding-left:0px">
                                                        <table width="100%" align="center" cellspacing="0" cellpadding="0"
                                                            border="0" style="border-collapse:collapse">
                                                            <tbody>
                                                                <tr>
                                                                    <td height="1"
                                                                        style="border-collapse:collapse;border-top:1px solid #dddddd;line-height:1px;font-size:1px">
                                                                         </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <table bgcolor="#f5f5f5" class="m_-7397014659233970794row"
                                            id="m_-7397014659233970794widget_2e60a34b1799b95ef0c43621627fa9d9" width="600"
                                            align="center" cellspacing="0" cellpadding="0" border="0"
                                            style="border-collapse:collapse">
                                            <tbody>
                                                <tr>
                                                    <td class="m_-7397014659233970794widget_top_bottom_padding"
                                                        style="border-collapse:collapse;padding-top:32px;padding-bottom:10px">
                                                        <table class="m_-7397014659233970794col-12" width="600" align="left"
                                                            cellspacing="0" cellpadding="0" border="0"
                                                            style="border-collapse:collapse;border-left:1px;border-right:1px">
                                                            <tbody>
                                                                <tr>
                                                                    <td style="border-collapse:collapse">
                                                                        <table class="m_-7397014659233970794block-content"
                                                                            width="100%" align="center" cellspacing="0"
                                                                            cellpadding="0" border="0"
                                                                            style="border-collapse:collapse;width:100%;text-align:center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center"
                                                                                        style="border-collapse:collapse;font-size:16px;line-height:18px;letter-spacing:0.0em;text-transform:none;padding-left:16px;padding-right:16px">
                                                                                        <h2
                                                                                            style="color:#0e1111;text-align:left;font-size:16px;margin:0">
                                                                                            <span
                                                                                                style="font-family:&#39;Roboto Bold&#39;,Arial,Helvetica,sans-serif">We’re
                                                                                                here to help</span></h2>
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
                                        <table bgcolor="#f5f5f5" class="m_-7397014659233970794row"
                                            id="m_-7397014659233970794widget_83bf76e54976a6f6c7b82a8b33a9571a" width="600"
                                            align="center" cellspacing="0" cellpadding="0" border="0"
                                            style="border-collapse:collapse">
                                            <tbody>
                                                <tr>
                                                    <td class="m_-7397014659233970794widget_top_bottom_padding"
                                                        style="border-collapse:collapse;padding-top:10px;padding-bottom:32px">
                                                        <table class="m_-7397014659233970794col-12" width="600" align="left"
                                                            cellspacing="0" cellpadding="0" border="0"
                                                            style="border-collapse:collapse;border-left:1px;border-right:1px">
                                                            <tbody>
                                                                <tr>
                                                                    <td style="border-collapse:collapse">
                                                                        <table class="m_-7397014659233970794block-content"
                                                                            width="100%" align="center" cellspacing="0"
                                                                            cellpadding="0" border="0"
                                                                            style="border-collapse:collapse;width:100%;text-align:center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center"
                                                                                        style="border-collapse:collapse;font-size:14px;line-height:18px;letter-spacing:0.0em;text-transform:none;padding-left:16px;padding-right:16px">
                                                                                        <p style="margin:0!important;color:#0e1111;text-align:left"
                                                                                            align="left"><span
                                                                                                style="font-family:&#39;Roboto Regular&#39;,Arial,Helvetica,sans-serif">Visit
                                                                                                our <a
                                                                                                    href="https://trk.bc.footlocker.com.au/ss/c/hVHNotmYA35oKI7Og-SINmL9PFqZICMffvOK7iWqlUbF_yYySGE2orLsoaMH6ek-qZgKKN7hlsPtk-ZcKq48Fg/3xz/IjRlaBFTTBGAlFfnOfvaOA/h4/cKCeNFfimHV-_MNOanEGGsv-6TqHq_-MrY4EIwcUVN4"
                                                                                                    rel="noopener"
                                                                                                    style="text-decoration:inherit!important"
                                                                                                    target="_blank"><span
                                                                                                        style="text-decoration:underline;color:#036ad8">Help
                                                                                                        Center</span></a>
                                                                                                for assistance.</span></p>
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
                                        <table class="m_-7397014659233970794row-spacer" bgcolor="#f5f5f5"
                                            id="m_-7397014659233970794widget_50e4ed5903f26c5117967a99f1bdaac2" width="600"
                                            align="center" cellspacing="0" cellpadding="0" border="0"
                                            style="border-collapse:collapse">
                                            <tbody>
                                                <tr>
                                                    <td class="m_-7397014659233970794widget_bottom_padding m_-7397014659233970794widget_top_padding"
                                                        align="center"
                                                        style="border-collapse:collapse;padding-right:30px;padding-left:30px;padding-bottom:10px;padding-top:10px">
                                                        <table width="100%" align="center" cellspacing="0" cellpadding="0"
                                                            border="0" style="border-collapse:collapse">
                                                            <tbody>
                                                                <tr>
                                                                    <td height="1"
                                                                        style="border-collapse:collapse;border-bottom:1px solid #dddddd;line-height:1px;font-size:1px">
                                                                         </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <table class="m_-7397014659233970794mobile-hide" bgcolor="#F5F5F5"
                                            id="m_-7397014659233970794widget_4f02e8e90387fe3a5bbb88f028cc5948" width="600"
                                            align="center" cellpadding="0" style="border-collapse:collapse">
                                            <tbody>
                                                <tr>
                                                    <td class="m_-7397014659233970794mc"
                                                        style="border-collapse:collapse;padding:56px 41px 56px 41px">
                                                        <table class="m_-7397014659233970794bp" width="360" align="center"
                                                            cellpadding="0" style="border-collapse:collapse">
                                                            <tbody>
                                                                <tr>
                                                                    <td width="120" class="m_-7397014659233970794c"
                                                                        style="border-collapse:collapse">
                                                                        <table align="center" cellpadding="0"
                                                                            cellspacing="0"
                                                                            style="border-collapse:collapse">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" width="120"
                                                                                        style="border-collapse:collapse"><a
                                                                                            href="https://trk.bc.footlocker.com.au/ss/c/hVHNotmYA35oKI7Og-SINmL9PFqZICMffvOK7iWqlUZiRTS-o0zu02-SWghMdz9zsjeNR8IsrmM7NRW7njUEOQ/3xz/IjRlaBFTTBGAlFfnOfvaOA/h5/hkDAgk5tSYXcLpCL3AHcAlWDHet-1bY18c_zw1yVRbo"
                                                                                            target="_blank"><img
                                                                                                src="https://partner-images.bluecore.com/footlocker_nz/findastore.png"
                                                                                                alt="Find a Store"
                                                                                                width="90"
                                                                                                style="display:block;height:auto;line-height:100%;text-decoration:none;outline:none;border:0 none"
                                                                                                height="auto"></a></td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                    <td width="120" class="m_-7397014659233970794c"
                                                                        style="border-collapse:collapse">
                                                                        <table align="center" cellpadding="0"
                                                                            cellspacing="0"
                                                                            style="border-collapse:collapse">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" width="120"
                                                                                        style="border-collapse:collapse"><a
                                                                                            href="https://trk.bc.footlocker.com.au/ss/c/hVHNotmYA35oKI7Og-SINmL9PFqZICMffvOK7iWqlUarcmr9gp8EmalN6BJn38jK_bqtbQ9LURMcqAC7dWT-rA/3xz/IjRlaBFTTBGAlFfnOfvaOA/h6/_DFGsP5KY_zwZoQ8KCWo0AFDLQg_r7AveBIqkBHOdX8"
                                                                                            target="_blank"><img
                                                                                                src="https://partner-images.bluecore.com/footlocker_nz/customerservice@2x.png"
                                                                                                alt="Customer Service"
                                                                                                width="90"
                                                                                                style="display:block;height:auto;line-height:100%;text-decoration:none;outline:none;border:0 none"
                                                                                                height="auto"></a></td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                    <td width="120" class="m_-7397014659233970794c"
                                                                        style="border-collapse:collapse">
                                                                        <table align="center" cellpadding="0"
                                                                            cellspacing="0"
                                                                            style="border-collapse:collapse">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" width="120"
                                                                                        style="border-collapse:collapse"><a
                                                                                            href="https://trk.bc.footlocker.com.au/ss/c/hVHNotmYA35oKI7Og-SINmL9PFqZICMffvOK7iWqlUYuxC_gZaeF60EwPNVlO0H-EgP8xi5H2f-AghMRQorpKQ/3xz/IjRlaBFTTBGAlFfnOfvaOA/h7/uf3VTnQ5gFxqp1OjWtYhdE8qUM4ZUeQTC1YaagWTb8M"
                                                                                            target="_blank"><img
                                                                                                src="https://partner-images.bluecore.com/footlocker_nz/shopexclusiveitems@2x.png"
                                                                                                alt="Shop Exclusive items"
                                                                                                width="90"
                                                                                                style="display:block;height:auto;line-height:100%;text-decoration:none;outline:none;border:0 none"
                                                                                                height="auto"></a></td>
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
                                        <table class="m_-7397014659233970794desktop-hide" bgcolor="#F5F5F5"
                                            id="m_-7397014659233970794widget_421eac251b8f63c723f4e0feeda58242" width="600"
                                            align="center" cellpadding="0"
                                            style="border-collapse:collapse;display:none;padding:0;max-height:0;overflow:hidden;float:left;font-size:0;line-height:0">
                                            <tbody>
                                                <tr>
                                                    <td class="m_-7397014659233970794mc"
                                                        style="border-collapse:collapse;padding:56px 0px 56px 0px">
                                                        <table class="m_-7397014659233970794bp" width="240" align="center"
                                                            cellpadding="0" style="border-collapse:collapse">
                                                            <tbody>
                                                                <tr>
                                                                    <td width="80" class="m_-7397014659233970794c"
                                                                        style="border-collapse:collapse">
                                                                        <table align="center" cellpadding="0"
                                                                            cellspacing="0"
                                                                            style="border-collapse:collapse">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" width="80"
                                                                                        style="border-collapse:collapse"><a
                                                                                            href="https://trk.bc.footlocker.com.au/ss/c/hVHNotmYA35oKI7Og-SINmL9PFqZICMffvOK7iWqlUaPqlPLAB0kzzkZNP48Vq34e9PAzRlBhQfMZ0l9Zjt9dA/3xz/IjRlaBFTTBGAlFfnOfvaOA/h8/Yg3ce61J_LnmU_8mCxSZV1rQN5uW1FAoSpWNCnG6Zwc"
                                                                                            target="_blank"><img
                                                                                                src="https://partner-images.bluecore.com/footlocker_nz/findastore.png"
                                                                                                alt="Find a Store" width="0"
                                                                                                style="display:block;height:auto;line-height:100%;text-decoration:none;outline:none;border:0 none;max-height:0;width:0"
                                                                                                height="auto"></a></td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                    <td width="80" class="m_-7397014659233970794c"
                                                                        style="border-collapse:collapse">
                                                                        <table align="center" cellpadding="0"
                                                                            cellspacing="0"
                                                                            style="border-collapse:collapse">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" width="80"
                                                                                        style="border-collapse:collapse"><a
                                                                                            href="https://trk.bc.footlocker.com.au/ss/c/hVHNotmYA35oKI7Og-SINmL9PFqZICMffvOK7iWqlUZ1UI65WvmWXB9ILzGsiJRqE7mDdXctNu1gON2gPXjFkA/3xz/IjRlaBFTTBGAlFfnOfvaOA/h9/X-DE_E8nKddZSi_UQesNIXcpbk00kiDpe7QKBe3J68I"
                                                                                            target="_blank"><img
                                                                                                src="https://partner-images.bluecore.com/footlocker_nz/customerservice@2x.png"
                                                                                                alt="Customer Service"
                                                                                                width="0"
                                                                                                style="display:block;height:auto;line-height:100%;text-decoration:none;outline:none;border:0 none;max-height:0;width:0"
                                                                                                height="auto"></a></td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                    <td width="80" class="m_-7397014659233970794c"
                                                                        style="border-collapse:collapse">
                                                                        <table align="center" cellpadding="0"
                                                                            cellspacing="0"
                                                                            style="border-collapse:collapse">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" width="80"
                                                                                        style="border-collapse:collapse"><a
                                                                                            href="https://trk.bc.footlocker.com.au/ss/c/hVHNotmYA35oKI7Og-SINmL9PFqZICMffvOK7iWqlUbMUbPPh9aR0R_t4avFf47b8DrzSnySzBsyQG_daOMXXA/3xz/IjRlaBFTTBGAlFfnOfvaOA/h10/h5no7V73X2kcuAkvphhJU86RjUOhlRWdjD8ycj_aE40"
                                                                                            target="_blank"><img
                                                                                                src="https://partner-images.bluecore.com/footlocker_nz/shopexclusiveitems@2x.png"
                                                                                                alt="Shop Exclusive items"
                                                                                                width="0"
                                                                                                style="display:block;height:auto;line-height:100%;text-decoration:none;outline:none;border:0 none;max-height:0;width:0"
                                                                                                height="auto"></a></td>
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
                                        <span>
                                            <table border="0" cellpadding="0" role="presentation" cellspacing="0"
                                                width="100%" style="border-collapse:collapse">
                                                <tbody>
                                                    <tr style="page-break-before:always">
                                                        <td align="center" valign="top" width="100%" cellpadding="0"
                                                            style="background-color:#ffffff;font-size:16px;line-height:16px;padding-top:24px;padding-bottom:24px;border-collapse:collapse"
                                                            bgcolor="#ffffff">
                                                            <table cellpadding="0" role="presentation" cellspacing="0"
                                                                width="100%" style="border-collapse:collapse">
                                                                <tbody>
                                                                    <tr>
                                                                        <td class="m_-7397014659233970794mobile-hide"
                                                                            width="16" style="border-collapse:collapse"> 
                                                                        </td>
                                                                        <td class="m_-7397014659233970794desktop-hide"
                                                                            width="10"
                                                                            style="border-collapse:collapse;display:none;padding:0;max-height:0;overflow:hidden;float:left;font-size:0;line-height:0">
                                                                             </td>
                                                                        <td style="border-collapse:collapse">
                                                                            <table class="m_-7397014659233970794fluid-row"
                                                                                role="presentation" width="100%"
                                                                                align="center" cellspacing="0"
                                                                                cellpadding="0" border="0" bgcolor="#ffffff"
                                                                                style="border-collapse:collapse">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td
                                                                                            style="border-collapse:collapse">
                                                                                            <table
                                                                                                class="m_-7397014659233970794col-12"
                                                                                                width="560" align="center"
                                                                                                cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                style="border-collapse:collapse;border-left:1px;border-right:1px">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td
                                                                                                            style="border-collapse:collapse;padding-right:14px;display:inline-block">
                                                                                                            <a href="https://trk.bc.footlocker.com.au/ss/c/hVHNotmYA35oKI7Og-SINmL9PFqZICMffvOK7iWqlUZpsiuulghQKDDp8ZLD2ZA_AR-mhwPw_WQUeLVSGVsIZA/3xz/IjRlaBFTTBGAlFfnOfvaOA/h11/dckvOIM407K3Tb-2VNujNIEvBczJp6esCYaGIQUlPyg"
                                                                                                                target="_blank"><img
                                                                                                                    width="20"
                                                                                                                    alt="Visit Foot Locker on Facebook"
                                                                                                                    src="https://partner-images.bluecore.com/eastbay_teamsales_us/Facebook.png"
                                                                                                                    style="display:block;height:auto;line-height:100%;text-decoration:none;outline:none;border:0 none"
                                                                                                                    height="auto"></a>
                                                                                                        </td>
                                                                                                        <td
                                                                                                            style="border-collapse:collapse;padding-right:14px;display:inline-block">
                                                                                                            <a href="https://trk.bc.footlocker.com.au/ss/c/hVHNotmYA35oKI7Og-SINmL9PFqZICMffvOK7iWqlUbOVyxCk_TUIoeDrhKCMmU_n1LDS4QsxD4O3SUpAzAMVA/3xz/IjRlaBFTTBGAlFfnOfvaOA/h12/Km9azPEKqhGGnbUPr-PR3LsKHLwbz2Vt2d-wWMXOOMg"
                                                                                                                target="_blank"><img
                                                                                                                    width="20"
                                                                                                                    alt="Visit Foot Locker on Instagram"
                                                                                                                    src="https://partner-images.bluecore.com/eastbay_teamsales_us/Instagram.png"
                                                                                                                    style="display:block;height:auto;line-height:100%;text-decoration:none;outline:none;border:0 none"
                                                                                                                    height="auto"></a>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                        </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                        <td class="m_-7397014659233970794mobile-hide"
                                                                            width="16" style="border-collapse:collapse"> 
                                                                        </td>
                                                                        <td class="m_-7397014659233970794desktop-hide"
                                                                            width="10"
                                                                            style="border-collapse:collapse;display:none;padding:0;max-height:0;overflow:hidden;float:left;font-size:0;line-height:0">
                                                                             </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </span>
                                        <table bgcolor="#ffffff" class="m_-7397014659233970794row"
                                            id="m_-7397014659233970794widget_4869f065b432651d6356d2c20024a779" width="600"
                                            align="center" cellspacing="0" cellpadding="0" border="0"
                                            style="border-collapse:collapse">
                                            <tbody>
                                                <tr>
                                                    <td class="m_-7397014659233970794widget_top_bottom_padding"
                                                        style="border-collapse:collapse;padding-top:0px;padding-bottom:0px">
                                                        <table class="m_-7397014659233970794col-12" width="600" align="left"
                                                            cellspacing="0" cellpadding="0" border="0"
                                                            style="border-collapse:collapse;border-left:1px;border-right:1px">
                                                            <tbody>
                                                                <tr>
                                                                    <td style="border-collapse:collapse">
                                                                        <table class="m_-7397014659233970794block-content"
                                                                            width="100%" align="center" cellspacing="0"
                                                                            cellpadding="0" border="0"
                                                                            style="border-collapse:collapse;width:100%;text-align:center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center"
                                                                                        style="border-collapse:collapse;font-size:14px;line-height:18px;letter-spacing:0.0em;text-transform:none;padding-left:16px;padding-right:16px">
                                                                                        <p style="margin:0!important;color:#000001;text-align:left"
                                                                                            align="left"><span
                                                                                                style="text-decoration:underline"><span
                                                                                                    style="font-family:&#39;Roboto Regular&#39;,Arial,Helvetica,sans-serif;color:#036ad8"><a
                                                                                                        href="https://trk.bc.footlocker.com.au/ss/c/hVHNotmYA35oKI7Og-SINmL9PFqZICMffvOK7iWqlUaXFZtMt5elsSB0XNn6YyeBoUUOiAsp0XjzntuT68ivBA/3xz/IjRlaBFTTBGAlFfnOfvaOA/h14/FBmF0j2Z_RQkyjatHphpuwVpAPddz8rU0zG69fIwNWk"
                                                                                                        rel="noopener"
                                                                                                        style="color:#036ad8;text-decoration:underline"
                                                                                                        target="_blank">footlocker.com.au</a></span></span>
                                                                                        </p>
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
                                        <table bgcolor="#ffffff" class="m_-7397014659233970794row"
                                            id="m_-7397014659233970794widget_d1c53ce30241b01072a01c40301d74a1" width="600"
                                            align="center" cellspacing="0" cellpadding="0" border="0"
                                            style="border-collapse:collapse">
                                            <tbody>
                                                <tr>
                                                    <td class="m_-7397014659233970794widget_top_bottom_padding"
                                                        style="border-collapse:collapse;padding-top:5px;padding-bottom:20px">
                                                        <table class="m_-7397014659233970794col-12" width="600" align="left"
                                                            cellspacing="0" cellpadding="0" border="0"
                                                            style="border-collapse:collapse;border-left:1px;border-right:1px">
                                                            <tbody>
                                                                <tr>
                                                                    <td style="border-collapse:collapse">
                                                                        <table class="m_-7397014659233970794block-content"
                                                                            width="100%" align="center" cellspacing="0"
                                                                            cellpadding="0" border="0"
                                                                            style="border-collapse:collapse;width:100%;text-align:center">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center"
                                                                                        style="border-collapse:collapse;font-size:14px;line-height:18px;letter-spacing:0.0em;text-transform:none;padding-left:16px;padding-right:16px">
                                                                                        <p style="margin:0!important;color:#000001;text-align:left"
                                                                                            align="left"><span
                                                                                                style="font-family:&#39;Roboto Regular&#39;,Arial,Helvetica,sans-serif;color:#0e1111">Foot
                                                                                                Locker Australia Inc
                                                                                                <br>ABN: 22619093977</span>
                                                                                        </p>
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

    </div>
    </div>
    </div>
    """

    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
