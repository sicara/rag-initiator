# %%
from langchain.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient

from src.constants import DATA_FOLDER_PATH

vector_store_path = DATA_FOLDER_PATH / "qdrant"
embeddings = OpenAIEmbeddings()
client = QdrantClient(path=str(vector_store_path))
db = Qdrant(client=client, collection_name="texts", embeddings=embeddings)

db.similarity_search(query="hello world", k=5)

# %%
