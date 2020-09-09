import pygame
from GameUtils import GameSettings as gs


def init():
    pygame.init()
    pygame.display.set_mode((gs.board_size[0] * gs.square_size, gs.board_size[1] * gs.square_size))
    pygame.display.get_surface().fill((0, 0, 0))
    paint_state(gs.current_state)


def paint_state(state):
    surface = pygame.display.get_surface()
    for i in range(state.board.shape[0]):
        for j in range(state.board.shape[1]):
            if state.board[i, j] == gs.block_sym:
                pygame.draw.rect(surface, (255, 255, 255),
                                 (j * gs.square_size, i * gs.square_size, gs.square_size,
                                  gs.square_size))
            elif state.board[i, j] > 0:
                pygame.draw.rect(surface, (state.board[i, j] * gs.player1.color[0] // gs.level_amount,
                                           state.board[i, j] * gs.player1.color[1] // gs.level_amount,
                                           state.board[i, j] * gs.player1.color[2] // gs.level_amount),
                                 (j * gs.square_size, i * gs.square_size, gs.square_size,
                                  gs.square_size))
            else:
                pygame.draw.rect(surface, (-state.board[i, j] * gs.player2.color[0] // gs.level_amount,
                                           -state.board[i, j] * gs.player2.color[1] // gs.level_amount,
                                           -state.board[i, j] * gs.player2.color[2] // gs.level_amount),
                                 (j * gs.square_size, i * gs.square_size, gs.square_size,
                                  gs.square_size))
    pygame.display.flip()


def paint_cursor(index):
    surface = pygame.display.get_surface()
    current_color = surface.get_at((index[1] * gs.square_size, index[0] * gs.square_size))
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
                     (index[1] * gs.square_size, index[0] * gs.square_size, gs.square_size,
                      gs.square_size))
    pygame.display.flip()