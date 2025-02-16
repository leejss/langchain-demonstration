# OpenAI Embeddings

## 개요

**문서 임베딩**은 자연어 처리(NLP)에서 문서의 의미를 수치적인 형태로 표현하는 기술입니다. 이를 통해 컴퓨터는 텍스트의 의미를 이해하고, 비교하거나 분석할 수 있습니다.

### 문서 임베딩의 기본 개념

- **토큰화**: 문서를 작은 단위(단어, 서브워드 등)로 분할합니다.
- **모델 입력**: 분할된 단위를 모델에 입력하여 각 단위에 대한 벡터를 얻습니다.
- **임베딩 생성**: 각 단위의 벡터를 평균하거나 합쳐 전체 문서의 벡터를 만듭니다.

임베딩은 다음과 같은 용도에 사용됩니다:

- **문서 분류**: 문서의 주제나 카테고리를 분류.
- **감성 분석**: 텍스트의 긍정/부정 감정을 분석.
- **유사도 계산**: 문서나 문장 간의 유사도를 측정.

[더 알아보기](https://platform.openai.com/docs/guides/embeddings/embedding-models)

## 설정

LangChain과 OpenAI의 API를 사용하기 위해 필요한 환경 설정입니다:

```python
from dotenv import load_dotenv

# API 키 정보 로드
load_dotenv()
```

LangSmith를 통해 작업을 추적할 수 있습니다:

```python
from langchain_teddynote import logging

logging.langsmith("CH08-Embeddings")
```

## 지원되는 모델

| 모델                   | 페이지 당 달러 | MTEB 평가 성능 | 최대 입력 |
|------------------------|----------------|----------------|----------|
| text-embedding-3-small | 62,500         | 62.3%          | 8191     |
| text-embedding-3-large | 9,615          | 64.6%          | 8191     |
| text-embedding-ada-002 | 12,500         | 61.0%          | 8191     |

### 모델 선택 시 고려사항

- **성능 vs 비용**: 성능이 높을수록 비용이 증가합니다.
- **입력 제한**: 모든 모델이 8191 토큰을 처리할 수 있지만, 실제로는 문서의 길이에 따라 모델 선택이 달라질 수 있습니다.

## OpenAIEmbeddings 클래스의 메소드 설명

### `.embed_query(text: str) -> List[float]`

- **역할**: 입력된 단일 텍스트를 임베딩 벡터로 변환.
- **사용 예**: 특정 쿼리나 문장의 임베딩을 추출할 때 사용.

### `.embed_documents(documents: List[str]) -> List[List[float]]`

- **역할**: 여러 문서를 한 번에 임베딩 벡터로 변환.
- **사용 예**: 여러 문서의 임베딩을 한꺼번에 계산할 때 유용합니다.

### 메소드 공통 파라미터

- **model**: 사용할 임베딩 모델을 지정. 기본값은 `text-embedding-3-small`.
- **dimensions**: 임베딩 벡터의 차원을 조정. 기본값은 종종 모델에 따라 다르지만, `text-embedding-3-small`의 경우 1536입니다.

## 쿼리 임베딩

임베딩을 통해 문장의 의미를 벡터로 변환하는 예제입니다:

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
text = "임베딩 테스트를 하기 위한 샘플 문장입니다."
query_result = embeddings.embed_query(text)
print(query_result[:5])  # 첫 5개 값만 출력
```

## Document 임베딩

여러 문서를 한 번에 임베딩하는 방법입니다:

```python
doc_result = embeddings.embed_documents([text, text, text, text])
print(len(doc_result))  # 임베딩된 문서 목록의 길이
print(doc_result[0][:5])  # 첫 번째 문서의 첫 5개 값
```

## 차원 지정

임베딩의 차원을 조정하여 메모리 사용량을 줄일 수 있습니다:

```python
embeddings_1024 = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1024)
print(len(embeddings_1024.embed_documents([text])[0]))  # 임베딩 차원 확인
```

## 유사도 계산

임베딩 벡터를 사용하여 문장 간의 유사도를 계산할 수 있습니다:

```python
from sklearn.metrics.pairwise import cosine_similarity

sentences = ["안녕하세요? 반갑습니다.", "안녕하세요? 반갑습니다!", "안녕하세요? 만나서 반가워요.", "Hi, nice to meet you.", "I like to eat apples."]
embedded_sentences = embeddings_1024.embed_documents(sentences)

def similarity(a, b):
    return cosine_similarity([a], [b])[0][0]

for i, sentence in enumerate(embedded_sentences):
    for j, other_sentence in enumerate(embedded_sentences):
        if i < j:
            print(f"[유사도 {similarity(sentence, other_sentence):.4f}] {sentences[i]} \t <=====> \t {sentences[j]}")
```

### 추가 정보

- **코사인 유사도**: 두 벡터 사이의 각도를 기반으로 유사도를 계산. 값이 1에 가까울수록 유사도가 높음.
- **차원 감소**: 임베딩 차원을 줄이면 계산 비용이 줄어들지만, 정보 손실이 발생할 수 있음.
