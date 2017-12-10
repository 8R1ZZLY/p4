from socket import socket, AF_INET, SOCK_STREAM
import re

class Protocole(object):

    VERSION = "VERSION"
    NB_VERSION = "1.0"
    LOGIN = "LOGIN"
    UNKNOWN_LOGIN = "UNKNOWN_LOGIN"
    CREATE_ACCOUNT = "CREATE_ACCOUNT"
    CONFIRM_ACCOUNT = "CONFIRM_ACCOUNT"
    PASSWORD = "PASSWORD"
    ASK_PASSWORD = "ASK_PASSWORD"
    WRONG_PASSWORD = "ERROR:WRONG_PASSWORD"
    SUCCESS_AUTHENTICATED = "SUCCESS:AUTHENTICATED"
    ACCOUNT_CREATED = "SUCCESS:ACCOUNT_CREATED"
    ASK_ROOMS = "ASK_ROOMS"
    SUCCESS_ROOMS = "SUCCESS:Rooms sent"
    EMPTY_ROOMS = "ERROR:No rooms found"
    CREATE_ROOM = "CREATE_ROOM"
    CREATE_ROMM_ERROR = "ERROR:Cannot create room"
    SELECT_ROOM = "SELECT_ROOM"
    SUCCESS_ROOM = "SUCCESS"
    ERROR_ROOM = "ROOM does not exist"
    COLOR = "COLOR"
    PAWN = ['X', 'O', '=']
    ERROR_COLOR = "ERROR:Color not available"
    BEGIN = "BEGIN"
    ERROR_MOVE = "ERROR:Impossible move"
    QUIT_ROOM = "QUIT_ROOM"
    QUIT_ROOM_SUCCESS = "SUCCESS:You left the room"
    QUIT_ROOM_ERROR = "ERROR:Can't left the room"
    GAME_FINISHED = "GAME_FINISHED"
    ASK_LIST = "ASK_LIST"
    LIST = "LIST"
    QUERY_LOGIN = "QUERY_LOGIN"
    LOGIN_INFO = "LOGIN_INFO"
    QUIT_SERVER = "QUIT_SERVER"
    BOARD = "BOARD:"
    MOVE = "MOVE"

    def __init__(self, server, sockt):
        self.SERVER_IP = server
        self.SERVER_SOCKET = sockt
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((self.SERVER_IP, self.SERVER_SOCKET))

    def sendMove(self, mv):
        self.sock.send("{}:{}".format(self.MOVE, mv).encode('UTF8'))

    def receive(self):
        return self.sock.recv(1024).decode('UTF8')

    def sendVersion(self):
        ''' send actual version  to the server  and parse  response '''
        self.sock.send("{}:{}".format(self.VERSION, self.NB_VERSION).encode('UTF8'))
        return self.sock.recv(1024).decode('UTF8') == "{}:{}".format(self.VERSION, self.NB_VERSION)

    def receiveVersion(self):
        print("receive version")
        rcv = self.sock.recv(1024).decode('UTF8')
        print("rcv  " + rcv)
        parties = rcv.split(':')
        if self.VERSION == parties[0]:
            return parties[1]
        return ""

    def sendLogin(self, login):
        self.sock.send("{}:{}".format(self.LOGIN, login).encode('UTF8'))

    def sendPassword(self, password):
        self.sock.send("{}:{}".format(self.PASSWORD, password).encode('UTF8'))

    def registerUser(self, login, password):
        self.sock.send("{}:{},{}:{}".format(self.CREATE_ACCOUNT, login, self.PASSWORD, password).encode('UTF8'))

    def confirmUser(self, login, confirm_password):
        self.sock.send("{}:{},{}:{}".format(self.CONFIRM_ACCOUNT, login, self.PASSWORD, confirm_password).encode('UTF8'))        

    def receiveRooms(self):
        self.sock.send("{}".format(self.ASK_ROOMS).encode('UTF8'))
        print("test receive")
        rooms_separator = "ROOM:"
        rcv = self.sock.recv(1024).decode('UTF8')
        print(rcv)
        print("post rcv")
        if self.EMPTY_ROOMS in rcv:
            print('[*] No rooms was been found')
        else:
            while not self.SUCCESS_ROOMS in rcv :
                rcv += self.sock.recv(1024).decode('UTF8')
            print(rcv)
            new_rcv=re.sub(self.SUCCESS_ROOMS, "", rcv)

            rooms = [ item for item in new_rcv.split(rooms_separator) if item]

            traitement = list(map(lambda x: [int(x[0]), x[1].split('|'), x[2]], map(lambda x: x.split(","), rooms)))
            print("retour1")
            return traitement
        print("retour2")
        return []

    def createRoom(self):
        envoie = "{}".format(self.CREATE_ROOM).encode('UTF8')
        print("envoi\n" )
        print(envoie)
        self.sock.send("{}".format(self.CREATE_ROOM).encode('UTF8'))

    def joinRoom(self, nb):
        envoie = "{}:{}".format(self.SELECT_ROOM, nb).encode('UTF8')
        print("envoi\n" )
        print(envoie)
        self.sock.send(envoie)
        print("envoyé\n" )

    def receiveAnswerRoom(self):
        print("attendte rep answer room")
        rcv = self.sock.recv(1024).decode('UTF8')
        print("rcv\n"+rcv)
        print("fin rcv answer room")
        parties = rcv.split(':')
        if self.SUCCESS_ROOM == parties[0]:
            num = parties[1]
            if num.isdigit():
                return int(num)
        return -1

    def receiveColorBegin(self):
        print("couleur")
        rcv = self.sock.recv(len(self.COLOR)+2).decode('UTF8')
        print("ici")
        print(rcv)
        print("fin rcv")
        parties = rcv.split(':')
        color =""
        begin =""
        # ex parties: "COLOR:OBEGIN:X"
        if self.COLOR in parties[0]: # COLOR
            color=parties[1] # O
        
        print("couleur")
        rcv = self.sock.recv(len(self.COLOR)+2).decode('UTF8')
        print("ici")
        print(rcv)
        print("fin rcv")
        parties = rcv.split(':')

        if self.BEGIN in parties[0]:
            begin=parties[1] # X
        return (color, begin)

    def getPlayersList(self):
        self.sock.send("{}".format(self.ASK_LIST).encode('UTF8'))
        rcv = self.sock.recv(1024).decode('UTF8')
        return re.sub('LIST:', '', rcv).split(',')

    def queryLogin(self, player):
        info = {}
        self.sock.send("{}:{}".format(self.QUERY_LOGIN, player).encode('UTF8'))
        rcv = re.sub('LOGIN_INFO:', '', self.sock.recv(1024).decode('UTF8')).split(',')
        #info['name'], info['last_connection'], info['best_score'], info['best_time'], info['nb_game'], info['first_game'] = rcv[0], rcv[1], rcv[2], rcv[3], rcv[4], rcv[5]
        info['name'], info['last_connection'], info['best_score'], info['best_time'], info['nb_game'], info['first_game'] = rcv[:6]
        return info

    def quitRoom(self):
        self.sock.send("{}".format(self.QUIT_ROOM).encode('UTF8'))
        rcv = self.sock.recv(1024).decode('UTF8')
        print("rcv")
        print(rcv)
        print("fin rcv")
        if rcv == self.QUIT_ROOM_SUCCESS:
            return True
        else:
            return False

    def quitServer(self):
        self.sock.send("{}".format(self.QUIT_SERVER).encode('UTF8'))
        print('[*]You left the server')
