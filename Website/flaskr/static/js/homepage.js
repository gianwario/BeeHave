const navLinks = document.querySelector('.nav-links');
const burger = document.querySelector('.hamburger-menu');
const navbar = document.querySelector('.navbar');

// Event listeners
burger.addEventListener('click', () => {
    navLinks.classList.toggle('nav-active');
    burger.classList.toggle('bar-change');
})

// Sticky navbar
window.addEventListener('scroll', () => {
    navbar.classList.toggle('sticky', scrollY > 0)
})