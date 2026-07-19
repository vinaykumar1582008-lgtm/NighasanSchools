from fastapi import FastAPI

app = FastAPI(title="Nighasan Schools API")

students = []

courses = [
    {
        "id": 1,
        "title": "Class 10 Science",
        "teacher": "Vinay Maurya"
    },
    {
        "id": 2,
        "title": "Class 12 Physics",
        "teacher": "Vinay Maurya"
    }
]

@app.get("/")
def home():
    return {
        "status": "OK",
        "message": "Nighasan Schools API चल रही है 🚀"
    }

@app.get("/courses")
def get_courses():
    return courses

@app.get("/students")
def get_students():
    return students

@app.post("/register")
def register(name: str, phone: str):
    student = {
        "name": name,
        "phone": phone
    }
    students.append(student)
    return {
        "status": "success",
        "student": student
    }
