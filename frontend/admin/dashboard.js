const API = "https://nighasanschools.onrender.com";

const token = localStorage.getItem("admin_token");

if (!token) {
    window.location.href = "login.html";
}

async function loadDashboard() {

const response = await fetch(API + "/admin/dashboard", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    if (!response.ok) {
        alert("Session Expired");
        localStorage.removeItem("admin_token");
        window.location.href = "login.html";
        return;
    }

    const data = await response.json();

    document.getElementById("students").innerHTML =
        data.total_students;

    document.getElementById("courses").innerHTML =
        data.total_courses;
}

function logout() {
    localStorage.removeItem("admin_token");
    window.location.href = "login.html";
}

loadDashboard();
