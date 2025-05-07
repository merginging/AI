# 슬랙에서 봇 작동 함수 
# 구현 덜 함 
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import requests
from flask import Flask, request, jsonify
from src.db.faiss_db import similarity_search
from src.llm.model import process_with_rag
from src.slack.slack_api import get_slack_access_token

app = Flask(__name__)


@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    if "event" in data:
        event = data["event"]

        if event.get("type") == "message" and "subtype" not in event:
            user_id = event.get("user")  # 메시지를 보낸 사용자 ID
            channel_id = event.get("channel")  # DM 채널 ID 
            question = event.get("text")  

            print(f"📩 질문 수신 (DM): {question}")

            slack_token = get_slack_access_token("test@gmail.com", "assistant1")

            #  DM 채널이 맞는지 확인
            if not channel_id.startswith("D"):
                print("메시지가 DM이 아님")
                return jsonify({"status": "ignored"})

            # FAISS 벡터 스토어 검색
            retrieved_docs = similarity_search(question)
            combined_context = "\n\n".join(doc.page_content for doc in retrieved_docs) if retrieved_docs else "검색된 정보가 없습니다."

            # RAG 모델 실행
            response = process_with_rag(question, combined_context)

            # Slack에 DM으로 응답 전송
            send_slack_dm(slack_token, channel_id, response)

    return jsonify({"status": "ok"})



def send_slack_dm(slack_token, channel_id, message):
    SLACK_DM_API = "https://slack.com/api/chat.postMessage"

    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }

    data = {
        "channel": channel_id,
        "text": message
    }

    response = requests.post(SLACK_DM_API, headers=headers, json=data)

    if response.status_code == 200:
        print(f"Slack 메시지 전송 성공: {message}")
    else:
        print(f"Slack 메시지 전송 실패: {response.text}")


if __name__ == "__main__":
    print("🚀 Flask Slack Bot 실행 중...")
    app.run(port=5000)