# notion 변경 사항 감지시 모델에 source data 업데이트 

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
#from src.doc_process.doc_process import process_document
#from src.db.faiss_db import add_document

#  http://localhost:8000/docs
app = FastAPI(
    title="Notion Update",
    description="Notion 변경 사항을 감지 및 업데이트",
    version="1.0.0"
)

class NotionPage(BaseModel):
    lastEditedTime: str
    title: str
    url: str

class NotionUpdateRequest(BaseModel):
    userEmail: str
    assistantName: str
    access_token: str
    notionPages:list[NotionPage]

@app.post("/notion/update", summary="Notion 페이지 변경 사항 업데이트", tags=["Notion"])
async def update_notion_pages(request: NotionUpdateRequest):
    try:
        print(f"📌 Received Notion update from {request.userEmail} for Assistant: {request.assistantName}")

        # 변경된 페이지 목록 확인
        for page in request.notionPages:
            print(f"Updating RAG model for Notion page: {page.title} ({page.url})")

            # (1) Notion 페이지 내용을 가져와 RAG 모델 업데이트
            process_notion_page(page)

        return {"message": "RAG model updated successfully", "userEmail": request.userEmail}

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update RAG model")


# 노션  업데이트 사항 반영하는 함수 
# def process_notion_page(page: NotionPage):

#         print(f"📌 Processing page: {page.title} ({page.url})")
#         documents = process_document(page.title)

       
#         add_documents(documents)

#         print(f"Notion page {update.page_id} has been updated in the vecstore.")
#         return {"message": "RAG model updated successfully", "page_id": update.page_id}

   