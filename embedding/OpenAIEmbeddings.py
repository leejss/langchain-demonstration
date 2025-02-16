from langchain_openai import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
embeddings_1024 = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1024)

# 쿼리 임베딩
text = "Hello everyone, how are you doing today?"
query_result = embeddings.embed_query(text)
print("Query Result (First 5 elements):", query_result[:5])

# 문서 임베딩
docs_result = embeddings.embed_documents([text] * 4)
print("Document Result Length:", len(docs_result))

# 유사도 계산
sentences = [
    "안녕하세요? 반갑습니다.",
    "안녕하세요? 반갑습니다!",
    "안녕하세요? 만나서 반가워요.",
    "Hi, nice to meet you.",
    "I like to eat apples.",
]
embedded_sentences = embeddings_1024.embed_documents(sentences)


def similarity(a, b):
    return cosine_similarity([a], [b])[0][0]


for i, sentence in enumerate(embedded_sentences):
    for j, other_sentence in enumerate(embedded_sentences):
        if i < j:
            print(
                f"[유사도 {similarity(sentence, other_sentence):.4f}] {sentences[i]} \t <=====> \t {sentences[j]}"
            )
