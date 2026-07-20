
const API = "https://nighasanschools.onrender.com";
async function login() {

    let phone = document.getElementById("phone").value;

    if (phone == "") {
        document.getElementById("msg").innerHTML = "मोबाइल नंबर दर्ज करें";
        return;
    }

    try {

        let response = await fetch(API + "/students");
        alert(response.status);
        let students = await response.json();

        let user = students.find(s => s.phone === phone);

        if (user) {

            localStorage.setItem("student", JSON.stringify(user));
            document.getElementById("msg").innerHTML = "✅ Login Successful";

            setTimeout(() => {
                window.location = "home.html";
            }, 1000);

        } else {

            document.getElementById("msg").innerHTML = "❌ Student नहीं मिला";

        }

    } catch (e) {

        document.getElementById("msg").innerHTML = "❌ API Connect नहीं हो रही";
        console.error(e);
        alert(e);

    }
}
