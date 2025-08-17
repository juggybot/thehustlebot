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
    msg['From'] = formataddr((f'Lego', sender_email))
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
    "Please enter the order date (12/03):",
    "Please enter the item price (WITHOUT THE $ SIGN):",
    "Please enter the image url (MUST BE FROM LEGO SITE):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira o nome do cliente (Juggy Resells):",
    "Por favor, insira a data do pedido (12/03):",
    "Por favor, insira o preço do item (SEM O SÍMBOLO $):",
    "Por favor, insira a URL da imagem (DEVE SER DO SITE DA LEGO):",
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
    part1 = random.randint(100000000, 999999999)  # Random 9-digit number

    # Combine the parts into order number
    order_number = f"N{part1}"
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
    recipient_email = f'{user_inputs[5]}'
    subject = f"Order #{order_num} confirmed"


    html_template = f"""
            <!DOCTYPE html>
            <html lang="it">
    
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Il tuo ordine su LEGO.it è confermato</title>
                <style>
                    * {{
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}
    
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f5f5f5;
                        color: #333;
                        line-height: 1.4;
                    }}
    
                    .container {{
                        max-width: 640px;
                        margin: 0 auto;
                        background-color: white;
                        position: relative;
                    }}
    
                    /* Watermark overlay */
                    .container::before {{
                        content: '';
                        position: absolute;
                        top: 0;
                        left: 0;
                        right: 0;
                        bottom: 0;
                        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100" viewBox="0 0 200 100"><text x="50%" y="50%" font-family="Arial" font-size="12" fill="%23ddd" text-anchor="middle" dominant-baseline="middle" transform="rotate(-45 100 50)">IT.A-RECEIPTS</text></svg>');
                        background-repeat: repeat;
                        opacity: 0.1;
                        pointer-events: none;
                        z-index: 1;
                    }}
    
                    .content {{
                        position: relative;
                        z-index: 2;
                    }}
    
                    /* Header */
                    .header {{
                        background: linear-gradient(135deg, #FFD700 0%, #FFC107 100%);
                        padding: 20px;
                        text-align: center;
                        position: relative;
                    }}
    
                    .account-link {{
                        position: absolute;
                        top: 8px;
                        right: 15px;
                        font-size: 11px;
                        color: #666;
                        text-decoration: none;
                    }}
    
                    .lego-logo {{
                        display: inline-block;
                        width: 80px;
                        height: 40px;
                        background-image: url('lego.png');
                        background-size: contain;
                        background-repeat: no-repeat;
                        background-position: center;
                    }}
    
                    /* Main content */
                    .main-content {{
                        padding: 25px 30px;
                    }}
    
                    .title {{
                        font-size: 24px;
                        font-weight: bold;
                        margin-bottom: 25px;
                        color: #333;
                    }}
    
                    .greeting {{
                        margin-bottom: 20px;
                        font-size: 14px;
                    }}
    
                    .paragraph {{
                        margin-bottom: 18px;
                        font-size: 14px;
                        line-height: 1.5;
                    }}
    
                    .link {{
                        color: #0066cc;
                        text-decoration: underline;
                    }}
    
                    .contact-info {{
                        margin: 25px 0;
                        font-size: 14px;
                    }}
    
                    .contact-info div {{
                        margin-bottom: 4px;
                    }}
    
                    .account-button {{
                        background-color: #333;
                        color: white;
                        padding: 12px 24px;
                        border: none;
                        border-radius: 4px;
                        font-size: 14px;
                        font-weight: bold;
                        cursor: pointer;
                        display: block;
                        margin: 25px auto;
                        text-transform: uppercase;
                    }}
    
                    /* Order details */
                    .order-details {{
                        margin-top: 35px;
                    }}
    
                    .section-title {{
                        font-size: 20px;
                        font-weight: bold;
                        margin-bottom: 20px;
                    }}
    
                    .detail-row {{
                        display: flex;
                        margin-bottom: 8px;
                        font-size: 14px;
                    }}
    
                    .detail-label {{
                        font-weight: bold;
                        min-width: 120px;
                    }}
    
                    .shipping-address {{
                        margin: 20px 0;
                        font-size: 14px;
                    }}
    
                    .shipping-label {{
                        font-weight: bold;
                        margin-bottom: 8px;
                    }}
    
                    /* Order summary */
                    .order-summary {{
                        margin-top: 30px;
                        border-top: 1px solid #eee;
                        padding-top: 20px;
                    }}
    
                    .summary-row {{
                        display: flex;
                        margin-bottom: 8px;
                        font-size: 14px;
                    }}
    
                    .summary-label {{
                        min-width: 120px;
                        font-weight: bold;
                    }}
    
                    .summary-row.total {{
                        font-weight: bold;
                        border-top: 1px solid #eee;
                        padding-top: 8px;
                        margin-top: 8px;
                    }}
    
                    .summary-row.total .summary-label {{
                        font-weight: bold;
                    }}
    
                    /* Product table */
                    .product-table {{
                        width: 100%;
                        margin-top: 25px;
                        border-collapse: collapse;
                    }}
    
                    .product-table th {{
                        background-color: #f8f8f8;
                        padding: 12px 8px;
                        text-align: left;
                        font-size: 13px;
                        font-weight: bold;
                        border-bottom: 1px solid #ddd;
                    }}
    
                    .product-table td {{
                        padding: 15px 8px;
                        border-bottom: 1px solid #eee;
                        font-size: 14px;
                        vertical-align: top;
                    }}
    
                    .product-image {{
                        width: 60px;
                        height: 40px;
                        object-fit: contain;
                    }}
    
                    .product-name {{
                        font-weight: normal;
                    }}
    
                    .status-row {{
                        margin-top: 15px;
                        font-size: 14px;
                    }}
    
                    .status-label {{
                        font-weight: bold;
                        display: inline-block;
                        width: 60px;
                    }}
    
                    /* Footer */
                    .footer {{
                        margin-top: 40px;
                    }}
    
                    .footer-buttons {{
                        background: linear-gradient(135deg, #FFD700 0%, #FFC107 100%);
                        display: flex;
                        height: 50px;
                    }}
    
                    .footer-button {{
                        flex: 1;
                        background: none;
                        border: none;
                        font-size: 12px;
                        font-weight: bold;
                        color: #333;
                        cursor: pointer;
                        text-transform: uppercase;
                        border-right: 1px solid rgba(0, 0, 0, 0.1);
                    }}
    
                    .footer-button:last-child {{
                        border-right: none;
                    }}
    
                    .footer-button:hover {{
                        background-color: rgba(0, 0, 0, 0.05);
                    }}
    
                    .social-footer {{
                        background-color: #333;
                        padding: 20px;
                        text-align: center;
                    }}
    
                    .social-icons {{
                        display: flex;
                        justify-content: center;
                        gap: 20px;
                    }}
    
                    .social-icon {{
                        width: 40px;
                        height: 40px;
                        background-color: white;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        text-decoration: none;
                        overflow: hidden;
                    }}
    
                    .social-icon img {{
                        width: 24px;
                        height: 24px;
                        object-fit: contain;
                    }}
    
                    /* Bottom text */
                    .bottom-text {{
                        padding: 20px 30px;
                        font-size: 12px;
                        line-height: 1.4;
                        color: #666;
                        background-color: #f8f8f8;
                    }}
    
                    .bottom-text p {{
                        margin-bottom: 12px;
                    }}
    
                    .bottom-text a {{
                        color: #0066cc;
                    }}
    
                    .company-info {{
                        margin-top: 15px;
                        font-size: 11px;
                        color: #999;
                    }}
                </style>
            </head>

        <body>
            <div class="container">
                <div class="content">
                    <div class="header">
                        <a href="#" class="account-link">Visualizza online | IL MIO ACCOUNT</a>
                        <div class="lego-logo"></div>
                    </div>

                    <div class="main-content">
                        <h1 class="title">Il tuo ordine su LEGO.it è confermato.</h1>

                        <div class="greeting">Ciao {user_inputs[0]},</div>

                        <div class="paragraph">
                            Ti ringraziamo per il tuo ordine. È ufficialmente iniziato il conto alla rovescia per iniziare a
                            costruire con i nostri mattoncini!
                        </div>

                        <div class="paragraph">
                            Ecco! un modo semplice per monitorare il tuo ordine, che ti garantirà un'esperienza senza intoppi.
                            Controllare lo stato dell'ordine è davvero facile e puoi farlo in qualsiasi momento. Fai clic sul
                            tuo nome nell'angolo in alto a destra sul sito LEGO per accedere al tuo account LEGO; qui troverai
                            tutti i tuoi ordini. <a href="#" class="link">Se non hai un account, puoi comunque controllare lo
                                stato del tuo ordine nell'apposita pagina, dove troverai tutte le informazioni di cui hai
                                bisogno.</a>
                        </div>

                        <div class="paragraph">
                            Il prossimo aggiornamento sarà un'altra email per comunicarti che la spedizione è in arrivo!
                        </div>

                        <div class="paragraph">
                            Tieni presente che, se hai ordinato più di un articolo, la tua merce potrebbe arrivare in spedizioni
                            separate.
                        </div>

                        <div class="contact-info">
                            <div>Divertiti con i nostri mattoncini!</div>
                            <div>Assistenza clienti LEGO</div>
                        </div>

                        <button class="account-button">ACCEDI AL MIO ACCOUNT</button>

                        <div class="order-details">
                            <h2 class="section-title">Dettagli dell'ordine</h2>

                            <div class="detail-row">
                                <span class="detail-label">Ordine:</span>
                                <span>{order_num}</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Data ordine:</span>
                                <span>{user_inputs[1]}</span>
                            </div>

                            <div class="shipping-address">
                                <div class="shipping-label">Indirizzo di consegna:</div>
                            </div>

                            <div class="order-summary">
                                <div class="summary-row">
                                    <span class="summary-label">SUBTOTALE:</span>
                                    <span>{user_inputs[4]}{user_inputs[2]}</span>
                                </div>
                                <div class="summary-row">
                                    <span class="summary-label">CONSEGNA:</span>
                                    <span>{user_inputs[4]}0.00</span>
                                </div>
                                <div class="summary-row total">
                                    <span class="summary-label">TOTALE ORDINE:</span>
                                    <span>{user_inputs[4]}{user_inputs[2]}</span>
                                </div>
                            </div>

                            <table class="product-table">
                                <thead>
                                    <tr>
                                        <th></th>
                                        <th>Prezzo</th>
                                        <th>Q.TÀ</th>
                                        <th>TOTALE</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>
                                            <div style="display: flex; align-items: center; gap: 15px;">
                                                <img src="{user_inputs[3]}" alt="" class="product-image">
                                                <div class="product-name"></div>
                                            </div>
                                        </td>
                                        <td>{user_inputs[4]}{user_inputs[2]}</td>
                                        <td>1</td>
                                        <td>{user_inputs[4]}{user_inputs[2]}</td>
                                    </tr>
                                </tbody>
                            </table>

                            <div class="status-row">
                                <span class="status-label">Stato:</span>
                                <span>In corso di evasione</span>
                            </div>
                        </div>
                    </div>

                    <div class="footer">
                        <div class="footer-buttons">
                            <button class="footer-button">CONTATTACI</button>
                            <button class="footer-button">IL MIO ACCOUNT</button>
                            <button class="footer-button">STATO DELL'ORDINE</button>
                            <button class="footer-button">RICERCA STORE</button>
                        </div>

                        <div class="social-footer">
                            <div class="social-icons">
                                <a href="#" class="social-icon"><img src="facebook.png" alt="Facebook"></a>
                                <a href="#" class="social-icon"><img src="twitter.png" alt="Twitter"></a>
                                <a href="#" class="social-icon"><img src="youtube.png" alt="YouTube"></a>
                                <a href="#" class="social-icon"><img src="instagram.png" alt="Instagram"></a>
                            </div>
                        </div>
                    </div>

                    <div class="bottom-text">
                        <p>Se l'ordine è stato pagato tramite una carta di credito, una carta di debito, Apple Pay o un buono
                            regalo, sarà autorizzato entro breve tempo. L'addebito effettivo per qualsiasi metodo di pagamento
                            tramite carta avviene solo alla spedizione dell'ordine. Se è stato usato PayPal, l'addebito per
                            l'ordine verrà effettuato quando gli articoli acquistati saranno disponibili nel nostro magazzino.
                        </p>

                        <p>*Tutti gli ordini sono soggetti a controllo, pertanto i tempi di spedizione potrebbero subire
                            variazioni.</p>

                        <p>Questa e-mail è stata inviata a: <a href="#">Giulia Rasi</a></p>

                        <p>Opinioni e feedback sui nostri prodotti e servizi sono sempre benvenuti. Per porre una domanda o
                            inviare un commento, accedere alla pagina <a href="#" class="link">LEGO.com/service</a> e compilare
                            il modulo e-mail appropriato.</p>

                        <div class="company-info">
                            <p>LEGO System A/S LEGO Aastvej 1, Billund, 7190, Denmark</p>
                            <p>LEGO e il logo LEGO sono marchi registrati del LEGO Group. © 2025 The LEGO Group.</p>
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
