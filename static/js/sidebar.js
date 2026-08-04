document.addEventListener("DOMContentLoaded", () => {

    const toggle = document.getElementById("sidebarToggle");
    const sidebar = document.getElementById("sidebar");
    const main = document.getElementById("mainContainer");

    console.log(toggle);
    console.log(sidebar);
    console.log(main);

    if (!toggle || !sidebar || !main) {
        console.error("One or more required elements were not found.");
        return;
    }

    toggle.addEventListener("click", () => {

        sidebar.classList.toggle("hidden");
        main.classList.toggle("expanded");

    });

});