import os
import time
import asyncio
import re
import pandas as pd
import requests
import threading
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from imapclient import IMAPClient
import pypdf

load_dotenv()

GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
VFS_URL = os.getenv("VFS_URL")
# ===== FUNÇÃO TELEGRAM =====
def enviar_telegram(dados):
    mensagem = f"""📢 <b>BOOKING BOT</b>
📄 <b>Reservation confirmation</b>

🛫 <b>Rota:</b> Angola → Portugal
📄 <b>Categoria:</b> Schengen (Curta Duração)
👤 <b>Aplicante:</b> {dados['nome']}
📑 <b>Ref VFS:</b> {dados['ref']}
🏦 <b>ENTIDADE:</b> {dados['entidade']}
🔢 <b>REFERÊNCIA:</b> {dados['ref']}
💰 <b>VALOR:</b> {dados['valor']}

⏳ <b>Pague o mais rápido possível para confirmar o agendamento!</b>
⚡ Fonte: VFS GLOBAL"""

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem, "parse_mode": "HTML"}
    requests.post(url, data=payload)
    print(f"[TELEGRAM] Enviado para {dados['nome']}")

# ===== PARSER PDF =====
def extrair_dados_pdf(pdf_path):
    reader = pypdf.PdfReader(pdf_path)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text() + "\n"

    ref = re.search(r'Reference\s*No[:\s]+(\d+)', texto, re.I)
    entidade = re.search(r'Entity\s*Code[:\s]+(\d+)', texto, re.I)
    valor = re.search(r'Total\s*Amount[:\s]+([\d\s,\.]+AOA)', texto, re.I)
    nome = re.search(r'Applicant\s*Name[:\s]+([A-Z\s]+)', texto, re.I)

    return {
        "nome
