import google.generativeai as genai
import os
from dotenv import dotenv_values
config = dotenv_values(dotenv_path="../.env")

# 設定 Google API Key
os.environ["GOOGLE_API_KEY"] = config.get("GOOGLE_API_KEY")
os.environ["GEMINI_MODEL_ID"] = config.get("GEMINI_MODEL_ID")

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel(
    model_name=os.environ["GEMINI_MODEL_ID"],
)

# 輸入一個問題
user_input = "如何獲得幸福人生？"

response = model.generate_content(
    user_input,
)

print("Q: " + user_input)
print("A: " + response.text)
