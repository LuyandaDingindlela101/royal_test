// fetch("http://127.0.0.1:5000/show-products/")
// .then(responce => responce.json())
// .then(data => {
//     console.log(data);
// })

let login_btn = document.querySelector('.login-btn');
let signup_btn = document.querySelector('.register-btn');

let login_form = document.querySelector(".login");
let register_form = document.querySelector(".register");

login_btn.addEventListener('click', () => {
    login_form.classList.toggle("inactive");
    register_form.classList.toggle("inactive");
});

signup_btn.addEventListener('click', () => {
    login_form.classList.toggle("inactive");
    register_form.classList.toggle("inactive");
});