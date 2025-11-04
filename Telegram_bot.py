import os
import requests
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters

app = Flask(__name__)

# ENV variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
N8N_API_KEY = os.getenv("N8N_API_KEY")
N8N_HOST = os.getenv("N8N_HOST")  # e.g., https://n8n.yourdomain.com

bot = Bot(token=TELEGRAM_TOKEN)

# Gemini API call
def query_gemini(prompt):
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    res = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
        headers=headers,
        json=payload
    )
    return res.json()["candidates"][0]["content"]["parts"][0]["text"]

# Create n8n workflow
def create_n8n_workflow(name, nodes, connections):
    headers = {"Authorization": f"Bearer {N8N_API_KEY}"}
    payload = {
        "name": name,
        "nodes": nodes,
        "connections": connections,
        "active": False
    }
    res = requests.post(f"{N8N_HOST}/api/v1/workflows", json=payload, headers=headers)
    return res.json()["id"]

# Telegram message handler
def handle_message(update: Update, context):
    msg = update.message
    chat_id = msg.chat.id
    text = msg.text

    # Step 1: Ask Gemini to generate workflow structure
    prompt = f"Generate an n8n workflow JSON for this request: {text}. Return only nodes and connections."
    gemini_output = query_gemini(prompt)

    # Step 2: Parse Gemini output (assumes valid JSON)
    try:
        exec_env = {}
        exec(f"workflow = {gemini_output}", {}, exec_env)
        workflow = exec_env["workflow"]
        workflow_id = create_n8n_workflow(name=text[:50], nodes=workflow["nodes"], connections=workflow["connections"])
        link = f"{N8N_HOST}/workflow/{workflow_id}"
        bot.send_message(chat_id, f"✅ Workflow created: {link}")
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Failed to create workflow: {str(e)}")

# Flask route for Telegram webhook
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher = Dispatcher(bot, None, workers=0)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.process_update(update)
    return "ok"

# Health check
@app.route("/")
def index():
    return "Bot is running"

if __name__ == "__main__":
    app.run(debug=True)