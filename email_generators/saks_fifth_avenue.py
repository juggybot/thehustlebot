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
    msg['From'] = formataddr((f'Saks Fifth Avenue', sender_email))
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
    "Please enter the customer full name (Juggy Resells):",
    "Please enter the image url (.jpg, .jpeg, .png):",
    "Please enter the product name (Embroidered Trumpet Midi-Dress):",
    "Please enter the item size (S/M/L):",
    "Please enter the color (Black):",
    "Please enter the product cost (WITHOUT THE $):",
    "Please enter the delivery cost (WITHOUT THE $):",
    "Please enter the tax cost (WITHOUT THE $):",
    "Please enter the total cost (WITHOUT THE $):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o primeiro nome do cliente (Juggy):",
    "Por favor, insira o nome completo do cliente (Juggy Resells):",
    "Por favor, insira a URL da imagem (.jpg, .jpeg, .png):",
    "Por favor, insira o nome do produto (Vestido Midi com Bordado e Babado):",
    "Por favor, insira o tamanho do item (P/M/G):",
    "Por favor, insira a cor (Preto):",
    "Por favor, insira o custo do produto (SEM O SÍMBOLO $):",
    "Por favor, insira o custo de entrega (SEM O SÍMBOLO $):",
    "Por favor, insira o valor do imposto (SEM O SÍMBOLO $):",
    "Por favor, insira o custo total (SEM O SÍMBOLO $):",
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
    part1 = "#"
    part2 = random.randint(100000000, 999999999)  # Random 9-digit number

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
    recipient_email = f'{user_inputs[11]}'
    subject = f"Thank you for your order {order_num}"

    html_template = f"""
            <div class=""><div class="aHl"></div><div id=":qg" tabindex="-1"></div><div id=":q6" class="ii gt" jslog="20277; u014N:xr6bB; 1:WyIjdGhyZWFkLWY6MTgwMjU2OTYzMDA5NDI5MTQ3MSJd; 4:WyIjbXNnLWY6MTgwMjU2OTYzMDA5NDI5MTQ3MSJd"><div id=":q5" class="a3s aiL "><div><div class="adM">
    </div><div style="margin:0px;padding:0px;min-width:100%;background-color:#ffffff"><div class="adM">
    </div><center style="width:100%;table-layout:fixed">
        <div style="display:none;font-size:1px;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden">Hi Amanda, we're writing to let you know that we're getting your order 
        <a href="https://www.saksfifthavenue.com" style="text-decoration:none;color:#000000" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.saksfifthavenue.com&amp;source=gmail&amp;ust=1719150762362000&amp;usg=AOvVaw33SxYJakhHATGkJLbNuw7K">
            <strong>{order_num}</strong>
        </a> ready and will send you an email as soon as it ships. In the meantime, you can find all the details below. 
        <br>
        </div>
        <div style="max-width:640px">
        <input id="m_5750059814468834653mobile-checkbox" style="display:none!important;max-height:0" type="checkbox">
        <table style="border-spacing:0px;font-family:helvetica,arial,sans-serif;margin:0px auto;width:100%;max-width:640px" align="center">
            <tbody style="font-family:helvetica,arial,sans-serif">
            <tr style="font-family:helvetica,arial,sans-serif">
                <td style="padding:0px 0px 10px;font-family:helvetica,arial,sans-serif;background-color:#ffffff">
                <table style="border-spacing:0px;font-family:helvetica,arial,sans-serif" border="0" width="100%" cellspacing="0" cellpadding="0" align="center">
                    <tbody style="font-family:helvetica,arial,sans-serif">
                    <tr style="font-family:helvetica,arial,sans-serif">
                        <td style="padding:0px 10px;font-family:helvetica,arial,sans-serif">
                        <table style="border-spacing:0px;font-family:helvetica,arial,sans-serif" border="0" width="100%" cellspacing="0" cellpadding="0" align="center">
                            <tbody style="font-family:helvetica,arial,sans-serif">
                            <tr style="font-family:helvetica,arial,sans-serif">
                                <td style="padding:15px 10px 20px;width:100%;text-align:left;font-family:helvetica,arial,sans-serif">
                                <table style="border-spacing:0px;width:100%;font-family:helvetica,arial,sans-serif">
                                    <tbody style="font-family:helvetica,arial,sans-serif">
                                    <tr style="font-family:helvetica,arial,sans-serif">
                                        <td style="font-family:helvetica,arial,sans-serif">
                                        <table style="width:100%;height:61px;font-family:helvetica,arial,sans-serif" border="0" cellspacing="0" cellpadding="0" align="center">
                                            <tbody style="font-family:helvetica,arial,sans-serif">
                                            <tr style="font-family:helvetica,arial,sans-serif">
                                                <td style="width:100%;height:60px;font-family:Helvetica,arial,sans-serif;font-size:15px;vertical-align:bottom;color:#333333" align="center">
                                                <h1 style="line-height:0;font-size:0px;padding:0px;margin:0px;font-family:Helvetica,arial,sans-serif">Saks Fifth Avenue 
                                                    <a href="https://www.saksfifthavenue.com?site_refer=EML3348TRIGTRAN" style="line-height:0;font-size:0px;padding:0px;margin:0px;font-family:Helvetica,arial,sans-serif" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.saksfifthavenue.com?site_refer%3DEML3348TRIGTRAN&amp;source=gmail&amp;ust=1719150762362000&amp;usg=AOvVaw2eQ4exjsyC-ife_vfkpnVq">Saks Fifth Avenue 
                                                    <img style="border-width:0px;font-family:Helvetica,arial,sans-serif" src="https://ci3.googleusercontent.com/meips/ADKq_Nbpzxl1hXvhqV9u3LeYuaNb4eI7zBoZEL2DotG_NocoztBwlnmPoz84pLMChaNZ9noEuBrflVJ6I9BxXesbT2mWyc5nk7wNJjoQfBHDi8bq8wReEgorJQ=s0-d-e1-ft#https://s3.us-east-2.amazonaws.com/hbc-email-images/saks-logo.png" alt="Saks Fifth Avenue" height="33" border="0" class="CToWUd" data-bit="iit">
                                                    </a>
                                                </h1>
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
            <tr style="font-family:helvetica,arial,sans-serif">
                <td style="padding:0px 10px 10px;font-family:helvetica,arial,sans-serif;background-color:#ffffff">
                <table style="width:100%;border-spacing:0px;font-family:helvetica,arial,sans-serif;font-size:14px;text-align:center" border="0" cellspacing="0" cellpadding="0">
                    <tbody style="font-family:helvetica,arial,sans-serif">
                    <tr style="font-family:helvetica,arial,sans-serif">
                        <td style="padding:0px 10px 15px;font-family:helvetica,arial,sans-serif">
                        <table style="width:100%;border-spacing:0px;font-family:helvetica,arial,sans-serif;font-size:14px;text-align:center" border="0" cellspacing="0" cellpadding="0">
                            <tbody style="font-family:helvetica,arial,sans-serif">
                            <tr style="font-family:helvetica,arial,sans-serif">
                                <td style="padding:0px;line-height:25px;font-size:25px;font-family:helvetica,arial,sans-serif;background-color:#ffffff">&nbsp;</td>
                            </tr>
                            <tr style="font-family:helvetica,arial,sans-serif">
                                <td style="padding:0px;font-family:helvetica,arial,sans-serif" align="center">
                                <h2 style="padding:0px;margin:0px;font-family:Helvetica;font-size:22px;font-weight:300;color:#000000">Your Order Is Confirmed</h2>
                                </td>
                            </tr>
                            <tr style="font-family:helvetica,arial,sans-serif">
                                <td style="padding:0px;line-height:20px;font-size:20px;font-family:helvetica,arial,sans-serif;background-color:#ffffff">&nbsp;</td>
                            </tr>
                            <tr style="font-family:helvetica,arial,sans-serif">
                                <td style="font-family:helvetica,arial,sans-serif" align="center">
                                <table style="border-spacing:0px;text-align:center;font-family:helvetica,arial,sans-serif" border="0" cellspacing="0" cellpadding="0">
                                    <tbody style="font-family:helvetica,arial,sans-serif">
                                    <tr style="font-family:helvetica,arial,sans-serif">
                                        <td style="padding:0px 20px;font-family:helvetica;width:450px;font-size:15px;font-weight:300;line-height:1.47;color:#000000" align="center">Hi {user_inputs[0]}, we're writing to let you know that we're getting your order 
                                        <a href="https://www.saksfifthavenue.com/account/order-status?billing_zip_code=95621-4213&amp;order_num=307437329&amp;site_refer=EML3348TRIGTRAN" style="text-decoration:none;font-family:helvetica;color:#000000" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.saksfifthavenue.com/account/order-status?billing_zip_code%3D95621-4213%26order_num%3D307437329%26site_refer%3DEML3348TRIGTRAN&amp;source=gmail&amp;ust=1719150762362000&amp;usg=AOvVaw25kBhVXkepPWRt7mqa7u87">
                                            <strong style="font-family:helvetica">{order_num}</strong>
                                        </a> ready and will send you an email as soon as it ships. In the meantime, you can find all the details below. 
                                        <br>
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
            <tr style="font-family:helvetica,arial,sans-serif">
                <td style="padding:20px 10px 0px;text-align:center;font-family:helvetica,arial,sans-serif;background-color:#ffffff" align="center">
                <table style="border-spacing:0px;padding-top:0px;padding-right:60px;margin-bottom:40px;padding-left:60px;text-align:left;table-layout:fixed;font-family:helvetica,arial,sans-serif" border="0" width="100%" cellspacing="0" cellpadding="0" align="center">
                    <tbody style="font-family:helvetica,arial,sans-serif">
                    <tr style="font-family:helvetica,arial,sans-serif">
                        <td style="padding:0px;font-family:helvetica,arial,sans-serif" align="center">
                        <a href="https://www.saksfifthavenue.com/" style="text-decoration:none;font-weight:bold;font-family:helvetica,arial,sans-serif;font-size:12px;border:2px solid black;padding:7px 20px;background-color:white;color:black" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.saksfifthavenue.com/&amp;source=gmail&amp;ust=1719150762362000&amp;usg=AOvVaw2ISkTIhysCtr9v2Tg9-8zv">VIEW OR MANAGE ORDER</a>
                        </td>
                    </tr>
                    </tbody>
                </table>
                </td>
            </tr>
            <tr style="font-family:helvetica,arial,sans-serif">
                <td style="font-family:helvetica,arial,sans-serif">
                <div style="border-top-width:1px;border-top-style:solid;margin:0px auto;padding:0px;width:100%;max-width:640px;font-family:helvetica,arial,sans-serif;border-top-color:#cccccc">&nbsp;</div>
                </td>
            </tr>
            <tr style="font-family:helvetica,arial,sans-serif">
                <td id="m_5750059814468834653shipping_information" style="text-align:center;font-size:0px;padding-top:10px;padding-bottom:20px;font-family:helvetica,arial,sans-serif">
                <table style="width:100%;vertical-align:top;border-spacing:0px;font-family:helvetica,arial,sans-serif" border="0" cellspacing="0" cellpadding="0">
                    <tbody style="font-family:helvetica,arial,sans-serif">
                    <tr style="font-family:helvetica,arial,sans-serif">
                        <td style="padding:0px 10px 10px;font-family:helvetica,arial,sans-serif">
                        <table style="width:100%;border-spacing:0px;font-family:helvetica,arial,sans-serif;font-size:14px;font-weight:300" border="0" cellspacing="0" cellpadding="0">
                            <tbody style="font-family:helvetica,arial,sans-serif">
                            <tr style="font-family:helvetica,arial,sans-serif">
                                <td style="padding:0px;text-align:center;width:100%;font-family:helvetica,arial,sans-serif" align="center">
                                <table style="border-spacing:0px;font-family:helvetica,arial,sans-serif" border="0" cellspacing="0" cellpadding="0" align="center">
                                    <tbody style="font-family:helvetica,arial,sans-serif">
                                    <tr style="font-family:helvetica,arial,sans-serif">
                                        <td style="text-align:center;font-family:helvetica,sans-serif;font-size:15px;line-height:22px;padding:0px;color:#000000">{user_inputs[1]}</td>
                                    </tr>
                                    <tr style="font-family:helvetica,arial,sans-serif">
                                        <td style="font-family:helvetica,sans-serif;font-size:15px;line-height:22px;padding:0px;color:#000000">
                                        <a href="#" style="font-family:helvetica,sans-serif" target="_blank" data-saferedirecturl="https://www.google.com/url?q=#"
                                        </td>
                                    </tr>
                                    <tr style="font-family:helvetica,arial,sans-serif">
                                        <td style="font-family:helvetica,sans-serif;font-size:15px;line-height:22px;padding:0px;color:#000000">
                                        <a href="#" style="font-family:helvetica,sans-serif" target="_blank" data-saferedirecturl="https://www.google.com/url?q=#"
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
            <tr style="font-family:helvetica,arial,sans-serif">
                <td style="padding:0px;font-family:helvetica,arial,sans-serif" align="center">
                <div style="display:inline-block;vertical-align:top;padding-left:15px;padding-right:15px;font-family:helvetica,arial,sans-serif">
                    <table style="padding:0px;font-family:sans-serif" border="0" width="100%" cellspacing="0" cellpadding="0">
                    <tbody style="font-family:sans-serif">
                        <tr style="font-family:sans-serif">
                        <td style="padding-top:0px;padding-bottom:10px;font-family:sans-serif">
                            <table style="padding:0px;margin:0px;font-family:sans-serif" border="0" width="100%" cellspacing="0" cellpadding="0">
                            <tbody style="font-family:sans-serif">
                                <tr style="font-family:sans-serif">
                                <td style="padding:0px 0px 20px;text-align:center;font-size:0px;font-family:sans-serif">
                                    <div style="width:100%;display:inline-block;vertical-align:top;font-family:sans-serif">
                                    <table style="border-spacing:0px;font-family:sans-serif;color:#333333" border="0" width="100%" cellspacing="0" cellpadding="0" align="center">
                                        <tbody style="font-family:sans-serif">
                                        <tr style="font-family:sans-serif">
                                            <td style="font-family:sans-serif">
                                            <table style="border-spacing:0px;font-family:sans-serif;width:100%;font-size:14px;color:#333333" border="0" cellspacing="0" cellpadding="0" align="center">
                                                <tbody style="font-family:sans-serif">
                                                <tr style="font-family:sans-serif">
                                                    <td style="padding:0px;width:160px;height:209px;font-family:sans-serif" align="center">
                                                    <a style="font-family:sans-serif" rel="noopener">
                                                        <img style="border-width:0px;display:block;max-width:160px;max-height:209px;font-family:sans-serif" src="{user_inputs[2]}" alt="2-Pack Trunk Boxer Briefs" class="CToWUd a6T" data-bit="iit" tabindex="0"><div class="a6S" dir="ltr" style="opacity: 0.01; left: 376.188px; top: 658.141px;"><span data-is-tooltip-wrapper="true" class="a5q" jsaction="JIbuQc:.CLIENT"><button class="VYBDae-JX-I VYBDae-JX-I-ql-ay5-ays CgzRE" jscontroller="PIVayb" jsaction="click:h5M12e; clickmod:h5M12e;pointerdown:FEiYhc;pointerup:mF5Elf;pointerenter:EX0mI;pointerleave:vpvbp;pointercancel:xyn4sd;contextmenu:xexox;focus:h06R8; blur:zjh6rb;mlnRJb:fLiPzd;" data-idom-class="CgzRE" jsname="hRZeKc" aria-label="Download attachment " data-tooltip-enabled="true" data-tooltip-id="tt-c31" data-tooltip-classes="AZPksf" id="" jslog="91252; u014N:cOuCgd,Kr2w4b,xr6bB; 4:WyIjbXNnLWY6MTgwMjU2OTYzMDA5NDI5MTQ3MSJd; 43:WyJpbWFnZS9qcGVnIl0."><span class="OiePBf-zPjgPe VYBDae-JX-UHGRz"></span><span class="bHC-Q" data-unbounded="false" jscontroller="LBaJxb" jsname="m9ZlFb" soy-skip="" ssk="6:RWVI5c"></span><span class="VYBDae-JX-ank-Rtc0Jf" jsname="S5tZuc" aria-hidden="true"><span class="bzc-ank" aria-hidden="true"><svg viewBox="0 -960 960 960" height="20" width="20" focusable="false" class=" aoH"><path d="M480-336L288-528l51-51L444-474V-816h72v342L621-579l51,51L480-336ZM263.72-192Q234-192 213-213.15T192-264v-72h72v72H696v-72h72v72q0,29.7-21.16,50.85T695.96-192H263.72Z"></path></svg></span></span><div class="VYBDae-JX-ano"></div></button><div class="ne2Ple-oshW8e-J9" id="tt-c31" role="tooltip" aria-hidden="true">Download</div></span></div>
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
                                    <div style="width:100%;vertical-align:top;padding:0px;font-family:sans-serif">
                                    <table style="border-spacing:0px;padding:0px;font-family:sans-serif" border="0" width="100%" cellspacing="0" cellpadding="0" align="left">
                                        <tbody style="font-family:sans-serif">
                                        <tr style="font-family:sans-serif">
                                            <td style="padding:20px 0px 10px;border-spacing:0px;font-family:sans-serif" align="center">
                                            <table style="border-spacing:0px;padding:0px;font-family:sans-serif" border="0" cellspacing="0" cellpadding="0">
                                                <tbody style="font-family:sans-serif">
                                                <tr style="font-family:sans-serif">
                                                    <td style="max-width:160px;padding:0px;font-family:helvetica,arial,sans-serif;font-size:15px;line-height:22px;font-weight:bold;color:#000000" align="center">
                                                    <a style="text-decoration:none;font-family:helvetica,arial,sans-serif;color:#000000" rel="noopener"></a>
                                                    </td>
                                                </tr>
                                                <tr style="font-family:sans-serif">
                                                    <td style="height:4px;padding:0px;font-family:sans-serif">&nbsp;</td>
                                                </tr>
                                                <tr style="font-family:sans-serif">
                                                    <td style="max-width:160px;padding:0px;font-family:helvetica,arial,sans-serif;font-size:15px;line-height:22px;font-weight:300;color:#000000" align="center">
                                                    <a href="https://www.SaksFifthAvenue.com/en/11878422.html?site_refer=EML3348TRIGTRAN" style="text-decoration:none;font-family:helvetica,arial,sans-serif;color:#000000" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.SaksFifthAvenue.com/en/11878422.html?site_refer%3DEML3348TRIGTRAN&amp;source=gmail&amp;ust=1719150762362000&amp;usg=AOvVaw14PvzmN90kR1Wvix_y9DOf">{user_inputs[3]}</a>
                                                    </td>
                                                </tr>
                                                <tr style="font-family:sans-serif">
                                                    <td style="max-width:160px;padding:0px;font-family:sans-serif" align="center">
                                                    <table style="border-spacing:0px;font-family:sans-serif" border="0" cellspacing="0" cellpadding="0">
                                                        <tbody style="font-family:sans-serif">
                                                        <tr style="font-family:sans-serif">
                                                            <td style="font-family:helvetica,arial,sans-serif;font-size:15px;line-height:22px;font-weight:300;padding:0px;color:#000000">{user_inputs[4]}</td>
                                                        </tr>
                                                        </tbody>
                                                    </table>
                                                    </td>
                                                </tr>
                                                <tr style="font-family:sans-serif">
                                                    <td style="max-width:160px;padding:0px;font-family:sans-serif" align="center">
                                                    <table style="border-spacing:0px;font-family:sans-serif" border="0" cellspacing="0" cellpadding="0">
                                                        <tbody style="font-family:sans-serif">
                                                        <tr style="font-family:sans-serif">
                                                            <td style="font-family:helvetica,arial,sans-serif;font-size:15px;line-height:22px;font-weight:300;padding:0px;color:#000000">{user_inputs[5]}</td>
                                                        </tr>
                                                        </tbody>
                                                    </table>
                                                    </td>
                                                </tr>
                                                <tr style="font-family:sans-serif">
                                                    <td style="max-width:160px;padding:0px;font-family:sans-serif">
                                                    <table style="border-spacing:0px;width:100%;font-family:sans-serif" border="0" cellspacing="0" cellpadding="0">
                                                        <tbody style="font-family:sans-serif">
                                                        <tr style="font-family:sans-serif">
                                                            <td style="font-family:helvetica,arial,sans-serif;font-size:15px;font-weight:300;line-height:22px;padding:0px;color:#000000" align="center">{user_inputs[6]}</td>
                                                        </tr>
                                                        </tbody>
                                                    </table>
                                                    </td>
                                                </tr>
                                                <tr style="font-family:sans-serif">
                                                    <td style="max-width:160px;padding:0px;font-family:sans-serif">
                                                    <table style="border-spacing:0px;font-family:sans-serif" border="0" cellspacing="0" cellpadding="0">
                                                        <tbody style="font-family:sans-serif">
                                                        <tr style="font-family:sans-serif">
                                                            <td style="height:8px;padding:0px;font-family:sans-serif">&nbsp;</td>
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
                        </td>
                        </tr>
                    </tbody>
                    </table>
                </div>
                </td>
            </tr>
            <tr style="font-family:helvetica,arial,sans-serif">
                <td style="font-family:helvetica,arial,sans-serif">
                <div style="border-top-width:1px;border-top-style:solid;margin:0px auto;padding:0px;width:100%;max-width:640px;font-family:helvetica,arial,sans-serif;border-top-color:#cccccc">&nbsp;</div>
                </td>
            </tr>
            <tr style="font-family:helvetica,arial,sans-serif">
                <td style="text-align:center;font-size:15px;line-height:22px;font-weight:bold;padding:32px 10px 0px;font-family:helvetica,arial,sans-serif">Order Number</td>
            </tr>
            <tr style="font-family:helvetica,arial,sans-serif">
                <td style="text-align:center;font-size:15px;line-height:22px;font-weight:300;padding:0px 10px 10px;font-family:helvetica,arial,sans-serif">{order_num}</td>
            </tr>
            <tr style="font-family:helvetica,arial,sans-serif">
                <td style="text-align:center;font-size:15px;line-height:22px;font-weight:bold;padding:10px 10px 0px;font-family:helvetica,arial,sans-serif">Placed On</td>
            </tr>
            <tr style="font-family:helvetica,arial,sans-serif">
                <td style="text-align:center;font-size:15px;line-height:22px;font-weight:300;padding:0px 10px 10px;font-family:helvetica,arial,sans-serif"></td>
            </tr>
            <tr style="font-family:helvetica,arial,sans-serif">
                <td style="text-align:center;font-size:0px;padding:20px 15px 15px;font-family:helvetica,arial,sans-serif">
                <table style="width:300px;display:inline-block;vertical-align:top;border-spacing:0px;font-family:helvetica,arial,sans-serif;background-color:#f8f8f8" border="0" cellspacing="0" cellpadding="0" align="center">
                    <tbody style="display:block;font-family:helvetica,arial,sans-serif">
                    <tr style="display:block;font-family:helvetica,arial,sans-serif">
                        <td style="display:block;padding:20px 34px 34px;font-family:helvetica,arial,sans-serif">
                        <table style="width:100%;border-spacing:0px;text-align:center;font-family:helvetica,arial,sans-serif" border="0" cellspacing="0" cellpadding="0">
                            <tbody style="font-family:helvetica,arial,sans-serif">
                            <tr style="font-family:helvetica,arial,sans-serif">
                                <th style="font-family:helvetica,arial,sans-serif;font-size:15px;line-height:22px;font-weight:bold;padding-bottom:10px;color:#000000" align="center">Order Summary</th>
                            </tr>
                            <tr style="font-family:helvetica,arial,sans-serif">
                                <td style="padding:0px;font-family:helvetica,arial,sans-serif">
                                <table style="border-spacing:0px;font-family:helvetica,arial,sans-serif" border="0" width="100%" cellspacing="0" cellpadding="0">
                                    <tbody style="font-family:helvetica,arial,sans-serif">
                                    <tr style="font-family:helvetica,arial,sans-serif">
                                        <td style="font-family:helvetica,sans-serif;font-size:15px;line-height:24px;font-weight:300;padding:0px;color:#000000" align="left">Subtotal</td>
                                        <td style="font-family:helvetica,sans-serif;font-size:15px;line-height:24px;font-weight:300;padding:0px;color:#000000" align="right">{user_inputs[6]}</td>
                                    </tr>
                                    </tbody>
                                </table>
                                </td>
                            </tr>
                            <tr style="font-family:helvetica,arial,sans-serif">
                                <td style="padding:0px;font-family:helvetica,arial,sans-serif">
                                <table style="border-spacing:0px;font-family:helvetica,arial,sans-serif" border="0" width="100%" cellspacing="0" cellpadding="0">
                                    <tbody style="font-family:helvetica,arial,sans-serif">
                                    <tr style="font-family:helvetica,arial,sans-serif">
                                        <td style="font-family:helvetica,sans-serif;font-size:15px;line-height:24px;font-weight:300;padding:0px;color:#000000" align="left">Shipping</td>
                                        <td style="font-family:helvetica,sans-serif;font-size:15px;line-height:24px;font-weight:300;padding:0px;color:#000000" align="right">{user_inputs[7]}</td>
                                    </tr>
                                    </tbody>
                                </table>
                                </td>
                            </tr>
                            
                            <tr style="font-family:helvetica,arial,sans-serif">
                                <td style="padding:0px;font-family:helvetica,arial,sans-serif">
                                <table style="border-spacing:0px;font-family:helvetica,arial,sans-serif" border="0" width="100%" cellspacing="0" cellpadding="0">
                                    <tbody style="font-family:helvetica,arial,sans-serif">
                                    <tr style="font-family:helvetica,arial,sans-serif">
                                        <td style="font-family:helvetica,sans-serif;font-size:15px;line-height:24px;font-weight:300;padding:0px;color:#000000" align="left">Tax</td>
                                        <td style="font-family:helvetica,sans-serif;font-size:15px;line-height:24px;font-weight:300;padding:0px;color:#000000" align="right">{user_inputs[8]}</td>
                                    </tr>
                                    </tbody>
                                </table>
                                </td>
                            </tr>
                            <tr style="font-family:helvetica,arial,sans-serif">
                                <td style="padding:0px;font-family:helvetica,arial,sans-serif">
                                <table style="border-spacing:0px;font-family:helvetica,arial,sans-serif" border="0" width="100%" cellspacing="0" cellpadding="0">
                                    <tbody style="font-family:helvetica,arial,sans-serif">
                                    <tr style="font-family:helvetica,arial,sans-serif">
                                        <td style="font-family:helvetica,sans-serif;font-size:15px;line-height:24px;font-weight:bold;padding:0px;text-transform:uppercase;color:#000000" align="left">Total</td>
                                        <td style="font-family:helvetica,sans-serif;font-size:15px;line-height:24px;font-weight:bold;padding:0px;color:#000000" align="right">{user_inputs[9]}</td>
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
            <tr style="font-family:helvetica,arial,sans-serif">
                <td style="padding:20px 10px 0px;text-align:center;font-family:helvetica,arial,sans-serif;background-color:#ffffff" align="center">
                <table style="border-spacing:0px;padding:0px 60px;text-align:left;table-layout:fixed;font-family:helvetica,arial,sans-serif" border="0" width="100%" cellspacing="0" cellpadding="0" align="center">
                    <tbody style="font-family:helvetica,arial,sans-serif">
                    <tr style="font-family:helvetica,arial,sans-serif">
                        <td style="padding:0px;font-family:helvetica,arial,sans-serif;font-size:12px;line-height:18px;color:#777777" align="center">We'll ship your items as soon as they're available. You may receive them in multiple 
                        <br>packages at no extra shipping cost.
                        </td>
                    </tr>
                    <tr style="font-family:helvetica,arial,sans-serif">
                        <td style="height:20px;font-size:20px;line-height:20px;font-family:helvetica,arial,sans-serif;background-color:#ffffff;color:#ffffff">&nbsp;</td>
                    </tr>
                    <tr style="font-family:helvetica,arial,sans-serif">
                        <td style="padding:0px 0px 27px;font-family:helvetica,arial,sans-serif;font-size:12px;line-height:18px;color:#777777" align="center">If you have any questions regarding your order, please 
                        <a href="https://support.saksfifthavenue.com/s/contactsupport" style="font-family:helvetica,arial,sans-serif" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://support.saksfifthavenue.com/s/contactsupport&amp;source=gmail&amp;ust=1719150762362000&amp;usg=AOvVaw0s_6H5KzVJNYGzCr6ucidC">contact us</a> for assistance.
                        </td>
                    </tr>
                    </tbody>
                </table>
                </td>
            </tr>
            <tr style="font-family:helvetica,arial,sans-serif">
                <td style="font-family:helvetica,arial,sans-serif">
                <div style="border-top-width:1px;border-top-style:solid;margin:0px auto;padding:0px;width:100%;max-width:640px;font-family:helvetica,arial,sans-serif;border-top-color:#cccccc">&nbsp;</div>
                </td>
            </tr>
            <tr style="font-family:helvetica,arial,sans-serif">
                <td style="font-family:helvetica,arial,sans-serif;background-color:#ffffff">
                <table style="border-spacing:0px;padding:0px;font-size:0px;font-family:helvetica,arial,sans-serif" border="0" width="100%" cellspacing="0" cellpadding="0">
                    <tbody style="font-family:helvetica,arial,sans-serif">
                    <tr style="font-family:helvetica,arial,sans-serif">
                        <td style="padding:10px;font-family:helvetica,arial,sans-serif">
                        <table style="border-spacing:0px;padding:0px;font-size:0px;font-family:helvetica,arial,sans-serif" border="0" width="100%" cellspacing="0" cellpadding="0">
                            <tbody style="font-family:helvetica,arial,sans-serif">
                            <tr style="font-family:helvetica,arial,sans-serif">
                                <td style="padding:20px 0px 0px;font-family:helvetica,arial,sans-serif;background-color:#ffffff">&nbsp;</td>
                            </tr>
                            <tr style="font-family:helvetica,arial,sans-serif">
                                <td style="padding:0px 10px;font-family:helvetica,arial,sans-serif">
                                <table style="border-spacing:0px;font-family:helvetica,arial,sans-serif" border="0" width="100%" cellspacing="0" cellpadding="0">
                                    <tbody style="font-family:helvetica,arial,sans-serif">
                                    <tr style="font-family:helvetica,arial,sans-serif">
                                        <th style="font-family:helvetica;font-size:18px;font-weight:300;line-height:1.11;padding:0px;text-align:center;color:#000000">Items You'll Love</th>
                                    </tr>
                                    </tbody>
                                </table>
                                </td>
                            </tr>
                            <tr style="font-family:helvetica,arial,sans-serif">
                                <td style="height:10px;padding:0px;font-size:20px;line-height:10px;font-family:helvetica,arial,sans-serif;background-color:#ffffff;color:#ffffff" width="100%">&nbsp;</td>
                            </tr>
                            <tr style="font-family:helvetica,arial,sans-serif">
                                <td style="padding:0px;font-size:20px;line-height:20px;font-family:helvetica,arial,sans-serif;background-color:#ffffff;color:#ffffff" width="100%">
                                <table style="max-width:600px;font-family:helvetica,arial,sans-serif" width="100%" cellspacing="0" cellpadding="0" align="center">
                                    <tbody style="font-family:helvetica,arial,sans-serif">
                                    <tr style="font-family:helvetica,arial,sans-serif">
                                        <td style="text-align:center;vertical-align:top;font-size:0px;font-family:helvetica,arial,sans-serif">
                                        <div style="width:300px;display:inline-block;vertical-align:top;font-family:helvetica,arial,sans-serif">
                                            <table style="font-family:helvetica,arial,sans-serif" width="100%">
                                            <tbody style="font-family:helvetica,arial,sans-serif">
                                                <tr style="font-family:helvetica,arial,sans-serif">
                                                <td style="font-family:helvetica,arial,sans-serif;font-size:14px;color:#333333">
                                                    <table style="font-family:helvetica,arial,sans-serif" width="100%">
                                                    <tbody style="font-family:helvetica,arial,sans-serif">
                                                        <tr style="font-family:helvetica,arial,sans-serif">
                                                        <td style="font-family:helvetica,arial,sans-serif" width="50%">
                                                            <span style="font-family:helvetica,arial,sans-serif">
                                                            <a href="http://rm.recs.richrelevance.com/rrmail/click/recs?apiKey=a92d0e9f58f55a71&amp;userId=624239018553009698813225260191075430838103190988412166565741&amp;campaign=OrderConfirm&amp;date=2025-06-12&amp;placement=OrderConfirm&amp;layout=mailservice&amp;region=&amp;slot=1&amp;productId=0400011878407&amp;categoryId=&amp;orderId=&amp;site_refer=EML3348TRIGTRAN" style="font-family:helvetica,arial,sans-serif;text-decoration:none!important" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=http://rm.recs.richrelevance.com/rrmail/click/recs?apiKey%3Da92d0e9f58f55a71%26userId%3D624239018553009698813225260191075430838103190988412166565741%26campaign%3DOrderConfirm%26date%3D2025-06-12%26placement%3DOrderConfirm%26layout%3Dmailservice%26region%3D%26slot%3D1%26productId%3D0400011878407%26categoryId%3D%26orderId%3D%26site_refer%3DEML3348TRIGTRAN&amp;source=gmail&amp;ust=1719150762362000&amp;usg=AOvVaw0JPXOh9pZtt3tr3o0Jpfkr">
                                                                <img style="display:block;border-width:0px;max-width:135px;height:auto;font-family:helvetica,arial,sans-serif" src="https://ci3.googleusercontent.com/meips/ADKq_NZxW2uSjUV5IKLStkF9Jzw7eiPwMzhgenbsRadhox0HF9IcFREw-FDv9D4nZWEd_q9i2HGNjN6HbKV1Iasf1iIAI_KXXMYGyS-WcZs9_FAyACfyMbfbmRAYQtf_xAe2-VNtFUyYaHz_40L0nbUELpzWzkHIoAryMvdjgBRNa8-ypqTs8fzxm374TsJm3lxvDc-7-WbCsBpWX5Q4bxvpXRrXfLnwXMCAUCfqV_WeMBgc5381fQXqf_lr9cjy_xeAdMcaMRhTC6YlARBY88begq9oGBdW_WbPUKb3tqkv4w5sB9ZKbP4yBZzTW4kI0ndHX30alb2hPMdQIHTj4kNcwAKa3gpIk6idGPtm4Zc73CPqLBPGg8NQJfDSaHEpPE8ZpCPzAtIKzn7YiMZ7gPkZC3SEb48DAg=s0-d-e1-ft#http://rm.recs.richrelevance.com/rrmail/image/recs?apiKey=a92d0e9f58f55a71&amp;userId=624239018553009698813225260191075430838103190988412166565741&amp;campaign=OrderConfirm&amp;date=2025-06-12&amp;placement=OrderConfirm&amp;layout=mailservice&amp;region=&amp;slot=1&amp;productId=0400011878407&amp;cate%0D+goryId=&amp;orderId=" alt="Items You'll Love" class="CToWUd" data-bit="iit">
                                                            </a>
                                                            </span>
                                                        </td>
                                                        <td style="font-family:helvetica,arial,sans-serif" width="50%">
                                                            <span style="font-family:helvetica,arial,sans-serif">
                                                            <a href="http://rm.recs.richrelevance.com/rrmail/click/recs?apiKey=a92d0e9f58f55a71&amp;userId=624239018553009698813225260191075430838103190988412166565741&amp;campaign=OrderConfirm&amp;date=2025-06-12&amp;placement=OrderConfirm&amp;layout=mailservice&amp;region=&amp;slot=2&amp;productId=0400011878407&amp;categoryId=&amp;orderId=&amp;site_refer=EML3348TRIGTRAN" style="font-family:helvetica,arial,sans-serif;text-decoration:none!important" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=http://rm.recs.richrelevance.com/rrmail/click/recs?apiKey%3Da92d0e9f58f55a71%26userId%3D624239018553009698813225260191075430838103190988412166565741%26campaign%3DOrderConfirm%26date%3D2025-06-12%26placement%3DOrderConfirm%26layout%3Dmailservice%26region%3D%26slot%3D2%26productId%3D0400011878407%26categoryId%3D%26orderId%3D%26site_refer%3DEML3348TRIGTRAN&amp;source=gmail&amp;ust=1719150762362000&amp;usg=AOvVaw1PC_gagcPdv2IgtU0jD6UV">
                                                                <img style="display:block;border-width:0px;max-width:135px;height:auto;font-family:helvetica,arial,sans-serif" src="https://ci3.googleusercontent.com/meips/ADKq_Nb62dRTuVUGp-SYlTh01zb56Wd4LlDI8xPLzV4l695cNMSrqQqIH7q6V5eL-GyRZrM4lNye0pbBSO6tceuHBK8q5uZ3xUwwIHYXPwLjpLKmiobJrEQmDLRNGTWukwUzdNPoIJy6qS4EqU3BxF-pJJbdD795d47KqoqYgJY_ZQNwNS8ZR9C9pM57MILnyzYbXraO_lcVWZh5jiJJFxt1Y-pSVoz10Wcezj0jtTcrmTVmlrDZ7ygXS_bch_q7-eEqjjxIl4B5iKXHbih5FtLIv8C8KvpPnLrgcLTAAE1tFDtgIfUuXZsNsynt6_btP6JUjgEO6_q0331L-x16Wy-yKhKzUltiua9YE9XEzl4erdGXXPPpIhgHkKQoyAXW22fGc9IpcbSkjbgBpZIU96BUx-sstNmN9g=s0-d-e1-ft#http://rm.recs.richrelevance.com/rrmail/image/recs?apiKey=a92d0e9f58f55a71&amp;userId=624239018553009698813225260191075430838103190988412166565741&amp;campaign=OrderConfirm&amp;date=2025-06-12&amp;placement=OrderConfirm&amp;layout=mailservice&amp;region=&amp;slot=2&amp;productId=0400011878407&amp;cate%0D+goryId=&amp;orderId=" alt="Items You'll Love" class="CToWUd" data-bit="iit">
                                                            </a>
                                                            </span>
                                                        </td>
                                                        </tr>
                                                    </tbody>
                                                    </table>
                                                </td>
                                                </tr>
                                            </tbody>
                                            </table>
                                        </div>
                                        <div style="width:300px;display:inline-block;vertical-align:top;font-family:helvetica,arial,sans-serif">
                                            <table style="font-family:helvetica,arial,sans-serif" width="100%">
                                            <tbody style="font-family:helvetica,arial,sans-serif">
                                                <tr style="font-family:helvetica,arial,sans-serif">
                                                <td style="font-family:helvetica,arial,sans-serif;font-size:14px;color:#333333">
                                                    <table style="font-family:helvetica,arial,sans-serif" width="100%">
                                                    <tbody style="font-family:helvetica,arial,sans-serif">
                                                        <tr style="font-family:helvetica,arial,sans-serif">
                                                        <td style="font-family:helvetica,arial,sans-serif" width="50%">
                                                            <span style="font-family:helvetica,arial,sans-serif">
                                                            <a href="http://rm.recs.richrelevance.com/rrmail/click/recs?apiKey=a92d0e9f58f55a71&amp;userId=624239018553009698813225260191075430838103190988412166565741&amp;campaign=OrderConfirm&amp;date=2025-06-12&amp;placement=OrderConfirm&amp;layout=mailservice&amp;region=&amp;slot=3&amp;productId=0400011878407&amp;categoryId=&amp;orderId=&amp;site_refer=EML3348TRIGTRAN" style="font-family:helvetica,arial,sans-serif;text-decoration:none!important" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=http://rm.recs.richrelevance.com/rrmail/click/recs?apiKey%3Da92d0e9f58f55a71%26userId%3D624239018553009698813225260191075430838103190988412166565741%26campaign%3DOrderConfirm%26date%3D2025-06-12%26placement%3DOrderConfirm%26layout%3Dmailservice%26region%3D%26slot%3D3%26productId%3D0400011878407%26categoryId%3D%26orderId%3D%26site_refer%3DEML3348TRIGTRAN&amp;source=gmail&amp;ust=1719150762363000&amp;usg=AOvVaw1AixOoOGBnKDyg2ZBFANq9">
                                                                <img style="display:block;border-width:0px;max-width:135px;height:auto;font-family:helvetica,arial,sans-serif" src="https://ci3.googleusercontent.com/meips/ADKq_NbghIn0-0sXSwEpydIX9rFN2XOCIQF-85uXv2atvAtk3-C0zBzMlVclFF-ma_eKwNn7HrBSX6a7FZZ2JNWIJAG9-qRQny2hS6swA37E1jUHHNFoSLZOtO9etMUJ_wwCFxKvzRGYQ8KVo_5SyUbPl6PcdZilgz_AgUJZR4oESaPS_a-TOudlD2ioiS3ij9ozuXiLJrlDyJCbDhCk6UVLiRTZGmRAzsaAKuP_5LIUAxz80dKLY2xNQ8OT5xQuxzQxjBsgnHhZ647QH4OW4pePXPCIPplhePIHBi4AurfIFhsihOttM_o8VYjYPER3u9oA5Ek-hNsZVg7DrLWlV4zF5bme_FKXq4loYGaayPBxOHfiG-SYvtl1N0YWMFIZlNTISFnc8gleJIk5iqWTNH79npbPTrXndw=s0-d-e1-ft#http://rm.recs.richrelevance.com/rrmail/image/recs?apiKey=a92d0e9f58f55a71&amp;userId=624239018553009698813225260191075430838103190988412166565741&amp;campaign=OrderConfirm&amp;date=2025-06-12&amp;placement=OrderConfirm&amp;layout=mailservice&amp;region=&amp;slot=3&amp;productId=0400011878407&amp;cate%0D+goryId=&amp;orderId=" alt="Items You'll Love" class="CToWUd" data-bit="iit">
                                                            </a>
                                                            </span>
                                                        </td>
                                                        <td style="font-family:helvetica,arial,sans-serif" width="50%">
                                                            <span style="font-family:helvetica,arial,sans-serif">
                                                            <a href="http://rm.recs.richrelevance.com/rrmail/click/recs?apiKey=a92d0e9f58f55a71&amp;userId=624239018553009698813225260191075430838103190988412166565741&amp;campaign=OrderConfirm&amp;date=2025-06-12&amp;placement=OrderConfirm&amp;layout=mailservice&amp;region=&amp;slot=4&amp;productId=0400011878407&amp;categoryId=&amp;orderId=&amp;site_refer=EML3348TRIGTRAN" style="font-family:helvetica,arial,sans-serif;text-decoration:none!important" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=http://rm.recs.richrelevance.com/rrmail/click/recs?apiKey%3Da92d0e9f58f55a71%26userId%3D624239018553009698813225260191075430838103190988412166565741%26campaign%3DOrderConfirm%26date%3D2025-06-12%26placement%3DOrderConfirm%26layout%3Dmailservice%26region%3D%26slot%3D4%26productId%3D0400011878407%26categoryId%3D%26orderId%3D%26site_refer%3DEML3348TRIGTRAN&amp;source=gmail&amp;ust=1719150762363000&amp;usg=AOvVaw0YUVhxIu9-H5GplwccJVeq">
                                                                <img style="display:block;border-width:0px;max-width:135px;height:auto;font-family:helvetica,arial,sans-serif" src="https://ci3.googleusercontent.com/meips/ADKq_NbLqWFsKWS3xOdx8XMYSHrotaWpLiyRqrLarABRRBRz2SjuOSHAKK5yfUA2njlDjwBjRHebp7UbH_pREIkDeUQQZ7aki76oE_1tC9saA9Gb4OiFIwzfHCDIXFGnmzkGmSpCguDIXJ5K6H1njD9CEzR4SboqluTahdvwInPHyHNuOXyvBBC2tZ4D8Up6uG9SOXaOXy8IkI5hYfF09AAqdzX-x6y58EUc9MRpaeB61RaeDRex_koEu103wds64oLTDYmjJdiFY9BuNPOTS0i7JTdX6tE5mX_F21PHw8AXbRG1BhWP9dLe86wGMlq0-I8RBOjjZ62GEZzcZMqVnMJL5tSJTcXovtA9nUgQsQkyKedDPIAG8cRqec-IDn7Sh2IbVrOomTe-6QX9bfaG2nG9wZAtWPjJMw=s0-d-e1-ft#http://rm.recs.richrelevance.com/rrmail/image/recs?apiKey=a92d0e9f58f55a71&amp;userId=624239018553009698813225260191075430838103190988412166565741&amp;campaign=OrderConfirm&amp;date=2025-06-12&amp;placement=OrderConfirm&amp;layout=mailservice&amp;region=&amp;slot=4&amp;productId=0400011878407&amp;cate%0D+goryId=&amp;orderId=" alt="Items You'll Love" class="CToWUd" data-bit="iit">
                                                            </a>
                                                            </span>
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
                            <tr style="font-family:helvetica,arial,sans-serif">
                                <td style="height:20px;padding:0px;font-size:20px;line-height:20px;font-family:helvetica,arial,sans-serif;background-color:#ffffff;color:#ffffff" width="100%">&nbsp;</td>
                            </tr>
                            </tbody>
                        </table>
                        </td>
                    </tr>
                    </tbody>
                </table>
                </td>
            </tr>
            <tr style="font-family:helvetica,arial,sans-serif">
                <td style="font-family:helvetica,arial,sans-serif">
                <div style="border-top-width:1px;border-top-style:solid;margin:0px auto;padding:0px;width:100%;max-width:640px;font-family:helvetica,arial,sans-serif;border-top-color:#cccccc">&nbsp;</div>
                </td>
            </tr>
            <tr style="font-family:helvetica,arial,sans-serif">
                <td id="m_5750059814468834653footer" style="text-align:center;font-family:helvetica,arial,sans-serif">
                <div id="m_5750059814468834653footer-social-icons" style="width:100%;max-width:100%;height:80px;display:inline-block;padding-top:20px;padding-right:20px;text-align:center;font-family:helvetica,arial,sans-serif;padding-bottom:20px!important">
                    <table style="max-width:75%;height:100%;text-align:center;border-spacing:0px;padding:0px;font-family:helvetica,arial,sans-serif" border="0" cellspacing="0" cellpadding="0" align="center">
                    <tbody style="font-family:helvetica,arial,sans-serif">
                        <tr style="font-family:helvetica,arial,sans-serif">
                        <td style="padding:0px;font-family:helvetica,arial,sans-serif" width="22">
                            <a href="https://www.facebook.com/saks" style="font-family:helvetica,arial,sans-serif" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.facebook.com/saks&amp;source=gmail&amp;ust=1719150762363000&amp;usg=AOvVaw3zMwaDIFQuFWEkSI_Pd3sB">
                            <img style="border-width:0px;display:block;font-family:helvetica,arial,sans-serif" src="https://ci3.googleusercontent.com/meips/ADKq_NYWiEF5oPe-LHnYIyUca194lFkgwCcPahe8E5x5_I9ESsGW35HW42EFL4l61OdiQW5m29aOUphixXjFvrviqZzL5YhzcdrkvQ_OVG1bcdGOOmyCFGLK=s0-d-e1-ft#https://s3.us-east-2.amazonaws.com/hbc-email-images/facebook.png" alt="Facebook" width="22" height="22" align="middle" class="CToWUd" data-bit="iit">
                            </a>
                        </td>
                        <td style="width:20px;font-family:helvetica,arial,sans-serif">&nbsp;</td>
                        <td style="padding:0px;font-family:helvetica,arial,sans-serif" width="22">
                            <a href="https://www.twitter.com/saks" style="font-family:helvetica,arial,sans-serif" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.twitter.com/saks&amp;source=gmail&amp;ust=1719150762363000&amp;usg=AOvVaw2EcHz350rzrXrLcAmrdjSi">
                            <img style="border-width:0px;display:block;font-family:helvetica,arial,sans-serif" src="https://ci3.googleusercontent.com/meips/ADKq_NZoqKdDO5rMIziMIwNvxbmJu2x9s8JmlBBI9etPytfY7yMUixFfZEgbiRyMPtp8nPm9SOSjB_vk3rdgzuWFkf5qRz-j2JH-Ot65BOkIgPWhJloOch4=s0-d-e1-ft#https://s3.us-east-2.amazonaws.com/hbc-email-images/twitter.png" alt="Twitter" width="22" height="22" align="middle" class="CToWUd" data-bit="iit">
                            </a>
                        </td>
                        <td style="width:20px;font-family:helvetica,arial,sans-serif">&nbsp;</td>
                        <td style="padding:0px;font-family:helvetica,arial,sans-serif" width="22">
                            <a href="https://www.instagram.com/saks/" style="font-family:helvetica,arial,sans-serif" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.instagram.com/saks/&amp;source=gmail&amp;ust=1719150762363000&amp;usg=AOvVaw1adkvsV7X6XGlr1-eYtrjp">
                            <img style="border-width:0px;display:block;font-family:helvetica,arial,sans-serif" src="https://ci3.googleusercontent.com/meips/ADKq_NYtEhl55DK2w-5XlgLLe5XwM0pRnovd1tMoF38JKl_b1MEv8k2Jv_ZBZS8LNiGEUfRMx6aba7DiOKE4cx61Ulh71_HB7ZzPf2Igcbu9GN7l31PyxDOXRQ=s0-d-e1-ft#https://s3.us-east-2.amazonaws.com/hbc-email-images/instagram.png" alt="Instagram" width="22" height="22" align="middle" class="CToWUd" data-bit="iit">
                            </a>
                        </td>
                        <td style="width:20px;font-family:helvetica,arial,sans-serif">&nbsp;</td>
                        <td style="padding:0px;font-family:helvetica,arial,sans-serif" width="22">
                            <a href="https://www.youtube.com/saks/" style="font-family:helvetica,arial,sans-serif" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.youtube.com/saks/&amp;source=gmail&amp;ust=1719150762363000&amp;usg=AOvVaw0X_iLG6bkiUid4SxlcdFLO">
                            <img style="border-width:0px;display:block;font-family:helvetica,arial,sans-serif" src="https://ci3.googleusercontent.com/meips/ADKq_Na3OGJ8YgsCs1689-Dnj_8e78WwylZd9ekCCmdRHKUFYBCCTQ3rZtwPdB3BMbxLpiRRAbZ30FLzFwsf8lA40L0UD2jOwvUtDmY5s82S0vgbeYRFMk8=s0-d-e1-ft#https://s3.us-east-2.amazonaws.com/hbc-email-images/youtube.png" alt="Youtube" width="22" height="22" align="middle" class="CToWUd" data-bit="iit">
                            </a>
                        </td>
                        <td style="width:25px;font-family:helvetica,arial,sans-serif">&nbsp;</td>
                        <td style="padding:0px;font-family:helvetica,arial,sans-serif" width="79">
                            <a href="https://itunes.apple.com/us/app/saks-fifth-avenue/id491507258?site_refer=EML3348TRIGTRAN" style="font-family:helvetica,arial,sans-serif" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://itunes.apple.com/us/app/saks-fifth-avenue/id491507258?site_refer%3DEML3348TRIGTRAN&amp;source=gmail&amp;ust=1719150762363000&amp;usg=AOvVaw096-730BLhH2GM2ntbcRWE">
                            <img style="border-width:0px;display:block;font-family:helvetica,arial,sans-serif" src="https://ci3.googleusercontent.com/meips/ADKq_NZWq4l_OJs6QcFGrEXDeKUV8CcYgCqenQinE8QHoYwCTFUx_j7eoDQXekPmwmW3KuMY9DNl6_Bpj8qMqj6lzGK91C7kZdvxcA3nV8Ol7f5Ss1wbb-WBoBMGEw=s0-d-e1-ft#https://s3.us-east-2.amazonaws.com/hbc-email-images/ios_appstore.png" alt="Get the Saks iOS App" width="79" height="24" align="middle" class="CToWUd" data-bit="iit">
                            </a>
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
    </center><div class="yj6qo"></div><div class="adL">
    </div></div><div class="adL">
    </div></div><div class="adL">

    </div></div></div><div class="WhmR8e" data-hash="0"></div></div>
    """

    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
