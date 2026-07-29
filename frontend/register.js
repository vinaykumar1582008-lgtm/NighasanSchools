const API = "https://nighasanschools.onrender.com";

async function registerStudent() {

    const name = document.getElementById("name").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const password = document.getElementById("password").value;

    if (name === "" || phone === "" || password === "") {
        document.getElementById("msg").innerHTML = "सभी जानकारी भरें";
        return;
    }

    try {

        const response = await fetch(API + "/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name,
                phone: phone,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById("msg").innerHTML = "✅ Registration Successful";

            setTimeout(() => {
                window.location = "index.html";
            }, 1500);

        } else {

            document.getElementById("msg").innerHTML = "❌ " + (data.detail || "Registration Failed");

        }

    } catch (err) {

        document.getElementById("msg").innerHTML = "❌ Server Error";
        console.log(err);

    }

}
