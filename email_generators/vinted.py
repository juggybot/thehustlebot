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
    msg['From'] = formataddr((f'Vinted', sender_email))
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
    "Please enter the sellers username (JuggyIsAReseller):",
    "Please enter the product name (Rilakkuma pouch):",
    "Please enter the product cost (WITHOUT THE $):",
    "Please enter the delivery cost (WITHOUT THE $):",
    "Please enter the tax cost (WITHOUT THE $):",
    "Please enter the total cost (WITHOUT THE $):",
    "Please enter the card type (Visa/Mastercard):",
    "Please enter the last 4 digits of the card used (1234):",
    "Please enter the payment date (12/03):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o primeiro nome do cliente (Juggy):",
    "Por favor, insira o nome de usuário do vendedor (JuggyIsAReseller):",
    "Por favor, insira o nome do produto (Bolsa Rilakkuma):",
    "Por favor, insira o custo do produto (SEM O SÍMBOLO $):",
    "Por favor, insira o custo da entrega (SEM O SÍMBOLO $):",
    "Por favor, insira o valor do imposto (SEM O SÍMBOLO $):",
    "Por favor, insira o custo total (SEM O SÍMBOLO $):",
    "Por favor, insira o tipo de cartão (Visa/Mastercard):",
    "Por favor, insira os últimos 4 dígitos do cartão usado (1234):",
    "Por favor, insira a data do pagamento (12/03):",
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
    # Generate random order
    part1 = random.randint(10000000000, 99999999999)  # Random 11-digit number
    
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
    recipient_email = f'{user_inputs[11]}'
    subject = f"Your receipt for '{user_inputs[2]}'"

    html_template = f"""
            <div>
    <div
        style="color:rgb(51,51,51);font-family:Helvetica,sans-serif;font-size:18px;font-weight:normal;line-height:150%;margin:0px auto;width:100%;max-width:680px">
        <table role="presentation" border="0" width="100%" cellspacing="0" cellpadding="0">
        <tbody>
            <tr>
            <td style="padding:0% 9%" align="left" valign="middle" height="110"><a href="https://vinted.com"
                rel="noreferrer noopener" target="_blank"
                data-saferedirecturl="https://www.google.com/url?q=https://vinted.com&amp;source=gmail&amp;ust=1744037468230000&amp;usg=AOvVaw2TuZR9s3dsZXkhTAkio_8n"><img
                    style="min-height:30px;display:block"
                    src="https://ci3.googleusercontent.com/meips/ADKq_NZ2XA6SHKSmoIcGlwZW4P4OCuTD8PHPmZZ-3GhqyNb6RY2tx5v24Vofeo_9sx0PDJu0FfdMU3ReiitzXtrrIV_x00_3usBX9sX4QO6wBtep4GYLo_PUKhJMoCvz=s0-d-e1-ft#https://static-assets.vinted.com/images/email/_shared/logo/default.png"
                    border="0" class="CToWUd" data-bit="iit"></a></td>
            </tr>
        </tbody>
        </table>
        <img
        src="https://ci3.googleusercontent.com/meips/ADKq_NZUSVGirhheuvf25tQSyzsqOgTpW8v8JOnXz0nZ_zW-NruFsfkm6sxVUfTbPIilouEvxz964s5jhfyaB1VFl_SKfLgjLm9Wd88B3_uYsg1gwwhebweGyCOvS-6mENeu6NMDHoCX2GZ7BGByOp3PSkocPe1yTLsaMCT9hhOXKOdrTrZax8dQ0fVW-gOFiIHXjPCBtWhM-4xsRLLJqdpdr4E=s0-d-e1-ft#https://www.vinted.com/crm/email_track?crm_email_id=182&amp;hash=260950611%3Ad4a2a23a14450499c9d033041bad14f531502fe735aab9ffb26dc78d3440ade0"
        width="1" height="1" alt="" class="CToWUd" data-bit="iit">
        <p style="line-height:20.8px"><strong>Hello {user_inputs[0]},</strong></p>
        <p style="line-height:20.8px">Your payment has been received.&nbsp;<br></p>
        <p style="line-height:20.8px"><strong>Your Vinted purchase&nbsp;receipt:</strong></p>
        <table style="border-collapse:collapse;border:0px solid black;width:100%;margin-bottom:10px;min-height:278.383px"
        border="0" cellspacing="1" cellpadding="1" align="left">
        <tbody>
            <tr style="min-height:22.3984px">
            <td style="width:150px;border:0px solid black;min-height:22.3984px"><strong>Seller:</strong></td>
            <td style="border:0px solid black;min-height:22.3984px">{user_inputs[1]}</td>
            </tr>
            <tr style="min-height:54.3984px">
            <td style="border:0px solid black;min-height:54.3984px"><strong>Order:</strong></td>
            <td style="border:0px solid black;min-height:54.3984px">
                <p>{user_inputs[2]}<br></p>
            </td>
            </tr>
            <tr style="min-height:67.1953px">
            <td style="border:0px solid black;min-height:67.1953px"><strong>Paid:</strong></td>
            <td style="border:0px solid black;min-height:67.1953px">{user_inputs[10]}{user_inputs[6]}&nbsp;&nbsp; <em>(shipping: </em> <em>{user_inputs[10]}{user_inputs[4]} +
                item: </em> <em>{user_inputs[10]}{user_inputs[3]} + Buyer Protection fee: {user_inputs[10]}0.00 + Sales tax: {user_inputs[10]}{user_inputs[5]})</em></td>
            </tr>
            <tr style="min-height:67.1953px">
            <td style="border:0px solid black;min-height:67.1953px"><strong>Payment method:</strong></td>
            <td style="border:0px solid black;min-height:67.1953px">{user_inputs[7]}, **********{user_inputs[8]} ({user_inputs[10]}{user_inputs[6]})</td>
            </tr>
            <tr style="min-height:22.3984px">
            <td style="border:0px solid black;min-height:22.3984px"><strong>Payment date:</strong></td>
            <td style="border:0px solid black;min-height:22.3984px">{user_inputs[9]}</td>
            </tr>
            <tr style="min-height:22.3984px">
            <td style="border:0px solid black;min-height:22.3984px"><strong>Transaction ID:</strong></td>
            <td style="border:0px solid black;min-height:22.3984px">{order_num}</td>
            </tr>
            <tr style="min-height:22.3984px">
            <td style="border:0px solid black;min-height:22.3984px">&nbsp;</td>
            </tr>
        </tbody>
        </table>
        <p>We’ll send you a message as soon as puts "{user_inputs[2]}" in the mail. Sellers have up to 7 days to make it
        happen. Once your package is sent, expect it to arrive in about 2 - 5 business days.&nbsp;</p>
        <p></p>
        <p>Team Vinted</p>
        <table role="presentation" border="0" width="100%" cellspacing="0" cellpadding="0">
        <tbody>
            <tr>
            <td align="right" bgcolor="#ffffff"><img style="display:block;max-width:680px;width:100%"
                src="https://ci3.googleusercontent.com/meips/ADKq_NbdF2O5iyb2RZSeE_Hchg61O_lHBGckPYUY6N55gAv3zxcbuIM9YSHUGN4xvbw5LAeb_BnLGU4Eu0jLJkoUZz_h9ywGrLE0xOQMYCVDCjd0hfFwLuGT_SnsRLWwusI7iYQ=s0-d-e1-ft#https://static-assets.vinted.com/admin/editor_assets/en/subtract-footer.png"
                width="680" border="0" class="CToWUd" data-bit="iit"></td>
            </tr>
            <tr>
            <td height="30">&nbsp;</td>
            </tr>
            <tr>
            <td
                style="font-family:Helvetica,sans-serif;font-size:12px;line-height:16px;margin:0px;color:rgb(73,75,77);padding:0% 9%;text-align:left"
                align="left">
                <p style="font-size:12px;line-height:16px;margin:0px;color:rgb(73,75,77)"><span style="font-weight:400">We
                    are required to send you this email in order to fulfill our <a
                    style="text-decoration:underline;color:#333333" href="https://www.vinted.com/terms_and_conditions"
                    rel="noreferrer noopener" target="_blank"
                    data-saferedirecturl="https://www.google.com/url?q=https://www.vinted.com/terms_and_conditions&amp;source=gmail&amp;ust=1744037468230000&amp;usg=AOvVaw3BWSQzm9h4MH-pS7Q4-uMS">Terms
                    and Conditions</a>, or for other legal reasons. It is not possible to unsubscribe from these emails.
                    To read up on your rights and more detailed information on how we use your personal data, please see our
                </span><a style="text-decoration:underline;color:#333333" href="https://www.vinted.com/privacy-policy"
                    rel="noreferrer noopener" target="_blank"
                    data-saferedirecturl="https://www.google.com/url?q=https://www.vinted.com/privacy-policy&amp;source=gmail&amp;ust=1744037468230000&amp;usg=AOvVaw16MQ4EEfJGyzTxGEx0rz9W"><span
                    style="font-weight:400">Privacy Policy</span></a><span style="font-weight:400">.</span></p>
            </td>
            </tr>
            <tr>
            <td height="64">&nbsp;</td>
            </tr>
        </tbody>
        </table>
        <div class="yj6qo"></div>
        <div class="adL">
        </div>
    </div>
    <div class="adL">
    </div>
    </div>
    """

    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
