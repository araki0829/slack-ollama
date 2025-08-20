import os, requests, logging, time, json, re
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

def format_duration(seconds):
    """秒数を 25s や 1m34s の形式に変換"""
    if seconds < 60:
        return f"{int(seconds)}s"
    else:
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes}m{remaining_seconds:02d}s"

def ollama_chat(user_text: str) -> str:
    logger.info(f"Ollama request: {user_text}")
    start_time = time.time()
    
    url = f"{OLLAMA}/api/chat"
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": user_text}],
        "stream": True  # ストリーミング有効
    }
    
    response_text = ""
    
    try:
        with requests.post(url, json=payload, stream=True, timeout=300) as response:
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode('utf-8'))
                        if 'message' in chunk and 'content' in chunk['message']:
                            content = chunk['message']['content']
                            response_text += content
                        
                        if chunk.get('done', False):
                            break
                    except json.JSONDecodeError:
                        continue
    
    finally:
        # 処理時間をログ出力
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"Processing time: {format_duration(duration)}")
    
    response_text = response_text.strip()
    logger.info(f"Ollama response: {response_text}")
    return response_text

# チャンネルでの @メンション
@app.event("app_mention")
def on_mention(body, say):
    logger.info("Mention event received")
    text = body["event"].get("text","")
    # <@UXXXXX> の部分を除去
    clean_text = re.sub(r'<@[A-Z0-9]+>\s*', '', text).strip()
    say(":hourglass_flowing_sand: 考え中…")
    say(ollama_chat(clean_text))

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
