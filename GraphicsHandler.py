import pygame
from GameUtils import GameSettings as gs
import GameUtils as gu

INFO_SIZE = 100
FONT_SIZE = 18
SCORE_FONT_SIZE = 20
ENDGAME_FONT_SIZE = 64
BACKGROUND = (0, 14, 28)


# Initiate pygame
def init():
    pygame.init()
    pygame.display.set_mode((600 + INFO_SIZE * 2, 600 + INFO_SIZE))
    pygame.display.get_surface().fill((0, 0, 0))
    pygame.font.init()
    global FONT
    global SCORE_FONT
    global ENDGAME_FONT
    FONT = pygame.font.SysFont('Helvetica', FONT_SIZE)
    SCORE_FONT = pygame.font.SysFont('Helvetica', SCORE_FONT_SIZE)
    ENDGAME_FONT = pygame.font.Font('hacker.ttf', ENDGAME_FONT_SIZE)


# Paint a given state of the board
def paint_state(state):
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
                pygame.draw.rect(surface, (state[i, j] * gs.player1.color[0] // gs.LEVEL_AMOUNT,
                                           state[i, j] * gs.player1.color[1] // gs.LEVEL_AMOUNT,
                                           state[i, j] * gs.player1.color[2] // gs.LEVEL_AMOUNT),
                                 (j * gs.SQUARE_SIZE + INFO_SIZE, i * gs.SQUARE_SIZE + INFO_SIZE, gs.SQUARE_SIZE,
                                  gs.SQUARE_SIZE))
            else:
                pygame.draw.rect(surface, (-state[i, j] * gs.player2.color[0] // gs.LEVEL_AMOUNT,
                                           -state[i, j] * gs.player2.color[1] // gs.LEVEL_AMOUNT,
                                           -state[i, j] * gs.player2.color[2] // gs.LEVEL_AMOUNT),
                                 (j * gs.SQUARE_SIZE + INFO_SIZE, i * gs.SQUARE_SIZE + INFO_SIZE, gs.SQUARE_SIZE,
                                  gs.SQUARE_SIZE))
    stats = gu.get_game_stats(state)
    player1 = stats[0]
    player2 = stats[1]
    for level in player1:
        text1 = FONT.render("Level {}: {}".format(level, player1[level]), False, gs.player1.color)
        text2 = FONT.render("Level {}: {}".format(level, player2[level]), False, gs.player2.color)
        surface.blit(text1, (INFO_SIZE + 605, INFO_SIZE + FONT_SIZE*level))
        surface.blit(text2, (5, INFO_SIZE + 600 - FONT_SIZE * (level+1)))
    surface.blit(FONT.render("Move: {}".format(gs.current_move), False, (255,255,255)), (0, 0))
    score_text1 = SCORE_FONT.render("Score: {}".format(gu.state_score(state, 1)), False, gs.player1.color)
    score_text2 = SCORE_FONT.render("Score: {}".format(gu.state_score(state, -1)), False, gs.player2.color)
    surface.blit(score_text1, (INFO_SIZE + 605, INFO_SIZE + FONT_SIZE * len(player1) + SCORE_FONT_SIZE))
    surface.blit(score_text2, (5, INFO_SIZE + 600 - FONT_SIZE * len(player2) - (FONT_SIZE + SCORE_FONT_SIZE)))
    pygame.display.flip()


# Display "THE AI IS THINKING" while minimax is calculating
def show_ai_thinking():
    surface = pygame.display.get_surface()
    ai_thinking = ENDGAME_FONT.render("THE ai IS Thinking", False, (255, 255, 255))
    surface.blit(ai_thinking, ((600 + INFO_SIZE * 2) // 2 - ai_thinking.get_size()[0] // 2, 20))
    pygame.display.flip()


# Paint the end-of-game "Winner" state
def paint_winner(state, winner):
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
                pygame.draw.rect(surface, (state[i, j] * gs.player1.color[0] // gs.LEVEL_AMOUNT,
                                           state[i, j] * gs.player1.color[1] // gs.LEVEL_AMOUNT,
                                           state[i, j] * gs.player1.color[2] // gs.LEVEL_AMOUNT),
                                 (j * gs.SQUARE_SIZE + INFO_SIZE, i * gs.SQUARE_SIZE + INFO_SIZE, gs.SQUARE_SIZE,
                                  gs.SQUARE_SIZE))
            else:
                pygame.draw.rect(surface, (-state[i, j] * gs.player2.color[0] // gs.LEVEL_AMOUNT,
                                           -state[i, j] * gs.player2.color[1] // gs.LEVEL_AMOUNT,
                                           -state[i, j] * gs.player2.color[2] // gs.LEVEL_AMOUNT),
                                 (j * gs.SQUARE_SIZE + INFO_SIZE, i * gs.SQUARE_SIZE + INFO_SIZE, gs.SQUARE_SIZE,
                                  gs.SQUARE_SIZE))
    score_text1 = SCORE_FONT.render("Score: {}".format(gu.state_score(state, 1)), False, gs.player1.color)
    score_text2 = SCORE_FONT.render("Score: {}".format(gu.state_score(state, -1)), False, gs.player2.color)
    surface.blit(score_text1, (INFO_SIZE + 605, INFO_SIZE + FONT_SIZE * gs.LEVEL_AMOUNT + SCORE_FONT_SIZE))
    surface.blit(score_text2, (5, INFO_SIZE + 600 - FONT_SIZE * gs.LEVEL_AMOUNT - (FONT_SIZE + SCORE_FONT_SIZE)))
    if winner == 1:
        endgame_text = ENDGAME_FONT.render("Player 1 Wins", False, gs.player1.color)
    elif winner == 2:
        endgame_text = ENDGAME_FONT.render("Player 2 Wins", False, gs.player2.color)
    surface.blit(endgame_text, ((600 + INFO_SIZE*2)//2 - endgame_text.get_size()[0]//2, 20))
    pygame.display.flip()


# Brighten up the place where the cursor is located
def paint_cursor(index):
    if index[1] < 0 or index[0] < 0 or index[1] >= gs.BOARD_SIZE:
        return
    surface = pygame.display.get_surface()
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