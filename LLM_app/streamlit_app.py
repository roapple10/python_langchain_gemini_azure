# https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/llm-quickstart

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import dotenv_values

# 嘗試從 .env 檔案讀取設定
config = dotenv_values(dotenv_path="../.env")

# 設定 Google API Key（從 .env 或使用者輸入）
env_api_key = config.get("GOOGLE_API_KEY", "")
env_model_id = config.get("GEMINI_MODEL_ID", "gemini-2.0-flash-exp")

st.title("🦜🔗 Gemini Quickstart App")

# 側邊欄輸入 Google API Key（如果 .env 沒有設定）
google_api_key = st.sidebar.text_input(
    "Google API Key", 
    value=env_api_key,
    type="password",
    help="如果已在 .env 檔案中設定，會自動載入"
)

# 選擇模型
model_id = st.sidebar.selectbox(
    "選擇 Gemini 模型",
    options=["gemini-2.0-flash-exp", "gemini-2.5-flash", "gemini-2.5-pro"],
    index=0 if env_model_id == "gemini-2.0-flash-exp" else 0
)

def generate_response(input_text):
    """使用 Gemini 生成回應"""
    # 設定環境變數
    os.environ["GOOGLE_API_KEY"] = google_api_key
    os.environ["GEMINI_MODEL_ID"] = model_id
    
    model = ChatGoogleGenerativeAI(
        model=os.environ["GEMINI_MODEL_ID"],
        temperature=0.7,
    )
    response = model.invoke(input_text)
    st.info(response.content)

with st.form("my_form"):
    text = st.text_area(
        "輸入文字:",
        "請告訴我學習程式設計的三個關鍵建議是什麼？",
    )
    submitted = st.form_submit_button("送出")
    
    if not google_api_key:
        st.warning("請輸入您的 Google API Key！", icon="⚠")
    
    if submitted and google_api_key:
        generate_response(text)

