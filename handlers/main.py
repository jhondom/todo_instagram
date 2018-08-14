import tornado
import os,glob
from tornado.web import RequestHandler
from utils import makephoto
import pycket
from pycket.session import SessionMixin
from utils import makephoto
from models.users import User


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
        posts = makephoto.get_posts()
        self.render('index.html',posts =posts)


class ExplorerHandler(RequestHandler):
    def get(self,*args, **kwargs):
        posts = makephoto.get_posts()
        self.render('explorer.html',posts= posts)


class PostHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,post_id,*args, **kwargs):
        post = makephoto.get_post(post_id)
        users = makephoto.get_like_users(post.id)
        self.render('post.html',post = post,users = users)


# class UploadHandler(BaseHandler):
#     @tornado.web.authenticated
#     def get(self, *args, **kwargs):
#         self.render('upload.html')
#     def post(self, *args, **kwargs):
#         # upload_path = os.path.join(os.path.dirname(__file__), 'static/images/uploads')
#         upload_path = 'static/images/uploads'
#         print(os.path.dirname(__file__))
#         images = self.request.files.get('newing',None)
#         print(images)
#         for img in images:
#             print(img)
#             filename = img['filename']
#             filepath = os.path.join(upload_path,filename)
#             with open(filepath,'wb') as f:
#                 f.write(img['body'])
#             makephoto.add_post(self.current_user,filepath)
#             #makephoto.make_images(filepath)
#         #self.write('uploads done.')
#         self.redirect(r'/explorer')



#使用UploadFile方法重写UploadHandler.
class UploadHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('upload.html')

    def post(self, *args, **kwargs):
        images = self.request.files.get('newing', None)
        print('~~~~~~~~~~~~~~~')
        print(images)
        for img in images:
            filename = img['filename']
            print(filename)
            #上传文件
            im = makephoto.UploadFile(self.settings['static_path'], img['filename'])
            #保存上传的文件
            im.save_upload_file(img['body'])
            #制作缩略图
            im.make_thumb()
            #保存上传文件到数据库
            makephoto.add_post(self.current_user, im.upload_url, im.thumb_url)
        self.redirect(r'/explorer')



#用户中心用户信息
class ProfileHandler(BaseHandler):
    @tornado.web.authenticated
    # 获取URL数据:get_argument可以获取 URL (查询字符串)中的参数
    def get(self):
        # name = self.get_argument('name',None)
        # print('Get Name:',name)
        # if not name:
        name = self.current_user
        print('current_user:',name)
        user = User.get_user(name)
        print('Get User:', user)
        if not user:
            self.set_status(404)
            self.write('username error!')
        else:
            like_posts = makephoto.get_like_posts(user.id)
            print(like_posts)
            self.render('profile.html',user = user,like_posts = like_posts)













