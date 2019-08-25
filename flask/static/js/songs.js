function show_form(){

    var song_mode = document.getElementById("mode").value

        if(song_mode == "vote")
        {
            document.getElementById("vote").style.display="block";
            document.getElementById("play").style.display="none";
            document.getElementById("add").style.display="none";
            document.getElementById("submit").style.display="block";
        }
        else if(song_mode == "play")
        {
            document.getElementById("vote").style.display="none";
            document.getElementById("play").style.display="block";
            document.getElementById("add").style.display="none";
            document.getElementById("submit").style.display="block";
        }
        else
        {
            document.getElementById("vote").style.display="none";
            document.getElementById("play").style.display="none";
            document.getElementById("add").style.display="block";
            document.getElementById("submit").style.display="block";
        }
}


function get_date(){
    var d = new Date();
    var n = d.toUTCString();

    document.getElementById("date").value = n;
}
    
