document.addEventListener("scroll", function () {
    const navbar = document.querySelector(".fixed-navbar");
    if (window.scrollY > 50) {
        navbar.classList.add("scrolled");
    } else {
        navbar.classList.remove("scrolled");
    }
});
