from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings


def semantic_chunker():
    with open("./data/appendix-keywords.txt") as f:
        content = f.read()

    # 1. Percentile
    text_splitter = SemanticChunker(
        OpenAIEmbeddings(),
        breakpoint_threshold_type="percentile",
        breakpoint_threshold_amount=70,
    )

    docs = text_splitter.create_documents([content])
    print(f"Number of chunks: {len(docs)}")
    for i, doc in enumerate(docs[:2]):
        print(f"\nChunk {i}:")
        print(doc.page_content)
        print("-" * 30)


if __name__ == "__main__":
    semantic_chunker()
