# TernakPro AI Service

AI Rekomendasi Ternak service untuk TernakPro.

## Setup

1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Place model file in `models/rekomendasi_ternak_ternakpro_v1_model.pkl`
4. Deploy to Vercel

## API Endpoints

- `POST /api/recommend-vikor` - Get livestock recommendation using VIKOR
- `GET /api/health` - Health check
- `GET /` - Root endpoint