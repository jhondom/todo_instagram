import tornado
from tornado.web import RequestHandler
from utils.account import HashSecret
from handlers import main
from pycket.session import SessionMixin
from utils.account import UserInfoList,register

#登录:
class LoginHandler(main.BaseHandler):
    def get(self, *args, **kwargs):
        next_url = self.get_argument('next','')
        self.render('login.html',next_url = next_url)

    def post(self, *args, **kwargs):
        username = self.get_body_argument('username',None)
        password = self.get_body_argument('password',None)
        next_url = self.get_argument('next','')
        passinto = HashSecret(username,password)
        print(username)
        print(password)
        print('the hash password is {}:'.format(passinto))

        if passinto:
            self.session.set('ID',username)    #登录session设置的ID与main.BaseHandler的self.session.get的ID相同才能使用.
            if next_url:
                self.render(next_url)
            else:
                self.redirect(r'/index')
        else:
            self.write('Login failed!!')


#登出:
class LogoutHandler(main.BaseHandler):
    #登出的同时清楚cookies
    def get(self, *args, **kwargs):
        self.session.delete('ID')
        self.redirect('/login')



#用户注册:
class SignUpHandler(main.BaseHandler):
    def get(self, *args, **kwargs):
        self.render('signup.html')

    def post(self, *args, **kwargs):
        username = self.get_body_argument('username',None)
        password = self.get_body_argument('password',None)
        confirmpassword = self.get_body_argument('confirmpassword',None)
        # email = self.get_body_argument('email',None)
        print('***********')
        if username and password and (password == confirmpassword):
            ret = register(username,password)
            print(username,password,confirmpassword,ret)
            self.session.set('ID',username)
            self.redirect('/index')
        else:
            self.write({'msg':'register fail'})



