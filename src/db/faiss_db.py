import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

embeddings = FastEmbedEmbeddings()

VECTOR_DB_BASE_PATH = "./src/db/faiss_index"

def get_vectorstore_path(identifier: str):
    """
    저장할 벡터스토어 경로 반환
    """
    return os.path.join(VECTOR_DB_BASE_PATH, f"{identifier}")


def initialize_vector_db(identifier: str):
    """
    FAISS 벡터 DB 초기화 (기존 데이터가 있으면 로드)
    """
    vector_db_path = get_vectorstore_path(identifier)

    if os.path.exists(vector_db_path):
        print(f" 기존 FAISS DB 로드 중... {identifier}")
        return FAISS.load_local(vector_db_path, embeddings, allow_dangerous_deserialization=True)

    print(f"🚀 새 FAISS DB 생성 중... {identifier}")
    
    sample_texts = ["init"]
    vectorstore = FAISS.from_texts(sample_texts, embeddings)
    
    vectorstore.save_local(vector_db_path)
    
    return vectorstore


def save_to_vectorstore(documents, identifier: str):
    """
    문서를 FAISS 벡터 스토어에 저장 (assistant_name, user_email 기반)
    """
    vector_db_path = get_vectorstore_path(identifier)
    vectorstore = initialize_vector_db(identifier)

    vectorstore.add_documents(documents)
    vectorstore.save_local(vector_db_path)

    print(f"{len(documents)}개의 문서가 벡터스토어 {identifier}에 저장됨.")



def similarity_search(query, identifier: str):
    """
    특정 assistant_name, user_email 기반으로 검색
    """
    vectorstore = initialize_vector_db(identifier)
    return vectorstore.similarity_search(query)