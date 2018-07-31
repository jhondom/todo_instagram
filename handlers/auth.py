import tornado
from tornado.web import RequestHandler
from utils.account import HashSecret
from handlers import main
from pycket.session import SessionMixin

#登录:
class LoginHandler(main.BaseHandler):
    def get(self, *args, **kwargs):
        self.render('login.html')

    def post(self, *args, **kwargs):
        username = self.get_body_argument('username',None)
        password = self.get_body_argument('password',None)
        passinto = HashSecret(username,password)
        print(username,password,passinto)
        if passinto:
            self.session.set('ID',username)    #登录session设置的ID与main.BaseHandler的self.session.get的ID相同才能使用.
            self.redirect(r'/index')
        else:
            self.write('Login failed')


#登出:
class LogoutHandler(main.BaseHandler):
    #登出的同时清楚cookies
    def get(self, *args, **kwargs):
        self.session.delete('ID')
        self.redirect('/login')



#注册:
class SignUpHandler(main.BaseHandler):
    def get(self, *args, **kwargs):
        self.render('signup.html')

    def post(self, *args, **kwargs):
        pass



