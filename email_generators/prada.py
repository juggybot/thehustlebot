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
    msg['From'] = formataddr((f'Prada', sender_email))
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
    "Please enter the image url (jpg, jpeg, png):",
    "Please enter the product name (Prada Symbole sunglasses):",
    "Please enter the product code (SPR17W_E1AB_F05S0_C_049):",
    "Please enter the product price (WITHOUT THE $):",
    "Please enter the product color (BLACK):",
    "Please enter the product size (S/M/L):",
    "Please enter the shipping cost (WITHOUT THE $):",
    "Please enter the tax amount (WITHOUT THE $):",
    "Please enter the order total (WITHOUT THE $):",
    "Please enter the street address (4211 Bahringer Place):",
    "Please enter the postcode (3709):",
    "Please enter the suburb (Williamston):",
    "Please enter the country (Australia):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira a URL da imagem (jpg, jpeg, png):",
    "Por favor, insira o nome do produto (Óculos de sol Prada Symbole):",
    "Por favor, insira o código do produto (SPR17W_E1AB_F05S0_C_049):",
    "Por favor, insira o preço do produto (SEM O SÍMBOLO $):",
    "Por favor, insira a cor do produto (PRETO):",
    "Por favor, insira o tamanho do produto (P/M/G):",
    "Por favor, insira o custo de envio (SEM O SÍMBOLO $):",
    "Por favor, insira o valor do imposto (SEM O SÍMBOLO $):",
    "Por favor, insira o total do pedido (SEM O SÍMBOLO $):",
    "Por favor, insira o endereço (4211 Bahringer Place):",
    "Por favor, insira o código postal (3709):",
    "Por favor, insira o bairro (Williamston):",
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
    part1 = "PR"
    part2 = random.randint(10000000, 99999999)  # Random 8-digit number

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
    recipient_email = f'{user_inputs[15]}'
    subject = f"Prada - Order acknowledgement - {order_num}"

    html_template = f"""
        <html>
        <body style="margin: 0; padding: 0px; background: #FFFFFF;">
        <table class="wrp" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none; min-width: 600px;" border="0" cellpadding="0" cellspacing="0" align="center" width="100%" bgcolor="#FFFFFF">
            <tr>
                <td class="wrp" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none; min-width: 600px;" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
                <table group_name="Container" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" class=""  bgcolor="#f4f5f7">
                    <!-- logo -->
                    <tr>
                        <td>
                            <table group_name="Header with Logo" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" class=""  bgcolor="#f4f5f7">
                            <tr>
                                <td style="padding: 0px; vertical-align: top; width: 10px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="10" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 580px;" class="padded" align="center">
                                    <table style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
                                        <tr>
                                        <td style="padding: 0px; vertical-align: top; width: 580px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 10px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                            height="10" border="0"></td>
                                        </tr>
                                        <tr block_name="Fluid Image">
                                        <td style="padding: 0px; width: 580px; font-size: 0; line-height: 1px; height: 1px; vertical-align: top" class="padded" align="center"><a href="#" target="_blank"> <img
                                            style="font-size: 0; margin: 0px; padding: 0px; display: inline;" src="https://1000logos.net/wp-content/uploads/2017/05/Prada-Logo.png" width="80" height="47" border="0" alt="">
                                            </a>
                                        </td>
                                        </tr>
                                        <tr>
                                        <td style="padding: 0px; vertical-align: top; width: 580px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 10px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                            height="10" border="0"></td>
                                        </tr>
                                    </table>
                                </td>
                                <td style="padding: 0px; vertical-align: top; width: 10px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="10" height="1" border="0"></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- img header big -->
                    <tr>
                        <td>
                            <table group_name="Header Img" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" class=""  bgcolor="#f4f5f7">
                            <tr block_name="Double Image">
                                    <span item_name="Desktop image">
                                    <img style="font-size:0; margin: 0px; padding: 0px; display: block;" src="https://assets.prada.com/content/dam/transactional/prada/banner/prada-galleria-milano-e1545421650426-600x233.jpg" width="600" border="0" alt="Alt Text" class="onlydesktop">
                                    </span>
                                    <span item_name="Mobile image">
                                        <div class="mobileversion" style="display: none; width: 0; overflow: hidden; max-height:0; min-height: 0; margin: 0; padding: 0; font-size:0; line-height:1px; height: 0px; vertical-align: top">
                                        <img src="https://assets.prada.com/content/dam/transactional/prada/banner/prada-galleria-milano-e1545421650426-600x233.jpg" width="320" border="0" alt="Alt Text" style="margin: 0px; padding: 0px; display:inline; width: 0px; max-height:0px;" class="mobileversion">
                                        </div>
                                    </span>
                                </td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- heading client -->
                    <tr>
                        <td>
                            <table group_name="Heading" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="left" class=""  bgcolor="#f4f5f7">
                            <tr>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 480px;" class="padded" align="center">
                                    <table style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
                                        <tr>
                                        <td style="padding: 0px; vertical-align: top; width: 480px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 40px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                            height="40" border="0"></td>
                                        </tr>
                                        <tr block_name="Client Name" >
                                        <td style="padding: 0px; vertical-align:top; width:480px; font-family: Arial, Helvetica, sans-serif; font-size: 14px; line-height: 20px; color:#000000;" class="padded" align="left">
                                            Dear
                                            {user_inputs[0]},
                                            <br><br>
                                        </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table group_name="Text" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" class=""  bgcolor="#f4f5f7">
                            <tr>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 480px;" class="padded" align="center">
                                    <table style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
                                        <tr>
                                        <td style="padding: 0px; vertical-align:top; width:580px; font-family: Arial, Helvetica, sans-serif; font-size: 14px; line-height: 21px; color:#000001;" class="padded" align="left">
                                            Thanks for shopping with Prada.
                                            <br><br>
                                            We received your order and we are currently processing it. We will notify you via e-mail as soon as your order is shipped.
                                            <br><br>
                                            We hope you enjoyed your shopping experience with us and we look forward to welcoming you again on prada.com.
                                            <br>
                                            <br>Order Number <br><b>{order_num}</b><br>
                                        </td>
                                        </tr>
                                    </table>
                                </td>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table group_name="Your Order" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" class=""  bgcolor="#f4f5f7">
                            <tr>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 480px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 20px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1" height="20"border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                            </tr>
                            <tr>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 480px;" class="padded" align="center">
                                    <table style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
                                        <tr block_name="Your Order" >
                                        <td style="padding: 0px; vertical-align:top; width:480px; font-family:  Arial, Helvetica, sans-serif; font-size: 14px; line-height: 20px; color:#000001; text-decoration: none;" class="padded" align="left">
                                            Please find below your order details:
                                        </td>
                                        </tr>
                                    </table>
                                </td>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                            </tr>
                            <tr>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 480px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 30px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1" height="30"border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table group_name="Product item" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" bgcolor="#f4f5f7">
                            <tr>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 480px;" class="paddedSmall" align="center">
                                    <table style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" width="100%" bgcolor="#FFFFFF">
                                        <tr>
                                        <td style="padding: 0px; vertical-align: top; width: 40px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="10" height="1" border="0"></td>
                                        <td style="padding: 0px; vertical-align: top; width: 400px;" class="padded" align="center">
                                            <table style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" width="100%" bgcolor="#FFFFFF">
                                                <tr>
                                                    <td style="padding: 0px; vertical-align: top; width: 400px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 30px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                                    height="30" border="0"></td>
                                                </tr>
                                                <tr>
                                                    <td>
                                                    <table class="two-col" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
                                                        <tr>
                                                            <td style="padding: 0px; vertical-align: top; width: 400px;">
                                                                <table class="columns" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none; width: 400px;" border="0" cellpadding="0" cellspacing="0" align="center">
                                                                <tr>
                                                                    <td style="padding: 0px; vertical-align: top;">
                                                                        <table block_name="Product Image" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="left">
                                                                            <tr>
                                                                            <td style="padding: 0px; vertical-align: top; width: 140px;" class="column">
                                                                                <table style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center">
                                                                                    <tr item_name="Image">
                                                                                        <td style="padding: 0px; vertical-align: top; width: 120px;" class="padded" align="center"><img style="margin: 0px; padding: 0px; display: inline;" src="{user_inputs[1]}"  width="130" alt="Product" border="0" /></td>
                                                                                    </tr>
                                                                                    <tr>
                                                                                        <td style="padding: 0px; vertical-align: top; width: 120px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 10px;" src="https://www.prada.com/content/dam/pradabkg_products/S/SPR/SPR17W/E1ABF05S0/SPR17W_E1AB_F05S0_C_049_SLF.jpg" width="1" height="10" border="0"></td>
                                                                                    </tr>
                                                                                </table>
                                                                            </td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                    <td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;vertical-align:top;" >
                                                                        <table lock_name="Column Info" style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="right" >
                                                                            <tr>
                                                                            <td style="padding: 0px; vertical-align:top; width:230px;" class="paddedSmall">
                                                                                <table style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none; width:100%" border="0" cellpadding="0" cellspacing="0" align="left">
                                                                                    <!-- product name -->
                                                                                    <tr item_name="product_name" >
                                                                                        <td style="padding: 0px; vertical-align:top; font-family:  Arial, Helvetica, sans-serif; font-size: 16px; color:#000000; text-decoration: none;" class="padded" align="left">
                                                                                        {user_inputs[2]}
                                                                                        </td>
                                                                                    </tr>
                                                                                    <!-- product code -->
                                                                                    <tr item_name="product_code" >
                                                                                        <td style="padding: 0px; vertical-align:top; font-family:  Arial, Helvetica, sans-serif; font-size: 10px; color:#000000; text-decoration: none; line-height: 2.15; letter-spacing: 0.3px;" class="padded" align="left">
                                                                                        PRODUCT CODE :</br>  {user_inputs[3]}<br>
                                                                                        </td>
                                                                                    </tr>
                                                                                    <!-- product prices -->
                                                                                    <!-- product details -->
                                                                                    <tr item_name="product_details">
                                                                                        <td>
                                                                                        <table item_name="Product_details" style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="left" >
                                                                                            <tr>
                                                                                                <td style="padding: 0px; vertical-align:top;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 10px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1" height="10" border="0"></td>
                                                                                            </tr>
                                                                                            <!-- product label 1 -->
                                                                                            <tr>
                                                                                                <!-- product price -->
                                                                                                <td style="padding: 0px; vertical-align:top; text-transform:uppercase; width: 45%;font-family:  Arial, Helvetica, sans-serif; font-size: 10px; color:#000000; text-decoration: none; line-height: 3.3; letter-spacing: 0.3px; font-weight: bold;" class="padded" align="left">
                                                                                                    PRICE:
                                                                                                </td>
                                                                                                <!-- product color -->
                                                                                                <td style="padding: 0px; vertical-align:top; text-transform:uppercase; width: 45%;font-family:  Arial, Helvetica, sans-serif; font-size: 10px; color:#000000; text-decoration: none; line-height: 3.3; letter-spacing: 0.3px; font-weight: bold;" class="padded" align="left">
                                                                                                    COLOR:
                                                                                                </td>
                                                                                            </tr>
                                                                                            <!-- product price and color-->
                                                                                            <tr>
                                                                                                <td style="padding: 0px; vertical-align:top; text-transform:uppercase; font-family:  Arial, Helvetica, sans-serif; font-size: 10px; color:#000000; text-decoration: none; line-height: 1.5;  font-weight: bold;" class="padded" align="left">
                                                                                                    {user_inputs[14]}{user_inputs[4]}<br>
                                                                                                </td>
                                                                                                <td style="padding: 0px; vertical-align:top; text-transform:uppercase; font-family:  Arial, Helvetica, sans-serif; font-size: 10px; color:#000000; text-decoration: none; line-height: 1.8; letter-spacing: 0.4px;" class="padded" align="left">
                                                                                                    {user_inputs[5]}<br>
                                                                                                </td>
                                                                                            </tr>
                                                                                            <!-- spazio bianco-->
                                                                                            <tr>
                                                                                                <td style="padding: 0px; vertical-align:top; width:290px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 25px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1" height="25" border="0"></td>
                                                                                            </tr>
                                                                                            <!-- product label 2 -->
                                                                                            <tr>
                                                                                                <td style="padding: 0px; vertical-align:top; text-transform:uppercase; font-family:  Arial, Helvetica, sans-serif; font-size: 10px; color:#000000; text-decoration: none; line-height: 3.3; letter-spacing: 0.3px; font-weight: bold; " class="padded" align="left">
                                                                                                    SIZE:
                                                                                                </td>
                                                                                                <td style="padding: 0px; vertical-align:top; text-transform:uppercase; font-family:  Arial, Helvetica, sans-serif; font-size: 10px; color:#000000; text-decoration: none; line-height: 3.3; letter-spacing: 0.3px; font-weight: bold;" class="padded" align="left">
                                                                                                    QUANTITY:
                                                                                                </td>
                                                                                            </tr>
                                                                                            <!-- product taglia e numero-->
                                                                                            <tr>
                                                                                                <td style="padding: 0px; vertical-align:top; text-transform:uppercase; font-family:  Arial, Helvetica, sans-serif; font-size: 11px; color:#000000; text-decoration: none; line-height: 2.79;" class="padded" align="left">
                                                                                                    {user_inputs[6]}<br>
                                                                                                </td>
                                                                                                <td style="padding: 0px; vertical-align:top; text-transform:uppercase; font-family:  Arial, Helvetica, sans-serif; font-size: 11px; color:#000000; text-decoration: none; line-height: 2.79; letter-spacing: 0.4px;" class="padded" align="left">
                                                                                                    1<br>
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
                                                            </td>
                                                        </tr>
                                                    </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 0px; vertical-align: top; width: 400px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 30px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                                    height="30" border="0"></td>
                                                </tr>
                                            </table>
                                        </td>
                                        <td style="padding: 0px; vertical-align: top; width: 40px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="10" height="1" border="0"></td>
                                        </tr>
                                    </table>
                                </td>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table group_name="Price Recap" style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="center" class="" bgcolor="#f4f5f7">
                            <tr>
                                <!--- padding-left -->
                                <td style="padding: 0px; vertical-align:top; width:60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align:top; width:480px;" class="padded" align="center">
                                    <!---Price -->
                                    <table group_name="Price Box" style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="center" bgcolor="#FFFFFF">
                                        <tr>
                                        <!--- padding left-->
                                        <td style="padding: 0px; vertical-align:top; width:40px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="10" height="1" border="0"></td>
                                        <!--- total price table -->
                                        <td style="padding: 0px; vertical-align:top; width:400px;" class="padded" align="center">
                                            <table style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="center">
                                                <tr>
                                                    <td style="padding: 0px; vertical-align:top;"><img style="margin: 0px; padding: 0px; display: block; height: 20px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1" height="20" border="0"></td>
                                                </tr>
                                                <!--- subtotal -->
                                                <tr block_name="subTotal">
                                                    <td style="padding: 0px; vertical-align:top; width:200px; font-family: Arial, Helvetica, sans-serif; font-size: 16px; color:#000000;">
                                                    Subtotal:
                                                    </td>
                                                    <td style="padding: 0px; vertical-align:top; width:200px; font-family: Arial, Helvetica, sans-serif; font-size: 16px; color:#000000;" align="right">
                                                    {user_inputs[14]}{user_inputs[4]}<br>
                                                    </td>
                                                </tr>
                                                <!--- margin -->
                                                <tr>
                                                    <td style="padding: 0px; vertical-align:top;"><img style="margin: 0px; padding: 0px; display: block; height: 5px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1" height="5" border="0"></td>
                                                </tr>
                                                <tr block_name="subTotal">
                                                    <td style="padding: 0px; vertical-align:top; width:200px; font-family: Arial, Helvetica, sans-serif; font-size: 16px; color:#000000;">
                                                    Shipping costs:
                                                    </td>
                                                    <td style="padding: 0px; vertical-align:top; width:200px; font-family: Arial, Helvetica, sans-serif; font-size: 16px; color:#000000;" align="right">
                                                    {user_inputs[14]}{user_inputs[7]}<br>
                                                    </td>
                                                </tr>
                                                <!--- margin -->
                                                <tr>
                                                    <td style="padding: 0px; vertical-align:top;"><img style="margin: 0px; padding: 0px; display: block; height: 5px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1" height="5" border="0"></td>
                                                </tr>
                                                <!--- Shipping -->
                                                <tr block_name="shipping">
                                                    <td style="padding: 0px; vertical-align:top; width:200px; font-family: Arial, Helvetica, sans-serif; font-size: 16px; color:#000000;">
                                                    Taxes on sale (incl):
                                                    </td>
                                                    <td style="padding: 0px; vertical-align:top; width:200px; font-family: Arial, Helvetica, sans-serif; font-size: 16px; color:#000000;" align="right">
                                                    {user_inputs[14]}{user_inputs[8]}
                                                    </td>
                                                </tr>
                                                <!--- margin -->
                                                <tr>
                                                    <td style="padding: 0px; vertical-align:top;"><img style="margin: 0px; padding: 0px; display: block; height: 5px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1" height="5" border="0"></td>
                                                </tr>
                                                <!--- other tax -->
                                                <!--- promo code -->
                                                <!--- margin -->
                                                <tr>
                                                    <td style="padding: 0px; vertical-align:top;"><img style="margin: 0px; padding: 0px; display: block; height: 5px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1" height="5" border="0"></td>
                                                </tr>
                                                <!--- margin -->
                                                <tr>
                                                    <td style="padding: 0px; vertical-align:top;"><img style="margin: 0px; padding: 0px; display: block; height: 5px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1" height="5" border="0"></td>
                                                </tr>
                                                <!--- total -->
                                                <tr block_name="Total">
                                                    <td style="padding: 0px; vertical-align:top; width:200px; font-family: Arial, Helvetica, sans-serif; font-size: 16px; color:#000000;">
                                                    Total:
                                                    </td>
                                                    <td style="padding: 0px; vertical-align:top; width:200px; font-family: Arial, Helvetica, sans-serif; font-size: 16px; color:#000000;" align="right">
                                                    {user_inputs[14]}{user_inputs[9]}<br>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 0px; vertical-align:top;"><img style="margin: 0px; padding: 0px; display: block; height: 30px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1" height="30" border="0"></td>
                                                </tr>
                                            </table>
                                        </td>
                                        <!--- padding rigth-->
                                        <td style="padding: 0px; vertical-align:top; width:40px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="10" height="1" border="0"></td>
                                        </tr>
                                    </table>
                                </td>
                                <!--- padding- right -->
                                <td style="padding: 0px; vertical-align:top; width:60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table group_name="White Space" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" bgcolor="#f4f5f7">
                            <tr>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 480px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 30px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                    height="30" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table group_name="2 Columns Address" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" bgcolor="#f4f5f7">
                            <tr>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 480px;" class="padded" align="center">
                                    <table style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
                                        <tr>
                                        <td style="padding: 0px; vertical-align: top; width: 480px;" class="padded" align="center">
                                            <table class="two-col" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
                                                <tr>
                                                    <td style="padding: 0px; vertical-align: top; width: 480px;">
                                                    <table class="columns" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none; width: 480px;" border="0" cellpadding="0" cellspacing="0" align="center">
                                                        <tr>
                                                            <td style="padding: 0px; vertical-align: top;">
                                                                <table block_name="Left Column" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="left">
                                                                <tr>
                                                                    <td style="padding: 0px; vertical-align: top; width: 230px;" class="column">
                                                                        <table style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="left">
                                                                            <tr item_name="Title">
                                                                            <td style="padding: 0px; vertical-align: top; width:220px; font-family: Arial, Helvetica, sans-serif; font-size: 14px; line-height: 24px; color: #000001; font-weight: bold;" class="padded" align="left">
                                                                                Delivery address:
                                                                            </td>
                                                                            </tr>
                                                                            <tr>
                                                                            <td style="padding: 0px; vertical-align: top; width:220px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 5px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                                                                height="5" border="0"></td>
                                                                            </tr>
                                                                            <tr item_name="Text">
                                                                            <td style="padding: 0px; vertical-align: top; width:220px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; line-height: 18px; color: #000000;font-weight: bold;" class="padded" align="left">
                                                                                {user_inputs[0]}<br>
                                                                            </td>
                                                                            </tr>
                                                                            <tr>
                                                                            <td style="padding: 0px; vertical-align: top; width:220px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 5px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                                                                height="5" border="0"></td>
                                                                            </tr>
                                                                            <tr item_name="Text">
                                                                            <td style="padding: 0px; vertical-align: top; width:220px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; line-height: 18px; color: #000000;" class="padded" align="left">
                                                                                {user_inputs[10]}<br> {user_inputs[11]}<br> {user_inputs[12]}<br>
                                                                            </td>
                                                                            </tr>
                                                                            <tr>
                                                                            <td style="padding: 0px; vertical-align: top; width:220px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 5px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                                                                height="5" border="0"></td>
                                                                            </tr>
                                                                            <tr>
                                                                            <td style="padding: 0px; vertical-align: top; width:220px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 5px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                                                                height="5" border="0"></td>
                                                                            </tr>
                                                                            <tr item_name="Text">
                                                                            <td style="padding: 0px; vertical-align: top; width:220px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; line-height: 18px; color: #000000;" class="padded" align="left">
                                                                                {user_inputs[13]}
                                                                            </td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr item_name="Image" class="mobileversion" style="display:none;">
                                                                    <td style="padding: 0px; vertical-align:top; width:150px;" class="padded" align="left">
                                                                        <div class="mobileversion" style="display: none; width: 0; overflow: hidden; max-height:0; min-height: 0; margin: 0; padding: 0; font-size:0; line-height:1px; height: 0px; vertical-align: top">
                                                                            <img style="margin: 0px; padding: 0px; display: block; height: 20px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="150" height="20" border="0">
                                                                        </div>
                                                                    </td>
                                                                </tr>
                                                                </table>
                                                                <!--[if mso]>
                                                            </td>
                                                            <td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;vertical-align:top;" >
                                                                <![endif]-->
                                                                <table block_name="Right Column" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="right">
                                                                <tr>
                                                                    <td style="padding: 0px; vertical-align: top; width: 230px;" class="column">
                                                                        <table style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="left">
                                                                            <tr item_name="Title">
                                                                            <td style="padding: 0px; vertical-align: top; width:220px; font-family: Arial, Helvetica, sans-serif; font-size: 14px; line-height: 24px; color: #000001; font-weight: bold;" class="padded" align="left">
                                                                                Billing address:
                                                                            </td>
                                                                            </tr>
                                                                            <tr>
                                                                            <td style="padding: 0px; vertical-align: top; width:220px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 5px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                                                                height="5" border="0"></td>
                                                                            </tr>
                                                                            <tr item_name="Text">
                                                                                <td style="padding: 0px; vertical-align: top; width:220px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; line-height: 18px; color: #000000;font-weight: bold;" class="padded" align="left">
                                                                                {user_inputs[0]}<br>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="padding: 0px; vertical-align: top; width:220px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 5px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                                                                height="5" border="0"></td>
                                                                            </tr>
                                                                            <tr item_name="Text">
                                                                                <td style="padding: 0px; vertical-align: top; width:220px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; line-height: 18px; color: #000000;" class="padded" align="left">
                                                                                {user_inputs[10]}<br> {user_inputs[11]}<br> {user_inputs[12]}<br>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="padding: 0px; vertical-align: top; width:220px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 5px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                                                                height="5" border="0"></td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="padding: 0px; vertical-align: top; width:220px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 5px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                                                                height="5" border="0"></td>
                                                                            </tr>
                                                                            <tr item_name="Text">
                                                                                <td style="padding: 0px; vertical-align: top; width:220px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; line-height: 18px; color: #000000;" class="padded" align="left">
                                                                                {user_inputs[13]}
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
                                        </td>
                                        </tr>
                                    </table>
                                </td>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table group_name="White Space" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" bgcolor="#f4f5f7">
                            <tr>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 480px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 30px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                    height="30" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table group_name="Payment" style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="center" class="" bgcolor="#f4f5f7" >
                            <tr>
                                <td style="padding: 0px; vertical-align:top; width:60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align:top; width:480px" class="padded" align="center">
                                    <table style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="left">
                                        <tr>
                                        <td style="padding: 0px; vertical-align:top; font-family: Arial, Helvetica, sans-serif; font-size: 14px; line-height:20px; color:#000000;">
                                            Payment method:
                                        </td>
                                        </tr>
                                        <tr>
                                        <td style="padding: 0px; vertical-align:top;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 10px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1" height="10" border="0"></td>
                                        </tr>
                                        <tr>
                                        <td style="padding: 0px; vertical-align:top;font-family: Arial, Helvetica, sans-serif; font-size: 14px; line-height:20px; color:#000000;">
                                            PayPal
                                            <br>
                                            <br>
                                        </td>
                                        </tr>
                                    </table>
                                </td>
                                <td style="padding: 0px; vertical-align:top; width:60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table group_name="Payment" style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="center" class="" bgcolor="#f4f5f7" >
                            <tr>
                                <td style="padding: 0px; vertical-align:top; width:60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align:top; width:480px" class="padded" align="center">
                                    <table style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="left">
                                        <tr>
                                        <td style="padding: 0px; vertical-align:top; font-family: Arial, Helvetica, sans-serif; font-size: 14px; line-height:20px; color:#000000;">
                                            Each order is subject to prior verification of product availability. You will be informed as soon as possible via e-mail in case we are not able to satisfy entirely or partially your request.
                                            <br><br>
                                            You will be notified via e-mail once the availability of the product(s) featured in your order is confirmed, and you will be charged accordingly. The amount of pre-ordered and/or personalized products, if any, will be charged as the relevant confirmation e-mail is sent, even though such products are not yet ready to be shipped.
                                            <br><br>
                                            This e-mail is only a recap of the order we received. The sale contract will be deemed executed only when you receive the final confirmation e-mail.
                                            <br>
                                            <br>
                                            Best regards,
                                            <br />
                                            Prada Client Service
                                        </td>
                                        </tr>
                                    </table>
                                </td>
                                <td style="padding: 0px; vertical-align:top; width:60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- infos 3 columns -->
                    <tr>
                        <td>
                            <table group_name="White Space" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" bgcolor="#f4f5f7">
                            <tr>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 480px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 40px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                    height="40" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- full line separator -->
                    <tr>
                        <td>
                            <table group_name="Separator" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" class="separator" border="0" cellpadding="0" cellspacing="0" align="center" bgcolor="#f4f5f7">
                            <tr>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 480px" colspan="1" bgcolor="#e6e9f0" class="padded" align="center"><img style="margin: 0px; padding: 0px; display: block; height: 1px;"src="https://store.prada.com/images/email/misc/spacer.gif" width="1" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <!--white space -->
                    <tr>
                        <td>
                            <table group_name="White Space" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" bgcolor="#f4f5f7">
                            <tr>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 480px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 30px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                    height="30" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table group_name="3 Columns Link" style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="center" class="" bgcolor="#f4f5f7" >
                            <tr>
                                <td style="padding: 0px; vertical-align:top; width:60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align:top; width:480px;" class="padded" align="center">
                                    <table style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
                                        <tr>
                                        <td style="padding: 0px; vertical-align:top; width:480px;" class="padded" align="center">
                                            <table class="three-col" style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="center" width="100%" >
                                                <tr>
                                                    <td style="padding: 0px; vertical-align:top; width:480px;">
                                                    <table class="columns" style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
                                                        <tr>
                                                            <td style="padding: 0px; vertical-align:top;">
                                                                <table block_name="Left Column" style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="left" class="">
                                                                <tr>
                                                                    <td style="padding: 0px; vertical-align:top; width:160px;" class="column">
                                                                        <table style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="left">
                                                                            <tr>
                                                                            <td style="padding: 0px; vertical-align:top; width:150px;" class="padded">
                                                                                <img style="margin: 0px; padding: 0px; display: block; height: 10px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="150" height="10" border="0">
                                                                            </td>
                                                                            </tr>
                                                                            <tr item_name="Title" class="">
                                                                            <td style="padding: 0px; vertical-align:top; width:150px; color:#000000; font-family: Arial, Helvetica, sans-serif; font-size:12px; line-height:20px; font-weight: bold;" class="padded" align="left">
                                                                                <a href="https://www.prada.com/contact-us.html" target="_blank"style="color:#000000; font-family: Arial, Helvetica, sans-serif; font-size:12px; line-height:16px; text-transform:uppercase; text-decoration: none;font-weight: bold;">
                                                                                Client Service
                                                                                </a>
                                                                            </td>
                                                                            </tr>
                                                                            <tr>
                                                                            <td style="padding: 0px; vertical-align:top; width:120px;" class="padded"><a href="#">
                                                                                <img style="margin: 0px; padding: 0px; display: block; height: 5px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="120" height="5" border="0"></a>
                                                                            </td>
                                                                            </tr>
                                                                            <tr item_name="Image" class="mobileversion" style="display:none;">
                                                                            <td style="padding: 0px; vertical-align:top; width:120px;" class="padded" align="left">
                                                                                <div class="mobileversion" style="display: none; width: 0; overflow: hidden; max-height:0; min-height: 0; margin: 0; padding: 0; font-size:0; line-height:1px; height: 0px; vertical-align: top">
                                                                                    <img style="margin: 0px; padding: 0px; display: block; height: 5px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="120" height="5" border="0">
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                            <tr item_name="Text">
                                                                            <td style="padding: 0px; vertical-align:top; width:120px; color:#000000; font-family: Arial, Helvetica, sans-serif; font-size:12px; line-height:16px;" class="padded" align="left">
                                                                                <a href="#" target="_blank" style="color:#000000; font-family: Arial, Helvetica, sans-serif; font-size:12px; line-height:16px; text-decoration: none;">
                                                                                Call us at 00 800 800 77232
                                                                                or send us an email
                                                                                </a>
                                                                            </td>
                                                                            </tr>
                                                                            <tr item_name="Image" class="mobileversion" style="display:none;">
                                                                            <td style="padding: 0px; vertical-align:top; width:120px;" class="padded" align="left">
                                                                                <div class="mobileversion" style="display: none; width: 0; overflow: hidden; max-height:0; min-height: 0; margin: 0; padding: 0; font-size:0; line-height:1px; height: 0px; vertical-align: top">
                                                                                    <img style="margin: 0px; padding: 0px; display: block; height: 25px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="120" height="25" border="0">
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                            <tr item_name="full line" class="mobileversion" style="display:none;">
                                                                            <td style="padding: 0px; vertical-align:top;" colspan="3" bgcolor="#E3E3E3" class="padded320" align="center"><img style="margin: 0px; padding: 0px; display: block; height: 1px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1" height="1" border="0"></td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                </table>
                                                                <!--[if mso]>
                                                            </td>
                                                            <td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;vertical-align:top;" >
                                                                <![endif]-->
                                                                <table block_name="Center Column" style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="left" class="">
                                                                <tr>
                                                                    <td style="padding: 0px; vertical-align:top; width:160px;" class="column">
                                                                        <table style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="left">
                                                                            <tr>
                                                                            <td style="padding: 0px; vertical-align:top; width:150px;" class="padded">
                                                                                <img style="margin: 0px; padding: 0px; display: block; height: 10px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="150" height="10" border="0">
                                                                            </td>
                                                                            </tr>
                                                                            <tr item_name="Title" class="">
                                                                            <td style="padding: 0px; vertical-align:top; width:150px; color:#000000; font-family: Arial, Helvetica, sans-serif; font-size:12px; line-height:20px; font-weight: bold;" class="padded" align="left">
                                                                                <a href="https://www.prada.com/info.html" target="_blank"style="color:#000000; font-family: Arial, Helvetica, sans-serif; font-size:12px; line-height:16px; text-transform:uppercase; text-decoration: none;font-weight: bold;">
                                                                                Shipping & Returns
                                                                                </a>
                                                                            </td>
                                                                            </tr>
                                                                            <tr>
                                                                            <td style="padding: 0px; vertical-align:top; width:120px;" class="padded"><a href="#">
                                                                                <img style="margin: 0px; padding: 0px; display: block; height: 5px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="120" height="5" border="0"></a>
                                                                            </td>
                                                                            </tr>
                                                                            <tr item_name="Image" class="mobileversion" style="display:none;">
                                                                            <td style="padding: 0px; vertical-align:top; width:120px;" class="padded" align="left">
                                                                                <div class="mobileversion" style="display: none; width: 0; overflow: hidden; max-height:0; min-height: 0; margin: 0; padding: 0; font-size:0; line-height:1px; height: 0px; vertical-align: top">
                                                                                    <img style="margin: 0px; padding: 0px; display: block; height: 5px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="120" height="5" border="0">
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                            <tr item_name="Text">
                                                                            <td style="padding: 0px; vertical-align:top; width:120px; color:#000000; font-family: Arial, Helvetica, sans-serif; font-size:12px; line-height:16px;" class="padded" align="left">
                                                                                <a href="#" target="_blank" style="color:#000000; font-family: Arial, Helvetica, sans-serif; font-size:12px; line-height:16px; text-decoration: none;">
                                                                                Enjoy fast shipping <br> and free returns
                                                                                </a>
                                                                            </td>
                                                                            </tr>
                                                                            <tr item_name="Image" class="mobileversion" style="display:none;">
                                                                            <td style="padding: 0px; vertical-align:top; width:120px;" class="padded" align="left">
                                                                                <div class="mobileversion" style="display: none; width: 0; overflow: hidden; max-height:0; min-height: 0; margin: 0; padding: 0; font-size:0; line-height:1px; height: 0px; vertical-align: top">
                                                                                    <img style="margin: 0px; padding: 0px; display: block; height: 25px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="120" height="25" border="0">
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                            <tr item_name="full line" class="mobileversion" style="display:none;">
                                                                            <td style="padding: 0px; vertical-align:top;" colspan="3" bgcolor="#E3E3E3" class="padded320" align="center"><img style="margin: 0px; padding: 0px; display: block; height: 1px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1" height="1" border="0"></td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                </table>
                                                                <!--[if mso]>
                                                            </td>
                                                            <td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;vertical-align:top;" >
                                                                <![endif]-->
                                                                <table block_name="Right Column" style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="right" class="">
                                                                <tr>
                                                                    <td style="padding: 0px; vertical-align:top; width:140px;" class="column">
                                                                        <table style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="right">
                                                                            <tr>
                                                                            <td style="padding: 0px; vertical-align:top; width:130px;" class="padded"><a href="#">
                                                                                <img style="margin: 0px; padding: 0px; display: block; height: 10px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="130" height="10" border="0"></a>
                                                                            </td>
                                                                            </tr>
                                                                            <tr item_name="Image" class="mobileversion" style="display:none;">
                                                                            <td style="padding: 0px; vertical-align:top; width:130px;" class="padded" align="left">
                                                                                <div class="mobileversion" style="display: none; width: 0; overflow: hidden; max-height:0; min-height: 0; margin: 0; padding: 0; font-size:0; line-height:1px; height: 0px; vertical-align: top">
                                                                                    <img style="margin: 0px; padding: 0px; display: block; height: 20px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="130" height="20" border="0">
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                            <tr item_name="Title" class="">
                                                                            <td style="padding: 0px; vertical-align:top; width:130px; color:#000000; font-family: Arial, Helvetica, sans-serif; font-size:12px; line-height:20px; font-weight: bold;" class="padded" align="left">
                                                                                <a href="https://www.prada.com/geored?url=store-locator.html&urlNew=store-locator.html" target="_blank" style="color:#000000; font-family: Arial, Helvetica, sans-serif; font-size:12px; text-transform:uppercase; line-height:16px; text-decoration: none; font-weight:bold">
                                                                                Stores
                                                                                </a>
                                                                            </td>
                                                                            </tr>
                                                                            <tr>
                                                                            <td style="padding: 0px; vertical-align:top; width:130px;" class="padded"><a href="#">
                                                                                <img style="margin: 0px; padding: 0px; display: block; height: 5px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="130" height="5" border="0"></a>
                                                                            </td>
                                                                            </tr>
                                                                            <tr item_name="Image" class="mobileversion" style="display:none;">
                                                                            <td style="padding: 0px; vertical-align:top; width:130px;" class="padded" align="left">
                                                                                <div class="mobileversion" style="display: none; width: 0; overflow: hidden; max-height:0; min-height: 0; margin: 0; padding: 0; font-size:0; line-height:1px; height: 0px; vertical-align: top">
                                                                                    <img style="margin: 0px; padding: 0px; display: block; height: 5px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="130" height="5" border="0">
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                            <tr item_name="Text" class="">
                                                                            <td style="padding: 0px; vertical-align:top; width:130px; color:#000000; font-family: Arial, Helvetica, sans-serif; font-size:12px; line-height:16px;" class="padded" align="left">
                                                                                <a href="#" target="_blank" style="color:#000000; font-family: Arial, Helvetica, sans-serif; font-size:12px; line-height:16px; text-decoration: none;">
                                                                                Find the nearest <br> Prada store
                                                                                </a>
                                                                            </td>
                                                                            </tr>
                                                                            <tr item_name="Image" class="mobileversion" style="display:none;">
                                                                            <td style="padding: 0px; vertical-align:top; width:130px;" class="padded" align="left">
                                                                                <div class="mobileversion" style="display: none; width: 0; overflow: hidden; max-height:0; min-height: 0; margin: 0; padding: 0; font-size:0; line-height:1px; height: 0px; vertical-align: top">
                                                                                    <img style="margin: 0px; padding: 0px; display: block; height: 25px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="130" height="25" border="0">
                                                                                </div>
                                                                            </td>
                                                                            </tr>
                                                                            <tr item_name="Image" class="mobileversion" style="display: none; width: 0; overflow: hidden; max-height:0; min-height: 0; margin: 0; padding: 0; font-size:0; line-height:1px; height: 0px; vertical-align: top">
                                                                            <td style="display: none; width: 0; overflow: hidden; max-height:0; min-height: 0; margin: 0; padding: 0; font-size:0; line-height:1px; height: 0px; vertical-align: top" class="mobileversion padded" align="left">
                                                                                <div class="mobileversion" style="display: none; width: 0; overflow: hidden; max-height:0; min-height: 0; margin: 0; padding: 0; font-size:0; line-height:1px; height: 0px; vertical-align: top">
                                                                                    <a href="#" class="mobileversion mybutton" style="color:#000000; font-family: Arial, Helvetica, sans-serif; text-transform:uppercase;font-size:14px; line-height:18px; text-decoration: none;display: none; width: 0; overflow: hidden; max-height:0; min-height: 0; margin: 0; padding: 0; font-size:0; line-height:1px; height: 0px; vertical-align: top">
                                                                                    Find a store
                                                                                    </a>
                                                                                </div>
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
                                        </td>
                                        </tr>
                                    </table>
                                </td>
                                <td style="padding: 0px; vertical-align:top; width:60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- white space -->
                    <tr>
                        <td>
                            <table group_name="White Space" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" bgcolor="#f4f5f7">
                            <tr>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 480px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 30px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                    height="30" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- black footer with logo-->
                    <tr>
                        <td>
                            <table group_name="FooterLogo" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" class=""  bgcolor="#000000">
                            <tr>
                                <td style="padding: 0px; vertical-align: top; width: 20px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="10" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 560px;" class="padded" align="center">
                                    <table style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
                                        <tr>
                                        <td style="padding: 0px; vertical-align: top; width: 580px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 40px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                            height="40" border="0"></td>
                                        </tr>
                                        <tr block_name="Fluid Image">
                                        <td style="padding: 0px; width: 580px; font-size: 0; line-height: 1px; height: 1px; vertical-align: top" class="padded" align="Left"><a href="#" target="_blank"> <img
                                            style="font-size: 0; margin: 0px; padding: 0px; display: inline;" src="https://assets.prada.com/content/dam/transactional/prada/logo/prada-white-79x13.png" width="79" height="13" border="0" alt="">
                                            </a>
                                        </td>
                                        </tr>
                                        <tr>
                                        <td style="padding: 0px; vertical-align: top; width: 560px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 10px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                            height="10" border="0"></td>
                                        </tr>
                                    </table>
                                </td>
                                <td style="padding: 0px; vertical-align: top; width: 20px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="10" height="1" border="0"></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- black footer with social and copyright info -->
                    <tr>
                        <td>
                            <table group_name="Social" style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="center" class="" bgcolor="#000000" >
                            <tr>
                                <td style="padding: 0px; vertical-align:top; width:20px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="20" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align:top; width:560px;" class="padded" align="center">
                                    <table style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
                                        <tr>
                                        <td style="padding: 0px; vertical-align:top; width:560px;" class="padded" align="center">
                                            <table class="two-col" style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="center" width="100%" >
                                                <tr>
                                                    <td style="padding: 0px; vertical-align:top; width:560px;">
                                                    <table class="columns" style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none; width:560px;" border="0" cellpadding="0" cellspacing="0" align="center">
                                                        <tr>
                                                            <td style="padding: 0px; vertical-align:top;" align="center">
                                                                <table block_name="Social" style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="left" class="">
                                                                <tr>
                                                                    <td style="padding: 0px; vertical-align:top; width:270px;" class="column" align="left">
                                                                        <table style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="left">
                                                                            <tr>
                                                                            <td class="padded">
                                                                                <table style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none; min-width: 52px;" border="0" cellpadding="0" cellspacing="0" class="center">
                                                                                    <tr>
                                                                                        <td style="padding: 0px; vertical-align:top; width:1px; color:#FFFFFF; font-family: Arial, Helvetica, sans-serif; font-size:10px; line-height:20px; text-transform:uppercase; width:280px;" class="padded" align="left">
                                                                                        Prada S.p.A. - Via Antonio Fogazzaro, 28 - 20135 Milano, Italia
                                                                                        </td>
                                                                                    </tr>
                                                                                </table>
                                                                            </td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                </table>
                                                                <!--[if mso]>
                                                            </td>
                                                            <td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;vertical-align:top;" >
                                                                <![endif]-->
                                                                <table block_name="Social" style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" class="" align="right">
                                                                <tr>
                                                                    <td style="padding: 0px; vertical-align:top; width:270px;" class="column" align="right">
                                                                        <table style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="right">
                                                                            <tr>
                                                                            <td class="padded" align="left">
                                                                                <table style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none; min-width: 100%;" border="0" cellpadding="0" cellspacing="0" class="center">
                                                                                    <tr>
                                                                                        <td style="padding: 0px; vertical-align:top; color:#ffffff; font-family: Arial, Helvetica, sans-serif; font-size:12px; line-height:20px; text-decoration:none" width="70"align="center">
                                                                                        <a href="http://www.facebook.com/prada" target="_blank" style="text-size-adjust: none; -moz-text-size-adjust: none; -ms-text-size-adjust: none; -webkit-text-size-adjust: none;  font-size:12px; line-height:20px; color:#FFFFFF; font-family: Arial, Helvetica, sans-serif;  text-align: center; text-decoration: none;">
                                                                                        Facebook
                                                                                        </a>
                                                                                        </td>
                                                                                        <td style="padding: 0px; vertical-align:top; color:#ffffff; font-family: Arial, Helvetica, sans-serif; font-size:12px; line-height:20px; text-decoration:none" width="70"align="center">
                                                                                        <a href="http://www.instagram.com/prada/" target="_blank" style="text-size-adjust: none; -moz-text-size-adjust: none; -ms-text-size-adjust: none; -webkit-text-size-adjust: none;  font-size:12px; line-height:20px; color:#FFFFFF; font-family: Arial, Helvetica, sans-serif;  text-align: center; text-decoration: none;">
                                                                                        Instagram
                                                                                        </a>
                                                                                        </td>
                                                                                        <td style="padding: 0px; vertical-align:top; color:#ffffff; font-family: Arial, Helvetica, sans-serif; font-size:12px; line-height:20px; text-decoration:none" width="60"align="center">
                                                                                        <a href="https://www.youtube.com/prada" target="_blank" style="text-size-adjust: none; -moz-text-size-adjust: none; -ms-text-size-adjust: none; -webkit-text-size-adjust: none;  font-size:12px; line-height:20px; color:#FFFFFF; font-family: Arial, Helvetica, sans-serif;  text-align: center; text-decoration: none;">
                                                                                        You Tube
                                                                                        </a>
                                                                                        </td>
                                                                                        <td style="padding: 0px; vertical-align:top; color:#ffffff; font-family: Arial, Helvetica, sans-serif; font-size:12px; line-height:20px; text-decoration:none" width="60"align="center">
                                                                                        <a href="http://twitter.com/prada" target="_blank" style="text-size-adjust: none; -moz-text-size-adjust: none; -ms-text-size-adjust: none; -webkit-text-size-adjust: none;  font-size:12px; line-height:20px; color:#FFFFFF; font-family: Arial, Helvetica, sans-serif;  text-align: center; text-decoration: none;">
                                                                                        Twitter
                                                                                        </a>
                                                                                        </td>
                                                                                        <td style="padding: 0px; vertical-align:top; color:#ffffff; font-family: Arial, Helvetica, sans-serif; font-size:12px; line-height:20px; text-decoration:none" width="60"align="center">
                                                                                        <a href="https://open.spotify.com/user/sz56yms9zgvax5w86re3bdmpf?si=klV3HcPyTBWAvOr9K-DX3A" target="_blank" style="text-size-adjust: none; -moz-text-size-adjust: none; -ms-text-size-adjust: none; -webkit-text-size-adjust: none;  font-size:12px; line-height:20px; color:#FFFFFF; font-family: Arial, Helvetica, sans-serif;  text-align: center; text-decoration: none;">
                                                                                        Spotify
                                                                                        </a>
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
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                        </tr>
                                    </table>
                                </td>
                                <td style="padding: 0px; vertical-align:top; width:20px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="20" height="1" border="0"></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- white space -->
                    <tr>
                        <td>
                            <table group_name="White Space" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" bgcolor="#000000">
                            <tr>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 480px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 20px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                    height="20" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- full line separator white -->
                    <tr>
                        <td>
                            <table group_name="Separator" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" class="separator--white" border="0" cellpadding="0" cellspacing="0" align="center" bgcolor="#000000">
                            <tr>
                                <td style="padding: 0px; vertical-align: top; width: 20px;" class="padding">
                                    <img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="20" height="1" border="0">
                                </td>
                                <td style="padding: 0px; vertical-align: top; width: 560px" colspan="1" bgcolor="#f4f5f7" class="padded" align="center">
                                    <img style="margin: 0px; padding: 0px; display: block; height: 1px;"src="https://store.prada.com/images/email/misc/spacer.gif" width="1" height="1" border="0">
                                </td>
                                <td style="padding: 0px; vertical-align: top; width: 20px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="20" height="1" border="0"></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- white space -->
                    <tr>
                        <td>
                            <table group_name="White Space" style="border-collapse: collapse; border-spacing: 0; -webkit-text-size-adjust: none;" border="0" cellpadding="0" cellspacing="0" align="center" bgcolor="#000000">
                            <tr>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 480px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 10px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                    height="10" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 60px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="60" height="1" border="0"></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- black footer terms-->
                    <tr>
                        <td>
                            <table group_name="Terms" style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="center" class="" bgcolor="#000000" >
                            <tr>
                                <td style="padding: 0px; vertical-align:top; width:20px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="20" height="1" border="0"></td>
                                <td class="alignMobile "style="padding: 0px; vertical-align:middle; width: 560px; height: 30px; font-family: Arial, Helvetica, sans-serif; font-size:12px; line-height:20px; color:#FFFFFF; text-align:right;" height="30">
                                    <a href="https://www.prada.com/terms.html" style="font-family: Arial, Helvetica, sans-serif; font-size:12px; line-height:20px; color:#FFFFFF; text-decoration: none;">
                                    Terms of Purchase
                                    </a>
                                    |
                                    <a href="https://www.prada.com/info.html" style="font-family: Arial, Helvetica, sans-serif; font-size:12px; line-height:20px; color:#FFFFFF; text-decoration: none;">
                                    Privacy policy
                                    </a>
                                </td>
                                <td style="padding: 0px; vertical-align:top; width:20px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="20" height="1" border="0"></td>
                            </tr>
                            <tr>
                                <td style="padding: 0px; vertical-align: top; width: 20px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="20" height="1" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 560px;" class="padded"><img style="margin: 0px; padding: 0px; display: block; height: 10px;" src="https://store.prada.com/images/email/misc/spacer.gif" width="1"
                                    height="10" border="0"></td>
                                <td style="padding: 0px; vertical-align: top; width: 20px;" class="padding"><img style="margin: 0px; padding: 0px; display: block;" src="https://store.prada.com/images/email/misc/spacer.gif" width="20" height="1" border="0"></td>
                            </tr>
                            </table>
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
