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
    msg['From'] = formataddr((f'Best Buy', sender_email))
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
    "Please enter the order date (10/10/2025):",
    "Please enter the image url (jpg, jpeg, png):",
    "Please enter the product name (AirPods Max - Space Grey):",
    "Please enter the product price (WITHOUT THE $):",
    "Please enter the product SKU (6447385):",
    "Please enter the customer name (Juggy Resells):",
    "Please enter the street address (511 Jonathan Station Street):",
    "Please enter the suburb/city (Howellborough):",
    "Please enter the postcode (1234):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]
prompts_pt = [
    "Por favor, insira o primeiro nome do cliente (Juggy):",
    "Por favor, insira a data do pedido (10/10/2025):",
    "Por favor, insira a URL da imagem (jpg, jpeg, png):",
    "Por favor, insira o nome do produto (AirPods Max - Cinza Espacial):",
    "Por favor, insira o preço do produto (SEM O SINAL $):",
    "Por favor, insira o SKU do produto (6447385):",
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira o endereço (511 Jonathan Station Street):",
    "Por favor, insira o bairro/cidade (Howellborough):",
    "Por favor, insira o código postal (1234):",
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
    part1 = random.randint(1000000000, 9999999999)  # Random 10-digit number

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
    sender_email = EMAIL
    sender_password = PASSWORD
    recipient_email = f'{user_inputs[11]}'
    subject = f"We're processing your order {order_num}" if lang == "en" else f"Estamos processando seu pedido {order_num}"
    html_template = f"""
    <!DOCTYPE html>
        <html lang="en">

        <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />

        </head>

        <body>
        <div><br></div>
        <div dir="auto">
        <div class="gmail_quote">
            <u></u>















            <div style="background-color:rgb(255,255,255)">
            <div style="background-color:rgb(255,255,255)">

                <div> </div>
                <div> </div>
                <div> </div>
                <div> </div>

                <div> </div>

                <div> </div>
                <div> </div>
                <div> </div>

                <div> </div>
                <div>


                </div>


                <div style="margin:0px auto;max-width:600px">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%">
                    <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:20px 0px;text-align:center">



                        <div style="margin:0px auto;max-width:600px">
                            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                            style="width:100%">
                            <tbody>
                                <tr>
                                <td
                                    style="border:1px solid rgb(197,203,213);direction:ltr;font-size:0px;padding:0px 27px 24px 23px;text-align:center">

                                    <div class="m_-3651230328894493609mj-column-per-100"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">
                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                        style="vertical-align:top" width="100%">
                                        <tbody>
                                        <tr>
                                            <td align="left" style="font-size:0px;padding:41px 0px 0px;word-break:break-word">
                                            <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                style="border-collapse:collapse;border-spacing:0px">
                                                <tbody>
                                                <tr>
                                                    <td style="width:72px">
                                                    <img height="42"
                                                        src="https://images.bbycastatic.ca/sf/images/emails/logos/bby-logo-primary3x-successgreen-150-75.png"
                                                        style="border: 0px; display: block; outline: currentcolor; text-decoration: none; height: 42px; width: 100%; font-size: 13px;"
                                                        width="72">
                                                    </td>
                                                </tr>
                                                </tbody>
                                            </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left" style="font-size:0px;padding:32px 0px 0px;word-break:break-word">
                                            <div
                                                style="font-family:Arial,Helvetica,sans-serif;font-size:24px;font-weight:bold;letter-spacing:0px;line-height:32px;text-align:left;color:rgb(29,37,44)">
                                                Hi {user_inputs[0]},</div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left" style="font-size:0px;padding:0px;word-break:break-word">
                                            <div
                                                style="font-family:Arial,Helvetica,sans-serif;font-size:24px;font-weight:bold;letter-spacing:0px;line-height:32px;text-align:left;color:rgb(29,37,44)">
                                                We have good news! Your order has shipped and is on its way to you.</div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left" style="font-size:0px;padding:24px 0px 0px;word-break:break-word">
                                            <div
                                                style="font-family:Arial,Helvetica,sans-serif;font-size:14px;letter-spacing:0px;line-height:20px;text-align:left;color:rgb(29,37,44)">
                                                <table style="font-family:Arial,Helvetica,sans-serif">
                                                <colgroup style="font-family:Arial,Helvetica,sans-serif">
                                                    <col style="font-family:Arial,Helvetica,sans-serif">
                                                </colgroup>
                                                <tbody style="font-family:Arial,Helvetica,sans-serif">
                                                    <tr style="font-family:Arial,Helvetica,sans-serif">
                                                    <td
                                                        style="font-weight:bold;padding-right:69px;font-family:Arial,Helvetica,sans-serif;color:rgba(0,0,0,0.87)">
                                                        Order Date</td>
                                                    <td
                                                        style="font-family:Arial;font-size:14px;line-height:20px;color:rgb(29,37,44)">
                                                        {user_inputs[1]} at 12:31:57 PT</td>
                                                    </tr>
                                                    <tr style="font-family:Arial,Helvetica,sans-serif">
                                                    <td
                                                        style="font-weight:bold;padding-right:69px;font-family:Arial,Helvetica,sans-serif;color:rgba(0,0,0,0.87)">
                                                        Order Number</td>
                                                    <td
                                                        style="font-family:Arial;font-size:14px;line-height:20px;color:rgb(29,37,44)">
                                                        {order_num}</td>
                                                    </tr>
                                                    <tr style="font-family:Arial,Helvetica,sans-serif">
                                                    <td
                                                        style="font-weight:bold;padding-right:69px;vertical-align:top;font-family:Arial,Helvetica,sans-serif;color:rgba(0,0,0,0.87)">
                                                        Tracking Number</td>
                                                    <td
                                                        style="font-family:Arial;font-size:14px;line-height:20px;color:rgb(29,37,44)">
                                                        <div style="font-family:Arial">0010073001</div>
                                                    </td>
                                                    </tr>

                                                </tbody>
                                                </table>
                                            </div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left" style="font-size:0px;padding:24px 0px 0px;word-break:break-word">
                                            <div
                                                style="font-family:Arial,Helvetica,sans-serif;font-size:14px;letter-spacing:0px;line-height:20px;text-align:left;color:rgb(29,37,44)">
                                                You can track your package online using the button below. Tracking will become
                                                available after 24 hours.</div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left" style="font-size:0px;padding:24px 0px 0px;word-break:break-word">
                                            <div
                                                style="font-family:Arial,Helvetica,sans-serif;font-size:14px;letter-spacing:0px;line-height:20px;text-align:left;color:rgb(29,37,44)">
                                                <table id="m_-3651230328894493609tracking-table"
                                                style="font-family:Arial,Helvetica,sans-serif">
                                                <tbody style="font-family:Arial,Helvetica,sans-serif">
                                                    <tr style="font-family:Arial,Helvetica,sans-serif">
                                                    <td style="padding-top:8px;font-family:Arial,Helvetica,sans-serif">
                                                        <img
                                                        src="https://www.bestbuy.ca/bestbuy/trackingimg/tforce?tracking_numbers=0010073082&amp;service=ST&amp;dzip=N1R0A2&amp;locale=en_ca"
                                                        width="360" height="150"
                                                        style="padding-bottom: 24px; font-family: Arial, Helvetica, sans-serif;">
                                                        <div style="font-family:Arial,Helvetica,sans-serif"><a
                                                            href="https://click.communications.bestbuypromotions.ca/?qs=b230495b93adeeabea471047b5f2a71f4f6917a25d917bb0afe15f476c510549fb530691d1c19a56e915c5f3f54d01b2cc40075271580ee053bbfa1067e74615"
                                                            target="_blank"
                                                            style="font-family:Arial,Helvetica,sans-serif"><button
                                                            style="background-color:#0046be;padding:16px 32px;text-align:center;font-family:Arial,Helvetica,sans-serif;font-size:14px;color:white;border:none;font-weight:bold">Track
                                                            My Package</button></a></div>
                                                    </td>
                                                    </tr>
                                                </tbody>
                                                </table>
                                            </div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left" style="font-size:0px;padding:24px 0px 0px;word-break:break-word">
                                            <div
                                                style="font-family:Arial,Helvetica,sans-serif;font-size:14px;letter-spacing:0px;line-height:20px;text-align:left;color:rgb(29,37,44)">
                                                We’ll send your receipt in our next email. You can also download your receipt
                                                from your <a
                                                style="text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:rgb(0,70,190)"
                                                href="https://click.communications.bestbuypromotions.ca/?qs=ba36279ee7169d6e6edd2b13538bb052615bb0825676eb2559bed3af74f8b5d7c5b53b815732dcb1c187738afa625ef975aecfe1d38f27cc"
                                                target="_blank">order details</a> page when it becomes available.</div>
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



                        <div style="margin:0px auto;max-width:600px">
                            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                            style="width:100%">
                            <tbody>
                                <tr>
                                <td
                                    style="border-bottom-width:1px;border-bottom-style:solid;border-left-width:1px;border-left-style:solid;border-right-width:1px;border-right-style:solid;direction:ltr;font-size:0px;padding:0px 27px 24px 23px;text-align:center;border-right-color:rgb(197,203,213);border-bottom-color:rgb(197,203,213);border-left-color:rgb(197,203,213)">

                                    <div class="m_-3651230328894493609mj-column-per-100"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">
                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                        style="vertical-align:top" width="100%">
                                        <tbody>
                                        <tr>
                                            <td align="left" style="font-size:0px;padding:24px 0px 0px;word-break:break-word">
                                            <div
                                                style="font-family:Arial,Helvetica,sans-serif;font-size:16px;font-weight:bold;letter-spacing:0px;line-height:20px;text-align:left;color:rgb(29,37,44)">
                                                Package Summary</div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left"
                                            style="font-size:0px;padding:8px 0px 0px 23px;word-break:break-word">
                                            <div
                                                style="font-family:Ubuntu,Helvetica,Arial,sans-serif;font-size:13px;line-height:1;text-align:left;color:rgb(0,0,0)">
                                                <table id="m_-3651230328894493609items-table"
                                                style="font-family:Ubuntu,Helvetica,Arial,sans-serif">
                                                <colgroup style="font-family:Ubuntu,Helvetica,Arial,sans-serif">
                                                    <col width="165px" style="font-family:Ubuntu,Helvetica,Arial,sans-serif">
                                                </colgroup>
                                                <tbody style="font-family:Ubuntu,Helvetica,Arial,sans-serif">
                                                    <tr style="font-family:Ubuntu,Helvetica,Arial,sans-serif">
                                                    <td
                                                        style="padding-right:69px;height:96px;width:96px;padding-top:24px;font-family:Ubuntu,Helvetica,Arial,sans-serif">
                                                        <img
                                                        style="margin: 0px; border: 0px; padding: 0px; display: block; font-family: Ubuntu, Helvetica, Arial, sans-serif; max-width: 96px; max-height: 96px;"
                                                        src="{user_inputs[2]}"></td>
                                                    <td
                                                        style="padding-top:24px;font-family:Ubuntu,Helvetica,Arial,sans-serif">
                                                        <div class="m_-3651230328894493609product-name-text"
                                                        style="font-family:Ubuntu,Helvetica,Arial,sans-serif">{user_inputs[3]}</div>
                                                        <div style="font-family:Ubuntu,Helvetica,Arial,sans-serif">
                                                        <table class="m_-3651230328894493609product-price-text"
                                                            style="padding-top:4px;font-family:Ubuntu,Helvetica,Arial,sans-serif">
                                                            <tbody style="font-family:Ubuntu,Helvetica,Arial,sans-serif">
                                                            <tr style="font-family:Ubuntu,Helvetica,Arial,sans-serif">
                                                                <td style="font-family:Ubuntu,Helvetica,Arial,sans-serif">{user_inputs[10]}{user_inputs[4]}
                                                                </td>
                                                            </tr>
                                                            </tbody>
                                                        </table>
                                                        </div>
                                                        <div class="m_-3651230328894493609product-qty-sku-text"
                                                        style="padding-top:4px;font-family:Ubuntu,Helvetica,Arial,sans-serif">
                                                        <b style="font-family:Ubuntu,Helvetica,Arial,sans-serif">Quantity:
                                                        </b>1</div>
                                                        <div class="m_-3651230328894493609product-qty-sku-text"
                                                        style="padding-top:4px;font-family:Ubuntu,Helvetica,Arial,sans-serif">
                                                        <b style="font-family:Ubuntu,Helvetica,Arial,sans-serif">Web Code:
                                                        </b>{user_inputs[5]}</div>
                                                    </td>
                                                    </tr>
                                                </tbody>
                                                </table>
                                            </div>
                                            </td>
                                        </tr>

                                        <tr>
                                            <td style="font-size:0px;padding:24px 0px 0px;word-break:break-word">
                                            <p
                                                style="border-top-width:1px;border-top-style:solid;margin:0px auto;width:100%;border-top-color:rgb(197,203,213)">
                                            </p>

                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left" style="font-size:0px;padding:24px 0px 0px;word-break:break-word">
                                            <div
                                                style="font-family:Arial,Helvetica,sans-serif;font-size:14px;letter-spacing:0px;line-height:20px;text-align:left;color:rgb(29,37,44)">
                                                <b style="font-family:Arial,Helvetica,sans-serif">Shipping Address</b>
                                                <p style="font-family:Arial,Helvetica,sans-serif">{user_inputs[6]}<br>{user_inputs[7]}<br>{user_inputs[8]}<br>{user_inputs[9]} US</p>
                                            </div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left" style="font-size:0px;padding:24px 0px 0px;word-break:break-word">
                                            <div
                                                style="font-family:Arial,Helvetica,sans-serif;font-size:14px;letter-spacing:0px;line-height:20px;text-align:left;color:rgb(29,37,44)">
                                                <b style="font-family:Arial,Helvetica,sans-serif">Your order has been shipped
                                                with</b>
                                                <p style="font-family:Arial,Helvetica,sans-serif">FedEx</p>
                                                <p style="font-family:Arial,Helvetica,sans-serif">Your order has been set up
                                                for the fastest delivery option. Make sure you&#39;re available to receive
                                                your delivery, as your package will be returned to Best Buy after 2 delivery
                                                attempts. <a
                                                    style="text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:rgb(0,70,190)"
                                                    href="https://click.communications.bestbuypromotions.ca/?qs=515ab2c94605835e1b25adc992780d8f8907ce4b3e8d0f1aa55df8857aebcdbbc277504c842406f4a6f1aff553980b96149e25730952a17d"
                                                    target="_blank">See what you need to know</a></p>
                                            </div>
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



                        <div style="margin:0px auto;max-width:600px">
                            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                            style="width:100%">
                            <tbody>
                                <tr>
                                <td
                                    style="border-left-width:1px;border-left-style:solid;border-right-width:1px;border-right-style:solid;direction:ltr;font-size:0px;padding:0px 27px 11px 23px;text-align:center;border-right-color:rgb(197,203,213);border-left-color:rgb(197,203,213)">

                                    <div class="m_-3651230328894493609mj-column-per-100"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">
                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                        style="vertical-align:top" width="100%">
                                        <tbody>
                                        <tr>
                                            <td align="left" style="font-size:0px;padding:24px 0px 0px;word-break:break-word">
                                            <div
                                                style="font-family:Arial,Helvetica,sans-serif;font-size:14px;letter-spacing:0px;line-height:20px;text-align:left;color:rgb(29,37,44)">
                                                <b style="font-family:Arial,Helvetica,sans-serif">FAQs</b>
                                                <p style="font-family:Arial,Helvetica,sans-serif"><b
                                                    style="font-family:Arial,Helvetica,sans-serif">What about my items that
                                                    haven&#39;t shipped yet?</b></p>
                                                <p style="font-family:Arial,Helvetica,sans-serif">For faster delivery
                                                we&#39;ll ship any additional item(s) to you as they become available, at no
                                                extra cost. You&#39;ll only be charged for an item when it ships and
                                                you&#39;ll get an email (like this one) each time.</p>
                                            </div>
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



                        <div style="background:0% repeat rgb(244,246,249);margin:0px auto;max-width:600px">
                            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                            style="background:0% repeat rgb(244,246,249);width:100%">
                            <tbody>
                                <tr>
                                <td
                                    style="border-bottom-width:1px;border-bottom-style:solid;border-left-width:1px;border-left-style:solid;border-right-width:1px;border-right-style:solid;direction:ltr;font-size:0px;padding:0px 24px 24px;text-align:center;border-right-color:rgb(197,203,213);border-bottom-color:rgb(197,203,213);border-left-color:rgb(197,203,213)">

                                    <div class="m_-3651230328894493609mj-column-per-100"
                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">
                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                        style="vertical-align:top" width="100%">
                                        <tbody>
                                        <tr>
                                            <td align="left" style="font-size:0px;padding:24px 0px 0px;word-break:break-word">
                                            <div
                                                style="font-family:Arial,Helvetica,sans-serif;font-size:16px;font-weight:bold;letter-spacing:0px;line-height:20px;text-align:left;color:rgb(0,0,0)">
                                                Thank you for shopping at BestBuy.com</div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left"
                                            style="font-size:0px;padding:8px 30px 0px 0px;word-break:break-word">
                                            <div
                                                style="font-family:Arial,Helvetica,sans-serif;font-size:12px;letter-spacing:0px;line-height:20px;text-align:left;color:rgba(0,0,0,0.87)">
                                                This email was sent from an outgoing-only address that cannot accept incoming
                                                emails. If you still have questions, please visit our <a
                                                style="text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:rgb(0,70,190)"
                                                href="https://click.communications.bestbuypromotions.ca/?qs=9466ad1948b7b1c8b243ea76db25a392aaf4f53e7edaa2f0e652329a976e9d136921c30b8fe5d3cf072d685f8e3de3b2caf49ed4bacf3e83"
                                                target="_blank">help centre</a> for more information. <p
                                                style="font-family:Arial,Helvetica,sans-serif"><b
                                                    style="font-family:Arial,Helvetica,sans-serif">Promotional Emails:</b> As
                                                a customer of Best Buy Canada, we may send you promotional emails. If you do
                                                not wish to receive promotional emails from Best Buy Canada, please feel
                                                free to
                                                <a style="text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:rgb(0,70,190)"
                                                    href="https://click.communications.bestbuypromotions.ca/?qs=00f38c2cae0cfd4e9ba0ecf675476fe51f3f54c2b3826832995e5d4b7ad6f2a4c3ea10d72efb5cc0d19027c20115d50c76e64927bcd7a916"
                                                    target="_blank">unsubscribe</a>.
                                                </p>
                                            </div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="font-size:0px;padding:12px 0px 24px;word-break:break-word">
                                            <p
                                                style="border-top-width:1px;border-top-style:solid;margin:0px auto;width:100%;border-top-color:rgb(224,224,224)">
                                            </p>

                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left" style="font-size:0px;padding:0px;word-break:break-word">
                                            <div
                                                style="font-family:Arial,Helvetica,sans-serif;font-size:10px;letter-spacing:0px;line-height:16px;text-align:left;color:rgba(0,0,0,0.54)">
                                                © Best Buy United States Ltd. <a
                                                href="https://www.google.com/maps/search/8800+Glenlyon+Pkwy.,+Burnaby+BC+V5J+5M3?entry=gmail&amp;source=g"
                                                style="font-family:Arial,Helvetica,sans-serif">8800 Glenlyon Pkwy., Burnaby
                                                BC V5J 5M3</a></div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left" style="font-size:0px;padding:4px 0px 0px;word-break:break-word">
                                            <div
                                                style="font-family:Arial,Helvetica,sans-serif;font-size:10px;letter-spacing:0px;line-height:24px;text-align:left;color:rgba(0,0,0,0.87)">
                                                <a style="text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:rgb(29,37,44)"
                                                href="https://click.communications.bestbuypromotions.ca/?qs=9466ad1948b7b1c8b243ea76db25a392aaf4f53e7edaa2f0e652329a976e9d136921c30b8fe5d3cf072d685f8e3de3b2caf49ed4bacf3e83"
                                                target="_blank">Contact Us</a> | <a
                                                style="text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:rgb(29,37,44)"
                                                href="https://click.communications.bestbuypromotions.ca/?qs=d26cb16fee1d2d57fc52f44541264b0c18d4a9373fe94e5458b8af2d9fabd86e3fba49ee6310ee2c794909f93f17f7f768e9d46dc057afb6"
                                                target="_blank">Returns &amp; Exchanges</a> |
                                                <a style="text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:rgb(29,37,44)"
                                                href="https://click.communications.bestbuypromotions.ca/?qs=5f6a9b022222a06b1af230a98de2b41fda99ba6d7d5adadbe5859fd8209363ced05d90f4d3c4a3b9d7e971db70c380651faed1344c108bf0"
                                                target="_blank">Privacy Policy</a> |
                                                <a style="text-decoration:none;font-family:Arial,Helvetica,sans-serif;color:rgb(29,37,44)"
                                                href="https://click.communications.bestbuypromotions.ca/?qs=d5c4d74310e2e655b7b975c2edf8cc2518078f80ca03ed90af4fef745c7ff53b470fd0cda8cd3cf1aee8bf024ab258aa000058fc153abdda"
                                                target="_blank">Terms &amp; Conditions</a>
                                            </div>
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

                        </td>
                    </tr>
                    </tbody>
                </table>
                </div>

                <img
                src="https://click.communications.bestbuypromotions.ca/open.aspx?ffcb10-fec913737d64067f-fe55127577610d7a7316-fe9a13727464057c7c-ff951777-fe6217727c60067d7612-fec716777066067b&amp;d=70181&amp;bmt=0"
                width="1" height="1" alt="">

            </div>
            </div>




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
