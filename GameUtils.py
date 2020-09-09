import numpy as np
import GraphicsHandler as gh
import pygame
from MiniMaxUtils import Tree
import time


class State:
    def __init__(self, board):
        self.board = board

    def __repr__(self):
        for a in self.board:
            print(a)


def pos_to_index(pos):
    return pos[1] // GameSettings.square_size, pos[0] // GameSettings.square_size


def add(state, index, player):
    board = np.copy(state.board)
    board[index] = player * GameSettings.level_amount
    return State(board)


def start(player1_is_ai, player2_is_ai):
    # temporary as fuck
    GameSettings.player1 = Player((225, 123, 240), player1_is_ai, 1)
    GameSettings.player2 = Player((240, 240, 123), player2_is_ai, -1)
    gh.init()
    GameSettings.player1.move()


def state_score(state, player):
    sum = 0
    valid_me = 0
    valid_them = 0
    for i in range(state.board.shape[0]):
        for j in range(state.board.shape[0]):
            if state.board[i, j] != GameSettings.block_sym:
                sum += state.board[i,j]
                if valid(state, (i, j), player):
                    valid_me += 1
                if valid(state, (i, j), -player):
                    valid_them += 1
    return player * sum + valid_me - valid_them // 2


def calculate_change(state):
    board = np.copy(state.board)
    for i in range(GameSettings.board_size[0]):
        for j in range(GameSettings.board_size[1]):
            if abs(state.board[i, j]) == GameSettings.level_amount:
                grow_environment(board, (i, j))
    return State(board)


def grow_environment(board, pos):
    sign = board[pos] // abs(board[pos])

    if pos[0] > 0:
        if board[pos[0] - 1, pos[1]] != GameSettings.block_sym:
            if board[pos[0] - 1, pos[1]] * sign == -GameSettings.level_amount:
                board[pos[0], pos[1]] -= sign
            if board[pos[0] - 1, pos[1]] * sign < GameSettings.level_amount:
                board[pos[0] - 1, pos[1]] += sign
    if pos[1] > 0:
        if board[pos[0], pos[1] - 1] != GameSettings.block_sym:
            if board[pos[0], pos[1] - 1] * sign == -GameSettings.level_amount:
                board[pos[0], pos[1]] -= sign
            if board[pos[0], pos[1] - 1] * sign < GameSettings.level_amount:
                board[pos[0], pos[1] - 1] += sign
    if pos[0] < GameSettings.board_size[0] - 1:
        if board[pos[0] + 1, pos[1]] != GameSettings.block_sym:
            if board[pos[0] + 1, pos[1]] * sign == -GameSettings.level_amount:
                board[pos[0], pos[1]] -= sign
            if board[pos[0] + 1, pos[1]] * sign < GameSettings.level_amount:
                board[pos[0] + 1, pos[1]] += sign
    if pos[1] < GameSettings.board_size[1] - 1:
        if board[pos[0], pos[1] + 1] != GameSettings.block_sym:
            if board[pos[0], pos[1] + 1] * sign == -GameSettings.level_amount:
                board[pos[0], pos[1]] -= sign
            if board[pos[0], pos[1] + 1] * sign < GameSettings.level_amount:
                board[pos[0], pos[1] + 1] += sign


def core_in_zone(state, index, player):
    board = np.copy(state.board)
    if index[0] > 0:
        if board[index[0] - 1, index[1]] == player * GameSettings.level_amount:
            return True
    if index[1] > 0:
        if board[index[0], index[1] - 1] == player * GameSettings.level_amount:
            return True
    if index[0] < GameSettings.board_size[0] - 1:
        if board[index[0] + 1, index[1]] == player * GameSettings.level_amount:
            return True
    if index[1] < GameSettings.board_size[1] - 1:
        if board[index[0], index[1] + 1] == player * GameSettings.level_amount:
            return True


def valid(state, index, player):
    board = np.copy(state.board)
    return -GameSettings.level_amount + 1 < player * board[index] < GameSettings.level_amount and board[index] != GameSettings.block_sym


def check_game_over(state):
    c1 = 0
    c2 = 0
    for i in range(GameSettings.board_size[0]):
        for j in range(GameSettings.board_size[1]):
            if valid(state, (i, j), 1):
                c1 += 1
            if valid(state, (i, j), -1):
                c2 += 1
    return c1 == 0 or c2 == 0


def check_winner(state):
    sum = 0
    for arr in state.board:
        for x in arr:
            if x != GameSettings.block_sym:
                sum += x
    if sum < 0:
        return -1
    elif sum > 0:
        return 1
    else:
        return 0


class Player:
    def __init__(self, color, computer, number):
        self.color = color
        self.is_computer = computer
        self.number = number

    def move(self):
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
            t.calc_scores(GameSettings.ai_depth_amount, self.number)
            if len(t.sons) > 0:
                move_state = t.max_son().state
                GameSettings.current_state = State(np.copy(move_state.board))
                gh.paint_state(GameSettings.current_state)
            if self.number == 1:
                GameSettings.player2.move()
            else:
                GameSettings.player1.move()


class GameSettings:
    board_size = (5, 5)
    square_size = 600 // board_size[0]
    level_amount = 5
    block_sym = 99

    ai_depth_amount = 3

    # temporary as fuck
    player1 = None
    player2 = None

    current_state = State(np.zeros(board_size))
    current_state.board[0, board_size[1] - 1] = level_amount
    current_state.board[board_size[0] - 1, 0] = -level_amount
    if board_size[0] % 2 == 1:
        current_state.board[board_size[0]//2, board_size[1]//2] = block_sym
