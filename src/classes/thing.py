from enum import Enum
import os
import functools
import pygame
import pygame.color
import os
from pygame.locals import *

from src.classes.client import Client


#Enumeration

#BoardBox is the status of the case
class BoardBox(Enum):
    EMPTY = 0
    PLAYER1 = 1 #BB2330 red
    PLAYER2 = 2 #FDC500 yellow



#Factory return the line to play if the column is playable or a number lower than 0 if it is not playable
class Factory():
    #whichrow is playable in this column
    def whichrow(column):
        for hplay in reversed(range(0,len(column))):
            if column[hplay] == BoardBox.EMPTY.value:
                return hplay
        return -1
    def bloc2pixel():
        return
    def pixel2bloc():
        return
    #window size !
    def windowsize():
        return 800, 400
    def gameoverscreen(pygame,screen,message):
        font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets','visitor2.ttf')
        fontobj = pygame.font.Font(font_path, 40)
        screenw, screenh = pygame.display.get_surface().get_size()
        textw, texth = fontobj.size(message)
        screen.fill((0, 0, 0))
        x= int(screenw - textw)//2
        y= int(screenh - texth)//2
        res = fontobj.render(message,1,(255,255,255))
        screen.blit(res,(x,y))
        

#Thing is the very great mother class
class Thing:
    def __init__(self,pygame,screen,x=0,y=0,z=0,visible=True):
        self.position = {'x':x,'y':y,'z':z}
        self.pygame = pygame
        self.screen = screen
        self.visible = visible
    def render(self):
        rendercallback()
        if self.visible == True:
            return True
        else:
            return False
    def rendercallback(self):
        #surcharge it in son's to add functionnality
        return True
    def togglevisible(self):
        self.visible = not self.visible
    def isvisible(self):
        return self.visible
    def pygame(self):
        return self.pygame
    def screen(self):
        return self.screen

###Board
class Board(Thing):
    def __init__(self,pygame,screen,x=0,y=0,z=0,w=7,h=6):
        super().__init__(pygame,screen,x,y,z)  
        #Number of columns and row
        self.w = w
        self.h = h
        #Size in pixel
        screenw,screenh  = Factory.windowsize()
        self.width = int(0.4*screenw)
        self.height = int(0.7*screenh)
        #margin left and top
        self.marginl = int((screenw-self.width))//2
        self.margint = int((screenh-self.height))//2
        #elt size
        self.tilesize = self.width//self.w
        #load assets
        self.tile_yellow = self.pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets','coin_yellow.png')).convert()
        self.tile_yellow = self.pygame.transform.scale(self.tile_yellow,(self.tilesize,self.tilesize))
        self.tile_red = self.pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets','coin_red.png')).convert()
        self.tile_red = self.pygame.transform.scale(self.tile_red,(self.tilesize,self.tilesize))
        self.tile_white = self.pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets','coin_white.png')).convert()
        self.tile_white = self.pygame.transform.scale(self.tile_white,(self.tilesize,self.tilesize))
        self.tile = [self.tile_white,self.tile_yellow,self.tile_red]
        # w columns and h rows
        #self.board = [[0,0,0,0,0,1],[0,0,0,0,0,2],[0,0,0,0,0,2],[0,0,0,0,0,2],[0,0,0,0,1,1],[0,0,0,0,1,2],[0,0,0,0,0,1]]
        self.board = [[0 for i in range(self.h)] for j in range(self.w)]

    #load 
    def load(self,board):
        #parse and construct the board
        return
        #self.logboard(board)
    #print the board on console 
    def logboard(self,board):
        print('')
        for j in range(self.h):  
            print("")
            for i in range(self.w):
                print(board[i][j],end=' ')
        print("")
    #set one case
    def setcase(self,w,h,s):
        self.board[w][h]=s
        
    #is the board full ?
    def isfull(self):
        for c in range(0,self.w):
            if whichrow(c) >= 0:
                return False
        return True
    #render the board on the screen
    def render(self):
        if self.isvisible():
            for i in range(self.w):
                for j in range(self.h):
                    case = self.board[i][j]
                    indice = 0

                    self.screen.blit(self.tile[case],(i*self.tilesize+self.marginl,j*self.tilesize+self.margint))

    #Diff entre deux boards
    def diff(self, otherboard):
        if len(self.board) != len(otherboard.board) or len(self.board[0]) != len(otherboard.board[0]):
            return False
        for row in range(otherboard):
            for col in range(otherboard):
                if otherboard.board[row][col] != self.board[row][col]:
                    False
        return True


##PlayerServer
class PlayerServer(Thing):
    def __init__(self,pygame,screen,board,client,position=0,x=0,player=1,playerturn=1):
        super().__init__(pygame,screen,x)
        self.pygame = pygame
        self.screen = screen
        self.client = client
        self.player = player
        self.position = position
        self.board = board
        self.playerturn = playerturn
        if self.playerturn == 0:
            self.togglevisible()
        self.screenw , self.screenh = Factory.windowsize()
        self.playersupport = [0]*self.board.w  #it is an array to choose the column to play
        self.playersupport[0]=1
        
        if player == 1:
            self.playerhand = self.pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets','arrow_p1.png')).convert()
        elif player == 2:
            self.playerhand = self.pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets','arrow_p2.png')).convert()
        elif player == 3:
            self.playerhand = self.pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets','arrow_p3.png')).convert()
        
        self.playerhand = self.pygame.transform.scale(self.playerhand,(self.board.tilesize,self.board.tilesize))
        self.width = int(0.4*self.screenw)
        self.height = self.board.tilesize

        self.x = int((self.screenw-self.width))//2
        self.y = 5

    def render(self):
        if(self.isvisible()):
            self.playerhand.set_alpha(255)
        else:
            self.playerhand.set_alpha(50)

        for i in range(self.board.w):
            if(self.playersupport[i] == 1):
                self.screen.blit(self.playerhand,(i*self.board.tilesize+self.x,self.y))
            if(self.playersupport[i] == 2):
                self.screen.blit(self.playerhand,(i*self.board.tilesize+self.x,self.y))

    #listen the server: if we receive board we fill it and we wait for the move instruction
    def listen(self):
        while True:    
            if self.client.listen() == "move":
                break
            elif self.client.listen() == "board":
                self.board.board = self.client.board

    #send your move to the server
    def send(self,mv):
        self.client.sendMove(mv)

    #setposition from outside
    def setposition(self,position):
        if position < 0 and position >= self.board.w:
            return False
        self.position = position
        index = self.playersupport.index(1)
        self.playersupport[index]=0
        self.playersupport[self.position]=1
        return True
    
        
    

##Player is the visible arrow which you can play
class Player(Thing):
    def __init__(self,pygame,screen,board,position=0,x=0,player=1,playerturn=1):
        super().__init__(pygame,screen,x)
        self.pygame = pygame
        self.screen = screen
        self.player = player
        self.position = position
        self.board = board
        self.playerturn = playerturn
        if self.playerturn == 0:
            self.togglevisible()
        self.screenw , self.screenh = Factory.windowsize()
        self.playersupport = [0]*self.board.w  #it is an array to choose the column to play
        self.playersupport[0]=1
        
        if player == 1:
            self.playerhand = self.pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets','arrow_p1.png')).convert()
        elif player == 2:
            self.playerhand = self.pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets','arrow_p2.png')).convert()
        elif player == 3:
            self.playerhand = self.pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets','arrow_p3.png')).convert()
        
        self.playerhand = self.pygame.transform.scale(self.playerhand,(self.board.tilesize,self.board.tilesize))
        self.width = int(0.4*self.screenw)
        self.height = self.board.tilesize

        self.x = int((self.screenw-self.width))//2
        self.y = 5
    def render(self):
        if(self.isvisible()):
            self.playerhand.set_alpha(255)
        else:
            self.playerhand.set_alpha(50)

        for i in range(self.board.w):
            if(self.playersupport[i] == 1):
                self.screen.blit(self.playerhand,(i*self.board.tilesize+self.x,self.y))
            if(self.playersupport[i] == 2):
                self.screen.blit(self.playerhand,(i*self.board.tilesize+self.x,self.y))

    #move player left or right
    def move(self,direction):
        if self.playerturn == 0:
            return False
        if direction >= 0:
            self.position = (self.position+1)%self.board.w
        else:
            if self.position == 0:
                self.position = self.board.w-1
            else:
                self.position = self.position-1
        index = self.playersupport.index(1)
        self.playersupport[index]=0
        self.playersupport[self.position]=1
        return True
    #move the enemy's cursor
    def moveenemy(self,newpos):
        index = self.playersupport.index(2)
        self.playersupport[index] = 0
        self.playersupport[newpos] = 2

    #setposition from outside
    def setposition(self,position):
        if position < 0 and position >= self.board.w:
            return False
        self.position = position
        return True
    #commit the choice
    def play(self):
        if self.playerturn == 0:
            return False
        hplay = Factory.whichrow(self.board.board[self.position])
        if(hplay < 0):
            return False
        if self.player == 1:
            coin = BoardBox.PLAYER1.value
        elif self.player == 2:
            coin = BoardBox.PLAYER2.value
        self.board.setcase(self.position,hplay,coin)
        
        return True
    #set the turn off
    def toggleturn(self):
        self.playerturn= (self.playerturn +1)%2
        self.togglevisible()
    


##Gui
class Gui(Thing):
    def __init__(self,screen,pygame,x=0,y=0,z=0):
        super().__init__(pygame,screen,x,y,z)
###Text
class Text(Gui):
    def __init__(self,pygame,screen,x=0,y=0,z=0,text="",font="",size=18):
        super().__init__(pygame,screen,x,y,z)
        self.font = font
        self.text = text
        self.size=size

####Player name
class PlayerGUI(Text):
    def __init__(self,pygame,screen,playername,score,playernumber,font="visitor2.ttf",x=0,y=0,z=0,size=18):
        super().__init__(pygame,screen,x,y,z,playername,font,32)
        #font
        self.pygame = pygame # i don't know why but in the great mother classes subobject was not initialized
        self.screen = screen
        font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets','visitor2.ttf')
        self.fontobj = self.pygame.font.Font(font_path, self.size)
        #...
        self.textw, self.texth = self.fontobj.size(self.text)
        self.w = self.textw+2+15
        self.h = self.texth
        self.score = score
        self.playernumber = playernumber
        self.screenw , self.screenh = Factory.windowsize()
        #load assets
        if self.playernumber == 0:
            rectpath = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets','rect_yellow.png')
        elif self.playernumber == 1:
            rectpath = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets','rect_red.png')
        elif self.playernumber == 2:
            rectpath = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets','rect_yellow.png')
        self.rect = self.pygame.image.load(rectpath).convert()
        self.rect = self.pygame.transform.scale(self.rect,(15,15))
        #left or right ?
        if playernumber == 0:
            self.x = int(self.screenw*0.3 - self.w)//2
        elif playernumber == 1:
            self.x = int(self.screenw*0.3 - self.w)//2 + int(self.screenw*0.4+self.screenw*0.3)
        self.y = int(self.screenh - self.h)//2 - 20
    #display the object
    def render(self):
        x = self.x
        y = self.y
        
        scoretext = str(self.score)
        if self.isvisible():
            self.screen.blit(self.rect,(x,y+5))
            playername = self.fontobj.render(self.text,1,(255,255,255))
            self.screen.blit(playername,(x+5+15,y))

            self.textw, self.texth = self.fontobj.size(scoretext)
            score = self.fontobj.render(scoretext,1,(255,255,255))

            scorex,scorey = self.fontobj.size(scoretext)
            
            if self.playernumber == 0:
                x= int(self.screenw*0.3-scorex)//2
            elif self.playernumber == 1:
                x = int(self.screenw*0.3-scorex)//2 + int(self.screenw*0.4+self.screenw*0.3)
            self.screen.blit(score,(x,y+scorey))

###Image for decoration
class Img(Gui):
    def __init__(self,pygame,screen,x=0,y=0,z=0,img=""):
        super().__init__(pygame,x,y,z)
        self.img=img

###Lobby to see players and score
class Lobby(Gui):
    def __init__(self,pygame,screen,players=[],x=0,y=0,z=0):
        super().__init__(pygame,screen,x,y,z)
        self.screenw, self.screenh = Factory.windowsize()
        self.pygame = pygame
        self.screen = screen
        #size and position of the lobby
        self.w = int(0.4*self.screenw)
        self.h = int(0.8*self.screenh)
        self.x = (self.screenw-self.w)//2
        self.y = (self.screenh-self.h)//2
        #init p and q  
        self.pinit = 0
        self.qinit = 13
        #p and q are the index of the begin and end of the visible array
        self.p = self.pinit
        self.q = self.qinit
        #i is the select index, it will select the player in the visible array
        self.i = 0
        #invisible array (out of screen)
        self.players = players 
        self.n = len(players)
        if self.q >= self.n:
            self.q = self.n
        #visible array, we use it to display the player in the screen
        self.playersdisplay = self.players[self.p:self.q]
        #text
        self.fontsize = 32
        font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets','visitor2.ttf')
        self.fontobj = self.pygame.font.Font(font_path, self.fontsize)
        #just calculate the height in pixel of the font
        tmp,self.texth = self.fontobj.size("omagad")
        self.arrow = self.pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets','arrow_right.png')).convert()
        self.arrow = self.pygame.transform.scale(self.arrow,(self.texth,self.texth))
        self.choosenroom = ""
        #...
        
    #fill the visible player list
    def fillplayers(self):
        if self.p>=0 and self.q<=self.n:
            self.playersdisplay = self.players[self.p:self.q]
            return True
        return False

    #render arrow
    def renderarrow(self):
        self.screen.blit(self.arrow,(self.x-32,self.i*self.texth+2+self.y))
        return
    #move arrow down
    def arrowdown(self):
        if self.i < self.q-self.p-1:
            self.i+=1
        else:
            if self.q < self.n:
                self.p+=1
                self.q+=1
                self.fillplayers()
    #move arrow up
    def arrowup(self):
        if self.p == 0 and self.i != 0:
            self.i-=1
        if self.p != 0:
            if self.i == 0:
                self.p-=1
                self.q-=1
                self.fillplayers()
            else:
                self.i-=1
    #ask to a player if he wanna play
    def ask(self,index):
        print(self.playersdisplay[index][0])
        self.choosenroom = self.playersdisplay[index][0]
        return self.playersdisplay[index][1][0]
    #refresh the players list
    def load(self,players):
        print("loading players")
        self.players = players
        self.n = len(self.players)
        self.p = self.pinit
        self.q = self.qinit
        if self.q >= self.n:
            self.q = self.n
        self.fillplayers()
        return
    #game loop is here to let the player choose his enemy. it returns the name of the player
    def loopchoice(self):
        while True:
            event = self.pygame.event.wait()
            self.screen.fill((0, 0, 0))
            if event.type == self.pygame.QUIT:
                self.pygame.quit()
                break
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.arrowup()
                elif event.key == K_DOWN:
                    self.arrowdown()
                elif event.key == K_RETURN or event.key == K_KP_ENTER:
                    return self.ask(self.i)
                elif event.key == K_c:
                    self.choosenroom = -1
                    return ""
                elif event.key == K_ESCAPE:
                    self.pygame.quit()
                    break
            self.render()
            #refresh screen
            self.pygame.display.flip()
    def render(self):
        size = self.q-self.p
        #render lobby
        for j in range(size):
            roomsplayers = functools.reduce(lambda x,y:str(x)+" "+str(y),self.playersdisplay[j][1])
            playername = self.fontobj.render(str(self.playersdisplay[j][0])+': '+roomsplayers,1,(255,255,255))
            self.screen.blit(playername,(self.x,self.y+j*self.texth+2))
        #render arrow
        self.renderarrow()
        return
#This class is the arbitrator of the four on the line (p4)
class GameRuler:
    def __init__(self,pygame,screen,playerlist=[]):
        self.rooms = []
        self.gamestatus = 0
        self.pygame = pygame
        self.playerlist = playerlist
        self.screen = screen
        self.pygame.display.set_caption('Pyssance 4')
        self.turn = 0
        #set the Object
        self.board = Board(self.pygame,self.screen)
        self.w = self.board.w
        self.h = self.board.h
        self.nbplayers = len(playerlist)
        #online case
        self.playerlist =playerlist
        if not playerlist:
            self.nbplayers = 2
        self.players = []
        self.playersgui = []
        
        #self.board = Board(self.pygame,self.screen)
        #self.p = Player(self.pygame,self.screen,self.board)
        self.clock = pygame.time.Clock()
    #change the turn, circular on the list
    def initboard(self,w=7,h=6):
        self.board = Board(self.pygame,self.screen,0,0,0,w,h)
        self.w = self.board.w
        self.h = self.board.h
        if  len(self.playerlist) == 0:
            #online case
            self.nbplayers = 2
        else:
            self.nbplayers = len(self.playerlist)
        
        
    def changeturn(self):
        self.turn = (self.turn+1)%self.nbplayers
    #check if the player (tile) is the winner
    def iswinner(self,board,tile):
        # check horizontal spaces
        for y in range(self.h):
            for x in range(self.w - 3):
                if board[x][y] == tile and board[x+1][y] == tile and board[x+2][y] == tile and board[x+3][y] == tile:
                    return True
        # check vertical spaces
        for x in range(self.w):
            for y in range(self.h - 3):
                if board[x][y] == tile and board[x][y+1] == tile and board[x][y+2] == tile and board[x][y+3] == tile:
                    return True
        # check / diagonal spaces
        for x in range(self.w - 3):
            for y in range(3, self.h):
                if board[x][y] == tile and board[x+1][y-1] == tile and board[x+2][y-2] == tile and board[x+3][y-3] == tile:
                    return True
        # check \ diagonal spaces
        for x in range(self.w - 3):
            for y in range(self.h - 3):
                if board[x][y] == tile and board[x+1][y+1] == tile and board[x+2][y+2] == tile and board[x+3][y+3] == tile:
                    return True
        return False


    #main loop online
    def runonline(self,user='coucou',passwd='coucou'):
        username = user
        password = passwd   
        client = Client(username,password)
        self.rooms = client.rooms
        #choose a room
        lobby = Lobby(self.pygame,self.screen,self.rooms)
        enemyname = lobby.loopchoice()
        lobby.choosenroom
        # -1 pour creer une room
        actualroom = client.initRoom(lobby.choosenroom)
        #get the color
        mycolor = client.color
        starter = client.begin
        print("MG: color:"+mycolor+" begin:"+starter)
        ibegin = 0
        if mycolor == starter:
            ibegin = 1
        ebegin = (ibegin + 1)%2
        self.turn = ibegin
        
        #initialize the online game with the information of the server
        while True:
            rep = client.listen()
            print("MG "+rep+" ", end='')
            if rep == "move":
                break
            elif rep == "board":
                self.screen.fill((0, 0, 0))
                wi = client.board[0]
                he = client.board[1]
                self.initboard(wi,he)
                self.board.board = client.board[2]
                me = Player(self.pygame,self.screen,self.board,0,0,ibegin+1,ibegin)
                megui = PlayerGUI(self.pygame,self.screen,username,str('score: 0000'),ibegin)
                enemy = PlayerServer(self.pygame,self.screen,self.board,client,0,0,ebegin+1,ebegin)
                if lobby.choosenroom >= 0:
                    enemyname = "Player 2"
                enemygui = PlayerGUI(self.pygame,self.screen,enemyname,str('score: 0000'),ebegin)
                me.render()
                megui.render()
                enemy.render()
                enemygui.render()
                self.board.render()
                self.pygame.display.flip()
        ############## 19h30 ######################
        #start the game loop
        while True:
            print("MG: jeu")
            self.screen.fill((0, 0, 0))
            #if this client begins
            if self.turn == 0:
                event = self.pygame.event.wait()
                if event.type == self.pygame.QUIT:
                    self.pygame.quit()
                    break
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        me.move(-1)
                    elif event.key == K_RIGHT:
                        me.move(1)
                    elif event.key == K_DOWN:
                        if me.play():
                            #the actual player gives the hand to the other player
                            me.toggleturn()
                            if self.iswinner(self.board.board,me.player):
                                self.gamestatus = 1
                                winner = username
                            else:
                                self.changeturn()
                                me.toggleturn()
                                #send the position
                                enemy.send(me.position)
                    elif event.key == K_ESCAPE:
                        self.pygame.quit()
                        break
            #if enemy begins
            elif self.turn == 1:
                enemy.listen()
                if self.iswinner(self.board.board,me.player):
                    self.gamestatus = 1
                    winner = enemyname
                else:
                    self.changeturn()
                    me.toggleturn()
            #refresh elt
            if self.gamestatus == 0:
                me.render()
                megui.render()
                enemy.render()
                enemygui.render()
                self.board.render()
            if self.gamestatus == 1:
                Factory.gameoverscreen(self.pygame,self.screen,winner+" is the winner !")
            #refresh screen
            self.pygame.display.flip()
            #free proc
            self.clock.tick(10)
    
    #main loop local
    def runlocal(self):
        
        self.initboard()
        for i in range(self.nbplayers):
            #le premier joueur de la liste commence
            if i == 0:
                playerturn = 1
            else:
                playerturn = 0
            self.players.append(Player(self.pygame,self.screen,self.board,0,0,i+1,playerturn))
            self.playersgui.append(PlayerGUI(self.pygame,self.screen,self.playerlist[i][0],str(self.playerlist[i][1]),i))
        while True:
            
            event = self.pygame.event.wait()
            self.screen.fill((0, 0, 0))
            # Leave the game if press Quit
            if event.type == self.pygame.QUIT:
                self.pygame.quit()
                break
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.players[self.turn].move(-1)
                elif event.key == K_RIGHT:
                    self.players[self.turn].move(1)
                elif event.key == K_DOWN:
                    if self.players[self.turn].play():
                        #the actual player gives the hand to the new player
                        self.players[self.turn].toggleturn()
                        if self.iswinner(self.board.board,self.players[self.turn].player):
                            self.gamestatus = 1
                        else:
                            self.changeturn()
                            self.players[self.turn].toggleturn()
                    
                elif event.key == K_ESCAPE:
                    self.pygame.quit()
                    break
            #refresh elt
            if self.gamestatus == 0:
                for i in range(self.nbplayers):
                    self.players[i].render()
                    self.playersgui[i].render()
                self.board.render()
            if self.gamestatus == 1:
                Factory.gameoverscreen(self.pygame,self.screen,self.playersgui[self.turn].text+" is the winner !")
            #refresh screen
            self.pygame.display.flip()
            #wait n second
            self.clock.tick(10)

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(Factory.windowsize(),HWSURFACE|DOUBLEBUF)#RESIZABLE
    
    #game = GameRuler(pygame,screen,[('Player 1',320),('Player 2','540')])
    #game.runlocal()
    #pygame,screen,x=0,y=0,z=0,players=[]
    #players = [['ROOM'+str(i),["player"+str(j) for j in range(2) ]] for i in range(40)]
    #lobby = Lobby(pygame,screen,players)
    #lobby.loopchoice()

    #test online
    game = GameRuler(pygame,screen)
    game.runonline()

if __name__ == '__main__':
    main()