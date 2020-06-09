#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 00:02:20 2020

@author: sahyadri
"""


import cx_Freeze
import pygame, sys
from pygame.locals import *
import numpy as np
from numpy import random
import time

boxes = []
nom=[]
mine_pos = []
buttons = []
var = ""

number = 0
dark_gray = (50,50,50)
background = (220,220,220)
gray = (100,100,100)
light_gray = (160,160,160)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

pygame.init()
window = pygame.display.set_mode((800,800))
window.fill(background)

smiley_face = pygame.image.load("/home/sahyadri/Downloads/mshapp.jpg")
sad_face = pygame.image.load("/home/sahyadri/Downloads/mssad.jpg")
mine = pygame.image.load("/home/sahyadri/Downloads/msmine.jpg")
flag = pygame.image.load("/home/sahyadri/Downloads/msflag.png")
mine = pygame.transform.scale(mine,(50,50))
smiley_face = pygame.transform.scale(smiley_face,(50,50))
sad_face = pygame.transform.scale(sad_face,(50,50))
flag = pygame.transform.scale(flag,(50,50))
font = pygame.font.SysFont('dejavusansmono', 20)

def text_objects(text, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

def message_display(text,x,y,colour,font_name,font_size):
    TextSurf, TextRect = text_objects(text, colour)
    TextRect.center = (x,y)
    window.blit(TextSurf, TextRect)
    font = pygame.font.SysFont(font_name, font_size)
    
def button_and_flag():
    blit_all = False
    mouse = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    if mouse_click[0]==True:
        for items in buttons:
            if items.collidepoint(mouse[0],mouse[1]):
                if items in mine_pos:
                    blit_all = True
                    break
                else:
                    pygame.draw.rect(window,background,items)
                    #index = int((items[0]/50)+((items[1]-100)/50)*16)
                    #message_display(nom[index], items[0]+25, items[1]+25, red, "ubuntu", 10)
    elif mouse_click[2]==True:
        for items in buttons:
            if items.collidepoint(mouse[0],mouse[1]):
                window.blit(flag,(items[0],items[1]))
    if blit_all ==True:
        for items in mine_pos:
            window.blit(mine,(items[0],items[1]))
        window.blit(sad_face,(375,40))
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.display.quit()
            
        
def draw_buttons():
    for j in range(16):
        for i in range(16):
            bon = pygame.Rect(2+i*50,102+j*50,48,48)
            border = pygame.Rect(0+i*50,100+j*50,50,50)
            pygame.draw.rect(window,white,border)
            pygame.draw.rect(window,dark_gray,bon)
            buttons.append(border)
 
#def g(x,y):
   # for elts in mine_pos:
    #    if elts[0]==x and elts[1]==y:
     #       return float(1)
      #  else:
       #     return float(0)
    
#def proximity_calc():
    #for elements in boxes:
     #   w = elements[0]
      #  z = elements[1]
       # proximity_number = str(g(w,z-50)+g(w,z+50)+g(w+50,z)+g(w-50,z)+g(w+50,z+50)+g(w+50,z-50)+g(w-50,z+50)+g(w-50,z-50))
        #print(g(w,z-50),g(w,z+50),g(w+50,z),g(w-50,z),g(w+50,z+50),g(w+50,z-50),g(w-50,z+50),g(w-50,z-50))
        
       # nom.append(proximity_number)


def draw_grid():
    for j in range(16):
        for i in range(16):
            box = pygame.Rect(0+i*50,100+j*50,50,50)
            boxes.append(box)
            pygame.draw.rect(window,black,box,2)
                
def mine_place():
    mouse = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed()
    if mouse_press[0]==True:
            for items in boxes:
                if items[0]<=mouse[0]<=items[0]+items[2] and items[1]<=mouse[1]<=items[1]+items[3]:
                    window.blit(mine,(items[0],items[1]))
                    mine_pos.append(items)
        
            
 
clock = pygame.time.Clock()
                   
def user():
    #proximity_calc()
    flag_count = 0
    clock_rect = pygame.Rect(50,40,50,50)
    flag_rect = pygame.Rect(700,50,50,50)
    message_display("Flags", 20, 475, black, "ubuntu", 20)
    pygame.draw.rect(window,black,flag_rect)
    draw_buttons()
    clock.tick(1)
    run = True
    while run:
        pygame.draw.rect(window,black,clock_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
        button_and_flag()
        window.blit(smiley_face,(375,40))
        time_elapsed = str(int(round(pygame.time.get_ticks()/1000)))
        message_display(time_elapsed,clock_rect[0]+(clock_rect[2]/2),clock_rect[1]+(clock_rect[3]/2),red,"ubuntu",20)
        pygame.display.update()
        
    
    

def admin():
    draw_grid()
    run = True
    #message_display("To proceed, press enter", 450, 40, black, "ubuntu", 20)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_RETURN:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mine_place()
        window.blit(smiley_face,(375,40))
        pygame.display.update()
   # print(g(0,100),g(100,50))
    #global mine_pos
    #mine_pos = list(dict.fromkeys(mine_pos))

        
admin()
user()

    
pygame.quit()    

    