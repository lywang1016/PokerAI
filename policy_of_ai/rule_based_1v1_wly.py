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
            val2 = self.hand[1].value
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

    def action_should_take(self):
        return [0, 0]