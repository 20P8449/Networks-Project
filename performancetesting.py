import threading
import logging
import time
import random
import string
from peer import peerMain
from socket import *

totaltimetofind = 0
chatroomflag=0
def generate_random_name():
    first_names = ['Alice', 'Bob', 'Charlie', 'David', 'Emma', 'Frank', 'Grace', 'Henry']
    last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson']
    random_first_name = random.choice(first_names)
    random_last_name = random.choice(last_names)
    return f"{random_first_name}_{random_last_name}"


def generate_random_password(length=12):
    # Define the characters to choose from
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate the random password
    password = ''.join(random.choice(characters) for _ in range(length))

    return password


class testPerformanceThread(threading.Thread):
    def __init__(self, user_id):
        self.user_id = user_id
        threading.Thread.__init__(self)
        new_logger = self.setup_logger()
        self.peer = peerMain()
        self.logger = new_logger
        global totaltimetofind
        global chatroomflag
        UserName = generate_random_name()
        PASS = generate_random_password(10)
        self.peer.createAccount(UserName,PASS)
        sock = socket()
        sock.bind(('', 0))
        peerServerPort = sock.getsockname()[1]
        self.peer.login(UserName, PASS, peerServerPort)
        self.logger.info(f"User_name:{UserName}")
        self.peer.createChatroom("chatroomperformancetest",UserName)
        starttime=time.time()
        self.peer.FindchatRoom("chatroomperformancetest")
        endtime = time.time()
        self.logger.info(f"Time to find chatroom: {endtime - starttime} seconds")
        totaltimetofind += endtime - starttime

    def setup_logger(self):
        logger = logging.getLogger(f"user_{self.user_id}")
        logger.setLevel(logging.INFO)
        return logger


       

        
def main():
    num_threads = 30
    threads = [testPerformanceThread(user_id=i) for i in range(num_threads)]
    for thread in threads:
        thread.start()
        time.sleep(.3)
    time.sleep(2)  
    for thread in threads:
        thread.join()
        
    print("Average time to find a chatroom: ", totaltimetofind / num_threads)
        

if __name__ == "__main__":
    main()
