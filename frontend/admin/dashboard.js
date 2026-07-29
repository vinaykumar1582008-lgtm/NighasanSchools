if (!localStorage.getItem("admin_token")) {
    window.location = "login.html";
}

function showPage(page){

    document.getElementById("title").innerHTML =
        page.charAt(0).toUpperCase() + page.slice(1);

    let html = "";

    if(page=="dashboard"){

        html=`
        <h2>Dashboard</h2>

        <div style="display:flex;gap:20px;flex-wrap:wrap;">

        <div class="card">
        👨‍🎓<br>Total Students<br><b id="studentsCount">0</b>
        </div>

        <div class="card">
        📚<br>Total Courses<br><b id="coursesCount">0</b>
        </div>

        <div class="card">
        👨‍💼<br>Total Admins<br><b id="adminsCount">0</b>
        </div>

        </div>
        `;

    }

    else if(page=="students"){

        html=`
        <h2>Students</h2>

        <button>Add Student</button>

        <div id="studentList"></div>
        `;

    }

    else if(page=="courses"){

        html=`
        <h2>Courses</h2>

        <button>Add Course</button>

        <div id="courseList"></div>
        `;

    }

    else if(page=="notes"){

        html="<h2>Notes Management</h2>";

    }

    else if(page=="tests"){

        html="<h2>Test Management</h2>";

    }

    else if(page=="admins"){

        html=`
        <h2>Admin Management</h2>

        <button>Add New Admin</button>

        <div id="adminList"></div>
        `;

    }

    else if(page=="settings"){

        html="<h2>Settings</h2>";

    }

    document.getElementById("content").innerHTML = html;

}

function logout(){

    localStorage.removeItem("admin_token");

    window.location="login.html";

}

showPage("dashboard");
