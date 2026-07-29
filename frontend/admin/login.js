const API = "https://nighasanschools.onrender.com";

async function loginAdmin() {

    let username = document.getElementById("username").value.trim();
    let password = document.getElementById("password").value;

    if(username=="" || password==""){
        document.getElementById("msg").innerHTML="Username और Password दर्ज करें";
        return;
    }

    try{

        let response = await fetch(API + "/admin/login",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                username:username,
                password:password
            })

        });

        let data = await response.json();

        if(response.ok){

            localStorage.setItem("admin_token",data.access_token);

            window.location="dashboard.html";

        }else{

            document.getElementById("msg").innerHTML=data.detail;

        }

    }catch(err){

        document.getElementById("msg").innerHTML="Server Error";

    }

}
