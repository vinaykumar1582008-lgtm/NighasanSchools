const API = "https://nighasanschools.onrender.com";

document.getElementById("thumbnail").onchange = function () {
    const file = this.files[0];
    if (file) {
        document.getElementById("preview").src = URL.createObjectURL(file);
    }
};

async function createCourse() {

    try {

        const title = document.getElementById("title").value.trim();
        const teacher = document.getElementById("teacher").value.trim();
        const description = document.getElementById("description").value.trim();

        const thumbnail = document.getElementById("thumbnail").files[0];
        const banner = document.getElementById("banner").files[0];

        if (!title || !teacher) {
            alert("Course Name aur Teacher Name bhariye");
            return;
        }

        const token = localStorage.getItem("admin_token");

        let thumbnailUrl = "";
        let bannerUrl = "";

        if (thumbnail) {

            const form = new FormData();
            form.append("file", thumbnail);

            const upload = await fetch(API + "/upload/thumbnail", {
                method: "POST",
                body: form
            });

            const result = await upload.json();
            thumbnailUrl = result.url;
        }

        if (banner) {

            const form = new FormData();
            form.append("file", banner);

            const upload = await fetch(API + "/upload/banner", {
                method: "POST",
                body: form
            });

            const result = await upload.json();
            bannerUrl = result.url;
        }

        const response = await fetch(API + "/courses", {

            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },

            body: JSON.stringify({

                title: title,
                teacher: teacher,
                description: description,
                thumbnail: thumbnailUrl,
                banner: bannerUrl

            })

        });

        const data = await response.json();

        if (response.ok) {

            alert("Course Created Successfully");

            window.location.href = "courses.html";

        } else {

            alert(data.detail || "Course Create Failed");

        }

    } catch (err) {

        console.log(err);

        alert("Error : " + err.message);

    }

}
