import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

# ✅ FastEmbed 임베딩 모델 초기화
embeddings = FastEmbedEmbeddings()

# ✅ 벡터 저장소 경로
vector_db_path = "./src/db/faiss_index"

def initialize_vector_db():
    """ FAISS 벡터 DB 초기화 (기존 데이터가 있으면 로드) """
    if os.path.exists(vector_db_path):
        print("✅ 기존 FAISS DB 로드 중...")
        return FAISS.load_local(vector_db_path, embeddings,  allow_dangerous_deserialization=True)
    
    print("🚀 새 FAISS DB 생성...")
    
    # ✅ 빈 FAISS 초기화 (빈 텍스트가 아닌, 최소한의 샘플 추가)
    sample_texts = ["init"]  # ✅ 최소한 하나의 더미 데이터 추가
    vectorstore = FAISS.from_texts(sample_texts, embeddings)
    
    # ✅ 새로 생성된 경우 저장
    vectorstore.save_local(vector_db_path)
    
    return vectorstore


vectorstore = initialize_vector_db()


def add_documents(documents):
    """
    문서를 FAISS 벡터 스토어에 추가합니다.
    documents는 langchain의 Document 객체 리스트여야 합니다.
    """
    global vectorstore  # 기존 vectorstore 업데이트
    vectorstore.add_documents(documents)

    # 문서를 추가한 후, 벡터 저장소를 업데이트하여 유지
    vectorstore.save_local(vector_db_path)
    print(f"✅ {len(documents)}개의 문서가 추가되었습니다.")


def similarity_search(query):
    return vectorstore.similarity_search(query)