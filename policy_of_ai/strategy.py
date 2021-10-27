class Strategy(object):
    def __init__(self):
        self.my_name = ''
        self.chips = 0
        self.hand = []
        self.flop = []
        self.turn = None
        self.river = None
        self.bfo = []
        self.afo = []
        self.game_log = []
        self.chips_to_call = 0
        self.min_raise = 0
        self.sb = 0
        self.bb = 0

    def load_attributes(self, my_name, chips, hand, flop, turn, river, bfo, afo, game_log, chips_to_call, min_raise):
        self.my_name = my_name
        self.chips = chips
        self.hand = hand
        self.flop = flop
        self.turn = turn
        self.river = river
        self.bfo = bfo
        self.afo = afo
        self.game_log = game_log
        self.chips_to_call = chips_to_call
        self.min_raise = min_raise
        for log in self.game_log[0]:
            if log.action == "small blind":
                self.sb = log.chip_bet
            if log.action == "big blind":
                self.bb = log.chip_bet

    def action_should_take(self):
        return [1, self.chips_to_call]