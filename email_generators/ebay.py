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
    msg['From'] = formataddr((f'Ebay', sender_email))
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
    "Please enter the street address (123 Test Street):",
    "Please enter the city & postcode (Sydney, 2000):",
    "Please enter the country (Australia):",
    "Please enter the delivery date (Fri, 22 Dec - Thu, 26 Dec):",
    "Please enter the image url (Must be eBay image link):",
    "Please enter the product name (Apple AirPods Pro (2nd Generation)):",
    "Please enter the product price (WITHOUT THE $ SIGN):",
    "Please enter the item ID (334638548148):",
    "Please enter the postage total (WITHOUT THE $ SIGN):",
    "Please enter the order total (WITHOUT THE $ SIGN):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira o endereço (123 Test Street):",
    "Por favor, insira a cidade e o código postal (Sydney, 2000):",
    "Por favor, insira o país (Austrália):",
    "Por favor, insira a data de entrega (Sex, 22 Dez - Qui, 26 Dez):",
    "Por favor, insira o URL da imagem (deve ser link de imagem do eBay):",
    "Por favor, insira o nome do produto (Apple AirPods Pro (2ª Geração)):",
    "Por favor, insira o preço do produto (SEM O SÍMBOLO $):",
    "Por favor, insira o ID do item (334638548148):",
    "Por favor, insira o valor do frete (SEM O SÍMBOLO $):",
    "Por favor, insira o total do pedido (SEM O SÍMBOLO $):",
    "Por favor, insira a moeda ($/€/£):",
    "Qual endereço de e-mail deve receber este e-mail (juggyresells@gmail.com):"
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
    part1 = "35"
    part2 = random.randint(10000, 99999)  # Random 5-digit number
    part3 = random.randint(10000, 99999)  # Random 5-digit number

    # Combine the parts into order number
    order_number = f"{part1}-{part2}-{part3}"
    return order_number

def generate_card_number():
    # Generate random card number
    part1 = random.randint(1000, 9999)  # Random 4-digit number

    # Combine the parts into order number
    card_number = f"{part1}"
    return card_number

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
    card_num = generate_card_number()

    sender_email = f'{EMAIL}'
    sender_password = f'{PASSWORD}'
    recipient_email = f'{user_inputs[12]}'
    subject = f"Thank you for your order"

    html_template=f"""
    <!DOCTYPE html>
    <!--f6e1b8d4-a963-4fd7-b0cb-e33d80d681ba_v151-->
    <html>
    </tr>
    </table>
    <table width="600" border="0" cellspacing="0" bgcolor="#FFFFFF" cellpadding="0" align="center" class="mgh-N1-IMAGE_FRAME-2023_OS_Header_Transactional_Generic fullwidth mgh" role="presentation">
    <tr>
    <td width="100%" valign="top" align="center" class="fullwidth" style="padding-bottom:0px;">
    <table width="568" border="0" cellspacing="0" cellpadding="0" align="center" class="fullwidth" role="presentation">
    <tr>
    <td style="font-size:1px;line-height:1px;vertical-align:top;" valign="top" align="center" class="">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center" role="presentation">
    <tr>
    <td width="79" style="font-size:1px;line-height:1px;vertical-align:top;" valign="top" align="left" class="floatleft fullwidth logo">
    <table width="79" border="0" cellspacing="0" cellpadding="0" align="left" role="presentation">
    <tr>
    <td height="32" style="font-size:1px;line-height:1px;vertical-align:top;padding-top:24px;" valign="top" class="heightauto pl16 pt16">
    <a href="https://www.ebay.co.uk?mkevt=1&mkpid=0&emsid=e11400.m144669.l147884&mkcid=7&ch=osgood&euid=ec979978cea742baaec4ea862883141c&bu=45592875971&exe=0&ext=0&osub=-1%7E1&crd=20230925181914&segname=11400" style="text-decoration:none;display:inline-block;" class="focus">
    <span class="focus__content" tabindex="-1">
    <img src="https://secureir.ebaystatic.com/cr/mscdn/2da6a871d3ba2f07594cec7f55bcf6ed/Logo_Legacy_2x.png" width="79" height="32" alt="eBay logo" border="0" style="display:inline-block;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;line-height:17px;color:#171717;font-weight:bold;text-decoration:none;" class=" light-image focus" />
    <!--[if !mso]><!-->
    <div class="dark-image" style="display:none;overflow:hidden;width:0px;max-height:0px;max-width:0px;line-height:0px;visibility:hidden;">
    <img src="https://secureir.ebaystatic.com/cr/mscdn/2da6a871d3ba2f07594cec7f55bcf6ed/Logo_Legacy_2x.png" width="79" height="32" alt="eBay logo" border="0" style="display:inline-block;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;line-height:17px;color:#171717;font-weight:bold;text-decoration:none;" class="focus" />
    </div>
    <!--<![endif]-->
    </span>
    </a>
    <img src="https://www.ebayadservices.com/marketingtracking/v1/impression?mkevt=4&siteId=3&mkpid=0&emsid=e11400&mkcid=7&ch=osgood&euid=ec979978cea742baaec4ea862883141c&bu=45592875971&exe=0&ext=0&osub=-1%7E1&crd=20230925181914&segname=11400" alt="" aria-hidden="true" role="presentation" style="border:0; height:1px; display:block; line-height:1px;float:left;" width="1" height="1" border="0" />
    </td>
    </tr>
    </table>
    </td>
    </tr>
    </table>
    </td>
    </tr>
    </table>
    </td>
    </tr>
    </table>
    <!--|MSME_gh_853016f5-aafd-453f-89d2-227f2f83462b_44_12.0_BCC_2023-OS-Header-Transactional-Generic_N1|--> <!--|MSMS_h|-->
    <table width="600" border="0" cellspacing="0" cellpadding="0" align="center" class="mh-N1-transactionalGeneric-2023_OS_Hero_Transactional_Generic heroMod fullwidth" role="presentation" bgcolor="#FFFFFF">
    <tbody>
    <tr>
    <td style="font-size:1px;line-height:1px;padding:0px 0px 0px 0px;" align="center" class="pb0">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center" role="presentation" bgcolor="#FFFFFF" class="mh-N1-transactionalGeneric-2023_OS_Hero_Transactional_Generic component">
    <tbody>
    <tr>
    <td style="font-size:1px;line-height:1px;padding:8px 16px 0px 16px;" class="pl0 pr0" align="center">
    <table width="568" border="0" cellspacing="0" cellpadding="0" align="center" class="fullwidth" role="presentation">
    <tbody>
    <tr>
    <td height="40" style="font-size:1px;line-height:1px;padding:0px 0px 0px 0px;" align="center" class="pl16 pr16 title">
    <h1 style="mso-line-height-rule:exactly;margin:0;line-height:40px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:24px;color:#111820;font-weight:bold;text-decoration:none;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-align:left" align="left" class="">
    Thanks for shopping. Your order is confirmed.
    </h1>
    </td>
    </tr>
    <tr>
    <td style="font-size:1px;line-height:1px;padding:16px 16px 24px 0px;" align="left" class="pl16 pr16 dmCTA">
    <table border="0" cellspacing="0" cellpadding="0" align="left" role="presentation">
    <tr>
    <th height="40" style="font-size:1px;line-height:1px;" align="left" class="fullwidth floatleft pb8">
    <div style="font-size:1px;line-height:1px;" align="left" class="all">
    <table border="0" cellspacing="0" cellpadding="0" bgcolor="#3665F3" style="display:inline-table;border-radius:24px;border-collapse:separate;" class="button cta" role="presentation">
    <tbody>
    <tr>
    <td height="40" style="font-size:1px;line-height:1px;vertical-align:middle;border:1px solid #3665F3;border-radius:24px;border-collapse:separate;" align="center" valign="middle">
    <p style="mso-line-height:exactly;margin:0;line-height:16px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;font-weight:bold;color:#FFFFFF;text-align:center;vertical-align:middle;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;border-radius:24px;" align="center">
    <a href="https://www.ebay.co.uk/vod/FetchOrderDetails?itemId=225783369730&transactionId=2823385376012&mkevt=1&mkpid=0&emsid=e11400.m144670.l152615&mkcid=7&ch=osgood&euid=ec979978cea742baaec4ea862883141c&bu=45592875971&exe=0&ext=0&osub=-1%7E1&crd=20230925181914&segname=11400" style="color:#FFFFFF;text-decoration:none;display:block!important;padding:11px 17px 11px 17px!important;border-radius:24px;" class="focus">
    <span class="focus__content" tabindex="-1">
    View order details
    </span>
    </a>
    </p>
    </td>
    </tr>
    </tbody>
    </table>
    </div>
    </th>
    <th height="40" style="font-size:1px;line-height:1px;padding-left:8px;" align="left" class="fullwidth floatleft pl0">
    <div style="font-size:1px;line-height:1px;" align="left" class="all">
    <table border="0" cellspacing="0" cellpadding="0" style="display:inline-table;border-radius:24px;border-collapse:separate;" class="button cta2" role="presentation">
    <tr>
    <td height="40" style="font-size:1px;line-height:1px;vertical-align:middle;border:1px solid #3665F3;border-radius:24px;border-collapse:separate;" align="center" valign="middle">
    <p style="mso-line-height:exactly;margin:0;line-height:16px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;font-weight:bold;color:#3665F3;text-align:center;vertical-align:middle;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;border-radius:24px;" align="center">
    <a href="https://www.ebay.co.uk/deals?mkevt=1&mkpid=0&emsid=e11400.m144670.l153066&mkcid=7&ch=osgood&euid=ec979978cea742baaec4ea862883141c&bu=45592875971&exe=0&ext=0&osub=-1%7E1&crd=20230925181914&segname=11400" style="color:#3665F3;text-decoration:none;display:block!important;padding:11px 17px 11px 17px!important;border-radius:24px;" class="focus">
    <span class="focus__content" tabindex="-1">
    Browse deals
    </span>
    </a>
    </p>
    </td>
    </tr>
    </table>
    </div>
    </th>
    </tr>
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

    <!--|MSME_h_3faf60c6-9627-42f1-870e-8c8a20c9b56c_46_6.0_BCC_2023-OS-Hero-Transactional-Generic_N1|--> <!--|MSMS_os|-->
    <table width="600" border="0" cellspacing="0" cellpadding="0" align="center" class="mos-N1-CONTAINER-none heroMod fullwidth" bgcolor="#FFFFFF" role="presentation">
    <tbody>
    <tr>
    <td style="font-size:1px;line-height:1px;padding:0px 0px 32px 0px;vertical-align:top;" valign="top" align="center" class="pl16 pr16 pb24">
    <table width="568" border="0" cellspacing="0" cellpadding="0" align="center" role="presentation" bgcolor="#F7F7F7" style="border-radius: 16px;" class="mos-N1-CONTAINER-none component fullwidth">
    <tbody>
    <tr>
    <td style="font-size:1px;line-height:1px;padding:32px 0px 32px 0px;vertical-align:top;" valign="top" align="center">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center" role="presentation">
    <tbody>
    <tr>
    <th style="font-size:1px;line-height:1px;vertical-align:top;padding:0px 0px 0px 0px;" valign="top" align="center" class="floatleft fullwidth left">
    <table border="0" cellspacing="0" cellpadding="0" align="center" class="fullwidth" role="presentation">
    <tbody>
    <tr>
    <td style="font-size:1px;line-height:1px;" align="center" class="pl16 pr16">
    <table width="252" border="0" cellspacing="0" cellpadding="0" align="center" class="fullwidth" role="presentation">
    <tbody>
    <tr>
    <td height="19" style="font-size:1px;line-height:1px;padding:0px 0px 0px 0px;" align="left" class="itemKey">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:19px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#414141;font-weight:normal;text-decoration:none;" align="left" class="fallbackfont">
    Your order will be dispatched to:
    </p>
    </td>
    </tr>
    <tr>
    <td height="19" style="font-size:1px;line-height:1px;padding:0px 40px 0px 0px;;" align="left" class="itemValue">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:19px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#111820;font-weight:normal;text-decoration:none;" align="left" class="fallbackfont">
    <span class="gmailFix primaryText" style="color:#111820;text-decoration:none;">
    {user_inputs[0]}<br>{user_inputs[1]}<br>{user_inputs[2]}<br>{user_inputs[3]}</span>
    </p>
    </td>
    </tr>
    </tbody>
    </table>
    </td>
    </tr>
    </tbody>
    </table>
    </th>
    <th style="font-size:1px;line-height:1px;vertical-align:top;padding:0px 0px 0px 0px;" valign="top" align="center" class="floatleft fullwidth right">
    <table border="0" cellspacing="0" cellpadding="0" align="center" class="fullwidth" role="presentation">
    <tbody>
    <tr>
    <td style="font-size:1px;line-height:1px;" align="center" class="pl16 pr16">
    <table width="252" border="0" cellspacing="0" cellpadding="0" align="center" class="fullwidth" role="presentation">
    <tbody>
    <tr>
    <td height="19" style="font-size:1px;line-height:1px;padding:0px 0px 0px 0px;" align="left" class="pt20 itemKey">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:19px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#414141;font-weight:normal;text-decoration:none;" align="left" class="fallbackfont">
    Estimated delivery:
    </p>
    </td>
    </tr>
    <tr>
    <td height="19" style="font-size:1px;line-height:1px;padding:0px 0px 0px 0px;;" align="left" class="itemValue">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:19px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#111820;font-weight:bold;text-decoration:none;" align="left" class="fallbackfont">
    {user_inputs[4]}
    </p>
    </td>
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
    </td>
    </tr>
    </tbody>
    </table>
    </td>
    </tr>
    </tbody>
    </table>

    <!--|MSME_os_d863b1e1-e9b4-49ed-ba08-0b811e8f78b2_45_3.0_BCC__N1|--> <!--|MSMS_t|-->
    <table width="600" border="0" cellspacing="0" cellpadding="0" align="center" bgcolor="#FFFFFF" class="mt-N1-undefined-none fullwidth" role="presentation">
    <tbody>
    <tr>
    <td style="font-size:1px;line-height:1px;vertical-align:top;" valign="top" align="center">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center" role="presentation">
    <tbody>
    <tr>
    <td height="32" style="font-size:1px;line-height:1px;padding:0px 16px 8px 16px;" align="left" class="pl16 pr16">
    <h1 style="mso-line-height-rule:exactly;margin:0;line-height:32px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:24px;color:#111820;font-weight:bold;text-decoration:none;" align="left" class="mt-N1-undefined-noneTitle fs24">
    Your order details
    </h1>
    </td>
    </tr>
    <tr>
    <td height="21" style="font-size:1px;line-height:1px;padding:0px 16px 24px 16px;" align="left" class="pl16 pr16">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:21px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#767676;font-weight:normal;text-decoration:none;" align="left" class="mt-N1-undefined-noneDescription">
    We'll let you know when your order has been dispatched.
    </p>
    </td>
    </tr>
    </tbody>
    </table>
    </td>
    </tr>
    </tbody>
    </table>
    <!--|MSME_t_37b18d65-a47b-4977-bc2a-f6f2d7d889a0_71_16.0_BCC__N1|-->
    <!--|MSMS_si|-->
    <table width="600" border="0" cellspacing="0" cellpadding="0" align="center" class="fullwidth msi-N1-undefined-none" role="presentation" bgcolor="#FFFFFF">
    <tr>
    <td style="font-size:1px;line-height:1px;padding:0px 0px 32px 0px;vertical-align:top;" valign="top" align="center" class="pb24">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center" role="presentation" class="">
    <!--[if !mso]><!-->
    <tr>
    <td style="font-size:1px;line-height:1px;vertical-align:top;padding:0px 0px 10px 0px;" valign="top" align="center" class="floatleft fullwidth right show_on_mobile">
    <table width="389" border="0" cellspacing="0" cellpadding="0" align="center" class="fullwidth show_on_mobile" role="presentation" style="display:none;overflow:hidden;width:0;height:0;max-height:0;mso-hide:all">
    <tr>
    <td style="font-size:1px;line-height:1px;" align="center" class="pl16 pr16">
    <table border="0" cellspacing="0" cellpadding="0" align="left" class="fullwidth" role="presentation">
    <tr>
    <td width="40%" height="21" style="font-size:1px;line-height:1px;padding:0px 8px 0px 0px;" align="center" valign="top" class="img">
    <a href="https://www.ebay.co.uk/" style="text-decoration:none;display:inline-block;" class="focus imgfullwidth">
    <span class="focus__content" tabindex="-1">
    <img src="https://i.ebayimg.com/images/g/L~UAAOSwzNxlErwu/s-l1600.jpg" width="178" height="178" alt="Genuine Samsung SM-R510 Galaxy Buds2 Pro Wireless Bluetooth Headphones Graphite" border="0" style="border-radius:8px;display:inline-block;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;line-height:17px;color:#171717;font-weight:bold;text-decoration:none;background:#F7F7F7;" class="imgfullwidth focus" />
    </span>
    </a>
    </td>
    <td width="60%" style="font-size:1px;line-height:1px;padding:0px 0px 0px 0px;" align="center" valign="top" >
    <table border="0" cellspacing="0" cellpadding="0" align="left" class="fullwidth" role="presentation">
    <tr>
    <td height="21" style="font-size:1px;line-height:1px;padding:0px 0px 0px 0px;" align="center" class="pr16 title">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:21px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#111820;font-weight:normal;text-decoration:none;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-align:left;" align="left" class="">
    <a href="https://www.ebay.co.uk" style="color:#111820;text-decoration:underline;display:block!important;" class="focus">
    <span class="focus__content" tabindex="-1">
    Genuine Samsung SM-R510 Galaxy Buds2 Pro Wireless Bluetooth Headphones Graphite
    </span>
    </a>
    </p>
    </td>
    </tr>
    </table>
    </td>
    </tr>
    </table>
    </td>
    </tr>
    </table>
    </td>
    </tr>
    <!--<![endif]-->
    <tr>
    <th style="font-size:1px;line-height:1px;vertical-align:top;" valign="top" align="center" class="floatleft fullwidth perc30 hide">
    <table width="194" border="0" cellspacing="0" cellpadding="0" align="center" class="fullwidth" role="presentation">
    <tr>
    <td style="font-size:1px;line-height:1px;padding:0px 0px 0px 0px;" align="center" class="pt0 pl16 img">
    <table width="194" border="0" cellspacing="0" cellpadding="0" align="center" class="fullwidth" role="presentation">
    <tr>
    <td height="178" style="font-size:1px;line-height:1px;padding:0px 0px 0px 0px;" align="right" class="alc heightauto">
    <a href="https://www.ebay.co.uk/" style="text-decoration:none;display:inline-block;" class="focus focus3 imgfullwidth">
    <span class="focus__content" tabindex="-1">
    <img src="{user_inputs[5]}" width="178" height="178" alt="{user_inputs[6]}" border="0" style="border-radius:8px;display:inline-block;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;line-height:17px;color:#171717;font-weight:bold;text-decoration:none;background:#F7F7F7;" class="imgfullwidth focus"/>
    </span>
    </a>
    </td>
    </tr>
    </table>
    </td>
    </tr>
    </table>
    </th>
    <th style="font-size:1px;line-height:1px;vertical-align:top;" valign="top" align="center" class="floatleft fullwidth perc70">
    <table width="406" border="0" cellspacing="0" cellpadding="0" align="center" class="fullwidth" role="presentation">
    <tr>
    <td style="font-size:1px;line-height:1px;padding:0px 0px 0px 0px;" align="center" class="pt0 pl16 pr16">
    <table width="374" border="0" cellspacing="0" cellpadding="0" align="center" class="fullwidth" role="presentation">
    <tr>
    <td height="24" style="font-size:1px;line-height:1px;padding:0px 0px 4px 0px;" align="center" class="pr16 hide title">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:24px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:16px;color:#111820;font-weight:normal;text-decoration:none;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-align:left;" align="left">
    <a href="https://www.ebay.co.uk" style="color:#111820;text-decoration:underline;display:block!important;" class="focus">
    <span class="focus__content" tabindex="-1">
    {user_inputs[6]}
    </span>
    </a>
    </p>
    </td>
    </tr>
    <tr>
    <td style="font-size:1px;line-height:1px;" align="center">
    <table border="0" cellspacing="0" cellpadding="0" align="left" class="" role="presentation">
    <tr>
    <td height="14" style="font-size:1px;line-height:1px;padding-top:4px;" align="center" valign="middle" class="badge">
    <a href="https://pages.ebay.co.uk/ebay-money-back-guarantee/?mkevt=1&mkpid=0&emsid=e11400.m144671.l159390&mkcid=7&ch=osgood&euid=ec979978cea742baaec4ea862883141c&bu=45592875971&exe=0&ext=0&osub=-1%7E1&crd=20230925181914&segname=11400" style="color:#767676;text-decoration:underline;" class="focus">
    <span class="focus__content" tabindex="-1">
    <img src="https://secureir.ebaystatic.com/cr/mscdn/7953f23caa56178e71c364f9814a6732/Money+back+guarantee+UK%403x.png" width="15" height="15" alt="eBay Money Back Guarantee" border="0" style="display:inline-block;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;line-height:17px;color:#171717;font-weight:bold;text-decoration:none;" class="focus" />
    </span>
    </a>
    </td>
    <td height="21" style="font-size:1px;line-height:1px;padding:2px 16px 0px 8px;" align="left" valign="middle" class="badge">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:21px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#767676;text-decoration:underline;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-align:left;" align="left" class="details fallbackfont">
    <a href="https://pages.ebay.co.uk/ebay-money-back-guarantee/?mkevt=1&mkpid=0&emsid=e11400.m144671.l159390&mkcid=7&ch=osgood&euid=ec979978cea742baaec4ea862883141c&bu=45592875971&exe=0&ext=0&osub=-1%7E1&crd=20230925181914&segname=11400" style="color:#767676;text-decoration:underline;" class="focus">
    <span class="focus__content" tabindex="-1">
    eBay Money Back Guarantee
    </span>
    </a>
    </p>
    </td>
    </tr>
    </table>
    </td>
    </tr>
    <tr>
    <td style="font-size:1px;line-height:1px;" align="center">
    <table width="357" border="0" cellspacing="0" cellpadding="0" align="left" class="fullwidth" role="presentation">
    <tr>
    <td height="21" style="font-size:1px;line-height:1px;padding:8px 0px 0px 0px;" align="center">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:21px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#767676;font-weight:normal;text-decoration:none;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-align:left;" align="left" class="info fallbackfont labelValueMapLabel">
    Price:
    </p>
    <p style="mso-line-height-rule:exactly;margin:0;line-height:21px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#111820;font-weight:normal;text-decoration:none;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-align:left;" align="left" class="details fallbackfont labelValueMapValue">
    <b>{user_inputs[11]}{user_inputs[7]}</b>
    </p>
    </td>
    </tr>
    <tr>
    <td height="21" style="font-size:1px;line-height:1px;padding:8px 0px 0px 0px;" align="center">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:21px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#767676;font-weight:normal;text-decoration:none;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-align:left;" align="left" class="info fallbackfont labelValueMapLabel">
    Item ID:
    </p>
    <p style="mso-line-height-rule:exactly;margin:0;line-height:21px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#111820;font-weight:normal;text-decoration:none;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-align:left;" align="left" class="details fallbackfont labelValueMapValue">
    {user_inputs[8]}
    </p>
    </td>
    </tr>
    <tr>
    <td height="21" style="font-size:1px;line-height:1px;padding:8px 0px 0px 0px;" align="center">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:21px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#767676;font-weight:normal;text-decoration:none;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-align:left;" align="left" class="info fallbackfont labelValueMapLabel">
    Order number:
    </p>
    <p style="mso-line-height-rule:exactly;margin:0;line-height:21px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#111820;font-weight:normal;text-decoration:none;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-align:left;" align="left" class="details fallbackfont labelValueMapValue">
    {order_num}
    </p>
    </td>
    </tr>
    <tr>
    <td height="21" style="font-size:1px;line-height:1px;padding:8px 0px 0px 0px;" align="center">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:21px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#767676;font-weight:normal;text-decoration:none;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-align:left;" align="left" class="info fallbackfont labelValueMapLabel">
    Seller:
    </p>
    <p style="mso-line-height-rule:exactly;margin:0;line-height:21px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#111820;font-weight:normal;text-decoration:none;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-align:left;" align="left" class="details fallbackfont labelValueMapValue">
    <a href="https://www.ebay.co.uk/str/Authentic-Accessories" style="text-decoration:underline!important;font-weight:inherit!important;color:#111820!important;" class="focus labelValueMapValue_3_l1"><span class="focus__content" tabindex="-1"><!--[if mso]><font color="#111820"><![endif]-->Explore more from this seller<!--[if mso]></font><![endif]--></span></a><br />
    </p>
    </td>
    </tr>
    </table>
    </td>
    </tr>
    </table>
    </td>
    </tr>
    </table>
    </th>
    </tr>
    </table>
    </td>
    </tr>
    </table>
    </style>
    </tr>
    </table>
    </td>
    </tr>
    </table>
    </td>
    </tr>
    </table>
    </th>
    </tr>
    </table>
    </td>
    </tr>
    </table>
    <table width="600" border="0" cellspacing="0" cellpadding="0" align="center" bgcolor="#FFFFFF" class="fullwidth moc-N1-undefined-none" role="presentation">
    <tr>
    <td style="font-size:1px;line-height:1px;vertical-align:top; padding:0px 16px 32px 16px" valign="top" align="center">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center" role="presentation" bgcolor="#F7F7F7" style="border-radius:16px;border-collapse:separate;" class="bgInnerDM" >
    <tr>
    <td colspan="2" height="20" style="font-size:1px;line-height:1px;padding:24px 16px 4px 24px;" align="left" class="pl24">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:20px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#767676;font-weight:normal;text-decoration:none;" align="left" class="titleDm">
    Order total:
    </p>
    </td>
    </tr>
    <tr>
    <td height="20" style="font-size:1px;line-height:1px;padding:0px 0px 0px 24px;" align="left" class="pl24 ">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:20px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#111820;font-weight:normal;text-decoration:none;" align="left" class="fallbackfont itemTextDM">
    Subtotal
    </p>
    </td>
    <td height="20" style="font-size:1px;line-height:1px;padding:0px 24px 0px 0px;" align="left" class="pr24 ">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:20px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#111820;font-weight:normal;text-decoration:none;" align="right" class="fallbackfont itemTextDM">
    {user_inputs[11]}{user_inputs[7]}
    </p>
    </td>
    </tr>
    <tr>
    <td height="20" style="font-size:1px;line-height:1px;padding:0px 0px 0px 24px;" align="left" class="pl24 ">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:20px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#111820;font-weight:normal;text-decoration:none;" align="left" class="fallbackfont itemTextDM">
    Postage
    </p>
    </td>
    <td height="20" style="font-size:1px;line-height:1px;padding:0px 24px 0px 0px;" align="left" class="pr24 ">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:20px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#111820;font-weight:normal;text-decoration:none;" align="right" class="fallbackfont itemTextDM">
    {user_inputs[11]}{user_inputs[9]}
    </p>
    </td>
    </tr>
    <tr>
    <td height="20" style="font-size:1px;line-height:1px;padding:0px 0px 2px 24px;" align="left" class="pl24 ">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:20px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#111820;font-weight:normal;text-decoration:none;" align="left" class="fallbackfont itemTextDM">
    Coupons, discounts, gift cards
    </p>
    </td>
    <td height="20" style="font-size:1px;line-height:1px;padding:0px 24px 2px 0px;" align="left" class="pr24 ">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:20px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#111820;font-weight:normal;text-decoration:none;" align="right" class="fallbackfont itemTextDM">
    {user_inputs[11]}0.00
    </p>
    </td>
    </tr>
    <tr>
    <td height="1" style="font-size:1px;line-height:1px;padding: 4px 0 4px 24px;" align="center" aria-hidden="true" class="">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center" class="full itemTextDM" role="presentation" bgcolor="#F7F7F7">
    <tbody style="width: 100%;">
    <tr style="width: 100%;">
    <td height="1" style="font-size:1px;line-height:1px;border-bottom:1px solid #111820;" align="center">
    &nbsp;
    </td>
    </tr>
    </tbody>
    </table>
    </td>
    <td height="1" style="font-size:1px;line-height:1px;padding: 4px 24px 4px 0;" align="center" aria-hidden="true" class="">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center" class="full itemTextDM" role="presentation" bgcolor="#F7F7F7">
    <tbody style="width: 100%;">
    <tr style="width: 100%;">
    <td height="1" style="font-size:1px;line-height:1px;border-bottom:1px solid #111820;" align="center">
    &nbsp;
    </td>
    </tr>
    </tbody>
    </table>
    </td>
    </tr>
    <tr>
    <td style="font-size:1px;line-height:1px;padding:4px 0 24px 24px;" class="pb24" align="left">
    <table cellpadding="0" cellspacing="0" border="0" align="left" role="presentation">
    <tr>
    <td height="20" style="font-size:1px;line-height:1px;" align="left" valign="middle">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:20px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#111820;font-weight:normal;text-decoration:none;" align="left" class="fallbackfont itemTextDM">
    <span class="focus__content" tabindex="-1" style="white-space:nowrap;">
    Total charged to
    </span>
    <span class="break"></span>
    <span class="focus__content" style="display:inline-block;mso-line-height-rule:exactly;margin:0;line-height:100%;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#111820;font-weight:normal;text-decoration:none;">
    <img src="https://secureir.ebaystatic.com/cr/mscdn/d8407b8ed6b8c7ec08dc1325c7f03424/Mastercard.png" alt="mastercard icon" width="33" height="20" border="0" valign="middle" style="display:inline-block;vertical-align: middle;" class="icon focus"/>
    &nbsp;
    </span>
    <span class="focus__content" style="mso-line-height-rule:exactly;margin:0;line-height:20px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;font-weight:normal;text-decoration:none;display:inline-block!important;">
    x -{card_num}
    </span>
    </p>
    </td>
    </tr>
    </table>
    </td>
    <td height="20" style="font-size:1px;line-height:1px;padding:4px 24px 24px 0;" align="right" class="pb24 pr24">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:20px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#111820;font-weight:normal;text-decoration:none;" align="right" class="fallbackfont itemTextDM">
    {user_inputs[11]}{user_inputs[10]}
    </p>
    </td>
    </tr>
    </table>
    </td>
    </tr>
    </table>
    </style>
    <table width="600" border="0" cellspacing="0" cellpadding="0" align="center" bgcolor="#FFFFFF" class="mbni-N1-ICON_COPY-none fullwidth" role="presentation">
    <tr>
    <td style="font-size:1px;line-height:1px;vertical-align:top;padding:0px 16px 32px 16px" valign="top" align="center" class="pb24">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center" bgcolor="#F7F7F7" class="component" role="presentation" style="border-radius:16px;" >
    <tr>
    <td style="font-size:1px;line-height:1px;vertical-align:middle;padding:16px 0px 16px 0px;" valign="middle" align="center" class="pt0 pb0">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center" role="presentation">
    <tr>
    <th style="font-size:1px;line-height:1px;vertical-align:middle;" valign="middle" align="left" class="floatleft fullwidth right">
    <table width="88" border="0" cellspacing="0" cellpadding="0" align="center" class="fullwidth" role="presentation">
    <tr>
    <td height="38" style="font-size:1px;line-height:1px;vertical-align:middle; padding-left:24px" align="left" valign="middle" class="all pt24 pb16">
    <img src="https://secureir.ebaystatic.com/cr/mscdn/7953f23caa56178e71c364f9814a6732/Money+back+guarantee+UK%403x.png" width="40" alt="eBay Money Back Guarantee logo" border="0" style="display:inline-block;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;line-height:17px;color:#FFFFFF;font-weight:bold;text-decoration:none;" class="w30" />
    </td>
    </tr>
    </table>
    </th>
    <th style="font-size:1px;line-height:1px;vertical-align:middle;" valign="middle" align="center" class="floatleft fullwidth left">
    <table width="480" border="0" cellspacing="0" cellpadding="0" align="left" class="fullwidth" role="presentation">
    <tr>
    <td style="font-size:1px;line-height:1px;" align="left" class="">
    <table width="480" border="0" cellspacing="0" cellpadding="0" align="center" class="fullwidth" role="presentation">
    <tr>
    <td height="32" style="font-size:1px;line-height:1px;padding:0px 24px 8px 0px;" align="left" class="pb4 pl24">
    <h2 style="mso-line-height-rule:exactly;margin:0;line-height:32px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:24px;color:#111820;font-weight:bold;text-decoration:none;" align="left" class="headline">
    Money Back Guarantee
    </h2>
    </td>
    </tr>
    <tr>
    <td height="21" style="font-size:1px;line-height:1px;padding:0px 24px 8px 0px;" align="left" class="pl24 pb24">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:21px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#111820;font-weight:normal;text-decoration:none;" align="left" class="fallbackfont subcopy">
    With the eBay Money Back Guarantee, we've got you covered. Receive your order or your money back – it's that easy.
    </p>
    </td>
    </tr>
    <tr>
    <td height="21" style="font-size:1px;line-height:1px;padding:0px 24px 0px 0px;" align="left" class="pb24 pl24">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:21px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;color:#111820;font-weight:700;text-decoration:underline;" align="left" class="fallbackfont">
    <a href="https://pages.ebay.co.uk/ebay-money-back-guarantee/?mkevt=1&mkpid=0&emsid=e11400.m145033.l153227&mkcid=7&ch=osgood&euid=ec979978cea742baaec4ea862883141c&bu=45592875971&exe=0&ext=0&osub=-1%7E1&crd=20230925181914&segname=11400" style="color:#111820;text-decoration:underline;" class="focus cta">
    <span class="focus__content" tabindex="-1">
    Learn more
    </span>
    </a>
    </p>
    </td>
    </tr>
    </table>
    </td>
    </tr>
    </table>
    </th>
    </tr>
    </table>
    </td>
    </tr>
    </table>
    </td>
    </tr>
    </table>
    <table width="600" bgcolor="#F7F7F7" border="0" cellspacing="0" cellpadding="0" align="center" class="footerMod fullwidth" role="presentation">
    <tr>
    <td valign="top" style="padding: 40px 16px 16px;">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" align="left" role="presentation">
    <tr>
    <td valign="top" align="left">
    <a href="https://www.ebay.co.uk/ulk/start/shop?mkevt=1&mkpid=0&emsid=e11400.m1852.l149990&mkcid=7&ch=osgood&euid=ec979978cea742baaec4ea862883141c&bu=45592875971&exe=0&ext=0&osub=-1%7E1&crd=20230925181914&segname=11400&mkevt=1&mkpid=0&emsid=e11400.m1852.l149990&mkcid=7&ch=osgood&euid=ec979978cea742baaec4ea862883141c&bu=45592875971&exe=0&ext=0&osub=-1%7E1&crd=20230925181914&segname=11400" target="_blank" class="focus" style="display: inline-block">
    <img src="https://secureir.ebaystatic.com/cr/mscdn/009a368c51d9e697acc4c9c13f9bc5d6/EBAY-LOGO-YUmcg.png" alt="eBay Logo" width="79" border="0" style="display:inline-block;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;line-height:17px;color:#111820;font-weight:bold;text-decoration:none;" class="light-image focus">
    <!--[if !mso]><!-->
    <div class="dark-image" style="display:none;overflow:hidden;float:left;width:0px;max-height:0px;max-width:0px;line-height:0px;visibility:hidden;">
    <img src="https://secureir.ebaystatic.com/cr/mscdn/4f21b716dbf816dac3f551990d80d9c2/EBAY-LOGO-dark-jIrfF.png" width="79" alt="eBay Logo" border="0" style="display:inline-block;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;line-height:17px;color:#111820;font-weight:bold;text-decoration:none;" class=" focus">
    </div>
    <!--<![endif]-->
    </a>
    </td>
    <td valign="top" align="right" >
    <table border="0" cellspacing="0" cellpadding="0" align="right" role="presentation">
    <tr>
    <td valign="top"style="padding-right: 16px;">
    <a href="https://www.ebayadservices.com/marketingtracking/v1/redirect?mpre=https%3A%2F%2Fwww.facebook.com%2FeBay.co.uk&mkevt=1&mkpid=0&emsid=e11400.m5219.l9641&mkcid=7&ch=osgood&euid=ec979978cea742baaec4ea862883141c&bu=45592875971&exe=0&ext=0&osub=-1%7E1&crd=20230925181914&segname=11400" target="_blank" class="focus" style="display: block">
    <img src="https://secureir.ebaystatic.com/cr/mscdn/3dd925153b74fae9863918b7750d0183/facebook-3Zomx.png" alt="facebook" width="32" border="0" style="display:inline-block;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;line-height:17px;color:#111820;font-weight:bold;text-decoration:none;" class="light-image focus">
    <!--[if !mso]><!-->
    <div class="dark-image" style="display:none;overflow:hidden;float:left;width:0px;max-height:0px;max-width:0px;line-height:0px;visibility:hidden;">
    <img src="https://secureir.ebaystatic.com/cr/mscdn/7581a7d369268b502a7ec75a72d540dc/facebook-dark-OZfEl.png" width="32" alt="facebook" border="0" style="display:inline-block;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;line-height:17px;color:#111820;font-weight:bold;text-decoration:none;" class=" focus">
    </div>
    <!--<![endif]-->
    </a>
    </td>
    <td valign="top"style="padding-right: 16px;">
    <a href="https://www.ebayadservices.com/marketingtracking/v1/redirect?mpre=https%3A%2F%2Fwww.instagram.com%2Febay_uk%2F&mkevt=1&mkpid=0&emsid=e11400.m5219.l9644&mkcid=7&ch=osgood&euid=ec979978cea742baaec4ea862883141c&bu=45592875971&exe=0&ext=0&osub=-1%7E1&crd=20230925181914&segname=11400" target="_blank" class="focus" style="display: block">
    <img src="https://secureir.ebaystatic.com/cr/mscdn/0d78f2625790856d7f6ec35d2e4cbfc6/instagram-qoyCT.png" alt="instagram" width="32" border="0" style="display:inline-block;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;line-height:17px;color:#111820;font-weight:bold;text-decoration:none;" class="light-image focus">
    <!--[if !mso]><!-->
    <div class="dark-image" style="display:none;overflow:hidden;float:left;width:0px;max-height:0px;max-width:0px;line-height:0px;visibility:hidden;">
    <img src="https://secureir.ebaystatic.com/cr/mscdn/97e7d93d220210823f210a912c51a9c2/instagram-dark-enD2l.png" width="32" alt="instagram" border="0" style="display:inline-block;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;line-height:17px;color:#111820;font-weight:bold;text-decoration:none;" class=" focus">
    </div>
    <!--<![endif]-->
    </a>
    </td>
    <td valign="top">
    <a href="https://www.ebayadservices.com/marketingtracking/v1/redirect?mpre=https%3A%2F%2Ftwitter.com%2FeBay_UK&mkevt=1&mkpid=0&emsid=e11400.m5219.l9642&mkcid=7&ch=osgood&euid=ec979978cea742baaec4ea862883141c&bu=45592875971&exe=0&ext=0&osub=-1%7E1&crd=20230925181914&segname=11400" target="_blank" class="focus" style="display: block">
    <img src="https://secureir.ebaystatic.com/cr/mscdn/71f381c19932bec76c1d64c961e12e74/X-icon-lightmode.png" alt="X" width="32" border="0" style="display:inline-block;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;line-height:17px;color:#111820;font-weight:bold;text-decoration:none;" class="light-image focus">
    <!--[if !mso]><!-->
    <div class="dark-image" style="display:none;overflow:hidden;float:left;width:0px;max-height:0px;max-width:0px;line-height:0px;visibility:hidden;">
    <img src="https://secureir.ebaystatic.com/cr/mscdn/19152476909c82b85f1a67836dc67ec7/X-icon-darkmode.png" width="32" alt="X" border="0" style="display:inline-block;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:14px;line-height:17px;color:#111820;font-weight:bold;text-decoration:none;" class=" focus">
    </div>
    <!--<![endif]-->
    </a>
    </td>
    </tr>
    </table>
    </td>
    </tr>
    </table>
    </td>
    </tr>
    <tr>
    <td valign="top" align="left" style="padding: 20px 16px 0px;">
    <table border="0" cellspacing="0" cellpadding="0" align="left" role="presentation">
    <tr>
    <td valign="top" style="padding-right: 16px;">
    <a href="https://www.ebay.com/ulk/start/shop?ul_alt=store&mkevt=1&mkpid=0&emsid=e11400.m1852.l3872&mkcid=7&ch=osgood&euid=ec979978cea742baaec4ea862883141c&bu=45592875971&exe=0&ext=0&osub=-1%7E1&crd=20230925181914&segname=11400" target="_blank" class="focus focus3" style="display:block">
    <img src="https://secureir.ebaystatic.com/cr/mscdn/05f55229ddf28e288c1b24f2b077a224/apple-store-gvKsT.png" alt="App Store" width="134" style="display:block;border:0">
    </a>
    </td>
    <td valign="top">
    <a href="https://www.ebay.com/ulk/start/shop?ul_alt=store&mkevt=1&mkpid=0&emsid=e11400.m1852.l3871&mkcid=7&ch=osgood&euid=ec979978cea742baaec4ea862883141c&bu=45592875971&exe=0&ext=0&osub=-1%7E1&crd=20230925181914&segname=11400" target="_blank" class="focus focus3" style="display:block">
    <img src="https://secureir.ebaystatic.com/cr/mscdn/cf962b9d55eebd75dcc4496a7b45f7e5/google-play-store-SSe2S.png" alt="Play Store" width="135" style="display:block;border:0">
    </a>
    </td>
    </tr>
    </table>
    </td>
    </tr>
    <tr>
    <td style="font-size:1px;line-height:1px;padding:0px 16px 48px 16px;" align="center">
    <table width="568" border="0" cellspacing="0" cellpadding="0" align="center" class="fullwidth" role="presentation">
    <tr>
    <td height="22" style="font-size:1px;line-height:1px;padding:24px 0px 0px 0px;" align="center">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:22px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:12px;color:#414141;font-weight:normal;text-decoration:none;" align="left">
    </p>
    </td>
    </tr>
    <tr>
    <td height="22" style="font-size:1px;line-height:1px;padding:4px 0px 0px 0px;" align="center">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:22px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:12px;color:#414141;font-weight:normal;text-decoration:none;" align="left">
    Update your <a href="https://commspreferences.ebay.co.uk/commsprefs?mkevt=1&mkpid=0&emsid=e11400.m1852.l1141&mkcid=7&ch=osgood&euid=ec979978cea742baaec4ea862883141c&bu=45592875971&exe=0&ext=0&osub=-1%7E1&crd=20230925181914&segname=11400" id="footerEmailPreferencesLink" style="color:#111820;text-decoration:underline!important;" class="focus focus3">email preferences</a>, <a href="https://marketing.ebay.co.uk/unsubscribe/home?token=AQAJAAAAgBwO5yBXMGn8d5DhCEtUTjxRGe48Lt3HYosqcwbl0Xd8Nep8g8Wm67VSZPeIJbGAN7QgFmQo-KGukgU_HsUwLpjqg2ax2xWPTcz7rQyUQ7OC_2jJcK8Hm-c5s8Dkd6wfrlaR8IOnFxzPeyUENdAt2IoBZdsldMZS_2PyDp5lujeI&mkevt=1&mkpid=0&emsid=e11400&mkcid=7&ch=osgood&euid=ec979978cea742baaec4ea862883141c&bu=45592875971&exe=0&ext=0&osub=-1%7E1&crd=20230925181914&segname=11400&mkevt=1&mkpid=0&emsid=e11400.m1852.l1142&mkcid=7&ch=osgood&euid=ec979978cea742baaec4ea862883141c&bu=45592875971&exe=0&ext=0&osub=-1%7E1&crd=20230925181914&segname=11400" id="footerUnsubscribeLink" style="color:#111820;text-decoration:underline!important;" class="focus focus3">unsubscribe</a> or learn about <a href="https://pages.ebay.co.uk/help/account/protecting-account.html?mkevt=1&mkpid=0&emsid=e11400.m1852.l3167&mkcid=7&ch=osgood&euid=ec979978cea742baaec4ea862883141c&bu=45592875971&exe=0&ext=0&osub=-1%7E1&crd=20230925181914&segname=11400" id="footerAccountProtectionLink" style="color:#111820;text-decoration:underline!important;" class="focus focus3">account protection</a>.<br>If you have a question, <a href="https://ocsnext.ebay.co.uk/ocs/home?mkevt=1&mkpid=0&emsid=e11400.m1852.l6369&mkcid=7&ch=osgood&euid=ec979978cea742baaec4ea862883141c&bu=45592875971&exe=0&ext=0&osub=-1%7E1&crd=20230925181914&segname=11400" id="footerContactUsLink" style="color:#111820;text-decoration:underline!important;" class="focus focus3">contact us</a>.
    </p>
    </td>
    </tr>
    <tr>
    <td height="22" style="font-size:1px;line-height:1px;padding:4px 0px 0px 0px;" align="center" class="footerPlaceholder">
    <p style="mso-line-height-rule:exactly;margin:0;line-height:22px;font-family:Helvetica,Arial,sans-serif,'Market Sans';font-size:12px;color:#414141;font-weight:normal;text-decoration:none;" align="left">
    &copy; 1995-2025 eBay Inc. or its affiliates
    </p>
    </td>
    </tr>
    </table>
    </td>
    </tr>
    </table>
    </body>
    </html>
    """
    
    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
