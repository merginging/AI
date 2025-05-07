import requests

SLACK_TOKEN_API = "https://www.branchify.site/api/assistantlist/search"

def get_slack_access_token(user_email: str, assistant_name: str):
    """
    이메일, 봇 이름 기준으로 slack access token 가져오기 
    """
    params = {
        "userEmail": user_email,
        "assistantName": assistant_name
    }

    response = requests.get(SLACK_TOKEN_API, params=params)

    if response.status_code == 200:
        slack_data = response.json()
        slack_oauth = slack_data.get("slackOAuth", {})
        slack_token = slack_oauth.get("accessToken")

        if slack_token:
            print(f"✅ Slack Access Token 가져오기: {slack_token[:10]}...")
            return slack_token
        else:
            raise ValueError("❌ Slack Access Token이 응답에 포함되지 않음")
    else:
        raise Exception(f"❌ 오류 발생! 응답 코드: {response.status_code}\n응답 내용: {response.text}")


# 테스트
if __name__ == "__main__":
    TEST_EMAIL = "test@gmail.com"
    TEST_ASSISTANT_NAME = "test"
    token = get_slack_access_token(TEST_EMAIL, TEST_ASSISTANT_NAME)
    print(f"🔑 Slack Token: {token}")