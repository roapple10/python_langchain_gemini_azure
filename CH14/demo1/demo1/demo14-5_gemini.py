
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from datetime import datetime
from typing import List, Dict
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pathlib import Path

import os
from dotenv import dotenv_values
# 基於當前文件位置構建絕對路徑到專案根目錄的 .env
env_path = Path(__file__).parent.parent.parent.parent / ".env"
config = dotenv_values(dotenv_path=str(env_path))

# 設定 Google API Key
os.environ["GOOGLE_API_KEY"] = config.get("GOOGLE_API_KEY")
os.environ["GEMINI_MODEL_ID"] = config.get("GEMINI_MODEL_ID")

# 初始化語言模型
llm = ChatGoogleGenerativeAI(
    model=os.environ["GEMINI_MODEL_ID"],
    temperature=0.2
)

# 模擬房間的可用資料
rooms_availability: List[Dict] =  [
    {"roomno":"001","roomtype":"雙人房","available_date":"2025/11/30"},
    {"roomno":"001","roomtype":"雙人房","available_date":"2025/12/02"},
    {"roomno":"002","roomtype":"單人房","available_date":"2025/11/30"},
    {"roomno":"002","roomtype":"單人房","available_date":"2025/12/03"},
    {"roomno":"003","roomtype":"雙人房","available_date":"2025/11/30"},
    {"roomno":"003","roomtype":"雙人房","available_date":"2025/12/01"},
    {"roomno":"003","roomtype":"雙人房","available_date":"2025/11/29"},
    {"roomno":"003","roomtype":"雙人房","available_date":"2025/12/09"},
    {"roomno":"003","roomtype":"雙人房","available_date":"2025/12/10"}
]

# 取得當前日期
@tool
def get_current_date() -> str:
    """
    取得今天日期。

    返回:
    str: 今天日期，格式為 YYYY/MM/DD
    """
    return datetime.now().strftime("%Y/%m/%d")

# 客戶評價
@tool
def get_customer_service_chain(input: str) -> str:
    """
    回應客戶評論。

    參數:
    input (str): 客戶提交的評論

    返回:
    str: 根據客戶評論的情感回應
    """
    system_prompt ="""
    請分析客戶評論的情感是正面(positiv)還是負面(negative)。
    
    ### 請注意：
    當客戶提供了正面評論時，請以感謝的態度回應這個評論。
    當客戶提供了負面評論時，請以安撫和道歉的態度回應這個評論。
    """
    prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

    response_chain = prompt | llm | StrOutputParser()
    return response_chain.invoke(input=input)


# 查詢指定日期的可用房間
@tool
def check_room_availability(date: str) -> str:
    """
    查詢指定日期的可用房間。

    參數:
    date (str): 查詢日期，格式為 YYYY/MM/DD

    返回:
    str: 可用房間的資訊，如果沒有可用房間則返回無可預訂空房的訊息
    """
    try:
        # 驗證日期格式
        query_date = datetime.strptime(date, "%Y/%m/%d")
    except ValueError:
        return "日期格式不正確，請使用 YYYY/MM/DD 格式。"

    available_rooms = [
            room for room in rooms_availability 
            if datetime.strptime(room["available_date"], "%Y/%m/%d").date() == query_date.date()
        ]

    if not available_rooms:
        return f"抱歉，{date} 沒有可預訂的房間。"

    result = f"{date} 可預訂的房間如下：\n"
    for room in available_rooms:
        result += f"房間號碼：{room['roomno']}，類型：{room['roomtype']}\n"

    return result

# 輸出LLM回應過程
def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

# 設定工具
tools = [get_current_date,check_room_availability,get_customer_service_chain]

# 加入 chat memory
memory = MemorySaver()

# 建立Agent
agent_prompt="你是酒店客戶經理，可以幫客人查詢空房資訊以及回覆客戶意見，並且回覆時請同時回應繁體中文以及英文二個語言資料。"
agent = create_react_agent(llm, tools=tools, checkpointer=memory, state_modifier=agent_prompt)

# Agent 啟動
config = {"configurable": {"thread_id": "168"}}

# 顯示示例輸入
print("=" * 60)
print("酒店訂房系統 - 示例輸入：")
print("=" * 60)
print("1. 可以預訂明天住宿嗎")
print("2. 我剛預訂了什麼時候的房間")
print("3. 你們的服務真的很是太棒了！")
print("4. 查詢 2025/12/01 的可用房間")
print("5. 今天的日期是什麼？")
print("=" * 60)
print("\n請輸入您的問題（輸入 'quit' 或 'exit' 結束）：\n")

# 用戶輸入循環
while True:
    user_input = input("您：").strip()
    
    if not user_input:
        continue
    
    if user_input.lower() in ['quit', 'exit', '退出', '結束']:
        print("\n感謝使用，再見！")
        break
    
    inputs = {"messages": [("user", user_input)]}
    print("\n系統回應：")
    print_stream(agent.stream(inputs, config=config, stream_mode="values"))
    print("\n" + "-" * 60 + "\n")

