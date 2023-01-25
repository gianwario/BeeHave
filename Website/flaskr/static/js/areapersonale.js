function openMulti() {
  if (document.querySelector(".selectWrapper").style.pointerEvents == "all") {
    document.querySelector(".selectWrapper").style.opacity = 0;
    document.querySelector(".selectWrapper").style.pointerEvents = "none";
    resetAllMenus();
  } else {
    document.querySelector(".selectWrapper").style.opacity = 1;
    document.querySelector(".selectWrapper").style.pointerEvents = "all";
  }
}
function nextMenu(e) {
  menuIndex = eval(event.target.parentNode.id.slice(-1));
  document.querySelectorAll(".multiSelect")[menuIndex].style.transform =
    "translateX(-100%)";
  // document.querySelectorAll(".multiSelect")[menuIndex].style.clipPath = "polygon(0 0, 0 0, 0 100%, 0% 100%)";
  document.querySelectorAll(".multiSelect")[menuIndex].style.clipPath =
    "polygon(100% 0, 100% 0, 100% 100%, 100% 100%)";
  document.querySelectorAll(".multiSelect")[menuIndex + 1].style.transform =
    "translateX(0)";
  document.querySelectorAll(".multiSelect")[menuIndex + 1].style.clipPath =
    "polygon(0 0, 100% 0, 100% 100%, 0% 100%)";
}
function prevMenu(e) {
  menuIndex = eval(event.target.parentNode.id.slice(-1));
  document.querySelectorAll(".multiSelect")[menuIndex].style.transform =
    "translateX(100%)";
  document.querySelectorAll(".multiSelect")[menuIndex].style.clipPath =
    "polygon(0 0, 0 0, 0 100%, 0% 100%)";
  document.querySelectorAll(".multiSelect")[menuIndex - 1].style.transform =
    "translateX(0)";
  document.querySelectorAll(".multiSelect")[menuIndex - 1].style.clipPath =
    "polygon(0 0, 100% 0, 100% 100%, 0% 100%)";
}
function resetAllMenus() {
  setTimeout(function () {
    var x = document.getElementsByClassName("multiSelect");
    var i;
    for (i = 1; i < x.length; i++) {
      x[i].style.transform = "translateX(100%)";
      x[i].style.clipPath = "polygon(0 0, 0 0, 0 100%, 0% 100%)";
    }
    document.querySelectorAll(".multiSelect")[0].style.transform =
      "translateX(0)";
    document.querySelectorAll(".multiSelect")[0].style.clipPath =
      "polygon(0 0, 100% 0, 100% 100%, 0% 100%)";
  }, 300);
}

