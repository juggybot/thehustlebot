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
    msg['From'] = formataddr((f'Target', sender_email))
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
    "Please enter the delivered date (January 1, 2025):",
    "Please enter the customer name (Juggy Resells):",
    "Please enter the street address (123 Test Street):",
    "Please enter the suburb (Sydney):",
    "Please enter the state (NSW):",
    "Please enter the postcode (2113):",
    "Please enter the image url (MUST BE FROM TARGET SITE):",
    "Please enter the product name (Airpods 4th Generation):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o primeiro nome do cliente (Juggy):",
    "Por favor, insira a data de entrega (1 de janeiro de 2025):",
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira o endereço (123 Test Street):",
    "Por favor, insira o bairro (Sydney):",
    "Por favor, insira o estado (NSW):",
    "Por favor, insira o código postal (2113):",
    "Por favor, insira a URL da imagem (DEVE SER DO SITE TARGET):",
    "Por favor, insira o nome do produto (Airpods 4ª Geração):",
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
    part1 = random.randint(1000000000000, 9999999999999)  # Random 13-digit number

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
    recipient_email = f'{user_inputs[9]}'
    subject = f"Your item has arrived from order #{order_num}!"

    html_template = f"""
                <div>
        </div>

        <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="min-width:100%">
            <tbody>
                <tr>
                    <td>


                    </td>
                </tr>
            </tbody>
        </table>



        <u></u>














        <div style="margin:0px;padding:0px">
            <div style="font-size:1px;display:none!important">Thanks for shopping with us.</div>

            <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="min-width:100%">
                <tbody>
                    <tr>
                        <td>
                            <table style="table-layout:fixed" role="presentation" width="100%" border="0" cellspacing="0"
                                cellpadding="0">
                                <tbody>
                                    <tr>
                                        <td style="padding:10px 0px" bgcolor="#ffffff" align="center">
                                            <table style="width:640px" class="m_-1337409137134888839wrapper" role="presentation"
                                                width="640" border="0" cellspacing="0" cellpadding="0">
                                                <tbody>
                                                    <tr>
                                                        <td>

                                                            <table role="presentation" width="100%" border="0" cellspacing="0"
                                                                cellpadding="0">


                                                                <tbody>
                                                                    <tr>
                                                                        <td>

                                                                            <table role="presentation" width="20%" border="0"
                                                                                align="left" cellspacing="0" cellpadding="0">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td>
                                                                                            <table role="presentation"
                                                                                                width="100%" border="0"
                                                                                                cellspacing="0" cellpadding="0">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td align="left"><img
                                                                                                                src="https://target.scene7.com/is/image/Target/bullseye_email?scl=1&amp;wid=150&amp;hei=150&amp;fmt=png-alpha"
                                                                                                                alt="Target Logo"
                                                                                                                style="display: block; padding: 5px 0px 3px 20px; font-family: Arial; font-weight: normal; font-size: 12px; border: 0px; background-color: rgb(255, 255, 255); color: rgb(204, 0, 0);"
                                                                                                                class="m_-1337409137134888839header-logo"
                                                                                                                width="45"
                                                                                                                border="0"></td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                        </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>



                                                                            <table role="presentation" width="62%" border="0"
                                                                                align="right" cellspacing="0" cellpadding="0">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td>
                                                                                            <table role="presentation"
                                                                                                width="100%" border="0"
                                                                                                cellspacing="0" cellpadding="0">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td style="padding:21px 20px 0px 10px;font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;font-weight:normal;font-size:16px;line-height:18px;color:rgb(102,102,102)"
                                                                                                            class="m_-1337409137134888839header-ordernum"
                                                                                                            align="right"> Order
                                                                                                            #

                                                                                                            <a href="https://click.oe.target.com/"
                                                                                                                style="text-decoration:none;font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;color:rgb(102,102,102)"
                                                                                                                target="_blank">{order_num}</a>

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
            <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="min-width:100%">
                <tbody>
                    <tr>
                        <td>
                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout:fixed"
                                role="presentation">
                                <tbody>
                                    <tr>
                                        <td align="center" bgcolor="#ffffff" style="padding:0px">

                                            <table border="0" cellpadding="0" cellspacing="0" width="640" style="width:640px"
                                                class="m_-1337409137134888839wrapper" role="presentation">

                                                <tbody>
                                                    <tr>
                                                        <td style="padding:0px 20px" valign="top" bgcolor="#ffffff"
                                                            align="center">
                                                            <h1 style="padding:0px;font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;font-size:38px;line-height:45px;margin:15px 10px 10px;color:rgb(204,0,0)"
                                                                class="m_-1337409137134888839banner-headline">


                                                                {user_inputs[0]}, your order has arrived


                                                            </h1>
                                                            <h2 style="margin:15px 10px 15px 0px;font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;font-size:23px;line-height:28px;text-align:center;color:rgb(51,51,51)"
                                                                class="m_-1337409137134888839banner-headline2">
                                                                Delivered {user_inputs[1]}
                                                            </h2>
                                                            <img src="https://target.scene7.com/is/image/Target/Joy-Delivered_v2_2x?scl=1"
                                                                width="325" alt="Bullseye in a box"
                                                                style="font-family: Arial; padding: 25px 10px 10px; color: rgb(204, 0, 0);">

                                                            <h3 align="center"
                                                                style="margin:15px 10px 10px;font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;font-size:16px;line-height:23px;color:rgb(51,51,51)"
                                                                class="m_-1337409137134888839banner-headline2">
                                                                Time to kick up your feet, settle in and enjoy your new stuff.
                                                            </h3>

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
            <table cellpadding="0" cellspacing="0" width="100%" style="min-width:100%">
                <tbody>
                    <tr>
                        <td>
                            <table style="table-layout:fixed" border="0" width="100%" cellspacing="0" cellpadding="0">
                                <tbody>
                                    <tr>
                                        <td style="padding:10px 0px 0px" bgcolor="#ffffff" align="center">

                                            <table style="width:640px" class="m_-1337409137134888839wrapper" border="0"
                                                width="640" cellspacing="0" cellpadding="0">
                                                <tbody>
                                                    <tr>
                                                        <td>

                                                            <table border="0" width="100%" cellspacing="0" cellpadding="0"
                                                                align="left">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="padding:5px 50px 10px;font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif"
                                                                            align="center">
                                                                            <p
                                                                                style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;font-weight:normal;font-size:15px;line-height:24px;margin:0px 0px 10px;color:rgb(51,51,51)">
                                                                                Thanks again for shopping Target.</p>
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

            <table cellpadding="0" cellspacing="0" width="100%" style="min-width:100%">
                <tbody>
                    <tr>
                        <td>
                            <table style="table-layout:fixed;width:100%!important" role="presentation" width="100%"
                                cellspacing="0" cellpadding="0" border="0">
                                <tbody>
                                    <tr>
                                        <td style="padding:0px" bgcolor="#ffffff" align="center">
                                            <table style="width:768px" class="m_-1337409137134888839wrapper" role="presentation"
                                                width="768" cellspacing="0" cellpadding="0" border="0" align="center">
                                                <tbody>
                                                    <tr>
                                                        <td style="padding:20px 0px" align="center">
                                                            <table cellspacing="0" cellpadding="0" border="0" align="center">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="border-radius:3px" bgcolor="#cc0000"
                                                                            align="center"><a
                                                                                href="https://click.oe.target.com/"
                                                                                style="font-size:16px;font-family:Helvetica,Arial,sans-serif;font-weight:normal;text-decoration:none;display:inline-block;border:1px solid rgb(204,0,0);padding:12px 50px;border-radius:3px;color:rgb(255,255,255)"
                                                                                target="_blank">Visit order details</a></td>
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
            <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="min-width:100%">
                <tbody>
                    <tr>
                        <td>
                            <table style="table-layout:fixed" role="presentation" width="100%" cellspacing="0" cellpadding="0"
                                border="0">
                                <tbody>
                                    <tr>
                                        <td style="padding:20px 0px 0px" bgcolor="#ffffff" align="center">

                                            <table style="width:640px" class="m_-1337409137134888839wrapper" role="presentation"
                                                width="640" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td>

                                                            <table role="presentation" width="100%" cellspacing="0"
                                                                cellpadding="0" border="0">
                                                                <tbody>
                                                                    <tr>
                                                                        <td>

                                                                            <table class="m_-1337409137134888839wrapper"
                                                                                role="presentation" width="100%" cellspacing="0"
                                                                                cellpadding="0" border="0" align="left">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td style="padding:5px 15px 0px">
                                                                                            <table role="presentation"
                                                                                                width="100%" cellspacing="0"
                                                                                                cellpadding="0" border="0">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td style="padding:15px 50px 0px;font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;font-size:15px;line-height:24px;color:rgb(51,51,51)"
                                                                                                            align="center">
                                                                                                            <a href="https://click.oe.target.com/"
                                                                                                                target="_blank"
                                                                                                                style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif"><img
                                                                                                                    src="https://target.scene7.com/is/image/Target/icon-box-2x?scl=1"
                                                                                                                    style="display: block; font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;"
                                                                                                                    alt="Target concierge shipping box"
                                                                                                                    width="80"
                                                                                                                    border="0"></a>
                                                                                                            <h2 style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;font-size:19px;line-height:21px;margin:15px 0px 0px;color:rgb(51,51,51)"
                                                                                                                class="m_-1337409137134888839divider-bar-text"
                                                                                                                align="center">
                                                                                                                Any issues with
                                                                                                                your order?</h2>
                                                                                                            <p
                                                                                                                style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;margin:10px 0px;font-size:15px;line-height:24px;color:rgb(51,51,51)">
                                                                                                                Fixing it is
                                                                                                                fast! Save time
                                                                                                                and fix it
                                                                                                                online. We’ll
                                                                                                                guide you
                                                                                                                through anything
                                                                                                                that’s not quite
                                                                                                                right.</p>
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
                            <table style="table-layout:fixed;width:100%" role="presentation" width="100%" cellspacing="0"
                                cellpadding="0" border="0" align="center">
                                <tbody>
                                    <tr>
                                        <td style="padding:0px" bgcolor="#ffffff" align="center">

                                            <table style="width:640px" class="m_-1337409137134888839wrapper" role="presentation"
                                                width="640" cellspacing="0" cellpadding="0" border="0" align="center">
                                                <tbody>
                                                    <tr>
                                                        <td style="padding:15px 0px" align="center">

                                                            <table cellspacing="0" cellpadding="0" border="0" align="center">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="border-radius:3px" bgcolor="#ffffff"
                                                                            align="center"><a
                                                                                href="https://click.oe.target.com/"
                                                                                style="font-size:15px;font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;text-decoration:none;display:inline-block;border:1px solid rgb(136,136,136);padding:12px 35px;border-radius:3px;color:rgb(51,51,51)"
                                                                                target="_blank">Fix an issue</a></td>
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
            <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="min-width:100%">
                <tbody>
                    <tr>
                        <td>
                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout:fixed"
                                role="presentation">
                                <tbody>
                                    <tr>
                                        <td align="center" bgcolor="#ffffff" style="padding:20px 0px 10px">

                                            <table border="0" cellpadding="0" cellspacing="0" width="640" style="width:640px"
                                                class="m_-1337409137134888839wrapper" role="presentation">

                                                <tbody>
                                                    <tr>
                                                        <td>

                                                            <table border="0" cellpadding="0" cellspacing="0" width="100%"
                                                                style="width:100%" role="presentation">

                                                                <tbody>
                                                                    <tr>
                                                                        <td align="center" style="padding:12px 0px"
                                                                            bgcolor="#eff0f1"
                                                                            class="m_-1337409137134888839divider-bar-gray">
                                                                            <h1 align="center"
                                                                                style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;font-weight:bold;font-size:19px;line-height:22px;margin:0px;color:rgb(51,51,51)"
                                                                                class="m_-1337409137134888839divider-bar-text">
                                                                                Item delivered</h1>
                                                                        </td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td align="center" valign="top" bgcolor="#FFFFFF"
                                                                            border="0" height="11" width="27"
                                                                            style="padding:0px;font-size:11px;line-height:11px;height:11px;width:27px">
                                                                            <img border="0" width="27" height="11"
                                                                                src="https://target.scene7.com/is/image/Target/down-arrow?scl=1"
                                                                                style="display: block;" alt="down arrow"></td>
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
            <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="min-width:100%">
                <tbody>
                    <tr>
                        <td>



                            <table style="table-layout:fixed" role="presentation" width="100%" cellspacing="0" cellpadding="0"
                                border="0">
                                <tbody>
                                    <tr>
                                        <td style="padding:15px 0px 0px" bgcolor="#ffffff" align="center">

                                            <table style="width:540px" class="m_-1337409137134888839wrapper80"
                                                role="presentation" width="540" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="padding:0px 0px 30px">

                                                            <h1 style="padding:0px;font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;font-weight:bold;font-size:16px;line-height:18px;color:rgb(51,51,51)"
                                                                class="m_-1337409137134888839ship-address" align="center">
                                                                Delivered to: <span
                                                                    style="font-weight:normal;font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;color:rgb(51,51,51)">{user_inputs[2]} <a
                                                                        href="https://www.google.com/maps/search/"
                                                                        style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif">{user_inputs[3]}, {user_inputs[4]}, {user_inputs[5]}, {user_inputs[6]}</a></span> </h1>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>



                            <table style="table-layout:fixed" role="presentation" width="100%" cellspacing="0" cellpadding="0"
                                border="0">
                                <tbody>
                                    <tr>
                                        <td style="padding:10px 0px 0px" bgcolor="#ffffff" align="center">

                                            <table style="width:540px" class="m_-1337409137134888839wrapper80"
                                                role="presentation" width="548" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td>

                                                            <table role="presentation" width="100%" cellspacing="0"
                                                                cellpadding="0" border="0">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="padding:0px 0px 15px">

                                                                            <table
                                                                                class="m_-1337409137134888839product-col-left"
                                                                                role="presentation" width="40%" cellspacing="0"
                                                                                cellpadding="0" border="0" align="left">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td style="padding:0px 35px 0px 0px"
                                                                                            class="m_-1337409137134888839product-image"
                                                                                            align="center">

                                                                                            <a href="https://click.oe.target.com/"
                                                                                                target="_blank"><img
                                                                                                    src="{user_inputs[7]}"
                                                                                                    alt="{user_inputs[8]}"
                                                                                                    style="width: 175px; height: auto; font-family: Arial; font-size: 16px; line-height: 24px; color: rgb(204, 0, 0);"
                                                                                                    width="175" border="0"></a>

                                                                                        </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>



                                                                            <table
                                                                                class="m_-1337409137134888839product-col-right"
                                                                                role="presentation" width="59%" cellspacing="0"
                                                                                cellpadding="0" border="0" align="left">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td style="padding:20px 0px 0px"
                                                                                            class="m_-1337409137134888839product-details"
                                                                                            align="left">

                                                                                            <h2
                                                                                                style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;font-size:18px;font-weight:bold;line-height:27px;margin:0px;color:rgb(51,51,51)">
                                                                                                <a href="https://click.oe.target.com/"
                                                                                                    style="text-decoration:none;outline:currentcolor;font-weight:bold;font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;color:rgb(51,51,51)"
                                                                                                    target="_blank">{user_inputs[8]}</a></h2>



                                                                                            <p
                                                                                                style="margin:5px 0px 0px;font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;font-size:15px;line-height:24px;color:rgb(51,51,51)">
                                                                                                Qty: 1 </p>




                                                                                            <table role="presentation"
                                                                                                width="100%" cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                align="left">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td style="padding:10px 0px 0px"
                                                                                                            valign="top">
                                                                                                            <table
                                                                                                                role="presentation"
                                                                                                                width="100%"
                                                                                                                cellspacing="0"
                                                                                                                cellpadding="0"
                                                                                                                border="0"
                                                                                                                align="left">
                                                                                                                <tbody>
                                                                                                                    <tr>



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

            <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="min-width:100%">
                <tbody>
                    <tr>
                        <td>

                            <table style="table-layout:fixed" role="presentation" width="100%" cellspacing="0" cellpadding="0"
                                border="0">
                                <tbody>
                                    <tr>
                                        <td style="padding:20px 0px 0px" bgcolor="#ffffff" align="center">

                                            <table style="width:640px" class="m_-1337409137134888839wrapper" role="presentation"
                                                width="640" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td align="center">

                                                            <table style="width:100%" class="m_-1337409137134888839wrapper"
                                                                role="presentation" width="100%" cellspacing="0" cellpadding="0"
                                                                border="0" align="center">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="width:100%;padding:12px 0px"
                                                                            class="m_-1337409137134888839divider-bar-gray"
                                                                            bgcolor="#eff0f1" align="center">
                                                                            <h2 style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;font-size:19px;line-height:22px;margin:0px;color:rgb(51,51,51)"
                                                                                class="m_-1337409137134888839divider-bar-text"
                                                                                align="center">Returning something?</h2>
                                                                        </td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td border="0"
                                                                            style="padding:0px;font-size:11px;line-height:11px;height:11px;width:27px"
                                                                            width="27" valign="top" bgcolor="#FFFFFF"
                                                                            align="center" height="11"><img
                                                                                src="https://target.scene7.com/is/image/Target/down-arrow?scl=1"
                                                                                style="display: block;" alt="down arrow"
                                                                                width="27" border="0" height="11"></td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>

                                                            <table role="presentation" width="100%" cellspacing="0"
                                                                cellpadding="0" border="0">
                                                                <tbody>
                                                                    <tr>
                                                                        <td>

                                                                            <table class="m_-1337409137134888839wrapper"
                                                                                role="presentation" width="100%" cellspacing="0"
                                                                                cellpadding="0" border="0" align="left">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td style="padding:5px 0px 0px">
                                                                                            <table role="presentation"
                                                                                                width="100%" cellspacing="0"
                                                                                                cellpadding="0" border="0">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td style="padding:20px 10px 0px;font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;color:rgb(51,51,51)"
                                                                                                            align="center">


                                                                                                            <p
                                                                                                                style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;font-size:15px;margin:5px 0px;color:rgb(51,51,51)">
                                                                                                                <strong
                                                                                                                    style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif">This
                                                                                                                    barcode
                                                                                                                    works as
                                                                                                                    your receipt
                                                                                                                    for in-store
                                                                                                                    returns.</strong>
                                                                                                            </p>
                                                                                                            <img style="width: 308px; height: 53px; font-family: Arial; text-align: center; font-size: 16px; color: rgb(204, 0, 0);"
                                                                                                                title="barcode"
                                                                                                                alt="return receipt barcode 230183991028934277"
                                                                                                                src="http://cl.S7.exct.net/LiveContent.aspx?qs=98f299b619f437b0b8b93d810bfb75cd2876085fa8590d09e4bd212fbe96f1f63b00c2cd9901b07a167964c57c628b01a447f4156fe3c181630cf73aaefa2dbd0033fa6e9bfefbc88ed1769b9b034a00afb7ea8becea2479ebd4d6b287ee58c9f708f35edeadb156"
                                                                                                                width="308"
                                                                                                                hspace="0"
                                                                                                                height="53"
                                                                                                                border="0">
                                                                                                            <p
                                                                                                                style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;font-size:14px;margin:5px 0px 15px;color:rgb(51,51,51)">
                                                                                                                <a
                                                                                                                    style="text-decoration:none;font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;color:rgb(51,51,51)">2-3018-3991-0289-3427-7</a>
                                                                                                            </p>

                                                                                                            <p
                                                                                                                style="font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;font-size:14px;margin:5px 10px 10px;color:rgb(51,51,51)">
                                                                                                                VCD: <a
                                                                                                                    style="text-decoration:none;font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;color:rgb(51,51,51)">755-214-458</a>
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
                            <table style="table-layout:fixed;width:100%!important" role="presentation" width="100%"
                                cellspacing="0" cellpadding="0" border="0">
                                <tbody>
                                    <tr>
                                        <td style="padding:0px" bgcolor="#ffffff">

                                            <table style="width:640px" class="m_-1337409137134888839wrapper" role="presentation"
                                                width="640" cellspacing="0" cellpadding="0" border="0" align="center">
                                                <tbody>
                                                    <tr>
                                                        <td style="padding:20px 0px">

                                                            <table cellspacing="0" cellpadding="0" border="0" align="center">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="border-radius:3px" bgcolor="#ffffff"
                                                                            align="center"><a
                                                                                href="https://click.oe.target.com/"
                                                                                style="font-size:15px;font-family:&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif;text-decoration:none;display:inline-block;border:1px solid rgb(136,136,136);padding:12px 50px;border-radius:3px;color:rgb(51,51,51)"
                                                                                target="_blank">Start a return by mail</a></td>
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
            <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="min-width:100%">
                <tbody>
                    <tr>
                        <td>
                            <table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation">


                                <tbody>
                                    <tr>
                                        <td align="center" valign="top" width="100%" style="padding:15px 0px 0px">

                                            <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%"
                                                style="max-width:640px" role="presentation">
                                                <tbody>
                                                    <tr>
                                                        <td align="center" valign="top"
                                                            style="padding:20px 10px;background-color:rgb(51,51,51)">

                                                            <p
                                                                style="font-family:Helvetica,Arial,sans-serif;font-size:16px;margin:0px!important;color:rgb(255,255,255)">
                                                                <a href="https://click.oe.target.com/"
                                                                    style="text-decoration:none;font-family:Helvetica,Arial,sans-serif;color:rgb(255,255,255)"
                                                                    target="_blank">Even more great ways to <strong
                                                                        style="font-family:Helvetica,Arial,sans-serif">save</strong>.
                                                                    ›</a></p>

                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>

                                        </td>
                                    </tr>



                                    <tr>
                                        <td align="center" valign="top" width="100%" style="padding:0px">

                                            <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%"
                                                style="max-width:640px" role="presentation">
                                                <tbody>
                                                    <tr>
                                                        <td align="center" valign="top" style="font-size:0px">

                                                            <div style="display:inline-block;max-width:320px;width:100%"
                                                                class="m_-1337409137134888839mw-wrapper">


                                                                <div style="display:inline-block;max-width:160px;vertical-align:top;width:100%"
                                                                    class="m_-1337409137134888839mw-wrapper">
                                                                    <table align="left" border="0" cellpadding="0"
                                                                        cellspacing="0" width="100%" style="max-width:160px"
                                                                        class="m_-1337409137134888839mw-wrapper"
                                                                        role="presentation">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td align="center" valign="top"
                                                                                    style="padding-bottom:15px;padding-top:5px;background-color:rgb(255,255,255)">
                                                                                    <a href="https://click.oe.target.com/"
                                                                                        style="border:medium"
                                                                                        target="_blank"><img
                                                                                            src="https://scene7.targetimg1.com/is/image/Target/Free2DayShipTruck?scl=1&amp;fmt=gif-alpha"
                                                                                            width="120" border="0"
                                                                                            alt="Free 2-Day Shipping"
                                                                                            style="display: block; font-size: 18px; text-align: center; color: rgb(204, 0, 0);"></a>
                                                                                    <p
                                                                                        style="font-family:Helvetica,Arial,sans-serif;font-size:13px;margin:0px;font-weight:bold;color:rgb(51,51,51)">
                                                                                        <a href="https://click.oe.target.com/"
                                                                                            style="text-decoration:none;font-family:Helvetica,Arial,sans-serif;color:rgb(51,51,51)"
                                                                                            target="_blank">Free 2-day ship
                                                                                            ›</a></p>

                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </div>

                                                                <div style="display:inline-block;max-width:160px;vertical-align:top;width:100%;background-color:rgb(250,250,250)"
                                                                    class="m_-1337409137134888839mw-wrapper">
                                                                    <table align="left" border="0" cellpadding="0"
                                                                        cellspacing="0" width="100%"
                                                                        style="max-width:160px;background-color:rgb(250,250,250)"
                                                                        class="m_-1337409137134888839mw-wrapper"
                                                                        role="presentation">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td align="center" valign="top"
                                                                                    style="padding-bottom:15px;padding-top:5px;background-color:rgb(250,250,250)">
                                                                                    <a href="https://click.oe.target.com/"
                                                                                        style="border:medium"
                                                                                        target="_blank"><img
                                                                                            src="https://scene7.targetimg1.com/is/image/Target/mrkt_clearance?scl=1&amp;fmt=gif-alpha"
                                                                                            alt="Target Clearance" width="120"
                                                                                            style="display: block; font-size: 18px; text-align: center; color: rgb(204, 0, 0);"
                                                                                            border="0"></a>
                                                                                    <p
                                                                                        style="font-family:Helvetica,Arial,sans-serif;font-size:13px;margin:0px;font-weight:bold;color:rgb(51,51,51)">
                                                                                        <a href="https://click.oe.target.com/"
                                                                                            style="text-decoration:none;font-family:Helvetica,Arial,sans-serif;color:rgb(51,51,51)"
                                                                                            target="_blank">Clearance ›</a></p>

                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </div>

                                                            </div>



                                                            <div style="display:inline-block;max-width:320px;vertical-align:top;width:100%"
                                                                class="m_-1337409137134888839mw-wrapper">

                                                                <div style="display:inline-block;max-width:160px;width:100%;background-color:rgb(245,245,245)"
                                                                    class="m_-1337409137134888839mw-wrapper">
                                                                    <table align="left" border="0" cellpadding="0"
                                                                        cellspacing="0" width="100%"
                                                                        style="max-width:160px;background-color:rgb(245,245,245)"
                                                                        class="m_-1337409137134888839mw-wrapper"
                                                                        role="presentation">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td align="center" valign="top"
                                                                                    style="padding-bottom:15px;padding-top:5px;background-color:rgb(245,245,245)">
                                                                                    <a href="https://click.oe.target.com/"
                                                                                        style="border:medium"
                                                                                        target="_blank"><img
                                                                                            src="https://scene7.targetimg1.com/is/image/Target/mrkt_targetapp?scl=1&amp;fmt=gif-alpha"
                                                                                            alt="Target Cartwheel" width="120"
                                                                                            style="display: block; font-size: 18px; text-align: center; color: rgb(204, 0, 0);"
                                                                                            border="0"></a>
                                                                                    <p
                                                                                        style="font-family:Helvetica,Arial,sans-serif;font-size:13px;margin:0px;font-weight:bold;color:rgb(51,51,51)">
                                                                                        <a href="https://click.oe.target.com/"
                                                                                            style="text-decoration:none;font-family:Helvetica,Arial,sans-serif;color:rgb(51,51,51)"
                                                                                            target="_blank">Target App ›</a></p>

                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </div>

                                                                <div style="display:inline-block;max-width:160px;vertical-align:top;width:100%;background-color:rgb(240,240,240)"
                                                                    class="m_-1337409137134888839mw-wrapper">
                                                                    <table align="left" border="0" cellpadding="0"
                                                                        cellspacing="0" width="100%"
                                                                        style="max-width:160px;background-color:rgb(240,240,240)"
                                                                        class="m_-1337409137134888839mw-wrapper"
                                                                        role="presentation">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td align="center" valign="top"
                                                                                    style="padding-bottom:15px;padding-top:5px;background-color:rgb(240,240,240)">
                                                                                    <a href="https://click.oe.target.com/"
                                                                                        style="border:medium"
                                                                                        target="_blank"><img
                                                                                            src="https://scene7.targetimg1.com/is/image/Target/SDDbag2x?scl=1&amp;fmt=gif-alpha"
                                                                                            alt="Same Day Delivery" width="120"
                                                                                            style="display: block; font-size: 18px; text-align: center; color: rgb(204, 0, 0);"
                                                                                            border="0"></a>
                                                                                    <p
                                                                                        style="font-family:Helvetica,Arial,sans-serif;font-size:13px;margin:0px;font-weight:bold;color:rgb(51,51,51)">
                                                                                        <a href="https://click.oe.target.com/"
                                                                                            style="text-decoration:none;font-family:Helvetica,Arial,sans-serif;color:rgb(51,51,51)"
                                                                                            target="_blank">Same Day Delivery
                                                                                            ›</a></p>

                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
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
            </table>
            <table cellpadding="0" cellspacing="0" width="100%" style="min-width:100%">
                <tbody>
                    <tr>
                        <td>
                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout:fixed"
                                align="center" role="presentation">
                                <tbody>
                                    <tr>
                                        <td align="center" style="padding:15px 0px 0px"
                                            class="m_-1337409137134888839footer-noborder">


                                            <table border="0" cellpadding="0" cellspacing="0" width="640" style="width:640px"
                                                align="center" role="presentation">
                                                <tbody>
                                                    <tr>
                                                        <td style="background:repeat;border-bottom-width:1px;border-bottom-style:solid;height:1px;width:100%;margin:0px;padding-top:0px;padding-bottom:0px;border-bottom-color:rgb(214,214,214)"
                                                            class="m_-1337409137134888839footer-noborder"> </td>
                                                    </tr>
                                                </tbody>
                                            </table>

                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout:fixed"
                                role="presentation">
                                <tbody>
                                    <tr>
                                        <td align="center" bgcolor="#ffffff" style="padding:30px 0px 0px">


                                            <table border="0" cellpadding="0" cellspacing="0" width="640" style="width:640px"
                                                class="m_-1337409137134888839wrapper90" align="center" role="presentation">
                                                <tbody>
                                                    <tr>
                                                        <td>

                                                            <table border="0" cellpadding="0" cellspacing="0" width="100%"
                                                                role="presentation">
                                                                <tbody>
                                                                    <tr>
                                                                        <td>

                                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                                align="left"
                                                                                class="m_-1337409137134888839footer-border-top-bottom"
                                                                                role="presentation">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td style="padding:0px 25px"
                                                                                            class="m_-1337409137134888839footer-pad">
                                                                                            <a href="https://click.oe.target.com/"
                                                                                                align="center"
                                                                                                style="text-decoration:none;display:block"
                                                                                                target="_blank"><span
                                                                                                    style="font-family:Arial,sans-serif;font-size:14px;font-weight:normal;line-height:16px;color:rgb(51,51,51)"
                                                                                                    class="m_-1337409137134888839footer-text">Help</span></a>
                                                                                        </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>



                                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                                align="left"
                                                                                class="m_-1337409137134888839footer-border-bottom"
                                                                                role="presentation">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td style="padding:0px 25px"
                                                                                            class="m_-1337409137134888839footer-pad">
                                                                                            <a href="https://click.oe.target.com/"
                                                                                                align="center"
                                                                                                style="text-decoration:none;display:block"
                                                                                                target="_blank"><span
                                                                                                    style="font-family:Arial,sans-serif;font-size:14px;font-weight:normal;line-height:16px;color:rgb(51,51,51)"
                                                                                                    class="m_-1337409137134888839footer-text">Returns</span></a>
                                                                                        </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>



                                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                                align="left"
                                                                                class="m_-1337409137134888839footer-border-bottom"
                                                                                role="presentation">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td style="padding:0px 25px"
                                                                                            class="m_-1337409137134888839footer-pad">
                                                                                            <a href="https://click.oe.target.com/"
                                                                                                align="center"
                                                                                                style="text-decoration:none;display:block"
                                                                                                target="_blank"><span
                                                                                                    style="font-family:Arial,sans-serif;font-size:14px;font-weight:normal;line-height:16px;color:rgb(51,51,51)"
                                                                                                    class="m_-1337409137134888839footer-text">Contact</span></a>
                                                                                        </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>



                                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                                align="left"
                                                                                class="m_-1337409137134888839footer-border-bottom"
                                                                                role="presentation">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td style="padding:0px 25px"
                                                                                            class="m_-1337409137134888839footer-pad">
                                                                                            <a href="https://click.oe.target.com/"
                                                                                                align="center"
                                                                                                style="text-decoration:none;display:block"
                                                                                                target="_blank"><span
                                                                                                    style="font-family:Arial,sans-serif;font-size:14px;font-weight:normal;line-height:16px;color:rgb(51,51,51)"
                                                                                                    class="m_-1337409137134888839footer-text">Find
                                                                                                    a store </span></a></td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>



                                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                                align="left"
                                                                                class="m_-1337409137134888839footer-border-bottom"
                                                                                role="presentation">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td style="padding:0px 25px"
                                                                                            class="m_-1337409137134888839footer-pad">
                                                                                            <a href="https://click.oe.target.com/"
                                                                                                align="center"
                                                                                                style="text-decoration:none;display:block"
                                                                                                target="_blank"><span
                                                                                                    style="font-family:Arial,sans-serif;font-size:14px;font-weight:normal;line-height:16px;color:rgb(51,51,51)"
                                                                                                    class="m_-1337409137134888839footer-text">Terms
                                                                                                    of use </span></a></td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>



                                                                            <table border="0" cellpadding="0" cellspacing="0"
                                                                                align="left"
                                                                                class="m_-1337409137134888839footer-border-bottom"
                                                                                role="presentation">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td style="padding:0px 25px"
                                                                                            class="m_-1337409137134888839footer-pad">
                                                                                            <a href="https://click.oe.target.com/"
                                                                                                align="center"
                                                                                                style="text-decoration:none;display:block"
                                                                                                target="_blank"><span
                                                                                                    style="font-family:Arial,sans-serif;font-size:14px;font-weight:normal;line-height:16px;color:rgb(51,51,51)"
                                                                                                    class="m_-1337409137134888839footer-text">Privacy</span></a>
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
                                                            <table border="0" cellpadding="0" cellspacing="0" width="100%"
                                                                role="presentation">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="padding:30px 0px 0px" align="center"><a
                                                                                href="https://click.oe.target.com/"
                                                                                style="text-decoration:none;display:block"
                                                                                target="_blank"><span
                                                                                    style="font-family:Arial,sans-serif;font-size:17px;font-weight:normal;line-height:22px;color:rgb(204,0,0)"
                                                                                    class="m_-1337409137134888839footer-targetcom">Target.com
                                                                                </span></a></td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="padding:5px 0px 20px">
                                                            <table border="0" cellpadding="0" cellspacing="0" width="100%"
                                                                role="presentation">
                                                                <tbody>
                                                                    <tr>
                                                                        <td align="center"
                                                                            style="padding:0px;font-family:Arial,sans-serif;font-weight:normal;font-size:13px;line-height:15px;color:rgb(0,0,0)">
                                                                            © 2025 Target Brands, Inc. </td>
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

            <img src="https://click.oe.target.com/open.aspx?"
                width="1" height="1" alt="">


        </div>

        </div>
        </div>
    """

    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
