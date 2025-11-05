import os
import requests
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

app = Flask(__name__)

# ENV variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
N8N_API_KEY = os.getenv("N8N_API_KEY")
N8N_HOST = os.getenv("N8N_HOST")  # e.g., https://n8n.yourdomain.com

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
    headers = {"X-N8N-API-KEY": N8N_API_KEY}
    payload = {
        "name": name,
        "nodes": nodes,
        "connections": connections,
        "active": False
    }
    res = requests.post(f"{N8N_HOST}/api/v1/workflows", json=payload, headers=headers)
    return res.json()["id"]

# Telegram message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    chat_id = msg.chat.id
    text = msg.text
    print("🔔 Message received:", update.message.text)

    prompt = f"Generate an n8n workflow JSON for this request: {text}. Return only nodes and connections."
    gemini_output = query_gemini(prompt)

    try:
        exec_env = {}
        exec(f"workflow = {gemini_output}", {}, exec_env)
        workflow = exec_env["workflow"]
        workflow_id = create_n8n_workflow(
            name=text[:50],
            nodes=workflow["nodes"],
            connections=workflow["connections"]
        )
        link = f"{N8N_HOST}/workflow/{workflow_id}"
        await context.bot.send_message(chat_id=chat_id, text=f"✅ Workflow created: {link}")
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"⚠️ Failed to create workflow: {str(e)}")

# Create the Telegram application
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Flask route for Telegram webhook
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    print("📬 Webhook triggered")
    update = Update.de_json(request.get_json(force=True), application.bot)
    import threading
    threading.Thread(target=application.update_queue.put_nowait, args=(update,)).start()
    return "ok"

# Health check
@app.route("/")
def index():
    return "Bot is running"

if __name__ == "__main__":
    app.run(debug=True)