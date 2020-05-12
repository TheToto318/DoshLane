const signUpSpan = document.querySelector(".signup-span");
const loginSpan = document.querySelector(".login-span");

const signUpForm = document.querySelector(".signup");
const loginForm = document.querySelector(".login");

// Init
let theme = localStorage.getItem("theme");
const body = document.querySelector("body");

init();
async function init() {
  if (theme) {
    body.classList.add(theme);
    await sleep(250).then(() => {
      body.classList.add("smooth-bg-change");
    });
  } else {
    localStorage.setItem("theme", "dark");
    body.classList.add("dark");
    await sleep(250).then(() => {
      body.classList.add("smooth-bg-change");
    });
  }
}

function switchForm() {
  signUpSpan.classList.toggle("active");
  loginSpan.classList.toggle("active");
  signUpForm.classList.toggle("visible");
  loginForm.classList.toggle("visible");
}

function getData(inputs) {
  let valid = false;
  data = { valid: null, data: {} };
  inputs.forEach((input) => {
    if (input.value != "") {
      data["data"][input.placeholder] = input.value;
      valid = true;
    } else {
      valid = false;
    }
  });
  data["valid"] = valid;
  return data;
}

function signUp() {
  let inputs = document.querySelectorAll(".signup input");
  if (inputs[1].value != inputs[2].value) {
    failed("Passwords aren't the same");
  } else {
    data = getData(inputs);
    if (data["valid"] === true) {
      eel.signup(data["data"]);
    } else {
      failed("Provide a username and a password");
    }
  }
}

function login() {
  let inputs = document.querySelectorAll(".login input");
  data = getData(inputs);
  if (data["valid"] === true) {
    eel.login(data["data"]);
  } else {
    failed("Provide a username and a password");
  }
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// eel functions
eel.expose(validSignUp);
function validSignUp() {
  Swal.fire("DoshLane", "Signed Up successfully", "success").then(() => {
    document.location = "../App/index.html";
  });
}

eel.expose(validLogin);
function validLogin() {
  Swal.fire("DoshLane", "Logged in successfully", "success").then(() => {
    document.location = "../App/index.html";
  });
}

eel.expose(failed);
function failed(reason) {
  Swal.fire("DoshLane", reason, "error");
}
