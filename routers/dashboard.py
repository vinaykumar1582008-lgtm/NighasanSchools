from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

import crud
from database import SessionLocal
from security import verify_token

router = APIRouter()

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/admin/dashboard")
def admin_dashboard(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = verify_token(credentials.credentials)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid Token")

    username = payload.get("sub")

    admin = crud.get_admin_by_username(db, username)

    if not admin:
        raise HTTPException(status_code=403, detail="Admin access only")

    return {
        "total_students": len(crud.get_students(db)),
        "total_courses": len(crud.get_courses(db)),
        "total_notes": len(crud.get_notes(db)),
        "total_videos": len(crud.get_videos(db))
    }
