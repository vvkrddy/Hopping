# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#import pygame_textinput
import cx_Freeze
import pygame, sys
from pygame.locals import *

black = (0,0,0)
green = (0,200,0)
white = (255,255,255)
red = (200,0,0)
bright_green = (0,255,0)
bright_red = (255,0,0)
gray = (100,100,100)
yellow = (0,200,200)

def fill_area(x,y,w,h):
    text=""
    active = False
    mouse = pygame.mouse.get_pos()
    pygame.draw.rect(window,white,(x,y,w,h))
    mouse_click = pygame.mouse.get_pressed()
    key = pygame.key.get_pressed()
    if x<=mouse[0]<=x+w and y<=mouse[1]<=y+h:
        if mouse_click[0] == True:
            active=True
            print(active)
        else:
            active = False
    while active==True:
        if key[pygame.K_RETURN]:
            message_display(text,x+w/2,y+h/2,black)
            active=False
            print(active)
            text=""
        elif key[pygame.K_BACKSPACE]:
            text=text[:-1]
        else:
            text += "Meh"

def text_objects(text, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


def button(msg,x,y,w,h,ic,ac):
    mouse = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    if x<=mouse[0]<=x+w and y<=mouse[1]<=y+h:
        pygame.draw.rect(window,ac,(x,y,w,h))
        message_display(msg,(x+(w/2)),(y+(h/2)),gray)
        if mouse_click[0]==True:
           pygame.display.quit()

    else:
        pygame.draw.rect(window,ic,(x,y,w,h))
        message_display(msg,(x+(w/2)),(y+(h/2)),white)

def message_display(text,x,y,colour):
    TextSurf, TextRect = text_objects(text, colour)
    TextRect.center = (x,y)
    window.blit(TextSurf, TextRect)
    
    pygame.display.update()
    
    
#textinput = pygame_textinput.TextInput

pygame.init()
window = pygame.display.set_mode((800,800))

pygame.display.set_caption("Hopper")
#background = pygame.image.load("/home/sahyadri/Downloads/crab.jpeg")
#background = pygame.transform.scale(background,(500,500))

font = pygame.font.SysFont(None, 20)
pygame.display.update()

def main_menu():
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run = False
        
        button("Option A",150,450,100,50,green,bright_green)
        button("Option B",550,450,100,50,red,bright_red)
        fill_area(150,200,400,25)
        
        pygame.display.update()
        
def first_screen():
    run1 = True
    while run1:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run1 = False
        
    pygame.display.update()
        

main_menu()



first_screen()

pygame.quit()