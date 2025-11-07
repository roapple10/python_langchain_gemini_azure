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

sentiment_prompt = ChatPromptTemplate.from_template("分析以下文本的情感傾向，你的回答必須使用繁體中文並且使用台灣慣用語: {text}")
topic_prompt = ChatPromptTemplate.from_template("提取以下文本的主要主題，你的回答必須使用繁體中文並且使用台灣慣用語: {text}")
summary_prompt = ChatPromptTemplate.from_template("為以下文本生成一個簡短的摘要，你的回答必須使用繁體中文並且使用台灣慣用語: {text}")

sentiment_chain = sentiment_prompt | llm | StrOutputParser()
topic_chain = topic_prompt | llm | StrOutputParser()
summary_chain = summary_prompt | llm | StrOutputParser()

# 建立 RunnableParallel
text_analyzer = RunnableParallel(
    sentiment=sentiment_chain,
    topic=topic_chain,
    summary=summary_chain
)

text = "上個星期入住了這家飯店，整體感覺還不錯，服務人員態度很好，房間也很乾淨，下次還會再來。"
results = text_analyzer.invoke({"text": text})

print("情感分析:", results["sentiment"])
print("主題:", results["topic"])
print("摘要:", results["summary"])

