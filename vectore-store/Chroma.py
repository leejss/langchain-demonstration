from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


text_splitter = RecursiveCharacterTextSplitter(
  chunk_size=600,
  chunk_overlap=0,
)

loader1 = TextLoader("./data/nlp-keywords.txt")
loader2 = TextLoader("./data/finance-keywords.txt")

split_doc1 = loader1.load_and_split(text_splitter)
split_doc2 = loader2.load_and_split(text_splitter)


DB_PATH = "./chroma-db"

db =Chroma.from_documents(
    documents=split_doc1 + split_doc2,
    embedding=OpenAIEmbeddings(),
    collection_name="my_db",
    persist_directory=DB_PATH
)


result = db.similarity_search("TF IDF 에 대하여 알려줘" )

# print(result)

retriever = db.as_retriever()
search_result = retriever.invoke("Word2Vec 에 대하여 알려줘" )

print(search_result[0])
