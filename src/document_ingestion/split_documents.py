from pathlib import Path


def split_documents_into_chunks(document_path: Path):
    match document_path.suffix:
        case ".pdf":
            return split_pdf_into_chunks(document_path)
        case _:
            raise ValueError(f"Unsupported document type: {document_path.suffix}")


def split_pdf_into_chunks(document_path: Path):
    from langchain_community.document_loaders import PyPDFLoader

    loader = PyPDFLoader(document_path)
    pages = loader.load_and_split()
    return pages
