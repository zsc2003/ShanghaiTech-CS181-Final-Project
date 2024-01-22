# -*- coding:utf-8 -*-
import pygame
import images

#正负无穷
POSI_INFI = 2147483647
NEGA_INFI  = -2147483647

#颜色
WHITE = (255,255,255)
BLUE = (0,0,255)
BLACK = (127,0,0)
GREY1 = (209,203,180)
GREY2 = (194,194,194)
GREEN = (114,139,114)

# chess board info
WIDTH , HEIGHT = 640 , 680  #界面的宽高
ROWS , COLS = 8 , 8         #棋盘的行列数
SIZE = 80                   #棋格宽度

# images for crowns
WHITE_CROWN = pygame.transform.scale(pygame.image.load('images/white.jpg'), (44, 25))
BLACK_CROWN = pygame.transform.scale(pygame.image.load('images/black.jpg'), (44, 25))