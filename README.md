# PDF Text Extractor

A modern web application for extracting text from PDF documents using a Streamlit frontend and Flask API backend.
## 🚀 Features

- **Easy PDF Upload**: Drag and drop or browse to upload PDF files
- **Text Extraction**: Extract text content from PDF documents
- **Clean Interface**: User-friendly Streamlit web interface
- **REST API**: Flask backend API for programmatic access
- **Cross-Platform**: Works on desktop and mobile browsers
- **Fast Processing**: Efficient PDF text extraction algorithms

## 🏗️ Architecture

```
┌─────────────┐    HTTP Requests    ┌─────────────┐
│             │ ─────────────────► │             │
│  Streamlit  │                    │  Flask API  │
│  Frontend   │ ◄───────────────── │   Backend   │
│             │    JSON Response   │             │
└─────────────┘                    └─────────────┘
```

## 🛠️ Tech Stack

### Frontend
- **Streamlit** - Web application framework
- **Python 3.8+** - Programming language
- **Requests** - HTTP library for API calls

### Backend
- **Flask** - Web framework
- **PyPDF2/pdfplumber** - PDF processing libraries
- **Flask-CORS** - Cross-origin resource sharing
- **Gunicorn** - WSGI HTTP Server

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Local Development Setup

1. **Clone the repository:**
```bash
git clone (https://github.com/Girishs07/pdf-text-extractor.git)
cd pdf-text-extractor
```

2. **Set up Backend:**
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Backend will run on `http://localhost:5000`

3. **Set up Frontend (in a new terminal):**
```bash
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```
Frontend will run on `http://localhost:8501`

## 🌐 Live Demo

- **Frontend:** https://pdf-text-extractor-2aombhdbxej9fyhxqmhr8m.streamlit.app/
- **API Endpoint:** https://pdf-textextractor.onrender.com

## 📖 API Documentation

### Extract Text from PDF

**Endpoint:** `POST /extract-text`

**Request:**
```bash
curl -X POST \
  https://your-backend-url.onrender.com/extract-text \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@path/to/your/document.pdf'
```

**Response:**
```json
{
  "success": true,
  "text": "Extracted text content from the PDF...",
  "page_count": 5,
  "file_name": "document.pdf"
}
```

### Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-05-31T10:30:00"
}
```

## 🚀 Deployment

This application is deployed on [Render](https://render.com) with separate services for frontend and backend.

### Deployment Architecture

```
Internet ──► Render Load Balancer ──► Streamlit Frontend ──► Flask Backend
                                            │
                                            ▼
                                     PDF Processing
```

### Environment Variables

**Frontend:**
- `BACKEND_URL`: URL of the Flask API backend

**Backend:**
- `PORT`: Port number (automatically set by Render)
- `FLASK_ENV`: Environment mode (production/development)

## 📁 Project Structure

```
pdf-text-extractor/
│── run.py      
├── requirements.txt            
├── backend/
│   ├── app.py               
│   ├── requirements.txt                   
├── README.md               
├── .gitignore             
```

## 🧪 Testing

### Manual Testing
1. Upload a PDF file through the Streamlit interface
2. Verify text extraction results
3. Test with different PDF formats and sizes

### API Testing with curl
```bash
# Test health endpoint
curl https://your-backend-url.onrender.com/health

# Test PDF extraction
curl -X POST \
  -F "file=@sample.pdf" \
  https://your-backend-url.onrender.com/extract-text
```

## 🔧 Configuration

### Streamlit Configuration
Located in `frontend/.streamlit/config.toml`:
```toml
[server]
port = 8501
headless = true

[theme]
primaryColor = "#ff6b6b"
backgroundColor = "#ffffff"
```

### Flask Configuration
Environment-based configuration in `backend/app.py`:
```python
DEBUG = os.environ.get('FLASK_ENV') == 'development'
PORT = int(os.environ.get('PORT', 5000))
```

## 🐛 Troubleshooting

### Common Issues

**Frontend not connecting to backend:**
- Verify `BACKEND_URL` environment variable
- Check CORS configuration in Flask app

**PDF processing errors:**
- Ensure PDF is not password protected
- Check file size limits (usually 16MB on free tier)

**Deployment issues:**
- Verify all dependencies in requirements.txt
- Check build and start commands in Render dashboard

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Girish** - *Initial work* - [YourGitHub](https://github.com/Girishs07)

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Flask community for the robust web framework
- PDF processing libraries contributors
- Render for hosting platform

## 📞 Support

For questions or support, please:
- Open an issue on GitHub
- Contact: girish792004@gmail.com
---

**Made with ❤️ and Python**
