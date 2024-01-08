import unittest
from unittest.mock import MagicMock, patch
import threading
from io import StringIO
import sys
from colorama import Fore, Back
import peer


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.peer_instance = peer.peerMain()
        self.peer_instance.tcpClientSocket = MagicMock()
        self.peer_instance.registryName = 'testRegistry'
        self.peer_instance.registryPort = 1234

    def tearDown(self):
        print("login")
        self.peer_instance.tcpClientSocket.close()

    def test_login(self):
        username = 'testteam'
        password = 'testPass'
        peerServerPort = 5555
        self.peer_instance.tcpClientSocket.recv.return_value = b'login-success'

        result = self.peer_instance.login(username, password, peerServerPort)

        self.assertEqual(result, 2)

    def test_login_account_donot_exist(self):
        username = 'testteam'
        password = 'testPass'
        peerServerPort = 5555
        self.peer_instance.tcpClientSocket.recv.return_value = b'login-account-not-exist'

        result = self.peer_instance.login(username, password, peerServerPort)

        self.assertEqual(result, 2)

    def test_login_with_account_online(self):
        username = 'testteam'
        password = 'testPass'
        peerServerPort = 5555
        self.peer_instance.tcpClientSocket.recv.return_value = b'login-online'

        result = self.peer_instance.login(username, password, peerServerPort)

        self.assertEqual(result, 1)

class TestCreateAccount(unittest.TestCase):
    def setUp(self):
        self.peer_instance = peer.peerMain()
        self.peer_instance.tcpClientSocket = MagicMock()
        self.peer_instance.registryName = 'testRegistry'
        self.peer_instance.registryPort = 1234

    def tearDown(self):
        print("create account")
        self.peer_instance.tcpClientSocket.close()

    def test_create_account(self):
        username = 'testteam'
        password = 'testPass'
        self.peer_instance.tcpClientSocket.recv.return_value = b'join-success'
        sys.stdout = StringIO()

        self.peer_instance.createAccount(username, password)

        self.peer_instance.tcpClientSocket.send.assert_called_once_with(b'JOIN testUser testPassword')
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output,f"{Fore.RED}Account created...{Fore.RESET}")
        print("test create account done")

class TestSearchUser(unittest.TestCase):
    def setUp(self):
        self.peer_instance = peer.peerMain()
        self.peer_instance.tcpClientSocket = MagicMock()
        self.peer_instance.registryName = 'testRegistry'
        self.peer_instance.registryPort = 1234

    def tearDown(self):
        print("search user")
        self.peer_instance.tcpClientSocket.close()

    def test_search_user(self):
        username = 'testteam'
        peerServerPort = 5555
        self.peer_instance.tcpClientSocket.recv.return_value = b'search-success 1234:5555'
        output = self.peer_instance.findUser(username)

        self.assertEqual(output, '1234:5555')

    def test_search_user_notOnline(self):
        username = 'testUser'
        password = 'testPassword'
        peerServerPort = 5555
        self.peer_instance.tcpClientSocket.recv.return_value = b'search-user-not-online 1234:5555'

        output = self.peer_instance.findUser(username)

        self.assertEqual(output, 0)

class TestJoinChatroom(unittest.TestCase):
    def setUp(self):
        self.peer_instance = peer.peerMain()  # replace with your class name
        self.peer_instance.tcpClientSocket = MagicMock()
        self.peer_instance.registryName = 'testRegistry'
        self.peer_instance.registryPort = 1234

    def tearDown(self):
        print("login")
        self.peer_instance.tcpClientSocket.close()

    def test_chatroom(self):
        roomname = 'testroomname'
        admin = 'testadmin'
        self.peer_instance.tcpClientSocket.recv.return_value = b'join-success'
        sys.stdout = StringIO()

        self.peer_instance.joinchatRoom(roomname, admin)

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, f'joined {roomname} successfully')

    #
    @patch('threading.Timer')
    def test_chatroom_notexist(self, mock_timer):
        roomname = 'testroomname'
        admin = 'testadmin'
        self.peer_instance.loginCredentials = ('testUser', 'testPassword')
        self.peer_instance.tcpClientSocket.recv.return_value = b'roomnotfound'
        sys.stdout = StringIO()

        self.peer_instance.joinchatRoom(roomname, admin)

        output = sys.stdout.getvalue().strip()

        self.assertEqual(output, 'Room not exist\nlogging out')


