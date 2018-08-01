from models.connect import BASE
from datetime import datetime
from sqlalchemy import Column,Integer,String,DateTime



class User(BASE):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(30),nullable=False)
    password = Column(String(30), nullable=False)
    lastlogin = Column(DateTime, default=datetime.now())
    createtime = Column(DateTime,default=datetime.now())

    def __repr__(self):
         return ('data:{}{}{}{}{}').format(self.id,self.name,self.password,self.lastlogin,self.createtime)