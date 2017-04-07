
import cherrypy
import json
import os
import shutil
import subprocess

curr_dir = "/home/pi/Desktop/showserver"




# error message handler
def error_page_default(status, message, trackback, version):
    ret = {
        'status': status,
        'version': version,
        'message': [message],
        'traceback': traceback }
    return json.dumps(ret)

    
    
class Root(object):
    
    _cp_config = {'error_page_default': error_page_default }

    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("/static/index.html")
        
    @cherrypy.expose
    def play(self):
        playing =subprocess.Popen(['mpg123',
                                   curr_dir+"/music/Lobo_Loco_-_15_-_Party_On_Xanox_5_ID_487.mp3"])
        return "play!"
        
    @cherrypy.expose        
    def next(self):
        return "next!"
    @cherrypy.expose       
    def prev(self):
        return "prev!"
        
    @cherrypy.expose
    def stop(self):
        subprocess.call(["killall", "mpg123"])
        return "stop!"
       
    @cherrypy.expose
    def panic(self):
        return "panic!"



if __name__ == "__main__":
    
    root_conf = {
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.abspath('/home/pi/Desktop/showserver/static')
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
