import os
import shutil
from config import CONFIG
from src.db.faiss_db import add_documents
from src.doc_process.doc_process import process_document, is_supported_file, SUPPORTED_EXTENSIONS

# 전역 변수: 처리된 파일 목록 (파일명)
current_files = []


def get_file_list():
    """
    현재 처리된 파일 목록을 문자열로 반환합니다.
    """
    return ", ".join(current_files) if current_files else "No documents found"


def add_file(file):
    """
    업로드된 파일을 데이터 디렉터리로 복사한 후 문서 처리 및 벡터 저장소에 추가합니다.
    성공한 경우 파일명을 전역 목록에 추가합니다.
    """
    global current_files

    if file is None:
        return "No file uploaded.", None, get_file_list()

    file_path = file.name
    if not is_supported_file(file_path):
        return (
            f"Unsupported file type. Supported types are: {', '.join(SUPPORTED_EXTENSIONS)}",
            None,
            get_file_list()
        )

    try:
        # 데이터 디렉터리 존재 여부 확인 및 생성
        data_dir = CONFIG['data_dir']
        os.makedirs(data_dir, exist_ok=True)
        
        destination = os.path.join(data_dir, os.path.basename(file_path))
        shutil.copy(file_path, destination)

        # 문서 처리 및 벡터 저장소에 추가
        documents = process_document(destination)
        add_documents(documents)

        file_name = os.path.basename(file_path)
        if file_name not in current_files:
            current_files.append(file_name)

        return f"File {file_name} added and processed successfully.", None, get_file_list()
    except Exception as e:
        error_msg = f"Error processing {os.path.basename(file_path)}: {str(e)}"
        print(error_msg)  # 추후 logging 모듈 사용 고려
        return error_msg, None, get_file_list()


def initialize_files():
    """
    데이터 디렉터리에 있는 파일들을 스캔하여 문서를 처리한 후 벡터 저장소에 추가합니다.
    처리에 성공한 파일들만 전역 목록에 남깁니다."""

    global current_files

    data_dir = CONFIG['data_dir']
    os.makedirs(data_dir, exist_ok=True)

    # 데이터 디렉터리에서 지원하는 파일 목록 가져오기
    files = [f for f in os.listdir(data_dir) if is_supported_file(f) and not f.startswith('.')]
    successful_files = []  # 처리에 성공한 파일 목록

    for file in files:
        file_path = os.path.join(data_dir, file)
        try:
            documents = process_document(file_path)
            add_documents(documents)
            print(f"Processed and added {file} to the vector store.")
            successful_files.append(file)
        except Exception as e:
            print(f"Error processing {file}: {str(e)}")

    current_files = successful_files
    return get_file_list()