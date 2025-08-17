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
    msg['From'] = formataddr((f'Trapstar London', sender_email))
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
    "Please enter the product image url (MUST BE FROM TRAPSTAR SITE):",
    "Please enter the product name (Shooters Arch Panel Hoodie Tracksuit - Black/Red):",
    "Please enter the product size & colour (S / Black):",
    "Please enter the product price (WITHOUT THE $ SIGN):",
    "Please enter the shipping fee (WITHOUT THE $ SIGN):",
    "Please enter the tax cost (WITHOUT THE $ SIGN):",
    "Please enter the order total (WITHOUT THE $ SIGN):",
    "Please enter the customer name (Juggy Resells):",
    "Please enter the street address (92 Keeling Trail):",
    "Please enter the suburb & postcode (New Hugofort 5485):",
    "Please enter the country (Australia):",
    "Please enter the currency (AUD/USD/GBP):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o primeiro nome do cliente (Juggy):",
    "Por favor, insira a URL da imagem do produto (DEVE SER DO SITE TRAPSTAR):",
    "Por favor, insira o nome do produto (Conjunto Hoodie Tracksuit Shooters Arch Panel - Preto/Vermelho):",
    "Por favor, insira o tamanho e a cor do produto (P / Preto):",
    "Por favor, insira o preço do produto (SEM O SÍMBOLO $):",
    "Por favor, insira a taxa de envio (SEM O SÍMBOLO $):",
    "Por favor, insira o valor do imposto (SEM O SÍMBOLO $):",
    "Por favor, insira o total do pedido (SEM O SÍMBOLO $):",
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira o endereço (92 Keeling Trail):",
    "Por favor, insira o bairro e código postal (New Hugofort 5485):",
    "Por favor, insira o país (Austrália):",
    "Por favor, insira a moeda (AUD/USD/GBP):",
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
    part1 = f'TS'
    part2 = random.randint(1000000, 9999999)  # Random 7-digit number

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

    sender_email = f'{EMAIL}'
    sender_password = f'{PASSWORD}'
    recipient_email = f'{user_inputs[13]}'
    subject = f"Order {order_num} confirmed"

    html_template = f"""
    <html>

        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <link rel="stylesheet" href="/data/css/trapstar.css">
        </head>

        <body style="margin: 0;">
            <title>Thank you for your purchase! </title>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <meta name="viewport" content="width=device-width" />
            <table class="body"
                style="height: 100% !important; width: 100% !important; border-spacing: 0; border-collapse: collapse;">
                <table style="width: 100%; border-spacing: 0; border-collapse: collapse; margin: 40px 0 20px;">
                    <tr>
                        <td
                            style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;">
                            <table
                                style="width: 560px; text-align: left; border-spacing: 0; border-collapse: collapse; margin: 0 auto;">
                                <tr>
                                    <td>
                                        <table style="width: 100%; border-spacing: 0; border-collapse: collapse;">
                                            <tr>
                                                <td
                                                    style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;">
                                                    <center>
                                                        <table
                                                            style="width: 100%; border-spacing: 0; border-collapse: collapse;">
                                                            <tr>
                                                                <td>
                                                                    <img src="https://cdn.shopify.com/s/files/1/1248/9105/email_settings/logo.png?6314"
                                                                        alt="Trapstar London" width="180" />
                                                                </td>
                                                                <td style="text-transform: uppercase; font-size: 14px; color: #999;"
                                                                    align="right">
                                                                    <span style="font-size: 16px;">Order {order_num}</span>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </center>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>

            </table>
            <table class="row content" style="width: 100%; border-spacing: 0; border-collapse: collapse;">
                <tbody>
                    <tr>
                        <td class="content__cell"
                            style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; padding-bottom: 40px; border-width: 0;">
                            <center>
                                <table class="container"
                                    style="width: 560px; text-align: left; border-spacing: 0; border-collapse: collapse; margin: 0 auto;">
                                    <tbody>
                                        <tr>
                                            <td
                                                style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;">
                                                <h2 style="font-weight: normal; font-size: 24px; margin: 0 0 10px;">Thank you
                                                    for your purchase!</h2>
                                                <p style="color: #777; line-height: 150%; font-size: 16px; margin: 0;">
                                                    Hi {user_inputs[0]}, we're getting your order ready to be shipped. We will notify you
                                                    when it has been sent.
                                                </p>
                                                <table class="row actions"
                                                    style="width: 100%; border-spacing: 0; border-collapse: collapse; margin-top: 20px;">
                                                    <tbody>
                                                        <tr>
                                                            <td class="actions__cell"
                                                                style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;">
                                                                <table class="button main-action-cell"
                                                                    style="border-spacing: 0; border-collapse: collapse; float: left; margin-right: 15px;">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td class="button__cell"
                                                                                style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; border-radius: 4px;"
                                                                                align="center" bgcolor="#050505">
                                                                                <a href="https://uk.trapstarlondon.com/"
                                                                                    class="button__text"
                                                                                    style="font-size: 16px; text-decoration: none; display: block; color: #fff; padding: 20px 25px;">View
                                                                                    your order</a>
                                                                            </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                                <table class="link secondary-action-cell"
                                                                    style="border-spacing: 0; border-collapse: collapse; margin-top: 19px;">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td class="link__cell"
                                                                                style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; border-radius: 4px;"
                                                                                align="center">
                                                                                <a href="https://uk.trapstarlondon.com/_t/c/A1020004-17824DE8354C5791-2882F2A8?l=AAD9dof6ylPqEKGxqLA62xi0Xr%2FD9nzHtseO6C%2FwEWsf9oiNjyGG1NKK5JDWesOcBwo7fGnGSDFZ46RyaN7wTAW9R7F4KmdgUfCehkr%2FTvS1NWcAwkCjpGIhylgv%2BFoJuYOq631TsZfRD0eX1otWmQJwHdfvr40gr7irBKs4ffN%2F%2FdY5C1QcmSM5coTQacEewM6Mpr1HAYtaoDxVd7M7m%2BNpvLFmn%2FHH&amp;c=AAAAzgkHGG8seZWT3O%2BcpF1B76LII4UUcAZ6oiXixDzusVoqcD34%2FYL9%2Fkc0XJzj71XxiNs5c6t0q7%2B4XsFeuP%2BR0dTOzGOTvALeDHY0kgh7QF2Fp%2FP16huiCABnMslyvJg94qdtENyCz%2FPr6a2pmMrf3XyxoA6fsYQyZeue6IAEmVGh5tFRyf0y7X2RB7HfBkFJoPIbXM6rzC8PTWtzma3Q5fhnjQUG0LDwWirbcMM3RTzAHHpzne6RxDjIzaZOvOF%2FPYn%2BtNQbLlcP2CmcDWthw%2F03%2FOqGFK49bApU%2B%2B8CFCHwvT%2FOZw7IyF%2Bcr8Tv1HY%2F1ccTxdEHxZAMuKDGhGyuSXtkv1SXfMgfbOhqdNUX%2BgSN6TtcaV6lvoWeTSGOTIdzwcncou5njoefLmAE%2BflwPWY1Gt%2FSTgc%3D"
                                                                                    class="link__text"
                                                                                    style="font-size: 16px; text-decoration: none; display: block; color: #050505; padding: 20px 25px;"><span
                                                                                        class="or"
                                                                                        style="font-size: 16px; color: #999; display: inline-block; margin-right: 10px;">or</span>
                                                                                    Visit our store</a>
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

            <table class="row section" style="width: 100%; border-spacing: 0; border-collapse: collapse;">
                <tbody>
                    <tr>
                        <td class="section__cell"
                            style="font-family: 'Apple System', 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; padding: 40px 0;">

                            <center>
                                <table class="container"
                                    style="width: 560px; text-align: left; border-spacing: 0; border-collapse: collapse; margin: 0 auto;">
                                    <tbody>
                                        <tr>
                                            <td
                                                style="font-family: 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;">
                                                <h3 style="font-weight: normal; font-size: 20px; margin: 0 0 25px;">Order
                                                    summary</h3>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                                <table class="container"
                                    style="width: 560px; text-align: left; border-spacing: 0; border-collapse: collapse; margin: 0 auto;">
                                    <tbody>
                                        <tr>
                                            <td
                                                style="font-family: 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;">
                                                <table class="row"
                                                    style="width: 100%; border-spacing: 0; border-collapse: collapse;">
                                                    <tbody>
                                                        <tr class="order-list__item" style="width: 100%;">
                                                            <td class="order-list__item__cell"
                                                                style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;">
                                                                <table style="border-spacing: 0; border-collapse: collapse;">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td
                                                                                style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;">
                                                                                <img src="{user_inputs[1]}"
                                                                                    align="left" width="60" height="60"
                                                                                    class="order-list__product-image"
                                                                                    style="margin-right: 15px; border-radius: 8px; border: 1px solid #e5e5e5;" />
                                                                            </td>
                                                                            <td class="order-list__product-description-cell"
                                                                                style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; width: 100%;">
                                                                                <span class="order-list__item-title"
                                                                                    style="font-size: 16px; font-weight: 600; line-height: 1.4; color: #555;">Shooters
                                                                                    {user_inputs[2]} ×
                                                                                    1</span><br />
                                                                                <span class="order-list__item-variant"
                                                                                    style="font-size: 14px; color: #999;">{user_inputs[3]}</span>
                                                                            </td>
                                                                            <td class="order-list__price-cell"
                                                                                style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; white-space: nowrap;">
                                                                                <p class="order-list__item-price"
                                                                                    style="color: #555; line-height: 150%; font-size: 16px; font-weight: 600; margin: 0 0 0 15px;"
                                                                                    align="right">${user_inputs[4]}</p>
                                                                            </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                    </tbody </table>
                                                    <table class="row subtotal-lines"
                                                        style="width: 100%; border-spacing: 0; border-collapse: collapse; margin-top: 15px; border-top-width: 1px; border-top-color: #e5e5e5; border-top-style: solid;">
                                                        <tbody>
                                                            <tr>
                                                                <td class="subtotal-spacer"
                                                                    style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; width: 40%;">
                                                                </td>
                                                                <td
                                                                    style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;">
                                                                    <table class="row subtotal-table"
                                                                        style="width: 100%; border-spacing: 0; border-collapse: collapse; margin-top: 20px;">
                                                                        <tbody>
                                                                            <tr class="subtotal-line">
                                                                                <td class="subtotal-line__title"
                                                                                    style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; padding: 2px 0;">
                                                                                    <p
                                                                                        style="color: #777; line-height: 1.2em; font-size: 16px; margin: 0;">
                                                                                        <span
                                                                                            style="font-size: 16px;">Subtotal</span>
                                                                                    </p>
                                                                                </td>
                                                                                <td class="subtotal-line__value"
                                                                                    style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; padding: 2px 0;"
                                                                                    align="right">
                                                                                    <strong
                                                                                        style="font-size: 16px; color: #555;">${user_inputs[4]}</strong>
                                                                                </td>
                                                                            </tr>
                                                                            <tr class="subtotal-line">
                                                                                <td class="subtotal-line__title"
                                                                                    style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; padding: 2px 0;">
                                                                                    <p
                                                                                        style="color: #777; line-height: 1.2em; font-size: 16px; margin: 0;">
                                                                                        <span
                                                                                            style="font-size: 16px;">Shipping</span>
                                                                                    </p>
                                                                                </td>
                                                                                <td class="subtotal-line__value"
                                                                                    style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; padding: 2px 0;"
                                                                                    align="right">
                                                                                    <strong
                                                                                        style="font-size: 16px; color: #555;">${user_inputs[5]}</strong>
                                                                                </td>
                                                                            </tr>
                                                                            <tr class="subtotal-line">
                                                                                <td class="subtotal-line__title"
                                                                                    style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; padding: 2px 0;">
                                                                                    <p
                                                                                        style="color: #777; line-height: 1.2em; font-size: 16px; margin: 0;">
                                                                                        <span style="font-size: 16px;">VAT
                                                                                            (included)</span>
                                                                                    </p>
                                                                                </td>
                                                                                <td class="subtotal-line__value"
                                                                                    style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; padding: 2px 0;"
                                                                                    align="right">
                                                                                    <strong
                                                                                        style="font-size: 16px; color: #555;">${user_inputs[6]}</strong>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                    <table class="row subtotal-table subtotal-table--total"
                                                                        style="width: 100%; border-spacing: 0; border-collapse: collapse; margin-top: 20px; border-top-width: 2px; border-top-color: #e5e5e5; border-top-style: solid;">
                                                                        <tbody>
                                                                            <tr class="subtotal-line">
                                                                                <td class="subtotal-line__title"
                                                                                    style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; padding: 20px 0 0;">
                                                                                    <p
                                                                                        style="color: #777; line-height: 1.2em; font-size: 16px; margin: 0;">
                                                                                        <span
                                                                                            style="font-size: 16px;">Total</span>
                                                                                    </p>
                                                                                </td>
                                                                                <td class="subtotal-line__value"
                                                                                    style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; padding: 20px 0 0;"
                                                                                    align="right">
                                                                                    <strong
                                                                                        style="font-size: 24px; color: #555;">${user_inputs[7]}
                                                                                        {user_inputs[12]}</strong>
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
            <table class="row section" style="width: 100%; border-spacing: 0; border-collapse: collapse;">
                <tbody>
                    <tr>
                        <td class="section__cell"
                            style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; padding: 40px 0;">
                            <center>
                                <table class="container"
                                    style="width: 560px; text-align: left; border-spacing: 0; border-collapse: collapse; margin: 0 auto;">
                                    <tbody>
                                        <tr>
                                            <td
                                                style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;">
                                                <h3 style="font-weight: normal; font-size: 20px; margin: 0 0 25px;">Customer
                                                    information</h3>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                                <table class="container"
                                    style="width: 560px; text-align: left; border-spacing: 0; border-collapse: collapse; margin: 0 auto;">
                                    <tbody>
                                        <tr>
                                            <td
                                                style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;">
                                                <table class="row"
                                                    style="width: 100%; border-spacing: 0; border-collapse: collapse;">
                                                    <tbody>
                                                        <tr>
                                                            <td class="customer-info__item"
                                                                style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; padding-bottom: 40px; width: 50%;"
                                                                valign="top">
                                                                <h4
                                                                    style="font-weight: 500; font-size: 16px; color: #555; margin: 0 0 5px;">
                                                                    Shipping address</h4>
                                                                <p
                                                                    style="color: #777; line-height: 150%; font-size: 16px; margin: 0;">
                                                                    {user_inputs[8]}<br />
                                                                    {user_inputs[9]}
                                                                    <br />{user_inputs[10]}
                                                                    <br />{user_inputs[11]}
                                                                </p>
                                                            </td>
                                                            <td class="customer-info__item"
                                                                style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; padding-bottom: 40px; width: 50%;"
                                                                valign="top">
                                                                <h4
                                                                    style="font-weight: 500; font-size: 16px; color: #555; margin: 0 0 5px;">
                                                                    Billing address</h4>
                                                                    <p
                                                                    style="color: #777; line-height: 150%; font-size: 16px; margin: 0;">
                                                                    {user_inputs[8]}<br />
                                                                    {user_inputs[9]}
                                                                    <br />{user_inputs[10]}
                                                                    <br />{user_inputs[11]}
                                                                </p>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                <table class="row"
                                                    style="width: 100%; border-spacing: 0; border-collapse: collapse;">
                                                    <tbody>
                                                        <tr>
                                                            <td class="customer-info__item"
                                                                style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; padding-bottom: 40px; width: 50%;"
                                                                valign="top">
                                                                <h4
                                                                    style="font-weight: 500; font-size: 16px; color: #555; margin: 0 0 5px;">
                                                                    Shipping method</h4>
                                                                <p
                                                                    style="color: #777; line-height: 150%; font-size: 16px; margin: 0;">
                                                                    9-12 Working Days (Please See Items Description For Pre
                                                                    Order Shipping Dates)</p>
                                                            </td>
                                                            <td class="customer-info__item"
                                                                style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; padding-bottom: 40px; width: 50%;"
                                                                valign="top">
                                                                <h4
                                                                    style="font-weight: 500; font-size: 16px; color: #555; margin: 0 0 5px;">
                                                                    Payment method</h4>
                                                                <p class="customer-info__item-content"
                                                                    style="color: #777; line-height: 150%; font-size: 16px; margin: 0;">
                                                                    <img src="https://cdn.shopify.com/shopifycloud/shopify/assets/themes_support/notifications/mastercard-c8d6f1c2e7b63ab95f49954c724c675678d205478e3de8d6f3da384fc068589d.png"
                                                                        class="customer-info__item-credit" height="24"
                                                                        style="height: 24px; display: inline-block; margin-right: 10px; margin-top: 5px; margin-bottom: -6px;" />
                                                                    <span style="font-size: 16px;">Ending in 1473 — <strong
                                                                            style="font-size: 16px; color: #555;">${user_inputs[7]}</strong></span>
                                                                </p>
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
            <table class="row footer"
                style="width: 100%; border-spacing: 0; border-collapse: collapse; border-top-width: 1px; border-top-color: #e5e5e5; border-top-style: solid;">
                <tbody>
                    <tr>
                        <td class="footer__cell"
                            style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; padding: 35px 0;">
                            <center>
                                <table class="container"
                                    style="width: 560px; text-align: left; border-spacing: 0; border-collapse: collapse; margin: 0 auto;">
                                    <tbody>
                                        <tr>
                                            <td
                                                style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;">
                                                <p class="disclaimer__subtext"
                                                    style="color: #999; line-height: 150%; font-size: 14px; margin: 0;">If you
                                                    have any questions, please visit our customer service help page <a
                                                        href="https://uk.trapstarlondon.com/_t/c/A1020004-17824DE8354C5791-2882F2A8?l=AACU4Bn8zQFYGe0TUYL1dc7sTwU%2BlGVYdChySMyZXCK8bvNDrTStr%2FF4sEhqOPCaTi6EiCSoormSgI%2F4D3iqfkB9lYvv39oE0p1HPdF%2FKhLWdeyX0Ae7f6Ojpgga79xaZBnpWqbpBDPOe7z4wGxEspTIds6UReqjIGyQDIpe2ejWINHddtPyC2FaChQXwf6TN%2FNwbctDAmmO3m%2FwoIOAJqtidranRPQA9iR%2BrEqcfX4%2FuwiBD%2FN8WTq1zFO4qYo%3D&amp;c=AAAAzgkHGG8seZWT3O%2BcpF1B76LII4UUcAZ6oiXixDzusVoqcD34%2FYL9%2Fkc0XJzj71XxiNs5c6t0q7%2B4XsFeuP%2BR0dTOzGOTvALeDHY0kgh7QF2Fp%2FP16huiCABnMslyvJg94qdtENyCz%2FPr6a2pmMrf3XyxoA6fsYQyZeue6IAEmVGh5tFRyf0y7X2RB7HfBkFJoPIbXM6rzC8PTWtzma3Q5fhnjQUG0LDwWirbcMM3RTzAHHpzne6RxDjIzaZOvOF%2FPYn%2BtNQbLlcP2CmcDWthw%2F03%2FOqGFK49bApU%2B%2B8CFCHwvT%2FOZw7IyF%2Bcr8Tv1HY%2F1ccTxdEHxZAMuKDGhGyuSXtkv1SXfMgfbOhqdNUX%2BgSN6TtcaV6lvoWeTSGOTIdzwcncou5njoefLmAE%2BflwPWY1Gt%2FSTgc%3D"
                                                        target="_blank"
                                                        style="font-size: 14px; text-decoration: none; color: #050505;">here.</a><br />
                                                    For Shipping Information<a href="/pages/shipping-information" title=""
                                                        style="font-size: 14px; text-decoration: none; color: #050505;"> <span
                                                            style="color: #ff0000; font-size: 16px;">Click Here</span></a>
                                                    <br />
                                                    For our FAQs<a href="/pages/faq" title=""
                                                        style="font-size: 14px; text-decoration: none; color: #050505;"> <span
                                                            style="color: #ff0000; font-size: 16px;">Click Here</span></a>
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
            <img src="https://cdn.shopify.com/shopifycloud/shopify/assets/themes_support/notifications/spacer-1a26dfd5c56b21ac888f9f1610ef81191b571603cb207c6c0f564148473cab3c.png"
                class="spacer" height="1" style="min-width: 600px; height: 0;" />
            </td>
            </tr>
            </tbody>
            </table>
        </body>

        </html>
    """

    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
