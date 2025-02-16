from langchain_text_splitters import RecursiveCharacterTextSplitter


def recursive_splitting():
    with open("./data/appendix-keywords.txt") as f:
        file = f.read()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=210, chunk_overlap=50, length_function=len, is_separator_regex=False
    )

    texts = text_splitter.create_documents([file])

    print("=== Basic Recursive Splitting Results ===")
    print(f"Number of text chunks: {len(texts)}")

    # Print first two documents
    print("\nFirst document:")
    print(texts[0])
    print("\nSecond document:")
    print(texts[1])


"""
주요 역할

계층적 분할 전략


큰 단위에서 작은 단위로 순차적으로 텍스트를 분할합니다:

먼저 단락 단위(\n\n)로 분할 시도
그 다음 문장 단위(\n)로 분할 시도
그 다음 단어 단위(공백)로 분할 시도
마지막으로 개별 문자 단위로 분할


의미 단위 보존


가능한 한 의미 있는 단위(단락, 문장)를 유지하면서 분할합니다
필요한 경우에만 더 작은 단위로 분할을 진행합니다

사용해야 하는 이유

더 나은 텍스트 일관성


CharacterTextSplitter는 단순히 지정된 크기로 텍스트를 자르지만
RecursiveCharacterTextSplitter는 문맥과 구조를 고려하여 분할합니다


자연스러운 청크 생성


단락이나 문장 단위로 분할되므로 더 자연스러운 텍스트 청크가 생성됩니다
이는 LLM이 텍스트를 이해하고 처리하는 데 더 효과적입니다


유연한 분할 처리


텍스트의 구조에 따라 적절한 분할 방식을 자동으로 선택합니다
긴 단락은 더 작은 단위로 분할되고, 짧은 단락은 그대로 유지됩니다

"""


if __name__ == "__main__":
    recursive_splitting()
