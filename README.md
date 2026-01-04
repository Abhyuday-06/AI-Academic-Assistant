# AI Academic Assistant

A powerful **FastAPI-based AI assistant** specifically designed for academic content processing, featuring a **unified agent system**, advanced **OCR for handwritten notes**, intelligent text extraction, comprehensive analysis, **professional PDF report generation**, and a **modern Next.js frontend**.

## Key Features

### Unified Processing System
- **Single Integrated Agent** that combines parsing and summarizing
- **Intelligent Content Flow** from parsing -> analysis -> bullet-point summaries
- **Enhanced Prompt Engineering** for better academic content understanding
- **No Context Limits** - processes full documents for comprehensive analysis

### Interactive Frontend Dashboard
- **Modern Next.js Interface** for seamless interaction
- **Real-time Dashboard** for managing academic tasks
- **Responsive Design** built with Tailwind CSS and Shadcn UI
- **Visual Feedback** for processing status and results

### Advanced Question Generator
- **Module-Based Generation**: Select from Modules 1-8 for targeted practice
- **Smart Selection Tools**: "Select All" and "Deselect All" for quick configuration
- **Customizable Output**: Generate questions based on specific syllabus modules
- **PDF Export**: Download generated question papers instantly

### Professional PDF Export
- **Comprehensive PDF Reports** with structured formatting
- **Metadata Tables** showing processing statistics
- **Formatted Keywords & Concepts** with importance scores
- **Study Questions** with difficulty levels
- **Professional Layout** using ReportLab for academic publications

### Advanced OCR for Handwritten Notes
- **Multi-strategy OCR** with quality scoring for optimal text extraction
- **Advanced image preprocessing** using OpenCV and PIL
- **AI-powered text correction** using local LLM
- **Support for scanned PDFs** and handwritten academic content
- **Real-time quality assessment** and debugging output

### Intelligent Content Analysis
- **Smart keyword extraction** from academic materials
- **Concept identification** with definitions from headings and topics
- **Automatic question extraction** from course materials
- **Bullet-point summarization** optimized for academic content

### Multi-Format File Support
- **PDF**: Text-based and scanned/handwritten documents
- **DOCX**: Microsoft Word documents  
- **PPTX**: PowerPoint presentations
- **TXT**: Plain text files
- **Enhanced file handling** up to 100MB for large academic documents

### Ollama-Powered AI System
- **Primary**: Local Ollama (Mistral 7B) for privacy and speed
- **Optimized Prompts** for academic content processing
- **Enhanced Token Limits** for comprehensive analysis
- **Bullet-point focused** summary generation

## Quick Start

### 1. Prerequisites
- Python 3.8+
- Node.js 18+ (for frontend)
- [Ollama](https://ollama.ai) installed and running
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for handwritten content
- [Poppler](https://poppler.freedesktop.org/) for PDF processing

### 2. Installation

#### Backend Setup
```bash
# Clone the repository
git clone https://github.com/Abhyuday-06/AI-Academic-Assistant.git
cd AI-Academic-Assistant

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
pnpm install
```

### 3. Environment Configuration
Create a `.env` file in the root directory with your configuration:
```env
# Ollama Configuration (primary)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b

# Application Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
SECRET_KEY=your_secret_key_here
LOG_LEVEL=INFO

# Optional: OpenAI Configuration (for fallback)
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Setup Ollama & Dependencies
```bash
# Install and start Ollama
ollama pull mistral:7b
ollama serve

# For Windows - Install Tesseract and Poppler:
# Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
# Poppler: Download and extract to C:\poppler-xx.x.x\
```

### 5. Run the Application

#### Start Backend
```bash
# From the root directory
python run_dev.py
# Or manually
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Start Frontend
```bash
# From the frontend directory
npm run dev
```

### 6. Access Your Assistant
- **Frontend Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **API Root**: http://localhost:8000/

## API Endpoints

### Unified Processing
```http
POST /parse           # Parse and summarize text content
POST /parse-file      # Parse and summarize uploaded files
POST /summarize       # Summarize text content only
POST /summarize-file  # Summarize uploaded files only
```

### PDF Export
```http
POST /parse/export-pdf           # Export parsing results to PDF
POST /parse-file/export-pdf      # Export file parsing results to PDF  
POST /summarize/export-pdf       # Export summary results to PDF
POST /summarize-file/export-pdf  # Export file summary results to PDF
```
**Features:**
- **Professional PDF reports** with formatted layouts
- **Metadata tables** with processing statistics
- **Structured content** with headers, bullet points, and tables
- **Keywords & concepts** with importance scores
- **Study questions** with difficulty levels

### Question Generation
```http
POST /generate-question-paper    # Generate questions from syllabus
```

### System Health
```http
GET /health
```

## Usage Examples

### Parse and Summarize Handwritten Notes
```python
import httpx

# Upload and get comprehensive analysis + summary
with open("handwritten_notes.pdf", "rb") as file:
    response = httpx.post(
        "http://localhost:8000/parse-file",
        files={"file": file},
        params={
            "extract_keywords": True,
            "extract_concepts": True,
            "extract_questions": True
        }
    )

result = response.json()
print(f"Summary: {result['parsed_content']}")
print(f"Keywords: {result['keywords']}")
print(f"Concepts: {result['concepts']}")
print(f"Questions: {result['study_questions']}")
```

### Export Results to Professional PDF
```python
import httpx

# Parse content and export to PDF in one call
response = httpx.post("http://localhost:8000/parse/export-pdf", json={
    "content": "Machine learning is a subset of artificial intelligence that enables computers to learn from data...",
    "extract_keywords": True,
    "extract_concepts": True,
    "extract_questions": True
})

# Save the PDF
with open("academic_analysis.pdf", "wb") as f:
    f.write(response.content)
```

## Project Architecture

```
AI-Academic-Assistant/
├── app/
│   ├── agents/           # AI processing agents
│   │   └── academic_agent.py # Unified parsing + summarizing agent
│   ├── models/           # Pydantic data models
│   ├── routers/          # FastAPI route handlers
│   │   └── academic_router.py # Unified API endpoints
│   └── utils/            # Core utilities
│       ├── config.py        # App configuration
│       ├── ollama_client.py # Local AI client
│       ├── openai_client.py # Fallback AI client
│       └── pdf_exporter.py  # PDF report generation
├── frontend/             # Next.js Frontend Application
│   ├── app/              # App router pages
│   ├── components/       # React components
│   └── lib/              # Frontend utilities
├── legacy/               # Previous implementation (backup)
├── local_files/          # File upload storage
├── main.py               # Application entry point
├── run_dev.py            # Development runner
├── requirements.txt      # Python dependencies
└── README.md             # You are here!
```

## What's New (January 2026)

### Major Updates:
- **Interactive Frontend**: Complete Next.js dashboard for easy interaction
- **Question Generator**: Advanced module-based question generation (Modules 1-8)
- **Unified Agent System**: Merged parsing and summarizing into single `AcademicAgent`
- **Professional PDF Export**: Generate formatted academic reports
- **Simplified API**: Clean endpoints without redundant variations

### API Simplification:
- **Before**: `/notes/parse`, `/notes/parse-file`, `/summarize/`, `/summarize/file`, etc.
- **After**: `/parse`, `/parse-file`, `/summarize`, `/summarize-file` + PDF endpoints

## Advanced Configuration

### OCR Settings
```python
# In .env or app/utils/config.py
OCR_DPI=300                              # Scan quality
OCR_PARALLEL_WORKERS=4                   # Processing threads
ENABLE_ADVANCED_OCR_PREPROCESSING=True   # Image enhancement
ENABLE_OCR_CORRECTION=True               # AI text correction
```

### File Limits
```python
MAX_FILE_SIZE_MB=100      # Large academic documents
MAX_CONTENT_LENGTH=500000 # Long research papers (no context limits!)
```

## Development & Testing

### Code Quality
```bash
# Format code
black app/
isort app/

# Type checking
mypy app/

# Linting
flake8 app/
```

### Debugging OCR
The system provides detailed OCR debugging output in the terminal:
```
ENHANCED ACADEMIC OCR SYSTEM
Successfully converted 5 pages to images
Processing page 1/5...
  Academic Mixed Content: 0.85 score, 234 chars
  Page 1: 234 chars, score: 0.85
FINAL RESULTS:
  Success rate: 5/5 pages (100.0%)
  Average quality score: 0.82
  Total extracted text: 1200 characters
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Ollama** for local AI inference with Mistral 7B
- **ReportLab** for professional PDF generation
- **Tesseract OCR** for text recognition
- **FastAPI** for the excellent web framework
- **OpenCV** for advanced image processing
- **OpenAI** for fallback AI capabilities
- **Next.js** for the modern frontend framework

---

**Built for students, researchers, and educators**

*Now with unified processing, professional PDF reports, and a modern frontend!*
