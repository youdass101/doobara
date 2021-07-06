document.addEventListener('DOMContentLoaded', function(){

    // Mobile humberger button for menu
    var menubtn = document.getElementById('btnm');
    // Mobile navigation menu
    var mobilemenu = document.getElementById('navigation-mobile');
    // Navigation bar 
    var navbar = document.getElementById('navbar');
    // Get the offset position of the navbar
    var sticky = navbar.offsetTop;

    // When the user clicks on the button, open the mobile navigation menu
    menubtn.onclick = function() {
        mobilemenu.classList.toggle('show');
    }

    // When the user clicks anywhere outside of the mobile navigation
    window.onclick = function(event) {
        if (event.target !== mobilemenu && event.target !== menubtn) {
            mobilemenu.classList.toggle('show', false);
        }   
    }

    window.onscroll = function() {myFunction()};
    // Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
    function myFunction() {
        if (window.pageYOffset >= sticky) {
        navbar.classList.add("sticky");
        } else {
        navbar.classList.remove("sticky");
        }
    }

    // SLIDER ON INDEX PAGE 
    var slideIndex = 1;
    showSlides(slideIndex);

    // Next/previous controls
    function plusSlides(n) {
        showSlides(slideIndex += n);
    }

    // Thumbnail image controls
    function currentSlide(n) {
        showSlides(slideIndex = n);
    }

    function showSlides(n) {
        var i;
        var slides = document.getElementsByClassName("mySlides");
        var dots = document.getElementsByClassName("dot");
        if (n > slides.length) {slideIndex = 1}
        if (n < 1) {slideIndex = slides.length}
        for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
        }
        for (i = 0; i < dots.length; i++) {
            dots[i].className = dots[i].className.replace(" active", "");
        }
        slides[slideIndex-1].style.display = "block";
        dots[slideIndex-1].className += " active";
    }
   
    
})

