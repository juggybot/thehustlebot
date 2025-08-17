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
    msg['From'] = formataddr((f'Stanley 1913', sender_email))
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
    "Please enter the image url (MUST BE FROM STANLEY SITE):",
    "Please enter the item name (Deco Collection Quencher H2.0 FlowState™):",
    "Please enter the item colour (Black):",
    "Please enter the item price (WITHOUT THE $ SIGN):",
    "Please enter the shipping cost (WITHOUT THE $ SIGN):",
    "Please enter the tax cost (WITHOUT THE $ SIGN):",
    "Please enter the order total (WITHOUT THE $ SIGN):",
    "Please enter the street address (7361 Paige Court):",
    "Please enter the suburb & postcode (West Aaron, 4346):",
    "Please enter the country (Australia):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira a URL da imagem (DEVE SER DO SITE DA STANLEY):",
    "Por favor, insira o nome do item (Deco Collection Quencher H2.0 FlowState™):",
    "Por favor, insira a cor do item (Preto):",
    "Por favor, insira o preço do item (SEM O SÍMBOLO $):",
    "Por favor, insira o custo de envio (SEM O SÍMBOLO $):",
    "Por favor, insira o valor do imposto (SEM O SÍMBOLO $):",
    "Por favor, insira o total do pedido (SEM O SÍMBOLO $):",
    "Por favor, insira o endereço (7361 Paige Court):",
    "Por favor, insira o bairro e código postal (West Aaron, 4346):",
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
    # Generate random order number
    part1 = random.randint(100000, 999999)  # Random 8-digit number

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
    recipient_email = f'{user_inputs[12]}'
    subject = f"Order #{order_num}"

    html_template = f"""
        <div>
    <div>
        <div class="gmail_quote">
            <div dir="ltr">
                <div class="gmail_quote">
                    <div dir="auto">
                        <br>
                        <blockquote>
                            <div dir="ltr">
                                <table
                                    style="border-spacing: 0px; border-collapse: collapse; height: 100%!important; width: 100%!important;">
                                    <tbody>
                                        <tr>
                                            <td
                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                <table
                                                    style="width: 100%; border-spacing: 0px; border-collapse: collapse; margin: 40px 0px 20px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                    <tbody
                                                        style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                        <tr
                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                            <td
                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                <center
                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                    <table
                                                                        style="width: 560px; text-align: left; border-spacing: 0px; border-collapse: collapse; margin: 0px auto; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                        <tbody
                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                            <tr
                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                <td
                                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                    <table
                                                                                        style="width: 100%; border-spacing: 0px; border-collapse: collapse; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                        <tbody
                                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                            <tr
                                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                <td
                                                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                    <img style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;"
                                                                                                        src="https://cdn.shopify.com/s/files/1/0375/3269/6635/email_settings/logo-main.png?15511"
                                                                                                        alt="Stanley 1913"
                                                                                                        width="180">
                                                                                                </td>
                                                                                                <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; text-transform: uppercase; font-size: 14px; color: #999999;"
                                                                                                    align="right">
                                                                                                    <span
                                                                                                        style="font-size: 16px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">Order
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
                                                <table
                                                    style="width: 100%; border-spacing: 0px; border-collapse: collapse; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                    <tbody
                                                        style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                        <tr
                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                            <td
                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding-bottom: 40px; border-width: 0px;">
                                                                <center
                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                    <table
                                                                        style="width: 560px; text-align: left; border-spacing: 0px; border-collapse: collapse; margin: 0px auto; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                        <tbody
                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                            <tr
                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                <td
                                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                    <h2
                                                                                        style="font-weight: normal; font-size: 24px; margin: 0px 0px 10px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                        Thank you for your purchase!
                                                                                    </h2>
                                                                                    <p
                                                                                        style="line-height: 150%; font-size: 16px; margin: 0px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #777777;">
                                                                                        Hi {user_inputs[0]},
                                                                                        <br>
                                                                                    </p>
                                                                                    <p
                                                                                        style="line-height: 150%; font-size: 16px; margin: 15px 0px 0px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #777777;">
                                                                                        We’re so excited to get you your
                                                                                        order. You will receive an email
                                                                                        notification once a tracking
                                                                                        number is assigned to your
                                                                                        package.</p>
                                                                                    <br>
                                                                                    <p
                                                                                        style="line-height: 150%; font-size: 16px; margin: 0px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #777777;">
                                                                                        Please be advised that due to
                                                                                        high demand, order processing
                                                                                        time is currently extended and
                                                                                        your order is expected to ship
                                                                                        within 5 to 7 business days for
                                                                                        non-customized items or 10-15
                                                                                        business days for Stanley Create
                                                                                        customized items.</p>
                                                                                    <br>
                                                                                    <p
                                                                                        style="line-height: 150%; font-size: 16px; margin: 0px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #777777;">
                                                                                        We appreciate your patience.</p>
                                                                                    <table
                                                                                        style="width: 100%; border-spacing: 0px; border-collapse: collapse; margin-top: 20px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                        <tbody
                                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                            <tr
                                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                <td
                                                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; line-height: 0em;">
                                                                                                    &nbsp;</td>
                                                                                            </tr>
                                                                                            <tr
                                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                <td
                                                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                    <table
                                                                                                        style="border-spacing: 0px; border-collapse: collapse; float: left; margin-right: 15px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                        <tbody
                                                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                            <tr
                                                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                                <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; border-radius: 4px;"
                                                                                                                    align="center"
                                                                                                                    bgcolor="#333333">
                                                                                                                    <a href="https://stanley1913.com"
                                                                                                                        style="font-size: 16px; text-decoration: none; display: block; padding: 20px 25px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #ffffff;"
                                                                                                                        target="_blank"
                                                                                                                        rel="noopener">View
                                                                                                                        your
                                                                                                                        order</a>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                    <table
                                                                                                        style="border-spacing: 0px; border-collapse: collapse; margin-top: 19px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                        <tbody
                                                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                            <tr
                                                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                                <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; border-radius: 4px;"
                                                                                                                    align="center">
                                                                                                                    or
                                                                                                                    <a href="https://www.stanley1913.com/_t/c/A1030004-179F9BC513DA06F6-E5E62DC5?l=AACRr8Oku3b%2BzbFzaawsiOeV%2FF3hlmouvFjHdApPI1Oid0a7z0FeMkqFhXxgiiaR7Bvf50a5Dx3ROCXt8RCvEBPywsKkzlUKEcr04iwBYXWpm0zPCN0HY2OlBvn34I35YKiMMZdHLuAmjomDy7Wz5vLjjP5Z7flZZx0iGNsKVrsRqp%2F6AhGM0icIsllj1piWTowxYTN7emTxwPHd%2BlzvL3W4M0aoDg%3D%3D&amp;c=AAB20i3y9iEQGBFxCKjvejNbi3aFbIlE5BHLt9yqUPPrBtu39mwoiDQ1%2BbILjk60c7FPBNMUUJcqom%2FKsWYGEE9L3bAvySuKizVgckQR%2FpmTQC3VqrAlSB%2BpI4E1LOrH6E3FfbOyjFQWLuRGEkeQcDXiqoDNLMWTVP24wynWSCpXmoJusWVpFt46V%2B7lFjRiYsCmgmwsJxJM%2BJiTYPZtjuoHpOM%2FI4xyK429mZDlswyOZDyhZyEBiMJGZskcYgAX7KwzUYjQ8G2hacLfjwVu3GzM%2FeRurDe9NWtMcpmwFDERykZeUVSDwm57pCULiup3plXBGo6AdbLbRbKdvIirnLItIJ3kZsqfupO79gaBVYqntvitlcG1WKkCtczZZzMnwxcGaYyIfNKO5P6CxIM4fUtn6oL3%2Bcpkqu2uM8Qeq4txjzeI7aSpRQR7NND%2FWPU8K662mO02WiNNyLXGs82LoN4EV%2BPOpDc4Ng%3D%3D"
                                                                                                                        style="font-size: 16px; text-decoration: none; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #333333;"
                                                                                                                        target="_blank"
                                                                                                                        rel="noopener">Visit
                                                                                                                        our
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
                                                <table
                                                    style="width: 100%; border-spacing: 0px; border-collapse: collapse; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                    <tbody
                                                        style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                        <tr
                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                            <td
                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 40px 0px;">
                                                                <center
                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                    <table
                                                                        style="width: 560px; text-align: left; border-spacing: 0px; border-collapse: collapse; margin: 0px auto; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                        <tbody
                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                            <tr
                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                <td
                                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                    <h3
                                                                                        style="font-weight: normal; font-size: 20px; margin: 0px 0px 25px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                        Order summary</h3>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                    <table
                                                                        style="width: 560px; text-align: left; border-spacing: 0px; border-collapse: collapse; margin: 0px auto; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                        <tbody
                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                            <tr
                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                <td
                                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                    <table
                                                                                        style="width: 100%; border-spacing: 0px; border-collapse: collapse; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                        <tbody
                                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                            <tr
                                                                                                style="width: 100%; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                <td
                                                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                    <table
                                                                                                        style="border-spacing: 0px; border-collapse: collapse; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                        <tbody
                                                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                            <tr
                                                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                                <td
                                                                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                                    <img style="margin-right: 15px; border-radius: 8px; border: 1px solid #e5e5e5; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;"
                                                                                                                        src="{user_inputs[1]}?crop=center&height=104&v=1706653604&width=104"
                                                                                                                        width="60"
                                                                                                                        height="60"
                                                                                                                        align="left">
                                                                                                                </td>
                                                                                                                <td
                                                                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; width: 100%;">
                                                                                                                    <span
                                                                                                                        style="font-size: 16px; font-weight: 600; line-height: 1.4; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #555555;">{user_inputs[2]}
                                                                                                                        ×
                                                                                                                        1</span>
                                                                                                                    <br>
                                                                                                                    <span
                                                                                                                        style="font-size: 14px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #999999;">Color:
                                                                                                                        {user_inputs[3]}</span>
                                                                                                                    <br>
                                                                                                                </td>
                                                                                                                <td
                                                                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; white-space: nowrap;">
                                                                                                                    <p style="line-height: 150%; font-size: 16px; font-weight: 600; margin: 0px 0px 0px 15px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #555555;"
                                                                                                                        align="right">
                                                                                                                        {user_inputs[11]}{user_inputs[4]}
                                                                                                                    </p>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                    <table
                                                                                        style="width: 100%; border-spacing: 0px; border-collapse: collapse; margin-top: 15px; border-top-width: 1px; border-top-style: solid; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; border-top-color: #e5e5e5;">
                                                                                        <tbody
                                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                            <tr
                                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                <td
                                                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; width: 40%;">
                                                                                                    &nbsp;</td>
                                                                                                <td
                                                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                    <table
                                                                                                        style="width: 100%; border-spacing: 0px; border-collapse: collapse; margin-top: 20px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                        <tbody
                                                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                            <tr
                                                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                                <td
                                                                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 2px 0px;">
                                                                                                                    <p
                                                                                                                        style="line-height: 1.2em; font-size: 16px; margin: 0px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #777777;">
                                                                                                                        <span
                                                                                                                            style="font-size: 16px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">Subtotal</span>
                                                                                                                    </p>
                                                                                                                </td>
                                                                                                                <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 2px 0px;"
                                                                                                                    align="right">
                                                                                                                    <strong
                                                                                                                        style="font-size: 16px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #555555;">{user_inputs[11]}{user_inputs[4]}</strong>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                            <tr
                                                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                                <td
                                                                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 2px 0px;">
                                                                                                                    <p
                                                                                                                        style="line-height: 1.2em; font-size: 16px; margin: 0px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #777777;">
                                                                                                                        <span
                                                                                                                            style="font-size: 16px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">Shipping</span>
                                                                                                                    </p>
                                                                                                                </td>
                                                                                                                <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 2px 0px;"
                                                                                                                    align="right">
                                                                                                                    <strong
                                                                                                                        style="font-size: 16px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #555555;">{user_inputs[11]}{user_inputs[5]}</strong>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                            <tr
                                                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                                <td
                                                                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 2px 0px;">
                                                                                                                    <p
                                                                                                                        style="line-height: 1.2em; font-size: 16px; margin: 0px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #777777;">
                                                                                                                        <span
                                                                                                                            style="font-size: 16px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">Taxes</span>
                                                                                                                    </p>
                                                                                                                </td>
                                                                                                                <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 2px 0px;"
                                                                                                                    align="right">
                                                                                                                    <strong
                                                                                                                        style="font-size: 16px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #555555;">{user_inputs[11]}{user_inputs[6]}</strong>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                    <table
                                                                                                        style="width: 100%; border-spacing: 0px; border-collapse: collapse; margin-top: 20px; border-top-width: 2px; border-top-style: solid; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; border-top-color: #e5e5e5;">
                                                                                                        <tbody
                                                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                            <tr
                                                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                                <td
                                                                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 20px 0px 0px;">
                                                                                                                    <p
                                                                                                                        style="line-height: 1.2em; font-size: 16px; margin: 0px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #777777;">
                                                                                                                        <span
                                                                                                                            style="font-size: 16px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">Total</span>
                                                                                                                    </p>
                                                                                                                </td>
                                                                                                                <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 20px 0px 0px;"
                                                                                                                    align="right">
                                                                                                                    <strong
                                                                                                                        style="font-size: 24px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #555555;">{user_inputs[11]}{user_inputs[7]}</strong>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                    <table
                                                                                                        style="width: 100%; border-spacing: 0px; border-collapse: collapse; margin-top: 20px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                        <tbody
                                                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                            <tr
                                                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                                <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; border-bottom-width: 1px; border-bottom-style: solid; height: 1px; padding: 0px; border-bottom-color: #e5e5e5;"
                                                                                                                    colspan="2">
                                                                                                                    &nbsp;
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                            <tr
                                                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                                <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; height: 10px;"
                                                                                                                    colspan="2">
                                                                                                                    &nbsp;
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
                                                    style="width: 100%; border-spacing: 0px; border-collapse: collapse; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                    <tbody
                                                        style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                        <tr
                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                            <td
                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 40px 0px;">
                                                                <center
                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                    <table
                                                                        style="width: 560px; text-align: left; border-spacing: 0px; border-collapse: collapse; margin: 0px auto; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                        <tbody
                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                            <tr
                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                <td
                                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                    <h3
                                                                                        style="font-weight: normal; font-size: 20px; margin: 0px 0px 25px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                        Customer information</h3>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                    <table
                                                                        style="width: 560px; text-align: left; border-spacing: 0px; border-collapse: collapse; margin: 0px auto; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                        <tbody
                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                            <tr
                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                <td
                                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                    <table
                                                                                        style="width: 100%; border-spacing: 0px; border-collapse: collapse; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                        <tbody
                                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                            <tr
                                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding-bottom: 40px; width: 50%;"
                                                                                                    valign="top">
                                                                                                    <h4
                                                                                                        style="font-weight: 500; font-size: 16px; margin: 0px 0px 5px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #555555;">
                                                                                                        Shipping address
                                                                                                    </h4>
                                                                                                    <p
                                                                                                        style="line-height: 150%; font-size: 16px; margin: 0px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #777777;">
                                                                                                        {user_inputs[0]}
                                                                                                        <br>{user_inputs[8]}
                                                                                                        <br>{user_inputs[9]}
                                                                                                        <br>{user_inputs[10]}
                                                                                                    </p>
                                                                                                </td>
                                                                                                <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding-bottom: 40px; width: 50%;"
                                                                                                    valign="top">
                                                                                                    <h4
                                                                                                        style="font-weight: 500; font-size: 16px; margin: 0px 0px 5px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #555555;">
                                                                                                        Billing address
                                                                                                    </h4>
                                                                                                    <p
                                                                                                        style="line-height: 150%; font-size: 16px; margin: 0px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #777777;">
                                                                                                        {user_inputs[0]}
                                                                                                        <br>{user_inputs[8]}
                                                                                                        <br>{user_inputs[9]}
                                                                                                        <br>{user_inputs[10]}
                                                                                                    </p>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                    <table
                                                                                        style="width: 100%; border-spacing: 0px; border-collapse: collapse; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                        <tbody
                                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                            <tr
                                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                                <td style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding-bottom: 40px; width: 50%;"
                                                                                                    valign="top">
                                                                                                    <h4
                                                                                                        style="font-weight: 500; font-size: 16px; margin: 0px 0px 5px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #555555;">
                                                                                                        Shipping method
                                                                                                    </h4>
                                                                                                    <p
                                                                                                        style="line-height: 150%; font-size: 16px; margin: 0px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #777777;">
                                                                                                        UPS</p>
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
                                                    style="width: 100%; border-spacing: 0px; border-collapse: collapse; border-top-width: 1px; border-top-style: solid; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; border-top-color: #e5e5e5;">
                                                    <tbody
                                                        style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                        <tr
                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                            <td
                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; padding: 35px 0px;">
                                                                <center
                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                    <table
                                                                        style="width: 560px; text-align: left; border-spacing: 0px; border-collapse: collapse; margin: 0px auto; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                        <tbody
                                                                            style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                            <tr
                                                                                style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                <td
                                                                                    style="font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif;">
                                                                                    <p
                                                                                        style="line-height: 150%; font-size: 14px; margin: 0px; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #999999;">
                                                                                        To reach the consumer support
                                                                                        team with questions regarding
                                                                                        your order please see the
                                                                                        commonly asked questions on our
                                                                                        <a href="https://www.stanley1913.com/_t/c/A1030004-179F9BC513DA06F6-E5E62DC5?l=AACXPX0y%2BY2BXFKHb8YuXdLqHv%2BHGIxaMdjL1zUCefHbHZuEoRK8uo%2BiwNcvadKbEKA3cRmZAFNh0H9BpgoRiqEZOdu8f2oj7CBAMq2oRDR1b6ZQ7fLqFincy5Vj3q8Vck2eZbUnr2d%2F4jsnMyQJKquZ1wxmAOlI45DyWwBwCZCDdJcCmaUJ7j5ZbQnYXa102VPxyk%2F8tVZqwsnF2bb9d%2Bm3EQxIw%2Fz5ZpkmEUU0d1Q%3D&amp;c=AAB20i3y9iEQGBFxCKjvejNbi3aFbIlE5BHLt9yqUPPrBtu39mwoiDQ1%2BbILjk60c7FPBNMUUJcqom%2FKsWYGEE9L3bAvySuKizVgckQR%2FpmTQC3VqrAlSB%2BpI4E1LOrH6E3FfbOyjFQWLuRGEkeQcDXiqoDNLMWTVP24wynWSCpXmoJusWVpFt46V%2B7lFjRiYsCmgmwsJxJM%2BJiTYPZtjuoHpOM%2FI4xyK429mZDlswyOZDyhZyEBiMJGZskcYgAX7KwzUYjQ8G2hacLfjwVu3GzM%2FeRurDe9NWtMcpmwFDERykZeUVSDwm57pCULiup3plXBGo6AdbLbRbKdvIirnLItIJ3kZsqfupO79gaBVYqntvitlcG1WKkCtczZZzMnwxcGaYyIfNKO5P6CxIM4fUtn6oL3%2Bcpkqu2uM8Qeq4txjzeI7aSpRQR7NND%2FWPU8K662mO02WiNNyLXGs82LoN4EV%2BPOpDc4Ng%3D%3D"
                                                                                            style="font-size: 14px; text-decoration: none; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #333333;"
                                                                                            target="_blank"
                                                                                            rel="noopener">FAQ page</a>
                                                                                        in addition to the
                                                                                        <a href="https://www.stanley1913.com/_t/c/A1030004-179F9BC513DA06F6-E5E62DC5?l=AACoQ2qiewiW9ci7UgtqXP%2F7F4K%2BYRJxg%2FKGB0l%2BWvwDzx22%2FXj8ZHNAyQfek4JnBmNVDxyF6bYhUCMXhDfmMIv7TjCm6dtsKd%2BN2z8OhZNd9bf6pouAM%2FHD7zwG6%2Bt02X5oDxWV0vFW%2Ftt%2Fid0bZQeL3S7dYFTrQLh9aw8dXYXzlU69vSnt3zzL5%2BgFwcZ5VlQ7rp91Yj0WwUmNIMV2Bl63eRU015bJU3YtMsMOhT6lx1Uc&amp;c=AAB20i3y9iEQGBFxCKjvejNbi3aFbIlE5BHLt9yqUPPrBtu39mwoiDQ1%2BbILjk60c7FPBNMUUJcqom%2FKsWYGEE9L3bAvySuKizVgckQR%2FpmTQC3VqrAlSB%2BpI4E1LOrH6E3FfbOyjFQWLuRGEkeQcDXiqoDNLMWTVP24wynWSCpXmoJusWVpFt46V%2B7lFjRiYsCmgmwsJxJM%2BJiTYPZtjuoHpOM%2FI4xyK429mZDlswyOZDyhZyEBiMJGZskcYgAX7KwzUYjQ8G2hacLfjwVu3GzM%2FeRurDe9NWtMcpmwFDERykZeUVSDwm57pCULiup3plXBGo6AdbLbRbKdvIirnLItIJ3kZsqfupO79gaBVYqntvitlcG1WKkCtczZZzMnwxcGaYyIfNKO5P6CxIM4fUtn6oL3%2Bcpkqu2uM8Qeq4txjzeI7aSpRQR7NND%2FWPU8K662mO02WiNNyLXGs82LoN4EV%2BPOpDc4Ng%3D%3D"
                                                                                            style="font-size: 14px; text-decoration: none; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Fira Sans','Droid Sans','Helvetica Neue',sans-serif; color: #333333;"
                                                                                            target="_blank"
                                                                                            rel="noopener">contact
                                                                                            us</a> form.
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
                                                <img style="min-width: 600px; height: 0px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;"
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
