import os
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from IPython.display import Image, display
from dotenv import dotenv_values

config = dotenv_values(dotenv_path="../.env")

# 設定 Google API Key
os.environ["GOOGLE_API_KEY"] = config.get("GOOGLE_API_KEY")
os.environ["GEMINI_MODEL_ID"] = config.get("GEMINI_MODEL_ID")

llm = ChatGoogleGenerativeAI(
    model=os.environ.get("GEMINI_MODEL_ID", "gemini-1.5-flash-latest")
)

user_messages = []
# append user input question
user_input = "圖片中的生物是什麼？"
user_messages.append({"type": "text", "text": user_input + "請使用繁體中文回答。"})
# append images
image_url = "https://i.ibb.co/KyNtMw5/IMG-20240321-172354614-AE.jpg"
user_messages.append({"type": "image_url", "image_url": image_url})
human_messages = HumanMessage(content=user_messages)
result = llm.invoke([human_messages])

print("Q: " + user_input)
print("A: " + result.content)

# Display the image
display(Image(url=image_url))
