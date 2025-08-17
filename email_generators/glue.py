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
    msg['From'] = formataddr((f'Glue Store', sender_email))
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
    "Please enter the order date (12 December, 2024):",
    "Please enter the customer name (Juggy Resells):",
    "Please enter the street address (123 Test Street):",
    "Please enter the suburb (Great Sydney):",
    "Please enter the state & postcode (NSW 2000):",
    "Please enter the country (Australia):",
    "Please enter the mobile number (0412345678):",
    "Please enter the receipt email (tester@gmail.com):",
    "Please enter the image url (MUST BE FROM GLUE SITE):",
    "Please enter the product name (Peace For Pansies):",
    "Please enter the product colour & size (Anthracite / S):",
    "Please enter the product brand (Deus):",
    "Please enter the product id (DMP231504B-Anthracite-S):",
    "Please enter the product price (WITHOUT THE $ SIGN):",
    "Please enter the sales tax amount (WITHOUT THE $ SIGN):",
    "Please enter the order total (WITHOUT THE $ SIGN):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o primeiro nome do cliente (Juggy):",
    "Por favor, insira a data do pedido (12 Dezembro, 2024):",
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira o endereço (123 Test Street):",
    "Por favor, insira o bairro (Great Sydney):",
    "Por favor, insira o estado e CEP (NSW 2000):",
    "Por favor, insira o país (Austrália):",
    "Por favor, insira o número de celular (0412345678):",
    "Por favor, insira o e-mail do recibo (tester@gmail.com):",
    "Por favor, insira a URL da imagem (DEVE SER DO SITE GLUE):",
    "Por favor, insira o nome do produto (Peace For Pansies):",
    "Por favor, insira a cor e tamanho do produto (Anthracite / S):",
    "Por favor, insira a marca do produto (Deus):",
    "Por favor, insira o ID do produto (DMP231504B-Anthracite-S):",
    "Por favor, insira o preço do produto (SEM O SÍMBOLO $):",
    "Por favor, insira o valor do imposto (SEM O SÍMBOLO $):",
    "Por favor, insira o total do pedido (SEM O SÍMBOLO $):",
    "Por favor, insira a moeda ($/€/£):",
    "Qual endereço de e-mail você quer receber este e-mail (juggyresells@gmail.com):"
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
    part1 = f'GLUEAU'
    part2 = random.randint(100000, 999999)  # Random 8-digit number

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
    recipient_email = f'{user_inputs[18]}'
    subject = f"Order {order_num} confirmed"

    # Format input into HTML template
    html_template = f"""
        <div>
        <div style="display:none;overflow:hidden;line-height:1px;max-height:0px;max-width:0px;opacity:0">
            Thank you for your purchase, we have your order. We
            will send you another email as soon as your order is
            shipped.
        </div>
        <div id="m_-2334459430010600387custom-preview-text"
            style="display:none;overflow:hidden;line-height:1px;max-height:0px;max-width:0px;opacity:0">
            ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ ͏‌ 
        </div>





        <table cellpadding="0" cellspacing="0" border="0" width="100%"
            style="border-collapse:collapse;min-width:100%;direction:ltr" role="presentation" bgcolor="#f8f8f8">
            <tbody>
                <tr>
                    <th valign="top">
                        <center style="width:100%">
                            <table border="0" width="600" cellpadding="0" cellspacing="0" align="center"
                                style="width:600px;min-width:600px;max-width:600px;direction:ltr;margin:auto"
                                role="presentation">
                                <tbody>
                                    <tr>
                                        <th valign="top">

                                            <table id="m_-2334459430010600387section-header" border="0" width="100%"
                                                cellpadding="0" cellspacing="0" align="center"
                                                style="min-width:100%;direction:ltr" role="presentation" bgcolor="#ffffff">
                                                <tbody>
                                                    <tr>
                                                        <td style="padding-top:22px;padding-bottom:22px" bgcolor="#ffffff">
                                                            <table border="0" width="100%" cellpadding="0" cellspacing="0"
                                                                align="center" style="min-width:100%;direction:ltr"
                                                                role="presentation">
                                                                <tbody>
                                                                    <tr>
                                                                        <th style="padding-top:0;padding-bottom:0"
                                                                            align="center" bgcolor="#ffffff">

                                                                            <a href="https://www.gluestore.com.au/_t/c/A1030004-179FF8A69851CE20-18FE78AF?l=AADKG4%2F4Pu9H5YbLEFSBVXS74gdf8UXoEyYtk5p8iEMWltBxC6pQb1UGblhk8WP1ihLnIXbGk2Exr4L5Bfv5f8O82YSVa78Ilqpm4q5uW972qBs2c0H2k33075ya8oNhi47h0eq40KqNymJnk6OEvFWWz0%2FFjNb0l2mqgRuS0ZIKPdZywmmW%2F7P6tuOOxap3%2FzDuPDmvLgt3XnG0N%2Bmz95DueeZUStlaaz9b0qU73RTbTUNsHWed8p%2BK0wzs9wac0VKk7kbf0TJX%2BlRDUPv7XybDEIcO0eT7NI898B4NxO%2FmZ%2BmEPnIOlNTcqc2uGaiAqS5AsbU2UcKQ8EUSJN%2BQcN6OpgtTJcy3iMoBDRGSayo%3D&amp;c=AAAByvIKcNB0UzR6nEWTj5EBqXDGFjkOVaxf%2BqCRQeq%2FBPmTqpIPzbTNVPGNBsFLf8OWal6Do8%2BbnqbvyUNyisJay7kYXAOdmMvWZkz4tDzz%2F3NS%2F9ySCPdXFn0sbD04jTC2LoNPpUBWGTjAg3UInXA0XwEiItNiuBR%2FqiSAimJdeoCI2%2FxDq71us86Zjt%2FXcMuldZuetmAJ5qKAUbD6t9AeL1VLtliPSHjlyTG%2BSl5tU37%2FhEynJc90jIVYYL1GW%2FSDJLbzCo0fSSRks%2BpNZOquZuMCCaoF%2FeF4LF7e3PEevgauEio%2BzR9M6Z2qoF0Nt87bbFYji8MSLNSQRwUdrDgkG7mBIi1re3YgbiQxrgUJLhGsVPouG75gsqHBq8usngjzJnGIeELW0whURduEFRXfXTsKa6NedDBokaK7wzQJVJJY7kdR7j7NfJgXCvfItHjPSBCAY%2FV8Z8it7cqI6Yrm5yi0tvn1Tyc%3D"
                                                                                style="color:#a7a7a7;text-decoration:none!important"
                                                                                target="_blank">
                                                                                <img src="https://cdn.filestackcontent.com/api/file/JhtIQYxmQxuWWKrZzCpo/convert?fit=max&amp;w=320"
                                                                                    width="160" border="0"
                                                                                    style="width:160px;height:auto!important;display:block;text-align:center;margin:auto">
                                                                            </a>

                                                                        </th>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>


                                            <table id="m_-2334459430010600387section-main" border="0" width="100%"
                                                cellpadding="0" cellspacing="0" align="center"
                                                style="min-width:100%;direction:ltr" role="presentation" bgcolor="#ffffff">
                                                <tbody>
                                                    <tr>
                                                        <td bgcolor="#ffffff">
                                                            <table border="0" width="100%" cellpadding="0" cellspacing="0"
                                                                align="center" style="min-width:100%;direction:ltr"
                                                                id="m_-2334459430010600387mixContainer" role="presentation">

                                                                <tbody>
                                                                    <tr id="m_-2334459430010600387section-6677880">
                                                                        <th style="padding:33px 44px 11px"
                                                                            bgcolor="#ffffff">
                                                                            <table cellspacing="0" cellpadding="0"
                                                                                border="0" width="100%" role="presentation"
                                                                                style="direction:ltr">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <th bgcolor="#ffffff" valign="top">
                                                                                            <h1 style="font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Karla&#39;;font-size:24px;line-height:36px;font-weight:700;color:#1a1a1a;text-transform:none;margin:0"
                                                                                                align="center">
                                                                                                Order
                                                                                                Invoice
                                                                                            </h1>
                                                                                        </th>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </th>
                                                                    </tr>


                                                                    <tr id="m_-2334459430010600387section-6677881">
                                                                        <th style="padding:22px 44px" bgcolor="#ffffff">
                                                                            <table cellspacing="0" cellpadding="0"
                                                                                border="0" width="100%" role="presentation"
                                                                                style="direction:ltr">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <th style="border-top-width:1px;border-top-color:#eeeeee;border-top-style:solid"
                                                                                            bgcolor="#ffffff" valign="top">
                                                                                        </th>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </th>
                                                                    </tr>


                                                                    <tr id="m_-2334459430010600387section-6677882">
                                                                        <th style="padding:11px 44px" bgcolor="#ffffff">

                                                                            <p style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;margin:0 0 11px"
                                                                                align="left">
                                                                                <span
                                                                                    style="text-align:left;direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777">
                                                                                    Hey
                                                                                </span>
                                                                                {user_inputs[0]},
                                                                            </p>

                                                                            <span
                                                                                style="text-align:left;direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777">
                                                                                <p style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;margin:11px 0 0"
                                                                                    align="left">
                                                                                </p>
                                                                                <p style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;margin:11px 0 0"
                                                                                    align="left">
                                                                                    Thank
                                                                                    you
                                                                                    for
                                                                                    your
                                                                                    purchase,
                                                                                    we
                                                                                    have
                                                                                    your
                                                                                    order.
                                                                                    We
                                                                                    will
                                                                                    send
                                                                                    you
                                                                                    another
                                                                                    email
                                                                                    as
                                                                                    soon
                                                                                    as
                                                                                    your
                                                                                    order
                                                                                    is
                                                                                    shipped.<br>
                                                                                </p>
                                                                            </span>
                                                                        </th>
                                                                    </tr>


                                                                    <tr id="m_-2334459430010600387section-6677883">
                                                                        <th style="padding:0 44px 11px" bgcolor="#ffffff">
                                                                            <table cellspacing="0" cellpadding="0"
                                                                                border="0" width="100%"
                                                                                style="direction:ltr">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <th style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;padding-bottom:11px"
                                                                                            align="left" bgcolor="#ffffff"
                                                                                            valign="top">
                                                                                            You
                                                                                            can
                                                                                            follow
                                                                                            the
                                                                                            status
                                                                                            of
                                                                                            your
                                                                                            order
                                                                                            by
                                                                                            clicking
                                                                                            the
                                                                                            button
                                                                                            below:
                                                                                        </th>
                                                                                    </tr>

                                                                                    <tr>
                                                                                        <th style="margin:0;padding:11px 0"
                                                                                            align="center" bgcolor="#ffffff"
                                                                                            valign="top">
                                                                                            <table cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                role="presentation"
                                                                                                style="direction:ltr;text-align:left;margin:0 auto"
                                                                                                bgcolor="transparent">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <th style="border-radius:1px"
                                                                                                            align="center"
                                                                                                            bgcolor="#ffffff"
                                                                                                            valign="top">
                                                                                                            <a href="https://www.gluestore.com.au/_t/c/A1030004-179FF851CE20-18FE78AF?l=AACuvMd84aC9AYFJTevU%2FyEuG8IS6hgr4pZUSyLdHZgMT%2FmUFKgIKY5ewaNUm5bM1kWsW6XLFvt8mz63jWYoX%2BtGLl7JsvQTXPjV8d691e3azpEpTlr74a%2FUdFcaNjlv4%2FQa0MpDCgktneJTi%2BgE3xe6bIxT3JpaaT6qcjzJPVhsZipI0MaYVlHf4UqHesJNkpKCS%2BrKDfMbLOGpnOmLWT%2F4HU4tBjg8CIGSmYOMTaTv9fQuABiJiUVz3MudkXJ76Uo9U5AJlZf4DQpZCIu27IKxXVyMNeUSj%2B47c2iUMS46SWsM%2FUu%2BL9Pv8RkptCi7UkDl7agoIYaHJxnMVYJfRC6klyfGKk95rkVslCypDyDZNg%3D%3D&amp;c=AAAByvIKcNB0UzR6nEWTj5EBqXDGFjkOVaxf%2BqCRQeq%2FBPmTqpIPzbTNVPGNBsFLf8OWal6Do8%2BbnqbvyUNyisJay7kYXAOdmMvWZkz4tDzz%2F3NS%2F9ySCPdXFn0sbD04jTC2LoNPpUBWGTjAg3UInXA0XwEiItNiuBR%2FqiSAimJdeoCI2%2FxDq71us86Zjt%2FXcMuldZuetmAJ5qKAUbD6t9AeL1VLtliPSHjlyTG%2BSl5tU37%2FhEynJc90jIVYYL1GW%2FSDJLbzCo0fSSRks%2BpNZOquZuMCCaoF%2FeF4LF7e3PEevgauEio%2BzR9M6Z2qoF0Nt87bbFYji8MSLNSQRwUdrDgkG7mBIi1re3YgbiQxrgUJLhGsVPouG75gsqHBq8usngjzJnGIeELW0whURduEFRXfXTsKa6NedDBokaK7wzQJVJJY7kdR7j7NfJgXCvfItHjPSBCAY%2FV8Z8it7cqI6Yrm5yi0tvn1Tyc%3D"
                                                                                                                style="color:#1a1a1a!important;text-decoration:none!important;word-wrap:break-word;line-height:15px;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Karla&#39;;font-size:15px;font-weight:700;text-transform:none;text-align:center;display:block;background-color:#ffffff;border-radius:1px;padding:13px 33px;border:2px solid #1a1a1a"
                                                                                                                target="_blank"><span
                                                                                                                    style="line-height:15px;color:#1a1a1a;font-weight:700;text-decoration:none;letter-spacing:0.5px"><span
                                                                                                                        style="line-height:15px;color:#1a1a1a;font-weight:700;text-decoration:none;letter-spacing:0.5px">View
                                                                                                                        Order
                                                                                                                        Status
                                                                                                                        &gt;</span></span></a>
                                                                                                        </th>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                        </th>
                                                                                    </tr>

                                                                                </tbody>
                                                                            </table>
                                                                        </th>
                                                                    </tr>


                                                                    <tr id="m_-2334459430010600387section-6677884">
                                                                        <th style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;padding:11px 44px"
                                                                            align="left" bgcolor="#ffffff">
                                                                            <p style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;margin:0"
                                                                                align="left">
                                                                                You&#39;ve
                                                                                got
                                                                                questions?
                                                                                We&#39;ve
                                                                                got
                                                                                answers.<br>
                                                                            </p>
                                                                            <p style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;margin:11px 0 0"
                                                                                align="left">
                                                                                Check
                                                                                out
                                                                                our
                                                                                FAQs
                                                                                <a href="https://www.gluestore.com.au/_t/c/A1030004-179FF8A69851CE20-18FE78AF?l=AABwrf8pAxX1M7B5K60quJ0dnxaz%2BR5P6Kve7G8hvMdPzVqy90VSo9QccsvDLCn8N3A9Tl2%2BBAfSJ4dvcI4ODWT1P39iwKfa6zg80CpJKkKotkUKNw1kINd7UUFJj87CnOIA3braAjiM7OKj32S%2Bc7EosiFX58NZ4n9gIe%2Fm2gwYjsXiW19X%2Fa18X3VkzAruzcLwCVZaB7LmL8%2FDsmKhOqqDFXa8X%2F6WgiVbmRX46Scu&amp;c=AAAByvIKcNB0UzR6nEWTj5EBqXDGFjkOVaxf%2BqCRQeq%2FBPmTqpIPzbTNVPGNBsFLf8OWal6Do8%2BbnqbvyUNyisJay7kYXAOdmMvWZkz4tDzz%2F3NS%2F9ySCPdXFn0sbD04jTC2LoNPpUBWGTjAg3UInXA0XwEiItNiuBR%2FqiSAimJdeoCI2%2FxDq71us86Zjt%2FXcMuldZuetmAJ5qKAUbD6t9AeL1VLtliPSHjlyTG%2BSl5tU37%2FhEynJc90jIVYYL1GW%2FSDJLbzCo0fSSRks%2BpNZOquZuMCCaoF%2FeF4LF7e3PEevgauEio%2BzR9M6Z2qoF0Nt87bbFYji8MSLNSQRwUdrDgkG7mBIi1re3YgbiQxrgUJLhGsVPouG75gsqHBq8usngjzJnGIeELW0whURduEFRXfXTsKa6NedDBokaK7wzQJVJJY7kdR7j7NfJgXCvfItHjPSBCAY%2FV8Z8it7cqI6Yrm5yi0tvn1Tyc%3D"
                                                                                    style="color:#0c0c09;text-decoration:none!important;word-wrap:break-word"
                                                                                    target="_blank">here</a>.
                                                                            </p>
                                                                            <p style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;margin:11px 0 0"
                                                                                align="left">
                                                                                Contact
                                                                                us
                                                                                <a href="https://www.gluestore.com.au/_t/c/A1030004-179FF8A69851CE20-18FE78AF?l=AAC2DnmUImwhtJDMhSODFyDPEoftLvyktd0Iyl4pSDevBOSlKFEPSKLDRGh427H0bOH9sWLr6xdA7LQJZ7PPcLncIptWgqmd1iXp29%2BmKIGOdia4CQ9t%2FGocJDCAi9gQ2NAmrh3lKOa3ZdI4UF8S1cXVsIFrU8%2BcQbqU03hgqqKqVkcSGddYYfLnwK2TZq4j4B%2BMKawOtgQCgnCgghGfCWVNbJLDY4mNiVNbcEORcwqs%2BmP5m8rTdChcW6mD0Q%3D%3D&amp;c=AAAByvIKcNB0UzR6nEWTj5EBqXDGFjkOVaxf%2BqCRQeq%2FBPmTqpIPzbTNVPGNBsFLf8OWal6Do8%2BbnqbvyUNyisJay7kYXAOdmMvWZkz4tDzz%2F3NS%2F9ySCPdXFn0sbD04jTC2LoNPpUBWGTjAg3UInXA0XwEiItNiuBR%2FqiSAimJdeoCI2%2FxDq71us86Zjt%2FXcMuldZuetmAJ5qKAUbD6t9AeL1VLtliPSHjlyTG%2BSl5tU37%2FhEynJc90jIVYYL1GW%2FSDJLbzCo0fSSRks%2BpNZOquZuMCCaoF%2FeF4LF7e3PEevgauEio%2BzR9M6Z2qoF0Nt87bbFYji8MSLNSQRwUdrDgkG7mBIi1re3YgbiQxrgUJLhGsVPouG75gsqHBq8usngjzJnGIeELW0whURduEFRXfXTsKa6NedDBokaK7wzQJVJJY7kdR7j7NfJgXCvfItHjPSBCAY%2FV8Z8it7cqI6Yrm5yi0tvn1Tyc%3D"
                                                                                    style="color:#0c0c09;text-decoration:none!important;word-wrap:break-word"
                                                                                    target="_blank">here</a>.
                                                                            </p>
                                                                        </th>
                                                                    </tr>


                                                                    <tr id="m_-2334459430010600387section-6677885">
                                                                        <th style="padding:22px 44px" bgcolor="#ffffff">
                                                                            <table cellspacing="0" cellpadding="0"
                                                                                border="0" width="100%" role="presentation"
                                                                                style="direction:ltr">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <th style="border-top-width:1px;border-top-color:#eeeeee;border-top-style:solid"
                                                                                            bgcolor="#ffffff" valign="top">
                                                                                        </th>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </th>
                                                                    </tr>


                                                                    <tr id="m_-2334459430010600387section-6677886">
                                                                        <th style="padding:11px 44px" bgcolor="#ffffff">

                                                                            <h2 style="font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Karla&#39;;color:#1a1a1a;font-size:14px;line-height:22px;font-weight:700;text-transform:none;margin:0"
                                                                                align="left">
                                                                                <span>Order
                                                                                    No.
                                                                                    /
                                                                                    Invoice
                                                                                    No.</span>
                                                                                {order_num}
                                                                            </h2>
                                                                            <p style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:13px;line-height:22px;font-weight:normal;text-transform:none;color:#999999;margin:0"
                                                                                align="left">
                                                                                {user_inputs[1]}
                                                                            </p>

                                                                        </th>
                                                                    </tr>


                                                                    <tr id="m_-2334459430010600387section-6677887">

                                                                        <th style="padding:11px 44px" bgcolor="#ffffff">
                                                                            <table border="0" width="100%" cellpadding="0"
                                                                                cellspacing="0" align="center"
                                                                                style="min-width:100%;direction:ltr"
                                                                                role="presentation">
                                                                                <tbody>
                                                                                    <tr>

                                                                                        <th width="50%" align="left"
                                                                                            bgcolor="#ffffff" valign="top">
                                                                                            <table align="center" border="0"
                                                                                                width="100%" cellpadding="0"
                                                                                                cellspacing="0"
                                                                                                style="min-width:100%;direction:ltr"
                                                                                                role="presentation">


                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <th style="padding-right:11px"
                                                                                                            align="left"
                                                                                                            bgcolor="#ffffff"
                                                                                                            valign="top">
                                                                                                            <h3 style="font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Karla&#39;;color:#1a1a1a;font-size:14px;line-height:22px;font-weight:700;text-transform:none;margin:0"
                                                                                                                align="left">
                                                                                                                Shipping
                                                                                                                Address
                                                                                                            </h3>
                                                                                                        </th>
                                                                                                    </tr>
                                                                                                    <tr>
                                                                                                        <th style="padding-right:11px"
                                                                                                            align="left"
                                                                                                            bgcolor="#ffffff"
                                                                                                            valign="top">
                                                                                                            <p style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;margin:0"
                                                                                                                align="left">
                                                                                                                {user_inputs[2]}<br>{user_inputs[3]}<br>{user_inputs[4]},
                                                                                                                {user_inputs[5]}<br>{user_inputs[6]}<br><span
                                                                                                                    style="text-align:left;direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777">Tel.</span>
                                                                                                                <span
                                                                                                                    style="color:inherit!important;text-decoration:none!important;text-align:left;direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none">{user_inputs[7]}</span><br>
                                                                                                            </p>
                                                                                                        </th>
                                                                                                    </tr>



                                                                                                </tbody>
                                                                                            </table>
                                                                                        </th>


                                                                                        <th width="50%" align="left"
                                                                                            bgcolor="#ffffff" valign="top">
                                                                                            <table align="center" border="0"
                                                                                                width="100%" cellpadding="0"
                                                                                                cellspacing="0"
                                                                                                style="min-width:100%;direction:ltr"
                                                                                                role="presentation">


                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <th style="padding-left:11px"
                                                                                                            align="left"
                                                                                                            bgcolor="#ffffff"
                                                                                                            valign="top">
                                                                                                            <h3 style="font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Karla&#39;;color:#1a1a1a;font-size:14px;line-height:22px;font-weight:700;text-transform:none;margin:0"
                                                                                                                align="left">
                                                                                                                Customer
                                                                                                            </h3>
                                                                                                        </th>
                                                                                                    </tr>

                                                                                                    <tr>
                                                                                                        <th style="padding-left:11px"
                                                                                                            align="left"
                                                                                                            bgcolor="#ffffff"
                                                                                                            valign="top">
                                                                                                            <p style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;margin:0"
                                                                                                                align="left">
                                                                                                                {user_inputs[2]}<br>{user_inputs[3]}<br>{user_inputs[4]},
                                                                                                                {user_inputs[5]}<br>{user_inputs[6]}<br><span
                                                                                                                    style="text-align:left;direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777">Tel.</span>
                                                                                                                <span
                                                                                                                    style="color:inherit!important;text-decoration:none!important;text-align:left;direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none">{user_inputs[7]}</span><br>
                                                                                                                <span
                                                                                                                    <br><a
                                                                                                                    href="mailto:{user_inputs[8]}"
                                                                                                                    style="color:#0c0c09;text-decoration:none!important;word-wrap:break-word"
                                                                                                                    target="_blank">{user_inputs[8]}</a>
                                                                                                            </p>
                                                                                                        </th>
                                                                                                    </tr>

                                                                                                </tbody>
                                                                                            </table>
                                                                                        </th>

                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </th>

                                                                    </tr>


                                                                    <tr id="m_-2334459430010600387section-6677888">





                                                                        <th style="padding:11px 44px" bgcolor="#ffffff">
                                                                            <table cellspacing="0" cellpadding="0"
                                                                                border="0" width="100%"
                                                                                style="min-width:100%;direction:ltr"
                                                                                role="presentation">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <th bgcolor="#ffffff" valign="top">
                                                                                            <table cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                width="100%"
                                                                                                style="min-width:100%;direction:ltr"
                                                                                                role="presentation">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <th colspan="2"
                                                                                                            bgcolor="#ffffff"
                                                                                                            valign="top">
                                                                                                            <h3 style="font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Karla&#39;;color:#1a1a1a;font-size:14px;line-height:22px;font-weight:700;text-transform:none;border-bottom-width:1px;border-bottom-color:#eeeeee;border-bottom-style:solid;margin:0"
                                                                                                                align="left">
                                                                                                                Items
                                                                                                                ordered
                                                                                                            </h3>
                                                                                                        </th>
                                                                                                    </tr>












                                                                                                    <tr>
                                                                                                        <th width="1"
                                                                                                            style="border-bottom-width:1px;border-bottom-color:#eeeeee;border-bottom-style:solid;padding:11px 11px 11px 0"
                                                                                                            bgcolor="#ffffff"
                                                                                                            valign="middle">
                                                                                                            <a href="https://www.gluestore.com.au/_t/c/A1030004-179FF8A69851CE20-18FE78AF?l=AADeReV0deiVvQiuyWa%2FKbj8o0ghl%2Bg65j1esBOr1%2BsGuHGW2N0M1s%2F6HWN356R9YQ85ugKYjAxKkDtjjzIYXCN4wbUPOlZ3%2B7pVlFgEgerCc0iHl0j2pt09ewC4RQSuLH3Eqh4Ix%2FSEvbCfV4C%2FcrjLzNdTKaVIsP0ePbS8y0QnVXZ8DM3n2Dks2CoUz88MifRahh1s%2BzBDj2PCCSHqjsQUFqR7JKbsQTCt%2BgsSZ72umoygcLwUppYv4CqWhBa7c5DGemJQh6%2FmVhggrNA3v7yNuhKcvBRA8nSoobWMftuB8s3L6%2FJ6CHykuziDld8TpQzsZDwltXEzg0DjwN61BiJ4mxWCzNBKZzTeTXT1gIdHtuy2otbLeioZqCh90vEYOjTdrEWggbuRArK4m9eFKe2eNWThlGAYa8fd4nxBR9wRZEtEN7%2BqMy03y0PWMxB0&amp;c=AAAByvIKcNB0UzR6nEWTj5EBqXDGFjkOVaxf%2BqCRQeq%2FBPmTqpIPzbTNVPGNBsFLf8OWal6Do8%2BbnqbvyUNyisJay7kYXAOdmMvWZkz4tDzz%2F3NS%2F9ySCPdXFn0sbD04jTC2LoNPpUBWGTjAg3UInXA0XwEiItNiuBR%2FqiSAimJdeoCI2%2FxDq71us86Zjt%2FXcMuldZuetmAJ5qKAUbD6t9AeL1VLtliPSHjlyTG%2BSl5tU37%2FhEynJc90jIVYYL1GW%2FSDJLbzCo0fSSRks%2BpNZOquZuMCCaoF%2FeF4LF7e3PEevgauEio%2BzR9M6Z2qoF0Nt87bbFYji8MSLNSQRwUdrDgkG7mBIi1re3YgbiQxrgUJLhGsVPouG75gsqHBq8usngjzJnGIeELW0whURduEFRXfXTsKa6NedDBokaK7wzQJVJJY7kdR7j7NfJgXCvfItHjPSBCAY%2FV8Z8it7cqI6Yrm5yi0tvn1Tyc%3D"
                                                                                                                style="color:#0c0c09;text-decoration:none!important;word-wrap:break-word"
                                                                                                                target="_blank"><img
                                                                                                                    width="120"
                                                                                                                    src="{user_inputs[9]}"
                                                                                                                    alt="{user_inputs[10]}"
                                                                                                                    style="vertical-align:middle;text-align:center;width:120px;max-width:120px;height:auto!important;border-radius:0px;padding:0px"></a>
                                                                                                        </th>
                                                                                                        <th style="padding-top:11px;padding-bottom:11px;border-bottom-width:1px;border-bottom-color:#eeeeee;border-bottom-style:solid"
                                                                                                            bgcolor="#ffffff"
                                                                                                            valign="middle">
                                                                                                            <table
                                                                                                                cellspacing="0"
                                                                                                                cellpadding="0"
                                                                                                                border="0"
                                                                                                                width="100%"
                                                                                                                style="min-width:100%;direction:ltr"
                                                                                                                role="presentation">
                                                                                                                <tbody>
                                                                                                                    <tr>

                                                                                                                        <th style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;padding:11px 5px 11px 0"
                                                                                                                            align="left"
                                                                                                                            bgcolor="#ffffff"
                                                                                                                            valign="top">
                                                                                                                            <p style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;margin:0"
                                                                                                                                align="left">
                                                                                                                                <a href="https://www.gluestore.com.au/_t/c/A1030004-179FF8A69851CE20-18FE78AF?l=AAAnlX35KDB2H8Wwe4fulqWujiKeAMWVaBDj0WPKFD57ZxhTrlFMVNH07%2BwvCECcn31Qd7NrketgK6ie1x0MIsZ87NCZo146XTI1qIr2Ob%2BC2Q%2BZuFxa7KEx8jTQGx46WYEkId%2BzkQi6LvqbUjlTKEqOEB1dv7kvwCypejGYvaJpOiuVg6LrB%2BnFoppd8%2ByHOj1MFKzLiNcPDcNs0MdcB8r%2Be7h5M4i%2Bc5Jm4Icp7RBPLgalMD0RRKcWtO%2BPzST9P2FfAgT30SfxcwRyuELbhXq15lJ3ogU6WrnagLPzBW5EqaeP1rxJ8z2dRfsUIq4BlHuz%2FdngyDJKpWWbTKfm49QOii67VNWgKKdvdQKdnrIHJa79gva4W2yaghpgDxmC85W5z6Qzj0SELEtUHeOV2oYqMP%2BdBv%2FzBnFkbP7iK%2BJGdJAvxN6Hj20KoINVCZRJ&amp;c=AAAByvIKcNB0UzR6nEWTj5EBqXDGFjkOVaxf%2BqCRQeq%2FBPmTqpIPzbTNVPGNBsFLf8OWal6Do8%2BbnqbvyUNyisJay7kYXAOdmMvWZkz4tDzz%2F3NS%2F9ySCPdXFn0sbD04jTC2LoNPpUBWGTjAg3UInXA0XwEiItNiuBR%2FqiSAimJdeoCI2%2FxDq71us86Zjt%2FXcMuldZuetmAJ5qKAUbD6t9AeL1VLtliPSHjlyTG%2BSl5tU37%2FhEynJc90jIVYYL1GW%2FSDJLbzCo0fSSRks%2BpNZOquZuMCCaoF%2FeF4LF7e3PEevgauEio%2BzR9M6Z2qoF0Nt87bbFYji8MSLNSQRwUdrDgkG7mBIi1re3YgbiQxrgUJLhGsVPouG75gsqHBq8usngjzJnGIeELW0whURduEFRXfXTsKa6NedDBokaK7wzQJVJJY7kdR7j7NfJgXCvfItHjPSBCAY%2FV8Z8it7cqI6Yrm5yi0tvn1Tyc%3D"
                                                                                                                                    style="color:#777777;text-decoration:none!important;word-wrap:break-word;text-align:left!important;font-weight:400"
                                                                                                                                    target="_blank">
                                                                                                                                    {user_inputs[10]}
                                                                                                                                </a>

                                                                                                                                <br>
                                                                                                                                <span
                                                                                                                                    style="text-align:left;direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:13px;line-height:22px;font-weight:normal;text-transform:none;color:#999999">{user_inputs[11]}</span>



                                                                                                                                <br>
                                                                                                                                <span
                                                                                                                                    style="text-align:left;direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:13px;line-height:22px;font-weight:normal;text-transform:none;color:#999999">{user_inputs[12]}</span>


                                                                                                                                <br>
                                                                                                                                <span
                                                                                                                                    style="text-align:left;direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:13px;line-height:22px;font-weight:normal;text-transform:none;color:#999999">{user_inputs[13]}</span>



                                                                                                                            </p>
                                                                                                                        </th>
                                                                                                                        <th width="1"
                                                                                                                            style="white-space:nowrap;padding:11px 5px 11px 22px"
                                                                                                                            align="right"
                                                                                                                            bgcolor="#ffffff"
                                                                                                                            valign="top">
                                                                                                                            <p style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;margin:0"
                                                                                                                                align="right">
                                                                                                                                x 1
                                                                                                                            </p>
                                                                                                                        </th>
                                                                                                                        <th width="1"
                                                                                                                            style="white-space:nowrap;padding:11px 0 11px 22px"
                                                                                                                            align="right"
                                                                                                                            bgcolor="#ffffff"
                                                                                                                            valign="top">
                                                                                                                            <p style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;margin:0"
                                                                                                                                align="right">
                                                                                                                                {user_inputs[17]}{user_inputs[14]}
                                                                                                                            </p>
                                                                                                                        </th>
                                                                                                                    </tr>
                                                                                                                </tbody>
                                                                                                            </table>
                                                                                                        </th>
                                                                                                    </tr>

                                                                                                    <tr>
                                                                                                        <th colspan="2"
                                                                                                            bgcolor="#ffffff"
                                                                                                            valign="top">
                                                                                                        </th>
                                                                                                    </tr>


                                                                                                </tbody>
                                                                                            </table>
                                                                                        </th>
                                                                                    </tr>
                                                                                    <tr>
                                                                                        <th style="padding:11px 0"
                                                                                            bgcolor="#ffffff" valign="top">
                                                                                            <table cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                width="100%"
                                                                                                style="min-width:100%;direction:ltr"
                                                                                                role="presentation">

                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <th style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;width:65%;padding:5px 0"
                                                                                                            align="left"
                                                                                                            bgcolor="#ffffff"
                                                                                                            valign="top">
                                                                                                            Subtotal
                                                                                                        </th>
                                                                                                        <th style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;width:35%;padding:5px 0"
                                                                                                            align="right"
                                                                                                            bgcolor="#ffffff"
                                                                                                            valign="middle">
                                                                                                            {user_inputs[17]}{user_inputs[14]}
                                                                                                        </th>
                                                                                                    </tr>




                                                                                                    <tr>
                                                                                                        <th style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;width:65%;padding:5px 0"
                                                                                                            align="left"
                                                                                                            bgcolor="#ffffff"
                                                                                                            valign="top">
                                                                                                            Sales
                                                                                                            tax
                                                                                                        </th>
                                                                                                        <th style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;width:35%;padding:5px 0"
                                                                                                            align="right"
                                                                                                            bgcolor="#ffffff"
                                                                                                            valign="middle">
                                                                                                            {user_inputs[17]}{user_inputs[15]}
                                                                                                        </th>
                                                                                                    </tr>

                                                                                                    <tr>
                                                                                                        <th style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Karla&#39;;font-size:15px;line-height:22px;font-weight:700;text-transform:none;color:#1a1a1a;width:65%;padding:5px 0"
                                                                                                            align="left"
                                                                                                            bgcolor="#ffffff"
                                                                                                            valign="top">
                                                                                                            Total
                                                                                                        </th>
                                                                                                        <th style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Karla&#39;;font-size:15px;line-height:22px;font-weight:700;text-transform:none;color:#1a1a1a;width:35%;padding:5px 0"
                                                                                                            align="right"
                                                                                                            bgcolor="#ffffff"
                                                                                                            valign="middle">
                                                                                                            {user_inputs[17]}{user_inputs[16]}
                                                                                                        </th>
                                                                                                    </tr>



                                                                                                </tbody>
                                                                                            </table>
                                                                                        </th>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </th>

                                                                    </tr>


                                                                    <tr id="m_-2334459430010600387section-6677889">
                                                                        <th style="padding:11px 44px" bgcolor="#ffffff">
                                                                            <table cellspacing="0" cellpadding="0"
                                                                                border="0" width="100%"
                                                                                style="min-width:100%;direction:ltr"
                                                                                role="presentation">






                                                                            </table>
                                                                        </th>
                                                                    </tr>


                                                                    <tr id="m_-2334459430010600387section-8143556">
                                                                        <th style="padding:22px 44px" bgcolor="#ffffff">
                                                                            <table cellspacing="0" cellpadding="0"
                                                                                border="0" width="100%" role="presentation"
                                                                                style="direction:ltr">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <th style="border-top-width:1px;border-top-color:#eeeeee;border-top-style:solid"
                                                                                            bgcolor="#ffffff" valign="top">
                                                                                        </th>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </th>
                                                                    </tr>


                                                                    <tr id="m_-2334459430010600387section-8143554">
                                                                        <th style="padding:22px 44px" align="center"
                                                                            bgcolor="#ffffff">
                                                                            <table cellspacing="0" cellpadding="0"
                                                                                border="0" width="100%"
                                                                                style="direction:ltr">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <th colspan="2" width="100%"
                                                                                            align="center" bgcolor="#ffffff"
                                                                                            valign="top">
                                                                                            <h1 style="font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Karla&#39;;font-size:24px;line-height:36px;font-weight:700;color:#1a1a1a;text-transform:none;margin:0"
                                                                                                align="center">
                                                                                                Track
                                                                                                &amp;
                                                                                                Manage
                                                                                                Your
                                                                                                Delivery
                                                                                                With
                                                                                                The
                                                                                                AusPost
                                                                                                App
                                                                                            </h1>
                                                                                        </th>
                                                                                    </tr>
                                                                                    <tr>
                                                                                        <th colspan="2" width="100%"
                                                                                            style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777"
                                                                                            align="center" bgcolor="#ffffff"
                                                                                            valign="top">
                                                                                            <p style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;margin:0"
                                                                                                align="center">
                                                                                                View
                                                                                                extra
                                                                                                tracking
                                                                                                information,
                                                                                                &amp;
                                                                                                request
                                                                                                to
                                                                                                have
                                                                                                parcels
                                                                                                left
                                                                                                in
                                                                                                a
                                                                                                safe
                                                                                                location.
                                                                                            </p>
                                                                                            <p style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;margin:11px 0 0"
                                                                                                align="center">
                                                                                                Redirect
                                                                                                parcels
                                                                                                while
                                                                                                they&#39;re
                                                                                                on
                                                                                                the
                                                                                                way,
                                                                                                to
                                                                                                a
                                                                                                Post
                                                                                                Office,
                                                                                                Parcel
                                                                                                Locker,
                                                                                                PO
                                                                                                Box
                                                                                                or
                                                                                                new
                                                                                                street
                                                                                                address.
                                                                                            </p>
                                                                                        </th>
                                                                                    </tr>
                                                                                    <tr>

                                                                                        <th align="center" bgcolor="#ffffff"
                                                                                            valign="top">
                                                                                            <table border="0" width="100%"
                                                                                                cellpadding="0"
                                                                                                cellspacing="0"
                                                                                                align="center"
                                                                                                style="min-width:100%;direction:ltr"
                                                                                                role="presentation">
                                                                                                <tbody>
                                                                                                    <tr>

                                                                                                        <th width="50%"
                                                                                                            align="center"
                                                                                                            bgcolor="#ffffff"
                                                                                                            valign="top">
                                                                                                            <table
                                                                                                                align="center"
                                                                                                                border="0"
                                                                                                                width="100%"
                                                                                                                cellpadding="0"
                                                                                                                cellspacing="0"
                                                                                                                style="min-width:100%;direction:ltr"
                                                                                                                role="presentation">
                                                                                                                <tbody>
                                                                                                                    <tr>
                                                                                                                        <th style="padding-right:11px;padding-top:22px"
                                                                                                                            align="left"
                                                                                                                            bgcolor="#ffffff"
                                                                                                                            valign="top">
                                                                                                                            <a href="https://www.gluestore.com.au/_t/c/A1030004-179FF8A69851CE20-18FE78AF?l=AAD%2BySmjZR6%2Fcb%2FhAYr9h1OJID8GvN1CRdErGRG518isRoEWgz4YyB93WHcTBGzuc5kwaOsQ5TjCZ42uZWdRMFptD270usqTKf6XiegbLAZrK1ApqXxQKU7aW52hrY1i4XiI1M1fVbmcEte32aiu2q4MvOSJ5Az1uHkzL9QwOkrRk%2FfclXL6khBDltujvqLHPPQ2s272WnzIPkKwmFZpjA%3D%3D&amp;c=AAAByvIKcNB0UzR6nEWTj5EBqXDGFjkOVaxf%2BqCRQeq%2FBPmTqpIPzbTNVPGNBsFLf8OWal6Do8%2BbnqbvyUNyisJay7kYXAOdmMvWZkz4tDzz%2F3NS%2F9ySCPdXFn0sbD04jTC2LoNPpUBWGTjAg3UInXA0XwEiItNiuBR%2FqiSAimJdeoCI2%2FxDq71us86Zjt%2FXcMuldZuetmAJ5qKAUbD6t9AeL1VLtliPSHjlyTG%2BSl5tU37%2FhEynJc90jIVYYL1GW%2FSDJLbzCo0fSSRks%2BpNZOquZuMCCaoF%2FeF4LF7e3PEevgauEio%2BzR9M6Z2qoF0Nt87bbFYji8MSLNSQRwUdrDgkG7mBIi1re3YgbiQxrgUJLhGsVPouG75gsqHBq8usngjzJnGIeELW0whURduEFRXfXTsKa6NedDBokaK7wzQJVJJY7kdR7j7NfJgXCvfItHjPSBCAY%2FV8Z8it7cqI6Yrm5yi0tvn1Tyc%3D"
                                                                                                                                style="color:#0c0c09;text-decoration:none!important;word-wrap:break-word;text-align:left"
                                                                                                                                target="_blank">
                                                                                                                                <img src="https://www.orderlyemails.com/app_store_banner_apple.png"
                                                                                                                                    width="200"
                                                                                                                                    border="0"
                                                                                                                                    style="width:200px;height:auto!important;display:block;max-width:200px;text-align:left;margin:auto">
                                                                                                                            </a>
                                                                                                                        </th>
                                                                                                                    </tr>
                                                                                                                </tbody>
                                                                                                            </table>
                                                                                                        </th>


                                                                                                        <th width="50%"
                                                                                                            align="center"
                                                                                                            bgcolor="#ffffff"
                                                                                                            valign="top">
                                                                                                            <table
                                                                                                                align="center"
                                                                                                                border="0"
                                                                                                                width="100%"
                                                                                                                cellpadding="0"
                                                                                                                cellspacing="0"
                                                                                                                style="min-width:100%;direction:ltr"
                                                                                                                role="presentation">
                                                                                                                <tbody>
                                                                                                                    <tr>
                                                                                                                        <th style="padding-left:11px;padding-top:22px"
                                                                                                                            align="left"
                                                                                                                            bgcolor="#ffffff"
                                                                                                                            valign="top">
                                                                                                                            <a href="https://www.gluestore.com.au/_t/c/A1030004-179FF8A69851CE20-18FE78AF?l=AACJDkQZpMqh%2Be7FGjaQx6HbgrQ96IIOy4LWkTJOqMh7eV9g92a5SWK3zp%2BVOh3reckPMfjqNfvsZc9JrS3Ns%2BlZ9dDGBbYD%2F4b001XznHgtAqeInRfGqvufHLT%2FtxdNTStouc04DtvmLMToOp6U9%2BJ4EMyw5r%2Bm0AqP%2FKTddYKEUP4XTTWfAGqdZArp%2F7SzXs329JwyXTjimz4je567S78LaQ%3D%3D&amp;c=AAAByvIKcNB0UzR6nEWTj5EBqXDGFjkOVaxf%2BqCRQeq%2FBPmTqpIPzbTNVPGNBsFLf8OWal6Do8%2BbnqbvyUNyisJay7kYXAOdmMvWZkz4tDzz%2F3NS%2F9ySCPdXFn0sbD04jTC2LoNPpUBWGTjAg3UInXA0XwEiItNiuBR%2FqiSAimJdeoCI2%2FxDq71us86Zjt%2FXcMuldZuetmAJ5qKAUbD6t9AeL1VLtliPSHjlyTG%2BSl5tU37%2FhEynJc90jIVYYL1GW%2FSDJLbzCo0fSSRks%2BpNZOquZuMCCaoF%2FeF4LF7e3PEevgauEio%2BzR9M6Z2qoF0Nt87bbFYji8MSLNSQRwUdrDgkG7mBIi1re3YgbiQxrgUJLhGsVPouG75gsqHBq8usngjzJnGIeELW0whURduEFRXfXTsKa6NedDBokaK7wzQJVJJY7kdR7j7NfJgXCvfItHjPSBCAY%2FV8Z8it7cqI6Yrm5yi0tvn1Tyc%3D"
                                                                                                                                style="color:#0c0c09;text-decoration:none!important;word-wrap:break-word;text-align:left"
                                                                                                                                target="_blank">
                                                                                                                                <img src="https://www.orderlyemails.com/app_store_banner_google.png"
                                                                                                                                    width="200"
                                                                                                                                    border="0"
                                                                                                                                    style="width:200px;height:auto!important;display:block;max-width:200px;text-align:left;margin:auto">
                                                                                                                            </a>
                                                                                                                        </th>
                                                                                                                    </tr>
                                                                                                                </tbody>
                                                                                                            </table>
                                                                                                        </th>

                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                        </th>

                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </th>
                                                                    </tr>


                                                                    <tr id="m_-2334459430010600387section-8143555">
                                                                        <th style="padding:22px 44px" bgcolor="#ffffff">
                                                                            <table cellspacing="0" cellpadding="0"
                                                                                border="0" width="100%" role="presentation"
                                                                                style="direction:ltr">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <th style="border-top-width:1px;border-top-color:#eeeeee;border-top-style:solid"
                                                                                            bgcolor="#ffffff" valign="top">
                                                                                        </th>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </th>
                                                                    </tr>


                                                                    <tr id="m_-2334459430010600387section-11177317">
                                                                        <th style="padding:11px 44px" bgcolor="#ffffff">
                                                                            <table cellspacing="0" cellpadding="0"
                                                                                border="0" width="100%" role="presentation"
                                                                                style="direction:ltr">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <th bgcolor="#ffffff" valign="top">
                                                                                            <h1 style="font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Karla&#39;;font-size:24px;line-height:36px;font-weight:700;color:#1a1a1a;text-transform:none;margin:0"
                                                                                                align="center">
                                                                                                Add
                                                                                                The
                                                                                                Finishing
                                                                                                Touch
                                                                                            </h1>
                                                                                        </th>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </th>
                                                                    </tr>


                                                                    <tr id="m_-2334459430010600387section-11177318">
                                                                        <th style="padding:11px 44px" bgcolor="#ffffff">
                                                                            <table cellspacing="0" cellpadding="0"
                                                                                border="0" width="100%" role="presentation"
                                                                                style="direction:ltr">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <th style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;padding-bottom:11px"
                                                                                            align="left" bgcolor="#ffffff"
                                                                                            valign="top">
                                                                                            <p style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Open Sans&#39;;font-size:15px;line-height:22px;font-weight:400;text-transform:none;color:#777777;margin:0"
                                                                                                align="left">
                                                                                                No
                                                                                                outfit
                                                                                                is
                                                                                                complete
                                                                                                without
                                                                                                the
                                                                                                right
                                                                                                shoes
                                                                                                and
                                                                                                accesories.
                                                                                                Add
                                                                                                the
                                                                                                finishing
                                                                                                touch
                                                                                                with
                                                                                                our
                                                                                                latest
                                                                                                arrivals
                                                                                                from
                                                                                                Nike,
                                                                                                Superga,
                                                                                                Dr
                                                                                                Martens,
                                                                                                Adidas
                                                                                                more.<br
                                                                                                    style="text-align:left">
                                                                                            </p>
                                                                                        </th>
                                                                                    </tr>

                                                                                    <tr>
                                                                                        <th style="margin:0;padding:11px 0"
                                                                                            align="center" bgcolor="#ffffff"
                                                                                            valign="top">
                                                                                            <table cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                role="presentation"
                                                                                                style="direction:ltr;text-align:left;margin:0 auto"
                                                                                                bgcolor="transparent">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <th style="border-radius:1px"
                                                                                                            align="center"
                                                                                                            bgcolor="#ffffff"
                                                                                                            valign="top">
                                                                                                            <a href="https://www.gluestore.com.au/_t/c/A1030004-179FF8A69851CE20-18FE78AF?l=AADdJlkdpJIPb1o42Kiz%2FXpcMhXtbhAmtpwVGmF4RqHcQWdoOzmhlUIKcyIxXKW4AcLZHGmYeaOS6QzcfI7xzTIxq%2FGL9ItwqtVfoWqZOXUEg1Mg6ZxRrjcp0dHLjIrpyBFZL%2FflU1O9J8LGEYKD2kNL%2Bn5zmk1LHVZqmsHmRIsNv48d4TUu8jkDO1zgC1uIBhLCqKvDfFFWYW9PiMU0l3eBYMRes3CsFlBLgoJbTxNzHYpmKD4QaBS4klfgczal%2BMA9Dag3kni%2BG5PfASnb0BIvoSZroUrIKTWkjUj80J1S%2B%2FcMTBbQbVKdV9J6I2oUF3%2FSP7afh9qBcpxJiwnsIRmC%2BPm8zxES6tsc8E4DVFbzC%2B9IeX2fVwtfvu6FuuUGgfGBO80vgVScJd%2Fjq%2Fv8xnGo5pCt5m8AZLyuix5PRXG5lpeo3jhjN%2FRUPiuVjviYA3CNpAzDH2S7utC9fQ%3D%3D&amp;c=AAAByvIKcNB0UzR6nEWTj5EBqXDGFjkOVaxf%2BqCRQeq%2FBPmTqpIPzbTNVPGNBsFLf8OWal6Do8%2BbnqbvyUNyisJay7kYXAOdmMvWZkz4tDzz%2F3NS%2F9ySCPdXFn0sbD04jTC2LoNPpUBWGTjAg3UInXA0XwEiItNiuBR%2FqiSAimJdeoCI2%2FxDq71us86Zjt%2FXcMuldZuetmAJ5qKAUbD6t9AeL1VLtliPSHjlyTG%2BSl5tU37%2FhEynJc90jIVYYL1GW%2FSDJLbzCo0fSSRks%2BpNZOquZuMCCaoF%2FeF4LF7e3PEevgauEio%2BzR9M6Z2qoF0Nt87bbFYji8MSLNSQRwUdrDgkG7mBIi1re3YgbiQxrgUJLhGsVPouG75gsqHBq8usngjzJnGIeELW0whURduEFRXfXTsKa6NedDBokaK7wzQJVJJY7kdR7j7NfJgXCvfItHjPSBCAY%2FV8Z8it7cqI6Yrm5yi0tvn1Tyc%3D"
                                                                                                                style="color:#1a1a1a!important;text-decoration:none!important;word-wrap:break-word;line-height:15px;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Karla&#39;;font-size:15px;font-weight:700;text-transform:none;text-align:center;display:block;background-color:#ffffff;border-radius:1px;padding:13px 33px;border:2px solid #1a1a1a"
                                                                                                                target="_blank"><span
                                                                                                                    style="line-height:15px;color:#1a1a1a;font-weight:700;text-decoration:none;letter-spacing:0.5px"><span
                                                                                                                        style="line-height:15px;color:#1a1a1a;font-weight:700;text-decoration:none;letter-spacing:0.5px">Complete
                                                                                                                        Your
                                                                                                                        Look</span></span></a>
                                                                                                        </th>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                        </th>
                                                                                    </tr>

                                                                                </tbody>
                                                                            </table>
                                                                        </th>
                                                                    </tr>


                                                                    <tr id="m_-2334459430010600387section-11177316">
                                                                        <th style="padding:22px 44px" bgcolor="#ffffff">
                                                                            <table cellspacing="0" cellpadding="0"
                                                                                border="0" width="100%" role="presentation"
                                                                                style="direction:ltr">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <th style="border-top-width:1px;border-top-color:#eeeeee;border-top-style:solid"
                                                                                            bgcolor="#ffffff" valign="top">
                                                                                        </th>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </th>
                                                                    </tr>


                                                                    <tr id="m_-2334459430010600387section-7445936">
                                                                        <th style="padding:11px 44px 33px"
                                                                            bgcolor="#ffffff">
                                                                            <table cellspacing="0" cellpadding="0"
                                                                                border="0" width="100%" role="presentation"
                                                                                style="direction:ltr">

                                                                                <tbody>
                                                                                    <tr>
                                                                                        <th style="margin:0;padding:11px 0"
                                                                                            align="center" bgcolor="#ffffff"
                                                                                            valign="top">
                                                                                            <table cellspacing="0"
                                                                                                cellpadding="0" border="0"
                                                                                                role="presentation"
                                                                                                style="direction:ltr;text-align:left;margin:0 auto"
                                                                                                bgcolor="transparent">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <th style="border-radius:1px"
                                                                                                            align="center"
                                                                                                            bgcolor="#ffffff"
                                                                                                            valign="top">
                                                                                                            <a href="https://www.gluestore.com.au/_t/c/A1030004-179FF8A69851CE20-18FE78AF?l=AAA73iF7zDYHORQ2l%2BDOotPILPm1N53Y%2Bcp4YMQzk%2Bj7yXTNgDOn01q5gG%2FexpgxRCBUX4UNeXOZctoVQqYWQC0pa7DADanOdTOcD%2FKq3jnVHUerl%2Bm3A96W%2FDFG7440gz0StxjpdlzsHddfNJY%2BLMUIirZ0goQkBKDxD6TwoSJ2QiBhQ%2BtMziYr1c8Q1ujV0mlB%2BKMjtxdDXW2CFlSuxcTRRmJ5Wc2aEUCsH8aDxnKHqENoGE%2FP5Oo%2BOSgdS2rslxRbx8Kt%2Fq3TJMj2jzWdjxL3cZJBjH5fVfX14zl135XMKAXQYrUAyi3cq9dA9dbYs6HZdB0Cf7XrFFQ766v7bUu3tQZWUPocTGSOgp53s3y3jTCuOcKghO9FldOz6CWdfAJOtSXPcUnAyiTAHQBvc7%2FVv3lz0MOJgwm9MmvOZWkP6SLMvofW9lCOu4eXldBZNygKCw%3D%3D&amp;c=AAAByvIKcNB0UzR6nEWTj5EBqXDGFjkOVaxf%2BqCRQeq%2FBPmTqpIPzbTNVPGNBsFLf8OWal6Do8%2BbnqbvyUNyisJay7kYXAOdmMvWZkz4tDzz%2F3NS%2F9ySCPdXFn0sbD04jTC2LoNPpUBWGTjAg3UInXA0XwEiItNiuBR%2FqiSAimJdeoCI2%2FxDq71us86Zjt%2FXcMuldZuetmAJ5qKAUbD6t9AeL1VLtliPSHjlyTG%2BSl5tU37%2FhEynJc90jIVYYL1GW%2FSDJLbzCo0fSSRks%2BpNZOquZuMCCaoF%2FeF4LF7e3PEevgauEio%2BzR9M6Z2qoF0Nt87bbFYji8MSLNSQRwUdrDgkG7mBIi1re3YgbiQxrgUJLhGsVPouG75gsqHBq8usngjzJnGIeELW0whURduEFRXfXTsKa6NedDBokaK7wzQJVJJY7kdR7j7NfJgXCvfItHjPSBCAY%2FV8Z8it7cqI6Yrm5yi0tvn1Tyc%3D"
                                                                                                                style="color:#1a1a1a!important;text-decoration:none!important;word-wrap:break-word;line-height:15px;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Karla&#39;;font-size:15px;font-weight:700;text-transform:none;text-align:center;display:block;background-color:#ffffff;border-radius:1px;padding:13px 33px;border:2px solid #1a1a1a"
                                                                                                                target="_blank"><span
                                                                                                                    style="line-height:15px;color:#1a1a1a;font-weight:700;text-decoration:none;letter-spacing:0.5px"><span
                                                                                                                        style="line-height:15px;color:#1a1a1a;font-weight:700;text-decoration:none;letter-spacing:0.5px">Glue
                                                                                                                        Store
                                                                                                                        Returns
                                                                                                                        Policy</span></span></a>
                                                                                                        </th>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                        </th>
                                                                                    </tr>

                                                                                </tbody>
                                                                            </table>
                                                                        </th>
                                                                    </tr>

                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>


                                            <table id="m_-2334459430010600387section-footer" border="0" width="100%"
                                                cellpadding="0" cellspacing="0" align="center"
                                                style="min-width:100%;direction:ltr" role="presentation" bgcolor="#1a1a1a">
                                                <tbody>
                                                    <tr align="center">
                                                        <td style="padding-top:22px;padding-bottom:22px" align="center"
                                                            bgcolor="#1a1a1a">
                                                            <table border="0" width="100%" cellpadding="0" cellspacing="0"
                                                                align="center"
                                                                style="min-width:100%;direction:ltr;text-align:center"
                                                                role="presentation">
                                                                <tbody>
                                                                    <tr align="center">
                                                                        <th align="center" bgcolor="#1a1a1a">
                                                                            <table border="0" width="100%" cellpadding="0"
                                                                                cellspacing="0" role="presentation"
                                                                                style="direction:ltr;text-align:center">
                                                                            </table>
                                                                        </th>
                                                                    </tr>
                                                                    <tr align="center">
                                                                        <th align="center" bgcolor="#1a1a1a">
                                                                            <table border="0" width="100%" cellpadding="0"
                                                                                cellspacing="0" role="presentation"
                                                                                style="direction:ltr;text-align:center">

                                                                                <tbody>
                                                                                    <tr align="center">
                                                                                        <th width="100%"
                                                                                            style="font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Karla&#39;;font-size:14px;line-height:22px;font-weight:400;color:#777777;text-transform:none;padding-bottom:22px"
                                                                                            align="center"
                                                                                            bgcolor="#1a1a1a">
                                                                                            <a href="https://www.gluestore.com.au/_t/c/A1030004-179FF8A69851CE20-18FE78AF?l=AABU7Dt8M%2FGVg6KViFwvNtvapEH47c%2BvYUNGfzxKNeJirhtqILUcCR5DPDGQvwbRuEmpJr8TjwxBDUvsyrHSZDnKdz5V6e8e%2FpjBVeaE0Rn74T1fy2wVfmZtUeHEkT2YqEvzNk9RWS2s%2BFiz0V0YQ1wxvp3PfXbBpSD75qAJdONMtIc414ZNHxNxlGV8KHCjVhZRo2s%2Fu4c8wq%2Ffs7mOA6AlBBugBWyypfTUzol%2FQzCawRDAzjO21vhrIP9PKLIuO2NEtYY3TxV4ciDIN%2FpfK%2B502cjlKuZClCRepBzD%2Bv9eswF1gfaac%2B4IsCxQ0ddA%2BqjOYMm5E7ylbXJ0icCV3S3X5DA%2BR2XTz5rjP%2FN%2FCcBNqO%2FTeuXZx25QwxfhqdjkPmsnyJclH5iGNYw%3D&amp;c=AAAByvIKcNB0UzR6nEWTj5EBqXDGFjkOVaxf%2BqCRQeq%2FBPmTqpIPzbTNVPGNBsFLf8OWal6Do8%2BbnqbvyUNyisJay7kYXAOdmMvWZkz4tDzz%2F3NS%2F9ySCPdXFn0sbD04jTC2LoNPpUBWGTjAg3UInXA0XwEiItNiuBR%2FqiSAimJdeoCI2%2FxDq71us86Zjt%2FXcMuldZuetmAJ5qKAUbD6t9AeL1VLtliPSHjlyTG%2BSl5tU37%2FhEynJc90jIVYYL1GW%2FSDJLbzCo0fSSRks%2BpNZOquZuMCCaoF%2FeF4LF7e3PEevgauEio%2BzR9M6Z2qoF0Nt87bbFYji8MSLNSQRwUdrDgkG7mBIi1re3YgbiQxrgUJLhGsVPouG75gsqHBq8usngjzJnGIeELW0whURduEFRXfXTsKa6NedDBokaK7wzQJVJJY7kdR7j7NfJgXCvfItHjPSBCAY%2FV8Z8it7cqI6Yrm5yi0tvn1Tyc%3D"
                                                                                                style="color:#ffffff;text-decoration:none!important;font-size:14px;font-weight:400;text-transform:none;text-align:center"
                                                                                                target="_blank">gluestore.com.au</a>
                                                                                        </th>
                                                                                    </tr>


                                                                                    <tr align="center">
                                                                                        <th width="100%"
                                                                                            style="font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Karla&#39;;font-size:14px;line-height:22px;font-weight:400;color:#777777;text-transform:none;padding-left:22px;padding-right:22px"
                                                                                            align="center"
                                                                                            bgcolor="#1a1a1a">
                                                                                            <p style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Karla&#39;;font-size:14px;line-height:22px;font-weight:400;text-transform:none;color:#777777;margin:0"
                                                                                                align="center">
                                                                                                Accent
                                                                                                Lifestyle
                                                                                                Pty
                                                                                                Ltd
                                                                                                trading
                                                                                                as
                                                                                                Glue
                                                                                                Store
                                                                                            </p>
                                                                                            <p style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Karla&#39;;font-size:14px;line-height:22px;font-weight:400;text-transform:none;color:#777777;margin:11px 0 0"
                                                                                                align="center">
                                                                                                ABN
                                                                                                79
                                                                                                636
                                                                                                815
                                                                                                284
                                                                                            </p>
                                                                                            <p style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Karla&#39;;font-size:14px;line-height:22px;font-weight:400;text-transform:none;color:#777777;margin:11px 0 0"
                                                                                                align="center">
                                                                                                L21
                                                                                                /
                                                                                                59
                                                                                                Goulburn
                                                                                                St,
                                                                                                Haymarket,
                                                                                                NSW
                                                                                                2000
                                                                                            </p>
                                                                                            <p style="direction:ltr;font-family:-apple-system,BlinkMacSystemFont,&#39;Segoe UI&#39;,Arial,&#39;Karla&#39;;font-size:14px;line-height:22px;font-weight:400;text-transform:none;color:#777777;margin:11px 0 0"
                                                                                                align="center">
                                                                                                Copyright
                                                                                                ©
                                                                                                2025<br
                                                                                                    style="text-align:center">
                                                                                            </p>
                                                                                        </th>
                                                                                    </tr>

                                                                                </tbody>
                                                                            </table>
                                                                        </th>
                                                                    </tr>
                                                                    <tr align="center">
                                                                        <th height="1" border="0"
                                                                            style="height:1px;line-height:1px;font-size:1px;padding:0"
                                                                            align="center" bgcolor="#1a1a1a">
                                                                            <img id="m_-2334459430010600387open-image"
                                                                                src="https://www.gluestore.com.au/tools/emails/open/order-confirmation/1"
                                                                                alt="" width="1" height="1" border="0"
                                                                                style="text-align:center">
                                                                        </th>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>

                                        </th>
                                    </tr>
                                </tbody>
                            </table>
                        </center>
                    </th>
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
