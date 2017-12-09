from protocole import Protocole

class Client(object):
    """docstring for Client"""
    def getBoard(self):
        largeur, hauteur, board = self.protocole.receiveBoard()
        return (largeur, hauteur, board)

    def tour(self, mv):
        if self.protocole.MOVE == self.protocole.receive():
            self.protocole.sendMove(mv)
            return True
        else:
            return False
           
    def drawRooms(self):
        for room in self.rooms:
            print(room)   

    def initRoom(self, ide):
       # room = input("voulez vous créer (c) ou rejoindre (r)\n")[0]
        self.room=-1
        if ide < 1 or self.rooms == []:
            print("crée")
            self.protocole.createRoom()
            self.room = self.protocole.receiveAnswerRoom()
        elif ide >=0 :
            print("test")
            self.protocole.joinRoom(ide)
            self.room = self.protocole.receiveAnswerRoom()
            print("wesh")
        return self.room

    def initColor(self):
        self.color, self.begin=self.protocole.receiveColorBegin()

    def askRooms(self):
        self.rooms = self.protocole.receiveRooms()
        return self.rooms

    def quitRoom(self):
        return self.protocole.quitRoom()

    def __init__(self, login, password, server="edznux.fr", sockt=5555):
        self.fini=False
        self.protocole = Protocole(server, sockt)
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