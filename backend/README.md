# TruthIn Backend API (YumSure)

A production-ready FastAPI + PostgreSQL backend replicating and advancing the core product scanning, ingredient analysis, health evaluation, and authentication engine of the **TruthIn** smart product scanner app.

---

## 🌟 Key Architecture & Improvements

### 1. P0: Separation of Product Facts & Calculated Assessments
- **Source Nutrition Facts Table (`nutrition_facts`)**: Preserves raw nutrient values as provided by manufacturers/catalogues without transformation. Crucially, **missing values remain `None` / `NULL` and are never converted to `0.0`**.
- **Versioned Assessments Table (`nutrition_analyses`)**: Calculated scores, color flags, Nova groups, and Nutri-Scores are stored independently associated with an explicit `rule_version` (e.g. `2026.1`). Updating scoring rules will never overwrite or corrupt historical source facts.

### 2. P0: Split Engine Architecture
- [nutrition_engine.py](file:///d:/YumSure/app/services/nutrition_engine.py): Pure functional module for nutrient normalization (sodium to salt conversion, per 100g basis), thresholds, scoring, completeness percentage, and personalized dietary alerts. Fully testable without a database or network.
- [ingredient_engine.py](file:///d:/YumSure/app/services/ingredient_engine.py): Pure functional parser for INS/E-number additive extraction with hazard classification (`SAFE`, `CAUTION`, `AVOID`), comprehensive multi-allergen matching, palm oil detection, and vegetarian verification.
- [assessment_service.py](file:///d:/YumSure/app/services/assessment_service.py): Shared assessment coordinator producing unified, versioned response schemas for scanner and product endpoints.

### 3. P0: Data Provenance & Completeness
- Every product and nutrition fact records:
  - `source`: Attribution origin (e.g., `local_seed`, `openfoodfacts`, `openbeautyfacts`, `user_contributed`).
  - `retrieved_at`: UTC timestamp of the retrieval.
  - `data_completeness_score`: Explicit percentage of mandatory nutrients present (energy, fat, saturated fat, carbs, sugars, fiber, protein, salt/sodium).
  - `verification_status`: `COMMUNITY`, `VERIFIED_INDEPENDENT`, or `OFFICIAL_MANUFACTURER`.

### 4. P0: Authentication & User Authorization
- **JWT Authentication & Bcrypt Password Hashing**: Implemented in [security.py](file:///d:/YumSure/app/core/security.py) and [auth.py](file:///d:/YumSure/app/api/v1/endpoints/auth.py).
- **Strict User Isolation**: All personal profile and scan history endpoints (`/api/v1/profile/me`, `/api/v1/history`) require a valid Bearer token and enforce strict user-level authorization so users can only view and mutate their own records.

### 5. P1: Robust Barcode Resolution & Caching
- **GS1 Modulo-10 Check Digit Validation**: Enforces valid format and check digit for EAN-13, EAN-8, and UPC-A barcodes before contacting upstream services.
- **Negative Caching**: Barcodes not found upstream are cached in-memory with a short TTL (10 minutes) to eliminate repetitive external traffic.
- **In-Flight Request Deduplication**: Async locks prevent duplicate concurrent upstream HTTP requests for the same barcode.
- **Source Priority & Category Routing**: Personal care and cosmetics are routed to Open Beauty Facts, packaged food to Open Food Facts, with fallback catalog support.
- **Upstream Resilience**: Configured HTTP timeouts (8.0s), 2 retry attempts, and exponential backoff.

### 6. P1: Alembic Database Migrations & Comprehensive Testing
- Managed by Alembic (`alembic upgrade head`).
- **28 Automated Pytest Scenarios** covering barcode check-digit validation, negative caching, nutrient scoring boundaries, rule versioning, additive hazard extraction, allergen detection, JWT auth flows, cross-user isolation, and DB null-preservation.

---

## 🗄️ Database Migrations with Alembic

The project uses **Alembic** to manage database schema evolution:

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Apply latest migrations
alembic upgrade head

# Generate a new migration after model changes
alembic revision --autogenerate -m "describe_changes"
```

---

## 🚀 Running Locally

### 1. Prerequisites
- Python 3.12+ (Python 3.14 compatible)
- PostgreSQL 15+ running on `localhost:5432` with database `truthin_db`

### 2. Seeding Initial Data
```bash
python init_db.py
```
This seeds popular FMCG items (Nestlé Maggi, Britannia Good Day, Parle-G, Amul Butter, Lay's, etc.), 30+ INS additives, and a demo user (`demo@yumsure.app` / `DemoUser123!`).

### 3. Start Dev Server
```bash
python run.py
```
- API: `http://localhost:8000`
- Swagger Docs: `http://localhost:8000/docs`

---

## 📡 Key API Endpoints

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/auth/register` | Register new user account |
| `POST` | `/api/v1/auth/login` | Login and obtain JWT access token |
| `GET` | `/api/v1/auth/me` | Fetch authenticated user information |

### Barcode Scanner
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/scanner/{barcode}` | Scan and assess barcode with check-digit validation |

### User Profile (Authenticated)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/profile/me` | Fetch own dietary profile and allergens |
| `PUT` | `/api/v1/profile/me` | Update personal allergies and health goals |
| `GET` | `/api/v1/profile/allergens/list` | List all supported allergen filters |
| `GET` | `/api/v1/profile/goals/list` | List all supported health goals |

### Scan History & Favorites (Authenticated)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/history` | List authenticated user's scan history |
| `PATCH` | `/api/v1/history/{id}/favorite` | Toggle favorite flag on own scan item |
| `DELETE` | `/api/v1/history/{id}` | Delete own scan history record |

### Products & Healthier Alternatives
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/products` | Search/filter products by name, category, flag |
| `GET` | `/api/v1/products/{id}` | Get product details, source facts, and assessment |
| `GET` | `/api/v1/products/{id}/alternatives` | Get healthier alternative suggestions |
| `POST` | `/api/v1/products` | Contribute a new product |

### Direct Ingredient Text / OCR Analysis
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/analysis/ingredients` | Analyze raw ingredient labels & OCR text |

---

## 🧪 Automated Test Suite

Run the full pytest suite:
```bash
.\venv\Scripts\python -m pytest -v
```
**Test Coverage (28/28 Passed)**:
- `tests/test_nutrition_engine.py`: Normalization, missing data preservation, completeness calculation, threshold boundaries, rule versioning.
- `tests/test_ingredient_engine.py`: Additive hazard parsing, allergen extraction, palm oil detection, vegetarian classification.
- `tests/test_barcode_resolver.py`: GS1 check-digit verification, negative caching with TTL, seed catalog resolution.
- `tests/test_auth.py`: Registration, JWT login, credential verification, cross-user isolation.
- `tests/test_data_validation.py`: Null value database retention, data provenance tracking, scoring rule independence.
- `tests/test_api.py`: Scanner, profile personalization, OCR analysis, and recommendations.
