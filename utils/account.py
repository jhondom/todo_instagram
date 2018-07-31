import hashlib

def HashFunc(text):
    return hashlib.md5(text.encode()).hexdigest()

UserInfoList ={
    'name':'Eason',
    'password':HashFunc('mima')
}


def HashSecret(Username,Password):
    return (UserInfoList['name'] == Username) and (UserInfoList['password'] == HashFunc(Password))
