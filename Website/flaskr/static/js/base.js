const navLinks = document.querySelector('.nav-links');
const burger = document.querySelector('.hamburger-menu');
const navbar = document.querySelector('.navbar');



// Sticky navbar
window.addEventListener('scroll', () => {
    navbar.classList.toggle('sticky', scrollY > 0)
})