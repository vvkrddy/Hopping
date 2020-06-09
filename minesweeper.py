#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 22:41:50 2020

@author: sahyadri
"""


import cx_Freeze
import pygame, sys
from pygame.locals import *
from numpy import random

number = 0
background = (220,220,220)
gray = (100,100,100)
light_gray = (160,160,160)
white = (255,255,255)

pygame.init()
window = pygame.display.set_mode((800,800))
window.fill(background)

smiley_face = pygame.image.load("/home/sahyadri/Downloads/mshapp.jpg")
sad_face = pygame.image.load("/home/sahyadri/Downloads/mssad.jpg")
mine = pygame.image.load("/home/sahyadri/Downloads/msmine.jpg")
mine = pygame.transform.scale(mine,(50,50))
smiley_face = pygame.transform.scale(smiley_face,(50,50))
sad_face = pygame.transform.scale(sad_face,(50,50))
font = pygame.font.SysFont('dejavusansmono', 20)

def text_objects(text, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

def message_display(text,x,y,colour,font_name,font_size):
    TextSurf, TextRect = text_objects(text, colour)
    TextRect.center = (x,y)
    window.blit(TextSurf, TextRect)
    font = pygame.font.SysFont(font_name, font_size)
    
class grid:
    number = 0

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.mine_prob = random.randint(0,101)
        
    def paste(self):
        if self.mine_prob>=80:
            window.blit(mine,(self.x,self.y))
            grid.number +=1
    
                
        

def box(x,y,w,h):
    mouse = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed()
    if x<=mouse[0]<=x+w and y<=mouse[1]<=y+h:
        pygame.draw.rect(window,gray,(x,y,w,h))
        if mouse_press[0]==True:
            window.blit(sad_face,(50,50))
            #run = False
                #game over!
            #else:
                #neighbour no.        
    else:
        pygame.draw.rect(window,light_gray,(x,y,w,h))
        

def main():
    run = True
    for j in range(16):
            for i in range(16):
                grid(0+i*50,100+j*50).paste()
                
                pygame.display.update()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        window.blit(smiley_face,(50,50))
        pygame.display.update()
        pygame.time.delay(1000)
        
main()
    
pygame.quit()    

            #draw rect at each posn