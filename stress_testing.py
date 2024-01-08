import time
from db import DB

def stressregister(users):
    first_time = time.time()
    db = DB()
    for user in range(users):
        username = f'test_user_{user}'
        password = f'test_password_{user}'
        db.register(username, password)
    overall_time = time.time() - first_time
    return overall_time


def stresslogin(users):
    first_time = time.time()
    db = DB()
    for user in range(users):
        username = f'test_user_{user}'
        ip = '127.0.0.1'
        port = 12340 + user
        db.user_login(username, ip, port)
    overall_time = time.time() - first_time
    return overall_time



register_time = stressregister(8000)
login_time = stresslogin(8000)

print(f"Register Time: {register_time} seconds")
print(f"Login Time: {login_time} seconds")
