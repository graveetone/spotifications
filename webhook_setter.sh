#!/bin/bash

# Usage: ./set_webhook.sh <BOT_TOKEN> <WEBHOOK_URL>
# Example: ./set_webhook.sh 123456:ABC-DEF1234 https://abcd.ngrok-free.app/api/webhook

if [ $# -ne 2 ]; then
  echo "Usage: $0 <BOT_TOKEN> <WEBHOOK_URL>"
  exit 1
fi

BOT_TOKEN=$1
WEBHOOK_URL=$2

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" \
    -d "url=${WEBHOOK_URL}" | jq .
