function show_groups(data,object){

    console.log(data)

    var university = object.value;

    console.log(university);

    var groups = data[university];

    console.log(groups);

    var select_groups = document.getElementById("group");
    select_groups.innerHTML = "";

    for (var i=0; len=groups.length, i<len; i++) {
        option = document.createElement("option");
        option.value = groups[i];
        option.text = groups[i];
        select_groups.appendChild(option);
    } 

}
