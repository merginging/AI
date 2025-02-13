from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Slack Oauth Create",
    description="Slack access token ",
    version="1.0.0")

class SlackOAuthData(BaseModel):
    workspace_id: str
    access_token: str
    assistantName: str
    userEmail: str

@app.post("/slack/oauth")
async def receive_slack_oauth(request: SlackOAuthData):

    try:
        print(f"Slack OAuth completed for workspace: {request.workspace_id}")
        print(f"Access Token: {request.access_token}, User: {request.user_email}")

        
        # 추후 로직 구현 

        return {"message": "Slack OAuth token received", "workspace_id": request.workspace_id}

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process Slack OAuth token")