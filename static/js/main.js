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

// ---------- Header shadow + hide-on-scroll ----------
const header = document.querySelector(".site-header");
if (header) {
    let lastScrollY = window.scrollY;

    const applyHeaderState = () => {
        const currentY = window.scrollY;
        header.classList.toggle("shadow", currentY > 4);

        const menuOpen = navLinks && navLinks.classList.contains("menu-open");
        if (menuOpen) {
            header.classList.remove("nav-hidden");
        } else if (currentY > lastScrollY && currentY > 120) {
            header.classList.add("nav-hidden");
        } else {
            header.classList.remove("nav-hidden");
        }

        lastScrollY = currentY;
    };

    applyHeaderState();
    window.addEventListener("scroll", applyHeaderState);
}

// ---------- Login / signup modal ----------
const authOverlay = document.getElementById("authOverlay");
const authModalClose = document.getElementById("authModalClose");
const loginPanel = document.getElementById("loginPanel");
const signupPanel = document.getElementById("signupPanel");

function showAuthPanel(name) {
    if (!loginPanel || !signupPanel) return;
    loginPanel.hidden = name !== "login";
    signupPanel.hidden = name !== "signup";
}

function openAuthModal(panel) {
    if (!authOverlay) return;
    showAuthPanel(panel);
    authOverlay.classList.add("active");
    document.body.classList.add("modal-open");
}

function closeAuthModal() {
    if (!authOverlay) return;
    authOverlay.classList.remove("active");
    document.body.classList.remove("modal-open");
}

document.querySelectorAll(".js-open-auth").forEach((btn) => {
    btn.addEventListener("click", (e) => {
        e.preventDefault();
        openAuthModal(btn.dataset.panel || "login");
    });
});

if (authModalClose) authModalClose.addEventListener("click", closeAuthModal);

if (authOverlay) {
    authOverlay.addEventListener("click", (e) => {
        if (e.target === authOverlay) closeAuthModal();
    });
}

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeAuthModal();
});

document.querySelectorAll(".switch-to-signup").forEach((link) => {
    link.addEventListener("click", (e) => {
        e.preventDefault();
        showAuthPanel("signup");
    });
});

document.querySelectorAll(".switch-to-login").forEach((link) => {
    link.addEventListener("click", (e) => {
        e.preventDefault();
        showAuthPanel("login");
    });
});

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