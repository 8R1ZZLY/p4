from src.classes.protocole import Protocole
import re

class Client(object):
    """docstring for Client"""
    #def getBoard(self):
    #    largeur, hauteur, board = self.protocole.receiveBoard()
    #    return (largeur, hauteur, board)

    MOVE="move"
    BOARD="board"

    def translateBoard(self, b):
        #datas = self.sock.recv(1024).decode('UTF8')
        stream = re.sub(self.protocole.BOARD, "", b)
        cases = stream.split(',') # attention la premeire case est la largeur
        largeur = int(cases[0])
        hauteur = (len(cases)-1)//largeur
        board = [["" for i in range(hauteur)] for j in range(largeur)]
        for i in range(len(cases)-1):
            x =  i // hauteur
            y = hauteur - 1- (i % hauteur) 
            board[x][y] = cases[i+1]
        return (largeur, hauteur, board)

    def listen(self):
        rcv = self.protocole.receive()
        print("debut rcv listen")
        print(rcv)
        print("fin rcv listen")
        if self.protocole.MOVE in rcv:
            return self.MOVE
        elif self.protocole.BOARD in rcv:
            self.board=self.translateBoard(rcv)
            return self.BOARD
        else:
            return ""

    def sendMove(self, mv):
        self.protocole.sendMove(mv)
           
    def drawRooms(self):
        for room in self.rooms:
            print(room)   

    def initRoom(self, ide):
       # room = input("voulez vous créer (c) ou rejoindre (r)\n")[0]
        
        if ide < 0 or self.rooms == []:
            print("crée")
            self.protocole.createRoom()
            self.room = self.protocole.receiveAnswerRoom()
        elif ide >=0 :
            print("test")
            self.protocole.joinRoom(ide)
            self.room = self.protocole.receiveAnswerRoom()
            print("wesh")
        self.initColor()
        return self.room

    def initColor(self):
        self.color, self.begin=self.protocole.receiveColorBegin()

    def askRooms(self):
        self.rooms = self.protocole.receiveRooms()
        return self.rooms

    def quitRoom(self):
        return self.protocole.quitRoom()

    def __init__(self, login, password, server="edznux.fr", sockt=5555):
        self.rooms=[]
        self.color=""
        self.begin=""
        self.room=-1
        self.fini=False
        self.protocole = Protocole(server, sockt)
        self.board=[]
        tries = 0
        self.protocole.sendVersion()
        #self.protocole.receiveVersion()

        self.protocole.sendLogin(login)
        rcv = self.protocole.receive()
        
        if rcv == self.protocole.ASK_PASSWORD:
            while(1):
                if tries == 2:
                  raise Exception("[!]Error three bad login attempts") 
                self.protocole.sendPassword(password)
                rcv = self.protocole.receive()
                if rcv == self.protocole.SUCCESS_AUTHENTICATED: # à rajouer
                    break
                else:
                  tries += 1
        
        elif rcv == self.protocole.UNKNOWN_LOGIN:
            self.protocole.registerUser(login, password)
            if self.protocole.receive() == self.protocole.CONFIRM_ACCOUNT:
                self.protocole.confirmUser(login, password)
                if self.protocole.receive() == self.protocole.ACCOUNT_CREATED:
                    print("[*]Your account has been created")
                else:
                    print(self.protocole.receive())
                    raise Exception("[!]The password didn't match")
            else:
                raise Exception("[!]Server don't ask to confirm credentials")
        else:
            raise Exception("[!]Can't connect to the serveur")
        print("authentification ok")
        self.askRooms()
        #print("on va draw")
        #self.drawRooms()
        self.fini=True