#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import sys
import os
dirname = os.path.dirname(__file__)


##################################################################################################
##################                      SELECTION DES JEUX                      ##################
##################################################################################################
def selection():
	pygame.init()

	screen_width = 700
	screen_height = 600

	screen = pygame.display.set_mode((screen_width, screen_height))
	pygame.display.set_caption("Board Games")

	font = pygame.font.SysFont('Constantia', 30)

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

		def __init__(self, x, y, text):
			self.x = x
			self.y = y
			self.text = text

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

	button1 = button(100, 100, 'Awele')
	button2 = button(350, 100, 'Othello')
	button3 = button(100, 250, 'Puissance4')
	button4 = button(350, 250, 'Squadro')
	button5 = button(100, 400, 'Chess')

	buttons = [button1, button2, button3, button4, button5]

	run = True
	while run:
		screen.fill(black)

		for button in buttons:
			if button.draw_button():
				os.system("python " + os.path.join(dirname, button.text + "/main.py") + " || python3 " + os.path.join(dirname, button.text + "/main.py"))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				sys.exit(0)

		pygame.display.update()