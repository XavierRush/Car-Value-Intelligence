// open search box 

let search = document.querySelector(".search-box");

document.querySelector(".search-icon").onclick = () => {
    search.classList.toggle("active")
}

//Menu open close 

let menu = document.querySelector(".menu-icon");
let navLinks = document.querySelector(".nav-link");

menu.onclick = () => {
    menu.classList.toggle("move")
    navLinks.classList.toggle(".menu-open")
}



// on scroll 


// header background on scroll

window.onscroll = () => {
    search.classList.remove("active");
}


// Header background changes on scroll

const header = document.querySelector("header");

window.addEventListener("scroll", () => {
    header.classList.toggle("shadow", window.scrollY > 0);
});




// faqs 
const accordionItem = document.querySelectorAll(".accordion-item"); 

accordionItem.forEach((item) => {
    const accordionHeader = item.querySelector(".accordion-header");

    accordionHeader.addEventListener("click", () => {
        const openItem = document.querySelector(".accordion-open");

        toggleItem(item);

        if (openItem && openItem !== item) {
            toggleItem(openItem);
        }
    })
})

const toggleItem = (item) => {
    const accordionCOntent = item.querySelector(".accordion-content");

    if (item.classList.contains("accordion-open")) {
        accordionCOntent.removeAttribute("style");
        item.classList.remove("accordion-open");
    } else {
        accordionCOntent.style.height = accordionCOntent.scrollHeight + "px";
        item.classList.add("accordion-open");
    }
}


/* Responsive */ 

