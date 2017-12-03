import pygame
import pygame.color
import os
from pygame.locals import *
WINDOW_SIZE = 800, 400

def main():
    ## Load PigGame
    pygame.init()

    # Initialize PyGame
    screen = pygame.display.set_mode(WINDOW_SIZE,HWSURFACE|DOUBLEBUF)#RESIZABLE
    pygame.display.set_caption('Puissance 4')
    #background = pygame.image.load('background.jpg')

    tilesize = 55
    rectsize = 15
    marginleft = 205
    margintop = 40
    tile_yellow = pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'src','assets','coin_yellow.png')).convert()
    tile_yellow = pygame.transform.scale(tile_yellow,(tilesize,tilesize))
    tile_red = pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'src','assets','coin_red.png')).convert()
    tile_red = pygame.transform.scale(tile_red,(tilesize,tilesize))
    tile_white = pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'src','assets','coin_white.png')).convert()
    tile_white = pygame.transform.scale(tile_white,(tilesize,tilesize))

    rectyellow =pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'src','assets','rect_yellow.png')).convert()
    rectred =pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'src','assets','rect_red.png')).convert()
    rectyellow = pygame.transform.scale(rectyellow,(rectsize,rectsize))
    rectred = pygame.transform.scale(rectred,(rectsize,rectsize))
    board = [[0]*6]*7
    

    board = [[0,0,0,0,0,1],[0,0,0,0,0,2],[0,0,0,0,0,2],[0,0,0,0,0,2],[0,0,0,0,1,1],[0,0,0,0,1,2],[0,0,0,0,0,1]]
    for i in range(len(board)):
        for j in range(len(board[0])):
            if(board[i][j] == 0):
                screen.blit(tile_white,(i*tilesize+marginleft,j*tilesize+margintop))
            if(board[i][j] == 1):
                screen.blit(tile_yellow,(i*tilesize+marginleft,j*tilesize+margintop))
            if(board[i][j] == 2):
                screen.blit(tile_red,(i*tilesize+marginleft,j*tilesize+margintop))

    #font
    pygame.font.init() ##################!!!!!!!!!!!!!!!
    font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'src','assets','visitor2.ttf')
    font_size = 32
    fontobj = pygame.font.Font(font_path, font_size)
   

    score = fontobj.render("1651",1,(255,255,255))
    screen.blit(score,(50+10+9,160+32))
    score = fontobj.render("1490",1,(255,255,255))
    screen.blit(score,(WINDOW_SIZE[0]-160+5+10+9,160+32))
    player2text = fontobj.render("Player 2",1,(255,255,255))
    player1text = fontobj.render("Player 1",1,(255,255,255))
    screen.blit(player1text,(50,160))
    player2text = fontobj.render("Player 2",1,(255,255,255))
    screen.blit(player2text,(WINDOW_SIZE[0]-160+5,160))
    screen.blit(rectyellow,(28,165))
    screen.blit(rectred,(WINDOW_SIZE[0]-160-7-rectsize+5,165))

    pygame.display.flip()

    print(os.path.dirname(os.path.realpath(__file__)))
    
    
    # Main game loop
    while True:
        event = pygame.event.wait()
        
        # Leave the game if press Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            break


if __name__ == '__main__':
    main()
