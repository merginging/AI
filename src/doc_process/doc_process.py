from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredFileLoader,
    UnstructuredMarkdownLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CONFIG

SUPPORTED_EXTENSIONS = ('.pdf', '.txt', '.md', '.markdown')

# 텍스트 분할기 초기화
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CONFIG['chunk_size'],
    chunk_overlap=CONFIG['chunk_overlap']
)

def get_loader_for_file(file_path):
    """
    파일 확장자에 따라 적절한 문서 로더를 반환
    """
    file_path_lower = file_path.lower()
    if file_path_lower.endswith('.pdf'):
        return PyPDFLoader(file_path)
    elif file_path_lower.endswith('.txt'):
        return UnstructuredFileLoader(file_path)
    elif file_path_lower.endswith(('.md', '.markdown')):
        return UnstructuredMarkdownLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

def process_document(file_path):
    """
    문서를 로드 및 텍스트 청크로 분할
    """
    loader = get_loader_for_file(file_path)
    documents = loader.load()
    spilt_docs = text_splitter.split_documents(documents)
    # PDF 파일의 경우, 'page' 정보 등 metadata가 그대로 유지됩니다.
    return spilt_docs

def is_supported_file(file_path):
    return file_path.lower().endswith(SUPPORTED_EXTENSIONS)