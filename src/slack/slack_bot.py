import os
from flask import Flask, request, jsonify
from src.db.faiss_db import similarity_search
from src.llm.model import process_with_rag
from src.slack.slack_api import get_slack_access_token
from src.slack.slack_utils import send_slack_message
from src.slack.slack_setup import invite_bot_to_channel

# 이메일이랑 어시스턴트 이름도 api로 받아오도록 로직 다시 짜기 
user_email = "test@gmail.com"
assistant_name = "assistant1"
SLACK_BOT_TOKEN = get_slack_access_token(user_email, assistant_name)

# 특정 Slack 채널에 Bot 추가 (자동 실행)
SLACK_CHANNEL_ID = "" # 채널 id도 받아오도록 짜기 
invite_bot_to_channel(SLACK_CHANNEL_ID)

app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    print(f"📩 수신된 Slack 이벤트: {data}")

    if "event" in data:
        event = data["event"]

        if event.get("type") == "message" and "subtype" not in event:
            user_id = event.get("user")
            channel_id = event.get("channel")
            question = event.get("text")

            print(f"📩 질문 수신: {question}")

            # 🔍 FAISS 벡터 스토어 검색
            retrieved_docs = similarity_search(question)
            combined_context = "\n\n".join(doc.page_content for doc in retrieved_docs) if retrieved_docs else "검색된 정보가 없습니다."

            # 🧠 RAG 모델 
            response = process_with_rag(question, combined_context)

            # 🔁 Slack에 응답 전송
            send_slack_message(channel_id, response)

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    print("🚀 Flask Slack Bot 실행 중...")
    app.run(port=5000, debug=True)