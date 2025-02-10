import requests
from src.slack.slack_api import get_slack_access_token

# 태스트 정보
user_email = "test@gmail.com"
assistant_name = "assistant1"

# 백엔드 API를 통해 Access Token 조회 
SLACK_BOT_TOKEN = get_slack_access_token(user_email, assistant_name)

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
        print(f"✅ Slack Bot User ID: {bot_user_id}")
        return bot_user_id
    else:
        raise Exception(f"❌ Slack Bot User ID 가져오기 실패 응답: {data}")


# 채널에 봇 추가 함수 
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
        print(f"✅ Slack Bot이 채널 {channel_id}에 추가")
    else:
        print(f"❌ Bot 채널 초대 실패 응답: {response_data}")


if __name__ == "__main__":
    SLACK_CHANNEL_ID = ""  # 실제 채널 id로 테스트 
    invite_bot_to_channel(SLACK_CHANNEL_ID)