//let colors = ["#24d05a", "#eb4888", "#10a2f5", "#e9bc3f"];
let colors = ["#553c7b", "#32CD32"];

(function () {
  setModeEventListener();
  setRandomLinkColor();
  setColorHoverListener();
  setSexnEventListener();

  setInterval(() => {
    setRandomLinkColor();
  }, 5000);
})();

/* Dark Mode */
function setModeEventListener() {
  let list = document.body.classList;
  document.getElementById("toggler").addEventListener("change", event => {
    event.target.checked ? list.add("dark-mode") : list.remove("dark-mode");
  });
}

/* Colors */

function getRandomColor() {
  return colors[Math.floor(Math.random() * colors.length)];
}

function setRandomLinkColor() {
  Array.from(document.getElementsByTagName("a")).forEach(e => {
    e.style.color = getRandomColor();
  });
}

function setColorHoverListener() {
  Array.from(document.querySelectorAll("a, button")).forEach(e => {
    e.addEventListener("mouseover", setRandomLinkColor);
  });
}

/* Sexn Toggles */

function setSexnEventListener() {
  Array.from(document.getElementsByTagName("button")).forEach(e => {
    e.addEventListener("click", sexnToggle);
  });
}

function sexnToggle(e) {
  let sexnType = e.target;
  let color = getRandomColor();
  off(sexnType);
  sexnType.style.cssText = `border-color: ${color}; color: ${color}; font-weight: bold;`;
  let sexnTypeElement = document.getElementsByClassName(sexnType.id)[0];
  if (sexnTypeElement !== undefined) sexnTypeElement.classList.add("show");
}

function off(sexnType) {
  Array.from(document.getElementsByTagName("button")).forEach(butt => {
    butt.style.borderColor = "#96979c";
    butt.style.color = "#96979c";
  });
  Array.from(document.getElementsByClassName("sexn")).forEach(e => {
    e.classList.remove("show");
  });
}
