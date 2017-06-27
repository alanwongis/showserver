from __future__ import division, print_function
import cherrypy

import glob
import json
import os
import pickle
import shutil
import subprocess



#curr_dir = "/home/pi/Desktop/showserver"
curr_dir = os.path.split(os.path.abspath(__file__))[0]
music_dir = os.path.join(curr_dir, "music")
playlist_dir = os.path.join(curr_dir, "playlists")

settings = {}
settings = pickle.load(open("settings.pkl", "r"))

playlists = {}
playlists = pickle.load(open("playlists.pkl", "r"))

curr_playlist_name = settings["default_playlist"]
curr_playlist = playlists[curr_playlist_name]
curr_playlist_song = 0


# error message handler
def error_page_default(status, message, trackback, version):
    ret = {
        'status': status,
        'version': version,
        'message': [message],
        'traceback': traceback }
    return json.dumps(ret)



def list_playlists():
    return playlists.keys()

def load_playlist(name):
    curr_playlist = playlists[name]
    curr_playlist_name = name

def new_playlist(name):
    if not(name in playlists.keys()):
        playlists[name] = []
    return playlists[name]
        
def update_playlist(name, songs):
    playlists[name] = songs
    pickle.dump(playlists, open("playlist.txt", "w"))
    

    
    
def list_music():
    filenames  = os.listdir(music_dir)
    return filenames
    
    
    
class Root(object):
    
    _cp_config = {'error_page_default': error_page_default }

    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("/static/index.html")

    # music player api
        
    @cherrypy.expose
    def play(self):
        try:
            playing = subprocess.Popen(['mpg123',
                                        curr_dir+"/music/Fanfare.mp3"])
        except:
            print("exception playing song")
            pass
        return "play!"
        
    @cherrypy.expose        
    def next(self):
        return "next!"
        
    @cherrypy.expose       
    def prev(self):
        return "prev!"
        
    @cherrypy.expose
    def stop(self):
        try:
            subprocess.call(["killall", "mpg123"])
        except:
            print("exception stopping song")
        return "stop!"
       
    @cherrypy.expose
    def panic(self):
        return "panic!"
        
    @cherrypy.expose
    def hello(self, name):
        names.append(name)
        return "<html><body><h1>Hello "+ str(names)+ "</h1></body</html>"

    # songlist API
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_songlist(self):
        return list_music()
    
    @cherrypy.expose
    def delete_song(self, filename):
        return
        
    @cherrypy.expose
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
    def get_playlist(self):
        return str(curr_playlist)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def update_playlist(self):
        items = cherrypy.request.json
        print(items)
        return "Done"

    def new_playlist(self):
        pass
        

if __name__ == "__main__":
    
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

    cherrypy.config.update({'server.socket_host': '0.0.0.0'} )
    cherrypy.quickstart(Root(), '/', root_conf)
