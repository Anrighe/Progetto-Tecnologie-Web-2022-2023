function navbar_toggle(x) 
{
    x.classList.toggle("change");
}

document.addEventListener("DOMContentLoaded", function() {
    const dropdownButton = document.getElementById("profileDropdown");
    const dropdownMenuDiv = document.getElementById("notification-div");

    dropdownButton.addEventListener("click", function(event) 
    {
        fetch('/query/notifications/')
            .then(response => response.json())
            .then(data => {
                
                dropdownMenuDiv.innerHTML = "";

                // Se la risposta è vuota mostro un messaggio per segnalare che non ci sono notifiche
                if (data.length == 0) 
                {
                    let emptyMessage = document.createElement("a");
                    emptyMessage.innerHTML = "Nessuna notifica";
                    emptyMessage.classList.add("dropdown-item");
                    dropdownMenuDiv.appendChild(emptyMessage);
                    return;
                }

                // Altrimenti mostra le notifiche
                for (let i = 0; i < data.length; i++) 
                {
                    let a = document.createElement("a");
                    a.setAttribute("href", "/profile/");
                    a.innerHTML = data[i].descrizione;
                    a.classList.add("dropdown-item");
                    dropdownMenuDiv.appendChild(a);
                }

            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });     
    });
    
});