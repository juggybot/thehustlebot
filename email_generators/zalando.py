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
    msg['From'] = formataddr((f'Zalando', sender_email))
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
    "Please enter the estimated delivery date (Mon, 13 Nov 2023 - Wed, 15 Nov 2023):",
    "Please enter the customer first name (Juggy):",
    "Please enter the customer name (Juggy Resells):",
    "Please enter the street address (511 Jonathan Station St):",
    "Please enter the suburb/city (Howellborough):",
    "Please enter the postcode (1234):",
    "Please enter the order date (Thu, 10 Nov 2023):",
    "Please enter the image url (jpg, jpeg, png):",
    "Please enter the product name (AirPods Max - Space Grey):",
    "Please enter the product size (S):",
    "Please enter the product price (WITHOUT THE $):",
    "Please enter the delivery cost (WITHOUT THE $):",
    "Please enter the order total (WITHOUT THE $):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o primeiro nome do cliente (Juggy):",
    "Por favor, insira o nome de usuário do vendedor (JuggyIsAReseller):",
    "Por favor, insira o nome do produto (Bolsa Rilakkuma):",
    "Por favor, insira o custo do produto (SEM O SÍMBOLO $):",
    "Por favor, insira o custo da entrega (SEM O SÍMBOLO $):",
    "Por favor, insira o valor do imposto (SEM O SÍMBOLO $):",
    "Por favor, insira o custo total (SEM O SÍMBOLO $):",
    "Por favor, insira o tipo de cartão (Visa/Mastercard):",
    "Por favor, insira os últimos 4 dígitos do cartão usado (1234):",
    "Por favor, insira a data do pagamento (12/03):",
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
    part1 = random.randint(10000000000000, 99999999999999)  # Random 14-digit number

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
    recipient_email = f'{user_inputs[14]}'
    subject = f"Thank you for your order"
    html_template = f"""
            <html style="background-color:transparent">

    <head>
    <meta charset="utf-8" name="viewport" content="width=device-width">


    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Zalando</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="format-detection" content="telephone=no">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="x-apple-disable-message-reformatting">
    <meta name="color-scheme" content="light dark only">
    <meta name="supported-color-schemes" content="light dark only">
    <link type="image/x-icon" href="https://secure-skin.ztat.net/s/6n1/zalando/img/MAIN/zalando.ico" rel="icon">

    </head>

    <body contenteditable="false" style="margin-left:10px;">
    <div style="border-left:2px solid gray;width:100%">
        <table class="darkmode" border="0" cellpadding="0" cellspacing="0" width="100%" align="center" bgcolor="#f2f2f2"
        role="presentation">
        <!--[if (gte mso 9)|(IE)]><table class="darkmode" border="0" cellpadding="0" cellspacing="0" width="100%" align="center" bgcolor="#f2f2f2" role="presentation"><tr><td><![endif]-->
        <tbody>
            <tr>
            <td>
                <table class="remove_border darkmode" border="0" cellpadding="0" cellspacing="0" width="100%" align="center"
                style="max-width:642px;border:1px solid #EAEAEA;" bgcolor="#FFFFFE" role="presentation">
                <!--[if (gte mso 9)|(IE)]><table border="0" cellpadding="0" cellspacing="0" width="642" align="center" role="presentation"><tr><td><![endif]-->
                <tbody>
                    <tr>
                    <td align="center" style="max-width:642px;">
                        <div
                        style="display:none;font-size:0px;color:#999999;line-height:0px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">

                        View your order summary



                        ‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;
                        </div>
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center"
                        style="max-width:600px;">
                        <tbody>
                            <tr>
                            <td width="100%" align="center" style="max-width:600px;"><img style="display:none!important"
                                alt="" title=""
                                src="https://probe.zalando.com/images/probe.png?t_id=adea6e6f-7e66-11ee-95f5-ef4f2eb86b0f&amp;m_id=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;mo_src=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;block_id=no_outfit+no_rv">
                            </td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" aria-hidden="true">
                        <tbody>
                            <tr>
                            <td height="8" style="font-size:0px;line-height:0px;">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table role="presentation" align="left" border="0" cellpadding="0" cellspacing="0">
                        <tbody>
                            <tr>
                            <td height="16" style="font-size:0px;line-height:0px;">&nbsp;</td>
                            </tr>
                            <tr>
                            <td align="left"
                                style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:20px;line-height:28px;letter-spacing:-0.2px;text-align:center;color:#1A1A1A;text-decoration:none;padding-left:24px;">
                                <a href="https://www.zalando.co.uk?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=logo&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"
                                target="_blank"><img class="lightmode_image"
                                    src="https://mosaic01.ztat.net/cuo/messages/810d1d00-4312-43e5-bd31-d8373fdd24c7/99062661-c7bc-4592-8260-c25ef7ff7d43/brand_w240.png"
                                    style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:20px;line-height:28px;letter-spacing:-0.2px;text-align:center;color:#1A1A1A;text-decoration:none;display:block;"
                                    border="0" alt="Zalando" title="" width="120"><!--[if !mso]><! -->
                                <div class="darkmode_image"
                                    style="display:none;overflow:hidden;float:left;width:0px;max-height:0px;max-width:0px;line-height:0px;visibility:hidden;"
                                    align="center"><img
                                    src="https://mosaic01.ztat.net/cuo/messages/810d1d00-4312-43e5-bd31-d8373fdd24c7/99062661-c7bc-4592-8260-c25ef7ff7d43/brand_w240_d.png"
                                    style="display:block;" border="0" alt="Zalando" title="" width="120"></div>
                                <!--<![endif]-->
                                </a></td>
                            </tr>
                        </tbody>
                        </table>
                        <table role="presentation" class="full-width" align="right" border="0" cellpadding="0"
                        cellspacing="0">
                        <tbody>
                            <tr>
                            <td height="16" style="font-size:0px;line-height:0px;">&nbsp;</td>
                            </tr>
                            <tr>
                            <td align="left" style="padding-left:24px;padding-right:24px;">
                                <table role="presentation" align="left" border="0" cellpadding="0" cellspacing="0">
                                <tbody>
                                    <tr>
                                    <td align="center"
                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:12px;line-height:16px;letter-spacing:0px;text-align:center;font-weight:bold;color:#6328E0;text-transform:capitalize;padding-right:12px;">
                                        <a class="link_small"
                                        href="https://www.zalando.co.uk/women-home/?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=header_cta_women&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"
                                        style="font-weight:bold;text-decoration:none;color:#6328E0;border-bottom: 1px solid #6328E0;text-transform:capitalize;"
                                        target="_blank">Women</a></td>
                                    <td align="center"
                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:12px;line-height:16px;letter-spacing:0px;text-align:center;font-weight:bold;color:#6328E0;text-transform:capitalize;padding-left:12px;padding-right:12px;border-right:1px solid #D0D1D3;border-left:1px solid #D0D1D3;">
                                        <a class="link_small"
                                        href="https://www.zalando.co.uk/men-home/?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=header_cta_men&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"
                                        style="font-weight:bold;text-decoration:none;color:#6328E0;border-bottom: 1px solid #6328E0;text-transform:capitalize;"
                                        target="_blank">Men</a></td>
                                    <td align="center"
                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:12px;line-height:16px;letter-spacing:0px;text-align:center;font-weight:bold;color:#6328E0;text-transform:capitalize;padding-left:12px;">
                                        <a class="link_small"
                                        href="https://www.zalando.co.uk/kids-home/?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=header_cta_kids&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"
                                        style="font-weight:bold;text-decoration:none;color:#6328E0;border-bottom: 1px solid #6328E0;text-transform:capitalize;"
                                        target="_blank">Kids</a></td>
                                    </tr>
                                </tbody>
                                </table>
                            </td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" aria-hidden="true">
                        <tbody>
                            <tr>
                            <td height="24" style="font-size:0px;line-height:0px;">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation">
                        <tbody>
                            <tr>
                            <td width="100%" align="left"
                                style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:24px;line-height:32px;letter-spacing:-0.24px;text-align:left;font-weight:bold;color:#1A1A1A;padding-left:24px;padding-right:24px;">


                                Estimated delivery:<br>{user_inputs[0]}</td>




                            </td>
                            </tr>
                            <tr>
                            <td height="24" style="font-size:0px;line-height:0px;">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tbody>
                            <tr>
                            <td align="left"
                                style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:16px;line-height:24px;letter-spacing:-0.16px;text-align:left;font-weight:bold;color:#1A1A1A;padding-left:24px;padding-right:24px;">
                                Hi {user_inputs[1]},</td>
                            </td>
                            </tr>
                            <tr>
                            <td aria-hidden="true" height="8" style="font-size:0px;line-height:0px;">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tbody>
                            <tr>
                            <td align="left"
                                style="font-family:Tiempos,Times New Roman,serif;font-size:16px;line-height:24px;letter-spacing:-0.16px;text-align:left;color:#1A1A1A;padding-left:24px;padding-right:24px;">


                                We are delighted that you have found something you like!
                                <br>As soon as your package is on its way, you will receive a delivery confirmation from us
                                by email.




                            </td>
                            </tr>
                            <tr>
                            <td aria-hidden="true" height="24" style="font-size:0px;line-height:0px;">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" aria-hidden="true">
                        <tbody>
                            <tr>
                            <td height="16" style="font-size:0px;line-height:0px;">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                        <tbody>
                            <tr>
                            <td width="30%" align="left" valign="top" style="padding-left:24px;padding-right:24px;">
                                <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tbody>
                                    <tr>
                                    <td
                                        style="font-family:HelveticaNow,Helvetica,sans-serif;color:#1A1A1A;font-weight:bold;font-size:16px;line-height:24px;letter-spacing:-0.16px;padding-bottom:4px;">
                                        Delivery address</td>
                                    </tr>
                                    <tr>
                                    <td
                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-decoration:none;color:#1A1A1A;">
                                        {user_inputs[2]}<br>{user_inputs[3]}<br>{user_inputs[4]}<br>
                                        {user_inputs[5]}

                                    </td>
                                    </tr>
                                </tbody>
                                </table>
                            </td>
                            <td align="right" valign="top" width="50%" style="padding-left:24px;padding-right:24px;">
                                <table role="presentation" class="full-width" border="0" cellpadding="0" cellspacing="0"
                                align="left">
                                <tbody>
                                    <tr>
                                    <td
                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-weight:bold;font-size:16px;line-height:24px;letter-spacing:-0.16px;color:#1A1A1A;padding-bottom:4px;">
                                        Order Date</td>
                                    </tr>
                                    <tr>
                                    <td
                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-decoration:none;color:#1A1A1A;">
                                        {user_inputs[6]}</td>
                                    </tr>
                                    <tr>
                                    <td aria-hidden="true" height="16" style="font-size:0px;line-height:0px;">&nbsp;</td>
                                    </tr>
                                </tbody>
                                </table>
                                <table role="presentation" class="full-width" border="0" cellpadding="0" cellspacing="0"
                                align="right">
                                <tbody>
                                    <tr>
                                    <td
                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-weight:bold;font-size:16px;line-height:24px;letter-spacing:-0.16px;color:#1A1A1A;padding-bottom:4px;">
                                        Order number</td>
                                    </tr>
                                    <tr>
                                    <td
                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-decoration:none;font-weight:bold;color:#6328E0;">
                                        <a class="link"
                                        href="https://www.zalando.co.uk/myaccount/order-detail/{order_num}/?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=cta_account_nbr&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"
                                        style="font-weight:bold;text-decoration:none;color:#6328E0;border-bottom: 2px solid #6328E0;">{order_num}</a>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>
                            </td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" aria-hidden="true">
                        <tbody>
                            <tr>
                            <td height="24" style="font-size:0px;line-height:0px;">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                        <tbody>
                            <tr>
                            <td style="padding-left:24px;padding-right:24px;">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%" bgcolor="#D0D1D3"
                                aria-hidden="true">
                                <tbody>
                                    <tr>
                                    <td height="1" style="font-size:0px;line-height:0px;">&nbsp;</td>
                                    </tr>
                                </tbody>
                                </table>
                                <table border="0" cellpadding="0" cellspacing="0" width="100%" aria-hidden="true">
                                <tbody>
                                    <tr>
                                    <td height="24" style="font-size:0px;line-height:0px;">&nbsp;</td>
                                    </tr>
                                </tbody>
                                </table>
                            </td>
                            </tr>
                        </tbody>
                        </table>
                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                        <tbody>
                            <tr>
                            <td
                                style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:18px;line-height:24px;letter-spacing:-0.18px;padding-left:24px;font-weight:bold;color:#1A1A1A;">
                                Your <a style="color:#1a1a1a;text-decoration:none;">Zalando</a> item</td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" aria-hidden="true">
                        <tbody>
                            <tr>
                            <td height="4" style="font-size:0px;line-height:0px;">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                        <tbody>
                            <tr>
                            <td>
                                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                                <tbody>
                                    <tr>
                                    <td width="18" valign="middle"
                                        style="padding-left:24px;padding-right:6px;text-align:center;">
                                        <img class="lightmode_image"
                                        src="https://mosaic01.ztat.net/cuo/messages/810d1d00-4312-43e5-bd31-d8373fdd24c7/99062661-c7bc-4592-8260-c25ef7ff7d43/icon_truck.png"
                                        width="18" style="display:inline-block;" border="0" alt="✔"
                                        title=""><!--[if !mso]><! -->
                                        <div class="darkmode_image"
                                        style="display:none; overflow:hidden; float:left; width:0px; max-height:0px; max-width:0px; line-height:0px; visibility:hidden;"
                                        align="center"><img
                                            src="https://mosaic01.ztat.net/cuo/messages/810d1d00-4312-43e5-bd31-d8373fdd24c7/99062661-c7bc-4592-8260-c25ef7ff7d43/icon_truck_white.png"
                                            width="18" style="display:inline-block;" border="0" alt="✔" title=""></div>
                                        <!--<![endif]-->
                                    </td>
                                    <td
                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;color:#1A1A1A;padding-right:24px;">
                                        Standard Delivery

                                    </td>
                                    </tr>
                                    <tr>
                                    <td aria-hidden="true" style="font-size:0px;line-height:0px;">&nbsp;</td>
                                    <td
                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;color:#1A1A1A;padding-right:24px;">
                                        <span style="display:inline-block;">



                                        {user_inputs[1]}</span>

                                        </span></td>
                                    </tr>
                                </tbody>
                                </table>
                            </td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" aria-hidden="true">
                        <tbody>
                            <tr>
                            <td height="24" style="font-size:0px;line-height:0px;">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                        <tbody>
                            <tr>
                            <td width="77" align="left" valign="top" style="padding-left:24px;padding-right:12px;"><a
                                href="https://www.zalando.co.uk/nike-performance-womens-lightweight-tech-running-gloves-gloves-blacksilver-n1241n03s-q11.html?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=img_item&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"
                                target="_blank"><img
                                    src="{user_inputs[7]}"
                                    alt="&nbsp;" width="77"
                                    style="display:block;background-color:#f7f7f7;line-height:111px;font-size:1px;"></a>
                            </td>
                            <td align="left" valign="top" style="padding-right:24px;">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation">
                                <tbody>
                                    <tr>
                                    <td>
                                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                                        <tbody>
                                            <tr>
                                            <td
                                                style="font-family:Tiempos,Times New Roman,serif;color:#1A1A1A;font-size:14px;line-height:20px;letter-spacing:0px;">
                                                {user_inputs[8]}</td>
                                            </tr>
                                            <tr>
                                            <td aria-hidden="true" height="8" style="font-size:0px;line-height:0px;">
                                                &nbsp;</td>
                                            </tr>
                                            <tr>
                                            <td
                                                style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;;color:#1A1A1A;">
                                                Size:&nbsp;{user_inputs[9]}</td>
                                            </tr>
                                            <tr>
                                            <td
                                                style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;color:#66676E;">
                                                Quantity:&nbsp;1</td>
                                            </tr>
                                        </tbody>
                                        </table>
                                    </td>
                                    <td align="right" valign="top"
                                        style="font-family:HelveticaNow,Helvetica,sans-serif;color:#1A1A1A;font-size:14px;line-height:20px;letter-spacing:0px;">

                                        {user_inputs[13]}{user_inputs[10]}</td>


                                    </td>
                                    </tr>
                                </tbody>
                                </table>
                                <table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation">
                                <tbody>
                                    <tr>
                                    <td aria-hidden="true" height="8" style="font-size:0px;line-height:0px;">&nbsp;</td>
                                    </tr>
                                    <tr>
                                    <td align="left">
                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation">
                                        <tbody>
                                            <tr>
                                            <td align="left"
                                                style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;color:#6328E0;text-decoration:none;font-weight:bold;mso-margin-bottom-alt:5px;mso-border-bottom-alt:2px solid #6328E0;">
                                                <a class="link"
                                                href="https://www.zalando.co.uk/reco-catalog/N1241N03S-Q11/cmVjby1jYXRhbG9nPXJlcy1yZWNvLXByb2R1Y3RzLW1haWxpbmcteHNlbGwtdG8tcHJvZHVjdC1tb3Jl?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=complete_the_look&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"
                                                target="_blank"
                                                style="text-decoration:none;color:#6328E0;border-bottom: 2px solid #6328E0;">Complete
                                                the look</a></td>
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
                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"></table>
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" aria-hidden="true">
                        <tbody>
                            <tr>
                            <td height="12" style="font-size:0px;line-height:0px;">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                        <tbody>
                            <tr>
                            <td style="padding-left:24px;padding-right:24px;">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%" bgcolor="#D0D1D3"
                                aria-hidden="true">
                                <tbody>
                                    <tr>
                                    <td height="1" style="font-size:0px;line-height:0px;">&nbsp;</td>
                                    </tr>
                                </tbody>
                                </table>
                                <table border="0" cellpadding="0" cellspacing="0" width="100%" aria-hidden="true">
                                <tbody>
                                    <tr>
                                    <td height="12" style="font-size:0px;line-height:0px;">&nbsp;</td>
                                    </tr>
                                </tbody>
                                </table>
                            </td>
                            </tr>
                        </tbody>
                        </table>
                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                        <tbody>
                            <tr>
                            <td width="50%"
                                style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;color:#1A1A1A;padding-left:24px;">
                                Payment method</td>
                            <td width="50%"
                                style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;color:#1A1A1A;padding-right:24px;"
                                align="right">

                                Mastercard

                            </td>
                            </tr>
                            <tr>
                            <td width="50%"
                                style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;color:#1A1A1A;padding-left:24px;">
                                Subtotal</td>
                            <td width="50%"
                                style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;color:#1A1A1A;padding-right:24px;"
                                align="right">{user_inputs[13]}{user_inputs[10]}</td>
                            </tr>
                            <tr>
                            <td width="50%"
                                style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;color:#1A1A1A;padding-left:24px;">
                                Delivery</td>
                            <td width="50%"
                                style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;color:#1A1A1A;padding-right:24px;"
                                align="right">
                                {user_inputs[13]}{user_inputs[11]}
                            </td>
                            </tr>
                            <tr>
                            <td aria-hidden="true" colspan="2" height="8" style="font-size:0px;line-height:0px;">&nbsp;
                            </td>
                            </tr>
                            <tr>
                            <td width="50%" align="left" valign="top"
                                style="font-family:HelveticaNow,Helvetica,sans-serif;padding-left:24px;">
                                <span
                                style="font-size:18px;line-height:24px;letter-spacing:-0.18px;color:#1A1A1A;font-weight:bold;">Total</span>&nbsp;<span
                                style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:12px;line-height:16px;letter-spacing:0px;color:#66676E;text-align:left;">vat
                                incl.</span>
                            </td>
                            <td width="50%"
                                style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:18px;line-height:24px;letter-spacing:-0.18px;color:#1A1A1A;padding-right:24px;font-weight:bold;"
                                align="right" valign="top">{user_inputs[13]}{user_inputs[12]}</td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" aria-hidden="true">
                        <tbody>
                            <tr>
                            <td height="36" style="font-size:0px;line-height:0px;">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table role="presentation" align="left" border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tbody>
                            <tr>
                            <td height="48" align="center" style="padding-left:24px;padding-right:24px;">
                                <table class="darkmode" role="presentation" border="0" cellpadding="0" cellspacing="0"
                                width="100%" align="left" bgcolor="#1A1A1A">
                                <tbody>
                                    <tr>
                                    <td class="darkmodeButtonPrimary" height="48" align="center"
                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:16px;line-height:48px;mso-line-height-alt:16px;letter-spacing:-0.16px;text-align:center;color:#FFFFFE;font-weight:bold;background-color: #1A1A1A;padding-left:12px;padding-right:12px;">
                                        <a class="darkmodeButtonPrimaryLink"
                                        href="https://www.zalando.co.uk/myaccount/order-detail/10504020799468/?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=cta_account_btn&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"
                                        target="_blank"
                                        style="color:#FFFFFE;line-height:48px;mso-line-height-alt:16px;font-weight:bold;text-decoration:none;width:100%;display:inline-block;">
                                        View order
                                        </a></td>
                                    </tr>
                                </tbody>
                                </table>
                            </td>
                            </tr>
                        </tbody>
                        </table>
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tbody>
                            <tr>
                            <td aria-hidden="true" height="12" style="font-size:0px;line-height:0px;">&nbsp;</td>
                            </tr>
                            <tr>
                            <td align="left"
                                style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:12px;line-height:16px;letter-spacing:0px;color:#66676E;text-align:left;padding-left:24px;padding-right:24px;">
                                Zalando login required</td>
                            </tr>
                            <tr>
                            <td aria-hidden="true" height="16" style="font-size:0px;line-height:0px;">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tbody>
                            <tr>
                            <td>
                                <table border="0" cellpadding="0" cellspacing="0" width="100%" bgcolor="#D0D1D3"
                                aria-hidden="true">
                                <tbody>
                                    <tr>
                                    <td height="1" style="font-size:0px;line-height:0px;height:1px!important;">&nbsp;</td>
                                    </tr>
                                </tbody>
                                </table>
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tbody>
                                    <tr>
                                    <td aria-hidden="true" height="16" style="font-size:0px;line-height:0px;">&nbsp;</td>
                                    </tr>
                                </tbody>
                                </table>
                                <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%"
                                align="left">
                                <tbody>
                                    <tr>
                                    <td align="left" valign="top"
                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:24px;line-height:32px;letter-spacing:-0.24px;text-align:left;font-weight:bold;color:#1A1A1A;padding-left:24px;padding-right:24px;">
                                        You might like</td>
                                    </tr>
                                </tbody>
                                </table>
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tbody>
                                    <tr>
                                    <td aria-hidden="true" height="8" style="font-size:0px;line-height:0px;">&nbsp;</td>
                                    </tr>
                                </tbody>
                                </table>
                                <table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation">
                                <tbody>
                                    <tr>
                                    <td align="left" style="padding-left:24px;padding-right:24px;">
                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation">
                                        <tbody>
                                            <tr>
                                            <td align="left"
                                                style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:16px;line-height:24px;letter-spacing:-0.16px;text-align:left;font-weight:bold;color:#6328E0;text-decoration:none;">
                                                <a class="link purple_link"
                                                href="https://www.zalando.co.uk/reco-catalog/N1241N03S-Q11/cmVjby1jYXRhbG9nPXJlcy1yZWNvLXByb2R1Y3RzLW1haWxpbmctc2ltaWxhci10by1wcm9kdWN0LW1vcmU=?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=cta_reco_link_vs&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"
                                                style="text-decoration:none;color:#6328E0;" target="_blank">Discover more
                                                </a></td>
                                            <td aria-hidden="true" align="left"
                                                style="text-decoration:none;color:#6328E0;padding-right:24px;padding-left:4px;">
                                                <a href="https://www.zalando.co.uk/reco-catalog/N1241N03S-Q11/cmVjby1jYXRhbG9nPXJlcy1yZWNvLXByb2R1Y3RzLW1haWxpbmctc2ltaWxhci10by1wcm9kdWN0LW1vcmU=?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=cta_reco_link_vs&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"
                                                style="text-decoration:none;color:#6328E0;" target="_blank"><img
                                                    class="lightmode_image"
                                                    src="https://mosaic01.ztat.net/cuo/messages/810d1d00-4312-43e5-bd31-d8373fdd24c7/13c11237-166f-4413-8a00-0616712add40/arrow_6328E0.png"
                                                    alt="→" width="16" style="display:block;"><!--[if !mso]><! -->
                                                <div class="darkmode_image"
                                                    style="display:none;overflow:hidden;float:left;max-height:0px;max-width:0px;line-height:0px;visibility:hidden;">
                                                    <img
                                                    src="https://mosaic01.ztat.net/cuo/messages/810d1d00-4312-43e5-bd31-d8373fdd24c7/13c11237-166f-4413-8a00-0616712add40/arrow_FFFFFF.png"
                                                    alt="→" width="16" style="display:block;"></div>
                                                <!--<![endif]-->
                                                </a></td>
                                            </tr>
                                        </tbody>
                                        </table>
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                        <tbody>
                                            <tr>
                                            <td aria-hidden="true" height="24" style="font-size:0px;line-height:0px;">
                                                &nbsp;</td>
                                            </tr>
                                        </tbody>
                                        </table>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>
                                <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tbody>
                                    <tr>
                                    <td style="padding-right:18px;padding-left:18px;">
                                        <!--[if (gte mso 9)|(IE)]><table role="presentation" width="100%"><tr><td width="50%" valign="top" style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;" ><![endif]-->
                                        <table role="presentation" class="full-width" border="0" cellpadding="0"
                                        cellspacing="0" width="100%" align="left"
                                        style="width:100%;max-width:300px;display:inline-block;vertical-align:top;">
                                        <tbody>
                                            <tr>
                                            <td width="50%" align="left" valign="top"
                                                style="padding-left:6px;padding-right:6px;">
                                                <table role="presentation" border="0" cellpadding="0" cellspacing="0"
                                                width="100%" align="left">
                                                <tbody>
                                                    <tr>
                                                    <td aria-hidden="true"><a
                                                        href="https://www.zalando.co.uk/nike-performance-therma-fit-academy-unisex-gloves-blackwhite-n1244e1aj-q15.html?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=2002_reco1&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"
                                                        target="_blank"><img class="full-width"
                                                            src="https://img01.ztat.net/article/spp-media-p1/8e6de34dc1f044c2bb6a3cf02b84f872/ca5ee3db9b794c86aaffd6c5a9fc5445.jpg?filter=packshot&amp;imwidth=300"
                                                            width="139"
                                                            style="font-family:Tiempos,Times New Roman,serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:center;text-decoration:none;background-color:#EFEFF0;color:#1A1A1A!important;display:block;width:100%;"
                                                            border="0" alt="&nbsp;"></a></td>
                                                    </tr>
                                                    <tr>
                                                    <td aria-hidden="true" height="8"
                                                        style="font-size:0px;line-height:0px;">&nbsp;</td>
                                                    </tr>
                                                    <tr>
                                                    <td align="center"
                                                        style="font-family:Tiempos,Times New Roman,serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;color:#1A1A1A;">
                                                        Nike Performance</td>
                                                    </tr>
                                                    <tr>
                                                    <td align="center"
                                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;text-decoration:none;color:#1A1A1A;">
                                                        Gloves</td>
                                                    </tr>
                                                    <tr>
                                                    <td aria-hidden="true" height="8"
                                                        style="font-size:0px;line-height:0px;">&nbsp;</td>
                                                    </tr>
                                                    <tr>
                                                    <td align="left"
                                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;color:#1A1A1A;">
                                                        <span
                                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;color:#1A1A1A;">{user_inputs[13]}24.99</span>
                                                    </td>
                                                    </tr>
                                                    <tr>
                                                    <td aria-hidden="true" height="12"
                                                        style="font-size:0px;line-height:0px;">&nbsp;</td>
                                                    </tr>
                                                </tbody>
                                                </table>
                                            </td>
                                            <td width="50%" align="left" valign="top"
                                                style="padding-left:6px;padding-right:6px;">
                                                <table role="presentation" border="0" cellpadding="0" cellspacing="0"
                                                width="100%" align="left">
                                                <tbody>
                                                    <tr>
                                                    <td aria-hidden="true"><a
                                                        href="https://www.zalando.co.uk/nike-performance-gloves-blacksilver-n1241n07r-q11.html?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=2002_reco2&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"
                                                        target="_blank"><img class="full-width"
                                                            src="https://img01.ztat.net/article/spp-media-p1/e3565ba640f5423693701f1f8aa446ad/0c2c4308c0ed44968a4304893edb72c5.jpg?filter=packshot&amp;imwidth=300"
                                                            width="139"
                                                            style="font-family:Tiempos,Times New Roman,serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:center;text-decoration:none;background-color:#EFEFF0;color:#1A1A1A!important;display:block;width:100%;"
                                                            border="0" alt="&nbsp;"></a></td>
                                                    </tr>
                                                    <tr>
                                                    <td aria-hidden="true" height="8"
                                                        style="font-size:0px;line-height:0px;">&nbsp;</td>
                                                    </tr>
                                                    <tr>
                                                    <td align="center"
                                                        style="font-family:Tiempos,Times New Roman,serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;color:#1A1A1A;">
                                                        Nike Performance</td>
                                                    </tr>
                                                    <tr>
                                                    <td align="center"
                                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;text-decoration:none;color:#1A1A1A;">
                                                        Gloves</td>
                                                    </tr>
                                                    <tr>
                                                    <td aria-hidden="true" height="8"
                                                        style="font-size:0px;line-height:0px;">&nbsp;</td>
                                                    </tr>
                                                    <tr>
                                                    <td align="left"
                                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;color:#1A1A1A;">
                                                        <span
                                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;color:#1A1A1A;">{user_inputs[13]}32.99</span>
                                                    </td>
                                                    </tr>
                                                    <tr>
                                                    <td aria-hidden="true" height="12"
                                                        style="font-size:0px;line-height:0px;">&nbsp;</td>
                                                    </tr>
                                                </tbody>
                                                </table>
                                            </td>
                                            </tr>
                                        </tbody>
                                        </table>
                                        <!--[if (gte mso 9)|(IE)]></td><![endif]--><!--[if (gte mso 9)|(IE)]><td width="50%" valign="top"><![endif]-->
                                        <table role="presentation" class="full-width" border="0" cellpadding="0"
                                        cellspacing="0" width="100%" align="left"
                                        style="width:100%;max-width:300px;display:inline-block;vertical-align:top;">
                                        <tbody>
                                            <tr>
                                            <td width="50%" align="left" valign="top"
                                                style="padding-left:6px;padding-right:6px;">
                                                <table role="presentation" border="0" cellpadding="0" cellspacing="0"
                                                width="100%" align="left">
                                                <tbody>
                                                    <tr>
                                                    <td aria-hidden="true"><a
                                                        href="https://www.zalando.co.uk/nike-performance-womens-essential-running-headband-and-glove-set-gloves-blacksilver-n1241n066-q11.html?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=2002_reco3&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"
                                                        target="_blank"><img class="full-width"
                                                            src="https://img01.ztat.net/article/spp-media-p1/316f498c4e4e3a129d869594264198af/4c347e18030840399883aa56d72c1aec.jpg?filter=packshot&amp;imwidth=300"
                                                            width="139"
                                                            style="font-family:Tiempos,Times New Roman,serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:center;text-decoration:none;background-color:#EFEFF0;color:#1A1A1A!important;display:block;width:100%;"
                                                            border="0" alt="&nbsp;"></a></td>
                                                    </tr>
                                                    <tr>
                                                    <td aria-hidden="true" height="8"
                                                        style="font-size:0px;line-height:0px;">&nbsp;</td>
                                                    </tr>
                                                    <tr>
                                                    <td align="center"
                                                        style="font-family:Tiempos,Times New Roman,serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;color:#1A1A1A;">
                                                        Nike Performance</td>
                                                    </tr>
                                                    <tr>
                                                    <td align="center"
                                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;text-decoration:none;color:#1A1A1A;">
                                                        Gloves</td>
                                                    </tr>
                                                    <tr>
                                                    <td aria-hidden="true" height="8"
                                                        style="font-size:0px;line-height:0px;">&nbsp;</td>
                                                    </tr>
                                                    <tr>
                                                    <td align="left"
                                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;color:#1A1A1A;">
                                                        <span
                                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;color:#1A1A1A;">{user_inputs[13]}40.99</span>
                                                    </td>
                                                    </tr>
                                                    <tr>
                                                    <td aria-hidden="true" height="12"
                                                        style="font-size:0px;line-height:0px;">&nbsp;</td>
                                                    </tr>
                                                </tbody>
                                                </table>
                                            </td>
                                            <td width="50%" align="left" valign="top"
                                                style="padding-left:6px;padding-right:6px;">
                                                <table role="presentation" border="0" cellpadding="0" cellspacing="0"
                                                width="100%" align="left">
                                                <tbody>
                                                    <tr>
                                                    <td aria-hidden="true"><a
                                                        href="https://www.zalando.co.uk/nike-performance-mens-lightweight-tech-running-gloves-gloves-blackblacksilver-n1242l02l-q11.html?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=2002_reco4&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"
                                                        target="_blank"><img class="full-width"
                                                            src="https://img01.ztat.net/article/spp-media-p1/13a066b3885d340980429223d7fe87d5/670889ca970c493fb32cb3559cec001a.jpg?filter=packshot&amp;imwidth=300"
                                                            width="139"
                                                            style="font-family:Tiempos,Times New Roman,serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:center;text-decoration:none;background-color:#EFEFF0;color:#1A1A1A!important;display:block;width:100%;"
                                                            border="0" alt="&nbsp;"></a></td>
                                                    </tr>
                                                    <tr>
                                                    <td aria-hidden="true" height="8"
                                                        style="font-size:0px;line-height:0px;">&nbsp;</td>
                                                    </tr>
                                                    <tr>
                                                    <td align="center"
                                                        style="font-family:Tiempos,Times New Roman,serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;color:#1A1A1A;">
                                                        Nike Performance</td>
                                                    </tr>
                                                    <tr>
                                                    <td align="center"
                                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;text-decoration:none;color:#1A1A1A;">
                                                        Gloves</td>
                                                    </tr>
                                                    <tr>
                                                    <td aria-hidden="true" height="8"
                                                        style="font-size:0px;line-height:0px;">&nbsp;</td>
                                                    </tr>
                                                    <tr>
                                                    <td align="left"
                                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;color:#1A1A1A;">
                                                        <span
                                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;color:#1A1A1A;">{user_inputs[13]}18.99</span>
                                                    </td>
                                                    </tr>
                                                    <tr>
                                                    <td aria-hidden="true" height="12"
                                                        style="font-size:0px;line-height:0px;">&nbsp;</td>
                                                    </tr>
                                                </tbody>
                                                </table>
                                            </td>
                                            </tr>
                                        </tbody>
                                        </table>
                                        <!--[if (gte mso 9)|(IE)]></td><![endif]--><!--[if (gte mso 9)|(IE)]></tr></table><![endif]-->
                                    </td>
                                    </tr>
                                </tbody>
                                </table>
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tbody>
                                    <tr>
                                    <td aria-hidden="true" height="16" style="font-size:0px;line-height:0px;">&nbsp;</td>
                                    </tr>
                                </tbody>
                                </table>
                            </td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation">
                        <tbody>
                            <tr>
                            <td colspan="2" align="left"
                                style="font-family:Tiempos,Times New Roman,serif;font-size:16px;line-height:24px;letter-spacing:-0.16px;text-align:left;color:#1A1A1A;padding-left:24px;padding-right:24px;">
                                Best wishes,</td>
                            </tr>
                            <tr>
                            <td aria-hidden="true" align="left" width="12" style="padding-left:24px;padding-right:6px;">
                                <img
                                src="https://mosaic01.ztat.net/cuo/messages/810d1d00-4312-43e5-bd31-d8373fdd24c7/99062661-c7bc-4592-8260-c25ef7ff7d43/icon_heart_orange.png"
                                border="0" title="" alt="♥" width="12"
                                style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:24px;line-height:32px;letter-spacing:-0.24px;text-align:left;color:#FF4E00;display:block;vertical-align:middle;">
                            </td>
                            <td align="left"
                                style="font-family:Tiempos,Times New Roman,serif;font-size:16px;line-height:24px;letter-spacing:-0.16px;text-align:left;color:#1A1A1A;padding-right:24px;">
                                Your Zalando Team</td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" aria-hidden="true">
                        <tbody>
                            <tr>
                            <td height="24" style="font-size:0px;line-height:0px;">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <!--//* If anchor recommendations */-->
                        <table class="darkmode_grey" cellpadding="0" cellspacing="0" border="0" width="100%" align="left"
                        bgcolor="#1A1A1A" role="presentation" style="text-align:left !important;">
                        <tbody>
                            <tr>
                            <td height="24" style="font-size:0px;line-height:0px;">&nbsp;</td>
                            </tr>
                            <tr>
                            <td align="left" class="faq_td"
                                style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;color:#FFFFFE;padding-left:24px;">
                                <p class="mso-margin0"
                                style="font-family:Tiempos,Times New Roman,serif;font-size:24px;line-height:32px;letter-spacing:-0.24px;color:#FFFFFE;padding-bottom:24px;margin:0!important;">
                                Need help?</p>
                                <table align="center" cellpadding="0" cellspacing="0" border="0"
                                style="border-spacing: 0; Margin: 0 auto; width: 100%; max-width: 600px; text-align: center; font-size: 0; letter-spacing: 0">
                                <tbody>
                                    <tr>
                                    <td>
                                        <!--[if (gte mso 9)|(IE)]><table width="100%"  cellpadding="0" cellspacing="0" border="0"><tr valign="top"><![endif]--><!--[if (gte mso 9)|(IE)]><td valign="top" width="48%"><![endif]-->
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0"
                                        style="width: 100%; display: inline-block; vertical-align: top; max-width: 280px; font-size: 14px; letter-spacing: 0.6px; line-height:22px"
                                        class="mobile-full">
                                        <tbody>
                                            <tr valign="top">
                                            <td align="left" valign="top" class="mobile-full">
                                                <ul style="padding-left:0px; margin: 0;">
                                                <li class="mso-margin0" style="list-style:none; margin-bottom:10px">
                                                    <table cellpadding="0" cellspacing="0" border="0" width="100%"
                                                    style="font-size: inherit; letter-spacing: inherit;">
                                                    <tbody>
                                                        <tr>
                                                        <td width="1" valign="top" align="left"><img width="1" height="0"
                                                            src="https://mosaic01.ztat.net/cuo/messages/810d1d00-4312-43e5-bd31-d8373fdd24c7/99062661-c7bc-4592-8260-c25ef7ff7d43/article_24x24_2x.png"
                                                            alt=""></td>
                                                        <td><a
                                                            style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;color:#FFFFFE;text-decoration:underline;"
                                                            href="https://www.zalando.co.uk/faq/Returns-and-Refunds/How-do-I-return-my-order.html?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=faq_return&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"><span>How
                                                                to return your order </span></a></td>
                                                        </tr>
                                                    </tbody>
                                                    </table>
                                                </li>
                                                <li class="mso-margin0" style="list-style:none; margin-bottom:10px">
                                                    <table cellpadding="0" cellspacing="0" border="0" width="100%"
                                                    style="font-size: inherit; letter-spacing: inherit;">
                                                    <tbody>
                                                        <tr>
                                                        <td width="1" valign="top" align="left"><img width="1" height="0"
                                                            src="https://mosaic01.ztat.net/cuo/messages/810d1d00-4312-43e5-bd31-d8373fdd24c7/99062661-c7bc-4592-8260-c25ef7ff7d43/article_24x24_2x.png"
                                                            alt=""></td>
                                                        <td><a
                                                            style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;color:#FFFFFE;text-decoration:underline;"
                                                            href="https://www.zalando.co.uk/faq/Delivery/Where-is-my-order.html?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=faq_parcel_tracking&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"><span>How
                                                                to track an order </span></a></td>
                                                        </tr>
                                                    </tbody>
                                                    </table>
                                                </li>
                                                <li class="mso-margin0" style="list-style:none; margin-bottom:10px">
                                                    <table cellpadding="0" cellspacing="0" border="0" width="100%"
                                                    style="font-size: inherit; letter-spacing: inherit;">
                                                    <tbody>
                                                        <tr>
                                                        <td width="1" valign="top" align="left"><img width="1" height="0"
                                                            src="https://mosaic01.ztat.net/cuo/messages/810d1d00-4312-43e5-bd31-d8373fdd24c7/99062661-c7bc-4592-8260-c25ef7ff7d43/article_24x24_2x.png"
                                                            alt=""></td>
                                                        <td><a
                                                            style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;color:#FFFFFE;text-decoration:underline;"
                                                            href="https://www.zalando.co.uk/faq/Orders/Can-I-modify-my-order-after-it-has-been-placed.html?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=faq_order_modifying&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"><span>Modifying
                                                                your order after it has been placed </span></a></td>
                                                        </tr>
                                                    </tbody>
                                                    </table>
                                                </li>
                                                <li class="mso-margin0" style="list-style:none; margin-bottom:10px">
                                                    <table cellpadding="0" cellspacing="0" border="0" width="100%"
                                                    style="font-size: inherit; letter-spacing: inherit;">
                                                    <tbody>
                                                        <tr>
                                                        <td width="1" valign="top" align="left"><img width="1" height="0"
                                                            src="https://mosaic01.ztat.net/cuo/messages/810d1d00-4312-43e5-bd31-d8373fdd24c7/99062661-c7bc-4592-8260-c25ef7ff7d43/article_24x24_2x.png"
                                                            alt=""></td>
                                                        <td><a
                                                            style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;color:#FFFFFE;text-decoration:underline;"
                                                            href="https://www.zalando.co.uk/faq/Vouchers/Gift-cards-and-vouchers-general-info.html?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=faq_voucher&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"><span>Voucher
                                                                Information </span></a></td>
                                                        </tr>
                                                    </tbody>
                                                    </table>
                                                </li>
                                                </ul>
                                            </td>
                                            </tr>
                                        </tbody>
                                        </table>
                                        <!--[if (gte mso 9)|(IE)]></td><td valign="top" width="2%"><![endif]-->
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0"
                                        style="width: 100%; display: inline-block; vertical-align: top; max-width: 20px;"
                                        class="mobile-full">
                                        <tbody>
                                            <tr valign="top">
                                            <td align="left" valign="top" class="mobile-full"></td>
                                            </tr>
                                        </tbody>
                                        </table>
                                        <!--[if (gte mso 9)|(IE)]></td><![endif]--><!--[if (gte mso 9)|(IE)]><td valign="top" width="48%"><![endif]-->
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0"
                                        style="width: 100%; display: inline-block; vertical-align: top; max-width: 280px; font-size: 14px; letter-spacing: 0.6px; line-height:22px"
                                        class="mobile-full">
                                        <tbody>
                                            <tr valign="top">
                                            <td align="left" valign="top" class="mobile-full">
                                                <ul style="padding-left:0px; margin: 0;">
                                                <li class="mso-margin0" style="list-style:none; margin-bottom:10px">
                                                    <table cellpadding="0" cellspacing="0" border="0" width="100%"
                                                    style="font-size: inherit; letter-spacing: inherit;">
                                                    <tbody>
                                                        <tr>
                                                        <td width="1" valign="top" align="left"><img width="1" height="0"
                                                            src="https://mosaic01.ztat.net/cuo/messages/810d1d00-4312-43e5-bd31-d8373fdd24c7/99062661-c7bc-4592-8260-c25ef7ff7d43/help_24x24_2x.png"
                                                            alt=""></td>
                                                        <td><a
                                                            style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;text-align:left;color:#FFFFFE;text-decoration:underline;"
                                                            href="https://www.zalando.co.uk/faq/?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=faq&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"><span>Help
                                                                &amp; Contact </span></a></td>
                                                        </tr>
                                                    </tbody>
                                                    </table>
                                                </li>
                                                </ul>
                                            </td>
                                            </tr>
                                        </tbody>
                                        </table>
                                        <!--[if (gte mso 9)|(IE)]></td><td valign="top" width="2%"><![endif]-->
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0"
                                        style="width: 100%; display: inline-block; vertical-align: top; max-width: 20px;"
                                        class="mobile-full">
                                        <tbody>
                                            <tr valign="top">
                                            <td align="left" valign="top" class="mobile-full"></td>
                                            </tr>
                                        </tbody>
                                        </table>
                                        <!--[if (gte mso 9)|(IE)]></td><![endif]--><!--[if (gte mso 9)|(IE)]></tr></table><![endif]-->
                                    </td>
                                    </tr>
                                </tbody>
                                </table>
                                <table border="0" cellpadding="0" cellspacing="0" width="100%" aria-hidden="true">
                                <tbody>
                                    <tr>
                                    <td height="16" style="font-size:0px;line-height:0px;">&nbsp;</td>
                                    </tr>
                                </tbody>
                                </table>
                            </td>
                            </tr>
                        </tbody>
                        </table>
                        <table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"
                        bgcolor="#6328E0">
                        <tbody>
                            <tr>
                            <td style="padding-left:24px;padding-right:24px;">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%" aria-hidden="true">
                                <tbody>
                                    <tr>
                                    <td height="24" style="font-size:0px;line-height:0px;">&nbsp;</td>
                                    </tr>
                                </tbody>
                                </table>
                                <table role="presentation" border="0" cellpadding="0" cellspacing="0" align="left">
                                <tbody>
                                    <tr>
                                    <td align="left"
                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;font-weight:bold;color:#FFFFFE!important;">
                                        Find inspiration</td>
                                    </tr>
                                    <tr>
                                    <td aria-hidden="true" height="8" style="font-size:0px;line-height:0px;">&nbsp;</td>
                                    </tr>
                                    <tr>
                                    <td align="left">
                                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" align="left">
                                        <tbody>
                                            <tr>
                                            <td align="left" style="padding-right:6px;"><a
                                                href="https://www.instagram.com/zalando/" target="_blank"><img
                                                    src="https://mosaic01.ztat.net/cuo/messages/810d1d00-4312-43e5-bd31-d8373fdd24c7/99062661-c7bc-4592-8260-c25ef7ff7d43/icon_instagram.png"
                                                    style="display:block;" width="35" border="0" alt=""></a></td>
                                            <td align="left" style="padding-right:6px;"><a
                                                href="https://www.facebook.com/zalando" target="_blank"><img
                                                    src="https://mosaic01.ztat.net/cuo/messages/810d1d00-4312-43e5-bd31-d8373fdd24c7/99062661-c7bc-4592-8260-c25ef7ff7d43/icon_facebook.png"
                                                    style="display:block;" width="35" border="0" alt=""></a></td>
                                            <td align="left" style="padding-right:6px;"><a
                                                href="https://www.tiktok.com/@zalando" target="_blank"><img
                                                    src="https://mosaic01.ztat.net/cuo/messages/810d1d00-4312-43e5-bd31-d8373fdd24c7/99062661-c7bc-4592-8260-c25ef7ff7d43/icon_tiktok.png"
                                                    style="display:block;" width="35" border="0" alt=""></a></td>
                                            </tr>
                                        </tbody>
                                        </table>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>
                                <table role="presentation" border="0" cellpadding="0" cellspacing="0" align="right">
                                <tbody>
                                    <tr>
                                    <td align="right"
                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:14px;line-height:20px;letter-spacing:0px;font-weight:bold;color:#FFFFFE!important;">
                                        Shop Easily</td>
                                    </tr>
                                    <tr>
                                    <td aria-hidden="true" height="8" style="font-size:0px;line-height:0px;">&nbsp;</td>
                                    </tr>
                                    <tr>
                                    <td>
                                        <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                                        <tbody>
                                            <tr>
                                            <td align="right" style="padding-left:6px;text-align:right;"><a
                                                href="https://play.google.com/store/apps/details?id=de.zalando.mobile"
                                                target="_blank"><img
                                                    src="https://mosaic01.ztat.net/cuo/messages/810d1d00-4312-43e5-bd31-d8373fdd24c7/13c11237-166f-4413-8a00-0616712add40/logo_android.png"
                                                    style="display:block;" width="35" border="0" alt=""></a></td>
                                            <td align="right" style="padding-left:6px;text-align:right;"><a
                                                href="https://apps.apple.com/de/app/zalando-fashion-and-shopping/id585629514"
                                                target="_blank"><img
                                                    src="https://mosaic01.ztat.net/cuo/messages/810d1d00-4312-43e5-bd31-d8373fdd24c7/13c11237-166f-4413-8a00-0616712add40/logo_apple.png"
                                                    style="display:block;" width="35" border="0" alt=""></a></td>
                                            </tr>
                                        </tbody>
                                        </table>
                                    </td>
                                    </tr>
                                </tbody>
                                </table>
                                <table border="0" cellpadding="0" cellspacing="0" width="100%" aria-hidden="true">
                                <tbody>
                                    <tr>
                                    <td aria-hidden="true" height="24" style="font-size:0px;line-height:0px;">&nbsp;</td>
                                    </tr>
                                </tbody>
                                </table>
                                <table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0">
                                <tbody>
                                    <tr>
                                    <td align="left"
                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:12px;line-height:16px;letter-spacing:0px;text-decoration:none;color:#FFFFFE!important;">
                                        <b>Legal notice</b><br><a
                                        href="https://www.zalando.co.uk?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=footer_home&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"
                                        target="_blank"
                                        style="color:#FFFFFE !important;text-decoration:underline;">Zalando.co.uk</a> is
                                        brought to you by Zalando SE
                                        <br>
                                        Zalando SE, Valeska-Gert-Straße 5, 10243 Berlin, Germany | Management Board:
                                        Robert Gentz &amp; David Schneider (both co-Chairs of the Board), David Schröder,
                                        Dr. Astrid Arndt, Dr. Sandra Dembeck | Chairperson of the Supervisory Board:
                                        Kelly Bennett | Registered at Amtsgericht Charlottenburg Berlin, HRB 158855 B | VAT
                                        ID: DE 260543043 | Tax number: 37/132/45004 | <a
                                        href="https://www.zalando.co.uk/legal-notice/?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=footer_more_details&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"
                                        target="_blank" style="color:#FFFFFE !important;text-decoration:underline;">See
                                        more details</a>
                                    </td>
                                    </tr>
                                    <tr>
                                    <td aria-hidden="true" height="24" style="font-size:0px;line-height:0px;">&nbsp;</td>
                                    </tr>
                                    <tr>
                                    <td align="left"
                                        style="font-family:HelveticaNow,Helvetica,sans-serif;font-size:12px;line-height:16px;letter-spacing:0px;text-decoration:none;color:#FFFFFE!important;">
                                        All prices include VAT. Only while stock lasts. All prices subject to change.
                                        "Originally" refers to the item's first listing price or recommended retail price.
                                        Zalando SE has assigned its claims under the above referenced purchase to Zalando
                                        Payments GmbH.
                                        <br><br>
                                        Responsible for contents of Zalando SE: Robert Gentz


                                        <br><br>
                                        This is an automatic email, please do not reply. Find out how to get in touch by
                                        visiting our <a
                                        href="https://www.zalando.co.uk/faq/Contact/77166764/Contact-and-Help-Information.htm?wmc=CRM44_TMS_EN.ONL_MIX_NMT_TM009_009_231108.&amp;cd084=faq_contact&amp;cd085=61e4329f-e929-4e84-9bff-8c5eb3040e1e&amp;wt_cd=004ac56ca2f3ffb4cc8e33b01a96d505&amp;tm_hem=ab9f0fabc8c0530cbf39f1313321d4e4"
                                        target="_blank" style="color:#FFFFFE !important;text-decoration:underline;">help
                                        and contact</a> pages.

                                    </td>
                                    </tr>
                                </tbody>
                                </table>
                                <table border="0" cellpadding="0" cellspacing="0" width="100%" aria-hidden="true">
                                <tbody>
                                    <tr>
                                    <td aria-hidden="true" height="24" style="font-size:0px;line-height:0px;">&nbsp;</td>
                                    </tr>
                                </tbody>
                                </table>
                            </td>
                            </tr>
                        </tbody>
                        </table>
                        <a name="footer"></a>
                    </td>
                    </tr>
                    <!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]-->
                </tbody>
                </table>
            </td>
            </tr>
            <!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]-->
        </tbody>
        </table>
        <table class="hide darkmode" border="0" cellpadding="0" cellspacing="0" width="100%" align="center"
        bgcolor="#f2f2f2" aria-hidden="true">
        <tbody>
            <tr>
            <td height="40" style="font-size:0px;line-height:0px;">&nbsp;</td>
            </tr>
        </tbody>
        </table>
    </div>
    </div>

    </body>

    </html>
    """

    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
