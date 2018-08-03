import glob
import os
from PIL import Image
from models.users import PostFile
from models.connect import session
from models import users

#获取图片
def get_images():
    images = glob.glob('/home/pyvip/.virtualenvs/ws/todo/static/images/uploads/*.jpg')
    make_images()
    #print(images,type(images),len(images))
    return len(images)

#压缩图片
def make_images():
    #os.walk(top, topdown=True, onerror=None, followlinks=False)得到一个三元tupple(dirpath, dirnames, filenames),
    #dirpath 是一个string，代表目录的路径，dirnames 是一个list，包含了dirpath下所有子目录的名字。filenames 是一个list，包含了非目录文件的名字。
    #名字不包含路径信息如果需要得到全路径，需要使用os.path.join(dirpath, name).
    file_path = '/home/pyvip/.virtualenvs/ws/todo/static/images/uploads'
    for root,dirs,files in os.walk(file_path):
        count = 1
        #print(root)
        #print(dirs)
        #print(files)
        #print('***************************')
        for file in files:
            #print(file)
            if file.endswith('.jpg'):
                path = os.path.join('/home/pyvip/.virtualenvs/ws/todo/static/images/uploads',file)
                im = Image.open(path)
                out = im.resize((60,40))
                out.save('/home/pyvip/.virtualenvs/ws/todo/static/images/uploads/upload' + str(count) + '.png','PNG')
                count +=1
                #print(file)


#图片保存到数据库
def add_post(username,img_url):
    user = session.query(users.User).filter_by(name =username).first()
    post = PostFile(userid =user.id,image_url=img_url)
    session.add(post)
    session.commit()

#查询图片
def get_posts():
    posts = session.query(PostFile).all()
    return posts


def get_post(post_id):
    post = session.query(PostFile).filter_by(id = post_id).scalar()
    return post