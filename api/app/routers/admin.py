from fastapi import APIRouter, Depends
from app.auth.dependencies import require_role
from app.models.enums import UserRole

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/only-admin")
def admin_only(
    _=Depends(require_role(UserRole.admin))
):
    return {"message": "Welcome Admin"}
