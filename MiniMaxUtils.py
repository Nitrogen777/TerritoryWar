import GameUtils as gu

class Tree:
    def __init__(self, state, player):
        self.sons = []
        self.state = state
        self.score = 0
        self.player = player

    # Calculate the scores
    def calc_scores(self, depth, player):
        if depth != 0:
            next_state = gu.calculate_change(self.state)
            for i in range(next_state.shape[0]):
                for j in range(next_state.shape[1]):
                    if gu.valid(next_state, (i,j), player):
                        self.add_son(gu.add(next_state, (i,j), player))
            if len(self.sons) > 0:
                for son in self.sons:
                    son.calc_scores(depth - 1, -player)
                if player == self.player:
                    self.score = self.max_son().score
                else:
                    self.score = self.min_son().score
            else:
                self.score = gu.state_score(self.state, self.player)

        else:
            self.score = gu.state_score(self.state, self.player)

    # Return the maximum tree out of an array of trees
    def max_son(self):
        max = self.sons[0].score
        maxson = self.sons[0]
        for son in self.sons:
            if son.score > max:
                max = son.score
                maxson = son
        return maxson

    # Return the minimum tree out of an array of trees
    def min_son(self):
        min = self.sons[0].score
        minson = self.sons[0]
        for son in self.sons:
            if son.score < min:
                min = son.score
                minson = son
        return minson

    def add_son(self, state):
        self.sons.append(Tree(state, self.player))

    def get_son(self, index):
        return self.sons[index]
