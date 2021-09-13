var sn;
function snumber(n) {
    sn = n
}

// DOM START HERE 
document.addEventListener('DOMContentLoaded', function(){

    // Menubtn is Html Element    
    // interp. menubtn is mobile menu button element under id btmn
    var menubtn = document.getElementById('btnm');

    // Mobilemenu is Html ELement
    // interp. mobilemenu is mobile menu links element under id navigation-mobile
    var mobilemenu = document.getElementById('navigation-mobile');

    // Navbar is Html Element 
    // interp. navbar is mobile menu links element under id navbar
    var navbar = document.getElementById('navbar');

    // Sticky is Number
    // Get the offset position of the navbar Assign to var
    // var sticky = navbar.offsetTop;

    // Event -> menubtn
    // MOBILE MENU ICON PRESSED (humberger) 
    //          display hidden menu links div
    menubtn.onclick = function() {
        mobilemenu.classList.toggle('show');

    }
    
    // Event -> mobilemenu
    // ON MOUSE CLICK ON SCREEN HIDE MOBILE MENU DIV
    window.onclick = function(event) {
        if (event.target !== mobilemenu && event.target !== menubtn) {
            mobilemenu.classList.toggle('show', false);
        }   
    }

    // window.onscroll is event function
    // ON MOUSE SCROLL call myfunction function
    window.onscroll = function() {myFunction()};

    // event -> navbar
    // ADD sticky CLASS TO NAVIGATION when scroll of default postion
    // REMOVE sticky CLASS from navigation when heigh position at top default                                
    function myFunction() {
        if (window.pageYOffset >= sticky) {
        navbar.classList.add("sticky-nav");
        } else {
        navbar.classList.remove("sticky-nav");
        }
    }

    if (document.querySelector(".mySlides"))
    {
        // alert(document.querySelector("mySlides"))
        // SLIDER is number 
        // slidIndex is image count
        var slideIndex = 1;
        showSlides(slideIndex);

        //Event -> Function
        // slider arrown control 
        document.getElementById("prv").onclick = function() {plusSlides(-1)};
        document.getElementById("nxt").onclick = function() {plusSlides(1)};

        // Number->Number
        // Slider auto change counter
        setInterval(function(){plusSlides(1) ; }, 5000);  

        // Number -> Number
        // Next/previous controls add n
        function plusSlides(n) {
            showSlides(slideIndex += n);
        }   

        // Number-> slides, SlideIndex(Number)
        // set slideindex cuurent afer calculation 
        function showSlides(n) {
            var i;
            var slides = document.getElementsByClassName("mySlides");
            if (n > slides.length) {slideIndex = 1}
            if (n < 1) {slideIndex = slides.length}
            for (i = 0; i < slides.length; i++) {
                slides[i].style.display = "none";
            }
            slides[slideIndex-1].style.display = "block";
        }
    }
})



