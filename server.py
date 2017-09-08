from __future__ import division, print_function
import cherrypy

import glob
import json
import os
import pickle
import shutil
import subprocess



# directories
#-------------

#curr_dir = "/home/pi/Desktop/showserver"
curr_dir = os.path.split(os.path.abspath(__file__))[0]
music_dir = os.path.join(curr_dir, "music")
playlist_dir = os.path.join(curr_dir, "playlists")



# error message handler
#-----------------------

def error_page_default(status, message, trackback, version):
    ret = {
        'status': status,
        'version': version,
        'message': [message],
        'traceback': traceback }
    return json.dumps(ret)


# settings
#----------

settings = {}

def update_settings():
    pickle.dump(settings, open("settings.pk1", "wb"), protocol=2)


def initialize_settings():
    global settings
    playlists = {"default": ["01 Common People.m4a",
                             "02 Mediational Field.m4a"] }
    pickle.dump(playlists, open("playlists.pkl", "wb"), protocol = 2)
    settings = {"last_playlist": "default"}
    pickle.dump(settings, open("settings.pkl", "wb"), protocol= 2)
    

try:
    settings = pickle.load(open("settings.pkl", "rb"))
except:
    initialize_settings()

      
# all music files 
#-------------
    
def list_music():
    filenames  = os.listdir(music_dir)
    return filenames
    

def save_music(file_name, data):
    return

   
# playlists
#----------

class PlaylistManager(object):

    def __init__(self):
        try:
            self.playlists  = pickle.load(open("playlists.pkl", "rb"))
        except:
            self.playlists = { "default": []}
        self.curr_playlist_name = "default"


    def list_all(self):
        """returns all the playlist names"""
        return self.playlists.keys()

    def select_playlist(self, name):
        self.curr_playlist_name = name

    def get_songs(self):
        return [self.curr_playlist_name,
                self.playlists[self.curr_playlist_name] ]

    def new_playlist(self):
        # creates a new empty playlist
        if not "new playlist" in self.playlists.keys():
            playlist_name = "new playlist"
        else:
            n = 1
            while "new playist "+str(n) in self.playlists.keys():
                n += 1
            playlist_name = "new playlist "+str(n)
        self.update_playlist(playlist_name, [])
        return playlist_name


    def rename_playlist(self, old_name, new_name):
        if not new_name in self.playlists.keys():
            self.playlists[new_name] = self.playlists[old_name]
            self.playlists.pop(old_name)
            return True
        else:
            return False # can't rename  because name already exists
            
            
    def update_playlist(self, name, songs):
        self.playlists[name] = songs
        pickle.dump(self.playlists, open("playlists.pkl", "wb"), protocol = 2)

     
playlists = PlaylistManager()
playlists.select_playlist(settings["last_playlist"])




#  music playback interface
#---------------------------

class DummyMusicPlayer(object):

    def __init__(self, playlist=None):
        self.playlist = playlist
        if self.playlist:
            self.curr_song = 0
            self.curr_song_name = self.playlist[0]
        else:
            self.curr_song = -1
            self.curr_song_name = "None"
        self.status = "stopped"
       
    def play(self):
        return self.get_status()
    
    def next(self):
        song_number = 1
        song_name = "next dummmy song"
        status = "playing"
        return self.get_status()
    
    
    def prev(self):
        song_number = 1
        song_name = "prev dummy song"
        status = "playing"
        return self.get_status()
  
  
    def stop(self):
        song_number = 1
        song_name = "prev dummy song"
        status = "playing"
        return self.get_status()
  
    def change_song(self, song_num = 1):
        return self.get_status()
      
    def get_status(self):
        return {"song_title_": "a songe", "track_num": 1,  "status": "playing", "time": 0, "length": 100}
       
       
music_player = DummyMusicPlayer() 
  

  
# web interface   
#---------------
    
class Root(object):
    
    _cp_config = {'error_page_default': error_page_default }

    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("/static/index.html")

    # player API
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def play(self):
        return music_player.play()
        
    @cherrypy.expose 
    @cherrypy.tools.json_out()    
    def next(self):
        return music_player.next()
        
    @cherrypy.expose 
    @cherrypy.tools.json_out()    
    def prev(self):
        return music_player.prev()
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def stop(self):
        return music_player.stop()
       
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def status(self):
        status_msg = { "song": "dummy song name",
                       "track_num": 1,
                       "track_lenght": 60,
                       "curr_time": 1, 
                       "state": "paused" }     
        return status_msg
        
    # songlist API
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_songlist(self):
        return list_music()
    
    @cherrypy.expose
    def delete_song(self, filename):
        # TODO...
        return
        
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def upload_song(self,songfile=None):
        filename = os.path.join(music_dir, songfile.filename)
        data = ""
        while True:
            chunk = songfile.file.read(8192)
            if not chunk:
                break
            else:
                data += chunk
        size = len(data)
        f = open(filename, "wb")
        f.write(data)
        f.close()
        return str( (filename, size) )
        
    # playlist API
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def list_all(self):
        return playlists.list_all()

    @cherrypy.expose
    def select_playlist(self, name):
        playlists.select_playlist(name)
        
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def update_playlist(self):
        request = cherrypy.request.json
        name = request[0]
        songs = request[1]
        playlists.update_playlist(name, songs)
        return "Done"
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def new_playlist(self):
        return playlists.new_playlist()
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_playlist(self):
        return playlists.get_songs()
        
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def rename_playlist(self):
        request = cherrypy.request.json
        old_name = request["old_name"]
        new_name = request["new_name"]
        return playlists.rename_playlist(old_name, new_name)
        
        
    

if __name__ == "__main__":

    # set up environment
    settings
    
    root_conf = {
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.abspath('./static')
        }           
    }

    rest_conf = {
        '/' : {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True
            #'tools.response.headers.on': True,
            #'tools.response.headers.headers': [('Content-Type', 'text/plain')]
        }
    }

    cherrypy.config.update({'server.socket_host': '127.0.0.1'} )
    cherrypy.quickstart(Root(), '/', root_conf)
