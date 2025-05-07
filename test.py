import sys
import os
import json
import requests
from notion2md.exporter.block import StringExporter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from src.notion.notion_api import get_notion_page_list  # Notion 페이지 조회 함수
from src.notion.notion_utils import to_markdown, extract_notion_text, fetch_notion_pages  # Notion 데이터 전처리 함수

# 테스트용 OAuth Access Token & Page ID
ACCESS_TOKEN = "ntn_b29039163674LZ9MN9dlPcq0addDeEgDTD9JTaI6rC2auf"  # 테스트용 OAuth 토큰
TEST_PAGE_ID = "9a234cbd-b115-4656-aaa4-dd95927a4804"  # 테스트할 Notion 페이지 ID

def extract_notion_text(access_token, page_list):
    """
    페이지 리스트를 순회하면서 Notion 데이터를 Markdown으로 변환
    """
    notion_text = ""

    for page in page_list:
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


def test_notion_processing():
    try:
        # 
        md_text = fetch_notion_pages(ACCESS_TOKEN, TEST_PAGE_ID)

        print("\n변환된 Markdown 내용:\n")
        print(md_text)

        # 결과 검증
        if md_text and isinstance(md_text, str):
            print("\n테스트 성공! Notion 페이지가 정상적으로 변환되었습니다.")
        else:
            print("\n테스트 실패! Notion 페이지 처리 결과가 비정상적입니다.")

    except Exception as e:
        print(f"\n테스트 중 오류 발생: {str(e)}")


def notion_page_to_markdown(access_token: str, page_id: str) -> str:
    """
    Notion 페이지를 Markdown 문자열로 변환하는 함수(블럭 단위만 반영하고, 페이지나 리스트는 반영 못함)
    """
    try:
        markdown_text = StringExporter(block_id=page_id, token=access_token).export()
        return markdown_text
    except Exception as e:
        print(f"Notion 페이지 Markdown 변환 실패: {str(e)}")
        return ""


def test_notion_to_markdown():
    markdown_text = notion_page_to_markdown(ACCESS_TOKEN, TEST_PAGE_ID)

    if markdown_text:
        print("\n=== 변환된 Markdown 내용 ===")
        print(markdown_text)
    else:
        print("\nMarkdown 변환 실패")

if __name__ == "__main__":
    test_notion_to_markdown()

# if __name__ == "__main__":
#     test_notion_processing()
    