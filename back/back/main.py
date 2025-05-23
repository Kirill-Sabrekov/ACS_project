from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.endpoints import router as api_router

app = FastAPI(title="Sensor Monitoring API")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутер API
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Sensor Monitoring API is running"}
