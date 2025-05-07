import requests
from src.doc_process.doc_process import process_document  # 문서 전처리 함수 호출
from src.db.faiss_db import save_to_vectorstore  # 벡터스토어 저장 함수 호출

def fetch_notion_pages(access_token: str, page_id: str):
    """
    Notion API를 통해 페이지의 블럭 데이터를 가져오는 함수 
    """
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Notion-Version": "2022-06-28"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()  #
            return data.get("results", [])
        except Exception as e:
            print(f"❌ JSON 변환 오류: {str(e)}")
            return []  
    else:
        print(f"Notion 페이지 조회 실패: {response.status_code} - {response.text}")
        return []  


def to_markdown(notion_data):
    """
    Notion API 응답 데이터를 Markdown 형식으로 변환
    """
    markdown_content = ""

    for block in notion_data.get("results", []):
        block_type = block.get("type")
        text_data = block.get(block_type, {}).get("text", [])
        rich_text = " ".join([t.get("plain_text", "") for t in text_data])

        if block_type == "heading_1":
            markdown_content += f"# {rich_text}\n\n"
        elif block_type == "heading_2":
            markdown_content += f"## {rich_text}\n\n"
        elif block_type == "heading_3":
            markdown_content += f"### {rich_text}\n\n"
        elif block_type == "paragraph":
            markdown_content += f"{rich_text}\n\n"
        elif block_type == "bulleted_list_item":
            markdown_content += f"- {rich_text}\n"
        elif block_type == "numbered_list_item":
            markdown_content += f"1. {rich_text}\n"
        elif block_type == "quote":
            markdown_content += f"> {rich_text}\n\n"
        elif block_type == "code":
            language = block.get("code", {}).get("language", "")
            markdown_content += f"```{language}\n{rich_text}\n```\n\n"
    
    return markdown_content.strip()

def extract_notion_text(access_token: str, pages: list):
    """
    Notion 페이지 리스트를 재귀적으로 탐색하여 모든 텍스트를 추출
    """
    notion_text = ""

    for page in pages:
        page_id = page.get("pageId")
        title = page.get("title", "Untitled")

        # Notion API에서 페이지 콘텐츠 가져오기
        page_content = fetch_notion_pages(access_token, page_id)
        md_content = to_markdown(page_content)

        notion_text += f"\n\n## {title}\n{md_content}"

        # 하위 페이지 처리 (재귀 호출)
        children = page.get("children", [])
        if children:
            notion_text += extract_notion_text(access_token, children)

    return notion_text


def process_notion_and_store(notion_text: str, user_email: str, assistant_name: str):
    """
    Notion 데이터를 전처리한 후 벡터스토어에 저장
    """
    # 문서 전처리 (Markdown 파일 없이 변수 직접 전달)
    processed_docs = process_document(notion_text)

    # 벡터스토어에 저장
    save_to_vectorstore(processed_docs, f"notion_{user_email}_{assistant_name}")

    print(f"벡터스토어 저장 완료: notion_{user_email}_{assistant_name}")