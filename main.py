from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
security = HTTPBearer()

# ==========================
# CORS
# ==========================

# ==========================
# Upload Folder
# ==========================

os.makedirs("uploads/videos", exist_ok=True)
os.makedirs("uploads/notes", exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

# ==========================
# Database
# ==========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================
# JWT Authentication
# ==========================

def admin_required(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    return payload
# ==========================
# Home
# ==========================

@app.get("/")
def home():
    return {
        "status": "OK",
        "message": "Nighasan Schools API चल रही है 🚀"
    }


# ==========================
# Student
# ==========================

@app.post("/register")
def register(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    return crud.create_student(db, student)


@app.get("/students")
def get_students(
    db: Session = Depends(get_db)
):
    return crud.get_students(db)


# ==========================
# Admin
# ==========================

@app.post("/admin/register")
def register_admin(
    admin: schemas.AdminCreate,
    db: Session = Depends(get_db)
):
    return crud.create_admin(db, admin)


@app.post("/admin/login")
def login_admin(
    admin: schemas.AdminLogin,
    db: Session = Depends(get_db)
):
    user = crud.admin_login(
        db,
        admin.username,
        admin.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
        {"sub": user.username}
    )

    return {
        "status": "success",
        "access_token": token,
        "token_type": "bearer"
    }
# ==========================
# Courses
# ==========================

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


@app.get("/courses/{course_id}")
def get_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    courses = crud.get_courses(db)

    for course in courses:
        if course.id == course_id:
            return course

    raise HTTPException(
        status_code=404,
        detail="Course not found"
    )


@app.delete("/courses/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    course = db.query(models.Course).filter(
        models.Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    db.delete(course)
    db.commit()

    return {
        "status": "success",
        "message": "Course deleted successfully"
    }
# ==========================
# Videos
# ==========================

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


# ==========================
# Notes
# ==========================

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


@app.get("/course/{course_id}/content")
def course_content(
    course_id: int,
    db: Session = Depends(get_db)
):
    videos = db.query(models.Video).filter(
        models.Video.course_id == course_id
    ).all()

    notes = db.query(models.Note).filter(
        models.Note.course_id == course_id
    ).all()

    return {
        "videos": videos,
        "notes": notes
    }
# ==========================
# Upload Video
# ==========================

@app.post("/upload/video")
def upload_video(
    file: UploadFile = File(...),
    admin=Depends(admin_required)
):
    file_path = f"uploads/videos/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "success",
        "filename": file.filename,
        "path": file_path,
        "url": f"/uploads/videos/{file.filename}"
    }


# ==========================
# Upload Notes
# ==========================

@app.post("/upload/note")
def upload_note(
    file: UploadFile = File(...),
    admin=Depends(admin_required)
):
    file_path = f"uploads/notes/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "success",
        "filename": file.filename,
        "path": file_path,
        "url": f"/uploads/notes/{file.filename}"
    }


# ==========================
# API Status
# ==========================

@app.get("/status")
def api_status():
    return {
        "status": "online",
        "app": "Nighasan Schools",
        "version": "1.0"
    }

@app.post("/login")
def student_login(
    student: schemas.StudentLogin,
    db: Session = Depends(get_db)
):
    user = crud.student_login(db, student.phone)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    token = create_access_token(
        {
            "sub": str(user.id),
            "role": "student"
        }
    )

    return {
        "status": "success",
        "access_token": token,
        "token_type": "bearer",
        "student": {
            "id": user.id,
            "name": user.name,
            "phone": user.phone
        }
    }

@app.get("/profile")
def student_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = verify_token(credentials.credentials)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    student_id = int(payload["sub"])

    student = crud.get_student_by_id(db, student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student
@app.put("/profile")
def update_profile(
    student: schemas.StudentUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = verify_token(credentials.credentials)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    student_id = int(payload["sub"])

    user = crud.update_student(db, student_id, student)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "status": "success",
        "message": "Profile updated successfully",
        "student": user
    }

@app.get("/search")
def search(
    q: str,
    db: Session = Depends(get_db)
):
    return crud.search_courses(db, q)

@app.get("/dashboard")
def student_dashboard(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = verify_token(credentials.credentials)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    if payload.get("role") != "student":
        raise HTTPException(
            status_code=403,
            detail="Student access only"
        )

    student_id = int(payload["sub"])

    student = crud.get_student_by_id(db, student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    courses = crud.get_courses(db)
    notes = crud.get_notes(db)
    videos = crud.get_videos(db)

    return {
        "student": student,
        "total_courses": len(courses),
        "total_notes": len(notes),
        "total_videos": len(videos)
    }
