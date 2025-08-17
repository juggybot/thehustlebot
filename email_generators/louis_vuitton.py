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
    msg['From'] = formataddr((f'Louis Vuitton', sender_email))
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
    "Please enter the image url (MUST BE FROM LV SITE)",
    "Please enter the item name (LV Waimea Sunglasses):",
    "Please enter the reference number (Z1082E):",
    "Please enter the item colour (Black):",
    "Please enter the delivery date (13/09 and 15/09):",
    "Please enter the street address (487 Eve Way):",
    "Please enter the postcode & suburb (5726 New Graceland):",
    "Please enter the country (Australia):",
    "Please enter the currency ($/€/£):",
    "Please enter the product price (WITHOUT THE $ SIGN)",
    "Please enter the shipping price (WITHOUT THE $ SIGN)",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira a URL da imagem (DEVE SER DO SITE DA LV):",
    "Por favor, insira o nome do item (LV Waimea Sunglasses):",
    "Por favor, insira o número de referência (Z1082E):",
    "Por favor, insira a cor do item (Preto):",
    "Por favor, insira a data de entrega (13/09 e 15/09):",
    "Por favor, insira o endereço (487 Eve Way):",
    "Por favor, insira o código postal e o bairro (5726 New Graceland):",
    "Por favor, insira o país (Austrália):",
    "Por favor, insira a moeda ($/€/£):",
    "Por favor, insira o preço do produto (SEM O SÍMBOLO $):",
    "Por favor, insira o valor do frete (SEM O SÍMBOLO $):",
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
    part1 = "nx"
    part2 = random.randint(100000000, 999999999)  # Random 8-digit number

    # Combine the parts into order number
    order_number = f"{part1}-{part2}"
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
    subject = f"Thank you for your order"

    html_template = f"""
            <html xmlns="http://www.w3.org/1999/xhtml">

    <head>
        <meta name="generator" content="HTML Tidy for Java (vers. 2009-12-01), see jtidy.sourceforge.net" />
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <meta name="viewport" content="initial-scale=1.0, maximum-scale=1.0" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="format-detection" content="telephone=no" />
        <title>LOUIS VUITTON</title>
        <link rel="stylesheet" type="text/css" href="/data/css/louis.css">
    </head>

    <body style="margin:0;padding:0;" bgcolor="#FFFFFF" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0" offset="0">
        <center>
            <div id="container">
                <table width="100%" border="0" cellspacing="0" cellpadding="0" style="border-collapse:collapse;table-layout: fixed;" bgcolor="#FFFFFF">
                    <tr>
                        <td align="center">
                            <!-- begin spacer -->
                            <table width="640" class="w300" border="0" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" align="center" style="border-collapse:collapse;">
                                <tr>
                                    <td style="font-size:1px; line-height:1px !important;"><img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="1" height="20" style="display:block;" border="0" /></td>
                                </tr>
                            </table>
                            <!-- end spacer -->
                            <!-- begin body -->
                            <table width="642" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" class="w320" style="border-collapse:collapse;">
                                <tr>
                                    <td>
                                        <!-- begin filet -->
                                        <table width="642" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#F1F0EC" class="hide" style="border-collapse:collapse;">
                                            <tr>
                                                <td bgcolor="#F1F0EC" style="font-size:1px; line-height:1px !important;" class="hide">
                                                    <img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="1" height="1" style="display:block;" border="0" class="hide" />
                                                </td>
                                            </tr>
                                        </table>
                                        <!-- end filet -->
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <table width="642" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" class="w320" style="border-collapse:collapse;">
                                            <tr>
                                                <td width="1" bgcolor="#F1F0EC" class="hide" style="font-size:1px; line-height:1px !important;"><img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="1" height="1" style="display:block;" border="0" class="hide" /></td>
                                                <td width="640" align="center" class="w320">
                                                    <!-- begin logo vuitton -->
                                                    <table width="600" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" class="w300" style="border-collapse:collapse;">
                                                        <tr>
                                                            <td style="font-size:1px; line-height:1px !important;"><img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="1" height="20" style="display:block;" border="0" /></td>
                                                        </tr>
                                                        <tr>
                                                            <td align="center"><a href="https://uk.louisvuitton.com/eng-gb/homepage" target="_blank" title="LOUIS VUITTON"><img src="https://www.louisvuitton.com/images/lv_logo.png" width="214" height="24" alt="LOUIS VUITTON" style="display:block;" border="0" /></a></td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-size:1px; line-height:1px !important;"><img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="1" height="20" style="display:block;" border="0" /></td>
                                                        </tr>
                                                    </table>
                                                    <!-- end logo vuitton -->
                                                    <!-- begin filet -->
                                                    <table width="600" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#F1F0EC" class="w300" style="border-collapse:collapse;">
                                                        <tr>
                                                            <td style="font-size:1px; line-height:1px !important;"><img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="1" height="1" style="display:block;" border="0" /></td>
                                                        </tr>
                                                    </table>
                                                    <!-- end filet -->
                                                    <!-- begin intro -->
                                                    <table width="600" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" class="w300" style="border-collapse:collapse;">
                                                        <tr>
                                                            <td style="font-size:1px; line-height:1px !important;"><img src="https://uk.louisvuitton.com/static/23.18.0-RC/css/images/email/spacer.gif" width="1" height="20" style="display:block;" border="0" /></td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:12px; line-height:normal; color:#19110b; text-align:left; vertical-align:top;">Dear
                                                                {user_inputs[0]},<br />
                                                                <br />
                                                                Thank you for choosing Louis Vuitton.<br />
                                                                <br />
                                                                We are pleased to confirm that your order {order_num} has been
                                                                received and will be processed accordingly.<br />
                                                                <br />
                                                                To follow the status of your order, you can visit your <a href="https://secure.louisvuitton.com/eng-gb/mylv">MyLV</a>
                                                                account.
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-size:1px; line-height:1px !important;"><img src="https://uk.louisvuitton.com/static/23.18.0-RC/css/images/email/spacer.gif" width="1" height="20" style="display:block;" border="0" /></td>
                                                        </tr>
                                                    </table>
                                                    <!-- end intro -->
                                                    <table width="600" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" class="w300" style="border-collapse:collapse;">
                                                        <tr>
                                                            <td style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:14px; font-weight:bold; line-height:normal; color: #19110b; text-align:left; vertical-align:middle; padding-bottom:20px; padding-top:20px;"></td>
                                                        </tr>
                                                    </table>
                                                    <table width="600" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" class="w300" style="border-collapse:collapse;">
                                                        <tr>
                                                            <td style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:14px; line-height:normal; color:#19110b; text-align:left; vertical-align:middle; padding-bottom:5px; padding-top:5px;"><strong>ORDER
                                                                    DETAILS</strong>
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-size:1px; line-height:1px !important;"><img src="https://uk.louisvuitton.com/static/23.18.0-RC/css/images/email/spacer.gif" width="1" height="10" style="display:block;" border="0" /></td>
                                                        </tr>
                                                    </table>
                                                    <table width="600" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#F6F5F3" class="w300" style="border-collapse:collapse;">
                                                        <tr>
                                                            <td width="100" style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:12px; line-height:normal; color:#19110b; text-align:center; vertical-align:middle; padding-top:10px; padding-bottom:10px;"><strong>Product</strong></td>
                                                            <td width="300" style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:12px; line-height:normal; color:#19110b; text-align:left; vertical-align:middle; padding-top:10px; padding-bottom:10px; padding-left:10px;"><strong>Description</strong></td>
                                                            <td width="100" style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:12px; line-height:normal; color:#19110b; text-align:center; vertical-align:middle; padding-top:10px; padding-bottom:10px;"><strong>Quantity</strong></td>
                                                            <td width="100" style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 12px; line-height: normal; color: #19110b; text-align: right; vertical-align: middle; padding-top: 10px; padding-bottom: 10px; padding-right: 10px;"><strong>Price</strong></td>
                                                        </tr>
                                                    </table>
                                                    <!-- end spacer -->
                                                    <table width="600" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" class="w300" style="border-collapse:collapse;">
                                                        <tr>
                                                            <td width="400" class="w150">
                                                                <table width="100%" border="0" align="left" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" style="border-collapse:collapse;">
                                                                    <tr>
                                                                        <td align="left">
                                                                            <table bgcolor="#FFFFFF" border="0" align="left" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
                                                                                <tr>
                                                                                    <td align="left" valign="middle" id="prodImg" style="position: relative; bottom: 40px;"><img src="{user_inputs[1]}" alt="image" width="100" /></td>
                                                                                </tr>
                                                                            </table>
                                                                            <table width="250" bgcolor="#FFFFFF" border="0" align="left" cellpadding="0" cellspacing="0" style="border-collapse:collapse;" class="w150">
                                                                                <tr>
                                                                                    <td width="10" style="font-size:1px; line-height:1px !important;">
                                                                                        <img src="https://uk.louisvuitton.com/static/23.18.0-RC/css/images/email/spacer.gif" width="1" height="10" style="display:block;" border="0" />
                                                                                    </td>
                                                                                    <td align="left" style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:12px; line-height:normal; color:#19110b; text-align:left; vertical-align:top; padding-top:10px; padding-bottom:10px;">
                                                                                        <font color="#19110B">
                                                                                            <!-- Display SKU Name -->
                                                                                            <a href="#commande1#" target="_blank" title="#Titre1#" style=" text-decoration:none; color:#19110b;">{user_inputs[2]}
                                                                                            </a><br />
                                                                                            <!-- Display Reference --> Reference : <strong class="lv-product__sku overline">
                                                                                                {user_inputs[3]}
                                                                                                <!-- --></strong><br />
                                                                                            <!-- Display Material --> Product Main Colour : {user_inputs[4]}<br />
                                                                                        </font>
                                                                                    </td>
                                                                                </tr>
                                                                            </table>
                                                                        </td>
                                                                    </tr>
                                                                </table>
                                                            </td>
                                                            <td width="100" align="center" valign="top" class="w70" style="padding-top:10px; padding-bottom:10px;">
                                                                <table border="0" cellspacing="0" cellpadding="0" align="center" style="border-collapse:collapse;">
                                                                    <tr>
                                                                        <td style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:12px; line-height:normal; color:#19110b; text-align:center; vertical-align:top;">1</td>
                                                                    </tr>
                                                                </table>
                                                            </td>
                                                            <td width="100" valign="top" class="w80">
                                                                <table width="100%" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" style="border-collapse:collapse;">
                                                                    <tr>
                                                                        <td style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:12px; line-height:normal; color:#19110b; text-align:right; vertical-align:middle; padding-top:10px; padding-bottom:10px;">{user_inputs[9]}{user_inputs[10]}<br /></td>
                                                                        <td width="10" style="font-size:1px; line-height:1px !important;">
                                                                            <img src="https://uk.louisvuitton.com/static/23.18.0-RC/css/images/email/spacer.gif" width="1" height="10" style="display:block;" border="0" />
                                                                        </td>
                                                                    </tr>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                    <!-- begin line sous-total -->
                                                    <table width="600" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#F6F5F3" class="w300" style="border-collapse:collapse;">
                                                        <tr>
                                                            <td width="500" valign="top" class="w220">
                                                                <table width="100%" border="0" align="center" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
                                                                    <tr>
                                                                        <td width="10" style="font-size:1px; line-height:1px !important;">
                                                                            <img src="https://uk.louisvuitton.com/static/23.18.0-RC/css/images/email/spacer.gif" width="1" height="10" style="display:block;" border="0" />
                                                                        </td>
                                                                        <td style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:12px; line-height:normal; color:#19110b; text-align:left; vertical-align:middle; padding-top:10px; padding-bottom:10px;">Subtotal</td>
                                                                    </tr>
                                                                </table>
                                                            </td>
                                                            <td width="100" valign="top" class="w80">
                                                                <table width="100%" border="0" align="center" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
                                                                    <tr>
                                                                        <td style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:12px; line-height:normal; color:#19110b; text-align:right; vertical-align:middle; padding-top:10px; padding-bottom:10px;">{user_inputs[9]}{user_inputs[10]}</td>
                                                                        <td width="10" style="font-size:1px; line-height:1px !important;">
                                                                            <img src="https://uk.louisvuitton.com/static/23.18.0-RC/css/images/email/spacer.gif" width="1" height="10" style="display:block;" border="0" />
                                                                        </td>
                                                                    </tr>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                    <!-- end line sous-total -->
                                                    <table width="600" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" class="w300" style="border-collapse:collapse;">
                                                        <tr>
                                                            <td width="500" valign="top" class="w220">
                                                                <table width="100%" border="0" align="center" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
                                                                    <tr>
                                                                        <td width="10" style="font-size:1px; line-height:1px !important;">
                                                                            <img src="https://uk.louisvuitton.com/static/23.18.0-RC/css/images/email/spacer.gif" width="1" height="10" style="display:block;" border="0" />
                                                                        </td>
                                                                        <td style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:12px; line-height:normal; color:#19110b; text-align:left; vertical-align:middle; padding-top:10px; padding-bottom:10px;">DELIVERY
                                                                            : Express home delivery estimated between {user_inputs[5]}
                                                                        </td>
                                                                    </tr>
                                                                </table>
                                                            </td>
                                                            <td width="100" valign="top" class="w80">
                                                                <table width="100%" border="0" align="center" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
                                                                    <tr>
                                                                        <td style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:12px; line-height:normal; color:#19110b; text-align:right; vertical-align:middle; padding-top:10px; padding-bottom:10px;">{user_inputs[9]}{user_inputs[11]}</td>
                                                                        <td width="10" style="font-size:1px; line-height:1px !important;">
                                                                            <img src="https://uk.louisvuitton.com/static/23.18.0-RC/css/images/email/spacer.gif" width="1" height="10" style="display:block;" border="0" />
                                                                        </td>
                                                                    </tr>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                    <!-- end Shipping -->
                                                    <!-- begin Additional Fee -->
                                                    <!-- end Additional Fee --><!-- begin Taxe 1 -->
                                                    <!-- end Taxe 1 -->
                                                    <!-- start credit note only if exchange with higher price order  -->
                                                    <!-- End of crdit not only if exchange with higher price order  -->
                                                    <!--     begin spacer -->
                                                    <!--     <table width="600" class="w300" border="0" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" align="center" style="border-collapse:collapse;"> -->
                                                    <!--       <tr> -->
                                                    <!--         <td style="font-size:1px; line-height:1px !important;"> -->
                                                    <!--         </td> -->
                                                    <!--       </tr> -->
                                                    <!--     </table> -->
                                                    <!-- end spacer -->
                                                    <!-- begin TOTAL -->
                                                    <!-- begin spacer -->
                                                    <table width="600" class="w300" border="0" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" align="center" style="border-collapse:collapse;">
                                                        <tr>
                                                            <td style="font-size:1px; line-height:1px !important;"><img src="https://uk.louisvuitton.com/static/23.18.0-RC/css//images/email/spacer.gif" width="1" height="10" style="display:block;" border="0" /></td>
                                                        </tr>
                                                    </table>
                                                    <!-- end spacer -->
                                                    <table width="600" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#F6F5F3" class="w300" style="border-collapse:collapse;">
                                                        <tr>
                                                            <td width="300" valign="top" class="w150">
                                                                <table width="100%" border="0" align="center" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
                                                                    <tr>
                                                                        <td width="10" style="font-size:1px; line-height:1px !important;"></td>
                                                                        <td style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:14px; line-height:normal; color:#19110b; text-align:left; vertical-align:middle; padding-top:10px; padding-bottom:10px;"><strong>Total</strong></td>
                                                                    </tr>
                                                                </table>
                                                            </td>
                                                            <td width="300" valign="top" class="w150">
                                                                <table width="100%" border="0" align="center" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
                                                                    <tr>
                                                                        <td style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:14px; line-height:normal; color:#19110b; text-align:right; vertical-align:middle; padding-top:10px; padding-bottom:10px;"><strong>{user_inputs[9]}{user_inputs[10]}</strong></td>
                                                                        <td width="10" style="font-size:1px; line-height:1px !important;"></td>
                                                                    </tr>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                    <!-- end TOTAL -->
                                                    <!-- begin adresses -->
                                                    <table bgcolor="#FFFFFF" width="600" border="0" align="center" cellpadding="0" cellspacing="0" style="border-collapse:collapse;" class="w300">
                                                        <tr>
                                                            <td valign="top" bgcolor="#FFFFFF">
                                                                <table class="w300" bgcolor="#FFFFFF" width="290" border="0" align="left" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
                                                                    <tr>
                                                                        <td align="left" valign="top" bgcolor="#FFFFFF" style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:12px; line-height:normal; color:#19110b; text-align:left; vertical-align:top; padding-top:10px; padding-bottom:10px; padding-left:10px;"><strong>Delivery
                                                                                address</strong>
                                                                        </td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td bgcolor="#E1DFD8" style="font-size:1px; line-height:1px !important;"><img src="https://uk.louisvuitton.com/static/23.18.0-RC/css/images/email/spacer.gif" width="1" height="1" style="display:block;" border="0" /></td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td align="left" valign="top" bgcolor="#FFFFFF" style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:12px; line-height:normal; color:#19110b; text-align:left; vertical-align:top; padding-top:10px; padding-bottom:10px; padding-left:10px;">Mr
                                                                            {user_inputs[0]}<br />
                                                                            {user_inputs[6]}<br />
                                                                            {user_inputs[7]}<br />
                                                                            {user_inputs[8]}<br />
                                                                        </td>
                                                                    </tr>
                                                                </table>
                                                                <!--[if gte mso 9]>
                                                    </td>
                                                    <td valign="top" bgcolor="#FFFFFF">
                                                        <![endif]-->
                                                                <table class="w300" bgcolor="#FFFFFF" width="290" border="0" align="right" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
                                                                    <tr>
                                                                        <td align="left" valign="top" bgcolor="#FFFFFF" style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:12px; line-height:normal; color:#19110b; text-align:left; vertical-align:top; padding-top:10px; padding-bottom:10px; padding-left:10px;"><strong>Billing
                                                                                address</strong>
                                                                        </td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td bgcolor="#E1DFD8" style="font-size:1px; line-height:1px !important;"><img src="https://uk.louisvuitton.com/static/23.18.0-RC/css/images/email/spacer.gif" width="1" height="1" style="display:block;" border="0" /></td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td align="left" valign="top" bgcolor="#FFFFFF" style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:12px; line-height:normal; color:#19110b; text-align:left; vertical-align:top; padding-top:10px; padding-bottom:10px; padding-left:10px;">Mr
                                                                            {user_inputs[0]}<br />
                                                                            {user_inputs[6]}<br />
                                                                            {user_inputs[7]}<br />
                                                                            {user_inputs[8]}<br />
                                                                        </td>
                                                                    </tr>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                    <!-- end adresses -->
                                                    <!--     begin spacer -->
                                                    <table width="600" class="w300" border="0" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" align="center" style="border-collapse:collapse;">
                                                        <tr>
                                                            <td style="font-size:1px; line-height:1px !important;"><img src="https://uk.louisvuitton.com/static/23.18.0-RC/css/images/email/spacer.gif" width="1" height="10" style="display:block;" border="0" /></td>
                                                        </tr>
                                                    </table>
                                                    <!--     begin spacer -->
                                                    <table width="600" class="w300" border="0" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" align="center" style="border-collapse:collapse;">
                                                        <tr>
                                                            <td style="font-size:1px; line-height:1px !important;"><img src="https://uk.louisvuitton.com/static/23.18.0-RC/css/images/email/spacer.gif" width="1" height="10" style="display:block;" border="0" /></td>
                                                        </tr>
                                                    </table>
                                                    <!-- begin conclusion -->
                                                    <table width="600" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" class="w300" style="border-collapse:collapse;">
                                                        <tr>
                                                            <td style="font-family: Arial, Futura, Georgia, Helvetica, sans-serif; font-size:12px; line-height:normal; color:#2b130f; text-align:left; vertical-align:top;">Consult
                                                                our <a href="https://uk.louisvuitton.com/eng-gb/delivery-and-returns-">Returns
                                                                    policy</a>.<br />
                                                                Consult our <a href="https://uk.louisvuitton.com/eng-gb/legal-privacy" target="_blank" style="color:#19110b;" title="Terms and Conditions">
                                                                    <font color="#C8A985">Terms and
                                                                        Conditions</font>
                                                                </a>.<br />
                                                                <br />
                                                                Should you require information or help during your journey, our
                                                                Client Services team will be delighted to assist you.<br />
                                                                <br />
                                                            </td>
                                                        </tr>
                                                    </table>
                                                    <!-- end conclusion
                                                <!== begin signature -->
                                                    <table width="600" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" class="w300" style="border-collapse:collapse;">
                                                        <tr>
                                                            <td style="font-size:1px; line-height:1px !important;"><img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="1" height="20" style="display:block;" border="0" /></td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-family: Arial, Futura, Georgia, Helvetica, sans-serif; font-size:12px; line-height:normal; color:#2b130f; text-align:left; vertical-align:top;">Warm
                                                                regards, Louis Vuitton Client Services<br />
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-size:1px; line-height:1px !important;"><img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="1" height="20" style="display:block;" border="0" /></td>
                                                        </tr>
                                                    </table>
                                                    <!-- end signature -->
                                                    <!-- begin filet -->
                                                    <table width="600" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#F1F0EC" class="w300" style="border-collapse:collapse;">
                                                        <tr>
                                                            <td style="font-size:1px; line-height:1px !important;"><img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="1" height="1" style="display:block;" border="0" /></td>
                                                        </tr>
                                                    </table>
                                                    <!-- end filet -->
                                                    <!-- begin body desk -->
                                                    <table width="600" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" class="w300" style="border-collapse:collapse;">
                                                        <tr>
                                                            <td style="font-size:1px; line-height:1px !important;"><img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="1" height="20" style="display:block;" border="0" /></td>
                                                        </tr>
                                                    </table>
                                                    <table width="480" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" class="hide" style="border-collapse:collapse;">
                                                        <tr>
                                                            <td><a href="https://uk.louisvuitton.com" target="_blank" title=""><img src="https://www.louisvuitton.com/images/is/image/lv/footer_email" width="480" height="223" alt="" style="display:block;" border="0" class="hide" /></a></td>
                                                        </tr>
                                                    </table>
                                                    <!-- end body desk -->
                                                    <!-- begin body mobile -->
                                                    <table width="300" border="0" cellspacing="0" cellpadding="0" style="border-collapse:collapse;display:none;font-size:0;max-height:0;line-height:0;mso-hide:all;" class="ShowMobile" align="center">
                                                        <tr>
                                                            <td><a href="https://uk.louisvuitton.com" target="_blank" title=""><img src="https://www.louisvuitton.com/images/is/image/lv/footer_email" width="0" height="0" alt="" style="display:none;" border="0" class="imgMainMobile" /></a></td>
                                                        </tr>
                                                    </table>
                                                    <!-- end body mobile -->
                                                    <!-- begin visitez -->
                                                    <table width="600" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" class="hide" style="border-collapse:collapse;">
                                                        <tr>
                                                            <td style="font-size:1px; line-height:1px !important;" class="hide"><img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="1" height="15" style="display:block;" border="0" class="hide" /></td>
                                                        </tr>
                                                        <tr>
                                                            <td align="right" class="hide">
                                                                <table align="right" border="0" cellspacing="0" cellpadding="0" class="hide" style="border-collapse:collapse;">
                                                                    <tr>
                                                                        <td style="font-size:1px; line-height:1px !important;" class="hide"></td>
                                                                        <td width="10" style="font-size:1px; line-height:1px !important;" class="hide"><img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="10" height="1" style="display:block;" border="0" class="hide" /></td>
                                                                        <td class="hide" style="font-family:Futura, Georgia, Arial, Helvetica; font-size:12px; line-height:normal; color:#2b130f; text-align:left; vertical-align:middle;"></td>
                                                                    </tr>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-size:1px; line-height:1px !important;" class="hide"><img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="1" height="15" style="display:block;" border="0" class="hide" /></td>
                                                        </tr>
                                                    </table>
                                                    <!-- end visitez -->
                                                    <!-- begin RS desk -->
                                                    <table width="640" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#F1F0EC" class="w150" style="border-collapse:collapse;">
                                                        <tr>
                                                            <td align="center">
                                                                <table bgcolor="#F1F0EC" width="640" border="0" align="left" cellpadding="0" cellspacing="0" style="border-collapse:collapse;" class="w320">
                                                                    <tr>
                                                                        <td width="640" style="font-size:1px; line-height:1px !important;">
                                                                            <img src="https://ceo-be.multimediabs.com/attachments/hosted/v2/imagec1d2f27c-0839-4339-b8da-7b0c77ada670" width="640" height="30" style="display:block;" border="0" />
                                                                        </td>
                                                                    </tr>
                                                                </table>
                                                                <table align="center" width="272" border="0" cellspacing="0" cellpadding="0" class="w320" style="border-collapse:collapse;">
                                                                    <tr>
                                                                        <td width="10" style="font-size:1px; line-height:1px !important;">
                                                                            <img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="10" height="1" style="display:block;" border="0" />
                                                                        </td>
                                                                        <td valign="middle" style="font-size:1px; line-height:1px !important;"><a href="https://uk.louisvuitton.com/eng-gb/apps" target="_blank" title="LV Pass"><img src="https://eu.louisvuitton.com/images/is/image/lv/1/LV/louis-vuitton--tpl_rs_lv.png" width="22" height="22" alt="LV Pass" style="display:block;" border="0" class="ImgPictoRSMobile" /></a></td>
                                                                        <td width="10" style="font-size:1px; line-height:1px !important;" class="hide"><img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="5" height="1" style="display:block;" border="0" class="hide" /></td>
                                                                        <td valign="middle" style="font-size:1px; line-height:1px !important;"><a href="https://www.facebook.com/LouisVuitton/" target="_blank" title="Facebook"><img src="https://eu.louisvuitton.com/images/is/image/lv/1/LV/louis-vuitton--tpl_rs_facebook.png" width="22" height="22" alt="Facebook" style="display:block;" border="0" class="ImgPictoRSMobile" /></a></td>
                                                                        <td width="10" style="font-size:1px; line-height:1px !important;" class="hide"><img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="5" height="1" style="display:block;" border="0" class="hide" /></td>
                                                                        <td valign="middle" style="font-size:1px; line-height:1px !important;"><a href="https://twitter.com/louisvuitton" target="_blank" title="twitter"><img src="https://eu.louisvuitton.com/images/is/image/lv/1/LV/louis-vuitton--tpl_rs_twitter.png" width="22" height="22" alt="twitter" style="display:block;" border="0" class="ImgPictoRSMobile" /></a></td>
                                                                        <td width="10" style="font-size:1px; line-height:1px !important;" class="hide"><img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="5" height="1" style="display:block;" border="0" class="hide" /></td>
                                                                        <td valign="middle" style="font-size:1px; line-height:1px !important;"><a href="https://www.youtube.com/louisvuitton" target="_blank" title="YouTube"><img src="https://eu.louisvuitton.com/images/is/image/lv/1/LV/louis-vuitton--tpl_rs_youtube.png" width="22" height="22" alt="YouTube" style="display:none;" border="0" class="ImgPictoRSMobile" /></a></td>
                                                                        <td width="10" style="font-size:1px; line-height:1px !important;">
                                                                            <img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="5" height="1" style="display:block;" border="0" />
                                                                        </td>
                                                                        <td valign="middle" style="font-size:1px; line-height:1px !important;"><a href="https://uk.louisvuitton.com/eng-gb/la-maison/louis-vuitton-on-snapchat" target="_blank" title="Snapchat"><img src="https://eu.louisvuitton.com/images/is/image/lv/1/LV/louis-vuitton--tpl_rs_snapchat.png" width="22" height="22" alt="Snapchat" style="display:block;" border="0" class="ImgPictoRSMobile" /></a></td>
                                                                        <td width="10" style="font-size:1px; line-height:1px !important;" class="hide"><img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="5" height="1" style="display:block;" border="0" class="hide" /></td>
                                                                        <td valign="middle" style="font-size:1px; line-height:1px !important;"><a href="https://www.instagram.com/louisvuitton/" target="_blank" title="instagram"><img src="https://eu.louisvuitton.com/images/is/image/lv/1/LV/louis-vuitton--tpl_rs_instagram.png" width="22" height="22" alt="instagram" style="display:block;" border="0" class="ImgPictoRSMobile" /></a></td>
                                                                        <td width="10" style="font-size:1px; line-height:1px !important;" class="hide"><img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="5" height="1" style="display:block;" border="0" class="hide" /></td>
                                                                        <td valign="middle" style="font-size:1px; line-height:1px !important;"><a href="https://www.pinterest.com/LouisVuitton/" target="_blank" title="Pinterest"><img src="https://eu.louisvuitton.com/images/is/image/lv/1/LV/louis-vuitton--tpl_rs_pinterest.png" width="22" height="22" alt="Pinterest" style="display:block;" border="0" class="ImgPictoRSMobile" /></a></td>
                                                                    </tr>
                                                                </table>
                                                                <table bgcolor="#F1F0EC" width="640" border="0" align="left" cellpadding="0" cellspacing="0" style="border-collapse:collapse;" class="w320">
                                                                    <tr>
                                                                        <td width="640" style="font-size:1px; line-height:1px !important;">
                                                                            <img src="https://ceo-be.multimediabs.com/attachments/hosted/v2/imagec1d2f27c-0839-4339-b8da-7b0c77ada670" width="640" height="30" style="display:block;" border="0" />
                                                                        </td>
                                                                    </tr>
                                                                </table>
                                                                <!-- end RS desk -->
                                                            </td>
                                                            <td width="1" bgcolor="#F1F0EC" class="hide" style="font-size:1px; line-height:1px !important;"><img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="1" height="1" style="display:block;" border="0" class="hide" /></td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                        <!-- end body -->
                                        <!-- BEGIN ML -->
                                        <table width="640" align="center" class="w300" border="0" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
                                            <tr>
                                                <td style="font-size:1px; line-height:1px;"><img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="1" height="20" style="display:block; border:0;" /></td>
                                            </tr>
                                            <tr>
                                                <td align="center" style="font-family: Arial, Futura, Georgia, Helvetica, sans-serif; color:#000000; font-size:10px; line-height:normal;">
                                                    <font color="#000000"><a href="https://uk.louisvuitton.com/eng-gb/legal-privacy" target="_blank" style="text-decoration:underline;color:#000000;" title="Legal Notice">
                                                            <font color="#000000">Legal Notice</font>
                                                        </a>
                                                        &#169; &#8203;2025 Louis Vuitton<br />
                                                        <br />
                                                        You may access your personal information and modify or delete
                                                        it.<br />
                                                        If needed, please send an email at: <a href="mailto:uk@contact.louisvuitton.com" style="text-decoration:underline;color:#000000;">
                                                            <font color="#000000">uk@contact.louisvuitton.com</font>
                                                        </a>
                                                    </font><br />
                                                    We look forward to continuing our journey together soon! Warm
                                                    regards, Louis Vuitton Client Services
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="font-size:1px; line-height:1px;"><img src="https://www.louisvuitton.com/static/css/images/email/spacer.gif" width="1" height="20" style="display:block; border:0;" /></td>
                                            </tr>
                                        </table>
                                        <!-- END ML -->
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </div>
        </center>
    </body>

    </html>
    """

    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
