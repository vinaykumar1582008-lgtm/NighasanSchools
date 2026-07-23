const API = "https://nighasanschools.onrender.com";

async function login() {

    let phone = document.getElementById("phone").value;

    if (phone == "") {
        document.getElementById("msg").innerHTML = "मोबाइल नंबर दर्ज करें";
        return;
    }

    try {

        let response = await fetch(API + "/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                phone: phone
            })
        });

        let data = await response.json();

        if (response.ok) {

            localStorage.setItem("token", data.access_token);
            localStorage.setItem("student", JSON.stringify(data.student));

            document.getElementById("msg").innerHTML = "✅ Login Successful";

            setTimeout(() => {
                window.location = "home.html";
            }, 1000);

        } else {

            document.getElementById("msg").innerHTML = "❌ " + data.detail;

        }

    } catch (e) {

        document.getElementById("msg").innerHTML = "❌ API Connect नहीं हो रही";
        console.log(e);

    }
}
