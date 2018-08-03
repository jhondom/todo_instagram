import hashlib
from models import users

def HashFunc(text):
    return hashlib.md5(text.encode()).hexdigest()

UserInfoList ={
    'name':'Eason',
    'password':HashFunc('mima')
}


def HashSecret(Username,Password):
    #return (UserInfoList['name'] == Username) and (UserInfoList['password'] == HashFunc(Password))
    if Username and Password:
        hash_pass = users.User.get_password(Username)
        return hash_pass and hash_pass == HashFunc(Password)
    else:
        return False



def register(username,password):
    if users.User.IS_EXISTS(username):
        return {'msg':'username is exists'}
    else:
        users.User.add_user(username,HashFunc(password))
        return {'msg':'ok'}