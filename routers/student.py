from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

router = APIRouter(tags=["Students"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    user = crud.create_student(db, student)

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Mobile number already registered"
        )

    return user


@router.get("/students")
def get_students(
    db: Session = Depends(get_db)
):
    return crud.get_students(db)
