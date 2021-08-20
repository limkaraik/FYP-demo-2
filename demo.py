import pygame
import time
pygame.init()
from graph import Graph
from misc import Misc
from data import DATA
from backend.agent import *
from backend.env import Env
from backend.data import *

WINDOW_SIZE = (1200,800)
BACKGROUND = (255,255,255)


#Create the screen
screen = pygame.display.set_mode(WINDOW_SIZE)

#title and icon
pygame.display.set_caption("Demo")

#misc functions
misc = Misc(screen)


def play():
    #env
    environment=Env('yishun')
    goals = EXITS
    theif = INIT_LOC[0]
    defenders = DEFENDER_INIT[0]
    limit=TIME_HORIZON
    gameover = False

     #init defender
    defender=AgentEvalYishun()

    #init graph
    graph = Graph(screen,theif,defenders,goals)

    game_state=environment.reset()

    #main loop
    running = True

    while running:
        screen.fill(BACKGROUND)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                #player select where to move for thief
                turn, attacker_a =graph.check_move()
                if turn:
                    #police move base on algo here
                    defender_obs, attacker_obs = game_state.obs()
                    def_current_legal_action, att_current_legal_action = game_state.legal_action()
                    defender_a = defender.select_action([defender_obs], [def_current_legal_action])
                    game_state = environment.simu_step(defender_a, attacker_a)
                    #move police in graph
                    graph.thief_move()
                    graph.police_move(defender_a)
                    limit-=1
                #after police has moved etc....
                graph.reset_move()
            
            elif event.type == pygame.QUIT:
                running = False
            
        
        #check who win
        result = graph.checkWin()
        if result ==1: #player win
            misc.message_to_screen('Player wins!',(255,0,0),0,0,'large')
            m= misc.button("Restart",850,320,150,150,(55,255,255),(0,255,0))
            gameover = True
            if m:
                return
        elif result ==2: #police win
            #draw game boundary
            pygame.draw.rect(screen,(0,0,0),(50,50,700,700),1)
            #display graph
            graph.display_lose()
            #display turns left
            misc.message_to_screen('You got caught! Player lose...',(0,0,255),330,-200,'small')
            m1= misc.button("Restart",850,320,150,150,(55,255,255),(0,255,0))
            gameover = True
            if m1:
                return
        elif limit==0:
            misc.message_to_screen('Time Out! Player Lose...',(0,255,0),0,0,'large')
            m2= misc.button("Restart",500,500,150,150,(55,255,255),(0,255,0))
            gameover = True
            if m2:
                return
        else:
            #display graph
            graph.display()
            #display turns left
            misc.message_to_screen('Turns left: '+str(limit),(0,0,255),310,-200,'medium')
            m= misc.button("Return",850,320,150,150,(55,255,255),(0,255,0))
            if m:
                return
        pygame.display.update()

def main():
    #main loop
    running = True
    while running:
        screen.fill(BACKGROUND)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #select difficulty
        misc.message_to_screen("Click Start to play!",(0,0,0),0,-150,'large')
        m= misc.button("Start",500,350,150,150,(55,255,255),(0,255,0))
        if m:
            play()
        pygame.display.update()

main()