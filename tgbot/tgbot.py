import cherrypy
import markdown2

from .bot import Bot
from .objects import Update
from .utils import Service


class TGBot(Service, Bot):
    exposed = True

    def __init__(
            self,
            service_name: str,
            service_address: str,
            service_token: str,
            catalog: str,
            tg_token: str,
            supabase_endpoint: str,
            supabase_token: str,
            supabase_email: str,
            supabase_password: str,
            supabase_table: str,
            debug: bool = False
    ):
        Bot.__init__(
            self,
            tg_token,
            supabase_endpoint=supabase_endpoint,
            supabase_token=supabase_token,
            supabase_email=supabase_email,
            supabase_password=supabase_password,
            supabase_table=supabase_table
        )
        if not debug:
            Service.__init__(
                self,
                name=service_name,
                address=service_address,
                token=service_token,
                catalog=catalog
            )

    def GET(self, *uri, **params):
        if len(uri) == 0:
            return markdown2.markdown_path("README.md")
        else:
            raise cherrypy.HTTPError(404)

    def POST(self, *uri, **params):
        if len(uri) != 1 or uri[0] != self.tg_token():
            raise cherrypy.HTTPError(404)
        self.parse(Update(params))
