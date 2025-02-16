# Chroma

## Cue Column

- TextLoader는 언제 쓰는가?
- load_and_split: 데이터를 로드하고, 분할해주는 함수
- VectorStore 생성하는 방법 (from_documents, from_texts)
- 벡터 스토어 생성시, 엠베딩 모델이 사용된다.
- persist_directory 옵션을 통해서 데이터베이스를 로컬디스크에 만들 수 있습니다.
- 로컬에 저장한 벡터스토어를 로드하는 방법은?
- 벡터스토어 통해서 유사도 검색 수행하기.
- 유사도 검색이란 주어진 쿼리와 가장 유사한 문서를 반환하는 것.
- Chrome 벡터 스토어에서는 similarity_search 메소드를 사용한다.
- k는 반환할 결과의 개수를 의미한다.
- 벡터 저장소를 만들고 이 후에 문서를 추가하려면 add_documents, add_texts 메소드를 사용한다.
- 문서 삭제는 delete 메소드를 사용한다.
- 벡터 저장소 통해서 retriever 생성할 수 있습니다. as_retriever 메소드를 사용한다.
