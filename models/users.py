from models.connect import BASE
from datetime import datetime
from sqlalchemy import Column,Integer,String,DateTime,sql,ForeignKey
from models.connect import session
from sqlalchemy.orm import relationship



class User(BASE):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(30),nullable=False)
    password = Column(String(30), nullable=False)
    lastlogin = Column(DateTime, default=datetime.now())
    createtime = Column(DateTime,default=datetime.now())

    def __repr__(self):
         return ('data:{}{}{}{}{}').format(self.id,self.name,self.password,self.lastlogin,self.createtime)


    @classmethod
    #判断注册的用户名是否存在:
    def IS_EXISTS(cls,username):
        return session.query(sql.exists().where(User.name == username)).scalar()

    @classmethod
    #添加注册用户:
    def add_user(cls,username,password):
        user = User(name = username,password = password)
        session.add(user)
        session.commit()

    @classmethod
    #获取密码:
    def get_password(cls,username):
        user = session.query(cls).filter_by(name = username).scalar()
        if user:
            return user.password
        else:
            return ''



class PostFile(BASE):
    __tablename__ = 'posts'
    id = Column(Integer,primary_key=True,autoincrement=True)
    image_url = Column(String(60), nullable=False)
    userid = Column(Integer,ForeignKey(User.id))
    createtime = Column(DateTime,default=datetime.now())
    user = relationship('User',backref = 'posts',uselist = False)

    def __repr__(self):
         return '<PostFile(#{}{}{})>'.format(self.id,self.image_url,self.userid)