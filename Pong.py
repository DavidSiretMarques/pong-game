"""Pong game by Thor-pedo
Simple version of the pong game, without AI.

Player 1 uses arrows, player 2 uses wasd
 """

import sys, pygame, random, time

#function that loads images to the screen in the position given
def loadimage(imagename,x,y):
    img = pygame.image.load(f".\Proyectos varios python\Pong\{imagename}").convert_alpha() #Load image and keep only the interesting parts
    imgrect = img.get_rect() #get the rect measurements for the img
    imgrect.center = (x,y)
    return img, imgrect

#randomize the direction the ball starts with, so it won't always start to the same side
def randomdir():
    if random.random() < 0.5: 
        return -1
    else:
        return 1

        
#main program: Pong game, the Idea is to be able to control both players, I'll add an AI for 1 player later on

def main():    

    #Restarting the game with new random speed 
    def restart():
        time.sleep(1)
        ballrect.center = (width/2,height/2)
        speed = [3*randomdir(), 3*randomdir()]
        score = [0,0]
        return speed, score
    
    #Blits the text for the winner
    def winner(i):
        wintext = font.render(f"The winner is player {i+1}. Press R to restart ",True,(0,0,0))
        wintextrect = wintext.get_rect()
        wintextrect.center = (width/2,height/2)
        screen.fill((255,255,255))
        screen.blit(text,textrect)
        screen.blit(wintext,wintextrect)
        pygame.display.flip()

    pygame.init()

    #constants
    width, height = pygame.display.get_desktop_sizes()[0]
    speed = [3*randomdir(), 3*randomdir()]
    score = [0,0]
    #set screen(window)
    screen = pygame.display.set_mode((width-100,height-50))
    #resetting width and height to fit the screen size
    width, height = pygame.display.get_window_size()
    # load ball and put ball in screen
    ball,ballrect = loadimage("circle.png",width/2,height/2)
    #load and put player 1 in screen
    player1, player1rect = loadimage("rectangle-player.png",0,height/2)
    #load and put player 1 in screen
    player2, player2rect = loadimage("rectangle-player.png",width,height/2)
    #Put text
    font = pygame.font.SysFont(None, 50)

    #making sounds
    pongsound = pygame.mixer.Sound(".\Proyectos varios python\Pong\pong-ball.flac")
    loosersound = pygame.mixer.Sound(".\Proyectos varios python\Pong\CSS-looser.wav")
    #making the sounds sound
    def pong_sound():
        pygame.mixer.Sound.play(pongsound)
    
    def looser_sound():
        pygame.mixer.Sound.play(loosersound)



    #Main loop of the game
    while True:

        #Events for interacting with the game
        for event in pygame.event.get():
            #push the x or the esc button to exit
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE] : sys.exit()

            #Push the space button to pause
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if speed != [0,0]:
                       v, speed = speed, [0,0]
                    else:
                        speed = v
        
        #render text to show stuff
        text = font.render(f"{score[1]}  {score[0]}",True,(0,0,0))
        textrect = text.get_rect()
        textrect.center = (width/2,20)
        
        #Restarting game
        if pygame.key.get_pressed()[pygame.K_r]: speed, score = restart()
        
        #Moving player 1
        if pygame.key.get_pressed()[pygame.K_s]: 
            if player1rect.bottom <= height: player1rect = player1rect.move(0,2)
        if pygame.key.get_pressed()[pygame.K_w]: 
            if player1rect.top >= 0: player1rect = player1rect.move(0,-2)
        
        #Moving player 2
        if pygame.key.get_pressed()[pygame.K_DOWN]: 
            if player2rect.bottom <= height: player2rect = player2rect.move(0,2)
        if pygame.key.get_pressed()[pygame.K_UP]: 
            if player2rect.top >= 0: player2rect = player2rect.move(0,-2)
        
        #move the ball
        ballrect = ballrect.move(speed)

        #make the ball bounce off the players
        if (ballrect.left <= player1rect.right and ballrect.bottom >= player1rect.top and ballrect.top <= player1rect.bottom) or (ballrect.right >= player2rect.left and ballrect.bottom >= player2rect.top and ballrect.top <= player2rect.bottom):
            speed[0] = -speed[0]
            pong_sound()
        #if players do not make it bounce, add score
        elif ballrect.left < 0 or ballrect.right > width:
            if ballrect.left <= player1rect.right:
                score[0] += 1
                looser_sound()
            elif ballrect.right >= player2rect.left:
                score[1] += 1
                looser_sound()
            speed, _ = restart()
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]
            pong_sound()        
        #End game if score reaches 10 and keep playing if not
        if score [0] >= 10: 
            winner(1)
        elif score [1] >= 10: 
            winner(0)
        else:
            #Paint everything to the screen
            screen.fill((255,255,255))
        
            #draw center line
            pygame.draw.lines(screen,(0,0,0),False,[(width/2,0),(width/2,height)], width = 4)
            
            #draw other stuff
            screen.blit(text,textrect)
            screen.blit(ball, ballrect)
            screen.blit(player1,player1rect)
            screen.blit(player2,player2rect)
            
            #update display
            pygame.display.flip()

#check if it's running as a script
if __name__=='__main__':
    main()
