"""
Streamlit UI for AI-Translate
"""
import streamlit as st
import requests
import time
from pathlib import Path
import os

# Page config
st.set_page_config(
    page_title="AI-Translate",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
        font-weight: 600;
    }
    .result-box {
        background-color: #0f3460;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #00d4ff;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def check_api_health():
    """Check if API is available"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def upload_file(file, target_lang):
    """Upload file to API"""
    files = {"file": file}
    data = {"target_lang": target_lang}
    
    response = requests.post(
        f"{API_BASE_URL}/api/upload",
        files=files,
        data=data,
        timeout=30
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Upload failed: {response.text}")

def get_result(job_id):
    """Get result for a job"""
    response = requests.get(f"{API_BASE_URL}/api/result/{job_id}", timeout=10)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to retrieve result")

# Header
col1, col2 = st.columns([1, 4])
with col1:
    st.image("/placeholder.svg?height=60&width=60", width=60)
with col2:
    st.title("🌐 AI-Translate")
    st.caption("Translate media in real-time with AI")

# Check API health
if not check_api_health():
    st.error("❌ Backend API is not available. Please ensure the API is running on " + API_BASE_URL)
    st.info("To start the backend, run: `uvicorn app.main:app --host 0.0.0.0 --port 8000`")
    st.stop()

st.success("✅ Backend API is connected")

# Sidebar
with st.sidebar:
    st.header("📋 Settings")
    
    st.subheader("Target Language")
    target_lang = st.selectbox(
        "Select target language:",
        options=["en", "ru", "kk"],
        format_func=lambda x: {
            "en": "🇬🇧 English",
            "ru": "🇷🇺 Russian",
            "kk": "🇰🇿 Kazakh"
        }[x]
    )
    
    st.subheader("ℹ️ Info")
    st.markdown("""
    **Supported formats:**
    - Audio: MP3, WAV, AAC
    - Video: MP4, AVI, MKV
    - Images: JPG, PNG
    
    **Features:**
    - Automatic speech/text extraction
    - Multi-language translation
    - Audio generation from translation
    """)

# Main content
st.header("📤 Upload Media")

tab1, tab2, tab3 = st.tabs(["Upload New", "Upload Examples", "View Jobs"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Select File Type")
        file_type = st.radio(
            "Choose media type:",
            ["Audio", "Video", "Image"],
            key="file_type"
        )
        
        # File type info
        if file_type == "Audio":
            st.info("📍 Converts speech to text, translates, and generates audio in target language")
        elif file_type == "Video":
            st.info("📹 Extracts audio/subtitle, translates, can generate dubbed audio")
        else:
            st.info("🖼️ Recognizes text in image, translates, and shows results")
    
    with col2:
        uploaded_file = st.file_uploader(
            "Choose a file:",
            type={
                "Audio": ["mp3", "wav", "aac", "m4a"],
                "Video": ["mp4", "avi", "mkv", "mov"],
                "Image": ["jpg", "jpeg", "png", "gif"]
            }[file_type]
        )
    
    if uploaded_file:
        st.write(f"**File:** {uploaded_file.name}")
        st.write(f"**Size:** {uploaded_file.size / 1024 / 1024:.2f} MB")
        
        if st.button("🚀 Translate", key="upload_btn", use_container_width=True):
            with st.spinner("⏳ Uploading and processing..."):
                try:
                    result = upload_file(uploaded_file, target_lang)
                    job_id = result["job_id"]
                    
                    st.success(f"✅ Job created: {job_id}")
                    st.session_state.job_id = job_id
                    st.session_state.processing = True
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

with tab2:
    st.subheader("📚 Example Workflows")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Audio Example**
        1. Upload English speech
        2. Select target language
        3. Get translation + audio
        """)
    
    with col2:
        st.markdown("""
        **Image Example**
        1. Upload photo with text
        2. OCR extracts text
        3. Translation displayed
        """)
    
    with col3:
        st.markdown("""
        **Video Example**
        1. Upload video file
        2. Speech extracted
        3. Translated & dubbed
        """)

with tab3:
    st.subheader("📊 All Jobs")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/jobs", timeout=10)
        if response.status_code == 200:
            jobs_data = response.json()
            jobs = jobs_data.get("jobs", [])
            
            if not jobs:
                st.info("No jobs yet")
            else:
                for job in jobs:
                    with st.expander(f"Job: {job['job_id'][:8]}... | Status: {job['status']}"):
                        st.write(job)
        else:
            st.error("Failed to retrieve jobs")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Results section
if "job_id" in st.session_state:
    st.divider()
    st.header("📊 Results")
    
    job_id = st.session_state.job_id
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    try:
        result = get_result(job_id)
        
        # Status
        status = result.get("status", "unknown")
        status_emoji = {
            "pending": "⏳",
            "processing": "🔄",
            "completed": "✅",
            "failed": "❌"
        }.get(status, "❓")
        
        st.subheader(f"{status_emoji} Status: {status}")
        
        if status == "processing":
            st.info("Processing in progress...")
            time.sleep(2)
            st.rerun()
        
        elif status == "completed":
            # Source text
            if result.get("source_text"):
                with st.expander("📝 Source Text", expanded=True):
                    st.text_area("Original:", value=result["source_text"], height=100, disabled=True)
            
            # Translated text
            if result.get("translated_text"):
                with st.expander("🌍 Translated Text", expanded=True):
                    st.text_area("Translation:", value=result["translated_text"], height=100, disabled=True)
            
            # Segments (for audio/video)
            if result.get("segments"):
                with st.expander("⏱️ Segments"):
                    for i, seg in enumerate(result["segments"]):
                        st.write(f"**[{seg['start']:.1f}s - {seg['end']:.1f}s]** {seg['text']}")
            
            # Bounding boxes (for images)
            if result.get("image_bboxes"):
                with st.expander("🎯 Recognized Text (OCR)"):
                    for bbox in result["image_bboxes"]:
                        st.write(f"**{bbox['text']}** (confidence: {bbox['confidence']:.2%})")
            
            # Audio download
            if result.get("audio_url"):
                with st.expander("🔊 Generated Audio", expanded=True):
                    st.audio(API_BASE_URL + result["audio_url"])
                    st.caption("Generated speech from translation")
        
        elif status == "failed":
            st.error(f"❌ Processing failed: {result.get('error_message', 'Unknown error')}")
    
    except Exception as e:
        st.error(f"Error retrieving results: {str(e)}")

# Footer
st.divider()
st.caption("AI-Translate v1.0.0 | Hackathon Project | Powered by FastAPI & Streamlit")
