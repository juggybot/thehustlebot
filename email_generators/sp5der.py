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
    msg['From'] = formataddr((f'SP5DER', sender_email))
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
    "Please enter the image url (jpg, jpeg, png):",
    "Please enter the product name (Sp5der P*NK Hoodie Black):",
    "Please enter the product price (WITHOUT THE $):",
    "Please enter the product size (S/M/L):",
    "Please enter the shipping cost (WITHOUT THE $):",
    "Please enter the tax cost (WITHOUT THE $):",
    "Please enter the order total (WITHOUT THE $):",
    "Please enter the customer name (Juggy Resells):",
    "Please enter the street address (109 Welch Parkway):",
    "Please enter the suburb & postcode (New Alexandra, 7239):",
    "Please enter the country (Australia):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira a URL da imagem (jpg, jpeg, png):",
    "Por favor, insira o nome do produto (Sp5der P*NK Hoodie Preto):",
    "Por favor, insira o preço do produto (SEM O SÍMBOLO $):",
    "Por favor, insira o tamanho do produto (P/M/G):",
    "Por favor, insira o custo de envio (SEM O SÍMBOLO $):",
    "Por favor, insira o valor do imposto (SEM O SÍMBOLO $):",
    "Por favor, insira o total do pedido (SEM O SÍMBOLO $):",
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira o endereço (109 Welch Parkway):",
    "Por favor, insira o bairro e código postal (New Alexandra, 7239):",
    "Por favor, insira o país (Austrália):",
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
    part1 = "SP"
    part2 = random.randint(100000, 999999)  # Random 6-digit number

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
    recipient_email = f'{user_inputs[12]}'
    subject = f"Order #{order_num} confirmed"

    html_template = f"""
        <div style="margin: 0;">
        <table style="height: 100%!important; width: 100%!important; border-spacing: 0; border-collapse: collapse;">
            <tbody>
                <tr>
                    <td
                        style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                        <table style="width: 100%; border-spacing: 0; border-collapse: collapse; margin: 40px 0 20px;">
                            <tbody>
                                <tr>
                                    <td
                                        style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                        <center>
                                            <table
                                                style="width: 560px; text-align: left; border-spacing: 0; border-collapse: collapse; margin: 0 auto;">
                                                <tbody>
                                                    <tr>
                                                        <td
                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                            <table
                                                                style="width: 100%; border-spacing: 0; border-collapse: collapse;">
                                                                <tbody>
                                                                    <tr>
                                                                        <td
                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                            <img src="https://cdn.shopify.com/s/files/1/0153/0219/7334/files/logo.png?6246"
                                                                                alt="SP5DER" width="152">
                                                                        </td>
                                                                        <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; text-transform: uppercase; font-size: 14px; color: #999;"
                                                                            align="right">
                                                                            <span style="font-size: 16px;">Order
                                                                                #{order_num}</span>
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
                        <table style="width: 100%; border-spacing: 0; border-collapse: collapse;">
                            <tbody>
                                <tr>
                                    <td
                                        style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding-bottom: 40px; border-width: 0;">
                                        <center>
                                            <table
                                                style="width: 560px; text-align: left; border-spacing: 0; border-collapse: collapse; margin: 0 auto;">
                                                <tbody>
                                                    <tr>
                                                        <td
                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                            <h2
                                                                style="font-weight: normal; font-size: 24px; margin: 0 0 10px;">
                                                                Thank you for your purchase.</h2>
                                                            <p
                                                                style="color: #777; line-height: 150%; font-size: 16px; margin: 0;">
                                                                &nbsp;</p>
                                                            <br>
                                                            <center>
                                                                <span style="color: #ff0000;">
                                                                    <strong style="color: rgb(0, 240, 0);">Please note, due
                                                                        to increased demand, your order may take up to 2
                                                                        weeks to ship. We appreciate your patience.</strong>
                                                                </span>
                                                            </center>
                                                            <br>
                                                            <table
                                                                style="width: 100%; border-spacing: 0; border-collapse: collapse; margin-top: 20px;">
                                                                <tbody>
                                                                    <tr>
                                                                        <td
                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; line-height: 0em;">
                                                                            &nbsp;</td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td
                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                            <table
                                                                                style="border-spacing: 0; border-collapse: collapse; float: left; margin-right: 15px;">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; border-radius: 4px;"
                                                                                            align="center"
                                                                                            bgcolor="#000000">
                                                                                            <a href="https://kingspider.co/"
                                                                                                style="font-size: 16px; text-decoration: none; display: block; color: #fff; padding: 20px 25px;"
                                                                                                target="_blank"
                                                                                                rel="noopener">View your
                                                                                                order</a>
                                                                                        </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                            <table
                                                                                style="border-spacing: 0; border-collapse: collapse; margin-top: 19px;">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; border-radius: 4px;"
                                                                                            align="center">or
                                                                                            <a href="https://kingspider.co/_t/aB32dfIGjyw%3D%3D&amp;c=AAD6xKrKPic1Assd7g%2BhQLrfB%2BwHMb47xiT8oSsUBsenBe6RA3M1z6wVhDCToblOlbwEVAFzAs9%2BEW7acii%2BOjfkPPMZ76qXUXJkXM0SKXX5JNaFPT5IZ2Cm4nKgHzO7YxuX2ufI0HFbwJrRlUCghccOynzfMJ28kSbycNf6XpTDibY11eghDm2dMvYHm9oHnXfXXQwqwniQGlXphZiKeiIbPjrdlYgIdc9nxwnYt0oOPgpk2AvSMqKXh0MF%2BdGHX36MJCISkwfI4MaDnicjMadHVSeyAjvLIfz5BRkgZZelLpADZXt%2B7JE8mISy4wwdan78tQi4cBgmfrZppFqfJI%2FEdUH0IbaaO1%2Fzwxp%2FA7%2FBTHRNvyWEXfBES5cNT9KZOUDywUFTU3OMR1eBbxta6VZmvvzaZaexLwLpyYPrxgMCPubNmKUhURbGzv8Iu2gDIjIbQxkkoUR8bKiqLr7O6zKqTQ%3D%3D"
                                                                                                style="font-size: 16px; text-decoration: none; color: #000000;"
                                                                                                target="_blank"
                                                                                                rel="noopener">Visit our
                                                                                                store</a>
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
                        <table style="width: 100%; border-spacing: 0; border-collapse: collapse;">
                            <tbody>
                                <tr>
                                    <td
                                        style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 40px 0;">
                                        <center>
                                            <table
                                                style="width: 560px; text-align: left; border-spacing: 0; border-collapse: collapse; margin: 0 auto;">
                                                <tbody>
                                                    <tr>
                                                        <td
                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                            <h3
                                                                style="font-weight: normal; font-size: 20px; margin: 0 0 0px;">
                                                                Order summary</h3>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                            <table
                                                style="width: 560px; text-align: left; border-spacing: 0; border-collapse: collapse; margin: 0 auto;">
                                                <tbody>
                                                    <tr>
                                                        <td
                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                            <table
                                                                style="width: 100%; border-spacing: 0; border-collapse: collapse;">
                                                                <tbody>
                                                                    <tr style="width: 100%;">
                                                                        <td
                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding-bottom: 15px;">
                                                                            <table
                                                                                style="border-spacing: 0; border-collapse: collapse;">
                                                                                <tbody>
                                                                                    <tr>



                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                    </tr>

                                                                    <td
                                                                        style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding-top: 15px;">
                                                                        <table
                                                                            style="border-spacing: 0; border-collapse: collapse;">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td
                                                                                        style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                        <img style="margin-right: 15px; border-radius: 8px; border: 1px solid #e5e5e5;"
                                                                                            src="{user_inputs[0]}"
                                                                                            width="60" height="60"
                                                                                            align="left">
                                                                                    </td>
                                                                                    <td
                                                                                        style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; width: 100%;">
                                                                                        <span
                                                                                            style="font-size: 16px; font-weight: 600; line-height: 1.4; color: #555;">
                                                                                            {user_inputs[1]} × 1</span>
                                                                                        <br>
                                                                                        <span
                                                                                            style="font-size: 14px; color: #999;">{user_inputs[3]}</span>
                                                                                        <br>
                                                                                    </td>
                                                                                    <td
                                                                                        style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; white-space: nowrap;">
                                                                                        <p style="color: #555; line-height: 150%; font-size: 16px; font-weight: 600; margin: 0 0 0 15px;"
                                                                                            align="right">{user_inputs[11]}{user_inputs[2]}</p>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                            <table
                                                style="width: 100%; border-spacing: 0; border-collapse: collapse; margin-top: 15px; border-top-width: 1px; border-top-color: #e5e5e5; border-top-style: solid;">
                                                <tbody>
                                                    <tr>
                                                        <td
                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; width: 40%;">
                                                            &nbsp;</td>
                                                        <td
                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                            <table
                                                                style="width: 100%; border-spacing: 0; border-collapse: collapse; margin-top: 20px;">
                                                                <tbody>
                                                                    <tr>
                                                                        <td
                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 2px 0;">
                                                                            <p
                                                                                style="color: #777; line-height: 1.2em; font-size: 16px; margin: 0;">
                                                                                <span
                                                                                    style="font-size: 16px;">Subtotal</span>
                                                                            </p>
                                                                        </td>
                                                                        <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 2px 0;"
                                                                            align="right">
                                                                            <strong
                                                                                style="font-size: 16px; color: #555;">{user_inputs[11]}{user_inputs[2]}</strong>
                                                                        </td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td
                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 2px 0;">
                                                                            <p
                                                                                style="color: #777; line-height: 1.2em; font-size: 16px; margin: 0;">
                                                                                <span
                                                                                    style="font-size: 16px;">Shipping</span>
                                                                            </p>
                                                                        </td>
                                                                        <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 2px 0;"
                                                                            align="right">
                                                                            <strong
                                                                                style="font-size: 16px; color: #555;">{user_inputs[11]}{user_inputs[4]}</strong>
                                                                        </td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td
                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 2px 0;">
                                                                            <p
                                                                                style="color: #777; line-height: 1.2em; font-size: 16px; margin: 0;">
                                                                                <span style="font-size: 16px;">Taxes</span>
                                                                            </p>
                                                                        </td>
                                                                        <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 2px 0;"
                                                                            align="right">
                                                                            <strong
                                                                                style="font-size: 16px; color: #555;">{user_inputs[11]}{user_inputs[5]}</strong>
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                            <table
                                                                style="width: 100%; border-spacing: 0; border-collapse: collapse; margin-top: 20px; border-top-width: 2px; border-top-color: #e5e5e5; border-top-style: solid;">
                                                                <tbody>
                                                                    <tr>
                                                                        <td
                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 20px 0 0;">
                                                                            <p
                                                                                style="color: #777; line-height: 1.2em; font-size: 16px; margin: 0;">
                                                                                <span style="font-size: 16px;">Total</span>
                                                                            </p>
                                                                        </td>
                                                                        <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 20px 0 0;"
                                                                            align="right">
                                                                            <strong
                                                                                style="font-size: 24px; color: #555;">{user_inputs[11]}{user_inputs[6]}</strong>
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
        <table style="width: 100%; border-spacing: 0; border-collapse: collapse;">
            <tbody>
                <tr>
                    <td
                        style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 40px 0;">
                        <center>
                            <table
                                style="width: 560px; text-align: left; border-spacing: 0; border-collapse: collapse; margin: 0 auto;">
                                <tbody>
                                    <tr>
                                        <td
                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                            <h3 style="font-weight: normal; font-size: 20px; margin: 0 0 25px;">Customer
                                                information</h3>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <table
                                style="width: 560px; text-align: left; border-spacing: 0; border-collapse: collapse; margin: 0 auto;">
                                <tbody>
                                    <tr>
                                        <td
                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                            <table style="width: 100%; border-spacing: 0; border-collapse: collapse;">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding-bottom: 40px; width: 50%;"
                                                            valign="top">
                                                            <h4
                                                                style="font-weight: 500; font-size: 16px; color: #555; margin: 0 0 5px;">
                                                                Shipping address</h4>
                                                            <p
                                                                style="color: #777; line-height: 150%; font-size: 16px; margin: 0;">
                                                                {user_inputs[7]}

                                                                <br>
                                                                <a>{user_inputs[8]}</a>
                                                                <br>
                                                                <a>{user_inputs[9]}</a>
                                                                <br>
                                                                <a>{user_inputs[10]}</a>
                                                            </p>
                                                        </td>
                                                        <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding-bottom: 40px; width: 50%;"
                                                            valign="top">
                                                            <h4
                                                                style="font-weight: 500; font-size: 16px; color: #555; margin: 0 0 5px;">
                                                                Billing address</h4>
                                                                <p
                                                                style="color: #777; line-height: 150%; font-size: 16px; margin: 0;">
                                                                {user_inputs[7]}

                                                                <br>
                                                                <a>{user_inputs[8]}</a>
                                                                <br>
                                                                <a>{user_inputs[9]}</a>
                                                                <br>
                                                                <a>{user_inputs[10]}</a>
                                                            </p>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                            <table style="width: 100%; border-spacing: 0; border-collapse: collapse;">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding-bottom: 40px; width: 50%;"
                                                            valign="top">
                                                            <h4
                                                                style="font-weight: 500; font-size: 16px; color: #555; margin: 0 0 5px;">
                                                                Payment</h4>
                                                            <p
                                                                style="color: #777; line-height: 150%; font-size: 16px; margin: 0;">
                                                                <img style="height: 24px; display: inline-block; margin-right: 10px; margin-top: 5px;"
                                                                    src="https://cdn.shopify.com/shopifycloud/shopify/assets/themes_support/notifications/visa-e96781bbd9d5a604ec37ca3959c7200b62b58790536de883a9f29852191da219.png"
                                                                    alt="Visa" height="24">
                                                                <span style="font-size: 16px;">ending with 2631</span>
                                                                <br>
                                                            </p>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding-bottom: 40px; width: 50%;"
                                                            valign="top">
                                                            <h4
                                                                style="font-weight: 500; font-size: 16px; color: #555; margin: 0 0 5px;">
                                                                Shipping method</h4>
                                                            <p
                                                                style="color: #777; line-height: 150%; font-size: 16px; margin: 0;">
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
            style="width: 100%; border-spacing: 0; border-collapse: collapse; border-top-width: 1px; border-top-color: #e5e5e5; border-top-style: solid;">
            <tbody>
                <tr>
                    <td
                        style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 35px 0;">
                        <center>
                            <table
                                style="width: 560px; text-align: left; border-spacing: 0; border-collapse: collapse; margin: 0 auto;">
                                <tbody>
                                    <tr>
                                        <td
                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                            <p style="color: #999; line-height: 150%; font-size: 14px; margin: 0;">If you
                                                have any questions, reply to this email or contact us at
                                                <a href="mailto:help@kingspider.co"
                                                    style="font-size: 14px; text-decoration: none; color: #000000;"
                                                    target="_blank" rel="noopener">help@kingspider.co</a>
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
        <img style="min-width: 600px; height: 0;"
            src="https://cdn.shopify.com/shopifycloud/shopify/assets/themes_support/notifications/spacer-1a26dfd5c56b21ac888f9f1610ef81191b571603cb207c6c0f564148473cab3c.png"
            height="1">
        </td>
        </tr>
        </tbody>
        </table>
    </div>
    </blockquote>
    </div>
    </div>
    """

    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
