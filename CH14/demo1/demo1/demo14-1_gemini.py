
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from datetime import datetime
from typing import List, Dict
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
tools = [get_current_date,check_room_availability]
# 建立Agent
agent = create_react_agent(llm, tools=tools)

# Agent 啟動
inputs = {"messages": [("user", "可以預約明天的住宿嗎")]}
print_stream(agent.stream(inputs, stream_mode="values"))

