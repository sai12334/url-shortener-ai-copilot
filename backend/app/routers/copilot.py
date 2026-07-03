"""
HTTP layer for the AI-assisted engineering copilot workflow.
"""
from fastapi import APIRouter

from app.schemas import CopilotRequest, CopilotResponse
from app.services.copilot_engine import run_copilot

router = APIRouter(prefix="/copilot", tags=["copilot"])


@router.post("/analyze", response_model=CopilotResponse)
def analyze_requirement(payload: CopilotRequest):
    return run_copilot(payload.requirement)
