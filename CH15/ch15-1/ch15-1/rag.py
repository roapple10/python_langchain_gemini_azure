from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from pathlib import Path
from dotenv import dotenv_values
import os
import sys

# 尋找 .env 檔案
# 優先順序：
# 1. /app/.env (Docker 容器中的掛載位置)
# 2. python_langchain_gemini_azure/.env (專案根目錄)
# 3. 當前目錄的 .env
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent.parent  # python_langchain_gemini_azure/

env_paths = [
    Path("/app/.env"),                    # Docker 容器中的位置
    project_root / ".env",                # python_langchain_gemini_azure/.env
    current_file.parent / ".env",         # ch15-1/ch15-1/.env
    current_file.parent.parent / ".env",  # ch15-1/.env
]

config = {}
env_path = None
for path in env_paths:
    if path.exists():
        env_path = path
        config = dotenv_values(dotenv_path=str(path))
        break

if not config:
    print(f"錯誤：找不到 .env 檔案。已嘗試以下路徑：")
    for path in env_paths:
        print(f"  - {path}")
    sys.exit(1)

# 驗證並設定環境變數
required_vars = {
    "GOOGLE_API_KEY": "GOOGLE_API_KEY",
    "GEMINI_MODEL_ID": "GEMINI_MODEL_ID",
    "QDRANT_URL": "QDRANT_URL",
    "QDRANT_API_KEY": "QDRANT_API_KEY",
}

missing_vars = []
for key, env_key in required_vars.items():
    value = config.get(key)
    if not value:
        missing_vars.append(key)
    else:
        os.environ[env_key] = value

if missing_vars:
    print(f"錯誤：.env 檔案中缺少以下必要的環境變數：")
    for var in missing_vars:
        print(f"  - {var}")
    print(f"\n.env 檔案位置：{env_path}")
    sys.exit(1)

qdrant_url = config.get("QDRANT_URL")
qdrant_api_key = config.get("QDRANT_API_KEY")

# Load PDF文件 - 參考 demo10-1_gemini.py 的路徑處理方式
pdf_path = Path(__file__).parent.parent / "qa.pdf"
loader = PyPDFLoader(str(pdf_path))
docs = loader.load()

# 分割文本
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_documents(docs)

# 初始化 Google Gemini Embeddings
embeddings_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.environ["GOOGLE_API_KEY"],
)


# 使用新版 QdrantVectorStore (langchain-qdrant)
qdrant = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings_model,
    url=qdrant_url,
    api_key=qdrant_api_key,
    collection_name="subsidy_qa",
    force_recreate=True,
)


retriever = qdrant.as_retriever(search_kwargs={"k": 3})

# 初始化 Google Gemini Chat Model
model = ChatGoogleGenerativeAI(
    model=os.environ["GEMINI_MODEL_ID"],
    temperature=0,
)

prompt = ChatPromptTemplate.from_template("""請回答依照 context 裡的資訊來回答問題:
<context>
{context}
</context>
Question: {input}""")


document_chain = create_stuff_documents_chain(model, prompt)

retrieval_chain = create_retrieval_chain(retriever, document_chain)

response = retrieval_chain.invoke({"input": "請問第二胎補助加發多少，共為多少錢？"})

print(response["answer"])
