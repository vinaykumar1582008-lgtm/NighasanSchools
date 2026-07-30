const API = "https://nighasanschools.onrender.com";

const token = localStorage.getItem("admin_token");

if (!token) {
    window.location.href = "login.html";
}

async function addCourse() {

    const title = document.getElementById("title").value;
    const teacher = document.getElementById("teacher").value;
    const description = document.getElementById("description").value;

    const response = await fetch(API + "/courses", {

        method: "POST",

        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },

        body: JSON.stringify({
            title: title,
            teacher: teacher,
            description: description
        })

    });

    if (response.ok) {

        alert("Course Added Successfully");

        document.getElementById("title").value = "";
        document.getElementById("teacher").value = "";
        document.getElementById("description").value = "";

        loadCourses();

    } else {

        alert("Error Adding Course");

    }

}

async function loadCourses() {

    const response = await fetch(API + "/courses");

    const data = await response.json();

    let html = "";

    data.forEach(course => {

        html += `
        <div class="card">
            <h3>${course.title}</h3>
            <p>${course.teacher}</p>
            <p>${course.description}</p>
        </div>
        `;

    });

    document.getElementById("courseList").innerHTML = html;

}

loadCourses();
