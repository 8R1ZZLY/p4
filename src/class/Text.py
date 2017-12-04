
def run():
    #initialize
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(Factory.windowsize(),HWSURFACE|DOUBLEBUF)#RESIZABLE
    pygame.display.set_caption('Puissance 4')

    font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','assets','visitor2.ttf')
    font_size = 32
    fontobj = pygame.font.Font(font_path, font_size)

    #set the Object
    board = Board(pygame,screen)
    p = Player(pygame,screen,board)
    playergui1 = PlayerGUI(pygame,screen,"player 1","1367",0)
    playergui2 = PlayerGUI(pygame,screen,"player 2","1517",1)

    #first display
    pygame.display.flip()

    #less energy !
    clock = pygame.time.Clock()
    while True:
        event = pygame.event.wait()
        screen.fill((0, 0, 0))
        
        # Leave the game if press Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                p.move(-1)
            elif event.key == K_RIGHT:
                p.move(1)
            elif event.key == K_DOWN:
                p.play()
            elif event.key == K_ESCAPE:
                pygame.quit()
                break

        #refresh elt
        board.render()
        playergui1.render()
        playergui2.render()
        p.render()
        #render all
        pygame.display.flip()

        #wait n second
        clock.tick(10)