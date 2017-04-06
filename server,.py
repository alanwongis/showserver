
import cherrypy
import json
import os
import shutil




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
        return "play"
        
    @cherrypy.expose        
    def next(self):
        return "next"
    @cherrypy.expose       
    def prev(self):
        return "prev"
        
    @cherrypy.expose
    def stop(self):
        return "stop"
       
    @cherrypy.expose
    def panic(self):
        return "panic"



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


    cherrypy.quickstart(Root(), '/', root_conf)