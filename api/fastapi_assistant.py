# assistant 생성 & 노션, pdf vecstore 저장까지 

import sys
import os

# src 디렉토리를 sys.path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import requests 
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from src.notion.notion_utils import fetch_notion_pages, to_markdown, extract_notion_text
from src.db.faiss_db import save_to_vectorstore
from src.doc_process.doc_process import process_document

ASSISTANT_SEARCH_API = "https://www.branchify.site/api/assistantlist/search"

app = FastAPI(
    title="Assistant Update ",
    description="Assistant 정보 update",
    version="1.0.0"
)

class NotionOAuthData(BaseModel):
    accessToken: str
    workspaceId: str
    workspaceName: Optional[str] = None

class SlackOAuthData(BaseModel):
    accessToken: str
    workspaceId: str
    workspaceName: Optional[str] = None

class AssistantUpdate(BaseModel):
    assistantName: str
    action_tag: str
    model_name: str
    notion_page_list: Optional[List[dict]] = None  # Notion 페이지 리스트
    open_api_key: Optional[str] = None
    prompt: str
    userEmail: str
    pdf_urls: Optional[List[str]] = None  # PDF URL 리스트
    notion_oauth: Optional[NotionOAuthData] = None  # Notion OAuth 정보
    slack_oauth: Optional[SlackOAuthData] = None  # Slack OAuth 정보
    s3_file_url: Optional[str] = None
 

def get_assistant_data(user_email: str, assistant_name: str):
    params = {"userEmail": user_email, "assistantName": assistant_name}
    
    print(f"🔄 Assistant 데이터 요청 시작: {params}")  # 요청 전 로그
    response = requests.get(ASSISTANT_SEARCH_API, params=params)
    print(f"🔄 API 응답 코드: {response.status_code}")  # 응답 코드 확인

    if response.status_code == 200:
        data = response.json()
        if data:
            print(f"✅ Assistant 데이터 조회 성공:{data}")
            return data
        else:
            raise HTTPException(status_code=404, detail="Assistant not found")
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch assistant data")

# pdf s3 url 전처리 , vecstore 저장 
# 아직 구현 안함 
# def process_and_store_pdf(assistant_name: str, user_email: str, pdf_urls: List[str]):
#     for url in pdf_urls:
#         local_pdf_path = download_pdf_from_s3(url)
#         text = extract_text_from_pdf(local_pdf_path)
#         save_to_vectorstore(text, f"pdf_{user_email}_{assistant_name}")  # ✅ pdf_{userEmail}_{assistantName} 형식으로 저장


# notion page 전처리, vecstore 저장 
# pagelist 구조 정리하는 코드 필요함 
def process_and_store_notion(assistant_name: str, user_email: str, access_token: str, notion_page_list: list):
    """
    Notion 데이터를 가져와서 마크다운 변환 → 전처리 → 벡터 저장
    """
    # JSON 문자열이면 리스트로 변환
    if isinstance(notion_page_list, str):
        try:
            notion_page_list = json.loads(notion_page_list)
        except json.JSONDecodeError:
            print("JSON 변환 오류: notion_page_list가 올바른 형식이 아닙니다.")
            notion_page_list = []

    # Notion 데이터를 추출 (notion_utils.py의 extract_notion_text 사용)
    notion_text = extract_notion_text(access_token, notion_page_list)

    # Notion 데이터를 전처리 후 벡터스토어에 저장
    processed_docs = process_document(notion_text)
    identifier = f"notion_{user_email}_{assistant_name}"
    print(f"🔄 FAISS 벡터 저장 시작: notion_{user_email}_{assistant_name}")

    save_to_vectorstore(processed_docs, identifier)

    print(f"✅ FAISS 벡터 저장 완료: notion_{user_email}_{assistant_name}")

    print(f"Notion 데이터가 {identifier}에 저장됨.")


@app.post("/assistant/update")
async def update_assistant(request: AssistantUpdate):
    try:
        assistant_name = request.assistantName
        user_email = request.userEmail

        print(f"🟢 New assistant update 요청: {assistant_name} / {user_email}")

        # ✅ 백엔드 API 호출 → DB에서 assistant 데이터 조회
        assistant_data = get_assistant_data(user_email, assistant_name)

        # # PDF 처리
        # if request.pdf_urls:
        #     process_and_store_pdf(assistant_name, user_email, request.pdf_urls)
        
        notion_page_list = assistant_data.get("notionPages", "[]") 
        notion_oauth = assistant_data.get("notionOAuth")

        print(f"📌 notion_page_list 타입: {type(notion_page_list)}, 길이: {len(notion_page_list) if isinstance(notion_page_list, list) else 'N/A'}")
        print(f"📌 notion_oauth: {notion_oauth}")
        
        # Notion 처리
        if notion_oauth and notion_page_list:
            print("✅ Notion 데이터 처리 시작")
            # process_and_store_notion(assistant_name, user_email, request.notion_oauth.accessToken, request.notion_page_list)
            print("✅ Notion 데이터 처리 완료")
        else:
            print("⚠️ Notion 데이터가 없거나 OAuth 인증이 없음")

        return {"message": "Assistant update processed successfully"}

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process assistant update")