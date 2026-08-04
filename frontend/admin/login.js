const API = "https://nighasanschools.onrender.com";

async function login() {
    try {
        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value;

        if (!username || !password) {
            alert("Username aur Password dijiye");
            return;
        }

        const response = await fetch(API + "/admin/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username,
                password
            })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem("admin_token", data.access_token);
            alert("Login Successful");
            window.location.href = "dashboard.html";
        } else {
            alert(data.detail || "Login Failed");
        }

    } catch (err) {
        console.log(err);
        alert("Error: " + err.message);
    }
}
