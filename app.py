# 实现类似instagram的图片上传，预览功能:
# 主要组成
# - 发现或最近上传的图片页面
# - 所关注的用户图片流
# - 单个图片详情页面
# - 数据库 Database
# - 用户档案 User Profile

# 图片上传查看常见的思路有两种：一是将图片上传至服务器的临时文件夹中，并返回该图片的url，然后渲染在html页面；另一种思路是，直接在本地内存中预览图片，用户确认提交后再上传至服务器保存。
# 这两种方法各有利弊，方法一很明显，浪费流量和服务器资源；方法二则加重了浏览器的负担，并且对浏览器的兼容性要求更高（在某些低版本中的IE浏览器不支持）。


import tornado
import tornado.web
from tornado.web import RequestHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from handlers import main
import os
import tornado.options
from tornado.options import define,options
from handlers import auth,chat,service
import redis

BASE_DIRS = os.path.dirname(__file__)
define('port',default=8000,help='listen port',type=int)


# if __name__=='__main__':
#     app = tornado.web.Application(
#         handlers =[
#             ('/index',main.IndexHandler),
#             ('/explorer',main.ExplorerHandler),
#             ('/post/(?P<post_id>[0-9]+)',main.PostHandler),
#     ],
#        debug = True,
#        template_path = 'templates',
#        static_path=os.path.join(BASE_DIRS,'static')
#     )
#     httpserver = HTTPServer(app)
#     httpserver.bind(options.port)
#     httpserver.start()
#     print('Server is Running!')
#     IOLoop.current().start()



class Application(tornado.web.Application):
    def __init__(self):
        handlers =[
            ('/index',main.IndexHandler),
            ('/explorer',main.ExplorerHandler),
            ('/post/(?P<post_id>[0-9]+)',main.PostHandler),
            ('/upload',main.UploadHandler),
            (r'/profile',main.ProfileHandler),
            (r'/login',auth.LoginHandler),
            (r'/logout',auth.LogoutHandler),
            (r'/signup',auth.SignUpHandler),
            (r'/chat',chat.RoomHandler),
            (r'/save',service.SyncSaveUrlHandler),
            (r'/saves',service.AsyncSaveUrlHandler)
        ]

        settings ={
            'debug' :True,
            'template_path':'templates',
            'static_path':'static',
            'login_url':'/login',
            'cookie_secret': 'GENERATE_YOUR_OWN_RANDOM_VALUE_HERE',
            'pycket' :{
            'engine': 'redis',
            'storage': { 'host': 'localhost',
                           'port': 6379,
                          # 'password': '',
                           'db_sessions': 5,  # redis db index
                           'db_notifications': 11,
                           'max_connections': 2 ** 30,},
            'cookies': {'expires_days': 30,},
                       }
                 }
#super 重写父类方法。但是又要用父类，前面的方法为父类的方法，将父类的__init__方法重写后将handlers,setting作为参数传给Application.
# **setting :对settings进行解包,相当于super(Application,self).__init__(handlers,debug = True,template_path = 'templates',static_path = 'static')
        super(Application,self).__init__(handlers,**settings)


if __name__=='__main__':
    app = Application()
    tornado.options.parse_command_line()
    app.listen(options.port)
    print('Server is Running at port:{}!'.format(options.port))
    IOLoop.current().start()





