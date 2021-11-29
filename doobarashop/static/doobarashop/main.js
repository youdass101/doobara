var sn;
function snumber(n) {
    sn = n
}

// DOM START HERE 
// When any page on the site load
document.addEventListener('DOMContentLoaded', function(){

    // mobile nav menu button element    
    var menubtn = document.getElementById('btnm');

    // secondary navigaton menu container for mobile media
    var mobilemenu = document.getElementById('navigation-mobile');

    // site logo container in the header-nav area
    var logo_nav = document.getElementById('logo-nav');   

    // search componenet container in the header-nav area 
    var search_nav = document.getElementById('search-box-nav');

    // Primary meny componenet in the header-nav area 
    var menu_nav = document.getElementById('navigation-menu');

    // cart information component in header-nav area  
    var cart_nav = document.getElementById('cart-nav');

    
    var mobile_menu_btn_nav = document.getElementById('mobile-menu-btn');
    var mobile_nav = document.getElementById('navigation-mobile');

    // Display account to none
    function account_default() {
        document.getElementById('account-wish-list').classList.toggle('show', false)
        document.getElementById('my-account-dashboard').style.display = 'none';
        document.getElementById('account-detail').classList.toggle('show', false)
        document.getElementById('view-order').classList.toggle("show",false)
    }

    // When account page loaded 
    if (document.getElementById('account-dash')) {

        //Account current orders
        document.getElementById('account-dash').onclick = () => {
            account_default()
            document.getElementById('my-account-dashboard').style.display = 'block'
        }

        //account order history
        document.getElementById('account-orders').onclick = () => {
            account_default()
            document.getElementById('my-account-dashboard').style.display = 'block'
        }

        //Navigation menu whishlistbutton
        document.getElementById('account-whishlist').onclick = () => {
            account_default()
            document.getElementById('account-wish-list').classList.toggle('show')
        }

        //Account edit
        document.getElementById('account-edit').onclick = () => {
            account_default()
            document.getElementById('account-detail').classList.toggle('show')
        }
        
        // ACCOUNT single ORDER VIEW 
        document.querySelectorAll('.view-order-button').forEach (button => {
            button.onclick = () => {
            account_default()
            document.getElementById('view-order').classList.toggle('show')
            }
        }) 
    }


    // MENU STICKY 

    // Sticky is Number
    // Get the offset position of the navbar Assign to var
    var sticky = logo_nav.offsetTop;

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
    window.onscroll = function() {sticky_menu_fn()};

    // event -> navbar
    // ADD sticky CLASS TO NAVIGATION when scroll of default postion
    // REMOVE sticky CLASS from navigation when heigh position at top default                                
    function sticky_menu_fn() {
        if (window.pageYOffset >= sticky) {
        logo_nav.classList.add("sticky-nav");
        search_nav.classList.add("sticky-nav");
        menu_nav.classList.add("sticky-navb");
        cart_nav.classList.add("sticky-navb");
        mobile_menu_btn_nav.classList.add("sticky-nav");
        mobile_nav.classList.add("sticky-navb");
        } else {
        logo_nav.classList.remove("sticky-nav");
        search_nav.classList.remove("sticky-nav");
        menu_nav.classList.remove("sticky-navb");
        cart_nav.classList.remove("sticky-navb");
        mobile_menu_btn_nav.classList.remove("sticky-nav");
        mobile_nav.classList.remove("sticky-navb");
        }
    }


    // SLIDER 
    if (document.querySelector(".mySlides"))
    {
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



