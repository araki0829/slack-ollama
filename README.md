# Slack-Ollama Bot

SlackでローカルのOllamaモデルと会話できるBot。

## 使用モデル

このBotは**gpt-oss-20B**モデルを使用。
- パラメータ数: 20.9B
- 量子化: MXFP4
- ローカル実行でApple SiliconのGPU最適化

## 機能

- Slackでの@メンション対応
- ダイレクトメッセージ対応
- ローカルOllamaサーバーとの連携
- 処理時間の表示
- Docker Composeでの簡単デプロイ

## セットアップ

### 1. 環境変数設定

`.env`ファイルを作成：

```env
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_APP_TOKEN=xapp-your-app-token-here
OLLAMA_URL=http://localhost:11434
MODEL=gpt-oss
```

### 2. Slackアプリ設定

- Event Subscriptions: ON
- Subscribe to bot events: `app_mentions:read`, `message.im`
- OAuth Scopes: `app_mentions:read`, `channels:history`, `chat:write`, `im:history`, `im:read`
- Socket Mode: Enable

### 3. 起動方法

#### Docker Compose（推奨）

```bash
docker-compose up -d --build
```

#### ローカル実行

```bash
pip install -r requirements.txt
python main.py
```

## 使い方

- **チャンネル**: `@BotName こんにちは`
- **DM**: 直接メッセージを送信

## 要件

- Python 3.12+
- ローカルでOllamaサーバーが動作していること
- Slackアプリの適切な設定
