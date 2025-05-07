import os
import faiss
import numpy as np
import PyPDF2
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# FAISS 인덱스 설정
FAISS_DIR = "faiss_db"
FAISS_INDEX_FILE = os.path.join(FAISS_DIR, "faiss_index.index")
DIMENSION = 384  # all-MiniLM-L6-v2 모델 기준 384차원 벡터

# 임베딩 모델 로드
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# PDF를 텍스트로 변환
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

# 텍스트를 벡터화하여 FAISS에 저장
def add_pdf_to_faiss(pdf_path):
    text = extract_text_from_pdf(pdf_path)

    # 문서 청크 나누기 (256 토큰 단위)
    chunk_size = 256
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    # FAISS 인덱스 생성 또는 불러오기
    if os.path.exists(FAISS_INDEX_FILE):
        index = faiss.read_index(FAISS_INDEX_FILE)
    else:
        index = faiss.IndexFlatL2(DIMENSION)

    # 벡터화 후 저장
    embeddings = embed_model.encode(chunks)
    index.add(np.array(embeddings))

    # FAISS 저장
    faiss.write_index(index, FAISS_INDEX_FILE)

    # 저장된 벡터 개수 및 예상 용량 출력
    num_vectors = index.ntotal
    estimated_size_mb = (num_vectors * DIMENSION * 4) / (1024 * 1024)  # MB 단위 변환
    return num_vectors, estimated_size_mb

# PDF 파일 경로 설정
pdf_file = "/Users/yujuyoung/Desktop/branchify_v2/data/jobapply.pdf"

# FAISS 벡터 저장 후 용량 확인
num_vectors, estimated_size_mb = add_pdf_to_faiss(pdf_file)
print(f"✅ 총 {num_vectors}개의 벡터 저장 완료")
print(f"📌 예상 저장 용량: {estimated_size_mb:.2f}MB")