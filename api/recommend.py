from fastapi import FastAPI
from fastapi import HTTPException

from fastapi.middleware.cors import (
    CORSMiddleware
)

from pydantic import BaseModel

from services.vikor import (
    calculate_vikor
)

# ======================================
# FASTAPI INIT
# ======================================

app = FastAPI(

    title=
        "TernakPro VIKOR API",

    description=
        "Sistem Pendukung Keputusan Rekomendasi Ternak Menggunakan Metode VIKOR",

    version="2.0.0"
)

# ======================================
# CORS
# ======================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# ======================================
# REQUEST MODEL
# ======================================

class VikorRequest(BaseModel):

    modal: float

    lahan: float

    waktu: int

    pengalaman: str

    mode: str = "pure"
    preset: str = "menengah"

# ======================================
# ROOT ENDPOINT
# ======================================

@app.get("/")
async def root():

    return {

        "message":
            "TernakPro VIKOR API",

        "status":
            "online",

        "method":
            "VIKOR",

        "version":
            "2.0.0"
    }

# ======================================
# HEALTH CHECK
# ======================================

@app.get("/api/health")
async def health_check():

    return {

        "status":
            "healthy",

        "service":
            "TernakPro VIKOR API",

        "method":
            "VIKOR"
    }

# ======================================
# VIKOR ENDPOINT
# ======================================

@app.post("/api/recommend-vikor")
async def recommend_vikor(

    request: VikorRequest
):

    try:

        user_input = {

            "modal":
                request.modal,

            "lahan":
                request.lahan,

            "waktu":
                request.waktu,

            "pengalaman":
                request.pengalaman,

            "mode":
                request.mode
        ,
            "preset":
                request.preset
        }

        result = calculate_vikor(
            user_input,
            mode=request.mode,
            preset=request.preset
        )

        return {

            "success": True,

            "method": "VIKOR",

            "mode": request.mode,

            "recommendations":
                result
        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )

# ======================================
# VERCEL HANDLER
# ======================================

def handler(request):

    return app