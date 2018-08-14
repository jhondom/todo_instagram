import tornado.web
from .main import BaseHandler
from tornado.httpclient import HTTPClient,AsyncHTTPClient
from utils.makephoto import UploadFile,add_post
from tornado import gen

# 同步处理用户请求
# https://unsplash.it/400/800/?random
class SyncSaveUrlHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        url = self.get_argument('url','')
        # 模拟客户端打开url连接
        client = HTTPClient()
        response = client.fetch(url)
        # 初始化实例
        IM = UploadFile(self.settings['static_path'],'xx.jpg')
        IM.save_upload_file(response.body)
        IM.make_thumb()
        post = add_post(self.current_user,IM.upload_url,IM.thumb_url)

        # self.redirect('/post/{}'.format(post.id))
        self.redirect('/explorer')

# 使用协程异步处理用户请求
class AsyncSaveUrlHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        url = self.get_argument('url','')
        client = AsyncHTTPClient()
        response = yield client.fetch(url)
        IM = UploadFile(self.settings['static_path'], 'xx.jpg')
        IM.save_upload_file(response.body)
        IM.make_thumb()
        post = add_post(self.current_user, IM.upload_url, IM.thumb_url)

        # self.redirect('/post/{}'.format(post.id))
        self.redirect('/explorer')




