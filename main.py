from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import shutil
import os

import models
import schemas
import crud
from database import engine, SessionLocal
from security import create_access_token, verify_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nighasan Schools API")
security = HTTPBearer()
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def admin_required(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return payload


@app.get("/")
def home():
    return {
        "status": "OK",
        "message": "Nighasan Schools API चल रही है 🚀"
    }


@app.post("/register")
def register(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)


@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    return crud.get_students(db)


@app.post("/admin/register")
def register_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    return crud.create_admin(db, admin)


@app.post("/admin/login")
def login_admin(admin: schemas.AdminLogin, db: Session = Depends(get_db)):
    user = crud.admin_login(db, admin.username, admin.password)

    if not user:
        return {
            "status": "error",
            "message": "Invalid username or password"
        }

    token = create_access_token({"sub": user.username})

    return {
        "status": "success",
        "access_token": token,
        "token_type": "bearer"
    }
@app.post("/courses")
def add_course(
    course: schemas.CourseCreate,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    return crud.create_course(db, course)


@app.get("/courses")
def list_courses(
    db: Session = Depends(get_db)
):
    return crud.get_courses(db)


@app.post("/videos")
def add_video(
    video: schemas.VideoCreate,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    return crud.create_video(db, video)


@app.get("/videos")
def list_videos(
    db: Session = Depends(get_db)
):
    return crud.get_videos(db)


@app.post("/notes")
def add_note(
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    return crud.create_note(db, note)


@app.get("/notes")
def list_notes(
    db: Session = Depends(get_db)
):
    return crud.get_notes(db)
@app.post("/upload/video")
def upload_video(
    file: UploadFile = File(...),
    admin=Depends(admin_required)
):
    os.makedirs("uploads/videos", exist_ok=True)

    file_path = f"uploads/videos/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "success",
        "filename": file.filename,
        "path": file_path,
        "url": f"/uploads/videos/{file.filename}"
    }


@app.post("/upload/note")
def upload_note(
    file: UploadFile = File(...),
):
    os.makedirs("uploads/notes", exist_ok=True)

    file_path = f"uploads/notes/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "success",
        "filename": file.filename,
        "path": file_path,
        "url": f"/uploads/notes/{file.filename}"
    }
