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
    msg['From'] = formataddr((f'Myer', sender_email))
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
    "Please enter the image url (Must be Myer image link):",
    "Please enter the item name (Invictus Platinum):",
    "Please enter the item SKU (942183100):",
    "Please enter the item price (WITHOUT THE $ SIGN):",
    "Please enter the delivery cost (WITHOUT THE $ SIGN):",
    "Please enter the order total (WITHOUT THE $ SIGN):",
    "Please enter the customer full name (Juggy Resells):",
    "Please enter the order date (Sunday 22 Jan 2024):",
    "Please enter the customer email (juggyresells@gmail.com):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o primeiro nome do cliente (Juggy):",
    "Por favor, insira a URL da imagem (Deve ser um link de imagem da Myer):",
    "Por favor, insira o nome do item (Invictus Platinum):",
    "Por favor, insira o SKU do item (942183100):",
    "Por favor, insira o preço do item (SEM O SÍMBOLO $):",
    "Por favor, insira o custo de entrega (SEM O SÍMBOLO $):",
    "Por favor, insira o total do pedido (SEM O SÍMBOLO $):",
    "Por favor, insira o nome completo do cliente (Juggy Resells):",
    "Por favor, insira a data do pedido (Domingo, 22 de Janeiro de 2024):",
    "Por favor, insira o e-mail do cliente (juggyresells@gmail.com):",
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
    part1 = random.randint(1000000000, 9999999999)  # Random 11-digit number

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
    subject = f"We’ve Received Your Order"

    html_template=f"""
        <div style="margin:0px;padding:0px" bgcolor="#e6e6e6" class="m_8173575535960799369em_body1">
        <img src="https://click.email.myerone.com.au/open.aspx?ffcb10-fe831679706c027573-fe0515717564007f72167571-fe9713737563057f71-ff66167371-fe2713797d65057e711271-fef911707d6d04&amp;d=70192&amp;bmt=0"
            width="1" height="1" alt="">
        <table width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#e6e6e6">


            <tbody>
                <tr>
                    <td align="center" valign="top">
                        <table align="center" class="m_8173575535960799369em_main_table" bgcolor="#e6e6e6" width="640"
                            border="0" cellspacing="0" cellpadding="0" style="table-layout:fixed;width:640px">
                            <tbody>
                                <tr>
                                    <td height="15" class="m_8173575535960799369em_height"
                                        style="line-height:0px;font-size:0px">
                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                            width="1" height="1" border="0" style="display: block;">
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center" class="m_8173575535960799369em_height"
                                        style="font-family:Arial,sans-serif;font-size:10px;line-height:18px;text-align:center;font-weight:normal;color:rgb(0,0,0)">
                                        Can&#39;t see this email?
                                        <a href="https://view.email.myerone.com.au/?qs=22e508e6efc0694f7bdc04cc945b9c1952e720618741d8752e8b49eacc3d814d5d5682703fa26ffef3229b68b5df8939b99ce8e99514a8ed5dc42e07e2a85126cd7ca93fdc62b7ea2f73394c1364acb3"
                                            style="text-decoration:underline;font-family:Arial,sans-serif;color:rgb(0,0,0)"
                                            target="_blank">View online</a>
                                    </td>
                                </tr>
                                <tr>
                                    <td height="15" class="m_8173575535960799369em_height"
                                        style="line-height:0px;font-size:0px">
                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                            width="1" height="1" border="0" style="display: block;">
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>



                <tr>
                    <td align="center" valign="top">
                        <table align="center" class="m_8173575535960799369em_main_table" bgcolor="#ffffff" width="640"
                            border="0" cellspacing="0" cellpadding="0" style="table-layout:fixed;width:640px">
                            <tbody>
                                <tr>
                                    <td height="42" class="m_8173575535960799369em_height"
                                        style="line-height:0px;font-size:0px">
                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                            width="1" height="1" border="0" style="display: block;">
                                    </td>
                                </tr>
                                <tr>
                                    <td valign="top" align="center">
                                        <a href="https://click.email.myerone.com.au/?qs=59cafe77a81f306b25e225f56534001ccd2b49058009fe86bf8644af0f969e09bfbd7a80c2d8eb97737676dc71ac3b34a3ebd2c63d4cf936"
                                            style="text-decoration:none" target="_blank"><img
                                                src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_logo1.jpg"
                                                alt="MYER" width="124" height="37"
                                                style="display: block; max-width: 124px; font-family: Arial, sans-serif; font-size: 14px; line-height: 16px; color: rgb(85, 85, 85);"
                                                border="0"></a>
                                    </td>
                                </tr>

                            </tbody>
                        </table>
                    </td>
                </tr>


                <tr>
                    <td><u></u></td>
                </tr>
                <tr>

                    <td align="center" valign="top">
                        <table align="center" class="m_8173575535960799369em_main_table" bgcolor="#ffffff" width="640"
                            border="0" cellspacing="0" cellpadding="0" style="table-layout:fixed;width:640px">
                            <tbody>
                                <tr>
                                    <td height="40" class="m_8173575535960799369em_height"
                                        style="line-height:0px;font-size:0px"><img
                                            src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                            alt="" width="1" height="1" border="0" style="display: block;"></td>
                                </tr>
                                <tr>
                                    <td class="m_8173575535960799369em_orange m_8173575535960799369em_aside" valign="top"
                                        align="left"
                                        style="font-family:Arial,sans-serif;font-size:24px;padding-left:63px;padding-right:63px;line-height:28px;font-weight:400;letter-spacing:2px;color:rgb(233,81,48)">
                                        THANK YOU FOR SHOPPING WITH US</td>
                                </tr>
                                <tr>
                                    <td height="30" style="line-height:0px;font-size:0px"><img
                                            src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                            alt="" width="1" height="1" border="0" style="display: block;"></td>
                                </tr>
                                <tr>
                                    <td class="m_8173575535960799369em_black m_8173575535960799369em_aside" valign="top"
                                        align="left"
                                        style="font-family:Arial,sans-serif;font-size:14px;padding-left:63px;padding-right:63px;line-height:21px;font-weight:400;color:rgb(0,0,0)">
                                        Hi
                                        {user_inputs[0]},
                                    </td>
                                </tr>
                                <tr>
                                    <td height="18" style="line-height:0px;font-size:0px"><img
                                            src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                            alt="" width="1" height="1" border="0" style="display: block;"></td>
                                </tr>
                                <tr>
                                    <td class="m_8173575535960799369em_black m_8173575535960799369em_aside" valign="top"
                                        align="left"
                                        style="font-family:Arial,sans-serif;font-size:14px;padding-left:63px;padding-right:63px;line-height:21px;font-weight:400;color:rgb(0,0,0)">
                                        Thanks for your order #
                                        {order_num}
                                        .
                                        <br><br><strong style="font-family:Arial,sans-serif">Myer Track My
                                            Order</strong><br>

                                        You can check the status of your order and parcels anytime with
                                        <a href="https://www.myer.com.au/track-my-order?utm_medium=email&amp;utm_source=sfmc&amp;utm_campaign=OrderConfirmationHD&amp;orderNum=1110213838"
                                            style="font-weight:bold;text-decoration:underline;font-family:Arial,sans-serif;color:rgb(0,0,0)"
                                            target="_blank">Myer Track My Order.</a><br><br><strong
                                            style="font-family:Arial,sans-serif">Multiple Parcels</strong><br>
                                        Occasionally your order might need to be sent in multiple parcels because items are
                                        coming from different locations. If this happens, we&#39;ll send you an email and an
                                        SMS when each parcel is sent.
                                        <br><br>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td align="center" valign="top">
                        <table align="center" class="m_8173575535960799369em_main_table" width="640" border="0"
                            cellspacing="0" cellpadding="0" style="table-layout:fixed;width:640px" bgcolor="#faf8f9">
                            <tbody>
                                <tr>
                                    <td valign="top" align="center" style="padding:0px 63px"
                                        class="m_8173575535960799369em_aside">
                                        <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center">
                                            <tbody>
                                                <tr>
                                                    <td valign="top" align="center">
                                                        <table width="100%" border="0" cellspacing="0" cellpadding="0"
                                                            align="center">
                                                            <tbody>
                                                                <tr>
                                                                    <td height="7" style="line-height:0px;font-size:0px">
                                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/spacer.gif"
                                                                            height="1" width="1" alt=""
                                                                            style="display: block; border: medium;"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td height="1" bgcolor="#000000"
                                                                        style="line-height:1px;font-size:1px"><img
                                                                            src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/spacer.gif"
                                                                            height="1" width="1" alt=""
                                                                            style="display: block; border: medium;"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td height="8" style="line-height:0px;font-size:0px">
                                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/spacer.gif"
                                                                            height="1" width="1" alt=""
                                                                            style="display: block; border: medium;"></td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                    <td width="37" class="m_8173575535960799369em_side"><img
                                                            src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/spacer.gif"
                                                            height="1" width="1" alt=""
                                                            style="display: block; border: medium;"></td>
                                                    <td class="m_8173575535960799369em_black" width="160" valign="top"
                                                        align="center"
                                                        style="font-family:Arial,sans-serif;font-size:14px;line-height:16px;color:rgb(0,0,0)">
                                                        ORDER DETAILS</td>
                                                    <td width="37" class="m_8173575535960799369em_side"><img
                                                            src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/spacer.gif"
                                                            height="1" width="1" alt=""
                                                            style="display: block; border: medium;"></td>
                                                    <td valign="top" align="center">
                                                        <table width="100%" border="0" cellspacing="0" cellpadding="0"
                                                            align="center">
                                                            <tbody>
                                                                <tr>
                                                                    <td height="7" style="line-height:0px;font-size:0px">
                                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/spacer.gif"
                                                                            height="1" width="1" alt=""
                                                                            style="display: block; border: medium;">
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td height="1" bgcolor="#000000"
                                                                        style="line-height:1px;font-size:1px"><img
                                                                            src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/spacer.gif"
                                                                            height="1" width="1" alt=""
                                                                            style="display: block; border: medium;"></td>
                                                                </tr>
                                                                <tr>
                                                                    <td height="8" style="line-height:0px;font-size:0px">
                                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/spacer.gif"
                                                                            height="1" width="1" alt=""
                                                                            style="display: block; border: medium;"></td>
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
                                    <td height="45" class="m_8173575535960799369em_height"><img
                                            src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/spacer.gif"
                                            height="1" width="1" alt="" style="display: block; border: medium;"></td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>

                <tr>
                    <td align="center" valign="top">
                        <table align="center" class="m_8173575535960799369em_main_table" bgcolor="#faf8f9" width="640"
                            border="0" cellspacing="0" cellpadding="0" style="table-layout:fixed;width:640px">
                            <tbody>
                                <tr>
                                    <td valign="top" align="center" class="m_8173575535960799369em_aside"
                                        style="padding-left:63px;padding-right:63px">
                                        <table align="center" width="100%" border="0" cellspacing="0" cellpadding="0">
                                            <tbody>
                                                <tr>
                                                    <td valign="top" align="right" width="250"
                                                        style="font-family:Arial,sans-serif;font-size:14px;font-weight:bold;color:rgb(29,29,29)">
                                                        Description</td>
                                                    <td valign="top" class="m_8173575535960799369em_hide" align="right"
                                                        width="170"
                                                        style="font-family:Arial,sans-serif;font-size:14px;font-weight:bold;color:rgb(29,29,29)">
                                                        Item</td>
                                                    <td valign="top" align="right" width="96"
                                                        style="font-family:Arial,sans-serif;font-size:14px;font-weight:bold;color:rgb(29,29,29)">
                                                        Total</td>
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
                        <table align="center" class="m_8173575535960799369em_main_table" bgcolor="#faf8f9" width="640"
                            border="0" cellspacing="0" cellpadding="0" style="table-layout:fixed;width:640px">
                            <tbody>
                                <tr>
                                    <td height="30" class="m_8173575535960799369em_height"
                                        style="line-height:0px;font-size:0px"><img
                                            src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                            width="1" height="1" alt="" border="0" style="display: block;"></td>
                                </tr>
                                <tr>
                                    <td valign="top" align="center" class="m_8173575535960799369em_aside"
                                        style="padding-left:63px;padding-right:63px">
                                        <table align="center" width="100%" border="0" cellspacing="0" cellpadding="0">
                                            <tbody>
                                                <tr>
                                                    <td valign="top" align="center" width="143"><img
                                                            src="{user_inputs[1]}"
                                                            alt="{user_inputs[2]}" width="143"
                                                            class="m_8173575535960799369em_full_img"
                                                            style="display: block; max-width: 143px;" border="0"></td>
                                                    <td width="16" style="width:16px" class="m_8173575535960799369em_side">
                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                                            width="1" height="1" alt="" border="0" style="display: block;">
                                                    </td>
                                                    <td valign="top" align="center">
                                                        <table align="center" width="100%" border="0" cellspacing="0"
                                                            cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td valign="top" align="center">
                                                                        <table align="center" width="100%" border="0"
                                                                            cellspacing="0" cellpadding="0">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td valign="top" align="center">
                                                                                        <table width="274"
                                                                                            style="width:274px"
                                                                                            class="m_8173575535960799369em_wrapper"
                                                                                            align="left" border="0"
                                                                                            cellspacing="0" cellpadding="0">
                                                                                            <tbody>
                                                                                                <tr>
                                                                                                    <td align="center"
                                                                                                        valign="top">
                                                                                                        <table width="274"
                                                                                                            style="width:274px"
                                                                                                            class="m_8173575535960799369em_wrapper"
                                                                                                            align="center"
                                                                                                            border="0"
                                                                                                            cellspacing="0"
                                                                                                            cellpadding="0">
                                                                                                            <tbody>
                                                                                                                <tr>
                                                                                                                    <td align="left"
                                                                                                                        valign="top">
                                                                                                                        <table
                                                                                                                            width="144"
                                                                                                                            style="width:144px;max-width:185px"
                                                                                                                            class="m_8173575535960799369em_wrapper"
                                                                                                                            align="left"
                                                                                                                            border="0"
                                                                                                                            cellspacing="0"
                                                                                                                            cellpadding="0">
                                                                                                                            <tbody>
                                                                                                                                <tr>
                                                                                                                                    <td class="m_8173575535960799369em_grey1"
                                                                                                                                        valign="top"
                                                                                                                                        align="left"
                                                                                                                                        style="font-family:Arial,sans-serif;font-size:14px;line-height:16px;word-break:break-all;color:rgb(85,85,85)">
                                                                                                                                        <strong
                                                                                                                                            style="font-family:Arial,sans-serif">                                                                                                                                        {user_inputs[2]}</strong><br><span
                                                                                                                                            style="font-size:10px;font-family:Arial,sans-serif"><strong
                                                                                                                                                style="font-family:Arial,sans-serif">
                                                                                                                                                QTY1</strong>

                                                                                                                                            <br>


                                                                                                                                            SKU:{user_inputs[3]}

                                                                                                                                            <br>

                                                                                                                                            Delivery
                                                                                                                                            Method:
                                                                                                                                            Standard
                                                                                                                                        </span>
                                                                                                                                    </td>
                                                                                                                                    <td width="10"
                                                                                                                                        style="width:10px">
                                                                                                                                    </td>
                                                                                                                                </tr>
                                                                                                                            </tbody>
                                                                                                                        </table>
                                                                                                                        <table
                                                                                                                            width="110"
                                                                                                                            style="width:100px"
                                                                                                                            class="m_8173575535960799369em_wrapper"
                                                                                                                            align="right"
                                                                                                                            border="0"
                                                                                                                            cellspacing="0"
                                                                                                                            cellpadding="0">
                                                                                                                            <tbody>
                                                                                                                                <tr>
                                                                                                                                    <td align="left"
                                                                                                                                        valign="top">
                                                                                                                                        <table
                                                                                                                                            width="110"
                                                                                                                                            style="width:110px"
                                                                                                                                            class="m_8173575535960799369em_wrapper"
                                                                                                                                            align="left"
                                                                                                                                            border="0"
                                                                                                                                            cellspacing="0"
                                                                                                                                            cellpadding="0">
                                                                                                                                            <tbody>
                                                                                                                                                <tr>
                                                                                                                                                    <td class="m_8173575535960799369em_grey2 m_8173575535960799369em_left"
                                                                                                                                                        valign="top"
                                                                                                                                                        align="right"
                                                                                                                                                        style="font-family:Arial,sans-serif;font-size:14px;line-height:18px;color:rgb(104,104,104)">
                                                                                                                                                        <strong
                                                                                                                                                            style="font-family:Arial,sans-serif">
                                                                                                                                                            {user_inputs[10]}{user_inputs[4]}</strong>
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
                                                                                    <td align="right" valign="top">
                                                                                        <table width="80"
                                                                                            class="m_8173575535960799369em_wrapper"
                                                                                            style="width:80px" align="right"
                                                                                            border="0" cellspacing="0"
                                                                                            cellpadding="0">
                                                                                            <tbody>
                                                                                                <tr>
                                                                                                    <td class="m_8173575535960799369em_grey2 m_8173575535960799369em_left"
                                                                                                        valign="top"
                                                                                                        align="right"
                                                                                                        style="font-family:Arial,sans-serif;font-size:14px;line-height:18px;color:rgb(104,104,104)">
                                                                                                        <strong
                                                                                                            style="font-family:Arial,sans-serif">
                                                                                                            {user_inputs[10]}{user_inputs[4]}</strong>
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
                                    <td height="30" class="m_8173575535960799369em_height"
                                        style="line-height:0px;font-size:0px"><img
                                            src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                            width="1" height="1" alt="" border="0" style="display: block;"></td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td align="center" valign="top">
                        <table align="center" class="m_8173575535960799369em_main_table" bgcolor="#faf8f9" width="640"
                            border="0" cellspacing="0" cellpadding="0" style="table-layout:fixed;width:640px">
                            <tbody>
                                <tr>
                                    <td height="2" style="line-height:1px;font-size:1px" bgcolor="#d9d7d7"><img
                                            src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/spacer.gif"
                                            alt="" height="1" width="1" style="display: block; border: medium;"></td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td align="center" valign="top">
                        <table align="center" class="m_8173575535960799369em_main_table" bgcolor="#f7f7f7" width="640"
                            border="0" cellspacing="0" cellpadding="0" style="table-layout:fixed;width:640px">
                            <tbody>
                                <tr>
                                    <td height="30" class="m_8173575535960799369em_height"
                                        style="line-height:0px;font-size:0px"><img
                                            src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                            alt="" width="1" height="1" border="0" style="display: block;"></td>
                                </tr>
                                <tr>
                                    <td valign="top" align="center" class="m_8173575535960799369em_aside"
                                        style="padding-left:222px;padding-right:63px">
                                        <table align="center" width="100%" border="0" cellspacing="0" cellpadding="0">
                                            <tbody>
                                                <tr>
                                                    <td valign="top" align="center">
                                                        <table align="center" width="100%" border="0" cellspacing="0"
                                                            cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td class="m_8173575535960799369em_grey" valign="top"
                                                                        align="left"
                                                                        style="font-family:Arial,sans-serif;font-size:14px;line-height:18px;color:rgb(29,29,29)">
                                                                        SUB TOTAL
                                                                        <br>DELIVERY CHARGE<br>
                                                                    </td>
                                                                    <td><img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                                                            alt="" width="1" height="1" border="0"
                                                                            style="display: block;"></td>
                                                                    <td class="m_8173575535960799369em_grey" valign="top"
                                                                        align="right"
                                                                        style="font-family:Arial,sans-serif;font-size:14px;line-height:18px;font-weight:bold;color:rgb(29,29,29)">
                                                                        {user_inputs[10]}{user_inputs[4]}<br>
                                                                        {user_inputs[10]}{user_inputs[5]}<br></td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td height="20"
                                                        style="line-height:0px;font-size:0px;border-bottom-width:1px;border-bottom-style:dashed;border-bottom-color:rgb(135,135,135)">
                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                                            alt="" width="1" height="1" border="0" style="display: block;">
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td height="20" style="line-height:0px;font-size:0px"><img
                                                            src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                                            alt="" width="1" height="1" border="0" style="display: block;">
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td valign="top" align="center">
                                                        <table align="center" width="100%" border="0" cellspacing="0"
                                                            cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td class="m_8173575535960799369em_grey" valign="top"
                                                                        align="left"
                                                                        style="font-family:Arial,sans-serif;font-size:18px;line-height:19px;color:rgb(29,29,29)">
                                                                        <strong
                                                                            style="font-family:Arial,sans-serif">TOTAL</strong><br><span
                                                                            style="font-size:10px;font-family:Arial,sans-serif">This
                                                                            is not a tax invoice</span></td>
                                                                    <td>
                                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                                                            alt="" width="1" height="1" border="0"
                                                                            style="display: block;">
                                                                    </td>
                                                                    <td class="m_8173575535960799369em_grey" valign="top"
                                                                        align="right"
                                                                        style="font-family:Arial,sans-serif;font-size:18px;line-height:19px;color:rgb(29,29,29)">
                                                                        <strong style="font-family:Arial,sans-serif">
                                                                            {user_inputs[10]}{user_inputs[6]}</strong><br>
                                                                    </td>
                                                                    <td><br></td>
                                                                </tr>
                                                                <tr>
                                                                    <td class="m_8173575535960799369em_grey"
                                                                        style="font-family:Arial,sans-serif;font-size:10px;line-height:10px">

                                                                        Change of mind returns and exchanges
                                                                        <br>
                                                                        will not be offered for goods designated as
                                                                        <strong
                                                                            style="font-family:Arial,sans-serif">*CLEARANCE*</strong><br><br>
                                                                        Exclusions and conditions apply. Please visit
                                                                        <a href="https://www.myer.com.au/content/returns-policy"
                                                                            style="font-weight:bold;text-decoration:underline;font-family:Arial,sans-serif;color:rgb(0,0,0)"
                                                                            target="_blank">our Returns Policy.</a>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td><img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                                                            alt="" width="1" height="1" border="0"
                                                                            style="display: block;"></td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td></td>
                                                </tr>
                                                <tr>
                                                    <td></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td valign="top" align="center"><img
                                            src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_img1.png"
                                            alt="" height="31" width="640"
                                            style="display: block; border: medium; font-family: Arial, sans-serif; font-size: 12px; line-height: 20px; max-width: 640px; color: rgb(0, 0, 0);"
                                            class="m_8173575535960799369em_full_img"></td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>

                <tr>
                    <td align="center" valign="top">
                        <table align="center" class="m_8173575535960799369em_main_table" width="640" border="0"
                            cellspacing="0" cellpadding="0" style="table-layout:fixed;width:640px" bgcolor="#e6e6e6">
                            <tbody>
                                <tr>
                                    <td valign="top" align="center" bgcolor="#ffffff">
                                        <table align="center" width="100%" border="0" cellspacing="0" cellpadding="0">
                                            <tbody>
                                                <tr>
                                                    <td height="20" style="line-height:0px;font-size:0px"><img
                                                            src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                                            alt="" width="1" height="1" border="0" style="display: block;">
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td valign="top" align="center" style="padding:0px 63px 20px"
                                                        class="m_8173575535960799369em_aside">
                                                        <table width="100%" border="0" cellspacing="0" cellpadding="0"
                                                            align="center">
                                                            <tbody>
                                                                <tr>
                                                                    <td class="m_8173575535960799369em_black" valign="top"
                                                                        align="left"
                                                                        style="width:50%;font-family:Arial,sans-serif;font-size:14px;line-height:20px;letter-spacing:3px;color:rgb(0,0,0)">
                                                                        YOUR PAYMENT SUMMARY</td>
                                                                    <td class="m_8173575535960799369em_side">
                                                                        <hr
                                                                            style="border-width:2px 0px 0px;border-color:rgb(255,255,255)">
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td valign="top" align="center" style="padding:0px 63px"
                                                        class="m_8173575535960799369em_aside">
                                                        <table align="center" width="100%" border="0" cellspacing="0"
                                                            cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td valign="top" align="center">
                                                                        <table align="left" width="240" border="0"
                                                                            cellspacing="0" cellpadding="0"
                                                                            style="width:240px"
                                                                            class="m_8173575535960799369em_wrapper">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td class="m_8173575535960799369em_black"
                                                                                        valign="top" align="left"
                                                                                        style="font-family:Arial,sans-serif;font-size:14px;line-height:20px;padding-bottom:12px;color:rgb(0,0,0)">
                                                                                        <strong
                                                                                            style="font-family:Arial,sans-serif">Name:
                                                                                        </strong>{user_inputs[7]}</td>
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
                                                    <td valign="top" align="center" style="padding:0px 63px"
                                                        class="m_8173575535960799369em_aside">
                                                        <table align="center" width="100%" border="0" cellspacing="0"
                                                            cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td valign="top" align="center">
                                                                        <table align="left" width="240" border="0"
                                                                            cellspacing="0" cellpadding="0"
                                                                            style="width:240px"
                                                                            class="m_8173575535960799369em_wrapper">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td class="m_8173575535960799369em_black"
                                                                                        valign="top" align="left"
                                                                                        style="font-family:Arial,sans-serif;font-size:14px;line-height:20px;padding-bottom:12px;color:rgb(0,0,0)">
                                                                                        <strong
                                                                                            style="font-family:Arial,sans-serif">Order
                                                                                            number: </strong>{order_num}</td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                        <table align="left" width="265" border="0" cellspacing="0"
                                                            cellpadding="0" style="width:265px"
                                                            class="m_8173575535960799369em_wrapper">
                                                            <tbody>
                                                                <tr>
                                                                    <td class="m_8173575535960799369em_black" valign="top"
                                                                        align="left"
                                                                        style="font-family:Arial,sans-serif;font-size:14px;line-height:20px;padding-bottom:12px;color:rgb(0,0,0)">
                                                                        <strong style="font-family:Arial,sans-serif">Order
                                                                            date:</strong> {user_inputs[8]}</td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td valign="top" align="center" style="padding:0px 63px"
                                                        class="m_8173575535960799369em_aside">
                                                        <table align="center" width="100%" border="0" cellspacing="0"
                                                            cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td valign="top" align="center">
                                                                        <table align="left" width="240" border="0"
                                                                            cellspacing="0" cellpadding="0"
                                                                            style="width:240px"
                                                                            class="m_8173575535960799369em_wrapper">

                                                                            <tbody>
                                                                                <tr>
                                                                                    <td class="m_8173575535960799369em_black"
                                                                                        valign="top" align="left"
                                                                                        style="font-family:Arial,sans-serif;font-size:14px;line-height:20px;padding-bottom:12px;color:rgb(0,0,0)">
                                                                                        <strong
                                                                                            style="font-family:Arial,sans-serif">Payment
                                                                                            type:</strong> CREDIT CARD</td>
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
                                                    <td valign="top" align="center" style="padding:0px 63px"
                                                        class="m_8173575535960799369em_aside">
                                                        <table align="center" width="100%" border="0" cellspacing="0"
                                                            cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td valign="top" align="center">
                                                                        <table align="left" width="314" border="0"
                                                                            cellspacing="0" cellpadding="0"
                                                                            style="width:314px"
                                                                            class="m_8173575535960799369em_wrapper">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td class="m_8173575535960799369em_black"
                                                                                        valign="top" align="left"
                                                                                        style="font-family:Arial,sans-serif;font-size:14px;line-height:20px;padding-bottom:12px;color:rgb(0,0,0)">
                                                                                        <strong
                                                                                            style="font-family:Arial,sans-serif">Email:
                                                                                        </strong><a
                                                                                            href="mailto:nic.notman3011@gmail.com"
                                                                                            style="font-family:Arial,sans-serif;text-decoration:none!important;color:rgb(0,0,0)"
                                                                                            target="_blank">
                                                                                            <span
                                                                                                style="font-family:Arial,sans-serif;text-decoration:none!important;color:rgb(0,0,0)">{user_inputs[9]}</span></a>
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
                                                    <td valign="top" align="center" style="padding:0px 63px"
                                                        class="m_8173575535960799369em_aside">
                                                        <table align="center" width="100%" border="0" cellspacing="0"
                                                            cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td valign="top" align="center"
                                                                        style="padding-bottom:20px;padding-top:10px"><img
                                                                            src="http://cl.S7.exct.net/LiveContent.aspx?qs=1eb218163dc6cfac8ea9dad2d3e8b2b4219d7a9cb829de76e9c59f5acff55f3ecf5f42b152a885a923f9afa8eeb717862b6ed35daead6662abc66468f4d35fcb92b91d816aad374ba493263a2f712a2aec174b9b8239964a05ad8e3c99b4bf4a"
                                                                            alt="1110213838"
                                                                            style="display: block; max-width: 400px; height: 80px;"
                                                                            border="0" width="400"
                                                                            class="m_8173575535960799369em_img"></td>
                                                                </tr>
                                                            </tbody>
                                                        </table><br>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td height="20" style="line-height:0px;font-size:0px">
                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                                            alt="" width="1" height="1" border="0" style="display: block;">
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="m_8173575535960799369em_orange m_8173575535960799369em_aside1"
                                                        valign="top" align="left"
                                                        style="font-family:Arial,sans-serif;font-size:14px;padding-left:63px;padding-right:63px;line-height:18px;letter-spacing:2px;padding-bottom:15px;font-weight:300;color:rgb(240,104,62)">
                                                        MYER one MEMBERSHIP</td>
                                                </tr>
                                                <tr>
                                                    <td class="m_8173575535960799369em_black m_8173575535960799369em_aside1"
                                                        valign="top" align="left"
                                                        style="font-family:Arial,sans-serif;font-weight:300;font-size:14px;line-height:20px;padding:0px 63px 11px;color:rgb(0,0,0)">
                                                        Join our MYER one loyalty program and be rewarded for shopping at
                                                        Myer. Best of all, membership is free!
                                                        <br><br>
                                                        Perks of being a member:
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td valign="top" align="center" class="m_8173575535960799369em_aside1"
                                                        style="padding-left:63px;padding-right:63px">
                                                        <table align="left" border="0" cellspacing="0" cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td valign="top" align="center">
                                                                        <table align="left" width="30" border="0"
                                                                            cellspacing="0" cellpadding="0"
                                                                            style="width:30px">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td height="7"
                                                                                        style="font-size:0px;line-height:0px">
                                                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                                                                            width="1" height="1" alt=""
                                                                                            border="0"
                                                                                            style="display: block;"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td width="30" align="left" valign="top"
                                                                                        style="font-size:0px;line-height:0px">
                                                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_bullet.jpg"
                                                                                            alt="" style="display: block;"
                                                                                            border="0" width="8" height="7">
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                    <td class="m_8173575535960799369em_black" valign="top"
                                                                        align="left"
                                                                        style="font-family:Arial,sans-serif;font-size:14px;line-height:20px;color:rgb(0,0,0)">
                                                                        Earn 2 Shopping Credits per dollar
                                                                        <sup
                                                                            style="font-size:8px;line-height:0;vertical-align:3px;font-family:Arial,sans-serif">#</sup>
                                                                        spent at Myer.
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td valign="top" align="center" class="m_8173575535960799369em_aside1"
                                                        style="padding-left:63px;padding-right:63px">
                                                        <table align="left" border="0" cellspacing="0" cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td valign="top" align="center">
                                                                        <table align="left" width="30" border="0"
                                                                            cellspacing="0" cellpadding="0"
                                                                            style="width:30px">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td height="7"
                                                                                        style="font-size:0px;line-height:0px">
                                                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                                                                            width="1" height="1" alt=""
                                                                                            border="0"
                                                                                            style="display: block;"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td width="30" align="left" valign="top"
                                                                                        style="font-size:0px;line-height:0px">
                                                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_bullet.jpg"
                                                                                            alt="" style="display: block;"
                                                                                            border="0" width="8" height="7">
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                    <td class="m_8173575535960799369em_black" valign="top"
                                                                        align="left"
                                                                        style="font-family:Arial,sans-serif;font-size:14px;line-height:20px;color:rgb(0,0,0)">
                                                                        Receive a {user_inputs[10]}10 MYER one Reward Card when you reach
                                                                        1000 Shopping Credits.
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td valign="top" align="center" class="m_8173575535960799369em_aside1"
                                                        style="padding-left:63px;padding-right:63px;padding-bottom:20px">
                                                        <table align="left" border="0" cellspacing="0" cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td valign="top" align="center">
                                                                        <table align="left" width="30" border="0"
                                                                            cellspacing="0" cellpadding="0"
                                                                            style="width:30px">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td height="7"
                                                                                        style="font-size:0px;line-height:0px">
                                                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                                                                            width="1" height="1" alt=""
                                                                                            border="0"
                                                                                            style="display: block;"></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td width="30" align="left" valign="top"
                                                                                        style="font-size:0px;line-height:0px">
                                                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_bullet.jpg"
                                                                                            alt="" style="display: block;"
                                                                                            border="0" width="8" height="7">
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                    <td class="m_8173575535960799369em_black" valign="top"
                                                                        align="left"
                                                                        style="font-family:Arial,sans-serif;font-size:14px;line-height:20px;color:rgb(0,0,0)">
                                                                        Exclusive offers and invites to special events.</td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td valign="top" align="left" style="padding:0px 63px"
                                                        class="m_8173575535960799369em_aside">
                                                        <table width="120" align="left" style="width:120px"
                                                            bgcolor="#e95130" border="0" cellspacing="0" cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td height="40" class="m_8173575535960799369em_white"
                                                                        valign="middle" align="center"
                                                                        style="font-family:Arial,sans-serif;font-size:12px;line-height:18px;font-weight:bold;color:rgb(255,255,255)">
                                                                        <a href="https://www.myer.com.au/join"
                                                                            title="Myerone tracking"
                                                                            style="text-decoration:none;line-height:26px;font-weight:bold;font-family:Arial,sans-serif;color:rgb(255,255,255)"
                                                                            target="_blank">Join Now</a></td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td height="25" class="m_8173575535960799369em_height"
                                                        style="line-height:0px;font-size:0px">
                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_spacer.gif"
                                                            width="1" height="1" alt="" border="0" style="display: block;">
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td valign="top" align="center" class="m_8173575535960799369em_aside">
                                                        <img class="m_8173575535960799369em_full_img"
                                                            src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1503390624690_image2.jpg"
                                                            alt="MYER one"
                                                            style="display: block; font-family: Arial, sans-serif; font-size: 20px; line-height: 24px; max-width: 510px; color: rgb(0, 0, 0);"
                                                            border="0" width="510"></td>
                                                </tr>
                                                <tr>
                                                    <td class="m_8173575535960799369em_black m_8173575535960799369em_aside1"
                                                        valign="top" align="left"
                                                        style="font-family:Arial,sans-serif;font-size:10px;padding:10px 63px;line-height:15px;color:rgb(0,0,0)">
                                                        <sup
                                                            style="font-size:8px;line-height:0;vertical-align:3px;font-family:Arial,sans-serif">#</sup>
                                                        Excludes purchases of Gift Cards, credit card and lay-by payments
                                                        and some food and service outlets.
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
                        <table align="center" class="m_8173575535960799369em_main_table" width="640" border="0"
                            cellspacing="0" cellpadding="0" style="table-layout:fixed;width:640px">
                            <tbody>
                                <tr>
                                    <td valign="top" align="center" bgcolor="#f7f7f7">
                                        <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center"
                                            bgcolor="#f7f7f7">

                                            <tbody>
                                                <tr>
                                                    <td height="1" style="line-height:1px;font-size:1px" bgcolor="#d9d7d7">
                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/spacer.gif"
                                                            height="1" width="1" alt=""
                                                            style="display: block; border: medium;">
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td height="22" class="m_8173575535960799369em_height">
                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/spacer.gif"
                                                            height="1" width="1" alt=""
                                                            style="display: block; border: medium;">
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td valign="top" align="center">
                                                        <table width="100%" border="0" cellspacing="0" cellpadding="0"
                                                            align="center">
                                                            <tbody>
                                                                <tr>
                                                                    <td valign="top" align="center">
                                                                        <table width="50%" border="0" cellspacing="0"
                                                                            cellpadding="0" align="right"
                                                                            class="m_8173575535960799369em_wrapper">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td valign="top" align="center"
                                                                                        class="m_8173575535960799369em_pad_topline">
                                                                                        <table width="98%" border="0"
                                                                                            cellspacing="0" cellpadding="0"
                                                                                            align="right">
                                                                                            <tbody>
                                                                                                <tr>


                                                                                                    <td valign="top"
                                                                                                        align="center">
                                                                                                        <table width="100%"
                                                                                                            border="0"
                                                                                                            cellspacing="0"
                                                                                                            cellpadding="0"
                                                                                                            align="right">
                                                                                                            <tbody>
                                                                                                                <tr>
                                                                                                                    <td valign="top"
                                                                                                                        align="center"
                                                                                                                        width="24"
                                                                                                                        style="padding-top:8px;padding-bottom:8px">
                                                                                                                        <img src="https://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/edf34569-3d61-47a9-a137-426fd537f496.png"
                                                                                                                            height="24"
                                                                                                                            width="24"
                                                                                                                            alt=""
                                                                                                                            style="display: block; border: medium; font-family: Arial, sans-serif; font-size: 12px; line-height: 20px; max-width: 47px; color: rgb(0, 0, 0);">
                                                                                                                    </td>
                                                                                                                </tr>
                                                                                                                <tr>
                                                                                                                    <td class="m_8173575535960799369em_black"
                                                                                                                        valign="top"
                                                                                                                        align="center"
                                                                                                                        style="font-family:Arial,sans-serif;font-size:10px;line-height:16px;padding-bottom:8px;color:rgb(0,0,0)">
                                                                                                                        We&#39;re
                                                                                                                        here
                                                                                                                        to
                                                                                                                        help.
                                                                                                                    </td>
                                                                                                                </tr>
                                                                                                                <tr>
                                                                                                                    <td class="m_8173575535960799369em_black"
                                                                                                                        valign="top"
                                                                                                                        align="center"
                                                                                                                        style="font-family:Arial,sans-serif;font-size:10px;line-height:13px;color:rgb(0,0,0)">
                                                                                                                        <a href="https://click.email.myerone.com.au/?qs=59cafe77a81f306b48b150fd7fbe2aecdfc42fe9dcb44bda6fcec50196d2d9d3c77e72c5f910241239f38b39f2483c4ce0a40d6867eaad00"
                                                                                                                            style="font-weight:bold;text-decoration:underline;font-family:Arial,sans-serif;color:rgb(0,0,0)"
                                                                                                                            target="_blank">Chat
                                                                                                                            to
                                                                                                                            the
                                                                                                                            Myer
                                                                                                                            Conceirge.</a>
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
                                                                    <td valign="center">

                                                                        <table width="50%" border="0" cellspacing="0"
                                                                            cellpadding="0" align="left"
                                                                            class="m_8173575535960799369em_wrapper">
                                                                            <tbody>
                                                                                <tr>

                                                                                    <td valign="top" align="left"
                                                                                        class="m_8173575535960799369em_pad_topline">
                                                                                        <table width="98%" border="0"
                                                                                            cellspacing="0" cellpadding="0"
                                                                                            align="left">
                                                                                            <tbody>
                                                                                                <tr>


                                                                                                    <td valign="top"
                                                                                                        align="center">
                                                                                                        <table width="100%"
                                                                                                            border="0"
                                                                                                            cellspacing="0"
                                                                                                            cellpadding="0"
                                                                                                            align="left">
                                                                                                            <tbody>
                                                                                                                <tr>
                                                                                                                    <td valign="top"
                                                                                                                        align="center"
                                                                                                                        width="24"
                                                                                                                        style="padding-top:8px;padding-bottom:8px">
                                                                                                                        <img src="https://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/1b90b8de-9571-4888-bc85-4966f87ef590.png"
                                                                                                                            height="24"
                                                                                                                            width="24"
                                                                                                                            alt=""
                                                                                                                            style="display: block; border: medium; font-family: Arial, sans-serif; font-size: 12px; line-height: 20px; max-width: 47px; color: rgb(0, 0, 0);">
                                                                                                                    </td>
                                                                                                                </tr>
                                                                                                                <tr>
                                                                                                                    <td class="m_8173575535960799369em_black"
                                                                                                                        valign="top"
                                                                                                                        align="center"
                                                                                                                        style="font-family:Arial,sans-serif;font-size:10px;line-height:16px;padding-bottom:8px;color:rgb(0,0,0)">
                                                                                                                        Returns
                                                                                                                        and
                                                                                                                        Exchanges
                                                                                                                        are
                                                                                                                        easy.
                                                                                                                    </td>
                                                                                                                </tr>
                                                                                                                <tr>
                                                                                                                    <td class="m_8173575535960799369em_black"
                                                                                                                        valign="top"
                                                                                                                        align="center"
                                                                                                                        style="font-family:Arial,sans-serif;font-size:10px;line-height:13px;color:rgb(0,0,0)">
                                                                                                                        <a href="https://click.email.myerone.com.au/?qs=59cafe77a81f306bcf4806a25fb0c5e236bc739f4bc06d8d623f1dc2c30817ef04c956ed88c2d2ea985cda86e16db5a920f1b4b77bfb6e71"
                                                                                                                            style="font-weight:bold;text-decoration:underline;font-family:Arial,sans-serif;color:rgb(0,0,0)"
                                                                                                                            target="_blank">View
                                                                                                                            our
                                                                                                                            Returns
                                                                                                                            policy.</a>
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
                                                    <td height="22" class="m_8173575535960799369em_height">
                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/spacer.gif"
                                                            height="1" width="1" alt=""
                                                            style="display: block; border: medium;">
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td height="15" style="line-height:1px;font-size:1px">
                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/spacer.gif"
                                                            height="1" width="1" alt=""
                                                            style="display: block; border: medium;">
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td valign="top" align="center">
                                                        <table width="249" border="0" cellspacing="0" cellpadding="0"
                                                            align="center" style="width:249px">
                                                            <tbody>
                                                                <tr>
                                                                    <td valign="top" align="center">
                                                                        <a href="https://click.email.myerone.com.au/?qs=59cafe77a81f306b7bcb4f012e2d4e1164442b283ca1803a9bd7a5a68ac43acc9793c85c66fb280543deac8970142a2423c8f8365e949b61"
                                                                            style="text-decoration:none"
                                                                            target="_blank"><img
                                                                                src="https://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/d7ece655-86bd-45c8-97b6-34942ec8b657.png"
                                                                                height="24" width="24" alt="FB"
                                                                                style="display: block; border: medium; font-family: Arial, sans-serif; font-size: 16px; line-height: 37px; max-width: 37px; color: rgb(0, 0, 0);"></a>
                                                                    </td>
                                                                    <td width="16">
                                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/spacer.gif"
                                                                            height="1" width="1" alt=""
                                                                            style="display: block; border: medium;">
                                                                    </td>
                                                                    <td valign="top" align="center">
                                                                        <a href="https://click.email.myerone.com.au/?qs=59cafe77a81f306badfa2dfa90b45c9657192cbecd895357515c871211c05f123f9fcc6377aa277adc594d20920407afd2fdb1be13efa284"
                                                                            style="text-decoration:none"
                                                                            target="_blank"><img
                                                                                src="https://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/e3cd78db-a5e1-4e4b-9659-4ba972e3f666.png"
                                                                                height="24" width="24" alt="TW"
                                                                                style="display: block; border: medium; font-family: Arial, sans-serif; font-size: 16px; line-height: 37px; max-width: 37px; color: rgb(0, 0, 0);"></a>
                                                                    </td>
                                                                    <td width="16">
                                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/spacer.gif"
                                                                            height="1" width="1" alt=""
                                                                            style="display: block; border: medium;">
                                                                    </td>
                                                                    <td valign="top" align="center">
                                                                        <a href="https://click.email.myerone.com.au/?qs=59cafe77a81f306b61f32718b5d95e0b9ce44cd97865ea8be7f710a15295a43b45d433dce4d1a16b3c794847dbe5fb9d824b0e2e2b71322f"
                                                                            style="text-decoration:none"
                                                                            target="_blank"><img
                                                                                src="https://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/8200b3c6-1700-48c6-9d6a-6d748e142c2e.png"
                                                                                height="24" width="24" alt="INSTA"
                                                                                style="display: block; border: medium; font-family: Arial, sans-serif; font-size: 16px; line-height: 37px; max-width: 37px; color: rgb(0, 0, 0);"></a>
                                                                    </td>
                                                                    <td width="16">
                                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/spacer.gif"
                                                                            height="1" width="1" alt=""
                                                                            style="display: block; border: medium;">
                                                                    </td>
                                                                    <td valign="top" align="center">
                                                                        <a href="https://click.email.myerone.com.au/?qs=59cafe77a81f306b8e5ed61e852a4067179deed2735ea19c964380355e311a9d78ed161d73f1ea4676f0ad67bf1d1c24632d6240d22a8fab"
                                                                            style="text-decoration:none"
                                                                            target="_blank"><img
                                                                                src="https://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/0df27919-2802-4645-8bed-a58638b4563d.png"
                                                                                height="24" width="24" alt="YT"
                                                                                style="display: block; border: medium; font-family: Arial, sans-serif; font-size: 16px; line-height: 37px; max-width: 37px; color: rgb(0, 0, 0);"></a>
                                                                    </td>
                                                                    <td width="16">
                                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/spacer.gif"
                                                                            height="1" width="1" alt=""
                                                                            style="display: block; border: medium;">
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td height="22" class="m_8173575535960799369em_height">
                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/spacer.gif"
                                                            height="1" width="1" alt=""
                                                            style="display: block; border: medium;">
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="m_8173575535960799369em_black" valign="top" align="center"
                                                        style="font-family:Arial,sans-serif;font-size:8px;line-height:15px;padding-bottom:4px;color:rgb(0,0,0)">
                                                        <a href="https://click.email.myerone.com.au/?qs=59cafe77a81f306bb29d0dbda21e1c0dcfb2e160e377fc3c5d55a3149e992c12c11de303c90794105d1d143396877303c3602d21e83213af"
                                                            style="text-decoration:none;font-family:Arial,sans-serif;color:rgb(0,0,0)"
                                                            target="_blank">Terms &amp; Conditions</a>
                                                        <span class="m_8173575535960799369em_hide"
                                                            style="font-family:Arial,sans-serif">-</span>
                                                        <span class="m_8173575535960799369em_br"
                                                            style="font-family:Arial,sans-serif"></span>
                                                        <a href="https://click.email.myerone.com.au/?qs=59cafe77a81f306bd3f85a2a345b7704e574760f6e1b2a09a77867eb7ba63e7cf67c9d90213d9fbb20a1b275441b38155fa2e7eefc0a61bb"
                                                            style="text-decoration:none;font-family:Arial,sans-serif;color:rgb(0,0,0)"
                                                            target="_blank">Privacy Policy</a>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="m_8173575535960799369em_black" valign="top" align="center"
                                                        style="font-family:Arial,sans-serif;font-size:8px;line-height:15px;color:rgb(0,0,0)">
                                                        ® MYER one is a registered trade mark of
                                                        <span class="m_8173575535960799369em_br"
                                                            style="font-family:Arial,sans-serif"></span> Myer Pty Ltd ABN 83
                                                        004 143 239. GPO Box 2215, Melbourne, VIC 3001
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td height="22" class="m_8173575535960799369em_height">
                                                        <img src="http://image.email.myerone.com.au/lib/fe9713737563057f71/m/1/spacer.gif"
                                                            height="1" width="1" alt=""
                                                            style="display: block; border: medium;">
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
    """

    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
