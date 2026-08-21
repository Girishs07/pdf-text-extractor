# PDF Text Extractor

A modern web application for extracting text from PDF documents using a **React + Vite** frontend and **Flask API** backend.

## 🚀 Features

- **Easy PDF Upload**: Drag and drop or browse to upload PDF files
- **Text Extraction**: Extract text content from PDF, DOCX, and TXT documents
- **Modern React UI**: Beautiful, responsive interface built with React + Vite
- **Clean Interface**: User-friendly web interface with real-time processing
- **REST API**: Flask backend API for programmatic access
- **Cross-Platform**: Works on desktop and mobile browsers
- **Fast Processing**: Efficient PDF text extraction algorithms
- **File Statistics**: Character, word, line, and paragraph counts
- **Download Results**: Save extracted text as .txt files

## 🏗️ Architecture

```
┌──────────────────────┐    HTTP Requests    ┌──────────────────────┐
│                      │ ─────────────────► │                      │
│  React + Vite        │                    │   Flask API          │
│  Frontend            │ ◄───────────────── │   Backend            │
│  (localhost:5173)    │    JSON Response   │   (Backend Service)  │
│                      │                    │                      │
└──────────────────────┘                    └──────────────────────┘
```

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI library
- **Vite 4** - Modern build tool
- **CSS 3** - Modern styling with gradients and animations
- **JavaScript ES6+** - Modern JavaScript

### Backend
- **FastAPI** - Web framework (Python)
- **pdfplumber** - PDF processing library
- **Python 3.8+** - Programming language
- **Uvicorn** - ASGI HTTP Server

## 📦 Installation & Setup

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- pip (Python package manager)

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start development server:**
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Start the backend server:**
```bash
python main.py
```

Or with Uvicorn:
```bash
uvicorn main:app --reload
```

Backend will be available at `http://localhost:8000`

## 🚀 Deployment

### Deploy Frontend

**Vercel (Recommended):**
```bash
cd frontend
npm run build
vercel deploy --prod
```

**Netlify:**
```bash
cd frontend
npm run build
netlify deploy --prod --dir=dist
```

**Render (Static Site):**
1. Connect GitHub repo
2. Set build command: `npm run build`
3. Set publish directory: `dist`

### Deploy Backend

**Render.com:**
1. Connect GitHub repo
2. Set start command: `gunicorn main:app` (or `uvicorn main:app --host 0.0.0.0`)
3. Deploy

**Heroku:**
```bash
git push heroku main
```

**Railway.app:**
- Connect GitHub and deploy with one click

## 📁 Project Structure

```
pdf-text-extractor/
├── frontend/                 # React + Vite application
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── Header.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── FileUploader.jsx
│   │   │   └── Results.jsx
│   │   ├── App.jsx          # Main app component
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
│
├── backend/                  # Flask API server
│   ├── main.py              # FastAPI application
│   └── requirements.txt
│
├── README.md                # Project documentation
└── render.yaml              # Render deployment config
```

## 📖 API Endpoints

### Extract PDF
```bash
POST /extract-pdf
Content-Type: multipart/form-data

Response:
{
  "extracted_text": "...",
  "characters_extracted": 1234,
  "pages_processed": 5
}
```

### Health Check
```bash
GET /health

Response:
{
  "status": "healthy"
}
```

## 🎨 UI Features

- **Header**: Logo, backend status indicator
- **Sidebar**: Features, tips, and supported formats
- **File Uploader**: Drag-and-drop with visual feedback
- **Statistics**: Character, word, line, and paragraph counts
- **Text Preview**: Adjustable preview with slider
- **Download**: One-click download of extracted text
- **Responsive Design**: Works perfectly on all screen sizes

## 🔧 Configuration

### Environment Variables

**Frontend (.env):**
```env
VITE_BACKEND_URL=https://your-backend-url.com
```

**Backend (.env or environment):**
```env
PORT=8000
DEBUG=False
```

## 📊 Supported File Types

| Format | Status | Notes |
|--------|--------|-------|
| PDF | ✅ Server-side | Text-based PDFs work best |
| DOCX | ✅ Server-side | Word documents |
| TXT | ✅ Client-side | Plain text files |

## ⚠️ Limitations

- Maximum file size: 100MB
- PDF extraction works best with text-based PDFs (not scanned images)
- Processing time depends on file size and server resources

## 🐛 Troubleshooting

**File upload fails?**
- Check if backend is online (status badge in header)
- Verify backend URL is correct in `.env`
- Ensure file size is under 100MB

**CORS errors?**
- Backend CORS is configured for all origins
- If issues persist, check browser console for details

**Slow processing?**
- Use smaller files
- Use text-based PDFs (avoid scanned documents)
- Check network connection and server status

## 📝 License

MIT License - This project is open source and free to use

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

## 👨‍💻 Author

PDF Text Extractor - Built with React, FastAPI, and ❤️

---

For more details, see:
- [Frontend Documentation](./frontend/README.md)
- [Backend Documentation](./backend/README.md)


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
