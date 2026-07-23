from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    phone: str

class StudentResponse(BaseModel):
    id: int
    name: str
    phone: str

    class Config:
        from_attributes = True
class AdminCreate(BaseModel):
    username: str
    password: str

class AdminResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
class CourseCreate(BaseModel):
    title: str
    description: str
    teacher: str

class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    teacher: str

    class Config:
        from_attributes = True


class VideoCreate(BaseModel):
    course_id: int
    title: str
    video_url: str

class VideoResponse(BaseModel):
    id: int
    course_id: int
    title: str
    video_url: str

    class Config:
        from_attributes = True

class NoteCreate(BaseModel):
    course_id: int
    title: str
    pdf_url: str


class NoteResponse(BaseModel):
    id: int
    course_id: int
    title: str
    pdf_url: str

    class Config:
        from_attributes = True

class AdminLogin(BaseModel):
    username: str
    password: str

class StudentLogin(BaseModel):
    phone: str

class StudentUpdate(BaseModel):
    name: str
    phone: str
