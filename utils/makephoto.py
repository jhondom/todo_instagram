import glob
import os,uuid,string
from PIL import Image
from models.users import PostFile
from models.connect import session
from models import users

# #获取图片
# def get_images():
#     images = glob.glob('/home/pyvip/.virtualenvs/ws/todo/static/images/uploads/*.jpg')
#     make_images()
#     #print(images,type(images),len(images))
#     return len(images)
#
# #压缩图片
# def make_images():
#     #os.walk(top, topdown=True, onerror=None, followlinks=False)得到一个三元tupple(dirpath, dirnames, filenames),
#     #dirpath 是一个string，代表目录的路径，dirnames 是一个list，包含了dirpath下所有子目录的名字。filenames 是一个list，包含了非目录文件的名字。
#     #名字不包含路径信息如果需要得到全路径，需要使用os.path.join(dirpath, name).
#     file_path = '/home/pyvip/.virtualenvs/ws/todo/static/images/uploads'
#     for root,dirs,files in os.walk(file_path):
#         count = 1
#         #print(root)
#         #print(dirs)
#         #print(files)
#         #print('***************************')
#         for file in files:
#             #print(file)
#             if file.endswith('.jpg'):
#                 path = os.path.join('/home/pyvip/.virtualenvs/ws/todo/static/images/uploads',file)
#                 im = Image.open(path)
#                 out = im.resize((60,40))
#                 out.save('/home/pyvip/.virtualenvs/ws/todo/static/images/uploads/upload' + str(count) + '.png','PNG')
#                 count +=1
#                 #print(file)



#使用类来定义上传的地址，减少硬编码:

class UploadFile(object):
    upload_dir = 'images/uploads'
    thumbs_dir = 'images/thumbs'
    thumbs_size = (200, 200)


    def __init__(self, static_path, upload_name):
        self.static_path = static_path
        self.upload_name = upload_name  # 文件名 xxx.jpg
        self.name = self.gen_name

    @property
    def gen_name(self):
        # 生成随机字符串用作文件名称
        _, ext = os.path.splitext(self.upload_name)
        return uuid.uuid4().hex + ext

    # @property广泛应用在类的定义中,Python内置的@property装饰器就是负责把一个方法变成属性调用的，
    # 可以让调用者写出简短的代码，同时保证对参数进行必要的检查，这样，程序运行时就减少了出错的可能性。

    @property
    def save_to_path(self):
        # 文件的写入路径
        return self.upload_url

    def save_upload_file(self, context):
        with open(self.save_to_path, 'wb') as f:
            f.write(context)

    @property
    def upload_url(self):
        return os.path.join(self.static_path,self.upload_dir, self.name)

    def make_thumb(self):
        im = Image.open(self.save_to_path)
        im.thumbnail(self.thumbs_size)
        im.save(os.path.join(self.thumb_url), 'JPEG')

    @property
    def thumb_url(self):
        #分割文件名与扩展名
        filename, ext = os.path.splitext(self.name)

        return (os.path.join(self.static_path, self.thumbs_dir,
                            '{}_{}x{}'.format(filename, self.thumbs_size[0], self.thumbs_size[1])) + ext)




#图片保存到数据库
def add_post(username,img_url,thumb_url):
    user = session.query(users.User).filter_by(name =username).first()
    post = PostFile(userid =user.id,image_url=img_url,thumb_url=thumb_url)
    session.add(post)
    session.commit()

#查询所有图片
def get_posts():
    posts = session.query(PostFile).all()
    return posts

#单张展示图片
def get_post(post_id):
    post = session.query(PostFile).filter_by(id = post_id).scalar()
    return post

#按用户id展示图片
def get_post_for(username):
    id = session.query(users.User).filter_by(name = username).scalar()
    posts = session.query(PostFile).filter_by(id = id).scalar()
    return posts
