from policy_of_ai.strategy import Strategy

class RuleBased1V1(Strategy):
    def __init__(self):
        super(RuleBased1V1, self).__init__()
        self.hand_power = {5: [[1,1,0], [13,13,0], [12,12,0], [1,13,0], [1,13,1]],
                           4: [[11,11,0], [10,10,0], [1,12,0], [1,12,1], [12,13,0], [12,13,1], [1,11,1]],
                           3: [[1,2,1], [1,3,1], [1,4,1], [1,5,1], [1,6,1], [1,7,1], [1,8,1], [1,9,1],
                               [1,10,1], [1,11,0], [11,13,0], [11,13,1], [11,12,0], [11,12,1], [10,13,1],
                               [9,9,0], [8,8,0]],
                           2: [[7,7,0], [6,6,0], [5,5,0], [4,4,0], [3,3,0], [2,2,0], [5,6,1], [6,7,1],
                               [7,8,1], [8,9,1], [9,10,1], [10,11,1], [8,10,1], [8,11,1], [9,12,1], 
                               [10,12,1], [9,13,1], [10,11,0], [10,12,0], [10,13,0], [1,10,0], [1,9,0],
                               [1,8,0], [1,7,0], [1,6,0], [1,5,0]],
                           1: [[1,2,0], [1,3,0], [1,4,0], [3,4,1], [4,5,1], [4,6,1], [5,7,1], [6,8,1],
                               [6,9,1], [7,9,1], [7,10,1], [8,11,1], [8,12,1], [8,13,1], [5,6,0], [6,7,0],
                               [6,8,0], [7,8,0], [7,9,0], [8,9,0], [8,10,0], [9,10,0], [8,11,0], [9,11,0],
                               [9,12,0], [9,13,0]]}

    def hand_card_encode(self):
        if self.hand != None:
            val1 = self.hand[0].value
            if val1 > 13:
                val1 = 1
            val2 = self.hand[1].value
            if val2 > 13:
                val2 = 1
            suit1 = self.hand[0].suit
            suit2 = self.hand[1].suit
            return [min(val1, val2), max(val1, val2), int(suit1==suit2)]
        else:
            return []
    
    def hand_card_power(self):
        encode = self.hand_card_encode()
        if len(encode) > 0:
            for power in range(5, 0, -1):
                if encode in self.hand_power[power]:
                    return power
        return 0

    def before_flop_action_should_take(self):
        # print("Bot have :")
        # for card in self.hand:
        #     card.show()

        power = self.hand_card_power()
        # print("Bot hand power is " + str(power))

        if power == 0:
            if self.chips_to_call == 0:
                return [1, 0] # check
            else:
                return [0, 0] # fold
        elif power == 1:
            if self.chips_to_call == 0:
                return [1, 0] # check
            else:
                call_pow = self.chips_to_call / self.bb
                if call_pow > 3:
                    return [0, 0] # fold
                else:
                    return [1, self.chips_to_call] # call
        elif power == 2:
            if self.chips_to_call == 0:
                return [1, 0] # check
            else:
                call_pow = self.chips_to_call / self.bb
                if call_pow > 9:
                    return [0, 0] # fold
                else:
                    return [1, self.chips_to_call] # call
        elif power == 3:
            return [1, self.chips_to_call] # check/call
        elif power == 4:
            last_log = self.game_log[0][-1]
            pot = last_log.pot
            if self.chips_to_call > 12*self.bb:
                return [1, self.chips_to_call] # call
            else:
                return [2, max(3*self.min_raise, int(0.8*pot))] # raise
        elif power == 5:
            last_log = self.game_log[0][-1]
            pot = last_log.pot
            opponent_chip = last_log.chip_left
            bet = min(4*self.min_raise, int(5*pot), opponent_chip)
            if bet <= self.chips_to_call:
                return [1, self.chips_to_call] # call
            else:
                return [2, bet] # raise
        else: # error happen, suppose not happen! just fold
            return [0, 0] # fold

    def flop_action_should_take(self):
        return [1, self.chips_to_call]

    def turn_action_should_take(self):
        return [1, self.chips_to_call]

    def river_action_should_take(self):
        return [1, self.chips_to_call]

    def action_should_take(self):
        if len(self.flop) == 0: # Before flop
            return self.before_flop_action_should_take()
        elif self.turn == None: # Flop
            return self.flop_action_should_take()
        elif self.river == None: # Turn
            return self.turn_action_should_take()
        else:                     # River
            return self.river_action_should_take()