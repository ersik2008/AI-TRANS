# 🌐 AI-Translate

**Multilingual media translation platform for AI hackathon**

Production-ready application that accepts media files, extracts text, translates to multiple languages, and generates localized audio output.

## 🎯 Features

- **Multi-format Support**: Audio (MP3, WAV), Video (MP4, AVI, MKV), Images (JPG, PNG)
- **Smart Extraction**:
  - Speech-to-Text via Whisper
  - Optical Character Recognition (OCR) via PaddleOCR
- **Multilingual Translation**: Russian, Kazakh, English via NLLB-200
- **Audio Generation**: Text-to-Speech synthesis in target language
- **Async Processing**: Background job handling with real-time status
- **REST API**: FastAPI with comprehensive documentation
- **Web UI**: Streamlit for intuitive user interaction

## 🏗️ Architecture

\`\`\`
ai-translate/
├── app/                          # FastAPI backend
│   ├── main.py                   # App entry point
│   ├── config.py                 # Configuration
│   ├── models/                   # Data models
│   │   └── job.py               # Job schema
│   ├── services/                 # ML services
│   │   ├── job_manager.py       # Job tracking
│   │   ├── speech_to_text.py    # Whisper integration
│   │   ├── image_to_text.py     # OCR integration
│   │   ├── translation.py        # NLLB integration
│   │   └── text_to_speech.py    # TTS integration
│   ├── routes/                   # API endpoints
│   │   ├── upload.py            # File upload
│   │   ├── results.py           # Result retrieval
│   │   └── worker.py            # Background worker
│   └── utils/                    # Utilities
│       └── file_utils.py        # File handling
├── frontend/                     # Streamlit UI
│   └── app.py                   # Web interface
├── scripts/                      # Test & run scripts
│   ├── test_api.sh             # API testing
│   └── run.sh                  # Local/Docker launcher
├── sample_files/                # Example media
├── Dockerfile                   # Container image
├── docker-compose.yml          # Multi-container setup
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
└── README.md                  # This file
\`\`\`

## 🚀 Quick Start

### Option 1: Docker (Recommended)

\`\`\`bash
# Clone and setup
git clone <repo>
cd ai-translate

# Start with Docker Compose
docker-compose up --build

# Access:
# Backend:  http://localhost:8000
# Frontend: http://localhost:8501
# Docs:     http://localhost:8000/docs
\`\`\`

### Option 2: Local Installation

\`\`\`bash
# Requirements
- Python 3.11+
- FFmpeg (for audio/video processing)

# Setup
pip install -r requirements.txt

# Run
./scripts/run.sh local

# Or separately:
# Terminal 1: Backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Frontend
streamlit run frontend/app.py --server.port 8501
\`\`\`

## 📡 API Documentation

### Upload File
\`\`\`bash
POST /api/upload
Content-Type: multipart/form-data

Parameters:
- file: Binary file (audio/video/image)
- target_lang: "ru" | "en" | "kk"

Response:
{
  "job_id": "uuid",
  "status": "processing"
}
\`\`\`

### Get Results
\`\`\`bash
GET /api/result/{job_id}

Response:
{
  "job_id": "uuid",
  "status": "completed",
  "file_type": "audio|video|image",
  "source_text": "...",
  "translated_text": "...",
  "segments": [
    {"start": 0.0, "end": 5.0, "text": "..."}
  ],
  "image_bboxes": [
    {"x": 10, "y": 20, "width": 100, "height": 30, "text": "...", "confidence": 0.95}
  ],
  "audio_url": "/media/uuid.mp3"
}
\`\`\`

### List Jobs
\`\`\`bash
GET /api/jobs

Response:
{
  "jobs": [...],
  "total": 42
}
\`\`\`

## 🧪 Testing

\`\`\`bash
# Run test suite
./scripts/test_api.sh

# Manual test with cURL
curl -X POST -F "file=@sample.mp3" -F "target_lang=en" http://localhost:8000/api/upload

# Interactive testing
curl http://localhost:8000/docs
\`\`\`

## 🔧 Configuration

### Environment Variables

\`\`\`env
# API
API_BASE_URL=http://localhost:8000
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# File Paths
UPLOAD_DIR=/tmp/uploads
AUDIO_OUTPUT_DIR=/tmp/audio_output
MODELS_DIR=/tmp/models

# Models
WHISPER_MODEL=base              # Options: tiny, base, small, medium, large
NLLB_MODEL=facebook/nllb-200-distilled-600M

# Limits
MAX_FILE_SIZE=500              # MB
\`\`\`

### Model Downloads

Models auto-download on first use:
- **Whisper**: `~140MB` (base model)
- **NLLB**: `~1.2GB` (distilled-600M)
- **PaddleOCR**: `~200MB`
- **TTS**: `~300MB`

Set `MODELS_DIR` to persistent storage for faster subsequent runs.

## 📊 Processing Pipeline

### Audio/Video
\`\`\`
Upload → Extract Audio → Speech-to-Text → Translate → Text-to-Speech → Generate MP3
\`\`\`

### Image
\`\`\`
Upload → OCR Extract → Translate → Generate Speech → Return Results
\`\`\`

## 🎯 Supported Languages

| Code | Language | Status |
|------|----------|--------|
| en   | English  | ✅     |
| ru   | Russian  | ✅     |
| kk   | Kazakh   | ✅     |

## 📈 Performance Notes

- **First run**: Slow (model downloads)
- **Subsequent runs**: Fast (cached models)
- **Large files**: May take 5-30 minutes
- **Recommended**: GPU machine (optional but faster)

## ⚠️ Limitations

- Max file size: 500MB
- Supported formats: MP3, WAV, MP4, PNG, JPG
- Processing timeout: 1 hour per job
- Memory: ~4GB minimum recommended

## 🛠️ Development

### Adding New Language

1. Update `SUPPORTED_LANGUAGES` in `app/config.py`
2. Add NLLB code to `NLLB_LANG_CODES`
3. Restart services

### Custom Model

Replace in `app/services/translation.py`:
\`\`\`python
NLLB_MODEL = "your/model/name"
\`\`\`

### Debugging

\`\`\`bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# View container logs
docker-compose logs -f backend
docker-compose logs -f frontend

# API documentation
http://localhost:8000/docs
\`\`\`

## 📦 Dependencies

**Core**:
- FastAPI: Web framework
- Streamlit: Frontend
- Uvicorn: ASGI server

**ML Models**:
- faster-whisper: Speech recognition
- PaddleOCR: Text recognition
- Transformers: Translation
- TTS: Audio synthesis

**Utilities**:
- FFmpeg: Media processing
- Pydantic: Data validation
- Requests: HTTP client

## 🏆 Hackathon Ready

This project includes:
- ✅ Production-ready code structure
- ✅ Error handling & logging
- ✅ Docker deployment
- ✅ API documentation
- ✅ UI/UX for demos
- ✅ Extensible architecture
- ✅ Mock services for quick testing

## 📝 License

MIT

## 👥 Contributing

1. Fork repository
2. Create feature branch
3. Submit pull request

## 🤝 Support

For issues or questions:
1. Check API docs: `http://localhost:8000/docs`
2. Review logs: `docker-compose logs`
3. Test endpoint: `./scripts/test_api.sh`

---

**Built for AI Hackathon** 🚀
Made with ❤️ by AI Engineering Team
