from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_chunker():

    return RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200, 
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
