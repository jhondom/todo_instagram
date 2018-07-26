import tornado
import tornado.web
from tornado.web import RequestHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from handlers import main
import os
import tornado.options
from tornado.options import define,options

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
        ('/post/(?P<post_id>[0-9]+)',main.PostHandler)
        ]
        settings ={
            'debug' :True,
            'template_path':'templates',
            'static_path':'static'
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





