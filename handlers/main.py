import tornado
from tornado.web import RequestHandler

class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')



class ExplorerHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('explorer.html')


class PostHandler(RequestHandler):
    def get(self,post_id,*args, **kwargs):
        self.render('post.html',post_id= post_id)