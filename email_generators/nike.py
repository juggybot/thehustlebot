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
    msg['From'] = formataddr((f'Nike', sender_email))
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
    "Please enter the customer address (52 Lesly Valleys, East Norma, Great Britain QH35 6AM):",
    "Please enter the customer first name (Juggy):",
    "Please enter the image url (Must be Nike image link):",
    "Please enter the product name (Nike Air Max Dn Older Kids' Shoes):",
    "Please enter the product price (WITHOUT THE $ SIGN):",
    "Please enter the product size (UK 1.5 M):",
    "Please enter the order date (Apr 11, 2024):",
    "Please enter the delivery date (Apr 21, 2024):",
    "Please enter the postage total (WITHOUT THE $ SIGN):",
    "Please enter the tax total (WITHOUT THE $ SIGN):",
    "Please enter the order total (WITHOUT THE $ SIGN):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira o endereço do cliente (52 Lesly Valleys, East Norma, Grã-Bretanha QH35 6AM):",
    "Por favor, insira o primeiro nome do cliente (Juggy):",
    "Por favor, insira a URL da imagem (Deve ser um link de imagem da Nike):",
    "Por favor, insira o nome do produto (Nike Air Max Dn Older Kids' Shoes):",
    "Por favor, insira o preço do produto (SEM O SÍMBOLO $):",
    "Por favor, insira o tamanho do produto (UK 1.5 M):",
    "Por favor, insira a data do pedido (11 de abril de 2024):",
    "Por favor, insira a data de entrega (21 de abril de 2024):",
    "Por favor, insira o total do frete (SEM O SÍMBOLO $):",
    "Por favor, insira o total de impostos (SEM O SÍMBOLO $):",
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
    part1 = "C"
    part2 = random.randint(10000000000, 99999999999)  # Random 11-digit number

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
    subject = f"Thanks for your order (#{order_num})"

    html_template=f"""
        <center>
                <table class="m_-2774923715066548899maintable" width="100%" align="center" cellspacing="0" cellpadding="0"
                    border="0" style="padding:0px;font-size:0px" role="presentation">
                    <tbody>
                        <tr>
                            <td class="m_-2774923715066548899sidebar"
                                style="font-size:0px;line-height:1px;overflow:hidden!important"> </td>
                            <td class="m_-2774923715066548899outershell" width="642" valign="top" align="center"
                                style="width:642px;border:1px solid rgb(229,229,229);max-width:642px!important;min-width:320px!important">
                                <table class="m_-2774923715066548899innershell" bgcolor="#FFFFFF" align="center"
                                    width="100%" valign="top" cellpadding="0" cellspacing="0" border="0"
                                    style="border:medium;width:100%;padding:0px;border-collapse:collapse;min-width:320px!important;max-width:640px!important"
                                    role="presentation">
                                    <tbody>
                                        <tr>
                                            <td class="m_-2774923715066548899container" align="center">
                                                <table align="center" width="100%" cellspacing="0" cellpadding="0"
                                                    border="0" style="width:100%">
                                                    <tbody>
                                                        <tr>
                                                            <td align="center"
                                                                style="border-bottom-width:1px;border-bottom-style:solid;border-bottom-color:rgb(229,229,229)">
                                                                <table width="100%" style="border-spacing:0px"
                                                                    role="presentation">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td bgcolor="#F7F7F7" align="center"
                                                                                style="padding:0px">
                                                                                <table align="center" width="94%"
                                                                                    valign="top" cellpadding="0"
                                                                                    cellspacing="0" border="0"
                                                                                    style="margin:0px auto;max-width:100%;min-width:320px;border:medium;border-collapse:collapse"
                                                                                    role="presentation">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td align="left" valign="middle"
                                                                                                style="padding:20px;font-size:0px">
                                                                                                <table width="100%"
                                                                                                    role="presentation">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td valign="top"
                                                                                                                align="left"
                                                                                                                style="font-family:Helvetica,Arial,sans-serif;font-size:14px;font-weight:bold;line-height:26px;padding:0px;color:rgb(17,17,17)">
                                                                                                                Shipping to:
                                                                                                                {user_inputs[0]}
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td valign="top"
                                                                                                                align="left"
                                                                                                                style="font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:26px;color:rgb(102,102,102)">
                                                                                                                <p
                                                                                                                    style="font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:26px;margin:0px;color:rgb(102,102,102)">
                                                                                                                    <span
                                                                                                                        class="m_-2774923715066548899address"
                                                                                                                        style="font-family:Helvetica,Arial,sans-serif">01352
                                                                                                                        {user_inputs[1]}</span>
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
                                                                        <tr>
                                                                            <td bgcolor="#ffffff" align="center"
                                                                                style="border-top-width:1px;border-top-style:solid;padding:0px;border-top-color:rgb(229,229,229)">
                                                                                <div
                                                                                    style="line-height:0px;padding:0px;width:0px;height:0px;display:none!important">
                                                                                </div>
                                                                                <table width="100%" role="presentation">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td style="text-align:center;font-size:14px;padding:50px 0px 20px"
                                                                                                align="center">
                                                                                                <table
                                                                                                    style="border-spacing:0px;min-width:275px;width:65%;margin:0px auto"
                                                                                                    role="presentation">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td style="padding:0px 0px 30px;text-align:center"
                                                                                                                align="left">
                                                                                                                <a href="http://click.official.nike.com/?qs=1d020c5277199bbf5a82305502c167d231dbcdf9b39e14d5c5e3d6623d07cd59129a39e3cceea7c21db17ebf57241ce11b98c13c85a7b0dd230367bd49aa6d87"
                                                                                                                    target="_blank"><img
                                                                                                                        style="border: 0px;"
                                                                                                                        src="http://image.official.nike.com/lib/fe9815737560077476/m/3/Swoosh2x.png"
                                                                                                                        width="57"
                                                                                                                        alt="logo"></a>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td style="padding:0px 0px 15px;text-align:center"
                                                                                                                align="left">
                                                                                                                <h1
                                                                                                                    style="font-size:28px;line-height:34px;font-family:Helvetica,Arial,sans-serif;margin:0px;color:rgb(17,17,17)">
                                                                                                                    <span
                                                                                                                        style="font-size:28px;line-height:34px;font-family:'Nike TG',Helvetica,Arial,sans-serif;color:rgb(17,17,17)">Thanks,
                                                                                                                        {user_inputs[2]}!
                                                                                                                        We&#39;re
                                                                                                                        On
                                                                                                                        It.</span>
                                                                                                                </h1>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td style="padding:0px 0px 20px;text-align:center;line-height:26px;font-family:Helvetica,Arial,sans-serif;color:rgb(109,109,109)"
                                                                                                                align="left">
                                                                                                                <span
                                                                                                                    style="font-family:Helvetica,Arial,sans-serif">
                                                                                                                    Your
                                                                                                                    order&#39;s
                                                                                                                    in.
                                                                                                                    We&#39;re
                                                                                                                    working
                                                                                                                    to get
                                                                                                                    it
                                                                                                                    packed
                                                                                                                    up and
                                                                                                                    out the
                                                                                                                    door. We
                                                                                                                    may send
                                                                                                                    your
                                                                                                                    order in
                                                                                                                    more
                                                                                                                    than one
                                                                                                                    shipment,
                                                                                                                    and if
                                                                                                                    we do,
                                                                                                                    we&#39;ll
                                                                                                                    send a
                                                                                                                    shipping
                                                                                                                    confirmation
                                                                                                                    email as
                                                                                                                    each
                                                                                                                    shipment
                                                                                                                    goes
                                                                                                                    out.
                                                                                                                </span>
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
                                                                            <td bgcolor="#ffffff" align="center"
                                                                                style="padding:0px">
                                                                                <table align="center" width="100%"
                                                                                    border="0" cellspacing="0"
                                                                                    cellpadding="0" style="padding:0px">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td bgcolor="#ffffff"
                                                                                                align="center"
                                                                                                style="border-top-width:1px;border-top-style:solid;padding:0px;border-top-color:rgb(229,229,229)">
                                                                                                <table align="center"
                                                                                                    width="94%" valign="top"
                                                                                                    cellpadding="0"
                                                                                                    cellspacing="0"
                                                                                                    border="0"
                                                                                                    style="margin:0px auto;max-width:100%;min-width:320px;border:medium;border-collapse:collapse"
                                                                                                    role="presentation">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td
                                                                                                                style="text-align:center;font-size:14px;padding:20px">
                                                                                                                <table
                                                                                                                    width="100%"
                                                                                                                    role="presentation">
                                                                                                                    <tbody>
                                                                                                                        <tr>
                                                                                                                            <td style="padding:0px;text-align:left;margin:0px"
                                                                                                                                align="left">
                                                                                                                                <span
                                                                                                                                    style="font-size:14px;font-family:Helvetica,Arial,sans-serif;line-height:24px;color:rgb(1,127,7)">Estimated
                                                                                                                                    Delivery
                                                                                                                                    Date
                                                                                                                                    {user_inputs[8]}</span>
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
                                                                                            <td bgcolor="" align="center"
                                                                                                style="padding:0px 0px 40px">
                                                                                                <div class="m_-2774923715066548899ghostdiv"
                                                                                                    style="width:300px;border:medium;display:inline-table;font-size:0px;vertical-align:top;padding:0px!important">
                                                                                                    <table
                                                                                                        class="m_-2774923715066548899container"
                                                                                                        align="center"
                                                                                                        width="100%"
                                                                                                        bgcolor="#FFFFFF"
                                                                                                        valign="top"
                                                                                                        border="0"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        style="font-size:16px;margin:0px;padding:0px;line-height:1.5;border-collapse:collapse;text-align:center;color:white"
                                                                                                        role="presentation">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td>
                                                                                                                    <table
                                                                                                                        style="margin-bottom:10px!important">
                                                                                                                        <tbody>
                                                                                                                            <tr>
                                                                                                                                <td align="center"
                                                                                                                                    valign="top"
                                                                                                                                    style="padding:0px 10px;text-align:center;background-color:rgb(246,244,248)">
                                                                                                                                    <img border="0"
                                                                                                                                        width="280"
                                                                                                                                        height="280"
                                                                                                                                        style="width: 280px; height: 280px; border: medium; border-collapse: collapse; display: block; padding: 0px; background-color: rgb(246, 244, 248);"
                                                                                                                                        src="{user_inputs[3]}"
                                                                                                                                        alt="">
                                                                                                                                </td>
                                                                                                                            </tr>
                                                                                                                        </tbody>
                                                                                                                    </table>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                                <div class="m_-2774923715066548899ghostdiv"
                                                                                                    style="width:280px;border:medium;display:inline-table;font-size:0px;vertical-align:top;padding:0px!important">
                                                                                                    <table width="100%"
                                                                                                        bgcolor="#FFFFFF"
                                                                                                        align="left"
                                                                                                        valign="top"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        style="font-size:16px;margin:0px;padding:0px;line-height:1.5"
                                                                                                        role="presentation">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td
                                                                                                                    style="padding:0px 10px">
                                                                                                                    <table
                                                                                                                        width="100%"
                                                                                                                        border="0"
                                                                                                                        cellspacing="0"
                                                                                                                        cellpadding="0"
                                                                                                                        role="presentation">
                                                                                                                        <tbody>
                                                                                                                            <tr>
                                                                                                                                <td valign="top"
                                                                                                                                    align="left"
                                                                                                                                    style="font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:24px;color:rgb(17,17,17)">
                                                                                                                                    {user_inputs[4]}
                                                                                                                                </td>
                                                                                                                                <td
                                                                                                                                    valign="top">
                                                                                                                                    <table
                                                                                                                                        width="100%"
                                                                                                                                        border="0"
                                                                                                                                        cellspacing="0"
                                                                                                                                        cellpadding="0"
                                                                                                                                        role="presentation">
                                                                                                                                        <tbody>
                                                                                                                                            <tr>
                                                                                                                                                <td valign="top"
                                                                                                                                                    align="right"
                                                                                                                                                    width="75"
                                                                                                                                                    style="white-space:nowrap;word-break:break-all;font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:24px;text-align:right;border:medium;color:rgb(17,17,17)">
                                                                                                                                                    {user_inputs[12]}{user_inputs[5]}
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
                                                                                                                <td valign="top"
                                                                                                                    align="left"
                                                                                                                    style="padding:0px 10px;width:200px;font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:22px;color:rgb(109,109,109)">
                                                                                                                    {user_inputs[6]}
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                            </td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td bgcolor="#ffffff" align="center"
                                                                                style="border-top-width:1px;border-top-style:solid;padding:0px;border-top-color:rgb(229,229,229)">
                                                                                <table width="94%"
                                                                                    style="margin:0px auto;min-width:320px"
                                                                                    role="presentation">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td align="left"
                                                                                                style="padding:20px 0px">
                                                                                                <div class="m_-2774923715066548899ghostdiv"
                                                                                                    style="border:medium;display:inline-table;font-size:0px;vertical-align:top;max-width:213px!important;padding:0px!important">
                                                                                                    <table
                                                                                                        class="m_-2774923715066548899container"
                                                                                                        width="233"
                                                                                                        align="left"
                                                                                                        valign="top"
                                                                                                        border="0"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        style="font-size:14px;margin:0px;padding:0px;line-height:17px;border-collapse:collapse;max-width:213px!important;min-width:213px!important;color:white"
                                                                                                        role="presentation">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td valign="top"
                                                                                                                    align="left"
                                                                                                                    style="padding:20px 0px 0px 20px;font-family:Helvetica,Arial,sans-serif;font-size:14px;font-weight:bold;line-height:26px;color:rgb(17,17,17)">
                                                                                                                    Order
                                                                                                                    Number
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                            <tr>
                                                                                                                <td valign="top"
                                                                                                                    align="left"
                                                                                                                    style="padding:0px 0px 0px 20px;font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:26px;color:rgb(102,102,102)">
                                                                                                                    #{order_num}
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                                <div class="m_-2774923715066548899ghostdiv"
                                                                                                    style="width:100%;border:medium;display:inline-table;font-size:0px;vertical-align:top;max-width:363px!important;padding:0px!important">
                                                                                                    <table
                                                                                                        class="m_-2774923715066548899container"
                                                                                                        width="100%"
                                                                                                        align="left"
                                                                                                        valign="top"
                                                                                                        border="0"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        style="max-width:363px;font-size:14px;margin:0px;padding:0px;line-height:17px;border-collapse:collapse;min-width:320px!important;color:white"
                                                                                                        role="presentation">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td valign="top"
                                                                                                                    width="150"
                                                                                                                    align="left"
                                                                                                                    style="width:150px;padding:20px 0px 0px 20px;font-family:Helvetica,Arial,sans-serif;font-size:14px;font-weight:bold;line-height:26px;color:rgb(17,17,17)">
                                                                                                                    Order
                                                                                                                    Date
                                                                                                                </td>
                                                                                                                <td
                                                                                                                    style="font-size:0px;max-width:40px">
                                                                                                                </td>
                                                                                                                <td valign="top"
                                                                                                                    width="150"
                                                                                                                    align="left"
                                                                                                                    style="width:150px;padding:20px 0px 0px 20px;font-family:Helvetica,Arial,sans-serif;font-size:14px;font-weight:bold;line-height:26px;color:rgb(17,17,17)">
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                            <tr>
                                                                                                                <td valign="top"
                                                                                                                    width="150"
                                                                                                                    align="left"
                                                                                                                    style="padding:0px 0px 20px 20px;font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:26px;color:rgb(102,102,102)">
                                                                                                                    {user_inputs[7]}
                                                                                                                </td>
                                                                                                                <td
                                                                                                                    style="font-size:0px;max-width:40px">
                                                                                                                </td>
                                                                                                                <td valign="top"
                                                                                                                    width="150"
                                                                                                                    align="left"
                                                                                                                    style="padding:0px 0px 20px 20px;font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:26px;color:rgb(102,102,102)">
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                                <div class="m_-2774923715066548899ghostdiv"
                                                                                                    style="width:100%;border:medium;display:inline-table;font-size:0px;vertical-align:top;max-width:100%!important;padding:0px!important">
                                                                                                    <table
                                                                                                        class="m_-2774923715066548899container"
                                                                                                        width="100%"
                                                                                                        align="center"
                                                                                                        valign="top"
                                                                                                        border="0"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        style="max-width:100%;font-size:14px;margin:0px;padding:0px;line-height:17px;border-collapse:collapse;min-width:320px!important;color:white"
                                                                                                        role="presentation">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td align="center"
                                                                                                                    style="padding:20px 0px">
                                                                                                                    <div
                                                                                                                        style="line-height:0px;padding:0px;width:0px;height:0px;display:none!important">
                                                                                                                    </div>
                                                                                                                    <table
                                                                                                                        class="m_-2774923715066548899button"
                                                                                                                        width="225"
                                                                                                                        align="center"
                                                                                                                        style="margin:0px auto;height:40px;width:225px;border:1px solid rgb(141,141,141);border-radius:2px;display:inline-table"
                                                                                                                        role="presentation">
                                                                                                                        <tbody>
                                                                                                                            <tr>
                                                                                                                                <td align="center"
                                                                                                                                    height="40"
                                                                                                                                    style="text-align:center;height:40px;font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:20px;color:rgb(0,0,0)">
                                                                                                                                    ‌<a href="http://click.official.nike.com/?qs=1d020c5277199bbf127ec037e425b76f6c8d0f790f550eab96390af2ded38a4028760854dca092eadceb8d41bd2994cb9740b1a4673ce3283db660b8673403dd"
                                                                                                                                        style="min-width:140px;font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:15px;text-align:center;text-decoration:none;padding:10px 40px;border:1px hidden rgb(255,255,255);display:inline-block;color:rgb(0,0,0)"
                                                                                                                                        target="_blank">
                                                                                                                                        <span
                                                                                                                                            style="font-size:14px;line-height:15px;font-family:'Nike TG',Helvetica,Arial,sans-serif;color:rgb(0,0,0)">
                                                                                                                                            Order
                                                                                                                                            Status
                                                                                                                                        </span>
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
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td bgcolor="#ffffff" align="center"
                                                                                style="border-top-width:1px;border-top-style:solid;padding:0px;border-top-color:rgb(229,229,229)">
                                                                                <table align="center" width="94%"
                                                                                    valign="top" cellpadding="0"
                                                                                    cellspacing="0" border="0"
                                                                                    style="margin:0px auto;max-width:100%;min-width:320px;border:medium;border-collapse:collapse"
                                                                                    role="presentation">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td align="left" valign="middle"
                                                                                                style="padding:0px 20px;font-size:0px">
                                                                                                <table width="100%"
                                                                                                    role="presentation">
                                                                                                    <tbody>
                                                                                                        <tr>
                                                                                                            <td align="center"
                                                                                                                style="font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:24px;padding:40px 0px;color:rgb(109,109,109)">
                                                                                                                <table
                                                                                                                    width="100%"
                                                                                                                    align="center"
                                                                                                                    border="0"
                                                                                                                    cellspacing="0"
                                                                                                                    cellpadding="0"
                                                                                                                    style="padding:0px;margin:0px;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif"
                                                                                                                    role="presentation">
                                                                                                                    <tbody
                                                                                                                        style="font-family:Helvetica,Arial,sans-serif">
                                                                                                                        <tr
                                                                                                                            style="font-family:Helvetica,Arial,sans-serif">
                                                                                                                            <td width="60%"
                                                                                                                                align="left"
                                                                                                                                style="padding:10px 0px;font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:24px;color:rgb(109,109,109)">
                                                                                                                                Payment
                                                                                                                            </td>
                                                                                                                            <td width="40%"
                                                                                                                                align="right"
                                                                                                                                style="padding:10px 0px;font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:24px;color:rgb(109,109,109)">
                                                                                                                                ****
                                                                                                                                ****
                                                                                                                                ****
                                                                                                                                9995
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr
                                                                                                                            style="font-family:Helvetica,Arial,sans-serif">
                                                                                                                            <td width="60%"
                                                                                                                                align="left"
                                                                                                                                style="padding:10px 0px;font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:24px;color:rgb(109,109,109)">
                                                                                                                                Subtotal
                                                                                                                            </td>
                                                                                                                            <td width="40%"
                                                                                                                                align="right"
                                                                                                                                style="padding:10px 0px;font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:24px;color:rgb(109,109,109)">
                                                                                                                                {user_inputs[12]}{user_inputs[5]}
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr
                                                                                                                            style="font-family:Helvetica,Arial,sans-serif">
                                                                                                                            <td width="60%"
                                                                                                                                align="left"
                                                                                                                                style="padding:10px 0px;font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:24px;color:rgb(109,109,109)">
                                                                                                                                Shipping
                                                                                                                                &amp;
                                                                                                                                Handling
                                                                                                                            </td>
                                                                                                                            <td width="40%"
                                                                                                                                align="right"
                                                                                                                                style="padding:10px 0px;font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:24px;color:rgb(109,109,109)">
                                                                                                                                {user_inputs[12]}{user_inputs[9]}
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr
                                                                                                                            style="font-family:Helvetica,Arial,sans-serif">
                                                                                                                            <td width="60%"
                                                                                                                                align="left"
                                                                                                                                style="padding:10px 0px;font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:24px;color:rgb(109,109,109)">
                                                                                                                                Estimated
                                                                                                                                Tax
                                                                                                                            </td>
                                                                                                                            <td width="40%"
                                                                                                                                align="right"
                                                                                                                                style="padding:10px 0px;font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:24px;color:rgb(109,109,109)">
                                                                                                                                {user_inputs[12]}{user_inputs[10]}
                                                                                                                            </td>
                                                                                                                        </tr>
                                                                                                                        <tr
                                                                                                                            style="font-family:Helvetica,Arial,sans-serif">
                                                                                                                            <td width="60%"
                                                                                                                                align="left"
                                                                                                                                style="padding:10px 0px 0px;font-family:Helvetica,Arial,sans-serif;font-size:18px;line-height:30px;color:rgb(17,17,17)">
                                                                                                                                Total
                                                                                                                            </td>
                                                                                                                            <td width="40%"
                                                                                                                                align="right"
                                                                                                                                style="padding:10px 0px 0px;font-family:Helvetica,Arial,sans-serif;font-size:18px;line-height:30px;color:rgb(17,17,17)">
                                                                                                                                {user_inputs[12]}{user_inputs[11]}
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
                                                            <td align="center">
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td align="center">
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td align="center">
                                                                <table align="center" border="0" cellspacing="0"
                                                                    cellpadding="0" width="100%"
                                                                    style="margin:0px;border-collapse:collapse;padding:0px;background-color:rgb(247,247,247)"
                                                                    role="presentation">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td style="font-size:0px">
                                                                                <table align="center" border="0"
                                                                                    cellspacing="0" cellpadding="0"
                                                                                    width="94%"
                                                                                    style="margin:0px auto;min-width:320px;border-collapse:collapse;padding:0px"
                                                                                    role="presentation">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td align="left"
                                                                                                style="padding:40px 0px 0px 20px;font-family:Helvetica,Arial,sans-serif;font-size:14px;font-weight:bold;line-height:28px;color:rgb(0,0,0)">
                                                                                                Get Help
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="left" valign="top"
                                                                                                style="font-size:0px;padding:0px 0px 40px;vertical-align:top">
                                                                                                <div
                                                                                                    style="display:inline-block;max-width:33.33333%;min-width:160px;width:100%;vertical-align:top">
                                                                                                    <table border="0"
                                                                                                        cellspacing="0"
                                                                                                        cellpadding="0"
                                                                                                        width="100%"
                                                                                                        style="min-width:160px;margin:0px auto;border-collapse:collapse;padding:0px"
                                                                                                        role="presentation">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td
                                                                                                                    style="width:100%;min-width:120px;padding:25px 20px 0px;font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:20px;color:rgb(17,17,17)">
                                                                                                                    <a href="http://click.official.nike.com/?qs=1d020c5277199bbf4b9151153d3c05bfe48af8ce82835e737980161b3f423983eff92236d50971f324ec44b33c6bd18b08de33bfed58f6e2638e7c61a03ca2ff"
                                                                                                                        style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:20px;text-decoration:none;color:rgb(17,17,17)"
                                                                                                                        target="_blank">Cancel
                                                                                                                        Order</a>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                                <div
                                                                                                    style="display:inline-block;max-width:33.33333%;min-width:160px;width:100%;vertical-align:top">
                                                                                                    <table border="0"
                                                                                                        cellspacing="0"
                                                                                                        cellpadding="0"
                                                                                                        width="100%"
                                                                                                        style="min-width:160px;margin:0px auto;border-collapse:collapse;padding:0px"
                                                                                                        role="presentation">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td
                                                                                                                    style="width:100%;min-width:120px;padding:25px 20px 0px;font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:20px;color:rgb(17,17,17)">
                                                                                                                    <a href="http://click.official.nike.com/?qs=1d020c5277199bbf1aa6a1c7cf9ad33e252a7e1befe2e10adc377d7d291b261439e676f1fa59c26da38081d4ca1206b80feb58a2976e27c17a3e5785b5948fb8"
                                                                                                                        style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:20px;text-decoration:none;color:rgb(17,17,17)"
                                                                                                                        target="_blank">Return
                                                                                                                        Policy</a>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                                <div
                                                                                                    style="display:inline-block;max-width:33.33333%;min-width:160px;width:100%;vertical-align:top">
                                                                                                    <table border="0"
                                                                                                        cellspacing="0"
                                                                                                        cellpadding="0"
                                                                                                        width="100%"
                                                                                                        style="min-width:160px;margin:0px auto;border-collapse:collapse;padding:0px"
                                                                                                        role="presentation">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td
                                                                                                                    style="width:100%;min-width:120px;padding:25px 20px 0px;font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:20px;color:rgb(17,17,17)">
                                                                                                                    <a href="http://click.official.nike.com/?qs=1d020c5277199bbfa4f273bfbe3a3e661c08ba7ac45804f5c8b7437b17a253b6ec9ead4314ce11bcb4f4abae9226a647dbe3aaa4d2cc445da64f455c239caa48"
                                                                                                                        style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:20px;text-decoration:none;color:rgb(17,17,17)"
                                                                                                                        target="_blank">Contact
                                                                                                                        Options</a>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                                <div
                                                                                                    style="display:inline-block;max-width:33.33333%;min-width:160px;width:100%;vertical-align:top">
                                                                                                    <table border="0"
                                                                                                        cellspacing="0"
                                                                                                        cellpadding="0"
                                                                                                        width="100%"
                                                                                                        style="min-width:160px;margin:0px auto;border-collapse:collapse;padding:0px"
                                                                                                        role="presentation">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td
                                                                                                                    style="width:100%;min-width:120px;padding:25px 20px 0px;font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:20px;color:rgb(17,17,17)">
                                                                                                                    <a href="http://click.official.nike.com/?qs=1d020c5277199bbf6c1ada6723d9f8975d0c42f35f1d5129197e4bc584c00b45384adbf21cf4f35739a68f52616fa6b9577c53df4e6e2803b79aacffdaa1ac07"
                                                                                                                        style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:20px;text-decoration:none;color:rgb(17,17,17)"
                                                                                                                        target="_blank">Gift
                                                                                                                        Card
                                                                                                                        Balance</a>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                                <div
                                                                                                    style="display:inline-block;max-width:33.33333%;min-width:160px;width:100%;vertical-align:top">
                                                                                                    <table border="0"
                                                                                                        cellspacing="0"
                                                                                                        cellpadding="0"
                                                                                                        width="100%"
                                                                                                        style="min-width:160px;margin:0px auto;border-collapse:collapse;padding:0px"
                                                                                                        role="presentation">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td
                                                                                                                    style="width:100%;min-width:160px;font-size:0px;line-height:1px">
                                                                                                                    <a href="http://click.official.nike.com/?qs=1d020c5277199bbf6c1ada6723d9f8975d0c42f35f1d5129197e4bc584c00b45384adbf21cf4f35739a68f52616fa6b9577c53df4e6e2803b79aacffdaa1ac07"
                                                                                                                        style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:20px;text-decoration:none;color:rgb(17,17,17)"
                                                                                                                        target="_blank"></a>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                                <div
                                                                                                    style="display:inline-block;max-width:33.33333%;min-width:160px;width:100%;vertical-align:top">
                                                                                                    <table border="0"
                                                                                                        cellspacing="0"
                                                                                                        cellpadding="0"
                                                                                                        width="100%"
                                                                                                        style="min-width:160px;margin:0px auto;border-collapse:collapse;padding:0px"
                                                                                                        role="presentation">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td
                                                                                                                    style="width:100%;min-width:120px;padding:25px 20px 0px;font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:20px;color:rgb(17,17,17)">
                                                                                                                    <a href="http://click.official.nike.com/?qs=1d020c5277199bbf6c1ada6723d9f8975d0c42f35f1d5129197e4bc584c00b45384adbf21cf4f35739a68f52616fa6b9577c53df4e6e2803b79aacffdaa1ac07"
                                                                                                                        style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:20px;text-decoration:none;color:rgb(17,17,17)"
                                                                                                                        target="_blank"></a>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td align="left" valign="top"
                                                                                                style="padding:40px 0px 25px;border-top-width:1px;border-top-style:solid;font-size:0px;border-top-color:rgb(229,229,229)">
                                                                                                <div
                                                                                                    style="display:inline-table;max-width:33.33333%;min-width:160px;width:100%;vertical-align:top">
                                                                                                    <table border="0"
                                                                                                        cellspacing="0"
                                                                                                        cellpadding="0"
                                                                                                        width="100%"
                                                                                                        style="min-width:160px;margin:0px auto;border-collapse:collapse;padding:0px"
                                                                                                        role="presentation">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td align="left"
                                                                                                                    valign="top"
                                                                                                                    width="20"
                                                                                                                    height="23"
                                                                                                                    style="min-width:20px;font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:22px;padding:0px 0px 0px 20px;color:rgb(0,0,0)">
                                                                                                                    <img width="14"
                                                                                                                        height="23"
                                                                                                                        src="http://image.official.nike.com/lib/fe9815737560077476/m/3/phone-icon2x.png"
                                                                                                                        style="font-family: Helvetica, Arial, sans-serif;">
                                                                                                                </td>
                                                                                                                <td align="left"
                                                                                                                    valign="top"
                                                                                                                    width="140"
                                                                                                                    height="23"
                                                                                                                    style="min-width:140px;font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:22px;padding:0px 20px 0px 0px;color:rgb(0,0,0)">
                                                                                                                    <a href="http://click.official.nike.com/?qs=1d020c5277199bbf9f03ad76c279f95adfb2912db484ef0f2a2eb69523fe4aff13dd788e3b829aad9bc22c835392229a1c47319168e6a9964d77df541d82ea3d"
                                                                                                                        style="text-decoration:none;white-space:nowrap;font-family:Helvetica,Arial,sans-serif;color:rgb(0,0,0)"
                                                                                                                        nowrap
                                                                                                                        target="_blank">1-800-806-6453</a>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                                <div
                                                                                                    style="display:inline-table;max-width:33.33333%;min-width:160px;width:100%;vertical-align:top">
                                                                                                    <table border="0"
                                                                                                        cellspacing="0"
                                                                                                        cellpadding="0"
                                                                                                        width="100%"
                                                                                                        valign="top"
                                                                                                        style="min-width:160px;margin:0px;border-collapse:collapse;padding:0px"
                                                                                                        role="presentation">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td valign="top"
                                                                                                                    style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:22px;padding:0px 20px;text-decoration:none;color:rgb(17,17,17)">
                                                                                                                    <span
                                                                                                                        style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:22px;color:rgb(0,0,0)">4
                                                                                                                        am -
                                                                                                                        11
                                                                                                                        pm
                                                                                                                        PT</span>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
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
                                                        <tr>
                                                            <td align="center">
                                                                <table align="center" border="0" cellspacing="0"
                                                                    cellpadding="0" width="100%"
                                                                    style="margin:0px;border-collapse:collapse;padding:0px"
                                                                    role="presentation">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td align="center"
                                                                                style="padding:45px 0px 28px;font-family:Helvetica,Arial,sans-serif;font-size:24px;line-height:28px;text-align:center;border-top-width:1px;border-top-style:solid;border-top-color:rgb(229,229,229);color:rgb(0,0,0)">
                                                                                <h1
                                                                                    style="margin:0px;font-family:Helvetica,Arial,sans-serif;font-size:24px;line-height:28px;color:rgb(0,0,0)">
                                                                                    <a href="http://click.official.nike.com/?qs=1d020c5277199bbffbd4c13905dbedaf44eccb6b5ceb6b590a4cf8d384c5fb2f461cbcf70868b5296f818569bb0964482152c2ffb20bd092fb5693248bc357f4"
                                                                                        style="margin:0px;font-family:Helvetica,Arial,sans-serif;font-size:24px;line-height:28px;text-decoration:none;color:rgb(0,0,0)"
                                                                                        target="_blank">
                                                                                        <span
                                                                                            style="font-size:24px;line-height:28px;font-family:'Nike TG',Helvetica,Arial,sans-serif;color:rgb(0,0,0)">Nike.com</span>
                                                                                    </a>
                                                                                </h1>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td align="center"
                                                                                style="font-size:0px;padding:0px 0px 35px;border-bottom-width:1px;border-bottom-style:solid;border-bottom-color:rgb(229,229,229)">
                                                                                <table align="center" border="0"
                                                                                    cellspacing="0" cellpadding="0"
                                                                                    width="65%"
                                                                                    style="min-width:300px;margin:0px auto;border-collapse:collapse;padding:0px"
                                                                                    role="presentation">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td align="center"
                                                                                                style="min-width:70px;max-width:25%;font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:16px;padding:0px 0px 17px;color:rgb(17,17,17)">
                                                                                                <a href="http://click.official.nike.com/?qs=1d020c5277199bbf045571f1f888259478226d50343ddd2ee7fdadeda009102bb612ef1467ee885d1b4948579f27d49d390cb4b7433fe4c1b44a2f3ab62dfa22"
                                                                                                    style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:16px;text-decoration:none;color:rgb(0,0,0)"
                                                                                                    target="_blank">Men</a>
                                                                                            </td>
                                                                                            <td
                                                                                                style="width:61px;font-size:0px">
                                                                                            </td>
                                                                                            <td align="center"
                                                                                                style="min-width:70px;max-width:25%;font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:16px;padding:0px 0px 17px;color:rgb(17,17,17)">
                                                                                                <a href="http://click.official.nike.com/?qs=1d020c5277199bbf94c22fc5e64be397262e2417a3da040475dc989ca032ba9c8e8e5a80c6b4c02473eae7b5183af879b2635de0afeaea612bb66fbd6ef852b9"
                                                                                                    style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:16px;text-decoration:none;color:rgb(0,0,0)"
                                                                                                    target="_blank">Women</a>
                                                                                            </td>
                                                                                            <td
                                                                                                style="width:61px;font-size:0px">
                                                                                            </td>
                                                                                            <td align="center"
                                                                                                style="min-width:70px;max-width:25%;font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:16px;padding:0px 0px 17px;color:rgb(17,17,17)">
                                                                                                <a href="http://click.official.nike.com/?qs=1d020c5277199bbf6714e3f8502d6c5e782b8086ba00d35378047c2d98726946820956c76304c39dc57209a29269b1ebfa5eecc697cec427acfaca264b3e9f86"
                                                                                                    style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:16px;text-decoration:none;color:rgb(0,0,0)"
                                                                                                    target="_blank">Kids</a>
                                                                                            </td>
                                                                                            <td
                                                                                                style="width:61px;font-size:0px">
                                                                                            </td>
                                                                                            <td align="center"
                                                                                                style="min-width:70px;max-width:25%;font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:16px;padding:0px 0px 17px;color:rgb(17,17,17)">
                                                                                                <a href="http://click.official.nike.com/?qs=1d020c5277199bbf95379e72d502b78ea339716a39fd8762c2aab0ad287faaaf386def16f47368c780de7f8f3bd073794b591a27ee7e32101b77a3f6e22a1701"
                                                                                                    style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:16px;text-decoration:none;color:rgb(0,0,0)"
                                                                                                    target="_blank">Customize</a>
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
                                                            <td align="center">
                                                                <table align="center" border="0" cellspacing="0"
                                                                    cellpadding="0" width="100%"
                                                                    style="margin:0px;border-collapse:collapse;padding:0px"
                                                                    role="presentation">
                                                                    <tbody>
                                                                        <tr>
                                                                            <td align="center"
                                                                                style="font-size:0px;padding:20px 0px 40px">
                                                                                <table align="center" border="0"
                                                                                    cellspacing="0" cellpadding="0"
                                                                                    style="margin:0px auto;border-collapse:collapse;padding:0px"
                                                                                    role="presentation">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td align="center"
                                                                                                style="min-width:70px;font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:26px;padding:0px;color:rgb(170,170,170)">
                                                                                                <a href="https://nike.com"
                                                                                                    style="white-space:nowrap;font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:26px;text-decoration:none;color:rgb(170,170,170)"
                                                                                                    target="_blank">Web
                                                                                                    Version</a>
                                                                                            </td>
                                                                                            <td
                                                                                                style="width:17px;min-width:17px;font-size:0px">
                                                                                            </td>
                                                                                            <td align="center"
                                                                                                style="min-width:70px;font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:26px;padding:0px;color:rgb(170,170,170)">
                                                                                                <a href="http://click.official.nike.com/?qs=1d020c5277199bbf25be27faaeedfc396c05f8eb144ce752ad440cdaf0520ff107aa88178f031a0a9f79b879edb913f0d121a781a319d866831e4d9a0f0dd1e7"
                                                                                                    style="white-space:nowrap;font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:26px;text-decoration:none;color:rgb(170,170,170)"
                                                                                                    target="_blank">Privacy
                                                                                                    Policy</a>
                                                                                            </td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td align="center"
                                                                                style="font-size:0px;padding:0px 30px">
                                                                                <p
                                                                                    style="margin:0px auto;font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:26px;padding:0px;color:rgb(170,170,170)">
                                                                                    Please <a
                                                                                        href="http://click.official.nike.com/?qs=1d020c5277199bbf0d04ace8c21958c8f6229fa9bbe4ceef9fb706cc99efff9b72e09207ff9b4ae26f62236b674096f8ddd45bb427f1e16281ba12f61a1bf894"
                                                                                        style="white-space:nowrap;font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:26px;color:rgb(170,170,170)"
                                                                                        target="_blank">contact us</a> if
                                                                                    you have any questions. (If you reply to
                                                                                    this email, we won&#39;t be able to see
                                                                                    it.)</p>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td align="center"
                                                                                style="font-size:0px;padding:43px 20px 0px">
                                                                                <p
                                                                                    style="margin:0px auto;font-family:Helvetica,Arial,sans-serif;font-size:11px;line-height:22px;padding:0px;color:rgb(170,170,170)">
                                                                                    © 2025 Nike, Inc. All Rights Reserved.
                                                                                </p>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td align="center"
                                                                                style="font-size:0px;padding:0px 20px 20px">
                                                                                <p
                                                                                    style="margin:0px auto;font-family:Helvetica,Arial,sans-serif;font-size:11px;line-height:22px;padding:0px;color:rgb(170,170,170)">
                                                                                    <span
                                                                                        class="m_-2774923715066548899address"
                                                                                        style="text-decoration:none;font-family:Helvetica,Arial,sans-serif">NIKE,
                                                                                        INC. <a
                                                                                            href="https://www.google.com/maps/search/One+Bowerman+Drive,+Beaverton,+Oregon+97005,+USA?entry=gmail&amp;source=g"
                                                                                            style="font-family:Helvetica,Arial,sans-serif">One
                                                                                            Bowerman Drive, Beaverton,
                                                                                            Oregon 97005, USA</a>.</span>
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
                            <td class="m_-2774923715066548899sidebar"
                                style="font-size:0px;line-height:1px;overflow:hidden!important"> </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </center>
    </div>
    </div>
    """

    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
