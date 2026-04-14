from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def profile():
    return {"message": "Profile API working"}