# %%
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Qdrant

from src.constants import DATA_FOLDER_PATH, INPUT_DATA_FOLDER
from src.document_ingestion.split_documents import split_pdf_into_chunks

embeddings = OpenAIEmbeddings()


document_paths = (INPUT_DATA_FOLDER / "documents").glob("*.pdf")
vector_store_path = DATA_FOLDER_PATH / "qdrant"
vector_store_path.mkdir(exist_ok=True, parents=True)
texts = []
for document_path in document_paths:
    texts.extend(split_pdf_into_chunks(document_path))


doc_store = Qdrant.from_documents(
    texts,
    embeddings,
    path=vector_store_path,
    collection_name="texts",
)


# %%
