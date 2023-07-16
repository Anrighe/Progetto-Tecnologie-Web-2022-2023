// Apre il modal per caricare un'immagine profilo
function openModal() 
{
    let modal = document.getElementById("modal-profile-image");
    modal.style.display = "block";
}

// Chiude il modal per caricare un'immagine profilo
function closeModal() 
{
    let modal = document.getElementById("modal-profile-image");
    modal.style.display = "none";
}

// Add a click event listener to the image
let profileImage = document.getElementById("profile-image");
profileImage.addEventListener("click", openModal);