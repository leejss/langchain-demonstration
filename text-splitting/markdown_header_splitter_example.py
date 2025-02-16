from langchain_text_splitters import MarkdownHeaderTextSplitter


def basic_header_splitter():
    with open("./data/example-markdown.md", "r") as f:
        content = f.read()

    # split header points
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ("####", "Header 4"),
        ("#####", "Header 5"),
        ("######", "Header 6"),
    ]

    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
    )
    splits = splitter.split_text(content)
    print("\n=== 기본 분할 결과 ===")
    for split in splits:
        print(f"\nContent: {split.page_content}")
        print(f"Metadata: {split.metadata}")

    splitter_with_headers = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on, strip_headers=False
    )

    splits_with_headers = splitter_with_headers.split_text(content)

    print("\n=== 헤더 포함 분할 결과 ===")
    for split in splits_with_headers:
        print(f"\nContent: {split.page_content}")
        print(f"Metadata: {split.metadata}")


if __name__ == "__main__":
    basic_header_splitter()
