from __future__ import division, print_function
import cherrypy

import glob
import json
import os
import shutil
import subprocess


#curr_dir = "/home/pi/Desktop/showserver"
curr_dir = os.path.split(os.path.abspath(__file__))[0]
music_dir = os.path.join(curr_dir, "music")

playlist = []
playlist_song = -1


# error message handler
def error_page_default(status, message, trackback, version):
    ret = {
        'status': status,
        'version': version,
        'message': [message],
        'traceback': traceback }
    return json.dumps(ret)

    
    
def list_music():
    filenames  = os.listdir(music_dir)
    return filenames
    
    
    
class Root(object):
    
    _cp_config = {'error_page_default': error_page_default }

    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("/static/index.html")
        
    @cherrypy.expose
    def play(self):
        try:
            playing =subprocess.Popen(['mpg123',
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


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def list_songs(self):
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
        
        
    @cherrypy.expose  
    def show_playlist(self):
        return str(playlist)

    @cherrypy.expose
    def update_playlist(self, items):
        return "Done"


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
