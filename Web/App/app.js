// INIT
let theme = localStorage.getItem("theme");
const body = document.querySelector("body");

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

retrievePassword([
  ["Edgar", "Google"],
  ["Edgar", "Discord"],
  ["Edgar", "Ecole Directe"],
  ["Edgar", "Youtube"],
]);

retrieveNotes([
  ["My Note", "Lorem ipsum dolor sit amet consectetur adipisicing elit. Eos libero accusamus, est ipsam excepturi cum reprehenderit? Optio culpa minima est. Officia fugit quis laborum quisquam repellendus magni unde, perferendis recusandae!"],
  ["Whoa", "Lorem ipsum dolor sit amet consectetur adipisicing elit. Eos libero accusamus, est ipsam excepturi cum reprehenderit? Optio culpa minima est. Officia fugit quis laborum quisquam repellendus magni unde, perferendis recusandae!"],
  ["Lorem", "Lorem ipsum dolor sit amet consectetur adipisicing elit. Eos libero accusamus, est ipsam excepturi cum reprehenderit? Optio culpa minima est. Officia fugit quis laborum quisquam repellendus magni unde, perferendis recusandae!"],
  ["Ipsum", "Lorem ipsum dolor sit amet consectetur adipisicing elit. Eos libero accusamus, est ipsam excepturi cum reprehenderit? Optio culpa minima est. Officia fugit quis laborum quisquam repellendus magni unde, perferendis recusandae!"],
]);

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
    if (sectionId === "health") {
      placeHealthSpan();
    } else {
      hideHealthSpan();
    }
  }
}

function placeHealthSpan() {
  let healthScore = 43;
  let span = document.querySelector(".health-nb");
  let shieldSvg = document.getElementById("shield");
  let front = shieldSvg.querySelector("#front")
  let dashoffset = front.getTotalLength()
  let curDash = healthScore/100*dashoffset

  console.log(dashoffset, curDash);
  
  front.style.strokeDasharray = `${curDash}px`
  span.innerHTML = healthScore;
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

function retrievePassword(data) {
  let userInfos = data;
  userInfos.forEach((infos) => {
    addPasswordField(infos[0], infos[1]);
  });
}

function retrieveNotes(data) {
  let userInfos = data;
  userInfos.forEach((infos) => {
    addNoteField(infos[0], infos[1]);
  });
}

function addPasswordField(username, website) {
  nbPaswds++;
  let container = `
  <div class="dropdown-wrapper smooth-height" id="pswd${nbPaswds}">
    <div class="dropdown__top">
      <h1 class="dropdown__domain">${website}</h1>
      <div class="arrow" onclick="showDetails(${nbPaswds}, 'pswd');">
        <div class="arrow-pt1"></div>
        <div class="arrow-pt2"></div>
      </div>
    </div>
    <div class="dropdown__bottom closed">
      <h1 class="username">${username}</h1>
      <button class="dropdown">Click to copy</button>
      <div class="bin">
        <svg onclick="deleteDropdown(${nbPaswds}, 'pswd');" viewBox="0 0 20.19 24.849">
          <path
            d="M6.052,9.693v15.53A1.558,1.558,0,0,0,7.6,26.777H21.582a1.558,1.558,0,0,0,1.553-1.553V9.693Zm4.659,13.977H9.158V12.8h1.553Zm3.106,0H12.264V12.8h1.553Zm3.106,0H15.37V12.8h1.553Zm3.106,0H18.476V12.8h1.553ZM23.523,5.034H18.476V3.093a1.168,1.168,0,0,0-1.165-1.165H11.876a1.168,1.168,0,0,0-1.165,1.165V5.034H5.664A1.168,1.168,0,0,0,4.5,6.2V8.14H24.688V6.2a1.168,1.168,0,0,0-1.165-1.165Zm-6.6,0H12.264V3.5h4.659V5.034Z"
            transform="translate(-4.499 -1.928)"
          />
        </svg>
      </div>
    </div>
  </div>`;
  document.querySelector(".password-container").innerHTML += container;
  showEmptySvg();
}

function addNoteField(title, content) {
  nbNotes++;
  let container = `
  <div class="dropdown-wrapper smooth-height" id="note${nbNotes}">
    <div class="dropdown__top">
      <h1 class="dropdown__title">${title}</h1>
      <div class="bin">
        <svg onclick="deleteDropdown(${nbNotes}, 'note');" viewBox="0 0 20.19 24.849">
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

function addPasswordBtn() {
  let data = document.querySelectorAll(".add-container input");
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
  if (usernames.includes(data[0].value) && websites.includes(data[2].value)) {
    Swal.fire("Error", "This username is already registered for this website", "error", {
      iconHtml: "../IMG/Logo.png",
    });
  } else {
    addPasswordField(data[0].value, data[2].value);
  }
}

function addNoteBtn() {
  let data = document.querySelectorAll(".add-note input");
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
  if (titles.includes(data[0].value)) {
    Swal.fire("Error", "This title is already used for another note", "error");
  } else if (contents.includes(data[1].value)) {
    Swal.fire("Error", "You have already wrote this in another note", "error");
  } else {
    addNoteField(data[0].value, data[1].value);
  }
}

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
      // if (model == "pswd") {
      //   nbPaswds--;
      // } else {
      //   nbNotes--;
      // }
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

// Utils Function
function choose(choices) {
  var index = Math.floor(Math.random() * choices.length);
  return choices[index];
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
