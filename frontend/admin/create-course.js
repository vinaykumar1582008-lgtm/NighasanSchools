document.getElementById("thumbnail").onchange = function(){

    const file = this.files[0];

    document.getElementById("preview").src =
        URL.createObjectURL(file);

}

const API = "https://nighasanschools.onrender.com";

async function createCourse() {

    const title = document.getElementById("title").value;
    const teacher = document.getElementById("teacher").value;
    const description = document.getElementById("description").value;

    if (!title || !teacher) {
        alert("Course Name aur Teacher Name bhariye");
        return;
    }

    const token = localStorage.getItem("admin_token");

    const response = await fetch(API + "/courses", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
            title,
            teacher,
            description
        })
    });

    const data = await response.json();

    if (response.ok) {
        alert("Course Created");
        window.location.href = "courses.html";
    } else {
        alert(data.detail || "Error");
    }
}
