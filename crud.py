from sqlalchemy.orm import Session

import models
import schemas
from security import hash_password, verify_password


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(
        name=student.name,
        phone=student.phone
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_students(db: Session):
    return db.query(models.Student).all()


def create_admin(db: Session, admin: schemas.AdminCreate):
    db_admin = models.Admin(
        username=admin.username,
        password=hash_password(admin.password)
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


def admin_login(db: Session, username: str, password: str):
    admin = db.query(models.Admin).filter(
        models.Admin.username == username
    ).first()

    if admin and verify_password(password, admin.password):
        return admin

    return None


def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(
        title=course.title,
        description=course.description,
        teacher=course.teacher
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def get_courses(db: Session):
    return db.query(models.Course).all()


def create_video(db: Session, video: schemas.VideoCreate):
    db_video = models.Video(
        course_id=video.course_id,
        title=video.title,
        video_url=video.video_url
    )
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


def get_videos(db: Session):
    return db.query(models.Video).all()


def create_note(db: Session, note: schemas.NoteCreate):
    db_note = models.Note(
        course_id=note.course_id,
        title=note.title,
        pdf_url=note.pdf_url
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_notes(db: Session):
    return db.query(models.Note).all()
