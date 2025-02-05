import asyncio
from config import CONFIG
from src.llm.model import process_with_rag
from src.db.faiss_db import similarity_search
from src.utils.utils import initialize_files

async def process_message(message):
    """
    사용자 메시지를 처리하여 유사 문서를 검색한 후,
    RAG 체인을 통해 답변을 생성합니다.
    """
    # 문맥 검색 (벡터 DB에서 유사 문서 조회)
    context = similarity_search(message)
    # RAG 체인을 통해 답변 생성 (synchronous 함수 호출)
    response = process_with_rag(message, context)
    return response

async def type_message(message, delay=0.0005):

    for i in range(len(message) + 1):
        yield message[:i]
        await asyncio.sleep(delay)

async def main():
    print("Initializing files...")
    file_list = initialize_files()
    print("Initialized files:", file_list)
    
    print("\nWelcome to the chatbot.")
    print("Type your message (or 'quit' to exit).")
    
    while True:
        user_input = input("User: ").strip()
        if user_input.lower() in ['quit', 'exit']:
            break

        # 사용자 메시지 처리 및 답변 생성 (비동기 처리)
        response = await process_message(user_input)
        
        # ✅ 전체 응답을 한 번만 출력
        print(f"Bot: {response}")
    
    print("Exiting chatbot.")

if __name__ == "__main__":
    asyncio.run(main())