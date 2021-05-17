import numpy as np
import GraphicsHandler as gh
import pygame
from MiniMaxUtils import Tree
import time


def pos_to_index(pos):
    """
    A function that converts an x,y pixel position to an index on a board.
    :param pos: A x,y pixel position on the screen.
    :return: A index representing the location of the tile on a board.
    """
    return (pos[1] - gh.INFO_SIZE) // GameSettings.SQUARE_SIZE, (pos[0] - gh.INFO_SIZE) // GameSettings.SQUARE_SIZE


def add(state, index, player):
    """
    Adds a player's core tile (a tile with the maximum control level) to the board.
    :param state: The board that the core tile is being added to.
    :param index: The index where the core tile is being added.
    :param player: The number representing the player (Player 1 is represented with 1, Player 2 is represented with -1)
    :return: The new board, with the core tile added.
    """
    board = np.copy(state)
    board[index] = player * GameSettings.LEVEL_AMOUNT
    return board


def start(player1, player2):
    """
    Starts a new game with 2 customizable players.
    :param player1: Player 1 (The 1 player).
    :param player2: Player 2 (The -1 player).
    """
    player1.number = 1
    player2.number = -1
    GameSettings.player1 = player1
    GameSettings.player2 = player2
    gh.init()
    gh.paint_state(GameSettings.current_state)
    pygame.mixer_music.load("music.mp3")
    pygame.mixer_music.play(0)
    GameSettings.player1.move()


def state_score(state, player):
    """
    Calculate the score of a given game state for a specific player.
    The score is calculated by summing all the levels of the tiles that the player controls,
    subtracting the levels of the tiles the enemy player controls, (since enemy levels are negative to the player level,
    we are essentially summing the whole board), and adding 1 for every tile controlled by the player
    :param state: The game state for which we are calculating the score.
    :param player: The player we are calculating the score for.
    :return: The score of the game state.
    """
    sum = 0
    for i in range(state.shape[0]):
        for j in range(state.shape[0]):
            if state[i, j] != GameSettings.BLOCK_SYM:
                sum += state[i, j]
                if state[i, j] * player > 0:
                    sum += player

    return int(player * sum)


def calculate_change(state):
    """
    Calculate all the changes made to a game state as a result of the core tiles expanding.
    :param state: The state where the changes are performed.
    :return: The new state with the changes performed.
    """
    board = np.copy(state)
    for i in range(GameSettings.BOARD_SIZE):
        for j in range(GameSettings.BOARD_SIZE):
            if abs(board[i, j]) == GameSettings.LEVEL_AMOUNT:
                grow_environment(board, (i, j))
    return board


def grow_environment(board, pos):
    """
    Expand the environment of a single core tile.
    :param board: The board where the changes are being performed.
    :param pos: The position where the core tile is located.
    """
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


def valid(state, index, player):
    """
    Check if playing a core tile in a specific location is a valid move.
    :param state: The game board.
    :param index: The location being checked.
    :param player: The player performing the move.
    :return: True if the move is valid, False otherwise.
    """
    if GameSettings.current_move == GameSettings.max_move:
        return False
    board = np.copy(state)
    return -GameSettings.LEVEL_AMOUNT + 1 <= player * board[index] < GameSettings.LEVEL_AMOUNT and \
           board[index] != GameSettings.BLOCK_SYM


def check_game_over(state):
    """
    Check if the game is over (if a player can't make any valid moves).
    :param state: The game state.
    :return: True if the game is over, False otherwise.
    """
    c1 = 0
    c2 = 0
    for i in range(GameSettings.BOARD_SIZE):
        for j in range(GameSettings.BOARD_SIZE):
            if valid(state, (i, j), 1):
                c1 += 1
            if valid(state, (i, j), -1):
                c2 += 1
    return c1 == 0 or c2 == 0


def get_game_stats(state):
    """
    Get a dictionary of the amounts of tiles in each level. Mostly used for graphics.
    :param state: The game state.
    :return: A tuple with 2 dictionaries, 1 for each player. Each dictionary holes the amount of tiles in
    a specific level, with the key being the level. For example, player1[5] returns the amount of Level 5 tiles
    controlled by player 1.
    """
    player1 = {}
    player2 = {}
    for i in range(GameSettings.LEVEL_AMOUNT, 0, -1):
        player1[i] = 0
        player2[i] = 0
    for i in range(GameSettings.BOARD_SIZE):
        for j in range(GameSettings.BOARD_SIZE):
            if 0 < state[i, j] <= GameSettings.LEVEL_AMOUNT:
                player1[state[i,j]] += 1
            elif -GameSettings.LEVEL_AMOUNT <= state[i, j] < 0:
                player2[-state[i,j]] += 1
    return player1, player2


def check_winner(state):
    """
    Checks which player 1.
    :param state: The game state.
    :return: 1 if player 1 won, -1 if player 2 won and 0 if its a tie.
    """
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
    def __init__(self, color, computer, ai_depth=4):
        self.color = color
        self.is_computer = computer
        self.ai_depth = ai_depth

    def move(self):
        """
        Execute the player's move.
        """
        GameSettings.current_move += 1
        time.sleep(0.25)
        GameSettings.current_state = calculate_change(GameSettings.current_state)
        gh.paint_state(GameSettings.current_state)
        # First check if the game is over
        if check_game_over(GameSettings.current_state):
            winner = check_winner(GameSettings.current_state)
            if winner == 1:
                gh.paint_winner(GameSettings.current_state, 1)
            elif winner == -1:
                gh.paint_winner(GameSettings.current_state, 2)
            else:
                gh.paint_winner(GameSettings.current_state, 0)
            pygame.mixer_music.load("buzz.mp3")
            pygame.mixer_music.play(0)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit(11)
        # Check if the player is a human
        if not self.is_computer:
            over = False
            current_pos = pos_to_index(pygame.mouse.get_pos())
            while not over:
                for event in pygame.event.get():
                    # Get where the player clicked
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if gh.INFO_SIZE < pygame.mouse.get_pos()[0] < gh.INFO_SIZE+ 600 and \
                                gh.INFO_SIZE < pygame.mouse.get_pos()[1] < gh.INFO_SIZE + 600:
                            if valid(GameSettings.current_state, pos_to_index(pygame.mouse.get_pos()), self.number):
                                GameSettings.current_state = add(GameSettings.current_state,
                                                                 pos_to_index(pygame.mouse.get_pos()), self.number)
                                gh.paint_state(GameSettings.current_state)
                                over = True
                                # Execute the other player's move
                                if self.number == 1:
                                    GameSettings.player2.move()
                                else:
                                    GameSettings.player1.move()
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit(11)

                if pos_to_index(pygame.mouse.get_pos()) != current_pos:
                    gh.paint_state(GameSettings.current_state)
                    gh.paint_cursor(pos_to_index(pygame.mouse.get_pos()))
                    current_pos = pos_to_index(pygame.mouse.get_pos())
        else:
            # Display "THE AI IS THINKING"
            gh.show_ai_thinking()
            # Minimax algorithm
            t = Tree(GameSettings.current_state, self.number)
            t.calc_scores(self.ai_depth, self.number)
            if len(t.sons) > 0:
                move_state = t.max_son().state
                GameSettings.current_state = np.copy(move_state)
                gh.paint_state(GameSettings.current_state)
            # Execute the other player's move
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
