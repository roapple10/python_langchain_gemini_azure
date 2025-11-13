import streamlit as st
import google.generativeai as genai
import os
import time
from dotenv import dotenv_values
import tempfile

# 設定頁面配置
st.set_page_config(
    page_title="Gemini 影片與圖片分析",
    page_icon="🎬",
    layout="wide"
)

# 載入環境變數
config = dotenv_values(dotenv_path="../.env")

# 設定 Google API Key
os.environ["GOOGLE_API_KEY"] = config.get("GOOGLE_API_KEY")
os.environ["GEMINI_MODEL_ID"] = config.get("GEMINI_MODEL_ID")

# 初始化 Gemini
if os.environ.get("GOOGLE_API_KEY"):
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
else:
    st.error("⚠️ 請設定 GOOGLE_API_KEY 環境變數")
    st.stop()

# 標題和說明
st.title("🎬 Gemini 影片與圖片分析工具")
st.markdown("""
這個工具可以讓您上傳影片或圖片（或兩者），並使用 Google Gemini AI 來分析內容。
支援的功能：
- 📹 分析影片內容（單獨或結合圖片）
- 🖼️ 分析圖片內容（單獨或結合影片）
- 💬 回答關於影片和圖片的問題
- 🔍 多模態比對分析（同時上傳影片和圖片時）
""")

# 側邊欄 - 設定和說明
with st.sidebar:
    st.header("⚙️ 設定")
    st.info(f"使用模型: {os.environ.get('GEMINI_MODEL_ID', '未設定')}")
    
    st.header("📖 使用說明")
    st.markdown("""
    1. **上傳檔案**（至少一個）：
       - 📹 影片檔案：支援 MP4、MOV 等格式
       - 🖼️ 圖片檔案：支援 JPG、PNG 等格式
    2. **輸入問題**：用繁體中文描述您想了解的問題
    3. **點擊分析**：等待 AI 處理並回傳結果
    
    **注意事項**：
    - 至少需要上傳一個檔案（影片或圖片）
    - 影片上傳後需要等待處理時間
    - 大型檔案可能需要較長時間
    - 建議問題範例：
      - "請問你從影片中看到什麼？"
      - "請詳細地條列出影片中每個人所說的話"
      - "請問影片中有沒有出現圖片裡的這個人，在第幾秒，他說了什麼"
      - "請描述這張圖片的內容"
    """)

# 初始化 session state
if 'uploaded_video_file' not in st.session_state:
    st.session_state.uploaded_video_file = None
if 'uploaded_image_file' not in st.session_state:
    st.session_state.uploaded_image_file = None
if 'video_file_uri' not in st.session_state:
    st.session_state.video_file_uri = None
if 'image_file_uri' not in st.session_state:
    st.session_state.image_file_uri = None
if 'video_file_name' not in st.session_state:
    st.session_state.video_file_name = None
if 'image_file_name' not in st.session_state:
    st.session_state.image_file_name = None
if 'video_file_uploaded' not in st.session_state:
    st.session_state.video_file_uploaded = None
if 'image_file_uploaded' not in st.session_state:
    st.session_state.image_file_uploaded = None

# 檔案上傳區域
col1, col2 = st.columns(2)

with col1:
    st.subheader("📹 上傳影片")
    video_file = st.file_uploader(
        "選擇影片檔案（可選）",
        type=['mp4', 'mov', 'avi', 'mkv'],
        key="video_uploader"
    )
    
    if video_file is not None:
        # 檢查檔案是否改變
        if st.session_state.video_file_name != video_file.name:
            # 檔案改變，清除舊的 URI
            st.session_state.video_file_uri = None
            st.session_state.video_file_uploaded = None
        st.session_state.uploaded_video_file = video_file
        st.session_state.video_file_name = video_file.name
        st.success(f"✅ 已選擇影片: {video_file.name}")
        st.info(f"檔案大小: {video_file.size / (1024*1024):.2f} MB")
        if st.session_state.video_file_uri:
            st.info("💡 檔案已上傳，重複提問時無需重新上傳")

with col2:
    st.subheader("🖼️ 上傳圖片")
    image_file = st.file_uploader(
        "選擇圖片檔案（可選）",
        type=['jpg', 'jpeg', 'png', 'gif', 'webp'],
        key="image_uploader"
    )
    
    if image_file is not None:
        # 檢查檔案是否改變
        if st.session_state.image_file_name != image_file.name:
            # 檔案改變，清除舊的 URI
            st.session_state.image_file_uri = None
            st.session_state.image_file_uploaded = None
        st.session_state.uploaded_image_file = image_file
        st.session_state.image_file_name = image_file.name
        st.success(f"✅ 已選擇圖片: {image_file.name}")
        st.info(f"檔案大小: {image_file.size / (1024*1024):.2f} MB")
        if st.session_state.image_file_uri:
            st.info("💡 檔案已上傳，重複提問時無需重新上傳")

# 問題輸入區域
st.subheader("💬 輸入問題")
prompt = st.text_area(
    "請輸入您想問的問題",
    height=100,
    placeholder="例如：請問你從影片中看到什麼？用繁體中文回答。"
)

# 預設問題範例
st.markdown("**快速問題範例：**")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("範例 1: 影片內容摘要"):
        prompt = "請問你從影片中看到什麼？用繁體中文回答。"
        st.session_state.example_prompt = prompt
with col2:
    if st.button("範例 2: 列出所有對話"):
        prompt = "請詳細地條列出影片中每個人所說的話，用繁體中文回答。"
        st.session_state.example_prompt = prompt
with col3:
    if st.button("範例 3: 比對圖片人物"):
        prompt = "請問影片中有沒有出現圖片裡的這個人，在第幾秒，他說了什麼，用繁體中文回答。"
        st.session_state.example_prompt = prompt

# 如果有選擇範例，更新 prompt
if 'example_prompt' in st.session_state:
    prompt = st.session_state.example_prompt
    del st.session_state.example_prompt

# 分析按鈕
if st.button("🚀 開始分析", type="primary", use_container_width=True):
    # 檢查是否有至少一個檔案上傳
    has_video = st.session_state.uploaded_video_file is not None
    has_image = st.session_state.uploaded_image_file is not None
    
    if not has_video and not has_image:
        st.error("❌ 請至少上傳一個檔案（影片或圖片）！")
    elif not prompt:
        st.error("❌ 請輸入問題！")
    else:
        # 顯示進度
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            video_file_uploaded = None
            image_file_uploaded = None
            tmp_video_path = None
            tmp_image_path = None
            
            # 步驟 1: 上傳影片（如果有且尚未上傳）
            if has_video:
                if st.session_state.video_file_uploaded and st.session_state.video_file_uri:
                    # 重用已上傳的檔案
                    status_text.text("♻️ 檢查已上傳的影片檔案...")
                    progress_bar.progress(30)
                    try:
                        # 檢查檔案狀態
                        video_file_uploaded = genai.get_file(st.session_state.video_file_uploaded.name)
                        if video_file_uploaded.state.name == "ACTIVE":
                            status_text.text("✅ 使用已上傳的影片檔案")
                            progress_bar.progress(60)
                            st.session_state.video_file_uploaded = video_file_uploaded
                        else:
                            # 如果檔案狀態異常，清除快取並重新上傳
                            st.session_state.video_file_uri = None
                            st.session_state.video_file_uploaded = None
                            video_file_uploaded = None
                    except Exception:
                        # 如果無法取得檔案，清除快取並重新上傳
                        st.session_state.video_file_uri = None
                        st.session_state.video_file_uploaded = None
                        video_file_uploaded = None
                
                # 如果沒有可重用的檔案，需要上傳新檔案
                if not video_file_uploaded:
                    # 需要上傳新檔案
                    status_text.text("📤 正在上傳影片檔案...")
                    progress_bar.progress(10)
                    
                    # 將上傳的檔案保存到臨時檔案
                    video_ext = os.path.splitext(st.session_state.uploaded_video_file.name)[1] or ".mp4"
                    with tempfile.NamedTemporaryFile(delete=False, suffix=video_ext) as tmp_video:
                        tmp_video.write(st.session_state.uploaded_video_file.read())
                        tmp_video_path = tmp_video.name
                    
                    video_file_uploaded = genai.upload_file(path=tmp_video_path)
                    st.session_state.video_file_uri = video_file_uploaded.uri
                    st.session_state.video_file_uploaded = video_file_uploaded
                    progress_bar.progress(30)
                    status_text.text(f"✅ 影片上傳完成: {video_file_uploaded.uri}")
                    
                    # 等待影片處理
                    status_text.text("⏳ 等待影片處理中...")
                    progress_bar.progress(40)
                    
                    while video_file_uploaded.state.name == "PROCESSING":
                        time.sleep(5)
                        video_file_uploaded = genai.get_file(video_file_uploaded.name)
                        status_text.text("⏳ 影片處理中，請稍候...")
                    
                    if video_file_uploaded.state.name == "FAILED":
                        st.error("❌ 影片處理失敗！")
                        st.stop()
                    
                    # 更新 session state
                    st.session_state.video_file_uploaded = video_file_uploaded
                    progress_bar.progress(60)
                    status_text.text("✅ 影片處理完成！")
            
            # 步驟 2: 上傳圖片（如果有且尚未上傳）
            if has_image:
                if st.session_state.image_file_uploaded and st.session_state.image_file_uri:
                    # 重用已上傳的檔案
                    if has_video:
                        progress_bar.progress(70)
                    else:
                        progress_bar.progress(30)
                    status_text.text("♻️ 檢查已上傳的圖片檔案...")
                    try:
                        # 檢查檔案狀態
                        image_file_uploaded = genai.get_file(st.session_state.image_file_uploaded.name)
                        if image_file_uploaded.state.name == "ACTIVE":
                            if has_video:
                                progress_bar.progress(80)
                            else:
                                progress_bar.progress(60)
                            status_text.text("✅ 使用已上傳的圖片檔案")
                            st.session_state.image_file_uploaded = image_file_uploaded
                        else:
                            # 如果檔案狀態異常，清除快取並重新上傳
                            st.session_state.image_file_uri = None
                            st.session_state.image_file_uploaded = None
                            image_file_uploaded = None
                    except Exception:
                        # 如果無法取得檔案，清除快取並重新上傳
                        st.session_state.image_file_uri = None
                        st.session_state.image_file_uploaded = None
                        image_file_uploaded = None
                else:
                    image_file_uploaded = None
                
                # 如果沒有可重用的檔案，需要上傳新檔案
                if not image_file_uploaded:
                    if has_video:
                        progress_bar.progress(70)
                    else:
                        progress_bar.progress(30)
                    
                    status_text.text("📤 正在上傳圖片檔案...")
                    
                    image_ext = os.path.splitext(st.session_state.uploaded_image_file.name)[1] or ".jpg"
                    with tempfile.NamedTemporaryFile(delete=False, suffix=image_ext) as tmp_image:
                        tmp_image.write(st.session_state.uploaded_image_file.read())
                        tmp_image_path = tmp_image.name
                    
                    image_file_uploaded = genai.upload_file(path=tmp_image_path)
                    st.session_state.image_file_uri = image_file_uploaded.uri
                    st.session_state.image_file_uploaded = image_file_uploaded
                    
                    if has_video:
                        progress_bar.progress(80)
                    else:
                        progress_bar.progress(60)
                    
                    status_text.text("✅ 圖片上傳完成！")
            
            # 步驟 3: 生成回應
            status_text.text("🤖 Gemini AI 正在思考中...")
            progress_bar.progress(90)
            
            model = genai.GenerativeModel(model_name=os.environ["GEMINI_MODEL_ID"])
            
            # 準備輸入內容，添加中文回答要求
            # 檢查 prompt 是否已經包含中文回答要求
            chinese_instruction = "請用繁體中文回答。"
            if chinese_instruction not in prompt and "中文" not in prompt and "繁體" not in prompt:
                prompt_with_chinese = f"{prompt}\n\n{chinese_instruction}"
            else:
                prompt_with_chinese = prompt
            
            content = [prompt_with_chinese]
            if image_file_uploaded:
                content.append(image_file_uploaded)
            if video_file_uploaded:
                content.append(video_file_uploaded)
            
            response = model.generate_content(
                content, 
                request_options={"timeout": 600}
            )
            
            progress_bar.progress(100)
            status_text.text("✅ 分析完成！")
            
            # 顯示結果
            st.success("🎉 分析完成！")
            st.subheader("📋 分析結果")
            st.markdown("---")
            st.markdown(response.text)
            
            # 清理臨時檔案
            if tmp_video_path:
                os.unlink(tmp_video_path)
            if tmp_image_path:
                os.unlink(tmp_image_path)
            
        except Exception as e:
            st.error(f"❌ 發生錯誤: {str(e)}")
            st.exception(e)
        finally:
            time.sleep(1)
            progress_bar.empty()
            status_text.empty()

# 顯示已上傳的檔案資訊
if st.session_state.video_file_uri or st.session_state.image_file_uri:
    st.markdown("---")
    st.subheader("📎 已上傳的檔案")
    if st.session_state.video_file_uri:
        st.info(f"影片 URI: {st.session_state.video_file_uri}")
    if st.session_state.image_file_uri:
        st.info(f"圖片 URI: {st.session_state.image_file_uri}")

# 頁尾
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Powered by Google Gemini AI | Streamlit</p>
</div>
""", unsafe_allow_html=True)

