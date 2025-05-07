# title, pageid, type만 가져와서 dict으로 저장해도 될거 같은데.. 
import requests

NOTION_API_URL = "https://www.branchify.site/api/assistantlist/notionPage"

def get_notion_page_list(user_email, assistant_name):
    """
    DB에 등록된 Notion 페이지를 리스트로 반환 
    """
    params = {
        "userEmail": user_email,
        "assistantName": assistant_name
    }

    response = requests.get(NOTION_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get("notionPageList", [])
    else:
        raise Exception(f"Notion 페이지 리스트 조회 실패! 응답: {response.text}")

 
if __name__ == "__main__":
    TEST_EMAIL = "test@gmail.com"
    TEST_ASSISTANT_NAME = "assistant1"

    pages = get_notion_page_list(TEST_EMAIL, TEST_ASSISTANT_NAME)
    print(" Notion Page List:", pages)