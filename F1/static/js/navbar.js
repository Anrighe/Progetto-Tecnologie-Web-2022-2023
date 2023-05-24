function navbar_toggle(x) 
{
    x.classList.toggle("change");
    
    let icons = document.getElementById("navbar-icons"); 

    if (document.getElementById('toggler').classList.contains('collapsed') && icons.classList.contains("ml-auto")) // Se le icone sono a destra le sposta a sinistra
    {
        console.log('navbar è aperta');
        icons.classList.remove("ml-auto");
        icons.classList.add("mr-auto");
    } 
    else if ((!document.getElementById('toggler').classList.contains('collapsed')) && icons.classList.contains("mr-auto"))// Se le icone sono a sinistra le sposta a destra
    {
        console.log('navbar è collassata');

        setTimeout(function() 
        {
            icons.classList.remove("mr-auto");
            icons.classList.add("ml-auto");

        }, 75);
    }
}

