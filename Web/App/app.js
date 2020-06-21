// INIT
let theme = localStorage.getItem("theme");
const body = document.querySelector("body");
const Pbtn = document.getElementById("changePswd");
const Ubtn = document.getElementById("changeUsrname");

if (theme) {
  body.classList.add(theme);
  sleep(250).then(() => {
    body.classList.add("smooth-bg-change");
    document.querySelector(".navbar").classList.add("smooth-nav-change");
  });
} else {
  localStorage.setItem("theme", "dark");
  body.classList.add("dark");
  sleep(250).then(() => {
    body.classList.add("smooth-bg-change");
    document.querySelector(".navbar").classList.add("smooth-nav-change");
  });
}

Pbtn.addEventListener("click", changePassword);
Ubtn.addEventListener("click", changeUsername);

// eel calls
eel.get_pswds_list();
eel.get_notes_list();

let nbPaswds = document.querySelectorAll(".password-wrapper").length;
let nbNotes = document.querySelectorAll(".password-wrapper").length;
document.querySelector(".param-wrapper-input input").value = 15;

let charsToUse = {
  letters: false,
  numbers: false,
  symbols: false,
  caps: false,
  spaces: false,
};

// SVG
function showEmptySvg() {
  if (nbPaswds == 0) {
    document.querySelector(".svg-if-no-pswd").style.display = "grid";
    document.querySelector(".home").style.paddingBottom = "0";
  } else {
    document.querySelector(".svg-if-no-pswd").style.display = "none";
    document.querySelector(".home").style.paddingBottom = "10vh";
  }
  if (nbNotes == 0) {
    document.querySelector(".svg-if-no-note").style.display = "grid";
    document.getElementById("notes").style.paddingBottom = "0";
  } else {
    document.querySelector(".svg-if-no-note").style.display = "none";
    document.getElementById("notes").style.paddingBottom = "10vh";
  }
}

// Section Handler
function switchsection(sectionId, svgId) {
  document.querySelector(".active").classList.toggle("active");
  document.getElementById(svgId).classList.toggle("active");

  newSection = document.getElementById(sectionId);
  oldSection = document.querySelector("section.visible");
  if (oldSection != newSection) {
    oldSection.classList.toggle("visible");
    newSection.classList.toggle("visible");
  }
}

// NavBar
async function hideNavOnClick() {
  let nav = document.querySelector(".navbar");
  if (window.innerWidth > 850) {
    nav.style.pointerEvents = "none";
    await sleep(750).then(() => {
      nav.style.pointerEvents = "all";
    });
  }
}

// Password Realated
async function showDetails(i, model) {
  const dropdownBox = document.getElementById(`${model}${i}`);
  if (dropdownBox.classList.contains("open-height")) {
    await sleep(10).then(() => {
      dropdownBox.classList.remove("smooth-height");
    });
    await sleep(10).then(() => {
      dropdownBox.classList.remove("open-height");
    });
    await sleep(10).then(() => {
      dropdownBox.classList.add("smooth-height");
    });
  } else {
    dropdownBox.classList.add("open-height");
  }

  // Change Arrow
  dropdownBox.querySelector(".arrow").classList.toggle("open");
  dropdownBox.querySelector(".dropdown__bottom").classList.toggle("open");
}

function updateDropdownContainer() {
  if (nbPaswds < 1) {
    showEmptySvg();
    document.querySelector(".password-container").classList.add("no-before");
  } else {
    document.querySelector(".password-container").classList.remove("no-before");
  }
  if (nbNotes < 1) {
    showEmptySvg();
    document.querySelector(".notes-container").classList.add("no-before");
  } else {
    document.querySelector(".notes-container").classList.remove("no-before");
  }
}

// Gettings Data
eel.expose(retrievePassword);
function retrievePassword(data) {
  let userInfos = data;
  userInfos.forEach((infos) => {
    addPasswordField(infos[0], infos[1]);
  });
}

eel.expose(retrieveNotes);
function retrieveNotes(data) {
  let userInfos = data;
  userInfos.forEach((infos) => {
    addNoteField(infos[0], infos[1]);
  });
}

function getPassword(i, model) {
  const box = document.querySelector(`#${model}${i}`);
  const website = box.querySelector(".dropdown__domain").innerHTML;
  const username = box.querySelector(".username").innerHTML;
  console.log(website, username);
  eel.get_pswd(username, website);
}

eel.expose(copyPassword);
function copyPassword(password) {
  copyToClipboard(password);
  Swal.fire("Copied!", "Password copied to your clipboard", "success");
}

// Adding Fields
eel.expose(addPasswordField);
function addPasswordField(username, website) {
  nbPaswds++;
  let container = `
  <div class="dropdown-wrapper smooth-height" id="pswd${nbPaswds}">
    <div class="dropdown__top">
      <h1 class="dropdown__domain">${website}</h1>
      <div class="edit-icon">
        <svg viewBox="0 0 150.004 149.998" onclick="edit(${nbPaswds}, 'pswd')">
          <path d="M85.178,27.316l37.506,37.506L41.241,146.265,7.8,149.956a7.032,7.032,0,0,1-7.761-7.767l3.721-33.463Zm60.7-5.584-17.61-17.61a14.07,14.07,0,0,0-19.9,0L91.808,20.689,129.313,58.2l16.567-16.567A14.07,14.07,0,0,0,145.881,21.732Z" transform="translate(0.003 -0.002)" class="svg-fill-main-color"/>     
        </svg>
      </div>
      <div class="bin">
        <svg onclick="eel.delete_password(${nbPaswds}, '${username}', '${website}');" viewBox="0 0 20.19 24.849">
          <path d="M6.052,9.693v15.53A1.558,1.558,0,0,0,7.6,26.777H21.582a1.558,1.558,0,0,0,1.553-1.553V9.693Zm4.659,13.977H9.158V12.8h1.553Zm3.106,0H12.264V12.8h1.553Zm3.106,0H15.37V12.8h1.553Zm3.106,0H18.476V12.8h1.553ZM23.523,5.034H18.476V3.093a1.168,1.168,0,0,0-1.165-1.165H11.876a1.168,1.168,0,0,0-1.165,1.165V5.034H5.664A1.168,1.168,0,0,0,4.5,6.2V8.14H24.688V6.2a1.168,1.168,0,0,0-1.165-1.165Zm-6.6,0H12.264V3.5h4.659V5.034Z" transform="translate(-4.499 -1.928)" />
        </svg>
      </div>
      <div class="arrow" onclick="showDetails(${nbPaswds}, 'pswd');">
        <div class="arrow-pt1"></div>
        <div class="arrow-pt2"></div>
      </div>
    </div>
    <div class="dropdown__bottom closed">
      <h1 class="username">${username}</h1>
      <button class="dropdown" onclick="getPassword(${nbPaswds}, 'pswd')">Click to copy</button>
    </div>
  </div>`;
  document.querySelector(".password-container").innerHTML += container;
  showEmptySvg();
}

eel.expose(addNoteField);
function addNoteField(title, content) {
  nbNotes++;
  let container = `
  <div class="dropdown-wrapper smooth-height" id="note${nbNotes}">
    <div class="dropdown__top">
      <h1 class="dropdown__title">${title}</h1>
      <div class="edit-icon">
        <svg viewBox="0 0 150.004 149.998" onclick="edit(${nbNotes}, 'note')">
          <path d="M85.178,27.316l37.506,37.506L41.241,146.265,7.8,149.956a7.032,7.032,0,0,1-7.761-7.767l3.721-33.463Zm60.7-5.584-17.61-17.61a14.07,14.07,0,0,0-19.9,0L91.808,20.689,129.313,58.2l16.567-16.567A14.07,14.07,0,0,0,145.881,21.732Z" transform="translate(0.003 -0.002)" class="svg-fill-main-color"/>     
        </svg>
      </div> 
      <div class="bin">
        <svg onclick="eel.delete_note(${nbNotes}, '${title}');" viewBox="0 0 20.19 24.849">
          <path d="M6.052,9.693v15.53A1.558,1.558,0,0,0,7.6,26.777H21.582a1.558,1.558,0,0,0,1.553-1.553V9.693Zm4.659,13.977H9.158V12.8h1.553Zm3.106,0H12.264V12.8h1.553Zm3.106,0H15.37V12.8h1.553Zm3.106,0H18.476V12.8h1.553ZM23.523,5.034H18.476V3.093a1.168,1.168,0,0,0-1.165-1.165H11.876a1.168,1.168,0,0,0-1.165,1.165V5.034H5.664A1.168,1.168,0,0,0,4.5,6.2V8.14H24.688V6.2a1.168,1.168,0,0,0-1.165-1.165Zm-6.6,0H12.264V3.5h4.659V5.034Z" transform="translate(-4.499 -1.928)"></path>
        </svg>
      </div>
      <div class="arrow" onclick="showDetails(${nbNotes}, 'note');">
        <div class="arrow-pt1"></div>
        <div class="arrow-pt2"></div>
      </div>
    </div>
    <div class="dropdown__bottom closed">
      <h1 class="content">${content}</h1>
    </div>
  </div>`;
  document.querySelector(".notes-container").innerHTML += container;
  showEmptySvg();
}

// Cheking exists function
function dontExists(data, model) {
  if (model === "pswd") {
    let usernamesElem = document.querySelectorAll(".username");
    let websitesElem = document.querySelectorAll(".dropdown__domain");
    usernames = [];
    websites = [];
    usernamesElem.forEach((elem) => {
      usernames.push(elem.innerHTML);
    });
    websitesElem.forEach((elem) => {
      websites.push(elem.innerHTML);
    });
    if (usernames.includes(data[0]) && websites.includes(data[2])) {
      Swal.fire("Error", "This username is already registered for this website", "error");
      return false;
    } else {
      return true;
    }
  } else if (model === "note") {
    let titlesElem = document.querySelectorAll(".dropdown__title");
    let contentElem = document.querySelectorAll(".content");
    titles = [];
    contents = [];
    titlesElem.forEach((elem) => {
      titles.push(elem.innerHTML);
    });
    contentElem.forEach((elem) => {
      contents.push(elem.innerHTML);
    });
    if (titles.includes(data[0])) {
      Swal.fire("Error", "This title is already used for another note", "error");
      return false;
    } else if (contents.includes(data[1])) {
      Swal.fire("Error", "You have already wrote this in another note", "error");
      return false;
    } else {
      return true;
    }
  }
}

// Adding Button
function addPasswordBtn() {
  let data = document.querySelectorAll(".add-container input");
  let dataObj = data;
  values = [];
  data.forEach((x) => {
    values.push(x.value);
  });
  data = values;
  if (dontExists(data, "pswd") === true) {
    eel.save_password(data[0], data[1], data[2]);
    dataObj.forEach((input) => {
      clearInput(input, 35);
    });
  }
}

function addNoteBtn() {
  let data = document.querySelectorAll(".add-note input");
  let dataObj = data;
  values = [];
  data.forEach((x) => {
    values.push(x.value);
  });
  data = values;
  if (dontExists(data, "note") === true) {
    eel.save_note(data[0], data[1]);
    dataObj.forEach((input) => {
      clearInput(input, 5);
    });
  }
}

// Editing Dropdown
function edit(i, model) {
  if (model == "pswd") {
    Swal.mixin({
      input: "text",
      showCancelButton: true,
      confirmButtonText: "Next",
      progressSteps: ["1", "2"],
    })
      .queue(["Username", "Password"])
      .then((result) => {
        if (result.value) {
          result = result.value;
          pswd = document.getElementById(`${model}${i}`);
          if (dontExists(result, "pswd") === true) {
            const website = pswd.querySelector(".dropdown__domain");
            const username = pswd.querySelector(".username");
            eel.update_password(i, username.innerHTML, website.innerHTML);
            username.innerHTML = result[0];
            pswd.querySelector(".bin").setAttribute("onclick", `eel.delete_password(${i}, '${result[0]}', '${website}');`);
            Swal.fire("Updated!", "Your data has been updated.", "success");
          }
        }
      });
  } else {
    Swal.mixin({
      input: "text",
      showCancelButton: true,
      confirmButtonText: "Next",
      progressSteps: ["1", "2"],
    })
      .queue(["Title", "Content"])
      .then((result) => {
        if (result.value) {
          result = result.value;
          note = document.getElementById(`${model}${i}`);
          noteTitle = note.querySelector(".dropdown__title");
          oldTitle = noteTitle.innerHTML;
          if (dontExists(result, "note")) {
            noteTitle.innerHTML = result[0];
            note.querySelector(".content").innerHTML = result[1];
            note.setAttribute("onclick", `eel.delete_note(${i}, '${result[0]}');`);
            eel.update_note(i, oldTitle, result[0], result[1]);
          }
        }
      });
  }
}

// Deleting Function
eel.expose(deleteDropdown);
function deleteDropdown(i, model) {
  const passwordBox = document.getElementById(`${model}${i}`);

  Swal.fire({
    title: "Are you sure?",
    text: "You won't be able to revert this!",
    icon: "warning",
    showCancelButton: true,
    cancelButtonColor: "#d33",
    confirmButtonText: "Yes, delete it!",
  }).then((result) => {
    if (result.value) {
      Swal.fire("Deleted!", "Your file has been deleted.", "success");
      passwordBox.remove();
      updateDropdownContainer();
    }
  });
}

// Checbox Animation
function animateCheckBox(i, char) {
  let checkbox = document.getElementById(`cb${i}`);
  let svg = document.getElementById(`checkbox${i}`);
  if (checkbox.checked) {
    charsToUse[char] = false;
    svg.classList.add("reverse");
  } else {
    charsToUse[char] = true;
    svg.classList.remove("reverse");
  }
  generate();
}

// Password Generation
function generate() {
  let length = document.querySelector(".param-wrapper-input input");
  if (length.value > 50) {
    length.value = 50;
  }
  let lists = {
    letters: ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"],
    numbers: ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    symbols: ["&", "~", '"', "#", "'", "{", "(", "[", "-", "|", "`", "_", "\\", "^", "@", ")", "]", "=", "}", "°", "+", "¨", "£", "%", "µ", "§", "/", ".", "?", ",", ";", ":", "!", "ù", "*", "^", "$", "¤"],
    caps: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
    spaces: [" "],
  };
  let toUse = [];
  for (const [key, value] of Object.entries(charsToUse)) {
    if (value === true) {
      lists[key].forEach((char) => {
        toUse.push(char);
      });
    }
  }
  let pswd = "";
  if (toUse.length != 0) {
    for (let i = 0; i <= length.value; i++) {
      pswd += choose(toUse);
    }
  }
  document.querySelector(".output-container").innerHTML = pswd;
}

function copyGenPswd() {
  var range = document.createRange();
  range.selectNode(document.getElementById("generatedPassword"));
  window.getSelection().removeAllRanges(); // clear current selection
  window.getSelection().addRange(range); // to select text
  document.execCommand("copy");
  window.getSelection().removeAllRanges(); // to deselect
  Swal.fire("Copied", "Copied the password successfully!", "success");
}

// Color
function switchTheme(theme) {
  if (theme === "dark") {
    body.classList.replace("light", "dark");
    localStorage.setItem("theme", "dark");
  } else {
    body.classList.replace("dark", "light");
    localStorage.setItem("theme", "light");
  }
}

// Change main password & username
function changePassword() {
  Swal.mixin({
    input: "password",
    confirmButtonText: "Next &rarr;",
    showCancelButton: true,
    progressSteps: ["1", "2", "3"],
  })
    .queue(["Enter your current password", "Enter your new password", "Repeat your new password"])
    .then((result) => {
      if (result.value) {
        const answers = result.value;
        if (answers[1] === answers[2]) {
          if (answers[0] !== answers[1]) {
            eel.update_pswd_main(new Array(answers[0], answers[2]));
          } else {
            Swal.fire("Useless!", "The new password is the same as the your current one", "warning");
          }
        } else {
          Swal.fire("Oops!", "New passwords aren't the same", "error");
        }
      }
    });
}

eel.expose(successPassword);
function successPassword() {
  Swal.fire("Success!", "Successfully updated your current password", "success");
}

function changeUsername() {
  Swal.mixin({
    input: "text",
    confirmButtonText: "Next &rarr;",
    showCancelButton: true,
    progressSteps: ["1", "2", "3"],
  })
    .queue(["Enter your current username", "Enter your new username", "Enter your password"])
    .then((result) => {
      if (result.value) {
        const answers = result.value;
        if (answers[0] !== answers[1]) {
          eel.update_username_main(new Array(answers[0], answers[1], answers[2]));
        } else {
          Swal.fire("Useless!", "The new username is the same as the your current one", "warning");
        }
      }
    });
}

eel.expose(successUsername);
function successUsername() {
  Swal.fire("Success!", "Successfully updated your current password", "success");
}

// Utils Function
function editSuccess() {
  Swal.fire("Updated!", "Your data has been updated.", "success");
}

function copyToClipboard(text) {
  if (window.clipboardData && window.clipboardData.setData) {
    // IE specific code path to prevent textarea being shown while dialog is visible.
    return clipboardData.setData("Text", text);
  } else if (document.queryCommandSupported && document.queryCommandSupported("copy")) {
    var textarea = document.createElement("textarea");
    textarea.textContent = text;
    textarea.style.position = "fixed"; // Prevent scrolling to bottom of page in MS Edge.
    document.body.appendChild(textarea);
    textarea.select();
    try {
      return document.execCommand("copy"); // Security exception may be thrown by some browsers.
    } catch (ex) {
      console.warn("Copy to clipboard failed.", ex);
      return false;
    } finally {
      document.body.removeChild(textarea);
    }
  }
}

function choose(choices) {
  var index = Math.floor(Math.random() * choices.length);
  return choices[index];
}

async function clearInput(input, inter) {
  let text = input.value;
  let length = text.length;
  for (let i = length; i > 0; i--) {
    text = text.slice(0, -1);
    await sleep(inter).then(() => {
      input.value = text;
    });
  }
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
