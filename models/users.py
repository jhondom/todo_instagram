from models.connect import BASE
from datetime import datetime
from sqlalchemy import Column,Integer,String,DateTime,sql,ForeignKey
from models.connect import session
from sqlalchemy.orm import relationship



class User(BASE):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(100),nullable=False)
    password = Column(String(100), nullable=False)
    lastlogin = Column(DateTime, default=datetime.now())
    createtime = Column(DateTime,default=datetime.now())

    def __repr__(self):
         return ('data:{}{}{}{}{}').format(self.id,self.name,self.password,self.lastlogin,self.createtime)


    @classmethod
    # classmethod是用来指定一个类的方法为类方法，没有此参数指定的类的方法为实例方法。
    # 要使用某个类的方法，需要先实例化一个对象再调用方法。而使用@staticmethod或@classmethod，就可以不需要实例化，直接类名.方法名()来调用。
    # @staticmethod不需要表示自身对象的self和自身类的cls参数，就跟使用函数一样。
    # @classmethod也不需要self参数，但第一个参数需要是表示自身类的cls参数。
    # 如果在@staticmethod中要调用到这个类的一些属性方法，只能直接类名.属性名或类名.方法名。
    # 而@classmethod因为持有cls参数，可以来调用类的属性，类的方法，实例化对象等，避免硬编码。

    #判断注册的用户名是否存在:
    def IS_EXISTS(cls,username):
        return session.query(sql.exists().where(User.name == username)).scalar()

    @classmethod
    #添加注册用户:
    def add_user(cls,username,password):
        # 生成你要创建的数据对象
        user = User(name = username,password = password)
        # 把要创建的数据对象添加到这个session里， 一会统一创建
        session.add(user)
        # 统一提交，创建数据
        session.commit()

    @classmethod
    #获取密码:
    def get_password(cls,username):
        user = session.query(cls).filter_by(name = username).scalar()
        if user:
            return user.password
        else:
            return ''

    @classmethod
    def get_user(cls,username):
        user = session.query(cls).filter_by(name = username).scalar()
        return user


class PostFile(BASE):
    __tablename__ = 'posts'
    id = Column(Integer,primary_key=True,autoincrement=True)
    image_url = Column(String(200), nullable=False)
    thumb_url = Column(String(200), nullable=False)
    userid = Column(Integer,ForeignKey(User.id))
    createtime = Column(DateTime,default=datetime.now())
    # 允许你在user表里通过backref字段反向查出所有它在posts表里的关联项
    user = relationship('User',backref = 'posts',uselist = False)

    def __repr__(self):
         return '<PostFile(#{}{}{})>'.format(self.id,self.image_url,self.userid)


class Like(BASE):
    __tablename__= 'likes'
    user_id = Column(Integer,primary_key=True,autoincrement=True)
    post_id = Column(Integer,autoincrement=True)
    createtime = Column(DateTime, default=datetime.now())


    def __repr__(self):
         return '<Like(#{}{})>'.format(self.user_id,self.post_id)