from fastapi import APIRouter, HTTPException
from app.models.request_models import AnalysisRequest
from app.agents.orchestrator import FinancialOrchestrator

router = APIRouter()

@router.post("/analyze")
async def analyze_finances(request: AnalysisRequest):
    try:
        # Gelen JSON verisini orkestratöre paslıyoruz
        orchestrator = FinancialOrchestrator(request)
        result = orchestrator.run_full_analysis()
        return result
    except Exception as e:
        # Bir hata olursa (örn: yanlış veri tipi) 500 hatası dönüyoruz
        raise HTTPException(status_code=500, detail=f"Analiz sırasında hata: {str(e)}")