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
        navbar.classList.add("sticky")
        } else {
        navbar.classList.remove("sticky");
        }
    }
        // window.onscroll = function() {
    //     if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
    //         navbar.classList.toggle('stickyNav', true);
    //       } else {
    //         navbar.classList.toggle('stickyNav', false);
    //       }

    // }
})