const API = "https://nighasanschools.onrender.com";

const thumbnailInput = document.getElementById("thumbnail");
const bannerInput = document.getElementById("banner");

if (thumbnailInput) {
    thumbnailInput.onchange = function () {
        const file = this.files[0];
        if (file) {
            const img = document.getElementById("preview");
            img.src = URL.createObjectURL(file);
            img.style.display = "block";
        }
    };
}

if (bannerInput) {
    bannerInput.onchange = function () {
        const file = this.files[0];
        if (file) {
            const img = document.getElementById("bannerPreview");
            if (img) {
                img.src = URL.createObjectURL(file);
                img.style.display = "block";
            }
        }
    };
}

async function uploadFile(file, endpoint) {

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(API + endpoint, {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        throw new Error("Upload Failed");
    }

    return await response.json();
}

async function createCourse() {

    try {

        const title = document.getElementById("title").value.trim();
        const teacher = document.getElementById("teacher").value.trim();
        const description = document.getElementById("description").value.trim();

        if (!title || !teacher) {
            alert("Course Name aur Teacher Name bhariye");
            return;
        }

        const thumbnail = thumbnailInput.files[0];
        const banner = bannerInput.files[0];

        let thumbnailUrl = "";
        let bannerUrl = "";

        if (thumbnail) {
            const res = await uploadFile(thumbnail, "/upload/thumbnail");
            thumbnailUrl = res.url;
        }

        if (banner) {
            const res = await uploadFile(banner, "/upload/banner");
            bannerUrl = res.url;
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
                description,
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
        alert(err.message);
    }
}
