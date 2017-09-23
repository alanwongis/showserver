var curr_action = 1;


var playlist;
var songlist;



/* ------------*/
/* UI handlers */
/* ------------*/


/* player message area */
/* ------------------- */

var show_message = function(song, state) {
    $("#message").html("<strong>" + song + " " + state + "</strong>");
};


/* tracklist (songs queued for play) */

var play_track = function(num) {
    console.log("play song" + num);
    console.log($("#track-"+num).text());
    $.ajax({
        url: "/play_track/"+num,
        success: function(result) {
            console.log(result);
        }
    });
};
 
 
var refresh_tracklist = function() {
    $.ajax({
        url: "/get_playlist",
        success: function(result) {
            console.log("success");
            var tracklist = $("#tracklist");
            var songs = result["songs"];
            console.log(songs);
            tracklist.empty() /* delete exisitng children */
            for(var i=0; i<songs.length; i++) {
                var track_title = songs[i];
                    tracklist.append('<li><a href="#" class="tracklist-play-button" onclick="play_track(' + i +' , this);"><div class="track-number">' + (i+1) + '</div></a><div class="tracklist-title" id="track-'+ i +'">' + track_title + '</div></li>');
            }
        }
    });
 }; 
 
 
 
/* edit playlist */
/* ------------- */



var get_playlist= function() {
    $.ajax({
        url: "/get_playlist", 
        success: function(result) {

            var playlist = $("#playlist");
            playlist.empty(); /* delete existing children */
            var title = result["title"];
            var songs = result["songs"];
            console.log(songs);
            $("#playlist_title").html(title);
            for(var i=0; i<songs.length; i++) {
                var song = songs[i];
                playlist.append('<li> <span class="playlist_song">' + song + '</span>' +
                    '<span class="playlist_remove"><a href="#" onclick="remove_playlist_item(this);">Remove</a><span></li>');           
            }
            playlist.listview("refresh");
            console.log(result);
        }
     
     });   
};


var save_playlist = function() {
    var playlist = $("#playlist li");
    var items = [];
    for(var i=0; i<playlist.length; i++) {
        //console.log($(playlist[i]).find(".playlist_song").text());
        items.push($(playlist[i]).find(".playlist_song").text());
    }
    console.log(items);
    $.ajax({
        url: "/update_playlist",
        contentType: "application/json",
        data: JSON.stringify(items),
        type: "POST",    
        success: function(results) {
            $("#playlist-save-btn").text("Saved");
            console.log("saved playlist");
            console.log(results);
        }
    });
};
  

var append_playlist = function(song) {
    var playlist = $("#playlist");
    playlist.append('<li> <span class="playlist_song">' + songlist[song] + '</span>' +
                    '<span class="playlist_remove"><a href="#" onclick="remove_playlist_item(this);">Remove</a><span></li>');
    playlist.listview("refresh");
};

var remove_playlist_item = function(item) {
    $(item).parent().parent().remove();
};



/*songlist*/
/*--------*/


var add_song = function(song_num) {
    console.log("add song " + song_num);
};



var update_songlist = function(ev) {
   $.ajax({
    url: "/get_songlist",
    success: function(result) {
        songlist = result;
        var ul = $("#songlist");
        ul.empty();
        for(var i=0; i<songlist.length; i++) {
            ul.append('<li>'+ songlist[i] +' <span style="float: right;"><a href="#" onclick="append_playlist('+i+');")>Add</a></span>');     
        }
        ul.listview("refresh");
      }
    });
 };





/* player buttons */

var play_action = function() {
    $.ajax({
       url: "/play",
       success: function(result) {
            show_message(result, "playing");
            console.log(result);
       }
    });
};


var stop_action = function() {
    $.ajax({
       url: "/stop",
       success: function(result) {
            show_message(result, "stopped");
            console.log(result);
       }
    });
};


var next_action = function() {
    $.ajax({
       url: "/next",
       success: function(result) {
            show_message(result, "next");
            console.log(result);
       }
    });
};  


var prev_action = function() {
    $.ajax({
       url: "/prev",
       success: function(result) {
            show_message(result, "prev");
            console.log(result);
       }
    });
};


var panic_action = function() {
    $.ajax({
       url: "/panic",
       success: function(result) {
            show_message(result, "emergency stop");
            console.log(result);
       }
    });
};

/* playlist panel */

var change_playlist = function(num) {
    var name = $($("#playlist_chooser").children()[num]).text();
    console.log(name);
    return;
    $.ajax({
        url: "/select_playlist",
        contentType: "application/json",
        data: JSON.jsonify(name),
        success: function(result) {
            refresh_tracklist();
        }
    });
};


/* song manager page */

var refresh_song_manager_list = function() {
   $.ajax({
    url: "/get_songlist",
    success: function(result) {
        console.log(result);
        songlist = result;
        var ul = $("#song_manager_list");
        ul.empty();
        for(var i=0; i<songlist.length; i++) {
            ul.append('<li>'+ songlist[i] +' <span style="float: right;"><a href="#" onclick="append_playlist('+i+');")>Add</a></span>');     
        }
        ul.listview("refresh");
     }
  });
};



/* app init */


$("#one").on("pagebeforeshow", function() {
      refresh_tracklist();
   }
);

$("#playlist_settings").on("pagebeforeshow", function() {
    get_playlist();
    $("#playlist").sortable();
    $("#playlist").disableSelection();
   update_songlist();
   /*reset save button*/
   $("#save-playlist-btn").text("Click to Save");
 }
);

$("#song-manager").on("pagebeforeshow", function() {
    refresh_song_manager_list();
  }
);

$("#upload-form").on("submit", function(ev) {
        ev.preventDefault();
        var files = document.getElementById("song-upload").files;
        var data = new FormData();
        $.each(files, function(key, value) {
            data.append(key, data);
        });
        console.log(data);
        $.ajax({
            url: "/upload_song",
            type: "POST",
            data: data,
            cache: false,
            dataType: "json",
            processData: false,
            contentType: false,
            success: function(data, textStatus, jqXHDR) {
                if(typeof data.error === 'undefined') {
                    submitForm(event, data);
                } else {
                    console.log("Errors: "+ data.error);
                }
            },
            error: function(jqxHdr, textStatus, ErrorThrown) {
                console.log("Errors: " + textStatus);
            }
         });
    }
 );
 
                
            
    }
);

