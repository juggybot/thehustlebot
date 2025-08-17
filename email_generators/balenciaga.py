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
    msg['From'] = formataddr((f'Balenciaga', sender_email))
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
    "Please enter the image url (MUST BE FROM BALENCIAGA):",
    "Please enter the product name (track trainers):",
    "Please enter the product price (WITHOUT THE $ SIGN):",
    "Please enter the product colour (BLACK):",
    "Please enter the product size (GB 11):",
    "Please enter the shipping fees (WITHOUT THE $ SIGN):",
    "Please enter the order total (WITHOUT THE $ SIGN):",
    "Please enter the customer name (Juggy Resells):",
    "Please enter the street address (05 Ellie Hill):",
    "Please enter the suburb (New Alex):",
    "Please enter the postcode (5563):",
    "Please enter the country (Australia):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]
prompts_pt = [
    "Por favor, insira o primeiro nome do cliente (Juggy):",
    "Por favor, insira a URL da imagem (DEVE SER DO SITE BALENCIAGA):",
    "Por favor, insira o nome do produto (track trainers):",
    "Por favor, insira o preço do produto (SEM O SINAL $):",
    "Por favor, insira a cor do produto (PRETO):",
    "Por favor, insira o tamanho do produto (GB 11):",
    "Por favor, insira as taxas de envio (SEM O SINAL $):",
    "Por favor, insira o total do pedido (SEM O SINAL $):",
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira o endereço (05 Ellie Hill):",
    "Por favor, insira o bairro (New Alex):",
    "Por favor, insira o código postal (5563):",
    "Por favor, insira o país (Austrália):",
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
    part1 = f'F1BAGBO'
    part2 = random.randint(100000000, 999999999)  # Random 8-digit number

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
    sender_email = EMAIL
    sender_password = PASSWORD
    recipient_email = f'{user_inputs[14]}'
    subject = f"Your Balenciaga Order" if lang == "en" else f"Seu pedido Balenciaga"
    html_template = f"""
    <img src="https://click.news.balenciaga.com/open.aspx?ffcb10-feb91c77726c0778-fe561375726503747410-fe3e15707564047f701372-ff971577-fe3116727c64077e731772-ff5812797d&d=100196&bmt=0"
        width="1" height="1" alt="">

















    <!DOCTYPE html
        PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml"
        xmlns:o="urn:schemas-microsoft-com:office:office">

    <head>
        <META NAME="ROBOTS" CONTENT="NOINDEX, NOFOLLOW">
        <META NAME="referrer" CONTENT="no-referrer">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <title>Balenciaga</title>
        <meta name="viewport" content="height=device-height, width=device-width, minimum-scale=1.0, user-scalable=no" />
        <meta name="format-detection" content="telephone=no">
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <base target="_blank">
        <!--[if gte mso 15]><xml><o:OfficeDocumentSettings><o:AllowPNG/>
    <o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml><![endif]-->
        <link rel="stylesheet" type="text/css" href="/50's Receipts/data/css/balenciaga.css">


    </head>

    <body style="margin: 0; padding: 0px; background: #ffffff;">

        <!-- ============== PREHEADER ============== -->
        <span class="preheader" style="display:none !important; visibility:hidden; opacity:0; color:transparent; height:0; width:0; color:#ffffff; font-size:1px;
    line-height:0; overflow:hidden; mso-hide:all;" block_name="Invisible Pre-header Text">
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
        </span>
        <!-- ============== END PREHEADER ============== -->
        <table class="wrp" style="-webkit-text-size-adjust:none; min-width:601px;" border="0" cellpadding="0"
            cellspacing="0" align="center" width="100%" bgcolor="#ffffff">
            <tr>
                <td class="wrp" style="-webkit-text-size-adjust:none; min-width:601px;" border="0" cellpadding="0"
                    cellspacing="0" align="center" width="100%">

                    <!--  spacer  -->
                    <table style="-webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0" align="center"
                        class="container_2">
                        <tr>
                            <td style="padding:0px;vertical-align:top;width:599px;" class="padded">
                                <img style="margin:0px;padding:0px;display:block;height:45px;"
                                    src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                    width="1" height="45" border="0">
                            </td>
                        </tr>
                    </table>
                    <!-- end spacer -->
                    <!-- ============== BODY ============== -->
                    <table style="-webkit-text-size-adjust:none; border-left:1px solid #000; border-right:1px solid #000;"
                        class="container remLRCls" border="0" cellpadding="0" cellspacing="0" align="center">
                        <tr>
                            <td align="center">
                                <!-- ============== LOGO ============== -->
                                <!--  border top  -->
                                <table style="-webkit-text-size-adjust:none; border-top:1px solid #000;" border="0"
                                    cellpadding="0" cellspacing="0" align="center" class="container_2">
                                    <tr>
                                        <td style="padding: 0px; vertical-align:top; width:599px;" class="padded">
                                            <img style="margin: 0px; padding: 0px; display: block;
                                    height: 14px;"
                                                src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                width="1" height="14" border="0">
                                        </td>
                                    </tr>
                                </table>
                                <!-- end border top -->
                                <table style="-webkit-text-size-adjust:none;" border="0" cellpadding="0" cellspacing="0"
                                    align="center">
                                    <tr>
                                        <td style="padding:0px;vertical-align:top;width:599px;" align="center"
                                            class="padded">
                                            <table
                                                style="border-collapse:collapse;border-spacing:0;-webkit-text-size-adjust:none;"
                                                border="0" cellpadding="0" cellspacing="0" align="center" bgcolor="#ffffff">
                                                <tr>
                                                    <td style="padding:0px;vertical-align:top;width:598px;font-family:Arial, Helvetica,sans-serif;font-size:14px;line-height:18px;color:#000000;"
                                                        class="padded" align="center"><a
                                                            href="https://click.news.balenciaga.com/?qs=d897245e4ffdacfb57e934dbdc490eeb6f2586c4f6927830c78b830afa510a35ee9506ce1c3a3de1812c018dddb290d532a9e68598d528a19b6cc8d2c94d7c36"
                                                            target="_blank">
                                                            <img style="font-size:0;margin:0px;padding:0px;display:block;"
                                                                src="https://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/73c19a3b-e950-4a7b-92a3-3b6c9767e6c7.png"
                                                                width="137" height="16" border="0"></a>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>

                                <!--  spacer  -->
                                <table style="-webkit-text-size-adjust:none;border-bottom:1px solid #000;" border="0"
                                    cellpadding="0" cellspacing="0" align="center">
                                    <tr>
                                        <td style="padding:0px;vertical-align:top;width:599px;" class="padded">
                                            <img style="margin:0px;padding:0px;display:block;height:14px;"
                                                src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                width="1" height="14" border="0">
                                        </td>
                                    </tr>
                                </table>
                                <!--  end spacer  -->
                                <!-- ============== LOGO ============== -->












































                                <!-- ============== SHIPPING METHOD IDENTIFIER ============== -->





                                <!-- ==============  SHIPPING METHOD IDENTIFIER END  ============== -->
                                <table style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none; "
                                    class="container" border="0" cellpadding="0" cellspacing="0" align="center">
                                    <tr>
                                        <td align="center">
                                            <!-- ============== Primo Blocco ============== -->
                                            <table
                                                style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                border="0" cellpadding="0" cellspacing="0" align="center">
                                                <tr>
                                                    <td class="padded320" align="center"
                                                        style="padding: 0px; vertical-align:top; width:599px;">
                                                        <table
                                                            style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                            border="0" cellpadding="0" cellspacing="0" align="center">
                                                            <tr>
                                                                <td align="center"
                                                                    style="padding: 0px; vertical-align:top; width:440px;">
                                                                    <table style="-webkit-text-size-adjust:none;" border="0"
                                                                        cellpadding="0" cellspacing="0" align="center">
                                                                        <tr>
                                                                            <td style="padding:0px;vertical-align:top;width:599px;"
                                                                                class="padded">
                                                                                <img style="margin:0px;padding:0px;display:block;height:80px;"
                                                                                    src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                                                    width="1" height="80" border="0">
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                    <table
                                                                        style="border-collapse:collapse;border-spacing:0;-webkit-text-size-adjust:none;"
                                                                        border="0" cellpadding="0" cellspacing="0"
                                                                        align="center" width="100%">
                                                                        <tr>
                                                                            <td style="padding:0px;width:440px;font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:center;line-height:20px;color:#000000;vertical-align:top;"
                                                                                align="center" class="container_2">
                                                                                <p
                                                                                    style="font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:center;line-height:20px;color:#000000;margin-left:10px; margin-right:10px;margin-top:10px;margin-bottom:10px;">
                                                                                    <strong>ORDER
                                                                                        REGISTRATION</strong><br><br> Dear
                                                                                    {user_inputs[0]},<br> Thank you for your order with
                                                                                    Balenciaga.
                                                                                </p>
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                    <table style="-webkit-text-size-adjust:none;" border="0"
                                                                        cellpadding="0" cellspacing="0" align="center">
                                                                        <tr>
                                                                            <td style="padding:0px;vertical-align:top;width:599px;"
                                                                                class="padded">
                                                                                <img style="margin:0px;padding:0px;display:block;height:80px;"
                                                                                    src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                                                    width="1" height="80" border="0">
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                            <!-- ============== END Primo Blocco ============== -->
                                            <!-- ============== Secondo blocco ============== -->
                                            <table
                                                style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;border-top:1px solid #000;"
                                                border="0" cellpadding="0" cellspacing="0" align="center">
                                                <tr>
                                                    <td class="padded320" align="center"
                                                        style="padding: 0px; vertical-align:top; width:599px;">
                                                        <table
                                                            style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                            border="0" cellpadding="0" cellspacing="0" align="center">
                                                            <tr>
                                                                <td align="center"
                                                                    style="padding: 0px; vertical-align:top; width:440px;">
                                                                    <table style="-webkit-text-size-adjust:none;" border="0"
                                                                        cellpadding="0" cellspacing="0" align="center">
                                                                        <tr>
                                                                            <td style="padding: 0px;vertical-align:top;width:599px;"
                                                                                class="padded">
                                                                                <img style="margin:0px;padding:0px;display:block;height:40px;"
                                                                                    src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                                                    width="1" height="40" border="0">
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                    <table
                                                                        style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                                        border="0" cellpadding="0" cellspacing="0"
                                                                        align="left" width="100%">
                                                                        <tr>
                                                                            <td style="padding: 0px; width:440px; font-family: Arial, Helvetica, sans-serif; font-size:14px;text-align:center;line-height:20px;color:#000000;vertical-align: top;"
                                                                                align="center" class="container_2">
                                                                                <p
                                                                                    style="font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:center;line-height:20px;color:#000000;margin-left:10px; margin-right:10px;margin-top:10px;margin-bottom:10px;">
                                                                                    We are pleased to confirm that your
                                                                                    order {order_num} has been
                                                                                    registered and will be processed
                                                                                    accordingly. <br>You can follow the
                                                                                    status of your order on our website,
                                                                                    either in our dedicated Client Service
                                                                                    area or by accessing the <a
                                                                                        href=https://www.balenciaga.com/en-gb/account
                                                                                        style='color:#000000; text-decoration:underline;'>My
                                                                                        Account</a> section if you already
                                                                                    have an account.</p>
                                                                            </td>
                                                                        </tr>

                                                                        <tr>
                                                                            <td style="padding:0px;width:440px;font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:center;line-height:20px;color:#000000;vertical-align:top;"
                                                                                align="center" class="container_2">
                                                                                <p
                                                                                    style="font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:center;line-height:20px;color:#000000;margin-left:10px; margin-right:10px;margin-top:10px;margin-bottom:10px;">
                                                                                    We will confirm the shipment of your
                                                                                    order by email.<br /><br />If you are a
                                                                                    registered client, you may cancel your
                                                                                    order via your account within 30 minutes
                                                                                    after placing it.</p>
                                                                            </td>
                                                                        </tr>


                                                                    </table>
                                                                    <table style="-webkit-text-size-adjust:none;" border="0"
                                                                        cellpadding="0" cellspacing="0" align="left">
                                                                        <tr>
                                                                            <td style="padding: 0px;vertical-align:top;width:599px;"
                                                                                class="padded">
                                                                                <img style="margin:0px;padding:0px;display:block;height:40px;"
                                                                                    src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                                                    width="1" height="40" border="0">
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                            <!-- ============== END Secondo Blocco ============== -->
                                            <!-- new condition for to disply bal engagement start-->
                                            <table
                                                style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;border-top:1px solid #000;"
                                                border="0" cellpadding="0" cellspacing="0" align="center">
                                                <tr>
                                                    <td class="padded320" align="center"
                                                        style="padding: 0px; vertical-align:top; width:599px;">
                                                        <table
                                                            style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                            border="0" cellpadding="0" cellspacing="0" align="center">
                                                            <tr>
                                                                <td align="center"
                                                                    style="padding: 0px; vertical-align:top; width:440px;">
                                                                    <table style="-webkit-text-size-adjust:none;" border="0"
                                                                        cellpadding="0" cellspacing="0" align="center">
                                                                        <tr>
                                                                            <td style="padding: 0px;vertical-align:top;width:599px;"
                                                                                class="padded">
                                                                                <img style="margin:0px;padding:0px;display:block;height:40px;"
                                                                                    src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                                                    width="1" height="40" border="0">
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                    <table
                                                                        style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                                        border="0" cellpadding="0" cellspacing="0"
                                                                        align="center" width="100%">
                                                                        <tr>
                                                                            <td style="padding: 0px; width:440px; font-family: Arial, Helvetica, sans-serif; font-size:14px;text-align:center;line-height:20px;color:#000000;vertical-align: top;"
                                                                                align="left" class="container_2">
                                                                                <p
                                                                                    style="font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:center;line-height:20px;color:#000000;margin-left:10px; margin-right:10px;margin-top:10px;margin-bottom:10px;">
                                                                                    <strong>ACTIVATE YOUR ENVIRONMENTAL
                                                                                        ASSET</strong><br><br>Balenciaga has
                                                                                    calculated the residual carbon emissions
                                                                                    generated by your purchase and invested
                                                                                    the corresponding amount in forestry and
                                                                                    conservation projects that protect local
                                                                                    biodiversity, restore natural
                                                                                    ecosystems, and increase resilience to
                                                                                    climate change. You may claim the
                                                                                    environmental assets corresponding to
                                                                                    this impact and track them through the
                                                                                    Reforestum platform.<br><br><a
                                                                                        href=https://app.reforestum.com/activation/5e76d924-dbdf-44d1-9f93-b054894cb865
                                                                                        style='color:#000000;text-decoration: underline;'>ACTIVATE
                                                                                        NOW</a>
                                                                                </p>
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                    <table style="-webkit-text-size-adjust:none;" border="0"
                                                                        cellpadding="0" cellspacing="0" align="left">
                                                                        <tr>
                                                                            <td style="padding: 0px;vertical-align:top;width:599px;"
                                                                                class="padded">
                                                                                <img style="margin:0px;padding:0px;display:block;height:40px;"
                                                                                    src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                                                    width="1" height="40" border="0">
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>

                                            <!-- new condition for to disply bal engagement ends -->
                                            <!-- ============== Title ============== -->
                                            <table
                                                style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;border-top:1px solid #000;"
                                                border="0" cellpadding="0" cellspacing="0" align="center">
                                                <tr>
                                                    <td class="padded320" align="center"
                                                        style="padding: 0px; vertical-align:top; width:599px;">
                                                        <table
                                                            style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                            border="0" cellpadding="0" cellspacing="0" align="center">
                                                            <tr>
                                                                <td align="center"
                                                                    style="padding: 0px; vertical-align:top; width:440px;">
                                                                    <table style="-webkit-text-size-adjust:none;" border="0"
                                                                        cellpadding="0" cellspacing="0" align="center">
                                                                        <tr>
                                                                            <td style="padding: 0px;vertical-align:top;width:599px;"
                                                                                class="padded">
                                                                                <img style="margin:0px;padding:0px;display:block;height:12px;"
                                                                                    src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                                                    width="1" height="12" border="0">
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                    <table
                                                                        style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                                        border="0" cellpadding="0" cellspacing="0"
                                                                        align="center" width="100%">
                                                                        <tr>
                                                                            <td style="padding: 0px; width:440px; font-family: Arial, Helvetica, sans-serif; font-size:14px;text-align:center;line-height:20px;color:#000000;vertical-align: top;"
                                                                                align="left" class="container_2">
                                                                                <p
                                                                                    style="font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:center;line-height:20px;color:#000000;margin-left:10px; margin-right:10px;margin-top:0;margin-bottom:0;">
                                                                                    <b>ORDER DETAILS</b>
                                                                                </p>
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                    <table style="-webkit-text-size-adjust:none;" border="0"
                                                                        cellpadding="0" cellspacing="0" align="left">
                                                                        <tr>
                                                                            <td style="padding: 0px;vertical-align:top;width:599px;"
                                                                                class="padded">
                                                                                <img style="margin:0px;padding:0px;display:block;height:12px;"
                                                                                    src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                                                    width="1" height="12" border="0">
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                            <!-- ============== END Title ============== -->















                                            <table
                                                style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;border-top:1px solid #000"
                                                border="0" cellpadding="0" cellspacing="0" align="center">
                                                <tr>
                                                    <td class="padded320" align="center"
                                                        style="padding: 0px; vertical-align:top; width:599px;">
                                                        <table
                                                            style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                            border="0" cellpadding="0" cellspacing="0" align="center">
                                                            <tr>
                                                                <td align="center"
                                                                    style="padding: 0px; vertical-align:top; width:599px;">

                                                                    <table
                                                                        style="border-collapse:collapse;border-spacing:0;-webkit-text-size-adjust:none;"
                                                                        border="0" cellpadding="0" cellspacing="0"
                                                                        align="center" width="100%">

                                                                        <tr>
                                                                            <!-- product image -->
                                                                            <td style="width:200px; background-color:#ffffff;vertical-align: middle;"
                                                                                align="center"
                                                                                class="mobile-side-product-img">
                                                                                <img src="{user_inputs[1]}"
                                                                                    width="200">
                                                                            </td>
                                                                            <!-- end product image -->
                                                                            <td>
                                                                                <table
                                                                                    style="-webkit-text-size-adjust:none;"
                                                                                    border="0" cellpadding="0"
                                                                                    cellspacing="0" align="center"
                                                                                    width="100%">
                                                                                    <!-- title -->
                                                                                    <tr>
                                                                                        <td style="font-family: Arial, Helvetica, sans-serif; width:290px; vertical-align: top; "
                                                                                            align="left"
                                                                                            class="container_3">
                                                                                            <p
                                                                                                style="font-family: Arial, Helvetica, sans-serif; font-size:14px; text-align: left; line-height:20px; color:#000000; margin-left: 10px; margin-right: 5px; margin-top: 10px; margin-bottom: 10px;text-transform: uppercase; ">
                                                                                                <strong>{user_inputs[2]}</strong><br>



                                                                                                {user_inputs[13]} {user_inputs[3]}




                                                                                            </p>
                                                                                        </td>
                                                                                    </tr>
                                                                                    <!-- end title -->
                                                                                    <!-- info -->
                                                                                    <tr>
                                                                                        <td style="font-family: Arial, Helvetica, sans-serif; width:290px; vertical-align: top; "
                                                                                            align="left"
                                                                                            class="container_3">
                                                                                            <p
                                                                                                style="font-family: Arial, Helvetica, sans-serif; font-size:14px; text-align: left; line-height:20px; color:#000000; margin-left: 10px; margin-right: 5px; margin-top: 10px; margin-bottom: 5px; ">
                                                                                                Colour:&nbsp;{user_inputs[4]}<br>
                                                                                                Size: {user_inputs[5]}<br>
                                                                                                Quantity:&nbsp;1
                                                                                            </p>
                                                                                        </td>
                                                                                    </tr>
                                                                                    <!-- end info -->
                                                                                    <!-- total -->

                                                                                    <tr>
                                                                                        <td style="padding: 0px;vertical-align:top;width:599px;"
                                                                                            class="padded"><img
                                                                                                style="margin:0px;padding:0px;display:block;height:12px;"
                                                                                                src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                                                                width="1" height="12"
                                                                                                border="0"></td>
                                                                                    </tr>


                                                                                    <!-- end total -->
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


                                            <!-- ============== Order Summary ============== -->



                                            <!-- ============== Totale ============== -->
                                            <table
                                                style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;border-top:1px solid #000;"
                                                border="0" cellpadding="0" cellspacing="0" align="center">
                                                <tr>
                                                    <td class="padded320" align="center"
                                                        style="padding: 0px; vertical-align:top; width:599px;">
                                                        <table
                                                            style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                            border="0" cellpadding="0" cellspacing="0" align="center">
                                                            <tr>
                                                                <td align="center"
                                                                    style="padding: 0px; vertical-align:top; width:580px;">
                                                                    <table style="-webkit-text-size-adjust:none;" border="0"
                                                                        cellpadding="0" cellspacing="0" align="center">
                                                                        <tr>
                                                                            <td style="padding: 0px;vertical-align:top;width:599px;"
                                                                                class="padded">
                                                                                <img style="margin:0px;padding:0px;display:block;height:40px;"
                                                                                    src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                                                    width="1" height="40" border="0">
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                    <table
                                                                        style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                                        border="0" cellpadding="0" cellspacing="0"
                                                                        align="left" width="100%">
                                                                        <tr>
                                                                            <td style="padding: 0px; width:440px; font-family: Arial, Helvetica, sans-serif; font-size:14px;text-align:left;line-height:20px;color:#000000;vertical-align: top;"
                                                                                align="left" class="container_2">



                                                                                <table
                                                                                    style="border-collapse:collapse;border-spacing:0;-webkit-text-size-adjust:none;"
                                                                                    border="0" cellpadding="0"
                                                                                    cellspacing="0" align="center"
                                                                                    width="100%">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td style='width:170px;'
                                                                                                align='center'
                                                                                                class='container_2 w200'>
                                                                                                <p
                                                                                                    style='font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:left;line-height:20px;color:#000000;margin-left:10px;margin-right:10px;margin-top:5px;margin-bottom:5px;'>
                                                                                                    Subtotal:
                                                                                                </p>
                                                                                            </td>
                                                                                            <td style='width:250px;
        vertical-align:top;' align='left' class='container_2 w100'>
                                                                                                <p
                                                                                                    style='font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:right;line-height:20px;color:#000000;margin-left:10px;margin-right:10px;margin-top:5px;margin-bottom:5px;'>
                                                                                                    {user_inputs[13]} {user_inputs[3]}
                                                                                                </p>
                                                                                            </td>
                                                                                        </tr>



                                                                                        <tr>
                                                                                            <td style='width:170px;'
                                                                                                align='center'
                                                                                                class='container_2 w200'>
                                                                                                <p
                                                                                                    style='font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:left;line-height:20px;color:#000000;margin-left:10px;margin-right:10px;margin-top:5px;margin-bottom:5px;'>
                                                                                                    Shipping fees:
                                                                                                </p>
                                                                                            </td>
                                                                                            <td style='width:250px;vertical-align:top;'
                                                                                                align='left'
                                                                                                class='container_2 w100'>
                                                                                                <p
                                                                                                    style='font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:right;line-height:20px;color:#000000;margin-left:10px;margin-right:10px;margin-top:5px;margin-bottom:5px;'>
                                                                                                    {user_inputs[13]} {user_inputs[6]}
                                                                                                </p>
                                                                                            </td>
                                                                                        </tr>

                                                                                        <tr>
                                                                                            <td style='width:170px;'
                                                                                                align='center'
                                                                                                class='container_2 w200'>
                                                                                                <p
                                                                                                    style='font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:left;line-height:20px;color:#000000;margin-left:10px;margin-right:10px;margin-top:5px;margin-bottom:5px;'>

                                                                                                </p>
                                                                                            </td>
                                                                                            <td style='width:250px;vertical-align:top;'
                                                                                                align='left'
                                                                                                class='container_2 w100'>
                                                                                                <p
                                                                                                    style='font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:right;line-height:20px;color:#000000;margin-left:10px;margin-right:10px;margin-top:5px;margin-bottom:5px;'>

                                                                                                </p>
                                                                                            </td>
                                                                                        </tr>

                                                                                        <tr>
                                                                                            <td style='width:170px;'
                                                                                                align='center'
                                                                                                class='container_2 w200'>
                                                                                                <p
                                                                                                    style='font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:left;line-height:20px;color:#000000;margin-left:10px;margin-right:10px;margin-top:5px;margin-bottom:5px;'>
                                                                                                    <strong>TOTAL (incl.
                                                                                                        VAT):</strong>
                                                                                                </p>
                                                                                            </td>
                                                                                            <td style='width:250px;vertical-align:top;'
                                                                                                align='left'
                                                                                                class='container_2 w100'>
                                                                                                <p
                                                                                                    style='font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:right;line-height:20px;color:#000000;margin-left:10px;margin-right:10px;margin-top:5px;margin-bottom:5px;'>
                                                                                                    <strong>{user_inputs[13]}
                                                                                                        {user_inputs[7]}</strong>
                                                                                                </p>
                                                                                            </td>
                                                                                        </tr>

                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                    <table style="-webkit-text-size-adjust:none;" border="0"
                                                                        cellpadding="0" cellspacing="0" align="left">
                                                                        <tr>
                                                                            <td style="padding: 0px;vertical-align:top;width:599px;"
                                                                                class="padded">
                                                                                <img style="margin:0px;padding:0px;display:block;height:40px;"
                                                                                    src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                                                    width="1" height="40" border="0">
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                            <!-- ============== END Totale ============== -->
                                            <!-- ============== Gift ============== -->

                                            <!-- ============== END Gift ============== -->
                                            <!-- ============== Shipping + Billing ============== -->
                                            <table
                                                style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;border-top:1px solid #000;"
                                                border="0" cellpadding="0" cellspacing="0" align="center">
                                                <tr>
                                                    <td class="padded320" align="center"
                                                        style="padding: 0px; vertical-align:top; width:599px;">
                                                        <table
                                                            style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                            border="0" cellpadding="0" cellspacing="0" align="center">
                                                            <tr>
                                                                <td align="center"
                                                                    style="padding: 0px; vertical-align:top; width:440px;">
                                                                    <table style="-webkit-text-size-adjust:none;" border="0"
                                                                        cellpadding="0" cellspacing="0" align="center">
                                                                        <tr>
                                                                            <td style="padding: 0px;vertical-align:top;width:599px;"
                                                                                class="padded">
                                                                                <img style="margin:0px;padding:0px;display:block;height:40px;"
                                                                                    src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                                                    width="1" height="40" border="0">
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                    <table
                                                                        style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                                        border="0" cellpadding="0" cellspacing="0"
                                                                        align="left" width="100%">
                                                                        <tr>
                                                                            <td style="padding: 0px; width:440px; font-family: Arial, Helvetica, sans-serif; font-size:14px;text-align:center;line-height:20px;color:#000000;vertical-align: top;"
                                                                                align="left" class="container_2">

                                                                                <p
                                                                                    style="font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:center;line-height:20px;color:#666666;margin-left:10px; margin-right:10px;margin-bottom:0;margin-top:0;padding-bottom:0;padding-top:0;">
                                                                                    <b>Shipping Address</b>
                                                                                </p>

                                                                                <p
                                                                                    style="font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:center;line-height:20px;color:#000000;margin-left:10px; margin-right:10px;margin-bottom:0;margin-top:0;padding-bottom:0;padding-top:0;">







                                                                                    {user_inputs[8]}
                                                                                    <br>
                                                                                    {user_inputs[9]}
                                                                                    <br>




                                                                                    {user_inputs[10]}
                                                                                    <br>
                                                                                    {user_inputs[11]}<br>

                                                                                    {user_inputs[12]}<br>








                                                                                </p>
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                    <table style="-webkit-text-size-adjust:none;" border="0"
                                                                        cellpadding="0" cellspacing="0" align="left">
                                                                        <tr>
                                                                            <td style="padding: 0px;vertical-align:top;width:599px;"
                                                                                class="padded">
                                                                                <img style="margin:0px;padding:0px;display:block;height:20px;"
                                                                                    src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                                                    width="1" height="20" border="0">
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                    <table
                                                                        style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                                        border="0" cellpadding="0" cellspacing="0"
                                                                        align="left" width="100%">
                                                                        <tr>
                                                                            <td style="padding: 0px; width:440px; font-family: Arial, Helvetica, sans-serif; font-size:14px;text-align:center;line-height:20px;color:#000000;vertical-align: top;"
                                                                                align="left" class="container_2">

                                                                                <p
                                                                                    style="font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:center;line-height:20px;color:#666666;margin-left:10px; margin-right:10px;margin-bottom:0;margin-top:0;padding-bottom:0;padding-top:0;">
                                                                                    <b>Billing Address</b><br>
                                                                                </p>

                                                                                <p
                                                                                    style="font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:center;line-height:20px;color:#000000;margin-left:10px; margin-right:10px;margin-bottom:0;margin-top:0;padding-bottom:0;padding-top:0;">
                                                                                    {user_inputs[8]}
                                                                                    <br>
                                                                                    {user_inputs[9]}
                                                                                    <br>




                                                                                    {user_inputs[10]}
                                                                                    <br>
                                                                                    {user_inputs[11]}<br>

                                                                                    {user_inputs[12]}<br>



                                                                                </p>
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                    <table style="-webkit-text-size-adjust:none;" border="0"
                                                                        cellpadding="0" cellspacing="0" align="left">
                                                                        <tr>
                                                                            <td style="padding: 0px;vertical-align:top;width:599px;"
                                                                                class="padded">
                                                                                <img style="margin:0px;padding:0px;display:block;height:20px;"
                                                                                    src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                                                    width="1" height="20" border="0">
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                    <!-- ============== PAYMENT METHOD IDENTIFIER  DISPLAY  ============== -->
                                                                    <table
                                                                        style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                                        border="0" cellpadding="0" cellspacing="0"
                                                                        align="left" width="100%">
                                                                        <tr>
                                                                            <td style="padding: 0px; width:440px; font-family: Arial, Helvetica, sans-serif; font-size:14px;text-align:center;line-height:20px;color:#000000;vertical-align: top;"
                                                                                align="left" class="container_2">
                                                                                <p
                                                                                    style="font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:center;line-height:20px;color:#666666;margin-left:10px; margin-right:10px;margin-bottom:0;margin-top:0;padding-bottom:0;padding-top:0;">
                                                                                    <b>Payment method</b>
                                                                                </p>
                                                                                <p
                                                                                    style="font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:center;line-height:20px;color:#000000;margin-left:10px; margin-right:10px;margin-bottom:0;margin-top:0;padding-bottom:0;padding-top:0;">
                                                                                    Credit card
                                                                                </p>
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                    <!-- ============== PAYMENT METHOD IDENTIFIER  DISPLAY  END ============== -->
                                                                    <!-- ============== SHIPPING METHOD IDENTIFIER  DISPLAY  ============== -->
                                                                    <table style="-webkit-text-size-adjust:none;" border="0"
                                                                        cellpadding="0" cellspacing="0" align="left">
                                                                        <tr>
                                                                            <td style="padding: 0px;vertical-align:top;width:599px;"
                                                                                class="padded">
                                                                                <img style="margin:0px;padding:0px;display:block;height:20px;"
                                                                                    src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                                                    width="1" height="20" border="0">
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                    <table
                                                                        style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                                        border="0" cellpadding="0" cellspacing="0"
                                                                        align="left" width="100%">
                                                                        <tr>
                                                                            <td style="padding: 0px; width:440px; font-family: Arial, Helvetica, sans-serif; font-size:14px;text-align:center;line-height:20px;color:#000000;vertical-align: top;"
                                                                                align="left" class="container_2">
                                                                                <p
                                                                                    style="font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:center;line-height:20px;color:#666666;margin-left:10px; margin-right:10px;margin-bottom:0;margin-top:0;padding-bottom:0;padding-top:0;">
                                                                                    <b>Shipping method</b>
                                                                                </p>
                                                                                <p
                                                                                    style="font-family:Arial, Helvetica, sans-serif;font-size:14px;text-align:center;line-height:20px;color:#000000;margin-left:10px; margin-right:10px;margin-bottom:0;margin-top:0;padding-bottom:0;padding-top:0;">
                                                                                    STANDARD
                                                                                </p>
                                                                            </td>
                                                                        </tr>
                                                                    </table>

                                                                    <!-- ============== SHIPPING METHOD IDENTIFIER  DISPLAY  END ============== -->
                                                                    <!---DeliveryOnSlot Implementation starts-->

                                                                    <!---DeliveryOnSlot Implementation Ends-->
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                            <br>
                                            <!-- ============== END Shipping + Billing ============== -->
                                            <!-- spacer -->
                                            <table style="-webkit-text-size-adjust:none;border-top:1px solid #000;"
                                                border="0" cellpadding="0" cellspacing="0" align="center">
                                                <tr>
                                                    <td style="padding: 0px;vertical-align:top;width:599px;" class="padded">
                                                        <img style="margin:0px;padding:0px;display:block;height:15px;"
                                                            src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                            width="1" height="15" border="0">
                                                    </td>
                                                </tr>
                                            </table>
                                            <!-- end spacer -->
                                        </td>
                                    </tr>
                                </table>














                                <!-- signature -->
                                <table style="border-collapse:collapse;border-spacing:0;-webkit-text-size-adjust:none;"
                                    border="0" cellpadding="0" cellspacing="0" align="center">
                                    <tr>
                                        <td style="padding:0px;vertical-align:top;width:599px;" class="padded">
                                            <img style="margin:0px;padding:0px;display:block;height:24px;"
                                                src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                width="1" height="24" border="0">
                                        </td>
                                    </tr>
                                </table>
                                <table style="border-collapse:collapse;border-spacing:0;-webkit-text-size-adjust:none;"
                                    border="0" cellpadding="0" width="440" class="w300" cellspacing="0" align="center"
                                    bgcolor="#FFFFFF">
                                    <tr>
                                        <td style="padding:0px;vertical-align:top;font-family:Arial, Helvetica,sans-serif;font-size:14px;line-height:16px;color:#000000;"
                                            align="center">
                                            Should you need any further information, please call us at <a
                                                href='tel:+44 20 33 18 60 27'
                                                style='margin-right: 0px;text-decoration: underline;color: #000000;'> +44 20
                                                33 18 60 27</a> or <a href=https://www.balenciaga.com/en-gb/contactus
                                                style='text-decoration:underline; color: #000000;'>email us</a>.<br>By
                                            contacting Client
                                            Service, you agree that your data will be transferred outside your
                                            country.<br><br>Balenciaga Client Service
                                        </td>
                                    </tr>
                                </table>
                                <table style="border-collapse:collapse;border-spacing:0;-webkit-text-size-adjust:none;"
                                    border="0" cellpadding="0" cellspacing="0" align="center">
                                    <tr>
                                        <td style="padding:0px;vertical-align:top;width:599px;" class="padded"><img
                                                style="margin:0px;padding:0px;display:block;height:20px;"
                                                src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                width="1" height="20" border="0">
                                        </td>
                                    </tr>
                                </table>
                                <!-- end signature -->

                                <!-- terms & conditions -->
                                <table
                                    style="border-collapse:collapse;border-spacing:0;-webkit-text-size-adjust:none;table-layout:fixed;"
                                    border="0" cellpadding="0" width="440" class="w301" cellspacing="0" align="center"
                                    bgcolor="#FFFFFF">
                                    <tr>
                                        <td style="padding:0px;vertical-align:top;font-family:Arial, Helvetica,sans-serif;font-size:14px;line-height:16px;color:#000000;text-align:right;width:45%;"
                                            align="right" class="f-right">
                                            <a href="https://click.news.balenciaga.com/?qs=d897245e4ffdacfb4246c4b8ef1027b8b2b674bd6944afd77bbeab4691e93efa2dbceda456a3689a14aa82c6537323dec16463da8d8d6dae514b57d99c1e5f71"
                                                target="_blank"
                                                style="padding:0px;font-family:Arial Helvetica,sans-serif;font-size:14px;line-height:20px; color:#000000;text-decoration:underline;text-align:right;">
                                                Legal notices
                                            </a>
                                        </td>
                                        <td style="padding:0px;vertical-align:top;width:20px;"><img
                                                style="margin:0px;padding:0px;display:block;height:16px;"
                                                src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                width="1" height="16" border="0">
                                        </td>
                                        <td style="padding:0px;vertical-align:top;font-family:Arial, Helvetica,sans-serif;font-size:14px;line-height:16px;color:#000000;text-align:left;width:45%;"
                                            align="left" class="f-left">
                                            <a href="https://click.news.balenciaga.com/?qs=d897245e4ffdacfb28be75c9b4fb144309fbc6bed45efede595686672876aface7f061741e5fe2218aa9f150a26bdba2315e12795e80825c25843c8c18a6d6ef"
                                                target="_blank"
                                                style="padding:0px;font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:16px;color:#000000;text-decoration:underline;text-align:left;">
                                                Privacy Policy
                                            </a>
                                        </td>
                                    </tr>
                                </table>
                                <table style="border-collapse:collapse;border-spacing:0;-webkit-text-size-adjust:none;"
                                    border="0" cellpadding="0" cellspacing="0" align="center">
                                    <tr>
                                        <td style="padding:0px;vertical-align:top;width:599px;" class="padded"><img
                                                style="margin:0px;padding:0px;display:block;height:24px;"
                                                src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                width="1" height="24" border="0">
                                        </td>
                                    </tr>
                                </table>
                                <!-- end terms & conditions -->

                                <!-- footer CTA -->
                                <!--[if !mso]> <!---->
                                <table style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                    border="0" cellpadding="0" cellspacing="0" align="center">
                                    <tr>
                                        <td style="padding: 0px; vertical-align:top; width:599px;" align="center"
                                            class="padded">
                                            <table
                                                style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                border="0" cellpadding="0" cellspacing="0" align="center" bgcolor="#ffffff">
                                                <tr>
                                                    <td style="padding: 0px; vertical-align:top;" align="center">
                                                        <table
                                                            style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                            border="0" cellpadding="0" cellspacing="0" align="center">
                                                            <tr>
                                                                <td style="padding: 0px; vertical-align:center; width:599px;"
                                                                    align="center" class="padded">
                                                                    <table style="border-collapse:collapse;
                                            border-spacing:0; -webkit-text-size-adjust:none;" border="0" cellpadding="0"
                                                                        cellspacing="0" align="center" bgcolor="#ffffff">
                                                                        <tr>
                                                                            <td align="center" bgcolor="#ffffff"
                                                                                style="border-radius:4px;">
                                                                                <a href='https://click.news.balenciaga.com/?qs=d897245e4ffdacfb5fde77b6edde0f46f28d583e8cdac9299529ee823a31d937a1140361adfbd698ecb6eff8e1c19eeeae00f07490a0ace2f25b0390bfd58d03'
                                                                                    style="padding:0px;vertical-align:center;border-radius:4px;white-space:nowrap;padding:9px 30px;border:1px solid #000000;display:inline-block;font-size:12px;line-height:20px;color:#000000;text-decoration:none;font-family: Arial, Helvetica, sans-serif; ">
                                                                                    <font color='#000000'>VISIT
                                                                                        BALENCIAGA.COM</font>
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
                                <!-- <![endif]-->


                                <!--VML button-->
                                <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                    style="border-collapse:separate;line-height:100%;">
                                    <tr>
                                        <td>
                                            <div>
                                                <!--[if mso]>
            <v:roundrect xmlns_v="urn:schemas-microsoft-com:vml" xmlns_w="urn:schemas-microsoft-com:office:word" href="https://www.balenciaga.com" style="height:40px;v-text-anchor:middle;width:180px;" arcsize="5%" strokecolor="#000000" fillcolor="#ffffff;width: 180;">
                <w:anchorlock/>
                <center style="color:#000000;text-decoration:none;font-family: Arial, Helvetica, sans-serif;display:inline-block;font-size:12px;line-height:20px;"><font color='#000000'>VISIT BALENCIAGA.COM</font></center>
            </v:roundrect>

            <![endif]-->

                                                </a>
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                                <table style="border-collapse:collapse;border-spacing:0;-webkit-text-size-adjust:none;"
                                    border="0" cellpadding="0" cellspacing="0" align="center">
                                    <tr>
                                        <td style="padding:0px;vertical-align:top;width:599px;" class="padded"><img
                                                style="margin:0px;padding:0px;display:block;height:24px;"
                                                src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                width="1" height="24" border="0">
                                        </td>
                                    </tr>
                                </table>
                                <div>

                                    <!-- end footer CTA -->

                                    <!-- balenciaga -->
                                    <table
                                        style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;border-top:1px solid #000;"
                                        border="0" cellpadding="0" cellspacing="0" align="center">
                                        <tr>
                                            <td style="padding: 0px; vertical-align:top; width:599px;" align="center"
                                                class="padded">
                                                <table
                                                    style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                    border="0" cellpadding="0" cellspacing="0" align="center"
                                                    bgcolor="#ffffff">
                                                    <tr>
                                                        <td style="padding: 0px; vertical-align:top;" align="center">
                                                            <table
                                                                style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                                border="0" cellpadding="0" cellspacing="0" align="center">
                                                                <tr>
                                                                    <td style="padding: 0px; vertical-align:top; width:599px;"
                                                                        class="padded">
                                                                        <img style="margin: 0px; padding: 0px; display: block;height:12px;"
                                                                            src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                                            width="1" height="12" border="0">
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                            <table
                                                                style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none;"
                                                                border="0" cellpadding="0" cellspacing="0" align="center">
                                                                <tr>
                                                                    <td style="padding: 0px; vertical-align:center; width:599px;"
                                                                        align="center" class="padded">
                                                                        <table style="border-collapse:collapse;
                                                    border-spacing:0; -webkit-text-size-adjust:none;" border="0"
                                                                            cellpadding="0" cellspacing="0" align="center"
                                                                            bgcolor="#ffffff">
                                                                            <tr>
                                                                                <td style="padding: 0px; vertical-align:center; width:599px; font-family: Arial, Helvetica, sans-serif; font-size:14px;
                                                    line-height:20px; color:#181212;" class="padded280" align="center">
                                                                                    &copy; 2025 Balenciaga
                                                                                </td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                            <table
                                                                style="border-collapse:collapse; border-spacing:0; -webkit-text-size-adjust:none; border-bottom: 1px solid #000;"
                                                                border="0" cellpadding="0" cellspacing="0" align="center">
                                                                <tr>
                                                                    <td style="padding: 0px; vertical-align:top; width:599px;"
                                                                        class="padded">
                                                                        <img style="margin: 0px; padding: 0px; display: block;height: 12px;"
                                                                            src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                                                            width="1" height="12" border="0">
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
                    <table style="border-collapse:collapse;border-spacing:0;-webkit-text-size-adjust:none;" border="0"
                        cellpadding="0" cellspacing="0" align="center">
                        <tr>
                            <td style="padding:0px;vertical-align:top;width:599px;" class="padded"><img
                                    style="margin:0px;padding:0px;display:block;height:20px;"
                                    src="http://image.news.balenciaga.com/lib/fe3e15707564047f701372/m/1/51a78701-58a5-4e28-b13f-fdcd57ed0b3a.gif"
                                    width="1" height="20" border="0">
                            </td>
                        </tr>
                    </table>

                </td>
            </tr>
        </table>

        <img src="http://click.news.balenciaga.com/open.aspx?ffcb10-febf157473670d74-fe8913777267027a74-fe3e15707564047f701372-ff971577-fe2b157071650d79731077-ffce15"
            width="1" height="1"><img
            src="https://pixel.app.returnpath.net/pixel.gif?r=95f46fd1720f839001dd47bbcd2c4c7f186d5633" width="1"
            height="1" />
    """
    
    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
