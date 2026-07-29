const student = JSON.parse(localStorage.getItem("student"));

if (!student) {
    window.location = "index.html";
}

document.getElementById("welcome").innerHTML =
    "Welcome, " + student.name + " 👋";

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("student");
    window.location = "index.html";
}
