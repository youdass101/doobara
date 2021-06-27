document.addEventListener('DOMContentLoaded', function(){

    var menubtn = document.getElementById('humberger');
    var mobilemenu = document.getElementById('navigation-mobile');

    // When the user clicks on the button, open the modal
    menubtn.onclick = function() {
        if (mobilemenu.style.display == 'block') {
            mobilemenu.style.display = "none";
        }
        else {
            mobilemenu.style.display = 'block';
        }
        
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == mobilemenu) {
            alert("asd")
            mobilemenu.style.display = "none";
        }
    }
})