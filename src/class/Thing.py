from enum import Enum
import os

import pygame
import pygame.color
import os
from pygame.locals import *

#Factory


#return the line to play if the column is playable or a number lower than 0 if it is not playable
class Factory():
    #whichrow is playable in this column
    def whichrow(column):
        for hplay in reversed(range(0,len(column))):
            if column[hplay] == BoardBox.EMPTY:
                return hplay
        return -1
    def bloc2pixel():
        return
    def pixel2bloc():
        return
    #window size !
    def windowsize():
        return 800, 400

#Enumeration

#BoardBox is the status of the case
class BoardBox(Enum):
    EMPTY = 0
    PLAYER1 = 1 #BB2330 red
    PLAYER2 = 2 #FDC500 yellow

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
        print(self.marginl)
        self.margint = int((screenh-self.height))//2
        print(self.margint)
        #elt size
        self.tilesize = int(self.width/self.w)
        #load assets
        self.tile_yellow = self.pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets','coin_yellow.png')).convert()
        self.tile_yellow = self.pygame.transform.scale(self.tile_yellow,(self.tilesize,self.tilesize))
        self.tile_red = self.pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets','coin_red.png')).convert()
        self.tile_red = self.pygame.transform.scale(self.tile_red,(self.tilesize,self.tilesize))
        self.tile_white = self.pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets','coin_white.png')).convert()
        self.tile_white = self.pygame.transform.scale(self.tile_white,(self.tilesize,self.tilesize))
        # w columns and h rows
        self.board = [[BoardBox.EMPTY]*self.h]*self.w
        self.board = [[0,0,0,0,0,1],[0,0,0,0,0,2],[0,0,0,0,0,2],[0,0,0,0,0,2],[0,0,0,0,1,1],[0,0,0,0,1,2],[0,0,0,0,0,1]]
    #load 
    def load(self,board=[]):
        if len(board)>0:
            self.board = board
        #parse and construct the board
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if(board[i][j] == 0):
                    self.screen.blit(self.tile_white,(i*self.tilesize+self.marginl,j*self.tilesize+self.margint))
                if(board[i][j] == 1):
                    self.screen.blit(self.tile_yellow,(i*self.tilesize+self.marginl,j*self.tilesize+self.margint))
                if(board[i][j] == 2):
                    self.screen.blit(self.tile_red,(i*self.tilesize+self.marginl,j*self.tilesize+self.margint))
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
            self.load(self.board)
            return


class Player(Thing):
    def __init__(self,pygame,screen,board,position=0,x=0,player=1,playerturn=0):
        super().__init__(pygame,screen,x)
        self.player = player
        self.position = position
        self.board = board
        self.playerturn = playerturn
        if self.playerturn == 0:
            self.togglevisible()

    #move player left or right
    def move(self,direction):
        if direction >= 0:
            self.position = (self.position+1)%self.board.w
        else:
            if self.position == 0:
                self.position = board.w-1
            else:
                self.position = self.position-1
    #setposition from outside
    def setposition(self,position):
        if position < 0 and position >= self.board.w:
            return False
        self.position = position
        return True
    #commit the choice
    def play(self):
        if playerturn == 0:
            return False
        hplay = Factory.whichrow(self.board.board[self.position])
        if(hplay < 0):
            return False
        self.board.setcase(self.position,hplay,BoardBox.PLAYER1)
        return True
    def toggleturn(self):
        numberofplayer = 2
        self.playerturn= (self.playerturn +1)%numberofplayer



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
        self.fontobj = self.pygame.font.Font(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets',self.font), self.size)      
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
        self.rect = self.pygame.image.load(rectpath).convert()
        self.rect = self.pygame.transform.scale(self.rect,(15,15))
        #left or right ?
        if playernumber == 0:
            self.x = int(self.screenw*0.3 - self.w)//2
        elif playernumber == 1:
            self.x = int(self.screenw*0.3 - self.w)//2 + int(self.w*0.4)
        self.y = int(self.screenh - self.h)//2
    #display the object
    def render(self):
        x = self.x
        y = self.y
        scoretext=2150
        scoretext = str(scoretext)
        if self.isvisible():
            self.screen.blit(self.rect,(x,y))
            playername = fontobj.render(self.text,1,(255,255,255))
            self.screen.blit(playername,(x+2+15,y))

            self.textw, self.texth = self.font.size(scoretext)
            score = fontobj.render(scoretext,1,(255,255,255))

            scorex,scorey = self.fontobj.size(scoretext)
            x= int(self.screenw*0.3-scorex)//2
            self.screen.blit(score,(x,y+scorey))

###Image for decoration
class Img(Gui):
    def __init__(self,pygame,screen,x=0,y=0,z=0,img=""):
        super().__init__(pygame,x,y,z)
        self.img=img

###Lobby to see players and score
class Lobby(Gui):
    def __init__(self,pygame,screen,x=0,y=0,z=0,players={}):
        super().__init__(pygame,screen,x,y,z)
        self.players = players
    #ask to a player if he wanna play
    def ask(self,playerid):
        return
    #refresh the players list
    def load(self,players):
        return
    def log(self,message):
        return


def run():
    #initialize
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(Factory.windowsize(),HWSURFACE|DOUBLEBUF)#RESIZABLE
    pygame.display.set_caption('Puissance 4')

    #set the Object
    #background = pygame.image.load('background.jpg')
    board = Board(pygame,screen)
    p = Player(pygame,screen,board)
    p.move(1)
    print(p.position)
    pygame.display.flip()

    #less energy !
    clock = pygame.time.Clock()
    while True:
        event = pygame.event.wait()
        screen.fill((0, 0, 0))
        board.render()
        
        # Leave the game if press Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            break

        #render all
        pygame.display.flip()

        #wait n second
        clock.tick(60)

#test run
run()