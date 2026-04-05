from fastapi import APIRouter
from service.user_auth import login, register

router = APIRouter(
    prefix="/v1/api/analysis",
    tags=["analysis"],
)

@router.post("/login")
async def login_endpoint():
    return {"message": "Login endpoint - not implemented"}

@router.post("/register")
async def register_endpoint():
    return {"message": "Register endpoint - not implemented"}