#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
sys.path.append(os.path.join(dirname, 'Joueurs'))
import joueur_humain, joueur_random, joueur_minimax_ab, MASTER, MCTS
import game
import pygame
from squadro import WIDTH, HEIGHT
import main


##################################################################################################
##################                      SELECTION DES JOUEURS                   ##################
##################################################################################################
def selection():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    font = pygame.font.SysFont("Constantia", 30)

    #define colours
    red = (255, 0, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)

    #define global variable
    global clicked
    clicked = False
    counter = 0

    class button():
        #colours for button and text
        button_col = (255, 0, 0)
        hover_col = (75, 225, 255)
        click_col = (50, 150, 255)
        text_col = black
        width = 240
        height = 70

        def __init__(self, x, y, text, modules):
            self.x = x
            self.y = y
            self.text = text
            self.modules = modules

        def draw_button(self):
            global clicked
            action = False

            #get mouse position
            pos = pygame.mouse.get_pos()

            #create pygame Rect object for the button
            button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

            #check mouseover and clicked conditions
            if button_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    clicked = True
                    pygame.draw.rect(screen, self.click_col, button_rect)
                elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                    clicked = False
                    action = True
                else:
                    pygame.draw.rect(screen, self.hover_col, button_rect)
            else:
                pygame.draw.rect(screen, self.button_col, button_rect)

            #add shading to button
            pygame.draw.line(screen, white, (self.x, self.y), (self.x + self.width, self.y), 2)
            pygame.draw.line(screen, white, (self.x, self.y), (self.x, self.y + self.height), 2)
            pygame.draw.line(screen, black, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
            pygame.draw.line(screen, black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

            #add text to button
            text_img = font.render(self.text, True, self.text_col)
            text_len = text_img.get_width()
            screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))
            return action

    button1 = button(100, 100, "Human v Human", (joueur_humain, joueur_humain))
    button2 = button(350, 100, "Human v AB", (joueur_humain, MASTER))
    button3 = button(100, 250, "AB v Human", (MASTER, joueur_humain))
    button4 = button(350, 250, "Human v MCTS", (joueur_humain, MCTS))
    button5 = button(100, 400, "MCTS v Human", (MCTS, joueur_humain))
    button6 = button(350, 400, "MCTS v AB", (MCTS, MASTER))
    button7 = button(100, 550, "AB v MCTS", (MASTER, MCTS))
    button8 = button(350, 550, "AB v AB", (MASTER, MASTER))

    buttons = [button1, button2, button3, button4, button5, button6, button7, button8]

    run = True
    while run:
        screen.fill(black)

        for button in buttons:
            if button.draw_button():
                game.joueur1 = button.modules[0]
                game.joueur2 = button.modules[1]
                main.main()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit(0)

        pygame.display.update()