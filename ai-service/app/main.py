import uvicorn
from fastapi import FastAPI
from app.api.endpoints import router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Garanti BBVA Fikrinle Parla - AI Analiz Servisi"
)


app.include_router(router, prefix=settings.API_STR)

@app.get("/")
def read_root():
    return {"status": "online", "message": "Finansal Pusula AI Servisi Aktif!"}

if __name__ == "__main__":

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)