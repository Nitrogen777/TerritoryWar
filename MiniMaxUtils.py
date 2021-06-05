"""
This file includes classes and methods used by the AI player's algorithm.
"""
import GameUtils as gu


class Tree:
    """
    A class of tree nodes used for Minimax calculations.
    """
    def __init__(self, state, player):
        self._sons = []
        self._state = state
        self._score = 0
        self._player = player

    def calc_scores(self, depth, player):
        """
        Calculate the scores for all future turns using the minimax algorithm.
        :param depth: How many turns in advance to calculate (More turns = Slower game performance).
        :param player: The "max" player.
        """
        if depth != 0:
            next_state = gu.calculate_change(self._state)
            for i in range(next_state.shape[0]):
                for j in range(next_state.shape[1]):
                    if gu.valid(next_state, (i,j), player):
                        self.add_son(gu.add(next_state, (i,j), player))
            if len(self._sons) > 0:
                for son in self._sons:
                    son.calc_scores(depth - 1, -player)
                if player == self._player:
                    self._score = self.max_son()._score
                else:
                    self._score = self.min_son()._score
            else:
                self._score = gu.state_score(self._state, self._player)

        else:
            self._score = gu.state_score(self._state, self._player)

    def max_son(self):
        """
        :return: The tree with the highest score out of an array of trees
        """
        max = self._sons[0]._score
        maxson = self._sons[0]
        for son in self._sons:
            if son._score > max:
                max = son._score
                maxson = son
        return maxson

    def min_son(self):
        """
        :return: The tree with the lowest score out of an array of trees
        """
        min = self._sons[0]._score
        minson = self._sons[0]
        for son in self._sons:
            if son._score < min:
                min = son._score
                minson = son
        return minson

    def add_son(self, state):
        """
        Add a son to the tree
        :param state: The state that the son represents
        """
        self._sons.append(Tree(state, self._player))

    def get_son(self, index):
        """
        Get a son at a specific array index.
        :param index: The index where the array is located.
        :return: The son at the index.
        """
        return self._sons[index]
