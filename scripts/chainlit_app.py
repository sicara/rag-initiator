# %%
import chainlit as cl
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable.config import RunnableConfig
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant
from src.constants import DATA_FOLDER_PATH

from langchain_core.runnables import RunnablePassthrough

@cl.on_chat_start
async def on_chat_start() -> None:
    model = ChatOpenAI(streaming=True)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You're a jedi. You answer wisely.",
            ),
            ("human", "{question}"),
        ]
    )
    vector_store_path = DATA_FOLDER_PATH / "qdrant"
    embeddings = OpenAIEmbeddings()
    client = QdrantClient(path=str(vector_store_path))
    vector_collection = Qdrant(client=client, collection_name="texts", embeddings=embeddings)
    
    retriever = vector_collection.as_retriever(
    search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5}
)
    parralel = {"context": retriever, "question": RunnablePassthrough()}

    runnable = parralel | prompt | model | StrOutputParser() 
    cl.user_session.set("runnable", runnable)
    cl.user_session.set("vector_collection", vector_collection)

@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable

    msg = cl.Message(content="")
    vector_collection = cl.user_session.get("vector_collection")
    async for chunk in runnable.astream(
        message.content    
    ,
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()
