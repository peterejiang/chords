function show_data(data,object){

    var table1 = document.getElementById("top_songs_table");
    var table2 = document.getElementById("recent_votes_table");
    
    if (table1 != null)
    {
        table1.remove();
    }
    if (table2 != null)
    {
        table2.remove();
    }
    
    for (var i = 1; i<7; i++){
        var n = i.toString();
        var br = document.getElementById(n);
        if (br != null)
        {
            br.remove();
        }
    }


    var group = object.value;

    var top_songs = data[group]["top_songs"];
    var recent_votes = data[group]["recent_votes"];

    var top_songs_table = document.createElement('table');
    
    top_songs_table.id = "top_songs_table";

    var top_songs_caption = document.createElement('caption');
    var text_caption = document.createTextNode('Top Songs');
    top_songs_caption.appendChild(text_caption);
    top_songs_table.appendChild(top_songs_caption); 

    var tr = document.createElement('tr');
   
    var th1 = document.createElement('th');
    var text1 = document.createTextNode('Ranking');
    th1.appendChild(text1);    
        
    var th2 = document.createElement('th');
    var text2 = document.createTextNode('Song Name');
    th2.appendChild(text2);
    
    var th3 = document.createElement('th');
    var text3 = document.createTextNode('Artist');
    th3.appendChild(text3);   
    
    var th4 = document.createElement('th');
    var text4 = document.createTextNode('Year');
    th4.appendChild(text4);   
    
    var th5 = document.createElement('th');
    var text5 = document.createTextNode('Score');
    th5.appendChild(text5);   
    
    tr.appendChild(th1);
    tr.appendChild(th2);
    tr.appendChild(th3);
    tr.appendChild(th4);
    tr.appendChild(th5);
    
    top_songs_table.appendChild(tr);

    for (var i = 0; len=top_songs.length, i<len; i++){
        var tr = document.createElement('tr');   

        var ranking = i + 1;
        var ranking_string = ranking.toString();
       
        var td1 = document.createElement('td');
        var text1 = document.createTextNode(ranking_string);
        td1.appendChild(text1);    
            
        var td2 = document.createElement('td');
        var text2 = document.createTextNode(top_songs[i][0]);
        td2.appendChild(text2);
        
        var td3 = document.createElement('td');
        var text3 = document.createTextNode(top_songs[i][1]);
        td3.appendChild(text3);   
        
        var td4 = document.createElement('td');
        var text4 = document.createTextNode(top_songs[i][2]);
        td4.appendChild(text4);   
        
        var td5 = document.createElement('td');
        var text5 = document.createTextNode(top_songs[i][3]);
        td5.appendChild(text5);   
        
        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        tr.appendChild(td4);
        tr.appendChild(td5);
        
        top_songs_table.appendChild(tr);
    }

    document.body.appendChild(top_songs_table);

    br1 = document.createElement("br");
    br1.id = "1";
    document.body.appendChild(br1);

    br2 = document.createElement("br");
    br2.id = "2";
    document.body.appendChild(br2);

    br3 = document.createElement("br");
    br3.id = "3";
    document.body.appendChild(br3);


    var recent_votes_table = document.createElement('table');
    
    recent_votes_table.id = "recent_votes_table";

    var recent_votes_caption = document.createElement('caption');
    var text_caption = document.createTextNode('Recent Votes');
    recent_votes_caption.appendChild(text_caption);
    recent_votes_table.appendChild(recent_votes_caption);

    var tr = document.createElement('tr');
   
    var th1 = document.createElement('th');
    var text1 = document.createTextNode('Song Name');
    th1.appendChild(text1);    
        
    var th2 = document.createElement('th');
    var text2 = document.createTextNode('Artist');
    th2.appendChild(text2);
    
    var th3 = document.createElement('th');
    var text3 = document.createTextNode('Vote Time');
    th3.appendChild(text3);   
    
    var th4 = document.createElement('th');
    var text4 = document.createTextNode('Vote Score');
    th4.appendChild(text4);   
    
    tr.appendChild(th1);
    tr.appendChild(th2);
    tr.appendChild(th3);
    tr.appendChild(th4);
    
    recent_votes_table.appendChild(tr);

    for (var i = 0; len=recent_votes.length, i<len; i++){
        var tr = document.createElement('tr');   
       
        var td1 = document.createElement('td');
        var text1 = document.createTextNode(recent_votes[i][0]);
        td1.appendChild(text1);    
            
        var td2 = document.createElement('td');
        var text2 = document.createTextNode(recent_votes[i][1]);
        td2.appendChild(text2);
        
        var td3 = document.createElement('td');
        var text3 = document.createTextNode(recent_votes[i][2]);
        td3.appendChild(text3);   
        
        var td4 = document.createElement('td');
        var text4 = document.createTextNode(recent_votes[i][3]);
        td4.appendChild(text4);   
        
        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        tr.appendChild(td4);
        
        recent_votes_table.appendChild(tr);
    }

    document.body.appendChild(recent_votes_table);

    br4 = document.createElement("br");
    br4.id = "4";
    document.body.appendChild(br4);

    br5 = document.createElement("br");
    br5.id = "5";
    document.body.appendChild(br5);

    br6 = document.createElement("br");
    br6.id = "6";
    document.body.appendChild(br6);



}
