# YumSure Frontend

This directory is reserved for the frontend client (e.g. React, Next.js, Flutter, React Native, or Vue).

---

## 🔗 Connecting to the Backend
The YumSure FastAPI backend runs by default at:
- **Base URL:** `http://localhost:8000`
- **Interactive Swagger Docs:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Key API Endpoints
- **Barcode Scanner:** `GET /api/v1/scanner/{barcode}`
- **Product Details:** `GET /api/v1/products/{id}`
- **Healthier Alternatives:** `GET /api/v1/products/{id}/alternatives`
- **TIA Chatbot:** `POST /api/v1/analysis/chat`
- **Custom Ingredient Analysis:** `POST /api/v1/analysis/custom-ingredients`
- **User Auth:** `POST /api/v1/auth/register` & `POST /api/v1/auth/login`
- **User Profile & Allergens:** `GET|PUT /api/v1/profile/me`
- **Scan History:** `GET /api/v1/history`
