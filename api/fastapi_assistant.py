from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Assistant Update ",
    description="Assistant 정보 update",
    version="1.0.0"
)

class AssistantUpdate(BaseModel):
    assistantName: str
    action_tag: str
    model_name: str
    notion_page_list: List[str]
    open_api_key: str
    prompt: str
    userEmail: str

@app.post("/assistant/update")
async def update_assistant(request: AssistantUpdate):
    try:
        print(f"📌 New assistant created: {request.assistant_name}")
        print(f"📌 Model: {request.model_name}, Action Tag: {request.action_tag}")
        print(f"📌 User: {request.user_email}, Notion Pages: {request.notion_page_list}")
        print(f"📌 Prompt: {request.prompt}") 

        # 데이터 전처리 로직 추가 

        return {"message": "Assistant update received", "assistant_id": request.assistant_id}

    except Exception as e:
        print(f" Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process assistant update")