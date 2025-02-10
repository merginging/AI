import requests
import json

def send_slack_message(channel_id, message, slack_token):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }
    data = {
        "channel": channel_id,
        "text": message
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()

    if response.status_code == 200 and response_data.get("ok"):
        print(f"✅ Slack 메시지 전송: {message}")
    else:
        print(f"❌ Slack 메시지 전송 실패 응답: {response_data}")



def get_channel_info(channel_id, slack_token):
    url = "https://slack.com/api/conversations.info"
    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {"channel": channel_id}

    response = requests.get(url, headers=headers, params=params)
    response_data = response.json()

    if response.status_code == 200 and response_data.get("ok"):
        return response_data["channel"]
    else:
        print(f"❌ 채널 정보 조회 실패! 응답: {response_data}")
        return None



def get_user_info(user_id, slack_token):
    url = "https://slack.com/api/users.info"
    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {"user": user_id}

    response = requests.get(url, headers=headers, params=params)
    response_data = response.json()

    if response.status_code == 200 and response_data.get("ok"):
        return response_data["user"]
    else:
        print(f"❌ 유저 정보 조회 실패 응답: {response_data}")
        return None
    


def log_slack_event(event_data, log_file="slack_events.log"):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(event_data, ensure_ascii=False, indent=4) + "\n")
    print(f"📝 Slack 이벤트 로그 저장 완료: {log_file}")