from fastapi import APIRouter, Depends
from app.auth.dependencies import require_role
from app.models.enums import UserRole
from app.seed import run as seed_run

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/only-admin")
def admin_only(
    _=Depends(require_role(UserRole.admin))
):
    return {"message": "Welcome Admin"}

@router.post("/seed")
def seed_database():
    seed_run()
    return {"status": "database seeded"}