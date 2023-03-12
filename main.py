import cherrypy

from config import config
from tgbot import TGBot


def create_app():
    app = cherrypy.tree.mount(TGBot(**config), "/", {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher()
        }
    })
    cherrypy.config.update({'engine.autoreload.on': False})
    cherrypy.server.unsubscribe()
    cherrypy.engine.start()
    return app
