# https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/llm-quickstart

import streamlit as st
from langchain_core.runnables import RunnableSequence, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import dotenv_values

# 讀取 .env 設定
config = dotenv_values(dotenv_path="../.env")
env_api_key = config.get("GOOGLE_API_KEY", "")
env_model_id = config.get("GEMINI_MODEL_ID", "gemini-2.0-flash-exp")

st.title("🎴 Gemini 對聯生成器")

# 側邊欄輸入 Google API Key
google_api_key = st.sidebar.text_input(
    "Google API Key",
    value=env_api_key,
    type="password",
    help="如果已在 .env 檔案中設定，會自動載入"
)

# 側邊欄選擇模型
model_id = st.sidebar.selectbox(
    "選擇 Gemini 模型",
    options=["gemini-2.0-flash-exp", "gemini-2.5-flash", "gemini-2.5-pro"],
    index=0 if env_model_id == "gemini-2.0-flash-exp" else 0
)

# 寫作風格範例
style_examples = """
1. 一鄉二里，共三夫子不識四書五經六義，竟敢教七八九子，十分大膽
2. 十室九貧，湊得八兩七錢六分五毫四厘，尚且又三心二意，一等下流
3. 圖畫裡，龍不吟，虎不嘯，小小書童可笑可笑
4. 棋盤裡，車無輪，馬無韁，叫聲將軍提防提防
5. 鶯鶯燕燕翠翠紅紅處處融融洽洽
6. 雨雨風風花花葉葉年年暮暮朝朝
"""

# 提示樣板
writing_template = ChatPromptTemplate.from_template("""
你是一位精通對聯創作的文學大師。請根據以下提供的主題創作一組對聯。

主題: {topic}

請參考以下的寫作風格範例，創作時要體現類似的韻律感和文字技巧：

{style_examples}

要求：
1. 創作一組對仗工整、意境深遠的對聯
2. 對聯應與給定主題相關
3. 儘量融入範例中展現的數字遞進、重複疊字等修辭技巧
4. 確保對聯在音律和結構上和諧統一

請提供：
- 上聯
- 下聯
- 簡短解釋（說明對聯與主題的關聯，以及使用的技巧）
""")

# 對聯分析函數
def analyze_couplet(couplet):
    lines = couplet.split('\n')
    if len(lines) < 2:
        return {"error": "無法識別完整對聯"}
    upper = lines[0].split('：')[-1].strip()
    lower = lines[1].split('：')[-1].strip()
    word_count = len(upper)
    char_set = set(upper + lower)
    repeated_chars = [char for char in char_set if (upper + lower).count(char) > 1]
    return {
        "字數": word_count,
        "獨特字元數": len(char_set),
        "重複字元": ', '.join(repeated_chars),
        "上聯": upper,
        "下聯": lower
    }

# 建立對聯生成系統
def get_couplet_system(api_key, model_id):
    os.environ["GOOGLE_API_KEY"] = api_key
    os.environ["GEMINI_MODEL_ID"] = model_id
    llm = ChatGoogleGenerativeAI(
        model=os.environ["GEMINI_MODEL_ID"],
        temperature=0.8,
    )
    return RunnableSequence(
        {
            "topic": RunnablePassthrough(),
            "style_examples": lambda _: style_examples
        },
        writing_template,
        llm,
        lambda x: {"content": x.content},
        RunnablePassthrough.assign(
            analysis=lambda x: analyze_couplet(x["content"])
        ),
        lambda x: {
            "content": x["content"],
            "analysis": x["analysis"],
        }
    )

with st.form("couplet_form"):
    topic = st.text_input("請輸入主題", "生成式AI")
    submitted = st.form_submit_button("生成對聯")
    if not google_api_key:
        st.warning("請輸入您的 Google API Key！", icon="⚠")
    elif submitted and google_api_key:
        couplet_system = get_couplet_system(google_api_key, model_id)
        result = couplet_system.invoke({"topic": topic})
        st.subheader("生成結果")
        st.write(result["content"])
        st.subheader("分析結果")
        st.json(result["analysis"], expanded=False)

