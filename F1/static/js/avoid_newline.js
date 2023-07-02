$(document).ready(function() 
{
    $('#user-data').on('keydown', function(e) 
    {
        // Impedisce di inserire caratteri di ritorno a capo
        if (e.keyCode === 13) 
        {
            e.preventDefault();
            return false;
        }
    });
});