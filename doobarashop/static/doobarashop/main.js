document.addEventListener('DOMContentLoaded', function(){

    var menubtn = document.getElementById('btnm');
    var mobilemenu = document.getElementById('navigation-mobile');

    // When the user clicks on the button, open the modal
    menubtn.onclick = function() {
        mobilemenu.classList.toggle('show');
    }

    // menubtn.onclick = function() {
    //     if (mobilemenu.style.display == 'block') {
    //         mobilemenu.style.display = "none";
    //     }
    //     else {
    //         mobilemenu.style.display = 'block';
    //     }
        
    // }

    
    // // When the user clicks anywhere outside of the modal, close it
    // window.onclick = function(event) {
    //     if (event.target !== mobilemenu && event.target !== menubtn ) {
    //         mobilemenu.style.display = "none";
    //     }
    // }
})