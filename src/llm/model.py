import openai
from config import CONFIG

# OpenAI API 키 설정
client = openai.OpenAI(api_key=CONFIG['openai_api_key'])

def process_with_rag(question, context):
    """
    주어진 문맥과 질문을 기반으로 OpenAI ChatCompletion API를 사용하여 답변을 생성합니다."""

    prompt = f"""당신은 지식 기반을 활용하여 사용자 질문에 대한 정확한 답변을 제공하는 AI 챗봇입니다. 
    사용자가 질문하면, 기존의 지식 데이터를 검색하여 신뢰할 수 있는 정보를 제공합니다.  
    만약, 질문과 관련된 정보가 데이터베이스에 존재하지 않는다면,  
    "해당 정보는 현재 제공할 수 없습니다."라고 답변하세요.  

    다음 컨텍스트를 바탕으로 질문에 답변하세요:
    {context}

    질문: {question}

    모든 답변은 **사용자의 질문과 동일한 언어(한국어 또는 영어)로 작성**하세요.  
    """
    
    # OpenAI ChatCompletion API 호출 (최신 방식)
    response = client.chat.completions.create(
        model=CONFIG['default_model'],  
        messages=[{"role": "user", "content": prompt}],
        temperature=CONFIG['temperature'],
        max_tokens=CONFIG['max_tokens']
    )
    
    return response.choices[0].message.content
