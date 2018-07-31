import tornado
import os,glob
from tornado.web import RequestHandler
from utils import makephoto
import pycket
from pycket.session import SessionMixin

class BaseHandler(RequestHandler,SessionMixin):
    def get_current_user(self):
        current_user = self.session.get('ID',None)
        if current_user:
            return current_user
        else:
            return None


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    #if not self.current_user: self.redirect()
    def get(self, *args, **kwargs):
        self.render('index.html')


class ExplorerHandler(RequestHandler):
    def get(self,*args, **kwargs):
        num = makephoto.get_images()
        self.render('explorer.html',num = num)


class PostHandler(RequestHandler):
    def get(self,post_id,*args, **kwargs):
        self.render('post.html',post_id= post_id)


class UploadHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('upload.html')
    def post(self, *args, **kwargs):
        # upload_path = os.path.join(os.path.dirname(__file__), 'static/images/uploads')
        upload_path = 'static/images/uploads'
        print(os.path.dirname(__file__))
        images = self.request.files.get('newing',None)
        print(images)
        for img in images:
            print(img)
            filename = img['filename']
            filepath = os.path.join(upload_path,filename)
            with open(filepath,'wb') as f:
                f.write(img['body'])
        #self.write('uploads done.')
        self.redirect(r'/explorer')
















