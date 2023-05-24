function navbar_toggle(x) 
{
    x.classList.toggle("change");

    let icons = document.getElementById("navbar-icons"); 

    let userIcon = document.getElementById("user-icon");
    let cartIcon = document.getElementById("cart-icon");
    let utente = document.getElementById("utente");
    let carrello = document.getElementById("carrello");

    if (document.getElementById('toggler').classList.contains('collapsed') && icons.classList.contains("ml-auto")) // Se le icone sono a destra le sposta a sinistra
    {
        console.log('navbar è aperta');
        icons.classList.remove("ml-auto");
        icons.classList.add("mr-auto");

        userIcon.style.visibility = "hidden";
        utente.innerHTML = "Profilo";

        cartIcon.style.visibility = "hidden";
        carrello.innerHTML = "Carrello";
    
    } 
    else if ((!document.getElementById('toggler').classList.contains('collapsed')) && icons.classList.contains("mr-auto"))// Se le icone sono a sinistra le sposta a destra
    {
        console.log('navbar è collassata');

        setTimeout(function() 
        {
            icons.classList.remove("mr-auto");
            icons.classList.add("ml-auto");

        }, 75);

        utente.innerHTML = "";
        carrello.innerHTML = "";

        // <i class="fa fa-fw fa-user" id="user-icon"></i>
        userIcon = document.createElement("i");
        userIcon.classList.add("fa", "fa-fw", "fa-user");
        userIcon.setAttribute("id", "user-icon");
        utente.appendChild(userIcon);

        //<i class="fa fa-fw fa-shopping-cart" id="cart-icon">
        cartIcon = document.createElement("i");
        cartIcon.classList.add("fa", "fa-fw", "fa-shopping-cart");
        cartIcon.setAttribute("id", "cart-icon");
        carrello.appendChild(cartIcon);

    }
}

