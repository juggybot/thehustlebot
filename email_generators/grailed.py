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
    msg['From'] = formataddr((f'Grailed', sender_email))
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
    "Please enter the image url (MUST BE FROM GOAT SITE):",
    "Please enter the brand name (NIKE):",
    "Please enter the item name (JORDAN 4S):",
    "Please enter the item size (US 10):",
    "Please enter the customer name (JUGGY RESELLS):",
    "Please enter the street address (123 TEST STREET):",
    "Please enter the city (SYDNEY):",
    "Please enter the country (AUSTRALIA):",
    "Please enter the product price (WITHOUT THE $ SIGN):",
    "Please enter the tax cost (WITHOUT THE $ SIGN):",
    "Please enter the order total (WITHOUT THE $ SIGN):",
    "Please enter the currency ($/€/£):",
    "What email address do you want to receive this email (juggyresells@gmail.com):"
]

prompts_pt = [
    "Por favor, insira a URL da imagem (DEVE SER DO SITE GOAT):",
    "Por favor, insira o nome da marca (NIKE):",
    "Por favor, insira o nome do item (JORDAN 4S):",
    "Por favor, insira o tamanho do item (US 10):",
    "Por favor, insira o nome do cliente (JUGGY RESELLS):",
    "Por favor, insira o endereço (123 TEST STREET):",
    "Por favor, insira a cidade (SYDNEY):",
    "Por favor, insira o país (AUSTRÁLIA):",
    "Por favor, insira o preço do produto (SEM O SÍMBOLO $):",
    "Por favor, insira o valor do imposto (SEM O SÍMBOLO $):",
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
    # Generate random order number
    part1 = random.randint(1000000, 9999999)  # Random 8-digit number

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
    recipient_email = f'{user_inputs[12]}'
    subject = f"Thank you for your order {order_num}"

    html_template = f"""
        <html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><style type="text/css">
        /*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3Njc3MvU2NyZWVuc2hvdENvbnRyb2wvX2J1dHRvbnMuc2NzcyIsIndlYnBhY2s6Ly8uL3Njc3MvU2NyZWVuc2hvdENvbnRyb2wuc2NzcyIsIndlYnBhY2s6Ly8uL3Njc3MvU2NyZWVuc2hvdENvbnRyb2wvX25vdGlmaWNhdGlvbnMuc2NzcyIsIndlYnBhY2s6Ly8uL3Njc3MvU2NyZWVuc2hvdENvbnRyb2wvX21vZGFsLnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUEsY0FFQyxpQkFBQSxDQUNBLGlCQUFBLENBQ0EsZUFBQSxDQUNBLFdBQUEsQ0FDQSxZQUFBLENBQ0EsT0FBQSxDQUNBLGNBQUEsQ0FFQSxVQUFBLENBQ0EsV0FBQSxDQUNBLFFBQUEsQ0FDQSxTQUFBLENBQ0EsT0FBQSxDQUNBLFNBQUEsQ0FFQSxVQUFBLENBQ0Esa0JBQUEsQ0FFRyx3QkFBQSxDQUVBLG9CQUNJLG9CQUFBLENBQ0Esd0JBQUEsQ0FHSixvQkFDSSxzQkFBQSxDQUNBLFNBQUEsQ0FRUixjQUVDLGVBQUEsQ0FDQSxXQUFBLENBRUEsNEJBQUEsQ0FDRywwQkFBQSxDQUNBLHFCQUFBLENBRUgseUJBQ0MscUJBQUEsQ0FDQSw0QkFBQSxDQUlGLFlBRUMsc0JBQUEsQ0FDRyxxQkFBQSxDQUVBLHlCQUFBLENBRUgsbUJBRUMscUJBQUEsQ0FDQSxzQkFBQSxDQUVBLHVCQUNDLFVBQUEsQ0FNSCxjQUNDLGVBQUEsQ0FDQSxXQUFBLENBQ0EsY0FBQSxDQUVBLFVBQUEsQ0FFQSxjQUFBLENBR0Esb0JBQUEsQ0FDQSxhQUFBLENBVUEsa0JBRUMsNkJBQUEsQ0FJRSxvQkFDSSxvQkFBQSxDQUNILHdCQUFBLENBSUwsV0FFQyxVQUFBLENBQ0EsY0FBQSxDQUNBLGlCQUFBLENBQ0EsVUFBQSxDQUNBLGNBQUEsQ0FFQSxpQkFDQyxTQUFBLENBSUYsYUFDQyxrQkFBQSxDQUVBLFlBQUEsQ0FFRSxjQUFBLENBQ0EsVUFBQSxDQUlDLG1CQUNJLFNBQUEsQ0FJUiww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SSx3REFBQSxDQUNBLDJCQUFBLENBRUEsVUFBQSxDQUNBLFdBQUEsQ0FFQSxrQkFBQSxDQUNBLGlCQUFBLENBQ0EsY0FBQSxDQUVBLG9CQUFBLENBR0osb0JBRUksb0JBQUEsQ0FDQSxXQUFBLENBRUEsMkJBQ0ksY0FBQSxDQUNBLGVBQUEsQ0FDQSxpQkFBQSxDQUVKLGlDQUNJLGNBQUEsQ0FDQSxtQkFBQSIsInNvdXJjZXNDb250ZW50IjpbIi5zc0J0bkRlZmF1bHQge1xuXHRcblx0cG9zaXRpb246IGFic29sdXRlO1xuXHR6LWluZGV4OiAxMDAwMDAwMDA7XG5cdGJhY2tncm91bmQ6bm9uZTtcblx0Ym9yZGVyOiBub25lO1xuXHRvdXRsaW5lOiBub25lO1xuXHRyaWdodDowO1xuXHRjdXJzb3I6IHBvaW50ZXI7XG5cdFxuXHR3aWR0aDogMjZweDtcblx0aGVpZ2h0OiAyNnB4O1xuXHRtYXJnaW46IDA7Ly81JSA4cHggMDtcblx0cGFkZGluZzowO1xuXHR0b3A6OHB4O1xuXHRyaWdodDo4cHg7XG5cdFxuXHRvcGFjaXR5OiAuNjtcblx0cG9pbnRlci1ldmVudHM6IGFsbDtcblx0Lyp0cmFuc2l0aW9uLWZpbGwtbW9kZTogZm9yd2FyZHM7Ki9cbiAgICB0cmFuc2l0aW9uLWR1cmF0aW9uOiAuMjVzO1xuXG4gICAgJjpob3ZlciB7XG4gICAgICAgIG9wYWNpdHk6IDEgIWltcG9ydGFudDsgXG4gICAgICAgIHRyYW5zaXRpb24tZHVyYXRpb246IC4yNXM7XG4gICAgfVxuXG4gICAgLmZhZGUge1xuICAgICAgICB0cmFuc2l0aW9uLWR1cmF0aW9uOiA1cztcbiAgICAgICAgb3BhY2l0eTogMDtcbiAgICB9XG4gICAgXG4gICAgLypzdmcge1xuICAgICAgICBiYWNrZ3JvdW5kLWNvbG9yOnJlZDtcbiAgICB9Ki9cbn1cblxuLnNzQnRuWW91VHViZSB7XG5cblx0YmFja2dyb3VuZDpub25lO1xuXHRib3JkZXI6IG5vbmU7XG5cdFxuXHRtYXJnaW4tcmlnaHQ6IDIwcHggIWltcG9ydGFudDtcbiAgICBwYWRkaW5nLXRvcDogMHB4ICFpbXBvcnRhbnQ7XG4gICAgd2lkdGg6IDI1cHggIWltcG9ydGFudDtcblxuXHQueXRwLWVtYmVkICYge1xuXHRcdHdpZHRoOiAyMHB4ICFpbXBvcnRhbnQ7XG5cdFx0bWFyZ2luLXJpZ2h0OiAxNXB4ICFpbXBvcnRhbnQ7XG5cdH1cbn1cblxuLnNzQnRuVmltZW8ge1xuXG5cdGhlaWdodDogMnJlbSAhaW1wb3J0YW50O1xuICAgIHdpZHRoOiAycmVtICFpbXBvcnRhbnQ7XG4gICAgLy9wYWRkaW5nOiA2cHggIWltcG9ydGFudDtcbiAgICBtYXJnaW4tdG9wOiA4cHggIWltcG9ydGFudDtcblxuXHRidXR0b24ge1xuXG5cdFx0d2lkdGg6IDEwMCUgIWltcG9ydGFudDtcblx0XHRoZWlnaHQ6IDEwMCUgIWltcG9ydGFudDtcblx0XHRcblx0XHRzdmcge1xuXHRcdFx0d2lkdGg6IDE5cHg7XG5cdFx0fVxuXHR9XG5cbn1cblxuLnNzQnRuTmV0ZmxpeCB7XG5cdGJhY2tncm91bmQ6bm9uZTtcblx0Ym9yZGVyOiBub25lO1xuXHRjdXJzb3I6IHBvaW50ZXI7XG5cblx0d2lkdGg6NHJlbTtcblx0XG5cdG1hcmdpbjogMCAwLjVyZW07XG5cdC8vbWFyZ2luOiAwIDJyZW0gMCA0cmVtO1xuXG5cdGRpc3BsYXk6aW5saW5lLWJsb2NrO1xuXHRmbGV4LXNocmluazogMDtcblx0XG5cdC8vbWFyZ2luLXRvcDotMXJlbTtcblx0Ly9oZWlnaHQ6Mi40cmVtO1xuXHQvL3dpZHRoOiA1MHB4O1xuXHQvL2hlaWdodDogMzVweCAhaW1wb3J0YW50O1xuXHQvL3dpZHRoOiAxMDAlOy8vMy42ZW0gIWltcG9ydGFudDtcbiAgICAvL2hlaWdodDogMTAwJTsvLzEuNmVtICFpbXBvcnRhbnQ7XG5cdC8vcGFkZGluZzowIDAgLjZlbSAwO1xuXG5cdCYgPiBzdmcge1xuXHRcdC8vbWFyZ2luLXRvcDotLjNyZW07XG5cdFx0dHJhbnNmb3JtOnRyYW5zbGF0ZVkoLS4zcmVtKTtcblx0XHQvL3RyYW5zZm9ybTogc2NhbGUoLjUpO1xuXHR9XG4gICAgXG4gICAgJjpob3ZlciB7XG4gICAgICAgIHRyYW5zZm9ybTpzY2FsZSgxLjIpO1xuXHQgICAgdHJhbnNpdGlvbi1kdXJhdGlvbjogLjI1cztcbiAgICB9XG59XG5cbi5zc0J0bkh1bHUge1xuXHRcblx0d2lkdGg6IDI3cHg7XG5cdG1hcmdpbi10b3A6IDRweDtcblx0bWFyZ2luLXJpZ2h0OjEwcHg7XG5cdG9wYWNpdHk6IC43O1xuXHRjdXJzb3I6IHBvaW50ZXI7XG5cdFxuXHQmOmhvdmVyIHtcblx0XHRvcGFjaXR5OiAxO1xuXHR9XG59XG5cbi5zc0J0bkFtYXpvbiB7XG5cdG1hcmdpbi1yaWdodDogMS41dnc7XG4gICAgXG5cdG91dGxpbmU6IG5vbmU7XG5cdFxuICAgY3Vyc29yOiBwb2ludGVyO1xuICAgb3BhY2l0eTogLjg7XG5cbiAgIC8vei1pbmRleDogOTk5OTk5OTk5OTtcblxuICAgICY6aG92ZXIge1xuICAgICAgICBvcGFjaXR5OiAxO1xuICAgIH1cbn1cblxuQG1lZGlhIChtaW4td2lkdGg6IDEyMDBweCkgeyAuc3NCdG5BbWF6b24geyB3aWR0aDogMS42NjY2NjY2NjY2NjY2NjY1dnc7IGhlaWdodDogMS42NjY2NjY2NjY2NjY2NjY1dnc7IH0gfVxuQG1lZGlhIChtYXgtd2lkdGg6IDExOTlweCkgeyAuc3NCdG5BbWF6b24geyB3aWR0aDogMjBweDsgaGVpZ2h0OiAyMHB4OyB9IH1cblxuXG4uc3NCdG5IQk8ge1xuXG4gICAgd2lkdGg6IDQ4cHg7XG4gICAgaGVpZ2h0OiA0OHB4O1xuICAgIHBvc2l0aW9uOiByZWxhdGl2ZTtcbiAgICBvcGFjaXR5OiAwLjc7XG4gICAgY3Vyc29yOiBwb2ludGVyO1xuICAgIGRpc3BsYXk6IGZsZXg7XG4gICAganVzdGlmeS1jb250ZW50OiBjZW50ZXI7XG4gICAgYWxpZ24taXRlbXM6IGNlbnRlcjtcblxuXHQmOmhvdmVyIHtcblx0XHRvcGFjaXR5OiAxO1xuXHRcdHRyYW5zZm9ybTogc2NhbGUoMS4yKTtcblx0fVxuXG5cdHN2ZyB7XG5cdFx0d2lkdGg6IDI0cHg7XG5cdFx0aGVpZ2h0OiAyNHB4O1xuXHR9XG59XG5cbi5zc0J0bkRpc25leSB7XG5cdC8vd2lkdGg6IDI2cHg7XG4gICAgLy9tYXJnaW4tcmlnaHQ6IDEzcHg7XG4gICAgb3BhY2l0eTogLjc7XG5cblx0Jjpob3ZlciB7XG5cdFx0b3BhY2l0eTogMTtcblx0fVxuXG5cdHN2ZyB7XG5cdFx0d2lkdGg6IDI1cHggIWltcG9ydGFudDtcblx0XHRoZWlnaHQ6IDMxcHggIWltcG9ydGFudDtcblx0XHRwYWRkaW5nLXRvcDogNHB4O1xuXHRcdG1hcmdpbi1yaWdodDogN3B4O1xuXHR9XG59XG5cbi5zc0J0bkFwcGxlIHtcblx0Ly93aWR0aDogMjZweDtcbiAgICAvL21hcmdpbi1yaWdodDogMTNweDtcblxuXHRjdXJzb3I6IHBvaW50ZXI7XG5cblxuICAgIG9wYWNpdHk6IC43O1xuXG5cdCY6aG92ZXIge1xuXHRcdG9wYWNpdHk6IDE7XG5cdH1cblxuXHRzdmcge1xuXHRcdHdpZHRoOiAyMnB4ICFpbXBvcnRhbnQ7XG5cdFx0aGVpZ2h0OiAyMnB4ICFpbXBvcnRhbnQ7XG5cdFx0bWFyZ2luLXJpZ2h0OiAycHggIWltcG9ydGFudDtcblx0fVxufSIsIkBpbXBvcnQgXCJTY3JlZW5zaG90Q29udHJvbC9idXR0b25zXCI7XG5cbmJvZHkge1xuXG5cdCNzc1RlbXBIb2xkZXIge1xuXHRcdHBvc2l0aW9uOmZpeGVkO1xuXHRcdHotaW5kZXg6MTAwMDAwMDAwMDAwMDtcblx0XHR3aWR0aDoxMDAlO1xuXHRcdGhlaWdodDoxMDAlO1xuXHRcdHRvcDowO1xuXHRcdHBvaW50ZXItZXZlbnRzOiBub25lO1xuXG5cdFx0dmlkZW8ge1xuXHRcdFx0d2lkdGg6YXV0byAhaW1wb3J0YW50O1xuXHRcdFx0aGVpZ2h0OmF1dG8gIWltcG9ydGFudDtcblx0XHRcdG1heC13aWR0aDoxMDAlICFpbXBvcnRhbnQ7XG5cdFx0XHRtYXgtaGVpZ2h0OiAxMDAlICFpbXBvcnRhbnQ7XG5cdFx0XHR0b3A6IDAgIWltcG9ydGFudDtcblx0XHRcdGxlZnQ6IDAgIWltcG9ydGFudDtcblx0XHRcdHRyYW5zZm9ybTogbm9uZSAhaW1wb3J0YW50O1xuXHRcdH1cblx0fVxuXG5cdCYuc3NUYWtlU2NyZWVuc2hvdCB7XG5cdFx0XG5cdFx0LnNzRWxlbWVudCB7XG5cdFx0XHR6LWluZGV4OiAxMDAwMDAwMDAwMDAgIWltcG9ydGFudDtcblx0XHR9XG5cdFx0XG5cdFx0Ji5zc05ldGZsaXgge1xuXHRcblx0XHRcdFtkYXRhLXVpYT12aWRlby1jYW52YXNdIHtcblx0XHRcdFx0ei1pbmRleDogMTAwMDAwMDA7XG5cdFx0XHR9XG5cdFx0XHRcblx0XHRcdHZpZGVvIHtcblx0XHRcdFx0YmFja2dyb3VuZC1jb2xvcjogIzAwMDAwMDtcblx0XHRcdFx0Ly9oZWlnaHQ6IGF1dG8gIWltcG9ydGFudDtcblx0XHRcdH1cblxuXHRcdFx0LnBsYXllci10aW1lZHRleHQge1xuXG5cdFx0XHRcdGRpc3BsYXk6bm9uZSAhaW1wb3J0YW50O1xuXHRcdFx0fVx0XHRcdFxuXG5cdFx0XHQmLnNob3dTdWJzIHtcblx0XHRcdFx0XG5cdFx0XHRcdC5wbGF5ZXItdGltZWR0ZXh0IHtcblxuXHRcdFx0XHRcdGRpc3BsYXk6IGJsb2NrICFpbXBvcnRhbnQ7XG5cdFx0XHRcdFx0Ly9ib3R0b206IDEwJSAhaW1wb3J0YW50O1xuXHRcdFx0XHR9XG5cdFx0XHR9XG5cdFx0fVxuXG5cdFx0Ji5zc0FtYXpvbiB7XG5cblx0XHRcdC5zY2FsaW5nVmlkZW9Db250YWluZXIge1xuXHRcdFx0XHR6LWluZGV4OiA5OTk5OTk5OSAhaW1wb3J0YW50O1xuXHRcdFx0fVxuXHRcdH1cblxuXHRcdCYuc3NEaXNuZXkge1xuXG5cdFx0XHQuYnRtLW1lZGlhLW92ZXJsYXlzLWNvbnRhaW5lciB7XG5cdFx0XHRcdGRpc3BsYXk6bm9uZTtcblx0XHRcdH1cblxuXHRcdFx0LmRzcy1obHMtc3VidGl0bGUtb3ZlcmxheSB7XG5cdFx0XHRcdGRpc3BsYXk6IG5vbmU7XG5cdFx0XHR9XG5cblx0XHRcdCYuc2hvd1N1YnMge1xuXHRcdFx0XHRcblx0XHRcdFx0LmRzcy1obHMtc3VidGl0bGUtb3ZlcmxheSB7XG5cdFx0XHRcdFx0ZGlzcGxheTogYmxvY2s7XG5cdFx0XHRcdH1cblx0XHRcdH1cblx0XHR9XG5cblx0XHQmLnNzSHVsdSB7XG5cdFx0XHQuQ29udGVudFBsYXllcl9fY29udGVudEFyZWEge1xuXHRcdFx0XHR6LWluZGV4OiAxMDAwMDAwMDAwMDtcbiAgICBcdFx0XHRwb3NpdGlvbjogcmVsYXRpdmU7XG5cdFx0XHR9XG5cblx0XHRcdC5DbG9zZWRDYXB0aW9uIHtcblx0XHRcdFx0ZGlzcGxheTpub25lO1xuXHRcdFx0fVxuXG5cdFx0XHQmLnNob3dTdWJzIHtcblx0XHRcdFx0LkNsb3NlZENhcHRpb24ge1xuXHRcdFx0XHRcdGRpc3BsYXk6YmxvY2s7XG5cblx0XHRcdFx0XHQuQ2xvc2VkQ2FwdGlvbl9fb3V0YmFuZCB7XG5cdFx0XHRcdFx0XHRib3R0b206IDMwcHggIWltcG9ydGFudDtcblx0XHRcdFx0XHR9XG5cdFx0XHRcdH1cblx0XHRcdH1cblx0XHR9XG5cblx0XHQmLnNzSEJPIHtcblxuXHRcdFx0dmlkZW8ge1xuXHRcdFx0XHR6LWluZGV4OiA5OTk5OTk5OTtcblx0XHRcdH1cblxuXHRcdFx0KjpoYXModmlkZW8pIHtcblx0XHRcdFx0ei1pbmRleDogOTk5OTk5OTk7XG5cdFx0XHR9XG5cblx0XHR9XG5cblx0XHQmLnNzWW91dHViZSB7XG5cblx0XHRcdC5odG1sNS12aWRlby1jb250YWluZXIsIC55dHAtY2FwdGlvbi13aW5kb3ctY29udGFpbmVyIHtcblx0XHRcdFx0ei1pbmRleDogOTk5OTk5OTk5ICFpbXBvcnRhbnQ7XG5cdFx0XHR9XG5cdFx0fVxuXG5cdFx0Ji5zc0FwcGxlIHtcblx0XHRcdCNhcHBsZS1tdXNpYy12aWRlby1wbGF5ZXIge1xuXHRcdFx0XHR6LWluZGV4OiA5OTk5OTk5OTkgIWltcG9ydGFudDtcblx0XHRcdH1cblxuXHRcdFx0LnNjcmltIHtcblx0XHRcdFx0ZGlzcGxheTpub25lO1xuXHRcdFx0fVxuXHRcdH1cblx0fVxuXG5cdC5zc1dyYXBwZXIge1xuXHRcdG92ZXJmbG93OiBoaWRkZW47XG5cdH1cblxuXHRAaW1wb3J0IFwiU2NyZWVuc2hvdENvbnRyb2wvbm90aWZpY2F0aW9uc1wiO1xuXHRAaW1wb3J0IFwiU2NyZWVuc2hvdENvbnRyb2wvbW9kYWxcIjtcbn0iLCIuc3NOb3RpZmljYXRpb24ge1xuXG4gICAgZGlzcGxheTogZmxleDtcbiAgICB3aWR0aDogMTAwJTtcbiAgICBoZWlnaHQ6IDRyZW07XG4gICAganVzdGlmeS1jb250ZW50OiBjZW50ZXI7XG4gICAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbiAgICBwb3NpdGlvbjogZml4ZWQ7XG4gICAgei1pbmRleDogMTAwMDAwMDAwMDtcbiAgICB0b3A6LTRyZW07XG5cbiAgICBhbmltYXRpb24tbmFtZTogbm90aWZpY2F0aW9uO1xuICAgIGFuaW1hdGlvbi1kdXJhdGlvbjogMnM7XG4gICAgYW5pbWF0aW9uLWl0ZXJhdGlvbi1jb3VudDogMTtcblxuICAgIEBrZXlmcmFtZXMgbm90aWZpY2F0aW9uIHtcbiAgICAgICAgMCUge3RvcDogLTRyZW07fVxuICAgICAgICAyNSUge3RvcDogM3JlbTt9XG4gICAgICAgIDg1JSB7dG9wOiAzcmVtO31cbiAgICB9XG5cbiAgICAuc3NOQ29udGVudCB7XG4gICAgICAgIC8vY29udGVudDogJ1NjcmVlbnNob3QgY29waWVkIHRvIGNsaXBib2FyZCEnO1xuICAgICAgICBwb3NpdGlvbjogYWJzb2x1dGU7XG4gICAgICAgIHotaW5kZXg6IDEwMDAwMDAwMDA7XG4gICAgICAgIHBhZGRpbmc6IC43NXJlbSAxLjI1ZW07XG4gICAgICAgIG1hcmdpbi1ib3R0b206IDFlbTtcbiAgICAgICAgYm9yZGVyOiAxcHggc29saWQgdHJhbnNwYXJlbnQ7XG4gICAgICAgIGJvcmRlci1yYWRpdXM6IC4yNWVtO1xuICAgICAgICBmb250LXNpemU6IDEycHg7XG4gICAgICAgIGhlaWdodDogZml0LWNvbnRlbnQ7XG4gICAgICAgIHRvcDowO1xuXG4gICAgICAgICYuc3VjY2VzcyB7XG4gICAgICAgICAgICBiYWNrZ3JvdW5kLWNvbG9yOiAjZDRlZGRhO1xuICAgICAgICAgICAgYm9yZGVyLWNvbG9yOiAjYzNlNmNiO1xuICAgICAgICAgICAgY29sb3I6ICMxNTU3MjQ7XG4gICAgICAgIH1cbiAgICBcbiAgICAgICAgJi5mYWlsIHtcbiAgICAgICAgICAgIGJhY2tncm91bmQtY29sb3I6ICNlZGQ0ZDQ7XG4gICAgICAgICAgICBib3JkZXItY29sb3I6ICNlNmMzYzM7XG4gICAgICAgICAgICBjb2xvcjogI2I2MjQyNDtcbiAgICAgICAgfVxuICAgIH1cblxufSIsIi5zc01vZGFsIHtcblxuICAgIGRpc3BsYXk6IG5vbmU7XG5cbiAgICAmLnZpc2libGUge1xuICAgICAgICBkaXNwbGF5OmJsb2NrO1xuICAgIH1cblxuICAgIHBvc2l0aW9uOiBmaXhlZDtcbiAgICB6LWluZGV4OiAxMDAwMDAwMDA7XG5cbiAgICByaWdodDoyMHB4O1xuICAgIFxuICAgIG9wYWNpdHk6IDA7XG5cbiAgICBiYWNrZ3JvdW5kLWNvbG9yOiNmZmZlZmE7XG4gICAgYm9yZGVyLXJhZGl1czogM3B4O1xuXG4gICAgcGFkZGluZzogMjVweDtcblxuICAgIGNvbG9yOiAjNTI1MjUyO1xuICAgIGZvbnQtZmFtaWx5OiBtdWxpLCBzYW5zLXNlcmlmO1xuICAgIFxuICAgICoge1xuICAgICAgICB2ZXJ0aWNhbC1hbGlnbjogbWlkZGxlO1xuICAgICAgICBsaW5lLWhlaWdodDogbm9ybWFsO1xuICAgICAgICBmb250LXdlaWdodDogbm9ybWFsO1xuICAgIH1cblxuICAgIGJveC1zaGFkb3c6IDBweCA0cHggOHB4IDBweCByZ2JhKDAsIDAsIDAsIDAuMTUpO1xuXG4gICAgYW5pbWF0aW9uLW5hbWU6IGFuaW1hdGVPbjtcbiAgICBhbmltYXRpb24tZHVyYXRpb246IC4ycztcbiAgICBhbmltYXRpb24tZmlsbC1tb2RlOiBmb3J3YXJkcztcblxuICAgIEBrZXlmcmFtZXMgYW5pbWF0ZU9uIHtcbiAgICAgICAgZnJvbSB7XG4gICAgICAgICAgICBvcGFjaXR5OiAwO1xuICAgICAgICAgICAgdG9wOiAwcHg7XG4gICAgICAgIH1cbiAgICAgICAgdG8ge1xuICAgICAgICAgICAgb3BhY2l0eTogMTtcbiAgICAgICAgICAgIHRvcDogMjBweDtcbiAgICAgICAgfVxuICAgIH1cblxuICAgIC5jbG9zZSB7XG4gICAgICAgIHBvc2l0aW9uOiBhYnNvbHV0ZTtcbiAgICAgICAgcmlnaHQ6IDEwcHg7XG4gICAgICAgIHRvcDogMTBweDtcbiAgICAgICAgY3Vyc29yOiBwb2ludGVyO1xuICAgICAgICBvcGFjaXR5OiAuNTtcblxuICAgICAgICBiYWNrZ3JvdW5kLWltYWdlOiB1cmwoJy4uL2ltYWdlcy9jbG9zZS5zdmcnKTtcblxuICAgICAgICB3aWR0aDoxMHB4O1xuICAgICAgICBoZWlnaHQ6MTBweDtcblxuICAgIH1cblxuICAgIC5zc0J1dHRvbnMge1xuXG4gICAgICAgIG1hcmdpbi10b3A6IDI1cHg7XG4gICAgICAgIHRleHQtYWxpZ246IHJpZ2h0O1xuXG4gICAgICAgIC5zc0J1dHRvbiwgYSAuc3NCdXR0b24ge1xuICAgICAgICAgICAgZGlzcGxheTppbmxpbmUtYmxvY2s7XG5cbiAgICAgICAgICAgIGhlaWdodDoyMHB4O1xuICAgICAgICAgICAgXG4gICAgICAgICAgICBwYWRkaW5nOjNweCAxMnB4IDNweDtcbiAgICAgICAgICAgIG1hcmdpbi1sZWZ0OiAxNHB4O1xuICAgICAgICAgICAgXG4gICAgICAgICAgICBib3JkZXItcmFkaXVzOiA0cHg7XG4gICAgICAgICAgICBib3gtc2hhZG93OiAwcHggNHB4IDhweCAwcHggcmdiYSgwLCAwLCAwLCAwLjE1KTtcbiAgICAgICAgICAgIGJhY2tncm91bmQtY29sb3I6ICNGRkZGRkY7XG4gICAgICAgICAgICBcbiAgICAgICAgICAgIGZvbnQtc2l6ZTogMTJweDtcbiAgICAgICAgICAgIGNvbG9yOiAjNTI1MjUyO1xuICAgICAgICAgICAgbGluZS1oZWlnaHQ6IDIwcHg7XG4gICAgICAgICAgICBmb250LXdlaWdodDogbm9ybWFsO1xuICAgIFxuICAgICAgICAgICAgY3Vyc29yOiBwb2ludGVyO1xuXG4gICAgICAgICAgICB0ZXh0LWRlY29yYXRpb246IG5vbmU7XG5cbiAgICAgICAgICAgIC5lbW9qaSB7XG4gICAgICAgICAgICAgICAgZm9udC1zaXplOiAxNXB4O1xuICAgICAgICAgICAgICAgIHZlcnRpY2FsLWFsaWduOiBib3R0b207XG4gICAgICAgICAgICB9XG4gICAgXG4gICAgICAgICAgICAmLmJsdWUge1xuICAgICAgICAgICAgICAgIGJhY2tncm91bmQtY29sb3I6ICMxOWFjZWY7XG4gICAgICAgICAgICAgICAgY29sb3I6ICNGRkZGRkY7XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICAuaWNvbiB7XG4gICAgICAgIGJhY2tncm91bmQtaW1hZ2U6IHVybCgnLi4vaW1hZ2VzL2ljb25CbHVlLnN2ZycpO1xuICAgICAgICBiYWNrZ3JvdW5kLXJlcGVhdDogbm8tcmVwZWF0O1xuXG4gICAgICAgIHdpZHRoOjMwcHg7XG4gICAgICAgIGhlaWdodDozMHB4O1xuXG4gICAgICAgIHZlcnRpY2FsLWFsaWduOiB0b3A7XG4gICAgICAgIG1hcmdpbi1yaWdodDogMjJweDtcbiAgICAgICAgbWFyZ2luLXRvcDoycHg7XG5cbiAgICAgICAgZGlzcGxheTppbmxpbmUtYmxvY2s7XG4gICAgfVxuXG4gICAgLmJvZHkge1xuXG4gICAgICAgIGRpc3BsYXk6aW5saW5lLWJsb2NrO1xuICAgICAgICB3aWR0aDozMTVweDtcblxuICAgICAgICAudGl0bGUge1xuICAgICAgICAgICAgZm9udC1zaXplOiAxNXB4O1xuICAgICAgICAgICAgZm9udC13ZWlnaHQ6IDYwMDtcbiAgICAgICAgICAgIG1hcmdpbi1ib3R0b206IDdweDtcbiAgICAgICAgfVxuICAgICAgICAuZGVzY3JpcHRpb24ge1xuICAgICAgICAgICAgZm9udC1zaXplOiAxM3B4O1xuICAgICAgICAgICAgZm9udC13ZWlnaHQ6IGxpZ2h0ZXI7XG4gICAgICAgIH1cbiAgICB9XG5cbn0iXSwic291cmNlUm9vdCI6IiJ9 */</style></head><body>
        <div style="font-family:Helvetica;font-size:12px;font-style:normal;font-variant-caps:normal;font-weight:400;letter-spacing:normal;text-align:start;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px;text-decoration:none">
        <table id="m_5714130242240911517bgwrapper" border="0" width="100%" cellspacing="0" cellpadding="0" align="center" style="border-collapse:collapse">
            <tbody>
            <tr>
                <td style="border-collapse:collapse">
                <table id="m_5714130242240911517wrapper" border="0" width="100%" cellspacing="0" cellpadding="0" align="center" style="border-collapse:collapse">
                    <tbody>
                    <tr>
                        <td align="center" valign="top" style="border-collapse:collapse">
                        <table id="m_5714130242240911517grailed-header-logo" border="0" width="620" cellspacing="0" cellpadding="0" align="center" style="border-collapse:collapse;width:620px">
                            <tbody>
                            <tr>
                                <td height="40" style="border-collapse:collapse;height:40px"></td>
                            </tr>
                            <tr>
                                <td align="center" valign="top" style="border-collapse:collapse">
                                <a href="https://www.grailed.com/?utm_campaign=buyer_purchase_confirmation_auto_refund&amp;utm_medium=email&amp;utm_source=mailgun-grailed&amp;utm_term=system_email" rel="noopener" style="color:rgb(57,57,58);text-decoration:none;border-collapse:collapse" target="_blank">
                                    <img src="https://ci3.googleusercontent.com/meips/ADKq_Nb5nIV2vNywfISlqgN1MpPc7kUvJUKdEIm1bhCMHn0nuZ6X7XdTQopQfbg6jpKVXhCxLZDiKzigkHt8CMKXDmRGx1GqNlTORvoCk5mv2USHMgbikK9eXVc=s0-d-e1-ft#https://ds6dnbdlsnuyn.cloudfront.net/emails/logo-no-whitespace.jpg" alt="GRAILED" width="225" border="0" style="display: block; font-family: Arial, sans-serif; font-size: 22px; font-weight: bold; letter-spacing: 2px; border: 0px; outline: none;">
                                </a>
                                </td>
                            </tr>
                            <tr>
                                <td height="30" style="border-collapse:collapse;height:30px"></td>
                            </tr>
                            </tbody>
                        </table>
                        </td>
                    </tr>
                    <tr>
                        <td style="border-collapse:collapse">
                        <table align="center" style="border-collapse:collapse;width:600px;text-align:center;font-family:Helvetica,Arial,sans-serif">
                            <tbody>
                            <tr>
                                <td style="border-collapse:collapse">
                                <div style="text-align:center;font-size:24px;margin-top:20px;margin-bottom:15px;font-family:TimesNewRoman">Congrats on Your Purchase!</div>
                                </td>
                            </tr>
                            <tr style="min-width:320px;max-width:600px">
                                <td style="border-collapse:collapse">
                                <hr style="margin-bottom:15px;margin-top:35px;border:1px solid rgb(225,225,225)">
                                <table style="border-collapse:collapse;width:598px;margin-bottom:20px">
                                    <tbody>
                                    <tr>
                                        <td style="border-collapse:collapse">
                                        <table align="left" style="border-collapse:collapse;width:200px;min-width:200px">
                                            <tbody>
                                            <tr>
                                                <td style="border-collapse:collapse;padding:10px;vertical-align:top">
                                                <a href="" rel="noopener" style="color:rgb(57,57,58);text-decoration:underline;border-collapse:collapse" target="_blank">
                                                    <img src="{user_inputs[0]}" style="width: 120px; max-width: 120px; border: 0px; outline: none;">
                                                </a>
                                                </td>
                                            </tr>
                                            </tbody>
                                        </table>
                                        <table style="border-collapse:collapse;width:357.594px;min-width:200px">
                                            <tbody>
                                            <tr>
                                                <td style="border-collapse:collapse">
                                                <table align="left" style="border-collapse:collapse;width:355.594px">
                                                    <tbody>
                                                    <tr>
                                                        <td style="border-collapse:collapse;padding:10px;text-align:left;vertical-align:top">
                                                        <div style="font-family:TimesNewRoman">ITEM</div>
                                                        <hr style="border:1px solid rgb(225,225,225)">
                                                        <div style="margin:0px;font-size:14px;line-height:25px;min-width:180px;padding:0px">
                                                            <strong>{user_inputs[1]}</strong>
                                                        </div>
                                                        <div style="margin:0px;font-size:14px;line-height:25px;padding:0px">{user_inputs[2]}</div>
                                                        <div style="margin:0px;font-size:14px;line-height:25px;padding:0px">{user_inputs[3]}</div>
                                                        </td>
                                                    </tr>
                                                    </tbody>
                                                </table>
                                                <table align="left" style="border-collapse:collapse;width:355.594px">
                                                    <tbody>
                                                    <tr>
                                                        <td style="border-collapse:collapse;padding:10px;text-align:left;vertical-align:top">
                                                        <div style="font-family:TimesNewRoman">SHIPPING DETAILS</div>
                                                        <hr style="border:1px solid rgb(225,225,225)">
                                                        <div style="margin:0px;font-size:14px;line-height:25px;padding:0px">
                                                            <strong>{user_inputs[4]}</strong>
                                                        </div>
                                                        <div style="margin:0px;font-size:14px;line-height:25px;padding:0px">{user_inputs[5]}</div>
                                                        <p style="margin:0px;font-size:14px;line-height:25px;padding:0px"></p>
                                                        <div style="margin:0px;font-size:14px;line-height:25px;padding:0px">{user_inputs[6]}</div>
                                                        <div style="margin:0px;font-size:14px;line-height:25px;padding:0px">{user_inputs[7]}</div>
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
                            <tr style="min-width:320px;max-width:600px">
                                <td style="border-collapse:collapse">
                                <table style="border-collapse:collapse;width:598px">
                                    <tbody>
                                    <tr>
                                        <td style="border-collapse:collapse">
                                        <table align="left" style="border-collapse:collapse;width:196.672px">
                                            <tbody>
                                            <tr>
                                                <td style="border-collapse:collapse;padding:10px;text-align:left;vertical-align:top"></td>
                                            </tr>
                                            </tbody>
                                        </table>
                                        <table align="left" style="border-collapse:collapse;width:357.594px;min-width:180px">
                                            <tbody>
                                            <tr>
                                                <td style="border-collapse:collapse;padding:10px;text-align:left;vertical-align:top">
                                                <div style="font-family:TimesNewRoman">PAYMENT</div>
                                                <hr style="border:1px solid rgb(225,225,225)">
                                                <table align="left" style="border-collapse:collapse;width:337.594px;min-width:30px">
                                                    <tbody>
                                                    <tr>
                                                        <td style="border-collapse:collapse;text-align:left;vertical-align:top;width:234.328px">
                                                        <div style="font-size:14px;line-height:25px;margin:0px;padding:0px">Sold Price</div>
                                                        </td>
                                                        <td style="border-collapse:collapse;text-align:right;vertical-align:top;width:99.2812px">
                                                        <div style="font-size:14px;line-height:25px;margin:0px;padding:0px">{user_inputs[11]}{user_inputs[8]}</div>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="border-collapse:collapse;text-align:left;vertical-align:top;width:234.328px">
                                                        <div style="font-size:14px;line-height:25px;margin:0px;padding:0px">Tax</div>
                                                        </td>
                                                        <td style="border-collapse:collapse;text-align:right;vertical-align:top;width:99.2812px">
                                                        <div style="font-size:14px;line-height:25px;margin:0px;padding:0px">{user_inputs[11]}{user_inputs[9]}</div>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="border-collapse:collapse;text-align:left;vertical-align:top;width:234.328px">
                                                        <div style="font-size:12px;line-height:10px;margin:0px;padding:0px">
                                                            <a href="https://help.grailed.com/hc/en-us/articles/9226890136347?utm_campaign=buyer_purchase_confirmation_auto_refund&amp;utm_medium=email&amp;utm_source=mailgun-grailed&amp;utm_term=system_email" rel="noopener" style="color:rgb(115,115,115);text-decoration:underline;border-collapse:collapse" target="_blank">Learn more</a>
                                                        </div>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="border-collapse:collapse;padding-top:10px;text-align:left;vertical-align:top;width:234.328px">
                                                        <div style="font-size:18px;line-height:25px;margin:0px;padding:0px">
                                                            <strong>TOTAL</strong>
                                                        </div>
                                                        </td>
                                                        <td style="border-collapse:collapse;padding-top:10px;text-align:right;vertical-align:top;width:99.2812px">
                                                        <div style="font-size:18px;line-height:25px;margin:0px;padding:0px">
                                                            <strong>€{user_inputs[10]}</strong>
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
                                    </tbody>
                                </table>
                                </td>
                            </tr>
                                <tr>
                                <td style="border-collapse:collapse">
                                <hr style="border:1px solid rgb(225,225,225);margin-bottom:30px">
                                <div style="margin:0px auto;font-family:TimesNewRoman;font-size:24px">Estimated Shipping Time</div>
                                <div style="margin:1.5rem 0px">
                                    <strong>International</strong>
                                    <span></span>: 3-6 weeks (or longer)
                                </div>
                                <div style="font-size:18px;margin-bottom:30px;text-align:left">Sellers have up to 7 days to ship the item and provide tracking. We'll send you an email as soon as the item is on its way. If you have any questions, you can reach out to the seller. <span></span>
                                    <br>
                                    <br>If you don't receive tracking within 7 days, Grailed is here to help. We'll cancel the order and issue you a full refund. <span></span>
                                    <a href="https://help.grailed.com/hc/en-us/articles/1260807541829?utm_campaign=buyer_purchase_confirmation_auto_refund&amp;utm_medium=email&amp;utm_source=mailgun-grailed&amp;utm_term=system_email" rel="noopener" style="text-decoration:underline;border-collapse:collapse" target="_blank">Learn more.</a>
                                </div>
                                </td>
                            </tr>
                            <tr>
                                <td style="border-collapse:collapse">
                                <hr style="border:1px solid rgb(225,225,225);margin-bottom:30px">
                                <table align="center" style="border-collapse:collapse;text-align:center;font-family:Helvetica,Arial,sans-serif;margin-top:10px">
                                    <tbody>
                                    <tr>
                                        <td style="border-collapse:collapse">
                                        <div style="font-size:24px;line-height:25px;padding-bottom:15px;font-family:TimesNewRoman">More Questions?</div>
                                        <div>Reach out to us anytime, we're here to help.</div>
                                        <div style="padding-top:30px">
                                            <a href="https://help.grailed.com/hc/en-us?utm_campaign=buyer_purchase_confirmation_auto_refund&amp;utm_medium=email&amp;utm_source=mailgun-grailed&amp;utm_term=system_email" rel="noopener" style="color:rgb(255,255,255);text-decoration:none;border-collapse:collapse;background-color:rgb(0,0,0);border-radius:2px;font-size:16px;line-height:32px;padding:12px 25px;font-family:Arial;width:156px;max-width:186px" target="_blank">Contact Support</a>
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
                        <td align="center" valign="top" style="border-collapse:collapse">
                        <table border="0" width="620" cellspacing="0" cellpadding="0" align="center" bgcolor="#f9f9f9" style="border-collapse:collapse;width:626px">
                            <tbody>
                            <tr>
                                <td width="10" style="border-collapse:collapse"></td>
                                <td align="center" valign="top" style="border-collapse:collapse">
                                <table border="0" width="600" cellspacing="0" cellpadding="0" align="center" style="border-collapse:collapse;width:600px">
                                    <tbody>
                                    <tr>
                                        <td height="28" style="border-collapse:collapse;height:28px"></td>
                                    </tr>
                                    <tr>
                                        <td align="center" valign="top" style="border-collapse:collapse;font-size:13px;line-height:22px;color:rgb(152,152,152);text-decoration:none">To make sure you don't miss out on the newest heat and latest price drops, add <span></span>
                                        <br>
                                        <a href="mailto:no-reply@grailed.com" style="color:rgb(34,34,34);text-decoration:none;border-collapse:collapse;font-size:13px;line-height:22px" target="_blank">no-reply@grailed.com</a>
                                        <span></span>to your address book. <span></span>
                                        <br>You can unsubscribe from receiving these emails by <span></span>
                                        <a href="https://www.grailed.com/users/notifications?utm_campaign=buyer_purchase_confirmation_auto_refund&amp;utm_medium=email&amp;utm_source=mailgun-grailed&amp;utm_term=system_email" rel="noopener" style="color:rgb(152,152,152);text-decoration:underline;border-collapse:collapse;font-size:13px;line-height:22px" target="_blank">editing your Grailed notification settings</a>. <span></span>
                                        <br>
                                        <br>All Grailed services are subject to our <span></span>
                                        <span style="border-collapse:collapse;text-decoration:underline">
                                            <a href="https://www.grailed.com/about/privacy?utm_campaign=buyer_purchase_confirmation_auto_refund&amp;utm_medium=email&amp;utm_source=mailgun-grailed&amp;utm_term=system_email" rel="noopener" style="color:rgb(152,152,152);text-decoration:underline;border-collapse:collapse;font-size:13px;line-height:22px" target="_blank">Privacy &amp; Cookies Policy</a>
                                            <span></span>
                                        </span>and <span></span>
                                        <span style="border-collapse:collapse;text-decoration:underline">
                                            <a href="https://www.grailed.com/about/terms?utm_campaign=buyer_purchase_confirmation_auto_refund&amp;utm_medium=email&amp;utm_source=mailgun-grailed&amp;utm_term=system_email" rel="noopener" style="color:rgb(152,152,152);text-decoration:underline;border-collapse:collapse;font-size:13px;line-height:22px" target="_blank">Terms &amp; Conditions</a>
                                            <span></span>
                                        </span>. <span></span>
                                        <br>By using our services you agree to these. <span></span>
                                        <br>
                                        <br>These services are operated and provided by Grailed Inc. <span></span>
                                        <br>
                                        <br>131 Spring St, Suite 601, New York, NY 10012 <span></span>
                                        <br>
                                        <br>
                                        <a href="https://www.grailed.com/?utm_campaign=buyer_purchase_confirmation_auto_refund&amp;utm_medium=email&amp;utm_source=mailgun-grailed&amp;utm_term=system_email" rel="noopener" style="color:rgb(152,152,152);text-decoration:none;border-collapse:collapse;font-size:13px;line-height:22px" target="_blank">www.grailed.com</a>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td height="28" style="border-collapse:collapse;height:28px"></td>
                                    </tr>
                                    </tbody>
                                </table>
                                </td>
                                <td width="10" style="border-collapse:collapse"></td>
                            </tr>
                            </tbody>
                        </table>
                        </td>
                    </tr>
                    </tbody>
                </table>
                <div style="white-space:nowrap;font-style:normal;font-variant-caps:normal;font-weight:normal;font-stretch:normal;font-size:20px;line-height:normal;font-family:courier;color:rgb(255,255,255)"></div>
                </td>
            </tr>
            </tbody>
        </table>
        <img src="./grailed_files/eJwVyzsOwyAMANDTlDGyjfl44DAGmxSpaaV06u2bvP15w1yQoxBLsCbZQcJqBERIKFAZuGxFevHUNdvoqLE_GPZT18ttG58jPNsA1aisKB1Fq0-qSSiNZDqj4QxnM_-u_T1O_937uPZ9_574JUg" alt="" width="1px" height="1px" style="border: 0px; outline: none;" bm45c2vki="">
        </div>



        <br>



        </body></html>
    """

    send_email(sender_email, sender_password, recipient_email, subject, html_template)
    return ConversationHandler.END

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You took too long to respond! Please try again.")
    return ConversationHandler.END
