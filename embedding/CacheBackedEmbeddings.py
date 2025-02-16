from time import time
from langchain_openai import OpenAIEmbeddings
from langchain.storage import InMemoryByteStore
from langchain.embeddings import CacheBackedEmbeddings


embeddings = OpenAIEmbeddings()
cache = InMemoryByteStore()

# embedding + cache backend
cache_embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings=embeddings,
    document_embedding_cache=cache,
    namespace=embeddings.model,
)

# 임베딩할 텍스트
text = "Hello, how are you?"

# first embedding (no cache)
start_time = time()
first_embedding = cache_embedder.embed_query(text)
end_time = time()
print(f"Time taken: {end_time - start_time:.4f} seconds")


# second embedding (with cache)
start_time = time()
second_embedding = cache_embedder.embed_query(text)
end_time = time()
print(f"Time taken: {end_time - start_time:.4f} seconds")


# 캐시된 키 확인
print("\nCached keys:")
print(list(cache.yield_keys()))

# 임베딩 결과 비교 (동일한지 확인)
print("\nAre embeddings identical?", first_embedding == second_embedding)
