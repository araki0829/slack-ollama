import os, requests, logging
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
OLLAMA = os.getenv("OLLAMA_URL", "http://localhost:11434").rstrip("/")
MODEL = os.getenv("MODEL", "gpt-oss")

# 起動時の設定確認
logger.info(f"OLLAMA URL: {OLLAMA}")
logger.info(f"MODEL: {MODEL}")
logger.info("Slack Bot starting...")

app = App(token=BOT_TOKEN)

def ollama_chat(user_text: str) -> str:
    logger.info(f"Ollama request: {user_text}")
    url = f"{OLLAMA}/api/chat"
    payload = {
        "model": MODEL,
        "messages": [{"role":"user","content": user_text}],
        "stream": False
    }
    r = requests.post(url, json=payload, timeout=300)
    r.raise_for_status()
    response = r.json()["message"]["content"].strip()
    logger.info(f"Ollama response: {response}")
    return response

# チャンネルでの @メンション
@app.event("app_mention")
def on_mention(body, say):
    logger.info("Mention event received")
    text = body["event"].get("text","")
    say(":hourglass_flowing_sand: 考え中…")
    say(ollama_chat(text))

# DM
@app.message("")
def on_dm(message, say):
    if message.get("channel_type") == "im" and not message.get("bot_id"):
        logger.info("DM received")
        say(":hourglass_flowing_sand: 考え中…")
        say(ollama_chat(message.get("text","")))

if __name__ == "__main__":
    logger.info("Starting Socket Mode Handler...")
    SocketModeHandler(app, APP_TOKEN).start()
