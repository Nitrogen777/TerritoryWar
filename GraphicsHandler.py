import pygame
from GameUtils import GameSettings as gs


def init():
    pygame.init()
    pygame.display.set_mode((gs.BOARD_SIZE * gs.SQUARE_SIZE, gs.BOARD_SIZE * gs.SQUARE_SIZE))
    pygame.display.get_surface().fill((0, 0, 0))
    pygame.font.init()

def paint_state(state):
    surface = pygame.display.get_surface()
    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            if state[i, j] == gs.BLOCK_SYM:
                pygame.draw.rect(surface, (255, 255, 255),
                                 (j * gs.SQUARE_SIZE, i * gs.SQUARE_SIZE, gs.SQUARE_SIZE,
                                  gs.SQUARE_SIZE))
            elif state[i, j] > 0:
                pygame.draw.rect(surface, (state[i, j] * gs.player1.color[0] // gs.LEVEL_AMOUNT,
                                           state[i, j] * gs.player1.color[1] // gs.LEVEL_AMOUNT,
                                           state[i, j] * gs.player1.color[2] // gs.LEVEL_AMOUNT),
                                 (j * gs.SQUARE_SIZE, i * gs.SQUARE_SIZE, gs.SQUARE_SIZE,
                                  gs.SQUARE_SIZE))
            else:
                pygame.draw.rect(surface, (-state[i, j] * gs.player2.color[0] // gs.LEVEL_AMOUNT,
                                           -state[i, j] * gs.player2.color[1] // gs.LEVEL_AMOUNT,
                                           -state[i, j] * gs.player2.color[2] // gs.LEVEL_AMOUNT),
                                 (j * gs.SQUARE_SIZE, i * gs.SQUARE_SIZE, gs.SQUARE_SIZE,
                                  gs.SQUARE_SIZE))
    pygame.display.flip()


def paint_cursor(index):
    surface = pygame.display.get_surface()
    current_color = surface.get_at((index[1] * gs.SQUARE_SIZE, index[0] * gs.SQUARE_SIZE))
    if current_color[0] + 50 > 255:
        r = 255
    else:
        r = current_color[0] + 50
    if current_color[1] + 50 > 255:
        g = 255
    else:
        g = current_color[1] + 50
    if current_color[2] + 50 > 255:
        b = 255
    else:
        b = current_color[2] + 50
    pygame.draw.rect(surface, (r, g, b),
                     (index[1] * gs.SQUARE_SIZE, index[0] * gs.SQUARE_SIZE, gs.SQUARE_SIZE,
                      gs.SQUARE_SIZE))
    pygame.display.flip()