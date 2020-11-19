import numpy as np
import GraphicsHandler as gh
import pygame
from MiniMaxUtils import Tree
import time


def pos_to_index(pos):
    return pos[1] // GameSettings.SQUARE_SIZE, pos[0] // GameSettings.SQUARE_SIZE


def add(state, index, player):
    # add a player's core tile to the board
    # player 1 is represented with positive values while player 2 is represented with negative values
    board = np.copy(state)
    board[index] = player * GameSettings.LEVEL_AMOUNT
    return board


def start(player1, player2):
    # temporary
    # TODO: add color chooser
    player1.number = 1
    player2.number = -1
    GameSettings.player1 = player1
    GameSettings.player2 = player2
    gh.init()
    gh.paint_state(GameSettings.current_state)
    GameSettings.player1.move()


def state_score(state, player):
    sum = 0
    valid_me = 0
    for i in range(state.shape[0]):
        for j in range(state.shape[0]):
            if state[i, j] != GameSettings.BLOCK_SYM:
                sum += state[i, j]
                if player * state[i, j] > 0:
                    sum += state[i, j] * 2
            if valid(state, (i, j), player):
                valid_me += player * state[i, j]

    return player * sum + valid_me


def calculate_change(state):
    # calculate the effects of all core tiles
    board = np.copy(state)
    for i in range(GameSettings.BOARD_SIZE):
        for j in range(GameSettings.BOARD_SIZE):
            if abs(state[i, j]) == GameSettings.LEVEL_AMOUNT:
                grow_environment(board, (i, j))
    return board


def grow_environment(board, pos):
    # calculate the effects of a core tile
    sign = board[pos] // abs(board[pos])

    if pos[0] > 0:
        if board[pos[0] - 1, pos[1]] != GameSettings.BLOCK_SYM:
            if board[pos[0] - 1, pos[1]] * sign == -GameSettings.LEVEL_AMOUNT:
                board[pos[0], pos[1]] -= sign
            if board[pos[0] - 1, pos[1]] * sign < GameSettings.LEVEL_AMOUNT:
                board[pos[0] - 1, pos[1]] += sign
    if pos[1] > 0:
        if board[pos[0], pos[1] - 1] != GameSettings.BLOCK_SYM:
            if board[pos[0], pos[1] - 1] * sign == -GameSettings.LEVEL_AMOUNT:
                board[pos[0], pos[1]] -= sign
            if board[pos[0], pos[1] - 1] * sign < GameSettings.LEVEL_AMOUNT:
                board[pos[0], pos[1] - 1] += sign
    if pos[0] < GameSettings.BOARD_SIZE - 1:
        if board[pos[0] + 1, pos[1]] != GameSettings.BLOCK_SYM:
            if board[pos[0] + 1, pos[1]] * sign == -GameSettings.LEVEL_AMOUNT:
                board[pos[0], pos[1]] -= sign
            if board[pos[0] + 1, pos[1]] * sign < GameSettings.LEVEL_AMOUNT:
                board[pos[0] + 1, pos[1]] += sign
    if pos[1] < GameSettings.BOARD_SIZE - 1:
        if board[pos[0], pos[1] + 1] != GameSettings.BLOCK_SYM:
            if board[pos[0], pos[1] + 1] * sign == -GameSettings.LEVEL_AMOUNT:
                board[pos[0], pos[1]] -= sign
            if board[pos[0], pos[1] + 1] * sign < GameSettings.LEVEL_AMOUNT:
                board[pos[0], pos[1] + 1] += sign


def core_in_zone(state, index, player):
    # check if a core tile is next to the given index

    # no longer in use (deprecated)
    board = np.copy(state)
    if index[0] > 0:
        if board[index[0] - 1, index[1]] == player * GameSettings.LEVEL_AMOUNT:
            return True
    if index[1] > 0:
        if board[index[0], index[1] - 1] == player * GameSettings.LEVEL_AMOUNT:
            return True
    if index[0] < GameSettings.BOARD_SIZE - 1:
        if board[index[0] + 1, index[1]] == player * GameSettings.LEVEL_AMOUNT:
            return True
    if index[1] < GameSettings.BOARD_SIZE - 1:
        if board[index[0], index[1] + 1] == player * GameSettings.LEVEL_AMOUNT:
            return True


def valid(state, index, player):
    # check if a move is valid
    if GameSettings.current_move == GameSettings.max_move:
        return False
    board = np.copy(state)
    return -GameSettings.LEVEL_AMOUNT + 1 < player * board[index] < GameSettings.LEVEL_AMOUNT and board[
        index] != GameSettings.BLOCK_SYM


def check_game_over(state):
    # check if the game is over (if one of the players can't make any valid moves)
    c1 = 0
    c2 = 0
    for i in range(GameSettings.BOARD_SIZE):
        for j in range(GameSettings.BOARD_SIZE):
            if valid(state, (i, j), 1):
                c1 += 1
            if valid(state, (i, j), -1):
                c2 += 1
    return c1 == 0 or c2 == 0


def check_winner(state):
    # check who won
    sum = 0
    for arr in state:
        for x in arr:
            if x != GameSettings.BLOCK_SYM:
                sum += x
    if sum < 0:
        return -1
    elif sum > 0:
        return 1
    else:
        return 0


class Player:
    def __init__(self, color, computer, ai_depth):
        self.color = color
        self.is_computer = computer
        self.ai_depth = ai_depth

    def move(self):
        GameSettings.current_move += 1
        time.sleep(0.25)
        GameSettings.current_state = calculate_change(GameSettings.current_state)
        gh.paint_state(GameSettings.current_state)
        if check_game_over(GameSettings.current_state):
            print("Game Over")
            winner = check_winner(GameSettings.current_state)
            if winner == 1:
                print("Player 1 wins")
            elif winner == -1:
                print("Player 2 wins")
            else:
                print("Tie")
            pygame.quit()
            exit(11)
        if not self.is_computer:
            over = False
            current_pos = pos_to_index(pygame.mouse.get_pos())
            while not over:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.number == 1:
                            if valid(GameSettings.current_state, pos_to_index(pygame.mouse.get_pos()), self.number):
                                GameSettings.current_state = add(GameSettings.current_state,
                                                                 pos_to_index(pygame.mouse.get_pos()), 1)
                                gh.paint_state(GameSettings.current_state)
                                over = True
                                GameSettings.player2.move()
                        else:
                            if valid(GameSettings.current_state, pos_to_index(pygame.mouse.get_pos()), self.number):
                                GameSettings.current_state = add(GameSettings.current_state,
                                                                 pos_to_index(pygame.mouse.get_pos()), -1)
                                gh.paint_state(GameSettings.current_state)
                                over = True
                                GameSettings.player1.move()
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit(11)

                if pos_to_index(pygame.mouse.get_pos()) != current_pos:
                    gh.paint_state(GameSettings.current_state)
                    gh.paint_cursor(pos_to_index(pygame.mouse.get_pos()))
                    current_pos = pos_to_index(pygame.mouse.get_pos())
        else:
            t = Tree(GameSettings.current_state, self.number)
            t.calc_scores(self.ai_depth, self.number)
            if len(t.sons) > 0:
                move_state = t.max_son().state
                GameSettings.current_state = np.copy(move_state)
                gh.paint_state(GameSettings.current_state)
            if self.number == 1:
                GameSettings.player2.move()
            else:
                GameSettings.player1.move()


class GameSettings:
    BOARD_SIZE = 5  # size of the board in tiles
    SQUARE_SIZE = 600 // BOARD_SIZE  # size of each tile on the board
    LEVEL_AMOUNT = 5  # amount of control levels every tile has
    BLOCK_SYM = 99  # symbol for the center block

    current_move = 0
    max_move = 50


    # temporary
    player1 = None
    player2 = None

    current_state = np.zeros((BOARD_SIZE, BOARD_SIZE))
    current_state[0, BOARD_SIZE - 1] = LEVEL_AMOUNT
    current_state[BOARD_SIZE - 1, 0] = -LEVEL_AMOUNT
    # if the board size is odd, add a center block
    if BOARD_SIZE % 2 == 1:
        current_state[BOARD_SIZE // 2, BOARD_SIZE // 2] = BLOCK_SYM
