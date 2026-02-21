# SearchThatImage

An **AI-powered image search engine**. Upload an image → an AI Vision API
generates descriptive tags → search your gallery by those tags.

---

## Tech Stack

| Layer     | Technology                              |
|-----------|-----------------------------------------|
| Backend   | Python 3.11+, Flask, SQLAlchemy, SQLite |
| Frontend  | React 18 (Vite), TailwindCSS            |

---

## Project Structure

```
SearchThatImage/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy models
│   │   │   ├── database.py  # Shared db instance
│   │   │   └── image.py     # Image model
│   │   ├── routes/          # Flask Blueprints (HTTP layer only)
│   │   │   ├── images.py    # /api/images/*
│   │   │   └── search.py    # /api/search/*
│   │   └── services/        # Business logic
│   │       ├── ai_service.py     # AI Vision API integration
│   │       ├── image_service.py  # Upload & persistence logic
│   │       └── search_service.py # Tag-based search logic
│   ├── uploads/             # Uploaded image files (git-ignored)
│   ├── app.py               # Application factory entry point
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   │   ├── ImageCard.jsx
│   │   │   ├── ImageUpload.jsx
│   │   │   └── SearchBar.jsx
│   │   ├── pages/           # Page-level components
│   │   │   ├── Home.jsx
│   │   │   └── Upload.jsx
│   │   ├── services/
│   │   │   └── api.js       # All axios calls live here
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
├── .env.example             # Required environment variables
├── .gitignore
└── .github/
    └── copilot-instructions.md
```

---

## Getting Started

### 1 – Clone and configure

```bash
git clone https://github.com/Pratham4040/SearchThatImage.git
cd SearchThatImage
cp .env.example .env          # Fill in your API key and other values
```

### 2 – Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask run                     # Starts on http://localhost:5000
```

### 3 – Frontend

```bash
cd frontend
npm install
npm run dev                   # Starts on http://localhost:5173
```

The Vite dev server proxies `/api/*` requests to the Flask backend
automatically (see `vite.config.js`).

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the required values:

| Variable               | Description                              |
|------------------------|------------------------------------------|
| `SECRET_KEY`           | Flask secret key                         |
| `DATABASE_URL`         | SQLAlchemy DB URI (default: SQLite)      |
| `AI_VISION_API_KEY`    | API key for your AI Vision provider     |
| `AI_VISION_API_URL`    | Endpoint URL for the AI Vision API      |
| `UPLOAD_FOLDER`        | Directory to store uploaded images       |
| `MAX_CONTENT_LENGTH_MB`| Max upload size in MB (default: 16)     |
| `ALLOWED_EXTENSIONS`   | Comma-separated list of allowed formats  |
| `CORS_ORIGINS`         | Frontend origin(s) allowed by CORS       |

---

## API Endpoints

| Method | Path                       | Description                    |
|--------|----------------------------|--------------------------------|
| `GET`  | `/api/images/`             | List all images (paginated)    |
| `GET`  | `/api/images/<id>`         | Get a single image by ID       |
| `POST` | `/api/images/upload`       | Upload a new image             |
| `GET`  | `/api/images/file/<name>`  | Serve the raw image file       |
| `GET`  | `/api/search/?q=<query>`   | Search images by tag           |