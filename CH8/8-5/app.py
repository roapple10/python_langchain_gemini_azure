import google.generativeai as genai
import os
from dotenv import dotenv_values

config = dotenv_values(dotenv_path="../.env")

# 設定 Google API Key
os.environ["GOOGLE_API_KEY"] = config.get("GOOGLE_API_KEY")
os.environ["GEMINI_MODEL_ID"] = config.get("GEMINI_MODEL_ID")

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


# Upload the singla audio file
script_dir = os.path.dirname(os.path.abspath(__file__))
audio_file_name = os.path.join(script_dir, "radio.mp3")
print(f"Uploading file...")
audio_file = genai.upload_file(path=audio_file_name)
print(f"Completed upload: {audio_file.uri}")

prompt = """
請仔細聆聽以下的音檔，再寫下這個聲音檔的重要內容摘要。
"""

model = genai.GenerativeModel(
    model_name=os.environ["GEMINI_MODEL_ID"],
    system_instruction="使用繁體中文回答。"
)
response = model.generate_content([prompt, audio_file])
print(response.text)


# 沒有要再問問題時，再把檔案從雲端刪除
# genai.delete_file(audio_file.name)
# print(f"Deleted file {audio_file.uri}")
