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
    msg['From'] = formataddr((f'Canada Goose', sender_email))
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
    "Please enter the invoice date (10/10/2024):",
    "Please enter the order date (10/10/2024):",
    "Please enter the street address (1234 Elmo Street):",
    "Please enter the suburb/city (New York City):",
    "Please enter the postcode (72133):",
    "Please enter the country (United States):",
    "Please enter the product name (Canada Goose puffer test):",
    "Please enter the colour & size (Black Large):",
    "Please enter the price (WITHOUT THE $ SIGN):",
    "Please enter the tax type (VAT/GST/SALES TAX):",
    "Please enter the tax amount (WITHOUT THE $ SIGN):",
    "Please enter the image url (MUST BE FROM CA SITE):",
    "Please enter the shipping price (WITHOUT THE $ SIGN):",
    "Please enter the subtotal exl tax (WITHOUT THE $ SIGN):",
    "Please enter the order total (WITHOUT THE $ SIGN):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira a data da fatura (10/10/2024):",
    "Por favor, insira a data do pedido (10/10/2024):",
    "Por favor, insira o endereço (1234 Elmo Street):",
    "Por favor, insira o subúrbio/cidade (New York City):",
    "Por favor, insira o código postal (72133):",
    "Por favor, insira o país (Estados Unidos):",
    "Por favor, insira o nome do produto (Canada Goose puffer test):",
    "Por favor, insira a cor e o tamanho (Black Large):",
    "Por favor, insira o preço (SEM O SINAL $):",
    "Por favor, insira o tipo de imposto (VAT/GST/SALES TAX):",
    "Por favor, insira o valor do imposto (SEM O SINAL $):",
    "Por favor, insira a URL da imagem (DEVE SER DO SITE CA):",
    "Por favor, insira o preço do frete (SEM O SINAL $):",
    "Por favor, insira o subtotal sem imposto (SEM O SINAL $):",
    "Por favor, insira o total do pedido (SEM O SINAL $):",
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
    part1 = random.randint(100000000, 999999999)  # Random 10-digit number

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
    sender_email = EMAIL
    sender_password = PASSWORD
    recipient_email = f'{user_inputs[17]}'
    subject = f"Your order invoice #{order_num}" if lang == "en" else f"Sua fatura de pedido #{order_num}"
    html_template = f"""
        <div class="gmail_quote">
        <blockquote class="gmail_quote" style="margin:0px 0px 0px 0.8ex;border-left-width:1px;border-left-style:solid;padding-left:1ex;border-left-color:rgb(204,204,204)">
        <div id="m_4174665745824026173m_-8528642198172593804:2c">
            <div style="padding:0px;margin:0px auto!important">
            <div></div>
            <table style="border-collapse:collapse;margin:0px auto!important" border="0" width="600" cellspacing="0" cellpadding="0" align="center" bgcolor="#ffffff">
                <tbody>
                <tr>
                    <td style="padding:15px 20px 0px">
                    <table border="0" width="100%" cellspacing="0" cellpadding="0">
                        <tbody>
                        <tr>
                            <td valign="top" width="50%">
                            <table border="0" width="auto" cellspacing="0" cellpadding="0">
                                <tbody>
                                <tr>
                                    <td valign="top">
                                    <div style="white-space:nowrap">
                                        <a href="https://click.enews.canadagoose.com/?qs=c3d216459162666dbc69e097d9f3b77e4525686062b84c0c1d9d7ca5a57c8097e1e1df5a93a737d1ab57cfbe06f4265340b8148db14556d3b829a9b188b532b4" style="text-decoration:none;text-transform:uppercase;font-size:8px;font-weight:bold;font-family:arial,tahoma,sans-serif;letter-spacing:1px;color:rgb(0,0,0)" rel="noopener noreferrer" target="_blank">My Account</a>
                                    </div>
                                    </td>
                                    <td>   </td>
                                    <td valign="top">
                                    <div style="white-space:nowrap;padding-left:15px">
                                        <a href="https://click.enews.canadagoose.com/?qs=c3d216459162666dfc74f6188427f7c000304d060d5497b419cf457e0ffd6ee466ddb012bc11e00b726a7e782f5b281457cf2e800ef5ec08f8f66f78a9dec530" style="text-decoration:none;text-transform:uppercase;font-size:8px;font-weight:bold;font-family:arial,tahoma,sans-serif;letter-spacing:1px;color:rgb(0,0,0)" rel="noopener noreferrer" target="_blank">Customer Care</a>
                                    </div>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                            </td>
                            <td style="text-align:right" valign="top" width="50%">
                            <div style="white-space:nowrap">
                                <a href="https://view.enews.canadagoose.com/?qs=9d651e2ce55b8156bf7bc334a98f2ccdf384cf03007eade7f83dfb1d606d9ef6d61d46cfc1ebd736c00c8e850b6672b43c7434addc2327253456d90ecfa91086c8407fb40d170139795572a6d7f1b3911b09c2491b15a117001798ee00ae72b0" style="text-decoration:none;text-transform:uppercase;font-size:8px;font-weight:bold;font-family:arial,tahoma,sans-serif;letter-spacing:1px;color:rgb(0,0,0)" rel="noopener noreferrer" target="_blank">View in Browser</a>
                            </div>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                    </td>
                </tr>
                <tr>
                    <td style="border-collapse:collapse;max-width:600px" align="center" valign="top" width="100%">
                    <table style="max-width:600px;border-collapse:collapse;margin-left:auto!important;margin-right:auto!important" border="0" width="100%" cellspacing="0" cellpadding="0" align="center">
                        <tbody>
                        <tr>
                            <td style="padding-top:20px;padding-bottom:20px" align="center">
                            <a href="https://click.enews.canadagoose.com/?qs=c3d216459162666dc7fc280b6f2adb2561fbfd9714a7c549cdbb46402ffe740edfa2b027c7991c56b8a9838cd72aae5b1016a9d5d8c1ac5efb56b858d14f7704" name="m_4174665745824026173_m_-8528642198172593804_m_2936198520465281869_m_-6956951117363112146_m_-2964404388666275271_home-page-header" rel="noopener noreferrer" target="_blank">
                                <img style="display: block; margin-left: auto !important; margin-right: auto !important;" src="http://image.enews.canadagoose.com/lib/fe6b15707d66007f7715/m/3/544315fd-222f-4e84-978b-6a7f30581637.png" alt="CANADA GOOSE" width="360" height="65" border="0">
                            </a>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                    </td>
                </tr>
                </tbody>
            </table>
            <table style="border-collapse:collapse;margin:0px auto!important" border="0" width="600" cellspacing="0" cellpadding="0" align="center" bgcolor="#ffffff">
                <tbody>
                <tr>
                    <td style="border-collapse:collapse;max-width:600px" align="center" valign="top" width="100%">
                    <table style="max-width:600px;border-collapse:collapse;margin-left:auto!important;margin-right:auto!important" border="0" width="100%" cellspacing="0" cellpadding="0" align="center">
                        <tbody>
                        <tr>
                            <td align="center" valign="top">
                            <table style="min-width:100%" role="presentation" width="100%" cellspacing="0" cellpadding="0">
                                <tbody>
                                <tr>
                                    <td>
                                    <table style="min-width:100%" role="presentation" width="100%" cellspacing="0" cellpadding="0">
                                        <tbody>
                                        <tr>
                                            <td>
                                            <table style="min-width:100%" role="presentation" width="100%" cellspacing="0" cellpadding="0">
                                                <tbody>
                                                <tr>
                                                    <td> </td>
                                                </tr>
                                                </tbody>
                                            </table>
                                            <table style="max-width:600px;width:100%;margin:0px auto!important" border="0" cellspacing="0" cellpadding="0" align="center">
                                                <tbody>
                                                <tr>
                                                    <td align="center" bgcolor="#fafafa">
                                                    <table border="0" width="100%" cellspacing="0" cellpadding="0" align="center">
                                                        <tbody>
                                                        <tr>
                                                            <td align="center" valign="top" bgcolor="#fafafa">
                                                            <img style="display: block; text-align: center; margin: 0px auto !important; width: 600px !important;" src="https://image.enews.canadagoose.com/lib/fe6b15707d66007f7715/m/7/bb4e49ae-cd7d-4fbe-8ec4-4f71aee1e2c0.png" alt="INVOICE" width="600" border="0">
                                                            <div dir="ltr" style="opacity:0.01">
                                                                <span>
                                                                <button aria-label="Download attachment " id="m_4174665745824026173m_-8528642198172593804">
                                                                    <span></span>
                                                                    <span></span>
                                                                    <span aria-hidden="true">
                                                                    <span aria-hidden="true">
                                                                        <u></u>
                                                                        <u></u>
                                                                        <u></u>
                                                                        <u></u>
                                                                    </span>
                                                                    </span>
                                                                    <div></div>
                                                                </button>
                                                                <div id="m_4174665745824026173m_-8528642198172593804tt-c104" role="tooltip" aria-hidden="true">Download</div>
                                                                </span>
                                                            </div>
                                                            <div dir="ltr" style="opacity:0.01">
                                                                <span>
                                                                <button aria-label="Download attachment " id="m_4174665745824026173m_-8528642198172593804m_2936198520465281869">
                                                                    <span></span>
                                                                    <span></span>
                                                                    <span aria-hidden="true">
                                                                    <span aria-hidden="true">
                                                                        <u></u>
                                                                        <u></u>
                                                                        <u></u>
                                                                        <u></u>
                                                                    </span>
                                                                    </span>
                                                                    <div></div>
                                                                </button>
                                                                <div id="m_4174665745824026173m_-8528642198172593804m_2936198520465281869tt-c62" role="tooltip" aria-hidden="true">Download</div>
                                                                </span>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        </tbody>
                                                    </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding:30px" align="center" valign="middle" bgcolor="#fafafa">
                                                    <table border="0" width="100%" cellspacing="0" cellpadding="0" bgcolor="#ffffff">
                                                        <tbody>
                                                        <tr>
                                                            <td style="padding:0px 30px">
                                                            <table border="0" width="100%" cellspacing="0" cellpadding="0" bgcolor="#ffffff">
                                                                <tbody>
                                                                <tr>
                                                                    <td style="padding:50px 0px 20px;font-family:Arial,Helvetica,sans-serif;font-size:12px;text-align:left;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)" bgcolor="#ffffff">
                                                                    <p style="font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:left;padding-bottom:7px;margin-top:0px;line-height:110%!important;color:rgb(0,0,0)">Hi {user_inputs[0]},</p>
                                                                    <p style="font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:left;padding-bottom:7px;line-height:110%!important;color:rgb(0,0,0)">Thank you for shopping with Canada Goose.</p>
                                                                    <p style="font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:left;padding-bottom:7px;margin-top:0px;line-height:110%!important;color:rgb(0,0,0)">
                                                                        <strong style="font-family:Arial,Helvetica,sans-serif">Have questions?</strong>
                                                                        <br>Our Customer Experience team is happy to help. They can be reached at <a href="tel:0%C2%A0800%C2%A0323%C2%A04844" style="text-decoration:underline;font-family:Arial,Helvetica,sans-serif;color:rgb(0,0,0)" name="m_4174665745824026173_m_-8528642198172593804_m_2936198520465281869_m_-6956951117363112146_m_-2964404388666275271_PhoneNumber-invoice" rel="noopener noreferrer" target="_blank">0 800 323 4844</a> or <a href="mailto:cguk@canadagoose.com" style="text-decoration:underline;font-family:Arial,Helvetica,sans-serif;color:rgb(0,0,0)" name="m_4174665745824026173_m_-8528642198172593804_m_2936198520465281869_m_-6956951117363112146_m_-2964404388666275271_AskUs-cancellation-invoice" rel="noopener noreferrer" target="_blank">cguk@canadagoose.com</a>.
                                                                    </p>
                                                                    <p style="font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:left;padding-bottom:7px;margin-top:0px;line-height:110%!important;color:rgb(0,0,0)">Here is your order invoice:</p>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td>
                                                                    <table style="width:100%;border-collapse:collapse" cellspacing="0" cellpadding="0">
                                                                        <tbody>
                                                                        <tr>
                                                                            <td style="border-top-width:1px;border-top-style:solid;border-top-color:rgb(204,204,204)" colspan="2"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="padding:40px 0px;font-family:Arial,Helvetica,sans-serif;font-size:13px;font-weight:normal;text-align:left;text-transform:uppercase;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)" width="50%">
                                                                            <strong style="font-family:Arial,Helvetica,sans-serif">Invoice Number</strong>
                                                                            <div style="padding-top:10px;font-family:Arial,Helvetica,sans-serif">30847775715827270383</div>
                                                                            </td>
                                                                            <td style="padding:49px 0px;font-family:Arial,Helvetica,sans-serif;font-size:13px;font-weight:normal;text-align:left;text-transform:uppercase;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)" width="50%">
                                                                            <strong style="font-family:Arial,Helvetica,sans-serif">Invoice Date</strong>
                                                                            <div style="padding-top:10px;font-family:Arial,Helvetica,sans-serif">{user_inputs[1]}</div>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="border-top-width:1px;border-top-style:solid;border-top-color:rgb(204,204,204)" colspan="2"> </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="padding:40px 0px;font-family:Arial,Helvetica,sans-serif;font-size:13px;font-weight:normal;text-align:left;text-transform:uppercase;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)">
                                                                            <strong style="font-family:Arial,Helvetica,sans-serif">Order Number</strong>
                                                                            <div style="padding-top:10px;font-family:Arial,Helvetica,sans-serif">CGGB_{order_num}</div>
                                                                            </td>
                                                                            <td style="padding:40px 0px;font-family:Arial,Helvetica,sans-serif;font-size:13px;font-weight:normal;text-align:left;text-transform:uppercase;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)">
                                                                            <strong style="font-family:Arial,Helvetica,sans-serif">Order Date</strong>
                                                                            <div style="padding-top:10px;font-family:Arial,Helvetica,sans-serif">{user_inputs[2]}</div>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td colspan="2">
                                                                            <table style="min-width:100%" role="presentation" width="100%" cellspacing="0" cellpadding="0">
                                                                                <tbody>
                                                                                <tr>
                                                                                    <td>
                                                                                    <table width="100%" cellspacing="0" cellpadding="0" align="center">
                                                                                        <tbody>
                                                                                        <tr>
                                                                                            <td style="border-top-width:1px;border-top-style:solid;border-top-color:rgb(204,204,204)" colspan="2"> </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="padding:40px 0px 0px;font-family:Arial,Helvetica,sans-serif;font-size:13px;font-weight:bold;text-align:left;letter-spacing:1px;text-transform:uppercase;line-height:110%!important;color:rgb(0,0,0)" align="left" valign="top" width="50%">Billing Address</td>
                                                                                            <td style="padding:40px 0px 0px;font-family:Arial,Helvetica,sans-serif;font-size:13px;font-weight:bold;text-align:left;letter-spacing:1px;text-transform:uppercase;line-height:110%!important;color:rgb(0,0,0)" align="left" valign="top" width="50%">Shipping Address</td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="padding:20px 0px" align="left" valign="top" width="50%">
                                                                                            <table style="min-width:100%;border-collapse:collapse" width="100%" cellspacing="0" cellpadding="0" align="left">
                                                                                                <tbody>
                                                                                                <tr>
                                                                                                    <td style="padding-top:4px">
                                                                                                    <p style="font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:left;margin:0px;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)">{user_inputs[0]}</p>
                                                                                                    </td>
                                                                                                </tr>
                                                                                                <tr>
                                                                                                    <td style="padding-top:4px" align="left" valign="top">
                                                                                                    <p style="font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:left;margin:0px;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)">{user_inputs[3]}</p>
                                                                                                    </td>
                                                                                                </tr>
                                                                                                <tr>
                                                                                                    <td style="padding-top:4px" align="left" valign="top">
                                                                                                    <p style="font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:left;margin:0px;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)">{user_inputs[4]}</p>
                                                                                                    </td>
                                                                                                </tr>
                                                                                                <tr>
                                                                                                    <td style="padding-top:4px" align="left" valign="top">
                                                                                                    <p style="font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:left;margin:0px;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)">{user_inputs[5]}</p>
                                                                                                    </td>
                                                                                                </tr>
                                                                                                <tr>
                                                                                                    <td style="padding-top:4px" align="left" valign="top">
                                                                                                    <p style="font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:left;margin:0px;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)">{user_inputs[6]}</p>
                                                                                                    </td>
                                                                                                </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                            </td>
                                                                                            <td style="padding:20px 0px 40px" align="left" valign="top" width="50%">
                                                                                            <table style="min-width:100%;border-collapse:collapse" width="100%" cellspacing="0" cellpadding="0" align="center">
                                                                                                <tbody>
                                                                                                <tr>
                                                                                                    <td style="padding-top:4px">
                                                                                                    <p style="font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:left;letter-spacing:1px;margin:0px;line-height:110%!important;color:rgb(0,0,0)">{user_inputs[0]}</p>
                                                                                                    </td>
                                                                                                </tr>
                                                                                                <tr>
                                                                                                    <td style="padding-top:4px" align="left" valign="top">
                                                                                                    <p style="font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:left;margin:0px;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)">{user_inputs[3]}</p>
                                                                                                    </td>
                                                                                                </tr>
                                                                                                <tr>
                                                                                                    <td style="padding-top:4px" align="left" valign="top">
                                                                                                    <p style="font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:left;margin:0px;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)">{user_inputs[4]}</p>
                                                                                                    </td>
                                                                                                </tr>
                                                                                                <tr>
                                                                                                    <td style="padding-top:4px" align="left" valign="top">
                                                                                                    <p style="font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:left;margin:0px;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)">{user_inputs[5]}</p>
                                                                                                    </td>
                                                                                                </tr>
                                                                                                <tr>
                                                                                                    <td style="padding-top:4px" align="left" valign="top">
                                                                                                    <p style="font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:left;margin:0px;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)">{user_inputs[6]}</p>
                                                                                                    </td>
                                                                                                </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                            </td>
                                                                                        </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                    <table width="100%" cellspacing="0" cellpadding="0" align="center">
                                                                                        <tbody>
                                                                                        <tr>
                                                                                            <td style="border-top-width:1px;border-top-style:solid;border-top-color:rgb(204,204,204)" colspan="2"> </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="padding:40px 0px 0px" align="left" valign="top" width="50%">
                                                                                            <h2 style="font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:bold;text-align:left;letter-spacing:1px;text-transform:uppercase;line-height:110%!important;color:rgb(0,0,0)">Shipping Method</h2>
                                                                                            </td>
                                                                                            <td style="padding:40px 0px 0px" align="left" valign="top" width="50%">
                                                                                            <h2 style="font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:bold;text-align:left;letter-spacing:1px;text-transform:uppercase;line-height:110%!important;color:rgb(0,0,0)">Payment Method</h2>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="padding:10px 0px 0px" align="left" valign="top" width="50%">
                                                                                            <p style="font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:left;margin:0px;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)">DHL Express</p>
                                                                                            </td>
                                                                                            <td style="padding:10px 0px 0px" align="left" valign="top" width="50%">
                                                                                            <p style="font-family:Arial,Helvetica,sans-serif;font-size:14px;font-weight:normal;text-align:left;margin:0px;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)">MasterCard  ************2854</p>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="padding-bottom:40px" colspan="2"> </td>
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
                                                                            <td colspan="2">
                                                                            <table style="min-width:100%" role="presentation" width="100%" cellspacing="0" cellpadding="0">
                                                                                <tbody>
                                                                                <tr>
                                                                                    <td>
                                                                                    <table style="min-width:100%;border-collapse:collapse" width="100%" cellspacing="0" cellpadding="0" align="center">
                                                                                        <tbody>
                                                                                        <tr>
                                                                                            <td style="border-top-width:1px;border-top-style:solid;border-top-color:rgb(204,204,204)" valign="top"> </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="padding:40px 15px 0px">
                                                                                            <table border="0" width="100%" cellspacing="0" cellpadding="0">
                                                                                                <tbody>
                                                                                                <tr>
                                                                                                    <td valign="top">
                                                                                                    <table style="width:90%;border-collapse:collapse" cellspacing="0" cellpadding="0">
                                                                                                        <tbody>
                                                                                                        <tr>
                                                                                                            <td style="padding:14px 0px">
                                                                                                            <h2 style="padding:0px;margin:0px;font-family:Arial,Helvetica,sans-serif;font-size:13px;font-weight:bold;text-align:left;text-transform:uppercase;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)">{user_inputs[7]}</h2>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td style="border-top-width:1px;border-top-style:solid;padding:14px 0px;border-top-color:rgb(204,204,204)">
                                                                                                            <div style="letter-spacing:1px;padding:0px;margin:0px;font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:left;text-transform:uppercase;line-height:110%!important;color:rgb(0,0,0)">{user_inputs[8]}</div>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td style="border-top-width:1px;border-top-style:solid;padding:14px 0px;border-top-color:rgb(204,204,204)">
                                                                                                            <table style="width:100%;border-collapse:collapse" width="100%" cellspacing="0" cellpadding="0" align="left">
                                                                                                                <tbody>
                                                                                                                <tr>
                                                                                                                    <td style="padding:0px;margin:0px;font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:bold;text-align:left;text-transform:uppercase;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)" width="50%">Qty: 1</td>
                                                                                                                    <td style="padding:0px;margin:0px;font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:bold;text-align:right;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)">{user_inputs[16]}{user_inputs[9]}</td>
                                                                                                                </tr>
                                                                                                                </tbody>
                                                                                                            </table>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td style="border-top-width:1px;border-top-style:solid;padding:14px 0px;border-top-color:rgb(204,204,204)">
                                                                                                            <table border="0" width="100%" cellspacing="0" cellpadding="0">
                                                                                                                <tbody>
                                                                                                                <tr>
                                                                                                                    <td style="padding:0px;margin:0px;font-family:Arial,Helvetica,sans-serif;font-size:12px;text-align:left;text-transform:uppercase;letter-spacing:1px;font-weight:bold;line-height:110%!important;color:rgb(0,0,0)" valign="top" width="50%">{user_inputs[10]}</td>
                                                                                                                    <td style="text-align:right;font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:bold;line-height:110%!important;color:rgb(0,0,0)" valign="top" width="50%">{user_inputs[16]}{user_inputs[11]}</td>
                                                                                                                </tr>
                                                                                                                </tbody>
                                                                                                            </table>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                    </td>
                                                                                                    <td valign="top" width="140">
                                                                                                    <img style="display: block; margin: 0px; text-align: left; max-width: 120px !important;" role="presentation" src="{user_inputs[12]}" alt="" width="120" height="185" align="right" border="0">
                                                                                                    </td>
                                                                                                </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="padding-bottom:40px" valign="top"> </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="border-top-width:1px;border-top-style:solid;padding:25px 0px 0px;border-top-color:rgb(204,204,204)" valign="top">
                                                                                            <table border="0" width="100%" cellspacing="0" cellpadding="0">
                                                                                                <tbody>
                                                                                                <tr>
                                                                                                    <td style="padding-top:14px;font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:bold;text-align:left;text-transform:uppercase;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)" colspan="2">Shipping &amp; Handling</td>
                                                                                                </tr>
                                                                                                <tr>
                                                                                                    <td style="padding-top:14px;font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:left;text-transform:uppercase;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)" valign="top">Price excl. {user_inputs[10]}</td>
                                                                                                    <td style="padding-top:14px;font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:right;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)" valign="top">{user_inputs[16]}{user_inputs[13]}</td>
                                                                                                </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="padding-bottom:40px" valign="top"> </td>
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
                                                                            <td style="padding-bottom:30px" colspan="2">
                                                                            <table style="min-width:100%" role="presentation" width="100%" cellspacing="0" cellpadding="0">
                                                                                <tbody>
                                                                                <tr>
                                                                                    <td>
                                                                                    <table width="100%" cellspacing="0" cellpadding="0" align="center">
                                                                                        <tbody>
                                                                                        <tr>
                                                                                            <td style="border-top-width:1px;border-top-style:solid;border-top-color:rgb(204,204,204)" colspan="2"> </td>
                                                                                        </tr>
                                                                                        <tr valign="top">
                                                                                            <td style="padding:40px 0px 0px;font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:left;text-transform:uppercase;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)" width="50%">Subtotal</td>
                                                                                            <td style="text-align:right;padding:40px 0px 0px;font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)" width="50%">{user_inputs[16]}{user_inputs[15]}</td>
                                                                                        </tr>
                                                                                        <tr style="padding-top:40px" valign="top">
                                                                                            <td style="padding-top:40px;font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:left;text-transform:uppercase;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)" width="50%">{user_inputs[10]} amount</td>
                                                                                            <td style="text-align:right;padding-top:40px;font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)" width="50%">{user_inputs[16]}{user_inputs[11]}</td>
                                                                                        </tr>
                                                                                        <tr valign="top">
                                                                                            <td style="padding-top:40px;font-family:Arial,Helvetica,sans-serif;font-size:13px;font-weight:bold;text-align:left;text-transform:uppercase;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)" width="50%">Total</td>
                                                                                            <td style="padding-top:40px;font-family:Arial,Helvetica,sans-serif;font-size:13px;font-weight:bold;text-align:right;letter-spacing:1px;line-height:110%!important;color:rgb(0,0,0)" width="50%">
                                                                                            <strong style="font-family:Arial,Helvetica,sans-serif">{user_inputs[16]}{user_inputs[15]}</strong>
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
            <table border="0" width="600" cellspacing="0" cellpadding="0" align="center">
                <tbody>
                <tr>
                    <td style="padding-top:50px" align="center">
                    <table style="min-width:100%" role="presentation" width="100%" cellspacing="0" cellpadding="0">
                        <tbody>
                        <tr>
                            <td>
                            <table border="0" width="580" cellspacing="0" cellpadding="0" align="center">
                                <tbody>
                                <tr>
                                    <td>
                                    <img style="display: block; border: 0px; width: 80px !important;" src="https://image.enews.canadagoose.com/lib/fe6b15707d66007f7715/m/14/spacer.png" width="80">
                                    </td>
                                    <td>
                                    <a title="Instagram" href="https://click.enews.canadagoose.com/?qs=c3d216459162666d6506c17425bd04559fbb5791ef47e1c43908484ee85271f34833152b942eb853ab0c0c705a6533144049aecd4e08f1083b7f9836afa4dbb732e0080b5c9709ea" rel="noopener noreferrer" target="_blank">
                                        <img style="display: block; border: 0px; width: 70px !important;" title="Instagram" src="https://image.enews.canadagoose.com/lib/fe6b15707d66007f7715/m/14/footer-social-v1-2.png" alt="Instagram" width="70">
                                    </a>
                                    </td>
                                    <td>
                                    <a title="Tiktok" href="https://click.enews.canadagoose.com/?qs=c3d216459162666d96259048bf9e1dc55892969007ae89777430d507c69186bd9e91a39a8a54f73179977b92225b5f5a35cdcdcf6d5b039d4aa10ffcbbcad45142d7632ea8f799af" rel="noopener noreferrer" target="_blank">
                                        <img style="display: block; border: 0px; width: 70px !important;" title="Tiktok" src="https://image.enews.canadagoose.com/lib/fe6b15707d66007f7715/m/14/footer-social-v1-3.png" alt="Tiktok" width="70">
                                    </a>
                                    </td>
                                    <td>
                                    <a title="Facebook" href="https://click.enews.canadagoose.com/?qs=c3d216459162666d9ca202fdb7f3a3fdd0ad40cbd723620e09bf42864d5f1570eebc69785f5fa162300568c303d342779a9e3b7f963d49ed46cde85ce98d457e82bb8536f8a72642" rel="noopener noreferrer" target="_blank">
                                        <img style="display: block; border: 0px; width: 70px !important;" title="Facebook" src="https://image.enews.canadagoose.com/lib/fe6b15707d66007f7715/m/14/footer-social-v1-4.png" alt="Facebook" width="70">
                                    </a>
                                    </td>
                                    <td>
                                    <a title="Twitter" href="https://click.enews.canadagoose.com/?qs=c3d216459162666d41737494789a10acbaa7cfa5f4c1c29abc4d5ccb48d6cee208747aa696ba922597219e76ff6f157e7e02b6aede18bbdec7ceced3eaa476367268d5f35b4ef76f" rel="noopener noreferrer" target="_blank">
                                        <img style="display: block; border: 0px; width: 70px !important;" title="Twitter" src="https://image.enews.canadagoose.com/lib/fe6b15707d66007f7715/m/14/footer-social-v1-5.png" alt="Twitter" width="70">
                                    </a>
                                    </td>
                                    <td>
                                    <a title="YouTube" href="https://click.enews.canadagoose.com/?qs=c3d216459162666dcbc3395320dcb5a3e29af5d80225c8ceae151c62f9784c008a0d9e9791574528d26001ce742fbcead7767d916977974db7ece8fd956561cb13d42da8d5ddddc2" rel="noopener noreferrer" target="_blank">
                                        <img style="display: block; border: 0px; width: 70px !important;" title="Youtube" src="https://image.enews.canadagoose.com/lib/fe6b15707d66007f7715/m/14/footer-social-v1-6.png" alt="Youtube" width="70">
                                    </a>
                                    </td>
                                    <td>
                                    <a title="Pinterest" href="https://click.enews.canadagoose.com/?qs=c3d216459162666d2447bc7e278dbf6f71798805aaa2753b125e0784a7e205f9ef3d9358141460b15bc23f15fbc589710be5bbb627703050fb2fbfb6555fdbc63ae17b3f42581292" rel="noopener noreferrer" target="_blank">
                                        <img style="display: block; border: 0px; width: 70px !important;" title="Pinterest" src="https://image.enews.canadagoose.com/lib/fe6b15707d66007f7715/m/14/footer-social-v1-7.png" alt="Pinterest" width="70">
                                    </a>
                                    </td>
                                    <td>
                                    <img style="display: block; border: 0px; width: 80px !important;" src="https://image.enews.canadagoose.com/lib/fe6b15707d66007f7715/m/14/spacer.png" width="80">
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding-top:8px" colspan="8"> </td>
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
                    <td style="padding-bottom:40px" align="center">
                    <table style="min-width:100%" role="presentation" width="100%" cellspacing="0" cellpadding="0">
                        <tbody>
                        <tr>
                            <td>
                            <table border="0" width="580" cellspacing="0" cellpadding="0" align="center">
                                <tbody>
                                <tr>
                                    <td style="font-family:Arial,Helvetica,sans-serif;font-size:12px;padding:0px 0px 20px;text-align:center;color:rgb(0,0,0)">In order to send you newsletters, you consent to the transfer of your personal data to the USA and it’s processing there.</td>
                                </tr>
                                <tr>
                                    <td>
                                    <div style="font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:normal;text-align:center;color:rgb(0,0,0)">
                                        <a href="https://click.enews.canadagoose.com/?qs=c3d216459162666d7077bc40c6000ab9a8c6118e7af03347ab549c6cf3c2678e43623f84d5eafc04883622261af5b56b48bc2b163582846e734e6edd0cdf2c0a" style="text-decoration:none;font-size:12px;font-family:Arial,Helvetica,sans-serif;color:rgb(0,0,0)" rel="noopener noreferrer" target="_blank">Contact Us</a>  |  <a href="https://click.enews.canadagoose.com/?qs=c3d216459162666de15b10ccd8991abf80471248a804d1abe7c2de8da470e3f30d2231c3d1b95cfeed02ebb35c7a6a8d22ae971d7bc0673e6f4af39ffee8a48c" style="text-decoration:none;font-size:12px;font-family:Arial,Helvetica,sans-serif;color:rgb(0,0,0)" rel="noopener noreferrer" target="_blank">Privacy Policy</a> |  <a href="https://click.enews.canadagoose.com/?qs=c3d216459162666db4e44a89a45460b0adc7ee0c859aeaf5d648c155464b423b089e0ea431f40d6d7b6d64044122fc034b8214f26ec59e02cb0ea1b0828f831d" style="text-decoration:none;font-size:12px;font-family:Arial,Helvetica,sans-serif;color:rgb(0,0,0)" rel="noopener noreferrer" target="_blank">Terms &amp; Conditions</a>
                                    </div>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                            <table border="0" width="600" cellspacing="0" cellpadding="0" align="center">
                                <tbody>
                                <tr>
                                    <td style="font-size:12px;font-family:arial,sans-serif;text-align:center;padding:6px 0px 30px;color:rgb(0,0,0)">© 2025 CANADA GOOSE EU B.V., UK Branch, Devonshire House Mayfair Place, Leister England , W1J 8AJ <br>VAT Registration GB433075907 </td>
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
            <img src="https://click.enews.canadagoose.com/open.aspx?ffcb10-fe31157073660574771d70-fdb715767161037b731678776d-fe6b15707d66007f7715-fe8c157374620d7b7c-fdf01578756d0d7e73137071-ff66157370&amp;d=10171&amp;bmt=0" alt="" width="1" height="1">
            <div></div>
            <div></div>
            <div></div>
            </div>
            <div></div>
        </div>
        </blockquote>
    </div>
    </div>

    </div></div>
    """
    
    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
