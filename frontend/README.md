# PDF Text Extractor - React Frontend

A modern React + Vite frontend for the PDF Text Extractor application.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm installed
- Backend API running (Flask)

### Installation

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Start development server:**
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## 🏗️ Build & Deployment

### Build for production:
```bash
npm run build
```

This creates an optimized production build in the `dist/` folder.

### Preview production build locally:
```bash
npm run preview
```

## 📦 Features

- ✨ Modern, responsive UI with Vite + React
- 📤 Drag-and-drop file upload
- 📊 File statistics and text preview
- 💾 Download extracted text
- 🔒 Secure client-side and server-side processing
- 🎨 Beautiful gradient designs and smooth animations
- 📱 Fully responsive on mobile, tablet, and desktop

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `frontend/` directory:

```env
VITE_BACKEND_URL=https://your-backend-url.com
```

Default backend URL: `https://pdf-textextractor.onrender.com`

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── Header.css
│   │   ├── Sidebar.jsx
│   │   ├── Sidebar.css
│   │   ├── FileUploader.jsx
│   │   ├── FileUploader.css
│   │   ├── Results.jsx
│   │   └── Results.css
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   └── index.css
├── public/
├── index.html
├── package.json
├── vite.config.js
└── .env
```

## 🎨 UI Features

- **Modern Design**: Clean, professional interface with gradient colors
- **Dark Sidebar**: Navigation and tips in a dark sidebar
- **Drag-and-Drop**: Easy file upload with visual feedback
- **Statistics Cards**: Display file stats with hover effects
- **Text Preview**: Adjustable preview with character count slider
- **Download**: One-click download of extracted text

## 🔗 API Integration

The frontend communicates with the Flask backend at:
- `POST /extract-pdf` - Extract text from PDF files
- `GET /health` - Check backend status

Supported file types:
- **PDF** (.pdf)
- **DOCX** (.docx)
- **TXT** (.txt)

## 📱 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 🚀 Deployment

### Deploy to Vercel (Recommended):
```bash
npm i -g vercel
vercel
```

### Deploy to Netlify:
```bash
npm i -g netlify-cli
netlify deploy --prod --dir=dist
```

### Deploy to Render (as static site):
1. Connect your GitHub repository
2. Set build command: `npm run build`
3. Set publish directory: `dist`

## 🐛 Troubleshooting

**File upload not working?**
- Ensure backend is online (check status badge in header)
- Verify backend URL in `.env` file
- Check browser console for errors

**CORS errors?**
- Backend must have CORS configured
- Check that `allow_origins` includes your frontend URL

**Slow file processing?**
- Reduce file size (max 100MB)
- Use text-based PDFs (not scanned images)
- Check network connection

## 📄 License

MIT License - See LICENSE file

## 👨‍💻 Author

[Your Name] - PDF Text Extractor Project
