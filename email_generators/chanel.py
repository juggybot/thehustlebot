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
    msg['From'] = formataddr((f'CHANEL', sender_email))
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
    "Please enter the image url (MUST BE FROM CHANEL SITE):",
    "Please enter the item name (Sabre Jacket Print Men's):",
    "Please enter the item price (WITHOUT THE $ SIGN):",
    "Please enter the tax price (WITHOUT THE $ SIGN):",
    "Please enter the delivery cost (WITHOUT THE $ SIGN):",
    "Please enter the total cost (WITHOUT THE $ SIGN):",
    "Please enter the customer's full name (Juggy Resells):",
    "Please enter the street address (123 Cartier St):",
    "Please enter the suburb (Sydney):",
    "Please enter the state + postcode (NSW 2000):",
    "Please enter the country (Australia):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira a URL da imagem (DEVE SER DO SITE DA CHANEL):",
    "Por favor, insira o nome do item (Sabre Jacket Print Masculino):",
    "Por favor, insira o preço do item (SEM O SINAL $):",
    "Por favor, insira o valor do imposto (SEM O SINAL $):",
    "Por favor, insira o custo de entrega (SEM O SINAL $):",
    "Por favor, insira o custo total (SEM O SINAL $):",
    "Por favor, insira o nome completo do cliente (Juggy Resells):",
    "Por favor, insira o endereço (123 Cartier St):",
    "Por favor, insira o bairro (Sydney):",
    "Por favor, insira o estado + CEP (NSW 2000):",
    "Por favor, insira o país (Austrália):",
    "Por favor, insira a moeda ($/€/£):",
    "Qual endereço de e-mail você deseja receber este e-mail (juggyresells@gmail.com):"
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
    part1 = random.randint(1000000000, 9999999999)  # Random 8-digit number

    # Combine the parts into order number
    order_number = f"MP1US{part1}"
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
    recipient_email = f'{user_inputs[12]}'
    subject = f"Your CHANEL Order {order_num} confirmation"

    html_template = f"""
            <td align="center" bgcolor="#ffffff">
        <table style="margin:0px auto" border="0" width="640" cellspacing="0" cellpadding="0" align="center" bgcolor="#ffffff">
        <tbody>
            <tr>
            <td align="center" valign="top" width="640">
                <table border="0" width="560" cellspacing="0" cellpadding="0">
                <tbody>
                    <tr>
                    <td style="line-height:8px;font-size:0px" bgcolor="#000000" height="8">&nbsp;</td>
                    </tr>
                </tbody>
                </table>
                <table border="0" width="560" cellspacing="0" cellpadding="0" align="center">
                <tbody>
                    <tr>
                    <td align="center" valign="top">
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:36px;line-height:36px" height="36">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <div style="height:28px">
                        <a href="https://enews-us.chanel.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%3DCAWTWAAT&amp;_ei_=ERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.&amp;_di_=kmi7mqaib1dfb8idkumfpejqadfe4g6khmmr6lk0r039h8nvklj0" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://enews-us.chanel.com/pub/cc?_ri_%3DX0Gzc2X%253DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%253DCAWTWAAT%26_ei_%3DERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.%26_di_%3Dkmi7mqaib1dfb8idkumfpejqadfe4g6khmmr6lk0r039h8nvklj0&amp;source=gmail&amp;ust=1718818826515000&amp;usg=AOvVaw2bF55_zeAv1oJOpBHSkUQE">
                            <img style="display:block;font-size:10px;font-family:Helvetica,Arial,sans-serif;color:#9b9b9b" src="https://ci3.googleusercontent.com/meips/ADKq_NagCdM7sFV6IH51IzhvtCwPPIIwVlz6LDvaXjsCQrmlS_xz2XW9GWGeINHX5zK_Bnwx5xZ4oXFFH1u9ywAFdNyvJquxW6ptXjAIWCYa9ZD49IRzUNmmCusoTJbB6_zxEwAcL999n2L1PrjiAvZFLgl3WV8mfO_usYe2y3pJVgTu3ijnNVraMsee4leauk4WzxoAGbNPKauD1iw=s0-d-e1-ft#https://enews-us.chanel.com/assets/responsysimages/chanel/contentlibrary/transactional/orderconfirmation/images/chanel-black@2x.png" alt="CHANEL" width="177" height="28" border="0" class="CToWUd" data-bit="iit">
                        </a>
                        </div>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:36px;line-height:36px" height="36">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                    </td>
                    </tr>
                </tbody>
                </table>
                <table border="0" width="560" cellspacing="0" cellpadding="0" align="center">
                <tbody>
                    <tr>
                    <td align="center" valign="top">
                        <div style="height:26px">
                        <img style="display:block;font-size:10px;font-family:Helvetica,Arial,sans-serif;color:#9b9b9b" src="https://ci3.googleusercontent.com/meips/ADKq_NYN_9uJMAPmEDRlfHKP839TVwsexLIxDOi8rTCDdQAFbtGlqkU_HVn0IOosbFkbmfpvuBnNG6kaXOWj9QXC_BLdJGEwdxsi7-77qGffJkAiOnJhCj2tnPbpMbPb31aXMlXJzm9YFv8XCKCCykWuhqiTgrX4LU8KS9PFnPhh7VZVT6xDmMIVnZadtQrMe1sPksAU5X_BBAnq0YgNc4nAdV6V=s0-d-e1-ft#https://enews-us.chanel.com/assets/responsysimages/chanel/contentlibrary/transactional/orderconfirmation/images/thank_you_for_order@2x.png" alt="THANK YOU FOR YOUR ORDER" width="450" height="26" border="0" class="CToWUd" data-bit="iit">
                        </div>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:36px;line-height:36px" height="36">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                    </td>
                    </tr>
                </tbody>
                </table>
                <table border="0" width="560" cellspacing="0" cellpadding="0" align="center">
                <tbody>
                    <tr>
                    <td align="left" valign="top">
                        <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:23px;font-weight:normal;color:#1d1d1d">Dear Amanda Morales, 
                        <br>
                        <br>We are pleased to confirm your order 
                        <strong style="font-family:Arial,Helvetica,sans-serif">{order_num}</strong> placed on the  has been received and is currently being processed. 
                        <br>
                        <br>You will receive a separate email once your purchase is sent for delivery, and you will not be charged until your order ships. 
                        <br>
                        <br>If you have any questions regarding your order, please call 
                        <a href="tel:1-800-550-0005" style="font-weight:bold;text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:#1d1d1d" rel="noopener" target="_blank">1.800.550.0005</a> to speak with a 
                        <a href="http://chanel.com" style="font-family:Arial,Helvetica,sans-serif" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=http://chanel.com&amp;source=gmail&amp;ust=1718818826516000&amp;usg=AOvVaw0q2OGlfpsP_FjZsEOrwWT5">chanel.com</a> Customer Care Representative.
                        </div>
                    </td>
                    </tr>
                </tbody>
                </table>
                <table border="0" cellspacing="0" cellpadding="0">
                <tbody>
                    <tr>
                    <td style="font-size:36px;line-height:36px" height="36">&nbsp;</td>
                    </tr>
                </tbody>
                </table>
                <table border="0" width="560" cellspacing="0" cellpadding="0" align="center">
                <tbody>
                    <tr>
                    <td align="left" valign="top">
                        <div style="height:15px">
                        <img style="display:block;font-size:10px;font-family:Helvetica,Arial,sans-serif;color:#9b9b9b" src="https://ci3.googleusercontent.com/meips/ADKq_Na42OizAFcEVYMfCQ0OzwXwWYKuCxqO3kouIRNk3c8va8GmhA2lBPmmg-1OtyS14L-50bRWQLPs66bdnbvb9tnJbD1vHPpwQr1hbBH4IkPMK-UXJqW5biBHOf_DxAoDD9--RZx1FVXxo4_XTf614UVtys4MvYT05nuBxTgZKZAgN11V4KZiy7sYf7qQWAMtNMFFEp6-lyEF5QpI=s0-d-e1-ft#https://enews-us.chanel.com/assets/responsysimages/chanel/contentlibrary/transactional/orderconfirmation/images/items_ordered@2x.png" alt="ITEM(S) ORDERED" width="174" height="15" border="0" class="CToWUd" data-bit="iit">
                        </div>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:9px;line-height:9px" height="9">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" width="560" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="line-height:1px;font-size:0px" bgcolor="#767676" height="1">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:36px;line-height:36px" height="36">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table style="padding-bottom:18px" border="0" width="560" cellspacing="0" cellpadding="0" align="center">
                        <tbody>
                            <tr>
                            <td align="left" valign="top" width="80">
                                <img style="display:block;font-size:10px;font-family:Helvetica,Arial,sans-serif;color:#9b9b9b" src="{user_inputs[0]}" alt="{user_inputs[1]}" width="80" height="80" border="0" class="CToWUd" data-bit="iit">
                            </td>
                            <td width="18">&nbsp;</td>
                            <td align="left" valign="top" width="462">
                                <table>
                                <tbody>
                                    <tr>
                                    <td align="left" valign="top" width="462">
                                        <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:22px;font-weight:bold;color:#1d1d1d">{user_inputs[1]}</div>
                                        <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:22px;font-weight:normal;color:#333333"></div>
                                        <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:22px;font-weight:normal;color:#333333"></div>
                                    </td>
                                    </tr>
                                    <tr>
                                    <td align="left" valign="top" width="80">
                                        <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;font-weight:normal;color:#333333">Qty 1</div>
                                    </td>
                                    <td align="right" valign="top" width="62">
                                        <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;font-weight:bold;color:#333333">{user_inputs[11]}{user_inputs[2]}</div>
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
                <table border="0" cellspacing="0" cellpadding="0">
                <tbody>
                    <tr>
                    <td style="font-size:16px;line-height:16px" height="36">&nbsp;</td>
                    </tr>
                </tbody>
                </table>
                <table border="0" width="560" cellspacing="0" cellpadding="0" align="center" bgcolor="#F9F9F9">
                <tbody>
                    <tr>
                    <td width="36">&nbsp;</td>
                    <td align="left" valign="top" width="488">
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:36px;line-height:36px" height="36">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td align="left" valign="top" width="244">
                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;font-weight:normal;color:#333333">Subtotal</div>
                            </td>
                            <td align="right" valign="top" width="244">
                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;font-weight:bold;color:#333333">{user_inputs[11]}{user_inputs[2]}</div>
                            </td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:18px;line-height:18px" height="18">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td align="left" valign="top" width="244">
                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;font-weight:normal;color:#333333">Taxes*</div>
                            </td>
                            <td align="right" valign="top" width="244">
                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;font-weight:bold;color:#333333">{user_inputs[11]}{user_inputs[3]}</div>
                            </td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:18px;line-height:18px" height="18">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td align="left" valign="top" width="244">
                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;font-weight:normal;color:#333333">Shipping - FedEx 2 Day</div>
                            </td>
                            <td align="right" valign="top" width="244">
                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;font-weight:bold;color:#333333">{user_inputs[11]}{user_inputs[4]}</div>
                            </td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:18px;line-height:18px" height="18">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td align="left" valign="top" width="244">
                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:22px;font-weight:bold;color:#1d1d1d">Total</div>
                            </td>
                            <td align="right" valign="top" width="244">
                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:18px;line-height:24px;font-weight:bold;color:#1d1d1d">{user_inputs[11]}{user_inputs[5]}</div>
                            </td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:36px;line-height:36px" height="36">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                    </td>
                    <td width="36">&nbsp;</td>
                    </tr>
                </tbody>
                </table>
                <table style="padding:20px 10px" border="0" width="560" cellspacing="0" cellpadding="0" align="center">
                <tbody>
                    <tr>
                    <td align="left" valign="top">
                        <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:23px;font-weight:normal;color:#a8a8a8">*The tax shown is an estimate and will be finalized once your order is charged. By placing an order, you consented to a pre-authorization charge of up to {user_inputs[11]}1 over the estimated tax amount. You will only be charged the final tax amount.</div>
                    </td>
                    </tr>
                </tbody>
                </table>
                <table border="0" cellspacing="0" cellpadding="0">
                <tbody>
                    <tr>
                    <td style="font-size:18px;line-height:18px" height="18">&nbsp;</td>
                    </tr>
                </tbody>
                </table>
                <table border="0" width="560" cellspacing="0" cellpadding="0" align="center">
                <tbody>
                    <tr>
                    <td align="left" valign="top">
                        <div style="height:13px">
                        <img style="display:block;font-size:10px;font-family:Helvetica,Arial,sans-serif;color:#9b9b9b" src="https://ci3.googleusercontent.com/meips/ADKq_NZB5ei5TpuvYFKtcG0PGLcjv0N0KVBUaphGhriTLLSpSLzn5I7UZxntIkykUg8CwghOetLj1QY8Ec9isOjsHXf6tajUdLbzJ1031IACrhEQp1-6RV2WfK_QmcZTHR8i1QDbwueCvNNEsOheYhy2X60hU2zEGlgeP1zvO3_7kigs58rVOq1OjoTUESjmmJh5IR0C8Yeg=s0-d-e1-ft#https://enews-us.chanel.com/assets/responsysimages/chanel/contentlibrary/transactional/orderconfirmation/images/shipping@2x.png" alt="SHIPPING" width="95" height="13" border="0" class="CToWUd" data-bit="iit">
                        </div>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:9px;line-height:9px" height="9">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" width="560" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="line-height:1px;font-size:0px" bgcolor="#767676" height="1">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:16px;line-height:16px" height="16">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                    </td>
                    </tr>
                    <tr>
                    <td align="left" valign="top">
                        <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:21px;font-weight:normal;color:#333333">{user_inputs[6]}<br>{user_inputs[7]}, {user_inputs[8]}<br>{user_inputs[9]}<br>{user_inputs[10]}<br>
                        <br>
                        <a href="#"
                        <br>
                        <a href="#"
                        </div>
                    </td>
                    </tr>
                </tbody>
                </table>
                <table border="0" cellspacing="0" cellpadding="0">
                <tbody>
                    <tr>
                    <td style="font-size:45px;line-height:45px" height="45">&nbsp;</td>
                    </tr>
                </tbody>
                </table>
                <table border="0" width="560" cellspacing="0" cellpadding="0" align="center">
                <tbody>
                    <tr>
                    <td align="left" valign="top">
                        <div style="height:13px">
                        <img style="display:block;font-size:10px;font-family:Helvetica,Arial,sans-serif;color:#9b9b9b" src="https://ci3.googleusercontent.com/meips/ADKq_NabN-a61E8ozSk8cmF2VVIZ7uWn4ozh2_bhoHNV4EbSEOkjJifSEXrsgrYHZdiPhtapF2b6SJSJyvhyyg59uIv8rFQDYLwmLwOSF2xVvXp_2d4wERp_uIGFG1nj2dhPDdTqBenBDqu4-mGvHZvtGEmvmpQP43LdZrnrdntPGYo1S2hoRbtQHxc9gG2NVmYXXeQg-qc=s0-d-e1-ft#https://enews-us.chanel.com/assets/responsysimages/chanel/contentlibrary/transactional/orderconfirmation/images/billing@2x.png" alt="BILLING" width="76" height="13" border="0" class="CToWUd" data-bit="iit">
                        </div>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:9px;line-height:9px" height="9">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" width="560" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="line-height:1px;font-size:0px" bgcolor="#767676" height="1">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:16px;line-height:16px" height="16">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;font-weight:bold;color:#333333">Billing address</div>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:9px;line-height:9px" height="9">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:21px;font-weight:normal;color:#333333">{user_inputs[6]}<br>{user_inputs[7]}, {user_inputs[8]}<br>{user_inputs[9]}<br>{user_inputs[10]}<br>
                        <br>
                        <a href="#"
                        <br>
                        <a href="#"
                        </div>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:27px;line-height:27px" height="27">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;font-weight:bold;color:#333333">Payment details</div>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:9px;line-height:9px" height="9">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td align="left" valign="top">
                                <img style="display:block;font-size:10px;font-family:Helvetica,Arial,sans-serif;color:#9b9b9b" src="https://ci3.googleusercontent.com/meips/ADKq_Nbc4TOLzU8qXlj0T6jVtZkqJnzknE7wSYG1EhWcq6Cjn4DN6sRvZJ4WONfwpkYCVLPc1gbnNFJ6v2odL2cfUQ3O1LM_I7RfJUdk7QI0FtqkGUuH-W-ZpBnP3yfK1MOMPyohPfvFvZw=s0-d-e1-ft#https://enews-us.chanel.com/assets/responsysimages/content/chanel/ApplePay@2x.png" alt="" width="43" height="24" border="0" class="CToWUd" data-bit="iit">
                            </td>
                            <td width="9">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                    </td>
                    </tr>
                </tbody>
                </table>
                <table border="0" cellspacing="0" cellpadding="0">
                <tbody>
                    <tr>
                    <td style="font-size:62px;line-height:62px" height="62">&nbsp;</td>
                    </tr>
                </tbody>
                </table>
                <table border="0" width="640" cellspacing="0" cellpadding="0" align="center">
                <tbody>
                    <tr>
                    <td align="center" valign="top">
                        <table border="0" width="640" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="line-height:1px;font-size:0px" bgcolor="#ECECEC" height="1">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:54px;line-height:54px" height="54">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <div style="height:11px">
                        <img style="display:block;font-size:10px;font-family:Helvetica,Arial,sans-serif;color:#9b9b9b" src="https://ci3.googleusercontent.com/meips/ADKq_NajEjx0wwjv91KcBC7CxUw4d77tvW_k1BXLIJKcHK0rpsJlUDL56XUntn6eGdT4ybAdEtAcyvRqj-paOkEHrfGE336KWPOXalITedT_C7sstzFdnVJGNWOvnEtM7A2MAsbkyz12JQfHtDk0yQJcDu1owgqs75vs_NW5NLIYY10O8wZM4oD5ztv3evXAiirOfY_eDznDXa0eoQgn=s0-d-e1-ft#https://enews-us.chanel.com/assets/responsysimages/chanel/contentlibrary/transactional/orderconfirmation/images/customer_care@2x.png" alt="CUSTOMER CARE" width="151" height="11" border="0" class="CToWUd" data-bit="iit">
                        </div>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:3px;line-height:3px" height="3">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;font-weight:normal;color:#767676">Monday to Sunday, 7 AM to 12 AM ET. 
                        <br>
                        <span style="font-family:Arial,Helvetica,sans-serif;color:#151515">Call 
                            <a href="tel:1-800-550-0005" style="text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:#151515" rel="noopener" target="_blank">1.800.550.0005</a>
                        </span>
                        </div>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:18px;line-height:18px" height="18">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                        <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;font-weight:normal;color:#333333">
                        <a href="mailto:customercare@chanelusa.com" style="font-weight:normal;text-decoration:underline;font-family:Arial,Helvetica,sans-serif;color:#333333" rel="noopener" target="_blank">Email</a>
                        </div>
                        <table border="0" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                            <td style="font-size:50px;line-height:50px" height="50">&nbsp;</td>
                            </tr>
                        </tbody>
                        </table>
                    </td>
                    </tr>
                </tbody>
                </table>
                <table border="0" width="640" cellspacing="0" cellpadding="0" align="center" bgcolor="#000000">
                <tbody>
                    <tr>
                    <td align="center" valign="top" width="640">
                        <table border="0" width="560" cellspacing="0" cellpadding="0" align="center" bgcolor="#000000">
                        <tbody>
                            <tr>
                            <td align="center" valign="top">
                                <table border="0" cellspacing="0" cellpadding="0">
                                <tbody>
                                    <tr>
                                    <td style="font-size:54px;line-height:54px" height="54">&nbsp;</td>
                                    </tr>
                                </tbody>
                                </table>
                                <div style="height:20px">
                                <a href="https://enews-us.chanel.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%3DCAWTWBRT&amp;_ei_=EW2tf9zs59idfPO1Sc_9BbmMBtwtsnA8PG0lUQvrDQ9H9paudvdySz91S2cr-ViAftI-bg1IrlR2Gw_w6wHN2dylzRiD46LTo7JcjiTVaMHwBY8hH36NoTRLtdkN.&amp;_di_=4oubpun86eckp3dhgo2jedoeko3sfrc3kfbo9ijhcl9fo8t1648g" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://enews-us.chanel.com/pub/cc?_ri_%3DX0Gzc2X%253DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%253DCAWTWBRT%26_ei_%3DEW2tf9zs59idfPO1Sc_9BbmMBtwtsnA8PG0lUQvrDQ9H9paudvdySz91S2cr-ViAftI-bg1IrlR2Gw_w6wHN2dylzRiD46LTo7JcjiTVaMHwBY8hH36NoTRLtdkN.%26_di_%3D4oubpun86eckp3dhgo2jedoeko3sfrc3kfbo9ijhcl9fo8t1648g&amp;source=gmail&amp;ust=1718818826516000&amp;usg=AOvVaw2hL7aSt58nN3tw5dDuRuxV">
                                    <img style="display:block;font-size:10px;font-family:Helvetica,Arial,sans-serif;color:#9b9b9b" src="https://ci3.googleusercontent.com/meips/ADKq_NaLe9VNbXpDEZW-oKf2saBupepybZmSaPVhHZyccr8ESL6sgkrVwOhs2kPRcyPoO30rQFPd3X3H4y7BFJrskHbSkpUHN5hmOcxePa7n0xX6gulY_mWjWJ3VIQwMg2WfZLNeuWTSJmy3XIz_uS75hEkkrvYTKVR1ZehqDO7j8OYorKRpyXnHoJWRv4e5OX2q_nTZg9w5DlcbzZ8=s0-d-e1-ft#https://enews-us.chanel.com/assets/responsysimages/chanel/contentlibrary/transactional/orderconfirmation/images/chanel-white@2x.png" alt="CHANEL" width="120" height="20" border="0" class="CToWUd" data-bit="iit">
                                </a>
                                </div>
                                <table border="0" cellspacing="0" cellpadding="0">
                                <tbody>
                                    <tr>
                                    <td style="font-size:54px;line-height:54px" height="54">&nbsp;</td>
                                    </tr>
                                </tbody>
                                </table>
                            </td>
                            </tr>
                            <tr>
                            <td align="center" valign="top">
                                <table border="0" width="560" cellspacing="0" cellpadding="0" align="center">
                                <tbody>
                                    <tr>
                                    <th align="left" valign="top">
                                        <table border="0" cellspacing="0" cellpadding="0">
                                        <tbody>
                                            <tr>
                                            <td align="left" valign="top">
                                                <div style="height:10px">
                                                <img style="display:block;font-size:10px;font-family:Helvetica,Arial,sans-serif;color:#9b9b9b" src="https://ci3.googleusercontent.com/meips/ADKq_NZk1iSGRXZ5tkVT1U4Qw68foadnPWq1FThRYflMBV6d3YEj6ZXsPfT7OSxG9O7GDJOoc_fHlX0cr_UtUotyjR9EmjJhb7OZdG0wljinxsfGveUEi7lgbkq1zDXJd10UkviYnoZLV5vtyjKFaYzuE4D241XZv0w370ObTh4LpcI222Vt4gJ5BxikyMUdZXJDPfR6L8I=s0-d-e1-ft#https://enews-us.chanel.com/assets/responsysimages/chanel/contentlibrary/transactional/orderconfirmation/images/explore@2x.png" alt="EXPLORE CHANEL.COM" width="173" height="10" border="0" class="CToWUd" data-bit="iit">
                                                </div>
                                                <table border="0" cellspacing="0" cellpadding="0">
                                                <tbody>
                                                    <tr>
                                                    <td style="font-size:13px;line-height:13px" height="13">&nbsp;</td>
                                                    </tr>
                                                </tbody>
                                                </table>
                                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:27px;font-weight:normal;color:#9b9b9b">
                                                <a href="https://enews-us.chanel.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%3DCAWTWBTT&amp;_ei_=ERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.&amp;_di_=6c3orf4go233g1sekbaljbr97po8abnb1foar41emn3ka70eqebg" style="font-weight:normal;text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:#9b9b9b" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://enews-us.chanel.com/pub/cc?_ri_%3DX0Gzc2X%253DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%253DCAWTWBTT%26_ei_%3DERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.%26_di_%3D6c3orf4go233g1sekbaljbr97po8abnb1foar41emn3ka70eqebg&amp;source=gmail&amp;ust=1718818826516000&amp;usg=AOvVaw2uTVtQwWrK0EADauXXxgE2">Haute Couture</a>
                                                </div>
                                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:27px;font-weight:normal;color:#9b9b9b">
                                                <a href="https://enews-us.chanel.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%3DCAWTWBWT&amp;_ei_=ERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.&amp;_di_=f0qd93iaf35fa648b3olq58mck2b4m5eqigjspf6sjpoca1t7kg0" style="font-weight:normal;text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:#9b9b9b" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://enews-us.chanel.com/pub/cc?_ri_%3DX0Gzc2X%253DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%253DCAWTWBWT%26_ei_%3DERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.%26_di_%3Df0qd93iaf35fa648b3olq58mck2b4m5eqigjspf6sjpoca1t7kg0&amp;source=gmail&amp;ust=1718818826517000&amp;usg=AOvVaw051oJy-4_WlZ7yijsAYvNN">Fashion</a>
                                                </div>
                                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:27px;font-weight:normal;color:#9b9b9b">
                                                <a href="https://enews-us.chanel.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%3DCAWTWBAT&amp;_ei_=ERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.&amp;_di_=n9fn0kgj2vuq9t870injukove0rla9f5j3ose5320fc8kqs36p00" style="font-weight:normal;text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:#9b9b9b" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://enews-us.chanel.com/pub/cc?_ri_%3DX0Gzc2X%253DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%253DCAWTWBAT%26_ei_%3DERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.%26_di_%3Dn9fn0kgj2vuq9t870injukove0rla9f5j3ose5320fc8kqs36p00&amp;source=gmail&amp;ust=1718818826517000&amp;usg=AOvVaw1Aita1f_RcK5ehFM12u-0M">Eyewear</a>
                                                </div>
                                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:27px;font-weight:normal;color:#9b9b9b">
                                                <a href="https://enews-us.chanel.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%3DCAWTWBCT&amp;_ei_=ERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.&amp;_di_=clf9c2sbrdc11nddrb5m852oivp18hocvo7aglsgdq4pgkigf58g" style="font-weight:normal;text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:#9b9b9b" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://enews-us.chanel.com/pub/cc?_ri_%3DX0Gzc2X%253DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%253DCAWTWBCT%26_ei_%3DERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.%26_di_%3Dclf9c2sbrdc11nddrb5m852oivp18hocvo7aglsgdq4pgkigf58g&amp;source=gmail&amp;ust=1718818826517000&amp;usg=AOvVaw0mrGn4yTHSNT1V85xTEGRG">Watches</a>
                                                </div>
                                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:27px;font-weight:normal;color:#9b9b9b">
                                                <a href="https://enews-us.chanel.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%3DCAWTWCRT&amp;_ei_=ERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.&amp;_di_=l5bovkat11dmjioqt7gdok59af7ftc4m6qtb4r4fk208a63dgq10" style="font-weight:normal;text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:#9b9b9b" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://enews-us.chanel.com/pub/cc?_ri_%3DX0Gzc2X%253DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%253DCAWTWCRT%26_ei_%3DERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.%26_di_%3Dl5bovkat11dmjioqt7gdok59af7ftc4m6qtb4r4fk208a63dgq10&amp;source=gmail&amp;ust=1718818826517000&amp;usg=AOvVaw3EwkhredXtlqBJR81oGZuB">Fine Jewelry</a>
                                                </div>
                                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:27px;font-weight:normal;color:#9b9b9b">
                                                <a href="https://enews-us.chanel.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%3DCAWTWCTT&amp;_ei_=ERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.&amp;_di_=j10klq21pg16rebaderh2nktj80s48i7s2bakdmitbemurkojg7g" style="font-weight:normal;text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:#9b9b9b" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://enews-us.chanel.com/pub/cc?_ri_%3DX0Gzc2X%253DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%253DCAWTWCTT%26_ei_%3DERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.%26_di_%3Dj10klq21pg16rebaderh2nktj80s48i7s2bakdmitbemurkojg7g&amp;source=gmail&amp;ust=1718818826517000&amp;usg=AOvVaw1YuZOBDMzl-juaTIhUOUD9">Fragrance</a>
                                                </div>
                                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:27px;font-weight:normal;color:#9b9b9b">
                                                <a href="https://enews-us.chanel.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%3DCAWTWCWT&amp;_ei_=ERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.&amp;_di_=2nr72bsebq5k667pcob9onr1ltitppbauj2pvut3t1iac3a9gcig" style="font-weight:normal;text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:#9b9b9b" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://enews-us.chanel.com/pub/cc?_ri_%3DX0Gzc2X%253DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%253DCAWTWCWT%26_ei_%3DERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.%26_di_%3D2nr72bsebq5k667pcob9onr1ltitppbauj2pvut3t1iac3a9gcig&amp;source=gmail&amp;ust=1718818826517000&amp;usg=AOvVaw0selJL2QA2W_9R_8_gjlLA">Makeup</a>
                                                </div>
                                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:27px;font-weight:normal;color:#9b9b9b">
                                                <a href="https://enews-us.chanel.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%3DCAWTWCAT&amp;_ei_=ERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.&amp;_di_=bks3qfcak6bvj6s9a56kids31k74b6vqvorck1f19mk5msrb5r2g" style="font-weight:normal;text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:#9b9b9b" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://enews-us.chanel.com/pub/cc?_ri_%3DX0Gzc2X%253DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%253DCAWTWCAT%26_ei_%3DERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.%26_di_%3Dbks3qfcak6bvj6s9a56kids31k74b6vqvorck1f19mk5msrb5r2g&amp;source=gmail&amp;ust=1718818826517000&amp;usg=AOvVaw2cknS4nelHyeV1DVR5aZUQ">Skincare</a>
                                                </div>
                                            </td>
                                            </tr>
                                        </tbody>
                                        </table>
                                        <table border="0" cellspacing="0" cellpadding="0">
                                        <tbody>
                                            <tr>
                                            <td style="font-size:27px;line-height:27px" height="27">&nbsp;</td>
                                            </tr>
                                        </tbody>
                                        </table>
                                    </th>
                                    <th width="120">&nbsp;</th>
                                    <th align="left" valign="top">
                                        <table border="0" cellspacing="0" cellpadding="0">
                                        <tbody>
                                            <tr>
                                            <td align="left" valign="top">
                                                <div style="height:10px">
                                                <img style="display:block;font-size:10px;font-family:Helvetica,Arial,sans-serif;color:#9b9b9b" src="https://ci3.googleusercontent.com/meips/ADKq_NZRUmAUhvJT1zHTySRclw7uSyg1Gau7iaYsF4yxDh8pHzy3uK_x1KoGlrDpIOD1iFHwUWiLWlR3VNd_Gqe_h3b1RU6IN5_jJgueVGUgZA9VFgYUP-Sqvwy0t3K3YLUDgoe52ZoFEqrl8nOOImSOOaVV_RkcqDThk0U-g1MrOBcqjwC4IQGNFlDWNt_OiTq-Yj-SWa72u3I3Rhhf_Vw=s0-d-e1-ft#https://enews-us.chanel.com/assets/responsysimages/chanel/contentlibrary/transactional/orderconfirmation/images/online_services@2x.png" alt="ONLINE SERVICES" width="135" height="10" border="0" class="CToWUd" data-bit="iit">
                                                </div>
                                                <table border="0" cellspacing="0" cellpadding="0">
                                                <tbody>
                                                    <tr>
                                                    <td style="font-size:13px;line-height:13px" height="13">&nbsp;</td>
                                                    </tr>
                                                </tbody>
                                                </table>
                                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:27px;font-weight:normal;color:#9b9b9b">
                                                <a href="https://enews-us.chanel.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%3DCAWTWCCT&amp;_ei_=ERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.&amp;_di_=gsup7al4gaoh4p63jtlevogu9mdi76br4hl04ok3l5i7h9sau040" style="font-weight:normal;text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:#9b9b9b" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://enews-us.chanel.com/pub/cc?_ri_%3DX0Gzc2X%253DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%253DCAWTWCCT%26_ei_%3DERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.%26_di_%3Dgsup7al4gaoh4p63jtlevogu9mdi76br4hl04ok3l5i7h9sau040&amp;source=gmail&amp;ust=1718818826517000&amp;usg=AOvVaw3NpjtsZ53TWZWIokrPIr35">Store Locator</a>
                                                </div>
                                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:27px;font-weight:normal;color:#9b9b9b">
                                                <a href="https://enews-us.chanel.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%3DCAWTWDRT&amp;_ei_=ERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.&amp;_di_=jva3if79k68pcg7cqgcb17ogo9h9k96do26pchojngm8ejhs97j0" style="font-weight:normal;text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:#9b9b9b" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://enews-us.chanel.com/pub/cc?_ri_%3DX0Gzc2X%253DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%253DCAWTWDRT%26_ei_%3DERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.%26_di_%3Djva3if79k68pcg7cqgcb17ogo9h9k96do26pchojngm8ejhs97j0&amp;source=gmail&amp;ust=1718818826517000&amp;usg=AOvVaw1FJWr6a6DKCrIf9vCZL2TX">My Account</a>
                                                </div>
                                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:27px;font-weight:normal;color:#9b9b9b">
                                                <a href="https://enews-us.chanel.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%3DCAWTWDTT&amp;_ei_=ERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.&amp;_di_=p3mui9i5cj52bud5mhe4cdbj9eq59q6pg2plovdtg10lb9kpean0" style="font-weight:normal;text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:#9b9b9b" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://enews-us.chanel.com/pub/cc?_ri_%3DX0Gzc2X%253DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%253DCAWTWDTT%26_ei_%3DERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.%26_di_%3Dp3mui9i5cj52bud5mhe4cdbj9eq59q6pg2plovdtg10lb9kpean0&amp;source=gmail&amp;ust=1718818826517000&amp;usg=AOvVaw0l08TeSW2lHVZKDHRuIqPq">Returns</a>
                                                </div>
                                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:27px;font-weight:normal;color:#9b9b9b">
                                                <a href="https://enews-us.chanel.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%3DCAWTWDWT&amp;_ei_=ERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.&amp;_di_=3ama6n36hg8tdevn80gia02ihse841jb3rlq01nbv4guv7ruu72g" style="font-weight:normal;text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:#9b9b9b" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://enews-us.chanel.com/pub/cc?_ri_%3DX0Gzc2X%253DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%253DCAWTWDWT%26_ei_%3DERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.%26_di_%3D3ama6n36hg8tdevn80gia02ihse841jb3rlq01nbv4guv7ruu72g&amp;source=gmail&amp;ust=1718818826517000&amp;usg=AOvVaw24NgwqbdIUj7J46KjkGPRA">FAQ</a>
                                                </div>
                                            </td>
                                            </tr>
                                        </tbody>
                                        </table>
                                        <table border="0" cellspacing="0" cellpadding="0">
                                        <tbody>
                                            <tr>
                                            <td style="font-size:27px;line-height:27px" height="27">&nbsp;</td>
                                            </tr>
                                        </tbody>
                                        </table>
                                    </th>
                                    </tr>
                                </tbody>
                                </table>
                            </td>
                            </tr>
                            <tr>
                            <td align="center" valign="top">
                                <table border="0" width="560" cellspacing="0" cellpadding="0">
                                <tbody>
                                    <tr>
                                    <td style="line-height:1px;font-size:0px" bgcolor="#333333" height="1">&nbsp;</td>
                                    </tr>
                                </tbody>
                                </table>
                                <table border="0" cellspacing="0" cellpadding="0">
                                <tbody>
                                    <tr>
                                    <td style="font-size:18px;line-height:18px" height="18">&nbsp;</td>
                                    </tr>
                                </tbody>
                                </table>
                                <div style="font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:27px;font-weight:normal;color:#9b9b9b">CHANEL 
                                <a href="#"
                                <a href="#"
                                <a href="https://enews-us.chanel.com/pub/cc?_ri_=X0Gzc2X%3DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%3DCAWTWDAT&amp;_ei_=ERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.&amp;_di_=5msmrdo2lug2fjl27ljt7sbqv7tqh8b6jftn503jd76hmhpe9ds0" style="font-weight:normal;text-decoration:underline;font-family:Arial,Helvetica,sans-serif;color:#9b9b9b" rel="noopener" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://enews-us.chanel.com/pub/cc?_ri_%3DX0Gzc2X%253DAQjkPkSTRQG2lWv8mBYEzfEnbaOzapYJ5TTq2RctPzbygzfow69zerzdkGMzfwwzbTImseu1CFcTJVXtpKX%253DCAWTWDAT%26_ei_%3DERl1MWjBAh1Q-h5-kAR0CZKRYJ9hQTwCLqGDoeqs8MTBMLkukUdxh-bappb5vd1ZjNWVcsuJTx31CWVrlr_5oUH7A2wVzd6lAiRystY5CVaHp5oI2yYyFAIWDi_tVnoMtdgNzM3kGehk7vX5y4N4sxkplCiJzIY4ei3mxNvY00tHmZy0CoKBpD5jRLndtwx-aVKpjZm87hS5LvohnCl_c3dqatSfnTtCILupmRDWfjJhqXRqdJk1La0LzqopNKemifkBr1g_8miIuycx9yMMtQUZoiVRHqq4yDnFsLAa2vXC4aZ6aWIvVe5xVCML90.%26_di_%3D5msmrdo2lug2fjl27ljt7sbqv7tqh8b6jftn503jd76hmhpe9ds0&amp;source=gmail&amp;ust=1718818826517000&amp;usg=AOvVaw0RNdgWZWH88HLCHQR3goaa">Privacy Policy</a>
                                </div>
                                <table border="0" cellspacing="0" cellpadding="0">
                                <tbody>
                                    <tr>
                                    <td style="font-size:27px;line-height:27px" height="27">&nbsp;</td>
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
    """
    
    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
