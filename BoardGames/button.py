#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame

font = pygame.font.SysFont('Constantia', 30)

#define colours
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Button():
        #colours for button and text
        button_col = RED
        hover_col = (75, 225, 255)
        click_col = (50, 150, 255)
        text_col = BLACK
        width = 240
        height = 70

        def __init__(self, x, y, text, modules=None, clicked=False):
            self.x = x
            self.y = y
            self.text = text
            self.modules = modules
            self.clicked = clicked

        def draw_button(self, screen):
            action = False

            #get mouse position
            pos = pygame.mouse.get_pos()

            #create pygame Rect object for the button
            button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

            #check mouseover and clicked conditions
            if button_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0]:
                    self.clicked = True
                    pygame.draw.rect(screen, self.click_col, button_rect)
                elif self.clicked:
                    self.clicked = False
                    action = True
                else:
                    pygame.draw.rect(screen, self.hover_col, button_rect)
            else:
                pygame.draw.rect(screen, self.button_col, button_rect)

            #add shading to button
            pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x + self.width, self.y), 2)
            pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x, self.y + self.height), 2)
            pygame.draw.line(screen, BLACK, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
            pygame.draw.line(screen, BLACK, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

            #add text to button
            text_img = font.render(self.text, True, self.text_col)
            text_len = text_img.get_width()
            screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))
            return action
