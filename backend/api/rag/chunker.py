from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_chunker():
    """
    Returns a configured text splitter.
    Chunk size 1000 with 200 overlap is standard for semantic search.
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
