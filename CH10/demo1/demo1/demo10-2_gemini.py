from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant
from pathlib import Path

import os
from dotenv import dotenv_values
# 基於當前文件位置構建絕對路徑到專案根目錄的 .env
env_path = Path(__file__).parent.parent.parent.parent / ".env"
config = dotenv_values(dotenv_path=str(env_path))

# 設定 Google API Key
os.environ["GOOGLE_API_KEY"] = config.get("GOOGLE_API_KEY")
os.environ["GEMINI_MODEL_ID"] = config.get("GEMINI_MODEL_ID")

qdrant_url = config.get("QDRANT_URL")
qdrant_api_key = config.get("QDRANT_API_KEY")

# 初始化語言模型
generator_llm = ChatGoogleGenerativeAI(
    model=os.environ["GEMINI_MODEL_ID"],
    temperature=0,
)

embedding_llm = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.environ["GOOGLE_API_KEY"],
)

# ----- 第一次要把知識文件加入Qdrant 向量資料庫時，執行以下程式碼 -----

# # Load PDF文件
# loader = PyPDFLoader("../docs/勞動基準法.pdf")
# pages = loader.load_and_split()

# # 分割文本
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# splits = text_splitter.split_documents(pages)

# # Qdrant向量資料庫
# qdrant = Qdrant.from_documents(
#     splits,
#     embedding_llm,
#     url=qdrant_url,
#     api_key=qdrant_api_key,
#     collection_name="km_docs",
# )

#---------------------------------------------------------




# ------- 後續查詢時，已有向量資料，請執行以下程式碼 -------

# Qdrant client
client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
collection_name = "km_docs"
qdrant = Qdrant(client, collection_name, embedding_llm)

# -------------------------------------------------------


# 設置檢索器
retriever = qdrant.as_retriever(search_kwargs={"k": 3}) # 檢索前3個最相似的文檔

# 建立提示樣板
q_template = ChatPromptTemplate.from_template("""你是一位精通台灣勞基法的專家。請根據以下參考資料回答問題：

參考資料：{context}

問題：{question}

專家回答：""")

# 建立 QA Chain
qa_chain = (
    {
        "context": retriever ,
        "question": RunnablePassthrough(),
    }
    | q_template
    | generator_llm
    | StrOutputParser()
)


# 步驟 7: 進行查詢
response = qa_chain.invoke("勞工加班費的計算方式是什麼？")

print(response)

