from fastapi import APIRouter, HTTPException
from analysis_queue.analysis_worker import process_brain_analysis
from schema.analysis_schema import AnalysisRequest

router = APIRouter(
    prefix="/v1/api/analysis",
    tags=["analysis"],
)

@router.post("/process")
async def process_brain_analysis_endpoint(req: AnalysisRequest):
    try:
        print(req)
        task = process_brain_analysis.delay(req.html, req.user_id)
        print(task)
        return {"status": "queued", "task_id": task.id}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))