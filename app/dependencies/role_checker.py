from fastapi import Depends, HTTPException, status
from app.utils.jwt import verify_token  # use your existing JWT function


def get_current_admin_user(token: str = Depends(verify_token)):
    if token.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return token