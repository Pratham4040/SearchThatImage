# Copilot Instructions for SearchThatImage

## Project Overview
SearchThatImage is an AI-powered image search engine. Users upload images; the
backend sends each image to an AI Vision API to obtain descriptive tags, stores
the image path + tags in SQLite (via SQLAlchemy), and exposes a search endpoint
so that users can query images by those tags.

---

## Tech Stack
| Layer     | Technology                          |
|-----------|-------------------------------------|
| Backend   | Python 3.11+, Flask, SQLAlchemy     |
| Frontend  | React (Vite), TailwindCSS           |
| Database  | SQLite                              |

---

## General Rules

### Python / Flask (backend/)
1. **Always use type hints** in every function signature and return type.
   ```python
   # Good
   def get_image(image_id: int) -> dict[str, object]:
       ...
   ```
2. **Use Flask Blueprints** – never add new routes directly to `app.py`.
   Each feature gets its own Blueprint inside `app/routes/`.
3. **Separate concerns** strictly:
   - `app/routes/`   – HTTP layer only (validate input, call service, return JSON).
   - `app/services/` – all business logic including AI API calls.
   - `app/models/`   – SQLAlchemy models and schema only.
4. **Keep AI logic isolated** inside `app/services/ai_service.py`.
   Routes must never call an AI API directly.
5. Use **python-dotenv** to load environment variables; never hard-code secrets.
6. Return consistent JSON error responses:
   ```json
   { "error": "Human-readable message", "status": 400 }
   ```
7. Write **docstrings** for every public function and class.
8. Prefer `pathlib.Path` over `os.path` for file-system operations.
9. Use **SQLAlchemy ORM** (not raw SQL) for all database access.
10. Always validate and sanitise file uploads (extension allow-list, size limit).

### JavaScript / React (frontend/)
1. **Use functional components** exclusively; never use class components.
2. Manage side effects with `useEffect`; avoid side effects in render bodies.
3. Use **TailwindCSS utility classes** for all styling; do not write custom CSS
   unless absolutely necessary.
4. Keep API call logic inside `src/services/api.js`; components must not call
   `fetch`/`axios` directly.
5. Name component files with **PascalCase** (e.g. `ImageCard.jsx`).
6. Name non-component files with **camelCase** (e.g. `api.js`).
7. Prefer **named exports** for components; use a default export only for page-
   level components.
8. Always handle loading and error states in components that perform async work.
9. Use `import.meta.env.VITE_*` variables for all environment-specific config.

### Git / General
- Commit messages follow **Conventional Commits** (`feat:`, `fix:`, `chore:` …).
- Never commit `.env` files; `.env.example` is the source of truth for required
  variables.
- Keep `backend/` and `frontend/` as self-contained workspaces with their own
  dependency files (`requirements.txt` / `package.json`).
