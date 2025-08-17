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
    msg['From'] = formataddr((f'Denim Tears', sender_email))
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
    "Please enter the delivery date (10/10/2025):",
    "Please enter the image url (.jpg, .png, .jpeg):",
    "Please enter the item name (Denim Tears x Nike Air Force 1):",
    "Please enter the item size (10.5):",
    "Please enter the item price (WITHOUT THE $):",
    "Please enter the postage price (WITHOUT THE $):",
    "Please enter the tax amount (WITHOUT THE $):",
    "Please enter the order total (WITHOUT THE $):",
    "Please enter the customer name (Juggy Resells):",
    "Please enter the street address (1234 Street Name):",
    "Please enter the city (City Name):",
    "Please enter the postcode (12345):",
    "Please enter the country (US):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o primeiro nome do cliente (Juggy):",
    "Por favor, insira a data de entrega (10/10/2025):",
    "Por favor, insira a URL da imagem (.jpg, .png, .jpeg):",
    "Por favor, insira o nome do item (Denim Tears x Nike Air Force 1):",
    "Por favor, insira o tamanho do item (10.5):",
    "Por favor, insira o preço do item (SEM O $):",
    "Por favor, insira o valor do frete (SEM O $):",
    "Por favor, insira o valor do imposto (SEM O $):",
    "Por favor, insira o total do pedido (SEM O $):",
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira o endereço (1234 Nome da Rua):",
    "Por favor, insira a cidade (Nome da Cidade):",
    "Por favor, insira o código postal (12345):",
    "Por favor, insira o país (BR):",
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
    part1 = random.randint(100000, 999999)  # Random 6-digit number

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
    recipient_email = f'{user_inputs[15]}'
    subject = f"Order #{order_num} confirmed"

    html_template = f"""
            <!DOCTYPE html>
    <html lang="en">

    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>

    <body style="margin: 0; padding: 0; box-sizing: border-box;">
    <div></div>
    <div>
        <div class="gmail_quote">
        <div>
            <table style="border-spacing:0px;border-collapse:collapse;height:100%!important;width:100%!important">
            <tbody>
                <tr>
                <td
                    style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                    <table
                    style="width:100%;border-spacing:0px;border-collapse:collapse;margin:40px 0px 20px;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                    <tbody
                        style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                        <tr
                        style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                        <td
                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                            <center
                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                            <table
                                style="width:560px;text-align:left;border-spacing:0px;border-collapse:collapse;margin:0px auto;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                <tbody
                                style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                <tr
                                    style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                    <td
                                    style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                    <table
                                        style="width:100%;border-spacing:0px;border-collapse:collapse;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                        <tbody
                                        style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                        <tr
                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                            <td
                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                            <img
                                                src="https://cdn.shopify.com/s/files/1/0258/6102/9962/files/DT-Floral-Logo.png?5177"
                                                alt="Denim Tears" width="180"
                                                style="font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, Oxygen, Ubuntu, Cantarell, &quot;Fira Sans&quot;, &quot;Droid Sans&quot;, &quot;Helvetica Neue&quot;, sans-serif;">
                                            </td>
                                            <td
                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;text-transform:uppercase;font-size:14px;color:rgb(153,153,153)"
                                            align="right"> </td>
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
                    <table
                    style="width:100%;border-spacing:0px;border-collapse:collapse;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                    <tbody
                        style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                        <tr
                        style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                        <td
                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;padding-bottom:40px;border:0px">
                            <center
                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                            <table
                                style="width:560px;text-align:left;border-spacing:0px;border-collapse:collapse;margin:0px auto;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                <tbody
                                style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                <tr
                                    style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                    <td style="font-family:Helvetica">
                                    <p
                                        style="font-weight:normal;font-size:16px;margin:0px 0px 10px;font-family:Helvetica">
                                        Thank you for your order, {user_inputs[0]}</p><br>
                                    <p
                                        style="line-height:150%;font-size:16px;margin:0px;font-family:Helvetica;color:rgb(119,119,119)">
                                        Your order #{order_num} has been successfully received on {user_inputs[1]}. Once your package
                                        ships we will send you an email with tracking information. Updates cannot be made to
                                        your order once tracking has been generated.</p>
                                    <table
                                        style="width:100%;border-spacing:0px;border-collapse:collapse;margin-top:20px;font-family:Helvetica">
                                        <tbody style="font-family:Helvetica">
                                        <tr style="font-family:Helvetica">
                                            <td
                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;line-height:0em">
                                            </td>
                                        </tr>
                                        <tr style="font-family:Helvetica">
                                            <td
                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                            <table
                                                style="border-spacing:0px;border-collapse:collapse;float:left;margin-right:15px;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                                <tbody
                                                style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                                <tr
                                                    style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                                    <td style="font-family:Helvetica;border-radius:4px" align="center"
                                                    bgcolor="#000000">
                                                    <a href="https://smymr.mjt.lu/lnk/CAAABWBKcwgAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwXlZwT9grqMTkCxkbNjkAJusgAlFbo/1/n61m998az3IaCcWZPKTr3Q/aHR0cHM6Ly9kZW5pbXRlYXJzLmNvbSZxdW90Ow"
                                                        style="font-size:16px;text-decoration:none;display:block;padding:20px 25px;font-family:Helvetica;color:rgb(255,255,255)"
                                                        target="_blank">View your order</a>
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
                            </center>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    style="width:100%;border-spacing:0px;border-collapse:collapse;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                    <tbody
                        style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                        <tr
                        style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                        <td
                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;padding:40px 0px">
                            <center
                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                            <table
                                style="width:560px;text-align:left;border-spacing:0px;border-collapse:collapse;margin:0px auto;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                <tbody
                                style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                <tr
                                    style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                    <td style="width:50%;font-family:&quot;Helvetica Neue&quot;,sans-serif">
                                    <h3
                                        style="font-weight:normal;font-size:16px;margin:0px 0px 25px;font-family:Helvetica;color:rgb(119,119,119)">
                                        {user_inputs[1]}</h3>
                                    </td>
                                    <td style="width:50%;font-family:&quot;Helvetica Neue&quot;,sans-serif">
                                    <h3
                                        style="font-weight:normal;font-size:16px;margin:0px 0px 25px;font-family:Helvetica;text-align:end;color:rgb(119,119,119)">
                                        Order #{order_num}</h3>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                            <table
                                style="width:560px;text-align:left;border-spacing:0px;border-collapse:collapse;margin:0px auto;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                <tbody
                                style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                <tr
                                    style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                    <td
                                    style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                    <table
                                        style="width:100%;border-spacing:0px;border-collapse:collapse;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                        <tbody
                                        style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                        <tr
                                            style="width:100%;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                            <td
                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;padding-bottom:15px">
                                            <table
                                                style="border-spacing:0px;border-collapse:collapse;border-top-width:1px;border-top-style:solid;border-bottom-width:1px;border-bottom-style:solid;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;border-top-color:rgb(229,229,229);border-bottom-color:rgb(229,229,229)">
                                                <tbody
                                                style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                                <tr
                                                    style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                                    <td
                                                    style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                                    <img
                                                        style="margin-top: 24px; margin-bottom: 24px; margin-right: 15px; font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, Oxygen, Ubuntu, Cantarell, &quot;Fira Sans&quot;, &quot;Droid Sans&quot;, &quot;Helvetica Neue&quot;, sans-serif;"
                                                        src="{user_inputs[2]}" width="120" height="auto" align="left">
                                                    </td>
                                                    <td
                                                    style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;width:100%">
                                                    <span
                                                        style="font-size:16px;line-height:1.4;font-family:Helvetica;color:rgb(85,85,85)">{user_inputs[3]}</span>
                                                    <br>
                                                    <span
                                                        style="font-family:Helvetica;font-size:16px;color:rgb(153,153,153)">{user_inputs[4]}</span>
                                                    <br>
                                                    <span
                                                        style="font-size:16px;font-family:Helvetica;color:rgb(153,153,153)"><br>Qty:
                                                        1</span>
                                                    </td>
                                                    <td style="font-family:Helvetica;white-space:nowrap">
                                                    <p style="font-family:Helvetica;line-height:150%;font-size:16px;margin:0px 0px 0px 15px;color:rgb(85,85,85)"
                                                        align="right">{user_inputs[14]}{user_inputs[5]}</p>
                                                    </td>
                                                </tr>
                                                </tbody>
                                            </table>
                                            </td>
                                        </tr>

                                        <tr
                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                            <td
                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                            <table
                                                style="width:100%;border-spacing:0px;border-collapse:collapse;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                                <tbody
                                                style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                                <tr
                                                    style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">

                                                    <td
                                                    style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                                    <table
                                                        style="width:100%;border-spacing:0px;border-collapse:collapse;margin-top:20px;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                                        <tbody
                                                        style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                                        <tr
                                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                                            <td
                                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;padding:5px 0px">
                                                            <p
                                                                style="line-height:1.2em;font-size:16px;margin:0px;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;color:rgb(119,119,119)">
                                                                <span
                                                                style="font-size:16px;font-family:Helvetica">Subtotal</span>
                                                            </p>
                                                            </td>
                                                            <td
                                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;padding:5px 0px"
                                                            align="right">
                                                            <p
                                                                style="font-size:16px;font-family:Helvetica;color:rgb(85,85,85)">
                                                                {user_inputs[14]}{user_inputs[5]}</p>
                                                            </td>
                                                        </tr>
                                                        <tr
                                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                                            <td
                                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;padding:5px 0px">
                                                            <p
                                                                style="line-height:1.2em;font-size:16px;margin:0px;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;color:rgb(119,119,119)">
                                                                <span
                                                                style="font-size:16px;font-family:Helvetica">Shipping</span>
                                                            </p>
                                                            </td>
                                                            <td
                                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;padding:5px 0px"
                                                            align="right">
                                                            <p
                                                                style="font-size:16px;font-family:Helvetica;color:rgb(85,85,85)">
                                                                {user_inputs[14]}{user_inputs[6]}</p>
                                                            </td>
                                                        </tr>
                                                        <tr
                                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                                            <td
                                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;padding:5px 0px">
                                                            <p
                                                                style="line-height:1.2em;font-size:16px;margin:0px;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;color:rgb(119,119,119)">
                                                                <span
                                                                style="font-size:16px;font-family:Helvetica">Taxes</span>
                                                            </p>
                                                            </td>
                                                            <td
                                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;padding:5px 0px"
                                                            align="right">
                                                            <p
                                                                style="font-size:16px;font-family:Helvetica;color:rgb(85,85,85)">
                                                                {user_inputs[14]}{user_inputs[7]}</p>
                                                            </td>
                                                        </tr>
                                                        <tr
                                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                                            <td
                                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;padding:5px 0px">
                                                            <p
                                                                style="line-height:1.2em;font-size:16px;margin:0px;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;color:rgb(119,119,119)">
                                                                <span
                                                                style="font-size:16px;font-family:Helvetica"><br>Total</span>
                                                            </p>
                                                            </td>
                                                            <td
                                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;padding:5px 0px"
                                                            align="right">
                                                            <p
                                                                style="font-size:16px;font-family:Helvetica;color:rgb(85,85,85)">
                                                                <br>{user_inputs[14]}{user_inputs[8]}</p>
                                                            </td>
                                                        </tr>
                                                        </tbody>
                                                    </table>

                                                    <table
                                                        style="width:100%;border-spacing:0px;border-collapse:collapse;margin-top:20px;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                                        <tbody
                                                        style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                                        <tr
                                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                                            <td
                                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;border-bottom-width:1px;border-bottom-style:solid;height:1px;padding:0px;border-bottom-color:rgb(229,229,229)"
                                                            colspan="2"> </td>
                                                        </tr>
                                                        <tr
                                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                                            <td
                                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;height:10px"
                                                            colspan="2"> </td>
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
                            </center>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    style="width:100%;border-spacing:0px;border-collapse:collapse;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                    <tbody
                        style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                        <tr
                        style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                        <td
                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;padding:40px 0px">
                            <center
                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                            <table
                                style="width:560px;text-align:left;border-spacing:0px;border-collapse:collapse;margin:0px auto;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                <tbody
                                style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                <tr
                                    style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                    <td style="font-family:Helvetica">
                                    <h3
                                        style="font-weight:normal;font-size:20px;margin:0px 0px 25px;font-family:Helvetica">
                                        Customer information</h3>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                            <table
                                style="width:560px;text-align:left;border-spacing:0px;border-collapse:collapse;margin:0px auto;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                <tbody
                                style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                <tr
                                    style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                    <td
                                    style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                    <table
                                        style="width:100%;border-spacing:0px;border-collapse:collapse;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                        <tbody
                                        style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                        <tr
                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                            <td style="font-family:Helvetica;padding-bottom:40px;width:50%" valign="top">
                                            <h4
                                                style="font-weight:500;font-size:16px;margin:0px 0px 5px;font-family:Helvetica;color:rgb(85,85,85)">
                                                Shipping address</h4>
                                            <p
                                                style="line-height:150%;font-size:16px;margin:0px;font-family:Helvetica;color:rgb(119,119,119)">
                                                {user_inputs[9]}
                                                <br>{user_inputs[10]}
                                                <br>{user_inputs[11]}
                                                <br>{user_inputs[12]}
                                                <br>{user_inputs[13]}
                                            </p>
                                            </td>
                                            <td style="font-family:Helvetica;padding-bottom:40px;width:50%" valign="top">
                                            <h4
                                                style="font-weight:500;font-size:16px;margin:0px 0px 5px;font-family:Helvetica;color:rgb(85,85,85)">
                                                Billing address</h4>
                                            <p
                                                style="line-height:150%;font-size:16px;margin:0px;font-family:Helvetica;color:rgb(119,119,119)">
                                                {user_inputs[9]}
                                                <br>{user_inputs[10]}
                                                <br>{user_inputs[11]}
                                                <br>{user_inputs[12]}
                                                <br>{user_inputs[13]}
                                            </p>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                    <table
                                        style="width:100%;border-spacing:0px;border-collapse:collapse;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                        <tbody
                                        style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                        <tr
                                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                            <td style="font-family:Helvetica;padding-bottom:40px;width:50%" valign="top">
                                            <h4
                                                style="font-weight:500;font-size:16px;margin:0px 0px 5px;font-family:Helvetica;color:rgb(85,85,85)">
                                                Shipping method</h4>
                                            <p
                                                style="line-height:150%;font-size:16px;margin:0px;font-family:Helvetica;color:rgb(119,119,119)">
                                                Standard</p>
                                            </td>
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
                    <table
                    style="width:100%;border-spacing:0px;border-collapse:collapse;border-top-width:1px;border-top-style:solid;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;border-top-color:rgb(229,229,229)">
                    <tbody
                        style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                        <tr
                        style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                        <td
                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif;padding:35px 0px">
                            <center
                            style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                            <table
                                style="width:560px;text-align:left;border-spacing:0px;border-collapse:collapse;margin:0px auto;font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                <tbody
                                style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                <tr
                                    style="font-family:-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Roboto,Oxygen,Ubuntu,Cantarell,&quot;Fira Sans&quot;,&quot;Droid Sans&quot;,&quot;Helvetica Neue&quot;,sans-serif">
                                    <td style="font-family:Helvetica">
                                    <p
                                        style="line-height:150%;font-size:14px;margin:0px;font-family:Helvetica;color:rgb(153,153,153)">
                                        If you have any questions, reply to this email or contact us at
                                        <a href="mailto:orders@denimtears.com"
                                        style="font-size:14px;text-decoration:none;font-family:Helvetica;color:rgb(0,0,0)"
                                        target="_blank">orders@denimtears.com</a>
                                    </p>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                            </center>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <img
                    style="min-width: 600px; height: 0px; font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, Oxygen, Ubuntu, Cantarell, &quot;Fira Sans&quot;, &quot;Droid Sans&quot;, &quot;Helvetica Neue&quot;, sans-serif;"
                    src="https://cdn.shopify.com/shopifycloud/shopify/assets/themes_support/notifications/spacer-1a26dfd5c56b21ac888f9f1610ef81191b571603cb207c6c0f564148473cab3c.png"
                    height="1">
                </td>
                </tr>
            </tbody>
            </table>
        </div>
        <br><img
            src="https://smymr.mjt.lu/oo/CAAABWBKcwgAAAAAAAAAAd_zRUcAAYCs4WsAAAAAACfwPQBmCwXlZwT9grqMTkCxkbNjkAJusgAlFbo/5d2fcccf/e.gif"
            height="1" width="1" alt="" border="0" style="height: 1px; width: 1px; border: 0px;">
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
