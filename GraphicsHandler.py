"""
This file includes methods used by the game's graphics.
"""

import pygame
from GameUtils import GameSettings as gs
import GameUtils as gu

INFO_SIZE = 100
FONT_SIZE = 18
SCORE_FONT_SIZE = 20
ENDGAME_FONT_SIZE = 64
BACKGROUND = (0, 14, 28)


def init():
    """
    Initiate the graphics for the game.
    """
    pygame.init()
    pygame.display.set_mode((600 + INFO_SIZE * 2, 600 + INFO_SIZE))
    pygame.display.get_surface().fill((0, 0, 0))
    pygame.display.set_caption("Territory War")
    pygame.font.init()
    global FONT
    global SCORE_FONT
    global ENDGAME_FONT
    FONT = pygame.font.SysFont('Helvetica', FONT_SIZE)
    SCORE_FONT = pygame.font.SysFont('Helvetica', SCORE_FONT_SIZE)
    ENDGAME_FONT = pygame.font.Font('hacker.ttf', ENDGAME_FONT_SIZE)


def paint_state(state):
    """
    Paint a given game state on the screen, including game stats.
    :param state: The game state.
    """
    surface = pygame.display.get_surface()
    surface.fill(BACKGROUND)
    pygame.draw.rect(surface, (255, 255, 255), (INFO_SIZE-1, INFO_SIZE-1, 602, 601))
    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            if state[i, j] == gs.BLOCK_SYM:
                pygame.draw.rect(surface, (255, 255, 255),
                                 (j * gs.SQUARE_SIZE + INFO_SIZE, i * gs.SQUARE_SIZE + INFO_SIZE, gs.SQUARE_SIZE,
                                  gs.SQUARE_SIZE))
            elif state[i, j] > 0:
                pygame.draw.rect(surface, (state[i, j] * gs.player1._color[0] // gs.LEVEL_AMOUNT,
                                           state[i, j] * gs.player1._color[1] // gs.LEVEL_AMOUNT,
                                           state[i, j] * gs.player1._color[2] // gs.LEVEL_AMOUNT),
                                 (j * gs.SQUARE_SIZE + INFO_SIZE, i * gs.SQUARE_SIZE + INFO_SIZE, gs.SQUARE_SIZE,
                                  gs.SQUARE_SIZE))
            else:
                pygame.draw.rect(surface, (-state[i, j] * gs.player2._color[0] // gs.LEVEL_AMOUNT,
                                           -state[i, j] * gs.player2._color[1] // gs.LEVEL_AMOUNT,
                                           -state[i, j] * gs.player2._color[2] // gs.LEVEL_AMOUNT),
                                 (j * gs.SQUARE_SIZE + INFO_SIZE, i * gs.SQUARE_SIZE + INFO_SIZE, gs.SQUARE_SIZE,
                                  gs.SQUARE_SIZE))
    stats = gu.get_game_stats(state)
    player1 = stats[0]
    player2 = stats[1]
    for level in player1:
        text1 = FONT.render("Level {}: {}".format(level, player1[level]), False, gs.player1._color)
        text2 = FONT.render("Level {}: {}".format(level, player2[level]), False, gs.player2._color)
        surface.blit(text1, (INFO_SIZE + 605, INFO_SIZE + FONT_SIZE*level))
        surface.blit(text2, (5, INFO_SIZE + 600 - FONT_SIZE * (level+1)))
    surface.blit(FONT.render("Move: {}".format(gs.current_move), False, (255,255,255)), (0, 0))
    score_text1 = SCORE_FONT.render("Score: {}".format(gu.state_score(state, 1)), False, gs.player1._color)
    score_text2 = SCORE_FONT.render("Score: {}".format(gu.state_score(state, -1)), False, gs.player2._color)
    surface.blit(score_text1, (INFO_SIZE + 605, INFO_SIZE + FONT_SIZE * len(player1) + SCORE_FONT_SIZE))
    surface.blit(score_text2, (5, INFO_SIZE + 600 - FONT_SIZE * len(player2) - (FONT_SIZE + SCORE_FONT_SIZE)))
    pygame.display.flip()


def show_ai_thinking():
    """
    Display "The AI is thinking" on the screen for a better user experience.
    """
    surface = pygame.display.get_surface()
    ai_thinking = ENDGAME_FONT.render("THE ai IS Thinking", False, (255, 255, 255))
    surface.blit(ai_thinking, ((600 + INFO_SIZE * 2) // 2 - ai_thinking.get_size()[0] // 2, 20))
    pygame.display.flip()


def paint_winner(state, winner):
    """
    Paint the state at which the game ended.
    :param state: The game state.
    :param winner: The winner. 1 for player 1, 2 for player 2 and 0 for tie
    :return:
    """
    surface = pygame.display.get_surface()
    surface.fill(BACKGROUND)
    pygame.draw.rect(surface, (255, 255, 255), (INFO_SIZE-1, INFO_SIZE-1, 602, 601))
    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            if state[i, j] == gs.BLOCK_SYM:
                pygame.draw.rect(surface, (255, 255, 255),
                                 (j * gs.SQUARE_SIZE + INFO_SIZE, i * gs.SQUARE_SIZE + INFO_SIZE, gs.SQUARE_SIZE,
                                  gs.SQUARE_SIZE))
            elif state[i, j] > 0:
                pygame.draw.rect(surface, (state[i, j] * gs.player1._color[0] // gs.LEVEL_AMOUNT,
                                           state[i, j] * gs.player1._color[1] // gs.LEVEL_AMOUNT,
                                           state[i, j] * gs.player1._color[2] // gs.LEVEL_AMOUNT),
                                 (j * gs.SQUARE_SIZE + INFO_SIZE, i * gs.SQUARE_SIZE + INFO_SIZE, gs.SQUARE_SIZE,
                                  gs.SQUARE_SIZE))
            else:
                pygame.draw.rect(surface, (-state[i, j] * gs.player2._color[0] // gs.LEVEL_AMOUNT,
                                           -state[i, j] * gs.player2._color[1] // gs.LEVEL_AMOUNT,
                                           -state[i, j] * gs.player2._color[2] // gs.LEVEL_AMOUNT),
                                 (j * gs.SQUARE_SIZE + INFO_SIZE, i * gs.SQUARE_SIZE + INFO_SIZE, gs.SQUARE_SIZE,
                                  gs.SQUARE_SIZE))
    score_text1 = SCORE_FONT.render("Score: {}".format(gu.state_score(state, 1)), False, gs.player1._color)
    score_text2 = SCORE_FONT.render("Score: {}".format(gu.state_score(state, -1)), False, gs.player2._color)
    surface.blit(score_text1, (INFO_SIZE + 605, INFO_SIZE + FONT_SIZE * gs.LEVEL_AMOUNT + SCORE_FONT_SIZE))
    surface.blit(score_text2, (5, INFO_SIZE + 600 - FONT_SIZE * gs.LEVEL_AMOUNT - (FONT_SIZE + SCORE_FONT_SIZE)))
    if winner == 1:
        endgame_text = ENDGAME_FONT.render("Player 1 Wins", False, gs.player1._color)
    elif winner == 2:
        endgame_text = ENDGAME_FONT.render("Player 2 Wins", False, gs.player2._color)
    elif winner == 0:
        endgame_text = ENDGAME_FONT.render("Its a TIE", False, (255, 255, 255))
    surface.blit(endgame_text, ((600 + INFO_SIZE*2)//2 - endgame_text.get_size()[0]//2, 20))
    pygame.display.flip()


def paint_cursor(index):
    """
    Brighten up a specific portion of the board.
    Also display the level number in the top right.
    :param index: The board index to brighten up.
    """
    if index[1] < 0 or index[0] < 0 or index[1] >= gs.BOARD_SIZE or gs.current_state[index[0], index[1]] == gs.BLOCK_SYM:
        return
    if gs.current_state[index[0],index[1]] > 0 and gs.current_state[index[0], index[1]] != gs.BLOCK_SYM:
        color = gs.player1._color
    elif gs.current_state[index[0],index[1]] < 0:
        color = gs.player2._color
    else:
        color = (255,255,255)

    level_text = ENDGAME_FONT.render("{}".format(int(abs(gs.current_state[index[0],index[1]]))), False, color)
    level_surf = pygame.Surface(level_text.get_size())
    level_surf.fill(BACKGROUND)
    level_surf.blit(level_text, (0,0))
    surface = pygame.display.get_surface()
    surface.blit(level_surf, (600 + INFO_SIZE*2-level_surf.get_size()[0],0))
    current_color = surface.get_at((index[1] * gs.SQUARE_SIZE + INFO_SIZE, index[0] * gs.SQUARE_SIZE + INFO_SIZE))
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
                     (index[1] * gs.SQUARE_SIZE + INFO_SIZE, index[0] * gs.SQUARE_SIZE + INFO_SIZE, gs.SQUARE_SIZE,
                      gs.SQUARE_SIZE))
    pygame.display.flip()