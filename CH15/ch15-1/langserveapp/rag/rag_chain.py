from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
import os
import sys

# 嘗試多個 .env 檔案位置
env_paths = [

    Path("../../../.env"),        # python_langchain_gemini_azure/.env
]

env_loaded = False
for env_path in env_paths:
    if env_path.exists():
        load_dotenv(env_path)
        print(f"已載入 .env 檔案: {env_path}")
        env_loaded = True
        break

if not env_loaded:
    # 如果都沒找到，嘗試從環境變數載入（Docker 可能透過 -e 傳入）
    load_dotenv()
    print("未找到 .env 檔案，使用系統環境變數")

google_api_key = os.getenv("GOOGLE_API_KEY")
gemini_model_id = os.getenv("GEMINI_MODEL_ID")
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

# 檢查必要的環境變數
missing_vars = []
if not google_api_key:
    missing_vars.append("GOOGLE_API_KEY")
if not gemini_model_id:
    missing_vars.append("GEMINI_MODEL_ID")
if not qdrant_url:
    missing_vars.append("QDRANT_URL")
if not qdrant_api_key:
    missing_vars.append("QDRANT_API_KEY")

if missing_vars:
    print(f"錯誤：缺少以下環境變數: {', '.join(missing_vars)}")
    print("請確認 .env 檔案已正確掛載到 /code/.env")
    sys.exit(1)

print(f"QDRANT_URL: {qdrant_url}")
print(f"GEMINI_MODEL_ID: {gemini_model_id}")

# 初始化 Google Gemini Embeddings
embeddings_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=google_api_key,
)

client = QdrantClient(
    url=qdrant_url, 
    api_key=qdrant_api_key
)

collection_name = "subsidy_qa"
qdrant = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
    embedding=embeddings_model,
)

retriever = qdrant.as_retriever(search_kwargs={"k": 3})

# 初始化 Google Gemini Chat Model
model = ChatGoogleGenerativeAI(
    model=gemini_model_id,
    temperature=0,
)

prompt = ChatPromptTemplate.from_template("""請回答依照 context 裡的資訊來回答問題:
<context>
{context}
</context>
Question: {input}""")


document_chain = create_stuff_documents_chain(model, prompt)

retrieval_chain = create_retrieval_chain(retriever, document_chain)

# Add typing for input
class Question(BaseModel):
    input: str


rag_chain = retrieval_chain.with_types(input_type=Question)

print("RAG Chain 初始化完成")
