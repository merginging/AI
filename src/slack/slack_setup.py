import os
import sys
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.slack.slack_api import get_slack_access_token

# 사용자 입력할때마다 조회하는 걸로 변경 
USER_EMAIL = "test@gmail.com"
ASSISTANT_NAME = "assistant1"

SLACK_BOT_TOKEN = get_slack_access_token(USER_EMAIL, ASSISTANT_NAME)

def get_bot_user_id():
    url = "https://slack.com/api/auth.test"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, headers=headers)
    data = response.json()

    if data.get("ok"):
        bot_user_id = data.get("user_id")
        print(f" Slack Bot User ID: {bot_user_id}")
        return bot_user_id
    else:
        raise Exception(f" Slack Bot User ID 가져오기 실패 응답: {data}")


def check_bot_in_workspace():
    url = "https://slack.com/api/users.list"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if data.get("ok"):
        bot_members = [user for user in data.get("members", []) if user.get("is_bot")]
        bot_names = [bot.get("name") for bot in bot_members]
        print(f"워크스페이스에 추가된 봇 목록: {bot_names}")
        return bot_names
    else:
        raise Exception(f"워크스페이스 내 봇 조회 실패 응답: {data}")


def invite_bot_to_channel(channel_id):
    bot_user_id = get_bot_user_id()

    url = "https://slack.com/api/conversations.invite"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "channel": channel_id,
        "users": bot_user_id
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()

    if response.status_code == 200 and response_data.get("ok"):
        print(f"Slack Bot이 채널 {channel_id}에 추가되었습니다.")
    else:
        print(f"Bot 채널 초대 실패 응답: {response_data}")



if __name__ == "__main__":
    print("🚀 Slack Setup 스크립트 실행 중...")

    bot_names = check_bot_in_workspace()
    
    print("Slack Setup 완료!")