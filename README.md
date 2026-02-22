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
│   │   ├── models/                  # SQLAlchemy models (database layer)
│   │   │   ├── __init__.py
│   │   │   ├── database.py          # Shared db instance & configuration
│   │   │   ├── image.py             # Image model with relationships
│   │   │   └── tag.py               # Tag model for AI-generated descriptors
│   │   ├── routes/                  # Flask Blueprints (HTTP layer only)
│   │   │   ├── __init__.py
│   │   │   ├── images.py            # /api/images/* endpoints
│   │   │   └── search.py            # /api/search/* endpoints
│   │   ├── services/                # Business logic & integrations
│   │   │   ├── __init__.py
│   │   │   ├── ai_service.py        # AI Vision API (Gemini) integration
│   │   │   ├── image_service.py     # Image upload & persistence
│   │   │   ├── search_service.py    # Tag-based search logic
│   │   │   ├── delete_service.py    # Image & tag deletion logic
│   │   │   └── download_service.py  # Image download utilities
│   │   └── __init__.py              # App factory & configuration
│   ├── tests/                       # Test suite
│   │   ├── conftest.py              # Pytest fixtures & configuration
│   │   └── test_endpoints.py        # API endpoint tests
│   ├── instance/                    # Flask instance folder (git-ignored)
│   ├── uploads/                     # Uploaded image files (git-ignored)
│   ├── app.py                       # Application entry point
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/              # Reusable React UI components
│   │   │   ├── ImageCard.jsx        # Image display with tags
│   │   │   ├── ImageUpload.jsx      # File upload component
│   │   │   └── SearchBar.jsx        # Search query input
│   │   ├── pages/                   # Page-level components (routes)
│   │   │   ├── Home.jsx             # Gallery & search results
│   │   │   └── Upload.jsx           # Upload image page
│   │   ├── services/
│   │   │   └── api.js               # Centralized API client (axios)
│   │   ├── App.jsx                  # Main React component
│   │   ├── main.jsx                 # React entry point
│   │   └── index.css                # Global styles
│   ├── index.html                   # HTML template
│   ├── package.json                 # Frontend dependencies
│   ├── postcss.config.js            # PostCSS configuration
│   ├── tailwind.config.js           # TailwindCSS configuration
│   ├── vite.config.js               # Vite dev server & build config
│   └── .gitignore
├── README.md                        # Project documentation
└── .env.example                     # Template for environment variables
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

## Key Technical Decisions

- **SQLite for persistence:** Keeps setup simple and fast for local dev and assessment review.
- **Gemini JSON mode:** Uses `response_mime_type="application/json"` to guarantee a predictable tag array, reducing parsing errors.
- **AI logic isolation:** All AI calls live in `backend/app/services/ai_service.py` to keep routes thin and make vendor swaps low-risk.

---

## Database Schema

### Many-to-Many Relationship: Images ↔ Tags

The application uses a **Many-to-Many** relationship to link images with their AI-generated tags efficiently.

#### Tables

**`images`** – Uploaded image metadata
| Column | Type | Constraints |
|--------|------|-------------|
| `id` | INTEGER | PRIMARY KEY, auto-increment |
| `filename` | VARCHAR(255) | NOT NULL, UNIQUE (UUID-based filename on disk) |
| `original_filename` | VARCHAR(255) | NOT NULL (filename as provided by user) |
| `file_path` | VARCHAR(512) | NOT NULL (absolute path to image file) |
| `tags` | TEXT | Default: "" (legacy comma-separated tags) |
| `created_at` | DATETIME | NOT NULL, DEFAULT: current UTC time |

**`tags`** – AI-generated descriptive tags
| Column | Type | Constraints |
|--------|------|-------------|
| `id` | INTEGER | PRIMARY KEY, auto-increment |
| `name` | VARCHAR(255) | NOT NULL, UNIQUE, INDEXED (lowercase tag name) |

**`image_tags`** – Many-to-Many association table
| Column | Type | Constraints |
|--------|------|-------------|
| `image_id` | INTEGER | FOREIGN KEY → images.id (CASCADE DELETE) |
| `tag_id` | INTEGER | FOREIGN KEY → tags.id (CASCADE DELETE) |
| | | Composite PRIMARY KEY (image_id, tag_id) |

#### Design Benefits

- **Efficient storage:** Tags are deduplicated (one Tag record per unique tag name)
- **Query flexibility:** Search images by tag name using `tag_objects` relationship
- **Cascade delete:** Deleting an image removes all its tag associations automatically
- **Shared tags:** Same tag can appear for multiple images if they have similar content
- **Backward compatible:** Legacy `tags` string field preserved for gradual migration

#### Example Data Flow

```plaintext
User uploads "cat_photo.jpg"
        ↓
AI generates tags: ["cat", "pet", "furry", "animal", "cute"]
        ↓
For each tag:
  - Check if Tag(name="cat") exists → use existing or create new
  - Add image-tag association to image_tags table
        ↓
Database state:
  images: [id=1, filename="abc123.jpg", original_filename="cat_photo.jpg", ...]
  tags: [
    {id=1, name="cat"},
    {id=2, name="pet"},
    {id=3, name="furry"},
    {id=4, name="animal"},
    {id=5, name="cute"}
  ]
  image_tags: [
    {image_id=1, tag_id=1},
    {image_id=1, tag_id=2},
    {image_id=1, tag_id=3},
    {image_id=1, tag_id=4},
    {image_id=1, tag_id=5}
  ]
        ↓
User searches "cat"
        ↓
Query returns image with id=1 (matches tag_objects.any(Tag.name LIKE "cat"))
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the required values:

| Variable               | Description                                    |
|------------------------|------------------------------------------------|
| `SECRET_KEY`           | Flask secret key (for session management)     |
| `DATABASE_URL`         | SQLAlchemy DB URI (default: SQLite local file)|
| `GEMINI_API_KEY`       | Google Gemini API key (get from cloud.google.com) |
| `UPLOAD_FOLDER`        | Directory to store uploaded images             |
| `MAX_CONTENT_LENGTH_MB`| Max upload size in MB (default: 16)            |
| `ALLOWED_EXTENSIONS`   | Comma-separated permitted file types           |
| `CORS_ORIGINS`         | Frontend origin(s) allowed by CORS             |

**Example `.env`:**
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-random-secret-key-here
DATABASE_URL=sqlite:///searchthatimage.db
GEMINI_API_KEY=AIza...your-actual-key-here...  # Get from Google Cloud
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH_MB=16
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,webp
CORS_ORIGINS=http://localhost:5173
```

---

## API Endpoints

| Method | Path                       | Description                    |
|--------|----------------------------|--------------------------------|
| `GET`  | `/api/images/`             | List all images (paginated)    |
| `GET`  | `/api/images/<id>`         | Get a single image by ID       |
| `POST` | `/api/images/upload`       | Upload a new image             |
| `GET`  | `/api/images/file/<name>`  | Serve the raw image file       |
| `GET`  | `/api/search/?q=<query>`   | Search images by tag           |