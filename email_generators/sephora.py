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
    msg['From'] = formataddr((f'Sephora', sender_email))
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
    "Please enter the image url (MUST BE FROM SEPHORA SITE):",
    "Please enter the product name (Valentino Donna Born in Roma):",
    "Please enter the item number (2541399):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o primeiro nome do cliente (Juggy):",
    "Por favor, insira a URL da imagem (DEVE SER DO SITE DA SEPHORA):",
    "Por favor, insira o nome do produto (Valentino Donna Born in Roma):",
    "Por favor, insira o número do item (2541399):",
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
    part1 = f'#'
    part2 = random.randint(11111111111, 99999999999)  # Random 10-digit number

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
    recipient_email = f'{user_inputs[4]}'
    subject = f"Get excited: Your order {order_num} is almost here!"
    html_template = f"""
        <div style="background-color:rgb(243,243,243)">
        <div style="background-color:rgb(243,243,243)">





            <div style="background:repeat rgb(255,255,255);margin:0px auto;max-width:600px">

                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                    style="background:repeat rgb(255,255,255);width:100%">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:0px;text-align:center">


                                <div class="m_7172884481085391228mj-column-per-100 m_7172884481085391228mobile-padding-5-10"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">

                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="vertical-align:top;padding:0px 40px">

                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                        width="100%">

                                                        <tbody>
                                                            <tr>
                                                                <td align="center" class="m_7172884481085391228mobile-8"
                                                                    style="font-size:0px;padding:10px 0px;word-break:break-word">

                                                                    <div
                                                                        style="font-family:Arial,Helvetica,sans-serif;font-size:8px;font-weight:500;letter-spacing:0px;line-height:14px;text-align:center;text-decoration:none;text-transform:none;color:rgb(0,0,0)">
                                                                        Your beauty’s so close</div>

                                                                </td>
                                                            </tr>

                                                        </tbody>
                                                    </table>

                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>

                                </div>


                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>





            <div style="background:repeat rgb(255,255,255);margin:0px auto;max-width:600px">

                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                    style="background:repeat rgb(255,255,255);width:100%">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:0px;text-align:center">


                                <div class="m_7172884481085391228mj-column-per-100 m_7172884481085391228mobile-padding-0"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">

                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="vertical-align:top;padding:0px">

                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                        width="100%">

                                                        <tbody>
                                                            <tr>
                                                                <td align="center"
                                                                    style="font-size:0px;padding:0px;word-break:break-word">

                                                                    <table border="0" cellpadding="0" cellspacing="0"
                                                                        role="presentation"
                                                                        style="border-collapse:collapse;border-spacing:0px"
                                                                        class="m_7172884481085391228mj-full-width-mobile">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td style="width:600px"
                                                                                    class="m_7172884481085391228mj-full-width-mobile">

                                                                                    <a href=""
                                                                                        target="_blank">

                                                                                        <img alt="Sephora" height="auto"
                                                                                            src="https://narvar-freighter-prod01.s3.us-west-2.amazonaws.com/sephora/7572f10f-7bc0-41f4-babd-6e42e250a1c3"
                                                                                            style="border: 0px; display: block; outline: currentcolor; text-decoration: none; height: auto; width: 100%; font-size: 13px;"
                                                                                            width="600">

                                                                                    </a>

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


                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>





            <div style="background:repeat rgb(255,255,255);margin:0px auto;max-width:600px">

                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                    style="background:repeat rgb(255,255,255);width:100%">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:0px;text-align:center">


                                <div class="m_7172884481085391228mj-column-per-100 m_7172884481085391228mobile-padding-0"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">

                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="vertical-align:top;padding:0px 40px">

                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                        width="100%">

                                                        <tbody>
                                                            <tr>
                                                                <td style="font-size:0px;word-break:break-word">




                                                                    <div style="height:20px">
                                                                         
                                                                    </div>




                                                                </td>
                                                            </tr>

                                                        </tbody>
                                                    </table>

                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>

                                </div>


                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>





            <div style="background:repeat rgb(255,255,255);margin:0px auto;max-width:600px">

                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                    style="background:repeat rgb(255,255,255);width:100%">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:0px;text-align:center">


                                <div class="m_7172884481085391228mj-column-per-100 m_7172884481085391228mobile-padding"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">

                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="vertical-align:top;padding:0px 40px">

                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                        width="100%">

                                                        <tbody>
                                                            <tr>
                                                                <td align="left"
                                                                    style="font-size:0px;padding:10px 0px;word-break:break-word">

                                                                    <div
                                                                        style="font-family:Helvetica,Arial,sans-serif;font-size:34px;font-style:normal;font-weight:500;letter-spacing:0px;line-height:34px;text-align:left;text-transform:none;color:rgb(0,0,0)">
                                                                        Arriving soon!</div>

                                                                </td>
                                                            </tr>

                                                        </tbody>
                                                    </table>

                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>

                                </div>


                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>





            <div style="background:repeat rgb(255,255,255);margin:0px auto;max-width:600px">

                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                    style="background:repeat rgb(255,255,255);width:100%">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:0px;text-align:center">


                                <div class="m_7172884481085391228mj-column-per-100 m_7172884481085391228mobile-padding-0"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">

                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="vertical-align:top;padding:0px 40px">

                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                        width="100%">

                                                        <tbody>
                                                            <tr>
                                                                <td style="font-size:0px;word-break:break-word">




                                                                    <div style="height:20px">
                                                                         
                                                                    </div>




                                                                </td>
                                                            </tr>

                                                        </tbody>
                                                    </table>

                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>

                                </div>


                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>





            <div class="m_7172884481085391228mobile-padding"
                style="background:repeat rgb(255,255,255);margin:0px auto;max-width:600px">

                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                    style="background:repeat rgb(255,255,255);width:100%">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:0px 40px;text-align:center">


                                <div class="m_7172884481085391228mj-column-per-50"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">

                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                        style="vertical-align:top" width="100%">

                                        <tbody>
                                            <tr>
                                                <td align="center"
                                                    class="m_7172884481085391228primary-button m_7172884481085391228mobile-11"
                                                    style="font-size:0px;padding:15px 0px;word-break:break-word">

                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                        style="border-collapse:separate;width:245px;line-height:100%">
                                                        <tbody>
                                                            <tr>
                                                                <td align="center" bgcolor="#FFFFFF" role="presentation"
                                                                    style="border:1px solid rgb(204,204,204);border-radius:0px;font-style:normal;height:40px;background:repeat rgb(255,255,255)"
                                                                    valign="middle">
                                                                    <a href=""
                                                                        style="display:inline-block;width:243px;background:repeat rgb(255,255,255);font-family:Helvetica,Arial,sans-serif;font-size:18px;font-style:normal;font-weight:700;line-height:120%;margin:0px;text-decoration:none;text-transform:none;padding:10px 0px;border-radius:0px;color:rgb(0,0,0)"
                                                                        target="_blank">
                                                                        TRACK YOUR ORDER ►
                                                                    </a>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>

                                                </td>
                                            </tr>

                                        </tbody>
                                    </table>

                                </div>



                                <div class="m_7172884481085391228mj-column-per-50"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">

                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                        style="vertical-align:top" width="100%">

                                        <tbody>
                                            <tr>
                                                <td align="center"
                                                    class="m_7172884481085391228primary-button m_7172884481085391228mobile-11"
                                                    style="font-size:0px;padding:15px 0px;word-break:break-word">

                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                        style="border-collapse:separate;width:245px;line-height:100%">
                                                        <tbody>
                                                            <tr>
                                                                <td align="center" bgcolor="#FFFFFF" role="presentation"
                                                                    style="border:1px solid rgb(204,204,204);border-radius:0px;font-style:normal;height:40px;background:repeat rgb(255,255,255)"
                                                                    valign="middle">
                                                                    <a href=""
                                                                        style="display:inline-block;width:243px;background:repeat rgb(255,255,255);font-family:Helvetica,Arial,sans-serif;font-size:18px;font-style:normal;font-weight:700;line-height:120%;margin:0px;text-decoration:none;text-transform:none;padding:10px 0px;border-radius:0px;color:rgb(0,0,0)"
                                                                        target="_blank">
                                                                        GET ORDER UPDATES ►
                                                                    </a>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>

                                                </td>
                                            </tr>

                                        </tbody>
                                    </table>

                                </div>


                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>





            <div style="background:repeat rgb(255,255,255);margin:0px auto;max-width:600px">

                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                    style="background:repeat rgb(255,255,255);width:100%">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:0px;text-align:center">


                                <div class="m_7172884481085391228mj-column-per-100 m_7172884481085391228mobile-padding-0"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">

                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="vertical-align:top;padding:0px 40px">

                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                        width="100%">

                                                        <tbody>
                                                            <tr>
                                                                <td style="font-size:0px;word-break:break-word">




                                                                    <div style="height:25px">
                                                                         
                                                                    </div>




                                                                </td>
                                                            </tr>

                                                        </tbody>
                                                    </table>

                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>

                                </div>


                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>





            <div style="background:repeat rgb(255,255,255);margin:0px auto;max-width:600px">

                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                    style="background:repeat rgb(255,255,255);width:100%">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:0px;text-align:center">


                                <div class="m_7172884481085391228mj-column-per-100 m_7172884481085391228mobile-padding-5-10"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">

                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="vertical-align:top;padding:0px 40px">

                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                        width="100%">

                                                        <tbody>
                                                            <tr>
                                                                <td align="left" class="m_7172884481085391228mobile-14"
                                                                    style="font-size:0px;padding:10px 0px;word-break:break-word">

                                                                    <div
                                                                        style="font-family:Helvetica,Arial,sans-serif;font-size:16px;font-weight:500;letter-spacing:0px;line-height:24px;text-align:left;text-decoration:none;text-transform:none;color:rgb(10,10,10)">
                                                                        Thank you for shopping with us, {user_inputs[0]}! Just a heads
                                                                        up that your
                                                                        order {order_num} is arriving soon.</div>

                                                                </td>
                                                            </tr>

                                                        </tbody>
                                                    </table>

                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>

                                </div>


                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>





            <div style="background:repeat rgb(255,255,255);margin:0px auto;max-width:600px">

                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                    style="background:repeat rgb(255,255,255);width:100%">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:0px;text-align:center">


                                <div class="m_7172884481085391228mj-column-per-100 m_7172884481085391228mobile-padding-0"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">

                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="vertical-align:top;padding:0px 40px">

                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                        width="100%">

                                                        <tbody>
                                                            <tr>
                                                                <td style="font-size:0px;word-break:break-word">




                                                                    <div style="height:35px">
                                                                         
                                                                    </div>




                                                                </td>
                                                            </tr>

                                                        </tbody>
                                                    </table>

                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>

                                </div>


                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>





            <div class="m_7172884481085391228mobile-padding"
                style="background:repeat rgb(255,255,255);margin:0px auto;max-width:600px">

                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                    style="background:repeat rgb(255,255,255);width:100%">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:0px 30px 5px;text-align:center">


                                <div class="m_7172884481085391228mj-column-per-100"
                                    style="font-size:0px;line-height:0;text-align:left;display:inline-block;width:100%;direction:ltr">


                                    <div class="m_7172884481085391228mj-column-per-76"
                                        style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:76%">

                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                            <tbody>
                                                <tr>
                                                    <td
                                                        style="border-bottom-width:2px;border-bottom-style:solid;border-top-width:5px;border-top-style:solid;vertical-align:top;padding:0px;border-top-color:rgb(204,204,204);border-bottom-color:rgb(204,204,204)">

                                                        <table border="0" cellpadding="0" cellspacing="0"
                                                            role="presentation" width="100%">

                                                            <tbody>
                                                                <tr>
                                                                    <td align="left" class="m_7172884481085391228mobile-12"
                                                                        style="font-size:0px;padding:5px 25px;word-break:break-word">

                                                                        <div
                                                                            style="font-family:Helvetica;font-size:14px;font-weight:700;line-height:18px;text-align:left;color:rgb(0,0,0)">
                                                                            Item</div>

                                                                    </td>
                                                                </tr>

                                                            </tbody>
                                                        </table>

                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>

                                    </div>



                                    <div class="m_7172884481085391228mj-column-per-24"
                                        style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:24%">

                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                            <tbody>
                                                <tr>
                                                    <td
                                                        style="border-bottom-width:2px;border-bottom-style:solid;border-top-width:5px;border-top-style:solid;vertical-align:top;padding:0px;border-top-color:rgb(204,204,204);border-bottom-color:rgb(204,204,204)">

                                                        <table border="0" cellpadding="0" cellspacing="0"
                                                            role="presentation" width="100%">

                                                            <tbody>
                                                                <tr>
                                                                    <td align="center"
                                                                        class="m_7172884481085391228mobile-12"
                                                                        style="font-size:0px;padding:5px 25px;word-break:break-word">

                                                                        <div
                                                                            style="font-family:Helvetica;font-size:14px;font-weight:700;line-height:18px;text-align:center;color:rgb(0,0,0)">
                                                                            Qty</div>

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


                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>





            <div class="m_7172884481085391228mobile-padding-0-10"
                style="background:repeat rgb(255,255,255);margin:0px auto;max-width:600px">

                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                    style="background:repeat rgb(255,255,255);width:100%">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:0px 30px;text-align:center">


                                <div class="m_7172884481085391228mj-column-per-100"
                                    style="font-size:0px;line-height:0;text-align:left;display:inline-block;width:100%;direction:ltr">


                                    <div class="m_7172884481085391228mj-column-per-22 m_7172884481085391228mobile-width-35-percent"
                                        style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:22%">

                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                            <tbody>
                                                <tr>
                                                    <td style="vertical-align:top;padding:12px 0px">

                                                        <table border="0" cellpadding="0" cellspacing="0"
                                                            role="presentation" width="100%">

                                                            <tbody>
                                                                <tr>
                                                                    <td align="left"
                                                                        style="font-size:0px;padding:0px 12px 0px 0px;word-break:break-word">

                                                                        <table border="0" cellpadding="0" cellspacing="0"
                                                                            role="presentation"
                                                                            style="border-collapse:collapse;border-spacing:0px">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="width:94px">

                                                                                        <a href=""
                                                                                            target="_blank">

                                                                                            <img height="auto"
                                                                                                src="{user_inputs[1]}"
                                                                                                style="border: 0px; display: block; outline: currentcolor; text-decoration: none; height: auto; width: 100%; font-size: 13px;"
                                                                                                width="94">

                                                                                        </a>

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



                                    <div class="m_7172884481085391228mj-column-per-54 m_7172884481085391228mobile-width-40-percent"
                                        style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:54%">

                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                            <tbody>
                                                <tr>
                                                    <td style="vertical-align:top;padding:20px 0px">

                                                        <table border="0" cellpadding="0" cellspacing="0"
                                                            role="presentation" width="100%">

                                                            <tbody>
                                                                <tr>
                                                                    <td align="left" class="m_7172884481085391228mobile-12"
                                                                        style="font-size:0px;padding:0px;word-break:break-word">

                                                                        <div
                                                                            style="font-family:Helvetica;font-size:12px;font-weight:700;line-height:18px;text-align:left;color:rgb(10,10,10)">
                                                                            {user_inputs[2]}</div>

                                                                    </td>
                                                                </tr>

                                                                <tr>
                                                                    <td align="left" class="m_7172884481085391228mobile-12"
                                                                        style="font-size:0px;padding:8px 0px 0px;word-break:break-word">

                                                                        <div
                                                                            style="font-family:Helvetica;font-size:12px;font-weight:400;line-height:18px;text-align:left;color:rgb(0,0,0)">
                                                                            ITEM {user_inputs[3]}</div>

                                                                    </td>
                                                                </tr>

                                                            </tbody>
                                                        </table>

                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>

                                    </div>



                                    <div class="m_7172884481085391228mj-column-per-24 m_7172884481085391228mobile-width-25-percent"
                                        style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:24%">

                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                            <tbody>
                                                <tr>
                                                    <td style="vertical-align:top;padding:20px 0px">

                                                        <table border="0" cellpadding="0" cellspacing="0"
                                                            role="presentation" width="100%">

                                                            <tbody>
                                                                <tr>
                                                                    <td align="right" class="m_7172884481085391228mobile-12"
                                                                        style="font-size:0px;padding:0px;word-break:break-word">

                                                                        <div
                                                                            style="font-family:Helvetica;font-size:12px;font-weight:400;line-height:18px;text-align:right;color:rgb(77,77,77)">
                                                                        </div>

                                                                    </td>
                                                                </tr>

                                                                <tr>
                                                                    <td align="center"
                                                                        class="m_7172884481085391228mobile-12"
                                                                        style="font-size:0px;padding:0px;word-break:break-word">

                                                                        <div
                                                                            style="font-family:Helvetica;font-size:12px;font-weight:400;line-height:18px;text-align:center;color:rgb(77,77,77)">
                                                                            1</div>

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


                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>





            <div class="m_7172884481085391228mobile-padding-0"
                style="background:repeat rgb(255,255,255);margin:0px auto;max-width:600px">

                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                    style="background:repeat rgb(255,255,255);width:100%">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:0px 30px 30px;text-align:center">


                                <div class="m_7172884481085391228mj-column-per-100 m_7172884481085391228mobile-padding-0-10"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">

                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="vertical-align:top;padding:0px">

                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                        width="100%">

                                                        <tbody>
                                                            <tr>
                                                                <td style="font-size:0px;padding:0px;word-break:break-word">

                                                                    <p
                                                                        style="border-top-width:2px;border-top-style:solid;font-size:1px;margin:0px auto;width:100%;border-top-color:rgb(204,204,204)">
                                                                    </p>




                                                                </td>
                                                            </tr>

                                                        </tbody>
                                                    </table>

                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>

                                </div>


                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>

            <div style="background:repeat rgb(255,255,255);margin:0px auto;max-width:600px">

                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                    style="background:repeat rgb(255,255,255);width:100%">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:0px;text-align:center">


                                <div class="m_7172884481085391228mj-column-per-100 m_7172884481085391228mobile-padding"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">

                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="vertical-align:top;padding:0px 40px">

                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                        width="100%">

                                                        <tbody>
                                                            <tr>
                                                                <td align="center"
                                                                    class="m_7172884481085391228primary-button m_7172884481085391228mobile-11"
                                                                    style="font-size:0px;padding:10px 0px;word-break:break-word">

                                                                    <table border="0" cellpadding="0" cellspacing="0"
                                                                        role="presentation"
                                                                        style="border-collapse:separate;width:70%;line-height:100%">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td align="center" bgcolor="#ffffff"
                                                                                    role="presentation"
                                                                                    style="border:1px solid rgb(204,204,204);border-radius:0px;height:75px;background:repeat rgb(255,255,255)"
                                                                                    valign="middle">
                                                                                    <a href=""
                                                                                        style="display:inline-block;background:repeat rgb(255,255,255);font-family:Helvetica,Arial,sans-serif;font-size:20px;font-weight:600;line-height:120%;letter-spacing:0px;margin:0px;text-decoration:none;text-transform:none;padding:10px 0px;border-radius:0px;color:rgb(0,0,0)"
                                                                                        target="_blank">
                                                                                        SEE ORDER DETAILS ►
                                                                                    </a>
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


                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>













            <div style="background:repeat rgb(255,255,255);margin:0px auto;max-width:600px">

                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                    style="background:repeat rgb(255,255,255);width:100%">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:0px;text-align:center">


                                <div class="m_7172884481085391228mj-column-per-100 m_7172884481085391228mobile-padding-0"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">

                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="vertical-align:top;padding:0px 40px">

                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                        width="100%">

                                                        <tbody>
                                                            <tr>
                                                                <td style="font-size:0px;word-break:break-word">




                                                                    <div style="height:45px">
                                                                         
                                                                    </div>




                                                                </td>
                                                            </tr>

                                                        </tbody>
                                                    </table>

                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>

                                </div>


                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>





            <div style="background:repeat rgb(255,255,255);margin:0px auto;max-width:600px">

                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                    style="background:repeat rgb(255,255,255);width:100%">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:0px;text-align:center">


                                <div class="m_7172884481085391228mj-column-per-100 m_7172884481085391228mobile-padding-0"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">

                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="vertical-align:top;padding:0px">

                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                        width="100%">

                                                        <tbody>
                                                            <tr>
                                                                <td align="center"
                                                                    style="font-size:0px;padding:0px;word-break:break-word">

                                                                    <table border="0" cellpadding="0" cellspacing="0"
                                                                        role="presentation"
                                                                        style="border-collapse:collapse;border-spacing:0px"
                                                                        class="m_7172884481085391228mj-full-width-mobile">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td style="width:600px"
                                                                                    class="m_7172884481085391228mj-full-width-mobile">

                                                                                    <a href=""
                                                                                        target="_blank">

                                                                                        <img alt="Need Help" height="auto"
                                                                                            src="https://narvar-freighter-prod01.s3.us-west-2.amazonaws.com/sephora/e2b12482-1267-49d6-8b37-fd098d77b079"
                                                                                            style="border: 0px; display: block; outline: currentcolor; text-decoration: none; height: auto; width: 100%; font-size: 13px;"
                                                                                            width="600">

                                                                                    </a>

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


                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>





            <div style="background:repeat rgb(255,255,255);margin:0px auto;max-width:600px">

                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                    style="background:repeat rgb(255,255,255);width:100%">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:0px;text-align:center">


                                <div class="m_7172884481085391228mj-column-per-100 m_7172884481085391228mobile-padding-0"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">

                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="vertical-align:top;padding:0px">

                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                        width="100%">

                                                        <tbody>
                                                            <tr>
                                                                <td align="center"
                                                                    style="font-size:0px;padding:0px;word-break:break-word">

                                                                    <table border="0" cellpadding="0" cellspacing="0"
                                                                        role="presentation"
                                                                        style="border-collapse:collapse;border-spacing:0px"
                                                                        class="m_7172884481085391228mj-full-width-mobile">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td style="width:600px"
                                                                                    class="m_7172884481085391228mj-full-width-mobile">

                                                                                    <a href=""
                                                                                        target="_blank">

                                                                                        <img alt="Sign Up for Text Udpates"
                                                                                            height="auto"
                                                                                            src="https://narvar-freighter-prod01.s3.us-west-2.amazonaws.com/sephora/57365c7a-7d34-4342-9e1f-802358d81341"
                                                                                            style="border: 0px; display: block; outline: currentcolor; text-decoration: none; height: auto; width: 100%; font-size: 13px;"
                                                                                            width="600">

                                                                                    </a>

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


                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>





            <div style="background:repeat rgb(255,255,255);margin:0px auto;max-width:600px">

                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                    style="background:repeat rgb(255,255,255);width:100%">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:0px;text-align:center">


                                <div class="m_7172884481085391228mj-column-per-100 m_7172884481085391228mobile-padding-0"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">

                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="vertical-align:top;padding:0px">

                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                        width="100%">

                                                        <tbody>
                                                            <tr>
                                                                <td align="center"
                                                                    style="font-size:0px;padding:0px;word-break:break-word">

                                                                    <table border="0" cellpadding="0" cellspacing="0"
                                                                        role="presentation"
                                                                        style="border-collapse:collapse;border-spacing:0px"
                                                                        class="m_7172884481085391228mj-full-width-mobile">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td style="width:600px"
                                                                                    class="m_7172884481085391228mj-full-width-mobile">

                                                                                    <a href=""
                                                                                        target="_blank">

                                                                                        <img alt="We Belong to Something Beautiful"
                                                                                            height="auto"
                                                                                            src="https://freighter-prod01.narvar.com/sephora/cb0227d7-ef71-4c71-96b7-96cd7bff95d8"
                                                                                            style="border: 0px; display: block; outline: currentcolor; text-decoration: none; height: auto; width: 100%; font-size: 13px;"
                                                                                            width="600">

                                                                                    </a>

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


                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>





            <div style="background:repeat rgb(0,0,0);margin:0px auto;max-width:600px">

                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                    style="background:repeat rgb(0,0,0);width:100%">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:0px;text-align:center">


                                <div class="m_7172884481085391228mj-column-per-100 m_7172884481085391228mobile-padding-15-10"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">

                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="vertical-align:top;padding:0px 40px">

                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                        width="100%">

                                                        <tbody>
                                                            <tr>
                                                                <td align="center" class="m_7172884481085391228mobile-10"
                                                                    style="font-size:0px;padding:30px 0px 45px;word-break:break-word">

                                                                    <div
                                                                        style="font-family:Arial,Helvetica,sans-serif;font-size:10px;font-weight:500;letter-spacing:0px;line-height:14px;text-align:center;text-decoration:none;text-transform:none;color:rgb(204,204,204)">
                                                                        <a href=""
                                                                            style="font-family:Arial,Helvetica,sans-serif;color:rgb(204,204,204)"
                                                                            target="_blank">Privacy Policy</a> |
                                                                        <a href=""
                                                                            style="font-family:Arial,Helvetica,sans-serif;color:rgb(204,204,204)"
                                                                            target="_blank">Contact Us</a>
                                                                        <br>
                                                                        <br>© 2025 Sephora USA, Inc.,
                                                                        <a
                                                                            style="font-family:Arial,Helvetica,sans-serif;color:rgb(204,204,204)">350
                                                                            Mission Street, Floor 7 San Francisco, CA
                                                                            94105</a>. All rights reserved.
                                                                    </div>

                                                                </td>
                                                            </tr>

                                                        </tbody>
                                                    </table>

                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>

                                </div>


                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>
    """

    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
