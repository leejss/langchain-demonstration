from langchain_text_splitters import CharacterTextSplitter


def basic_splitting_example():

    # file read

    with open("./data/appendix-keywords.txt") as f:
        file = f.read()

    # text splitter instance

    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=210,
        chunk_overlap=0,
        length_function=len,
    )

    documents = text_splitter.create_documents([file])
    print("First chunk from create_documents:")
    print(f"Length: {len(documents[0].page_content)}")
    print(documents[0])
    print("\n" + "=" * 50 + "\n")

    return documents


def splitting_with_metadata_example():

    with open("./data/appendix-keywords.txt") as f:
        file = f.read()

    metadatas = [{"document": 1}, {"document": 2}]

    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=210,
        chunk_overlap=0,
        length_function=len,
    )
    # metadata와 함꼐 document 생성
    documents = text_splitter.create_documents([file, file], metadatas=metadatas)

    print("Documents with metadata:")
    print("First document:")
    print(documents[0])
    print("\nMetadata of second document:")
    print(documents[1].metadata)
    print("\nTotal number of documents:", len(documents))
    print("\n" + "=" * 50 + "\n")

    return documents


if __name__ == "__main__":
    # basic_splitting_example()
    splitting_with_metadata_example()
