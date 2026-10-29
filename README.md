# YumSure

A comprehensive food product scanner, ingredient safety analysis, and health evaluation platform — an independent, production-grade clone of **TruthIn**.

---

## 📂 Project Structure

```
YumSure/
├── backend/                  # FastAPI + PostgreSQL REST API backend
│   ├── alembic/              # Database schema versioning & migrations
│   ├── app/                  # Application core, API endpoints, models & engines
│   │   ├── api/v1/           # Scanner, Products, Analysis, Auth, Profile, History
│   │   ├── core/             # Configuration, Database engine, Security (JWT)
│   │   ├── models/           # SQLAlchemy models (Facts, Analyses, Additives, etc.)
│   │   ├── schemas/          # Pydantic v2 schemas
│   │   └── services/         # Nutrition engine, Ingredient engine, Barcode resolver
│   ├── tests/                # Automated pytest test suite (28 passing tests)
│   ├── .env.example          # Environment configuration template
│   ├── alembic.ini           # Alembic configuration
│   ├── init_db.py            # Standalone DB initialization & seed script
│   ├── requirements.txt      # Python dependencies
│   ├── run.py                # Local server launcher
│   └── README.md             # Detailed backend architecture & API guide
│
├── frontend/                 # Frontend client application (React / Next.js / Mobile)
│   └── README.md             # Frontend integration notes & endpoint references
│
└── README.md                 # Root project overview
```

---

## 🚀 Quick Start (Backend)

```bash
# 1. Navigate to backend directory
cd backend

# 2. Activate virtual environment
..\venv\Scripts\activate      # Windows PowerShell / CMD
# source ../venv/bin/activate # Linux / macOS

# 3. Initialize & Seed Database (PostgreSQL)
python init_db.py

# 4. Run the API Server
python run.py
```

The API will be available at:
- **API Base:** `http://localhost:8000`
- **Swagger UI Docs:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## 🧪 Running Tests

```bash
cd backend
python -m pytest -v
```
*(All 28 tests passing)*
