
function show_form(){

    var group_mode = document.getElementById("mode").value

        if(group_mode == "join")
        {
            document.getElementById("join").style.display="block";
            document.getElementById("leave").style.display="none";
            document.getElementById("add").style.display="none";
            document.getElementById("submit").style.display="block";
        }
        else if(group_mode == "leave")
        {
            document.getElementById("join").style.display="none";
            document.getElementById("leave").style.display="block";
            document.getElementById("add").style.display="none";
            document.getElementById("submit").style.display="block";
        }
        else
        {
            document.getElementById("join").style.display="none";
            document.getElementById("leave").style.display="none";
            document.getElementById("add").style.display="block";
            document.getElementById("submit").style.display="block";
        }
}

function show_add_form(){

    var add_group_type = document.getElementById("group_type").value

        if(add_group_type == "club")
        {
            document.getElementById("club").style.display="block";
            document.getElementById("major").style.display="none";
            document.getElementById("residence").style.display="none";
            document.getElementById("class").style.display="none";
            document.getElementById("other").style.display="none";
            document.getElementById("submit2").style.display="block";
        }
        else if(add_group_type == "major")
        {
            document.getElementById("club").style.display="none";
            document.getElementById("major").style.display="block";
            document.getElementById("residence").style.display="none";
            document.getElementById("class").style.display="none";
            document.getElementById("other").style.display="none";
            document.getElementById("submit2").style.display="block";
        }
        else if(add_group_type == "residence")
        {
            document.getElementById("club").style.display="none";
            document.getElementById("major").style.display="none";
            document.getElementById("residence").style.display="block";
            document.getElementById("class").style.display="none";
            document.getElementById("other").style.display="none";
            document.getElementById("submit2").style.display="block";
        }
        else if(add_group_type == "class")
        {
            document.getElementById("club").style.display="none";
            document.getElementById("major").style.display="none";
            document.getElementById("residence").style.display="none";
            document.getElementById("class").style.display="block";
            document.getElementById("other").style.display="none";
            document.getElementById("submit2").style.display="block";
        }
        else
        {
            document.getElementById("club").style.display="none";
            document.getElementById("major").style.display="none";
            document.getElementById("residence").style.display="none";
            document.getElementById("class").style.display="none";
            document.getElementById("other").style.display="block";
            document.getElementById("submit2").style.display="block";
        }
}

function get_date()
{
    /*
    var current_date = new Date();
    var day = current_date.getUTCDate();
    var month = current_date.getUTCMonth()+1;
    var year = current_date.getUTCFullYear();
    if(dd<10)
    {
        day = '0'+ day
    } 
    if(mm<10)
    {
        month = '0' + month
    }
    current_date = year+"-"+month+"-"+day;

    */

    var d = new Date();
    var n = d.toUTCString();

    document.getElementById("date").value = n;

}
    
