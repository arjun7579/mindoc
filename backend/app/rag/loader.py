import os
from langchain_community.document_loaders import PyMuPDFLoader, UnstructuredPowerPointLoader
from langchain_core.documents import Document
from typing import List

def load_document(file_path: str) -> List[Document]:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        # PyMuPDF is faster and preserves math symbols better than PyPDF
        loader = PyMuPDFLoader(file_path)
    elif ext in [".ppt", ".pptx"]:
        loader = UnstructuredPowerPointLoader(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    return loader.load()
