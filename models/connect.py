#创建连接
from sqlalchemy import create_engine


HOSTNAME = '127.0.0.1'
PORT ='3306'
DATABASE ='toproject'
USERNAME ='develop'
PASSWROD ='QWEqwe123'

#创建数据连接uri:
db_uri ='mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(USERNAME,PASSWROD,HOSTNAME,DATABASE)
engine = create_engine(db_uri)

# oracle+cx_oracle://user:pass@host:port/dbname[?key=value&key=value...]

#创建module的BASE类:
# 对象关系型映射，数据库中的表与python中的类相对应，创建的类必须继承自 sqlalchemy 中的基类。
# 使用 declarative 方法定义的映射类依据一个基类，这个基类是维系类和数据表关系的目录。
# 应用通常只需要有一个 Base 的实例。我们通过 declarative_base() 功能创建一个基类。
from sqlalchemy.ext.declarative import declarative_base
BASE = declarative_base(engine)

#创建会话:
from sqlalchemy.orm import sessionmaker
# 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
Session = sessionmaker(engine)
# 生成session实例
session = Session()


if __name__=='__main__':
    connect = engine.connect()
    result = connect.execute('select * from Student')
    print(result.fetchall())
