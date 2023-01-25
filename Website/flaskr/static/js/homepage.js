window.onload = () => {
    var navbar = document.getElementById("navbar");
    var page = document.title;
    if (page == "Home"){
        window.onscroll = function() {stick()};
    } else {
        navbar.className ="navbar navbar-expand-sm bg-dark";
    }
}

function stick() {
    var navbar = document.getElementById("navbar");
    var sticky = 180;
    if (window.pageYOffset >= sticky) {
        navbar.className ="navbar navbar-expand-sm bg-dark";
    } else {
        navbar.className ="navbar navbar-expand-sm ";
    }
}