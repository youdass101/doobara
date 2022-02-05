var sn;
function snumber(n) {
    sn = n
}

// DOM START HERE 
// When any page on the site load
document.addEventListener('DOMContentLoaded', function(){

    // mobile_menu_btn_nav is Element id
    // Mobile menu button component container 
    var mobile_menu_btn_nav = document.getElementById('mobile-menu-btn');

    // menubtn is Element id
    // mobile nav menu button element    
    var menubtn = document.getElementById('btnm');

    // mobilemenu is Element id
    // secondary navigaton menu container for mobile media
    var mobilemenu = document.getElementById('navigation-mobile');

    // logo_nav is Element id
    // site logo container in the header-nav area
    var logo_nav = document.getElementById('logo-nav');   

    // search_nav is Element id
    // search componenet container in the header-nav area 
    var search_nav = document.getElementById('search-box-nav');

    // menu_nav is Element id
    // Primary meny componenet in the header-nav area 
    var menu_nav = document.getElementById('navigation-menu');

    // cart_nav is Element id
    // cart information component in header-nav area  
    var cart_nav = document.getElementById('cart-nav');
    
    // Set all account page data element display to none
    function account_default() {
        document.getElementById('account-wish-list').classList.toggle('show', false)
        document.getElementById('my-account-dashboard').style.display = 'none';
        document.getElementById('account-detail').classList.toggle('show', false)
        document.getElementById('view-order').classList.toggle("show",false)
    }

    // When account page compnents loaded 
    if (document.getElementById('account-dash')) {

        // When dashboard button is clicked in account page 
        // Show Account current active orders container
        document.getElementById('account-dash').onclick = () => {
            account_default()
            document.getElementById('my-account-dashboard').style.display = 'block'
        }

        // When Orders button clicked in account page 
        // Show account order history container
        document.getElementById('account-orders').onclick = () => {
            account_default()
            document.getElementById('my-account-dashboard').style.display = 'block'
        }

        // When whishlist button clicked in account page 
        // Show account whishlistbutton container
        document.getElementById('account-whishlist').onclick = () => {
            account_default()
            document.getElementById('account-wish-list').classList.toggle('show')
        }

        // When account details button is clicked in account page 
        //show Account edit form contianer 
        document.getElementById('account-edit').onclick = () => {
            account_default()
            document.getElementById('account-detail').classList.toggle('show')
        }
        
        // When view button is clicked in orders and dash container in account page 
        // Show ACCOUNT single ORDER VIEW 
        document.querySelectorAll('.view-order-button').forEach (button => {
            button.onclick = () => {
            account_default()
            document.getElementById('view-order').classList.toggle('show')
            }
        }) 
    }


    // STICKY HEADER
    // sticky is Number
    // Get the offset position of the navbar Assign to var
    var sticky = logo_nav.offsetTop;

    // menubtn -> show mobile menu
    // MOBILE MENU ICON clicked (humberger) 
    //          display hidden menu nav container
    menubtn.onclick = function() {
        mobilemenu.classList.toggle('show');
    }
    
    // anywhere click -> hide mobilemenu
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
        // add sticky-nav class to all header componenets
        if (window.pageYOffset >= sticky) {
        logo_nav.classList.add("sticky-nav");
        search_nav.classList.add("sticky-nav");
        menu_nav.classList.add("sticky-navb");
        cart_nav.classList.add("sticky-navb");
        mobile_menu_btn_nav.classList.add("sticky-nav");
        mobilemenu.classList.add("sticky-navb");
        }
        // remove stick-nav class from all header components
         else {
        logo_nav.classList.remove("sticky-nav");
        search_nav.classList.remove("sticky-nav");
        menu_nav.classList.remove("sticky-navb");
        cart_nav.classList.remove("sticky-navb");
        mobile_menu_btn_nav.classList.remove("sticky-nav");
        mobilemenu.classList.remove("sticky-navb");
        }
    }


    // SLIDER component
    // when index page is loaded (where mySlides class exist)
    if (document.querySelector(".mySlides"))
    {
        // slidIndex is image count
        var slideIndex = 1;
        showSlides(slideIndex);

        // onclick -> integer
        // slider arrown control previews clicked substract 1 from plusSlides
        document.getElementById("prv").onclick = function() {plusSlides(-1)};

        // onclick -> integer
        // slider arrown control next clicked add 1 to plusSlides 
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
        // set slideindex cuurent after calculation 
        function showSlides(n) {
            var i;
            var slides = document.getElementsByClassName("mySlides");
            // n is larger than index length (when next pressed on last index)
            if (n > slides.length) {slideIndex = 1}
            // n is smaller that index length (when previes is press on 1st index)
            if (n < 1) {slideIndex = slides.length}
            // set all element display to none
            for (i = 0; i < slides.length; i++) {
                slides[i].style.display = "none";
            }
            // show targeted index
            slides[slideIndex-1].style.display = "block";
        }
    }

    // PRODUCT SINGLE PAGE SELECT ELEMENT TO CHANGE PRODUCT VARIANT DATA (SO FAR PRICE ONLY CHANGE)
    if (document.getElementById("variants")) {
        obj = document.getElementById("variants")
        obj.onchange = function() {
            val = obj.options[obj.selectedIndex].value
            document.getElementById("spp").innerHTML = val
        }
    }

    // SINGLE PRODUCT IMAGE THUMB CHANGE MAIN IMAGE BY CLICK ON THUMB
    if (document.getElementsByClassName("sp-thumb-image")) {
        document.querySelectorAll('.sp-thumb-image').forEach (image => {
            image.onclick = () => {
                document.getElementById("spi").src = image.src
         

            }
        }) 

    }

    // ADD TO CART BUTTON AT SHOP PAGE 
    // event * component -> 
    if(document.querySelectorAll('.shop-add-to-cart')){
        document.querySelectorAll(".shop-add-to-cart").forEach (button => {
            button.onclick = () => {
                if (document.getElementById('spq')) {
                    qtt = document.getElementById('spq').value
                }
                else {
                    qtt = 1
                }
                
                fetch('/shopaddtocart', {
                    method: 'PUT',
                    body: JSON.stringify({
                        pid : button.value,
                        quantity : qtt
                    }),
                    headers:{
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                
                .then (response => response.json())
                .then (result => {
                    console.log(result)
                    if (result.result=="login"){
                        alert("please login")
                    }
                    else {
                        document.getElementById('carttotal').innerHTML = result.cart.total
                        document.getElementById('cartitemsqtt').innerHTML = result.cart.item
                    }
                })
            }
        })
    }


    // CSRF token function  
    function getCookie(name) {
        if (!document.cookie) {
            return null;
        }
        const token = document.cookie.split(';')
            .map(c => c.trim())
            .filter(c => c.startsWith(name + '='));

        if (token.length === 0) {
            return null;
        }
        return decodeURIComponent(token[0].split('=')[1]);
    }
})



