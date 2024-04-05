// var frame = document.querySelector(".iframe");

window.onload = (e) => {
    var frame = document.querySelector(".iframe");
    header = frame.contentDocument.querySelector(".navbar.navbar-light.navbar-expand-lg");
    header.remove();
    footer = frame.contentDocument.querySelector(".web-footer");
    footer.remove();
}