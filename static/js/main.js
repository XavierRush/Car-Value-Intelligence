// ---------- Search box ----------
const searchIcon = document.querySelector(".search-icon");
const search = document.querySelector(".search-box");
if (searchIcon && search) {
    searchIcon.addEventListener("click", () => search.classList.toggle("active"));
    window.addEventListener("scroll", () => search.classList.remove("active"));
}

// ---------- Mobile menu ----------
const menu = document.querySelector(".menu-icon");
const navLinks = document.querySelector(".nav-links");
if (menu && navLinks) {
    menu.addEventListener("click", () => {
        menu.classList.toggle("move");
        navLinks.classList.toggle("menu-open");
    });
}

// ---------- Header shadow on scroll ----------
const header = document.querySelector(".site-header");
if (header) {
    const applyShadow = () => header.classList.toggle("shadow", window.scrollY > 4);
    applyShadow();
    window.addEventListener("scroll", applyShadow);
}

// ---------- FAQ / accordion ----------
document.querySelectorAll(".accordion-item").forEach((item) => {
    const trigger = item.querySelector(".accordion-header");
    const content = item.querySelector(".accordion-content");
    if (!trigger || !content) return;

    trigger.addEventListener("click", () => {
        document.querySelectorAll(".accordion-item").forEach((other) => {
            if (other !== item) {
                other.classList.remove("accordion-open");
                other.querySelector(".accordion-content").removeAttribute("style");
            }
        });

        if (item.classList.contains("accordion-open")) {
            content.removeAttribute("style");
            item.classList.remove("accordion-open");
        } else {
            content.style.height = content.scrollHeight + "px";
            item.classList.add("accordion-open");
        }
    });
});
