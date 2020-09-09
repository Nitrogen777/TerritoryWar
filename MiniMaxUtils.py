import GameUtils as gu

class Tree:
    def __init__(self, state, player):
        self.sons = []
        self.state = state
        self.score = 0
        self.player = player

    def calc_scores(self, depth, player):
        if depth != 0:
            next_state = gu.calculate_change(self.state)
            next_board = next_state.board
            for i in range(next_board.shape[0]):
                for j in range(next_board.shape[1]):
                    if gu.valid(next_state, (i,j), player):
                        self.add_son(gu.add(next_state, (i,j), player))
            if len(self.sons) > 0:
                for son in self.sons:
                    son.calc_scores(depth - 1, -player)
                self.score = self.max_son().score
            else:
                self.score = gu.state_score(self.state, self.player)
        else:
            self.score = gu.state_score(self.state, self.player)

    def max_son(self):
        max = self.sons[0].score
        maxson = self.sons[0]
        for son in self.sons:
            if son.score > max:
                max = son.score
                maxson = son
        return maxson

    def add_son(self, state):
        self.sons.append(Tree(state, self.player))

    def get_son(self, index):
        return self.sons[index]
