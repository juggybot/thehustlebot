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
    msg['From'] = formataddr((f'Samsung', sender_email))
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
    "Please enter the order date (12 September 2024, 08:49 PM):",
    "Please enter the image url (jpg, jpeg, png):",
    "Please enter the product name (Galaxy S23 Ultra Enterprise Edition):",
    "Please enter the product price (WITHOUT THE $):",
    "Please enter the product ID (SM-S918BZKDEEB):",
    "Please enter the requested delivery (14/09/2024):",
    "Please enter the customer name (Juggy Resells):",
    "Please enter the street address (4016 Test Street):",
    "Please enter the suburb & postcode (East Jamesmouth, 4362):",
    "Please enter the country (Australia):",
    "Please enter the tax type (GST/VAT/SALES TAX):",
    "Please enter the tax amount (WITHOUT THE $):",
    "Please enter the order total (WITHOUT THE $):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira a data do pedido (12 de setembro de 2024, 20:49):",
    "Por favor, insira a URL da imagem (jpg, jpeg, png):",
    "Por favor, insira o nome do produto (Galaxy S23 Ultra Enterprise Edition):",
    "Por favor, insira o preço do produto (SEM O SÍMBOLO $):",
    "Por favor, insira o ID do produto (SM-S918BZKDEEB):",
    "Por favor, insira a data solicitada para entrega (14/09/2024):",
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira o endereço (4016 Test Street):",
    "Por favor, insira o bairro e código postal (East Jamesmouth, 4362):",
    "Por favor, insira o país (Austrália):",
    "Por favor, insira o tipo de imposto (GST/VAT/IMPOSTO SOBRE VENDAS):",
    "Por favor, insira o valor do imposto (SEM O SÍMBOLO $):",
    "Por favor, insira o total do pedido (SEM O SÍMBOLO $):",
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
    part1 = "SM"
    part2 = random.randint(100000, 999999)  # Random 6-digit number
    part3 = random.randint(100000, 999999)  # Random 6-digit number

    # Combine the parts into order number
    order_number = f"{part1}{part2}-{part3}"
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
    subject = f"Thanks for ordering from Samsung.com (Order #{order_num})"

    html_template = f"""
        <div bgcolor="#ffffff">
        <table width="100%" style="min-width:600px" border="0" align="center" cellpadding="0" cellspacing="0"
            bgcolor="#ffffff">
            <tbody>
                <tr>
                    <td>
                        <table style="padding:8px;border-bottom:solid 1px #e7e7e8;width:100%;margin-bottom:54px"
                            width="100%" align="center" cellpadding="0" cellspacing="0" bgcolor="#f8f8f8">
                            <tbody>
                                <tr>
                                    <td align="center">
                                        <font
                                            style="font-size:12px;font-family:Helvetica,Arial,sans-serif;color:#75787b;line-height:16px">
                                            If this message does not appear correctly, <a
                                                href="https://shop.samsung.com/uk/mypage/orders" target="_blank">click
                                                here</a>
                                        </font>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td align="center" valign="top">
                        <table style="max-width:600px;padding-bottom:15px" width="600" border="0" align="center"
                            cellpadding="0" cellspacing="0">
                            <tbody>
                                <tr>
                                    <td width="100%" border="0" align="left" cellpadding="0" cellspacing="0"
                                        style="padding:20px 0 5px 0">
                                        <font
                                            style="font-size:28px;font-weight:bold;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:1.43">
                                            ﻿<div>
                                                Thank you for your order
                                            </div>

                                        </font>
                                    </td>
                                    <td width="50%" border="0" align="right" cellpadding="0" cellspacing="0">
                                        <img style="vertical-align:middle;padding-top:5px"
                                            src="https://1000logos.net/wp-content/uploads/2017/06/Samsung-emblem.png"
                                            width="100" alt="Samsung" title="Samsung">
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table style="max-width:600px;padding-bottom:15px" width="600" border="0" align="center"
                            cellpadding="0" cellspacing="0">
                            <tbody>
                                <tr>
                                    <td width="100%" border="0" align="left" cellpadding="0" cellspacing="0"
                                        style="padding:20px 0 5px 0">
                                        <font
                                            style="font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:1.5">
                                            ﻿<div>
                                                <p>We&#39;ve received your order and are currently processing it.</p>
                                                <p>We&#39;ll send you another email once we&#39;ve dispatched the items in
                                                    your order, usually within a day or two. Please note that once we have
                                                    dispatched your order, you can no longer cancel or change it.</p>
                                                <p>Our courier partner will send you a text to confirm your delivery day. On
                                                    the delivery day itself you will receive another text confirming the
                                                    timeslot. This will include options to rearrange or provide further
                                                    delivery instructions.</p>In some circumstances, depending on the area
                                                you live or for very heavy items (of 135kg or more), our courier partner,
                                                Panther, will contact you within 24 hours via text message and email to
                                                arrange your delivery directly with you. If this applies to your order, it
                                                will show on the delivery option details in this email.
                                            </div>

                                        </font>
                                    </td>
                                </tr>
                            </tbody>
                        </table>


                        <table style="max-width:600px;padding-bottom:15px" width="600" border="0" align="center"
                            cellpadding="0" cellspacing="0">
                            <tbody>
                                <tr>
                                    <td width="100%" border="0" align="left" cellpadding="0" cellspacing="0"
                                        style="padding:20px 0 5px 0">
                                        <font
                                            style="font-size:16px;font-weight:bold;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:1.5">
                                            Your order</font>
                                    </td>
                                </tr>
                                <tr>
                                    <td width="100%" border="0" align="left" cellpadding="0" cellspacing="0"
                                        style="padding:20px 0 5px 0">
                                        <font
                                            style="font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:1.5">
                                            Order number: <a href="https://shop.samsung.com"
                                                target="_blank">#{order_num}</a></font>
                                    </td>
                                </tr>
                                <tr>
                                    <td width="100%" border="0" align="left" cellpadding="0" cellspacing="0"
                                        style="padding:0px 0 5px 0">
                                        <font
                                            style="font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:1.5">
                                            Order date: {user_inputs[0]}</font>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table style="max-width:600px" align="center" width="600">
                            <tbody>
                                <tr>
                                    <td width="100%" border="0" align="left" cellpadding="0" cellspacing="0"
                                        style="padding:20px 0 15px 0">
                                        <font
                                            style="font-size:16px;font-weight:bold;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:1.5">
                                            Order details</font>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table
                            style="border-top:1px solid #e7e7e8;border-left:1px solid #e7e7e8;border-right:1px solid #e7e7e8"
                            width="600" align="center" cellpadding="0" cellspacing="0">
                            <tbody>
                                <tr>
                                    <td colspan="3" valign="top" height="24" style="height:24px;border-collapse:collapse">
                                    </td>
                                </tr>
                                <tr>
                                    <td valign="top">
                                        <table style="vertical-align:top" width="150" border="0" cellpadding="0"
                                            cellspacing="0">
                                            <tbody>
                                                <tr>
                                                    <td>
                                                        <img src="{user_inputs[1]}"
                                                            width="140" height="100"
                                                            alt="{user_inputs[2]}"
                                                            title="Galaxy S23 Ultra Enterprise Edition">
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                    <td valign="top">
                                        <table style="vertical-align:top" width="450" cellpadding="0" cellspacing="0">
                                            <tbody>
                                                <tr>
                                                    <td valign="top">
                                                        <table style="padding-bottom:16px" width="320" border="0"
                                                            cellpadding="0" cellspacing="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td>
                                                                        <font
                                                                            style="font-size:18px;font-family:Helvetica,Arial,sans-serif;font-weight:bold;color:#000000;line-height:32px">
                                                                            1 x {user_inputs[2]}
                                                                        </font>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td>
                                                                        <font
                                                                            style="font-size:12px;font-family:Helvetica,Arial,sans-serif;color:#666666;line-height:16px">
                                                                            {user_inputs[4]}
                                                                        </font>
                                                                    </td>
                                                                </tr>
                                                                <tr style="padding-top:16px">
                                                                    <td width="70px">
                                                                        <font
                                                                            style="font-size:12px;font-family:Helvetica,Arial,sans-serif;color:#666666;line-height:16px">
                                                                            Delivery requested for: {user_inputs[5]}
                                                                        </font>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                    <td valign="top">
                                                        <table style="padding-right:20px" width="130" border="0"
                                                            cellpadding="0" cellspacing="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td align="right">
                                                                        <font
                                                                            style="font-size:18px;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:32px;letter-spacing:-0.2px">
                                                                            {user_inputs[13]}{user_inputs[3]} </font>
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
                                    <td height="24" style="height:24px;border-collapse:collapse"> </td>
                                </tr>
                            </tbody>
                        </table>
                        <table style="border:1px solid #e7e7e8;border-collapse:collapse" width="600" align="center"
                            cellpadding="0" cellspacing="0">
                            <tbody>
                                <tr>
                                    <td valign="top">
                                        <table style="padding-top:20px;padding-left:20px" width="470" border="0"
                                            cellpadding="0" cellspacing="0">
                                            <tbody>
                                                <tr>
                                                    <td>
                                                        <font
                                                            style="font-size:14px;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:4px">
                                                            Delivery Only</font>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                    <td valign="top">
                                        <table style="padding-top:20px;padding-right:20px;padding-bottom:20px" width="130"
                                            cellpadding="0" cellspacing="0">
                                            <tbody>
                                                <tr>
                                                    <td align="right">
                                                        <font
                                                            style="font-size:14px;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:4px">
                                                            FREE</font>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table width="600" align="center" cellpadding="0" cellspacing="0">
                            <tbody>
                                <tr>
                                    <td height="24" style="height:24px"> </td>
                                </tr>
                            </tbody>
                        </table>
                        <table style="max-width:600px" width="600" border="0" align="center" cellpadding="25"
                            cellspacing="0" bgcolor="#f8f8f8">
                            <tbody>
                                <tr>
                                    <td>
                                        <table>
                                            <tbody>
                                                <tr>
                                                    <td align="left" width="300" valign="top"
                                                        style="padding:10px;word-break:break-all;max-width:300px">
                                                        <font
                                                            style="font-size:14px;font-weight:bold;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:24px">
                                                            Delivery Address:
                                                        </font>
                                                        <p style="margin:3px 0">
                                                            <font
                                                                style="font-size:14px;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:24px">
                                                                {user_inputs[6]}<br>
                                                                {user_inputs[7]}<br>
                                                                {user_inputs[8]}<br>
                                                                {user_inputs[9]}<br>
                                                            </font>
                                                        </p>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="left" width="300" valign="top"
                                                        style="padding:10px;word-break:break-all;max-width:300px">
                                                        <font
                                                            style="font-size:14px;font-weight:bold;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:24px">
                                                            Billing address:
                                                        </font>
                                                        <p style="margin:3px 0">
                                                            <font
                                                                style="font-size:14px;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:24px">
                                                                {user_inputs[6]}<br>
                                                                {user_inputs[7]}<br>
                                                                {user_inputs[8]}<br>
                                                                {user_inputs[9]}<br>
                                                            </font>
                                                        </p>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="left" width="300" valign="top"
                                                        style="padding:10px;word-break:break-all;max-width:300px">
                                                        <font
                                                            style="font-size:14px;font-weight:bold;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:24px">
                                                            Payment type:
                                                        </font>
                                                        <p style="margin:3px 0">
                                                            <font
                                                                style="font-size:14px;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:24px">
                                                                Credit Card
                                                            </font>
                                                        </p>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <br>

                        <table style="max-width:600px;padding-bottom:48px" width="600" border="0" align="center"
                            cellpadding="0" cellspacing="0">
                            <tbody>
                                <tr>
                                    <td width="50%" valign="top" style="padding:10px">
                                        <table style="max-width:600px;padding-bottom:23px" width="100%" border="0"
                                            align="center" cellpadding="0" cellspacing="0">
                                            <tbody>
                                                <tr>
                                                    <td>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td><br>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="left" width="50%" valign="top" style="float:left">
                                                        <font
                                                            style="font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:1.5">
                                                            Delivery
                                                        </font>
                                                    </td>
                                                    <td width="50%" valign="top" style="float:right;text-align:right">
                                                        <font
                                                            style="font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:1.5">
                                                            FREE
                                                        </font>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="left" width="50%" valign="top" style="float:left">
                                                        <font
                                                            style="font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:32px">
                                                            Base Price
                                                        </font>
                                                    </td>
                                                    <td width="50%" valign="top" style="float:right;text-align:right">
                                                        <font
                                                            style="font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:32px">
                                                            {user_inputs[13]}{user_inputs[3]}
                                                        </font>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="left" width="50%" valign="top" style="float:left">
                                                        <font
                                                            style="font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:32px">
                                                            {user_inputs[10]}
                                                        </font>
                                                    </td>
                                                    <td width="50%" valign="top" style="float:right;text-align:right">
                                                        <font
                                                            style="font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:32px">
                                                            {user_inputs[13]}{user_inputs[11]}
                                                        </font>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="left" width="50%" valign="top" style="float:left">
                                                        <font
                                                            style="font-size:18px;font-weight:bold;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:1.5">
                                                            Total
                                                        </font>
                                                    </td>
                                                    <td width="50%" valign="top" style="float:right;text-align:right">
                                                        <font
                                                            style="font-size:18px;font-weight:bold;font-family:Helvetica,Arial,sans-serif;color:#000000;line-height:1.5">
                                                            {user_inputs[13]}{user_inputs[12]}
                                                        </font>
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
                    <td height="30"> </td>
                </tr>
                <tr>
                    <td align="center" valign="top">
                        <table style="max-width:600px;padding-bottom:15px" width="600" border="0" align="center"
                            cellpadding="0" cellspacing="0">
                            <tbody>
                                <tr>
                                    <td>
                                        <div>
                                            <p>
                                                <b>
                                                    Based on your experience, how likely are you to recommend purchasing
                                                    from the Samsung website to your friends or colleagues?
                                                </b>
                                            </p>

                                            <table style="max-width:600px" width="600" border="0" align="center"
                                                cellpadding="0" cellspacing="0">
                                                <tbody>
                                                    <tr colspan="11"
                                                        style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:1.5;color:#75787b">
                                                        <td align="left">
                                                            Not at all likely
                                                        </td>
                                                        <td align="right">
                                                            Extremely likely
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                            <table style="max-width:600px" width="600" border="0" align="center"
                                                cellpadding="0" cellspacing="0">
                                                <tbody>
                                                    <tr style="text-align:center">
                                                        <td width="9.09%" style="padding-bottom:24px">
                                                            <a style="font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#000000;text-decoration:none;background:a;outline:1px solid #0001;box-sizing:border-box;padding:20px 10px;border-radius:5px;line-height:0px;display:block;margin:5px"
                                                                href="https://samsungcustomerboard.fra1.qualtrics.com/jfe/form/SV_3QPN2XNQYPMjwYC?Q_PopulateResponse=%7B%22QID37%22%3A%220%22%7D&amp;Product_SKU=&amp;Order_ID=UK230912-92850302"
                                                                target="_blank">0</a>
                                                        </td>
                                                        <td width="9.09%" style="padding-bottom:24px">
                                                            <a style="font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#000000;text-decoration:none;background:a;outline:1px solid #0001;box-sizing:border-box;padding:20px 10px;border-radius:5px;line-height:0px;display:block;margin:5px"
                                                                href="https://samsungcustomerboard.fra1.qualtrics.com/jfe/form/SV_3QPN2XNQYPMjwYC?Q_PopulateResponse=%7B%22QID37%22%3A%221%22%7D&amp;Product_SKU=&amp;Order_ID=UK230912-92850302"
                                                                target="_blank">1</a>
                                                        </td>
                                                        <td width="9.09%" style="padding-bottom:24px">
                                                            <a style="font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#000000;text-decoration:none;background:a;outline:1px solid #0001;box-sizing:border-box;padding:20px 10px;border-radius:5px;line-height:0px;display:block;margin:5px"
                                                                href="https://samsungcustomerboard.fra1.qualtrics.com/jfe/form/SV_3QPN2XNQYPMjwYC?Q_PopulateResponse=%7B%22QID37%22%3A%222%22%7D&amp;Product_SKU=&amp;Order_ID=UK230912-92850302"
                                                                target="_blank">2</a>
                                                        </td>
                                                        <td width="9.09%" style="padding-bottom:24px">
                                                            <a style="font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#000000;text-decoration:none;background:a;outline:1px solid #0001;box-sizing:border-box;padding:20px 10px;border-radius:5px;line-height:0px;display:block;margin:5px"
                                                                href="https://samsungcustomerboard.fra1.qualtrics.com/jfe/form/SV_3QPN2XNQYPMjwYC?Q_PopulateResponse=%7B%22QID37%22%3A%223%22%7D&amp;Product_SKU=&amp;Order_ID=UK230912-92850302"
                                                                target="_blank">3</a>
                                                        </td>
                                                        <td width="9.09%" style="padding-bottom:24px">
                                                            <a style="font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#000000;text-decoration:none;background:a;outline:1px solid #0001;box-sizing:border-box;padding:20px 10px;border-radius:5px;line-height:0px;display:block;margin:5px"
                                                                href="https://samsungcustomerboard.fra1.qualtrics.com/jfe/form/SV_3QPN2XNQYPMjwYC?Q_PopulateResponse=%7B%22QID37%22%3A%224%22%7D&amp;Product_SKU=&amp;Order_ID=UK230912-92850302"
                                                                target="_blank">4</a>
                                                        </td>
                                                        <td width="9.09%" style="padding-bottom:24px">
                                                            <a style="font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#000000;text-decoration:none;background:a;outline:1px solid #0001;box-sizing:border-box;padding:20px 10px;border-radius:5px;line-height:0px;display:block;margin:5px"
                                                                href="https://samsungcustomerboard.fra1.qualtrics.com/jfe/form/SV_3QPN2XNQYPMjwYC?Q_PopulateResponse=%7B%22QID37%22%3A%225%22%7D&amp;Product_SKU=&amp;Order_ID=UK230912-92850302"
                                                                target="_blank">5</a>
                                                        </td>
                                                        <td width="9.09%" style="padding-bottom:24px">
                                                            <a style="font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#000000;text-decoration:none;background:a;outline:1px solid #0001;box-sizing:border-box;padding:20px 10px;border-radius:5px;line-height:0px;display:block;margin:5px"
                                                                href="https://samsungcustomerboard.fra1.qualtrics.com/jfe/form/SV_3QPN2XNQYPMjwYC?Q_PopulateResponse=%7B%22QID37%22%3A%226%22%7D&amp;Product_SKU=&amp;Order_ID=UK230912-92850302"
                                                                target="_blank">6</a>
                                                        </td>
                                                        <td width="9.09%" style="padding-bottom:24px">
                                                            <a style="font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#000000;text-decoration:none;background:a;outline:1px solid #0001;box-sizing:border-box;padding:20px 10px;border-radius:5px;line-height:0px;display:block;margin:5px"
                                                                href="https://samsungcustomerboard.fra1.qualtrics.com/jfe/form/SV_3QPN2XNQYPMjwYC?Q_PopulateResponse=%7B%22QID37%22%3A%227%22%7D&amp;Product_SKU=&amp;Order_ID=UK230912-92850302"
                                                                target="_blank">7</a>
                                                        </td>
                                                        <td width="9.09%" style="padding-bottom:24px">
                                                            <a style="font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#000000;text-decoration:none;background:a;outline:1px solid #0001;box-sizing:border-box;padding:20px 10px;border-radius:5px;line-height:0px;display:block;margin:5px"
                                                                href="https://samsungcustomerboard.fra1.qualtrics.com/jfe/form/SV_3QPN2XNQYPMjwYC?Q_PopulateResponse=%7B%22QID37%22%3A%228%22%7D&amp;Product_SKU=&amp;Order_ID=UK230912-92850302"
                                                                target="_blank">8</a>
                                                        </td>
                                                        <td width="9.09%" style="padding-bottom:24px">
                                                            <a style="font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#000000;text-decoration:none;background:a;outline:1px solid #0001;box-sizing:border-box;padding:20px 10px;border-radius:5px;line-height:0px;display:block;margin:5px"
                                                                href="https://samsungcustomerboard.fra1.qualtrics.com/jfe/form/SV_3QPN2XNQYPMjwYC?Q_PopulateResponse=%7B%22QID37%22%3A%229%22%7D&amp;Product_SKU=&amp;Order_ID=UK230912-92850302"
                                                                target="_blank">9</a>
                                                        </td>
                                                        <td width="9.09%" style="padding-bottom:24px">
                                                            <a style="font-size:16px;font-family:Helvetica,Arial,sans-serif;color:#000000;text-decoration:none;background:a;outline:1px solid #0001;box-sizing:border-box;padding:20px 10px;border-radius:5px;line-height:0px;display:block;margin:5px"
                                                                href="https://samsungcustomerboard.fra1.qualtrics.com/jfe/form/SV_3QPN2XNQYPMjwYC?Q_PopulateResponse=%7B%22QID37%22%3A%2210%22%7D&amp;Product_SKU=&amp;Order_ID=UK230912-92850302"
                                                                target="_blank">10</a>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                            <p>
                                                Please visit <a href="https://shop.samsung.com/uk/mypage/orders"
                                                    target="_blank">Order Look Up</a> to track or change your order (before
                                                order has been
                                                dispatched).
                                            </p>


                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td align="center" valign="top">
                        <table style="max-width:600px;padding-bottom:15px" width="600" border="0" align="center"
                            cellpadding="0" cellspacing="0">
                            <tbody>
                                <tr>
                                    <td>﻿<div>
                                        </div>

                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td align="center" valign="top">
                        <table style="max-width:600px;padding-bottom:15px" width="600" border="0" align="center"
                            cellpadding="0" cellspacing="0">
                            <tbody>
                                <tr>
                                    <td>﻿<div>
                                            <p> </p>
                                            <p style="font-size:18px"><b>Thank you for shopping at Samsung.com</b></p>
                                            <p>For help and support, please refer to our <a
                                                    href="https://www.samsung.com/uk/shop-faq/" target="_blank">Shop
                                                    FAQs</a>.</p>
                                            <p>If you can&#39;t find an answer to your question, you can contact <a
                                                    href="https://www.samsung.com/uk/support/contact/#shop-support"
                                                    target="_blank">Customer Support</a>.</p>
                                            <p> </p>
                                            <p></p>
                                            <p style="font-size:12px">This inbox is not attended so please don&#39;t reply
                                                to this email. You will receive these no matter what your marketing
                                                communication preferences are.</p>
                                            <p></p>
                                            <p></p>
                                        </div>

                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td valign="top">
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
