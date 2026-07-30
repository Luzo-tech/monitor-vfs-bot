from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import os
import time

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot VFS Online!"

@app.route("/check")
def check_vfs():
    # Aqui vai a lógica do teu bot pra verificar vagas
    return jsonify({"status": "ok", "message": "Verificação rodando"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
