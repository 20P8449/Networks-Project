from pymongo import MongoClient
import hashlib
class DB:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['p2p-chat']

    def is_account_exist(self, username):
        return len(list(self.db.accounts.find({'username': username}))) > 0

    def register(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        account = {
            "username": username,
            "password": hashed_password

        }
        self.db.accounts.insert_one(account)

    def get_password(self, username):
        return self.db.accounts.find_one({"username": username})["password"]

    def is_account_online(self, username):
        if self.db.online_peers.count_documents({"username": username}) > 0:
            return True
        else:
            return False
    # def is_account_online(self, username):
    #     return len(list(self.db.online_peers.find({"username": username}))) > 0

    def user_login(self, username, ip, port):
        online_peer = {
            "username": username,
            "ip": ip,
            "port": port
        }
        self.db.online_peers.insert_one(online_peer)

    def user_logout(self, username):
        self.db.online_peers.remove({"username": username})

    def get_peer_ip_port(self, username):
        res = self.db.online_peers.find_one({"username": username})
        return (res["ip"], res["port"])

    def get_online_users(self):
        projection = {'_id': 0, 'username': 1}
        return list(self.db.online_peers.find({}, projection))
    # def list_online_users(self):
    #     online_users = []
    #     for user in online_users:
    #         if user.isOnline:
    #             online_users.append(user.username)
    #     return online_users
    def chatroom_exist(self, chatroomName):
        chatroom_exists = self.db.chatrooms.find_one({'chatroomName': chatroomName})
        if chatroom_exists is not None:
            return True
        else:
            return False

    def leave_room(self,chatroom, username):
        self.db.chatrooms.update_one(
            {"chatroomName": chatroom},
            {'$pull': {'peers': {'username': username}}}
        )
    def SearchUserinChatroom(self,chatroomName, username):
        return self.db.chatrooms.count_documents({'chatroomName': chatroomName, 'peers': username}) > 0

    def print_users(self, chatroomName):
        ChatRoom = self.db.chatrooms.find_one({"chatroomName": chatroomName})
        if ChatRoom and 'peers' in ChatRoom:
            return ChatRoom['peers']

    def JoinRoom(self, chatroomName, username):
        if not self.SearchUserinChatroom(chatroomName,username):
            self.db.chatrooms.update_one(
                {"chatroomName": chatroomName}, {"$push": {"peers": username}}
            )
            self.db.accounts.update_one(
                {"username": username}, {"$push": {"ChatRooms": chatroomName}}
            )

    def addroom(self, chatroomName, RoomCreator):
        if not self.chatroom_exist(chatroomName):
            chatroom = {
                "chatroomName": chatroomName,
                "RoomCreator": RoomCreator,
                "peers": [RoomCreator]
            }
            self.db.accounts.update_one(
                {"username": RoomCreator}, {"$push": {"ChatRooms": chatroomName}}
            )
            self.db.chatrooms.insert_one(chatroom)
