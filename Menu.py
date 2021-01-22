import pygame
import GraphicsHandler as gh

def start_menu():
    gh.init()
    over = False

    while not over:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(11)