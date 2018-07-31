import tornado
from tornado.web import RequestHandler

class LoginHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('login.html')


