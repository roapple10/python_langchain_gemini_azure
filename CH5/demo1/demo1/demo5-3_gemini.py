from langchain_core.runnables import RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

import os
from dotenv import dotenv_values

config = dotenv_values(dotenv_path="../../.env")

# 設定 Google API Key
os.environ["GOOGLE_API_KEY"] = config.get("GOOGLE_API_KEY")
os.environ["GEMINI_MODEL_ID"] = config.get("GEMINI_MODEL_ID")

# 初始化語言模型
llm = ChatGoogleGenerativeAI(
    model=os.environ["GEMINI_MODEL_ID"],
    temperature=0.7,
)

english_prompt = ChatPromptTemplate.from_template("你是一位英文語言專家，請將以下短文翻譯成英文 : {text}")
japan_prompt = ChatPromptTemplate.from_template("你是一位日文語言專家，請將以下短文翻譯成日文 : {text}")
french_prompt = ChatPromptTemplate.from_template("你是一位法語語言專家，請將以下短文翻譯成法文 : {text}")

english_chain = english_prompt | llm | StrOutputParser()
japan_chain = japan_prompt | llm | StrOutputParser()
french_chain = french_prompt | llm | StrOutputParser()

# 建立 RunnableParallel
text_analyzer = RunnableParallel(
    english=english_chain,
    japan=japan_chain,
    french=french_chain
)

text = "生成式人工智慧是一種人工智慧系統,能夠產生文字、圖像或其他媒體,而提示工程將大大的影響其生成結果。"
results = text_analyzer.invoke({"text": text})

print("英文:", results["english"])
print("日文:", results["japan"])
print("法文:", results["french"])

