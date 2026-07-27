const firebaseConfig = {
  apiKey: "AIzaSyCxZsSJw53sGHAAezLsv63G15QC9rWxIro",
  authDomain: "nighasanschools-3287b.firebaseapp.com",
  projectId: "nighasanschools-3287b",
  storageBucket: "nighasanschools-3287b.firebasestorage.app",
  messagingSenderId: "411459741463",
  appId: "1:411459741463:web:e7a296a176219744453952"
};

firebase.initializeApp(firebaseConfig);

const auth = firebase.auth();

window.onload = function () {
    window.recaptchaVerifier = new firebase.auth.RecaptchaVerifier(
        "recaptcha-container",
        {
            size: "normal"
        }
    );
    recaptchaVerifier.render();
};

let confirmationResult = null;

function sendOTP() {
    const phone = document.getElementById("phone").value.trim();

    if (phone.length != 10) {
        document.getElementById("msg").innerHTML = "10 अंकों का मोबाइल नंबर दर्ज करें";
        return;
    }

    auth.signInWithPhoneNumber("+91" + phone, window.recaptchaVerifier)
        .then((result) => {
            confirmationResult = result;
            document.getElementById("otpBox").style.display = "block";
            document.getElementById("msg").innerHTML = "OTP भेज दिया गया";
        })
        .catch((error) => {
            document.getElementById("msg").innerHTML = error.message;
        });
}

function verifyOTP() {
    const otp = document.getElementById("otp").value;

    confirmationResult.confirm(otp)
        .then((result) => {
            document.getElementById("msg").innerHTML = "Login Successful";
            console.log(result.user);
        })
        .catch((error) => {
            document.getElementById("msg").innerHTML = "गलत OTP";
        });
}
