# CacheBackedEmbeddings

## 개요

**문서 임베딩**은 텍스트를 수치 벡터로 변환하는 과정으로, 이를 통해 자연어 처리 작업(문서 분류, 유사도 계산 등)을 수행할 수 있습니다. 그러나 동일한 텍스트를 반복적으로 임베딩하면 계산 비용이 증가하고 시간이 낭비됩니다. 이를 해결하기 위해 **CacheBackedEmbeddings**는 임베딩 결과를 캐싱하여 재계산을 방지합니다.

### CacheBackedEmbeddings의 기본 개념

- **캐싱**: 이미 계산된 임베딩을 저장하여 동일한 텍스트에 대해 다시 계산하지 않음.
- **키-값 저장소**: 텍스트를 해시하여 고유한 키를 생성하고, 이 키에 해당하는 임베딩 벡터를 저장.
- **네임스페이스**: 동일한 텍스트가 다른 모델로 임베딩될 때 충돌을 방지하기 위해 사용.

### CacheBackedEmbeddings 초기화

`CacheBackedEmbeddings.from_bytes_store` 메서드를 사용하여 초기화합니다. 주요 매개변수는 다음과 같습니다:

- `underlying_embeddings`: 실제 임베딩을 생성하는 모델 (예: OpenAIEmbeddings).
- `document_embedding_cache`: 캐싱에 사용할 저장소 (예: LocalFileStore, InMemoryByteStore).
- `namespace`: 캐시 충돌을 방지하기 위한 네임스페이스 (선택 사항, 기본값은 `""`).

**주의**: 동일한 텍스트가 다른 임베딩 모델로 처리될 경우 충돌을 방지하려면 `namespace`를 모델 이름으로 설정하는 것이 좋습니다.

## 설정

LangChain과 OpenAI API를 사용하기 위한 기본 설정입니다:

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

## LocalFileStore를 사용한 캐싱 (영구 보관)

임베딩 결과를 로컬 파일 시스템에 저장하여 영구적으로 보관하는 방법입니다. 이를 통해 프로그램을 종료해도 캐시가 유지됩니다.

### 설정 및 캐시 생성

```python
from langchain.storage import LocalFileStore
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.vectorstores.faiss import FAISS

# 기본 임베딩 모델 설정
embedding = OpenAIEmbeddings()

# 로컬 파일 저장소 설정
store = LocalFileStore("./cache/")

# 캐시 지원 임베딩 생성
cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings=embedding,
    document_embedding_cache=store,
    namespace=embedding.model
)
```

### 캐시 확인

```python
# 캐시된 키 목록 확인
list(store.yield_keys())
```

### 문서 처리 및 캐싱

문서를 로드하고, 청크로 분할한 후, 캐시된 임베딩을 사용하여 FAISS 벡터 저장소를 생성합니다.

```python
from langchain.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

# 문서 로드
raw_documents = TextLoader("./data/appendix-keywords.txt").load()

# 문자 단위로 텍스트 분할
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)

# FAISS 벡터 저장소 생성 (시간 측정)
%time db = FAISS.from_documents(documents, cached_embedder)
```

### 캐싱의 이점

동일한 문서를 다시 처리할 때 캐시된 임베딩을 사용하므로 속도가 크게 향상됩니다.

```python
# 캐시된 임베딩을 사용하여 FAISS 벡터 저장소 재생성 (시간 측정)
%time db2 = FAISS.from_documents(documents, cached_embedder)
```

**부연 설명**: 첫 번째 실행 시에는 임베딩이 계산되고 캐시에 저장되며, 두 번째 실행 시에는 캐시에서 임베딩을 가져오므로 시간이 단축됩니다. 이는 대규모 데이터셋에서 특히 유용합니다.

## InMemoryByteStore를 사용한 캐싱 (비영구적)

`InMemoryByteStore`는 메모리 내에서 캐시를 저장하는 방법으로, 프로그램 종료 시 캐시가 사라집니다. 임시 작업에 적합합니다.

### 설정 및 캐시 생성

```python
from langchain.storage import InMemoryByteStore

# 메모리 내 저장소 설정
store = InMemoryByteStore()

# 캐시 지원 임베딩 생성
cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings=embedding,
    document_embedding_cache=store,
    namespace=embedding.model
)
```

**부연 설명**: `InMemoryByteStore`는 디스크에 저장하지 않으므로 속도가 빠르지만, 메모리 사용량이 증가할 수 있습니다. 대규모 데이터셋에는 적합하지 않을 수 있습니다.

## CacheBackedEmbeddings의 장점과 사용 시 고려사항

### 장점

- **속도 향상**: 동일한 텍스트를 반복적으로 임베딩할 필요가 없음.
- **비용 절감**: OpenAI API 호출 횟수를 줄여 비용을 절감.
- **유연성**: 영구적(LocalFileStore) 또는 비영구적(InMemoryByteStore) 캐싱 선택 가능.

### 고려사항

- **캐시 크기 관리**: `LocalFileStore`를 사용할 경우 디스크 공간을 모니터링해야 함.
- **네임스페이스 설정**: 동일한 텍스트가 다른 모델로 임베딩될 경우 충돌 방지를 위해 필수.
- **메모리 사용량**: `InMemoryByteStore`는 메모리 사용량이 많아질 수 있으므로 주의.

이 문서는 `CacheBackedEmbeddings`의 개념과 사용 방법을 설명하며, 캐싱을 통해 임베딩 작업의 효율성을 높이는 방법을 다룹니다.
