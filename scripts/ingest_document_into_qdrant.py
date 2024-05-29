from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Qdrant

from src.constants import INPUT_DATA_FOLDER
from src.document_ingestion.split_documents import split_pdf_into_chunks

embeddings = OpenAIEmbeddings()


document_paths = (INPUT_DATA_FOLDER / "documents").glob("*.pdf")
texts = []
for document_path in document_paths:
    texts.extend(split_pdf_into_chunks(document_path))

doc_store = Qdrant.from_documents(
    texts,
    embeddings,
    url="<qdrant-url>",
    api_key="<qdrant-api-key>",
    collection_name="texts",
)
