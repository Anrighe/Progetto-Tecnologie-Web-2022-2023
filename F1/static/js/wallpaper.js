function adaptWallpaper() 
{
    let wallpaper = document.getElementById('bg');
    wallpaper.style.width = window.innerWidth + 'px';
    wallpaper.style.height = window.innerHeight + 'px';
}

window.onload = function() 
{
    adaptWallpaper();
};
  
window.onresize = function() 
{
    adaptWallpaper();
};