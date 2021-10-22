from policy_of_ai.strategy import Strategy

class AlwaysFold(Strategy):
    def __init__(self, my_name, chips, hand, flop, turn, river, bfo, afo, game_log, chips_to_call, min_raise):
        super(AlwaysFold, self).__init__(my_name, chips, hand, flop, turn, river, bfo, afo, game_log, chips_to_call, min_raise)

    def action_should_take(self):
        return [0, 0]

class AlwaysCall(Strategy):
    def __init__(self, my_name, chips, hand, flop, turn, river, bfo, afo, game_log, chips_to_call, min_raise):
        super(AlwaysCall, self).__init__(my_name, chips, hand, flop, turn, river, bfo, afo, game_log, chips_to_call, min_raise)

    def action_should_take(self):
        return [1, self.chips_to_call]

class AlwaysRaise(Strategy):
    def __init__(self, my_name, chips, hand, flop, turn, river, bfo, afo, game_log, chips_to_call, min_raise):
        super(AlwaysRaise, self).__init__(my_name, chips, hand, flop, turn, river, bfo, afo, game_log, chips_to_call, min_raise)

    def action_should_take(self):
        return [2, self.min_raise]
