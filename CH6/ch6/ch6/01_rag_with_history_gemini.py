#以筆者們的上一本書「極速ChatGPT開發者兵器指南」做為retrival資料來源的範例
#https://www.drmaster.com.tw/bookinfo.asp?BookID=MP22359


from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from dotenv import dotenv_values
import os

config = dotenv_values(dotenv_path="../../.env")

# 設定 Google API Key
os.environ["GOOGLE_API_KEY"] = config.get("GOOGLE_API_KEY")
os.environ["GEMINI_MODEL_ID"] = config.get("GEMINI_MODEL_ID")

qdrant_url = config.get("QDRANT_URL")
qdrant_api_key = config.get("QDRANT_API_KEY")

loader = WebBaseLoader("https://www.drmaster.com.tw/bookinfo.asp?BookID=MP22359")

docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)

model = ChatGoogleGenerativeAI(
    model=os.environ["GEMINI_MODEL_ID"],
    temperature=0,
)

embeddings_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.environ["GOOGLE_API_KEY"],
)

qdrant = Qdrant.from_documents(
    documents,
    embeddings_model,
    url=qdrant_url, 
    api_key=qdrant_api_key,
    collection_name="book",
    force_recreate=True,
)

retriever = qdrant.as_retriever()

prompt = ChatPromptTemplate.from_messages([
    ("system", "請回答依照 context 裡的資訊來回答問題:{context}。問題{input}"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
    ])

document_chain = create_stuff_documents_chain(model, prompt)

retrieval_chain = create_retrieval_chain(retriever, document_chain)

def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, "sqlite:///./langchain.db")

chain_with_history = RunnableWithMessageHistory(
    retrieval_chain,
    get_session_history,
    input_messages_key="input",
    output_messages_key="answer",
    history_messages_key="history",
)

config = {"configurable": {"session_id": "1"}}


response = chain_with_history.invoke({"input": "請問這本書的作者？"}, config=config)
print(response["answer"])

response = chain_with_history.invoke({"input": "我剛剛的問題是什麼"}, config=config)
print(response["answer"])

