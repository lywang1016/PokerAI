import numpy as np
from icecream import ic
from policy_of_ai.strategy import Strategy
from game_frame_work.deckofcards import Card, Deck
from game_frame_work.evaluation import Classification, CompareHands, Cards7Evaluate

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
                               [9,12,0], [9,13,0]],
                           0: [[2,3,0], [2,4,0], [2,5,0], [2,6,0], [2,7,0], [2,8,0], [2,9,0], [2,10,0],
                               [2,11,0], [2,12,0], [2,13,0], [2,3,1], [2,4,1], [2,5,1], [2,6,1], [2,7,1], 
                               [2,8,1], [2,9,1], [2,10,1], [2,11,1], [2,12,1], [2,13,1], [3,4,0], [3,5,0], 
                               [3,6,0], [3,7,0], [3,8,0], [3,9,0], [3,10,0], [3,11,0], [3,12,0], [3,13,0],
                               [3,5,1], [3,6,1], [3,7,1], [3,8,1], [3,9,1], [3,10,1], [3,11,1], [3,12,1], 
                               [3,13,1], [4,5,0], [4,6,0], [4,7,0], [4,8,0], [4,9,0], [4,10,0], [4,11,0], 
                               [4,12,0], [4,13,0], [4,7,1], [4,8,1], [4,9,1], [4,10,1], [4,11,1], [4,12,1], 
                               [4,13,1], [5,7,0], [5,8,0], [5,9,0], [5,10,0], [5,11,0], [5,12,0], [5,13,0],
                               [5,8,1], [5,9,1], [5,10,1], [5,11,1], [5,12,1], [5,13,1], [6,9,0], [6,10,0],
                               [6,11,0], [6,12,0], [6,13,0], [6,10,1], [6,11,1], [6,12,1], [6,13,1], [7,10,0], 
                               [7,11,0], [7,12,0], [7,13,0], [7,11,1], [7,12,1], [7,13,1], [8,12,0], [8,13,0]]}

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
    
    def hand_card_decode(self, code):
        if len(code) > 0:
            val1 = code[0]
            if val1 > 13:
                val1 = 1
            val2 = code[1]
            if val2 > 13:
                val2 = 1
            suit_flag = code[2]
            suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
            if val1 == val2:
                res = []
                for i in range(3):
                    for j in range(i+1, 4):
                        suit1 = suits[i]
                        suit2 = suits[j]
                        card1 = Card(suit1, val1)
                        card2 = Card(suit2, val1)
                        res.append([card1, card2])
                return res
            else:
                if suit_flag:
                    res = []
                    for suit in suits:
                        card1 = Card(suit, val1)
                        card2 = Card(suit, val2)
                        res.append([card1, card2])
                    return res
                else:
                    res = []
                    for i in range(3):
                        for j in range(i+1, 4):
                            suit1 = suits[i]
                            suit2 = suits[j]
                            card1 = Card(suit1, val1)
                            card2 = Card(suit2, val2)
                            res.append([card1, card2])
                            card1 = Card(suit2, val1)
                            card2 = Card(suit1, val2)
                            res.append([card1, card2])
                    return res
        else:
            return None
    
    def my_hand_card_power(self):
        encode = self.hand_card_encode()
        if len(encode) > 0:
            for power in range(5, 0, -1):
                if encode in self.hand_power[power]:
                    return power
        return 0

    def preflop_analyze(self):
        # just assume is log before flop is done
        # return opponent hand power range, opponent range, my range, I open?
        log_before_flop = self.game_log[0]
        if self.my_name == self.bfo[0]: # I'm sb
            log3 = log_before_flop[2] # My action
            log4 = log_before_flop[3]
            if log3.action == 'call':
                if log4.action == 'raise':
                    return [2,3,4,5], [1,10,11,12,13], \
                           [6,7,8,9,10,11,12], False
                else:
                    return [0,1,2], [2,3,4,5,6,7,8,9], \
                           [2,3,4,5,6,7,8,9], False
            if log3.action == 'raise':
                if log4.action == 'raise':
                    return [4,5], [1,10,11,12,13], \
                           [8,9,10,11,12,13,1], False
                else:
                    return [2,3,4], [6,7,8,9,10,11,12], \
                           [8,9,10,11,12,13,1], True
        else:                           # I'm bb
            log3 = log_before_flop[2] 
            log4 = log_before_flop[3] # My action
            if log3.action == 'call':
                if log4.action == 'raise':
                    log5 = log_before_flop[4]
                    if log5.action == 'call':
                        return [1,2,3], [6,7,8,9,10,11,12], \
                               [8,9,10,11,12,13,1], True
                    if log5.action == 'raise':
                        return [2,3,4], [1,6,7,8,9,10,11,12,13], \
                               [8,9,10,11,12,13,1], False
                else:
                    return [0,1,2], [2,3,4,5,6,7,8,9], \
                           [2,3,4,5,6,7,8,9], False
            if log3.action == 'raise':
                if log4.action == 'raise':
                    log5 = log_before_flop[4]
                    if log5.action == 'call':
                        return [3,4,5], [8,9,10,11,12,13,1], \
                               [8,9,10,11,12,13,1], False
                    if log5.action == 'raise':
                        return [4,5], [10,11,12,13,1], \
                               [10,11,12,13,1], True
                else:
                    return [2,3,4,5], [8,9,10,11,12,13,1], \
                           [6,7,8,9,10,11,12], False

    def opponent_hand_card_pool(self, powers):
        res = []
        for power in powers:
            codes = self.hand_power[power]
            for code in codes:
                temp_cards = self.hand_card_decode(code)
                for temp in temp_cards:
                    res.append(temp)

        known_cards = []
        if len(self.hand) != 0:
            known_cards.append(self.hand[0])
            known_cards.append(self.hand[1])
        if len(self.flop) != 0:
            known_cards.append(self.flop[0])
            known_cards.append(self.flop[1])
            known_cards.append(self.flop[2])
        if self.turn != None:
            known_cards.append(self.turn)
        if self.river != None: 
            known_cards.append(self.river)

        final_res = []
        for hand_cards in res:
            card1 = hand_cards[0]
            card2 = hand_cards[1]
            good_flag = True
            for i in range(len(known_cards)):
                known_card = known_cards[i]
                if card1.value == known_card.value and card1.suit == known_card.suit:
                    good_flag = False
                if card2.value == known_card.value and card2.suit == known_card.suit:
                    good_flag = False
            if good_flag:
                final_res.append(hand_cards)

        return final_res

    def flop_approximate_win_rate(self, my_current_power, ev):
        if len(self.flop) > 0:
            if my_current_power > 6:
                return 1
            elif my_current_power == 6:
                return 0.95
            elif my_current_power == 5:
                return 0.9
            elif my_current_power == 4:
                return 0.85
            elif my_current_power == 3:
                return 0.8
            elif my_current_power == 2:
                return 0.751 # call if 3*pot
            else: # on the way
                card5 = [self.hand[0],self.hand[1],self.flop[0],self.flop[1],self.flop[2]]
                outs = []
                deck = Deck()
                # kick the cards in known_cards
                cards_left = []
                for card in deck.cards:
                    good_flag = True
                    for i in range(len(card5)):
                        known_card = card5[i]
                        if card.value == known_card.value and card.suit == known_card.suit:
                            good_flag = False
                            break
                    if good_flag:
                        cards_left.append(card)
                # deal with wait flush
                flush_dict = {}
                for card in card5:
                    suit = card.suit
                    if suit not in flush_dict:
                        flush_dict[suit] = 1
                    else:
                        flush_dict[suit] += 1
                flush_suit = None
                for suit in flush_dict:
                    if flush_dict[suit] == 4:
                        flush_suit = suit
                if flush_suit != None:
                    for card in cards_left:
                        if card.suit == flush_suit:
                            if card.value == 14:
                                card.value = 1
                            outs.append(card)
                # deal with wait straight
                for i in range(5):
                    for card in cards_left:
                        test_list5 = [card]
                        for j in range(5):
                            if i != j:
                                test_list5.append(card5[j])
                        if ev.if_straight(test_list5):
                            flag = True
                            if card.value == 14:
                                card.value = 1
                            for k in range(len(outs)):
                                if card.value == outs[k].value and card.suit == outs[k].suit:
                                    flag = False # card already in outs
                                    break
                            if flag:
                                outs.append(card)
                # deal with wait set
                if my_current_power == 1:
                    val1 = self.hand[0].value
                    val2 = self.hand[1].value
                    if val1 == 14:
                        val1 = 1
                    if val2 == 14:
                        val2 = 1
                    fval1 = self.flop[0].value
                    fval2 = self.flop[1].value
                    fval3 = self.flop[2].value
                    if fval1 == 14:
                        fval1 = 1
                    if fval2 == 14:
                        fval2 = 1
                    if fval3 == 14:
                        fval3 = 1
                    target_val = 0
                    if val1 == val2 or val1 == fval1 or val1 == fval2 or val1 == fval3:
                        target_val = val1
                    if val2 == fval1 or val2 == fval2 or val2 == fval3:
                        target_val = val2
                    if target_val != 0: # find target val cards in left
                        for card in cards_left:
                            if card.value == 14:
                                card.value = 1
                            if card.value == target_val:
                                flag = True
                                for k in range(len(outs)):
                                    if card.value == outs[k].value and card.suit == outs[k].suit:
                                        flag = False # card already in outs
                                        break
                                if flag:
                                    outs.append(card)
                if len(outs) == 0:
                    return 0.1
                else:
                    for temp in outs:
                        temp.show()
                    return float(len(outs)*4/100)
        else:
            return 0

    def get_win_rate(self, opponent_hands):
        case_num = 0
        i_win_num = 0
        compare = CompareHands()
        for oc in opponent_hands:
            known_cards = [oc[0],oc[1],self.hand[0],self.hand[1]]
            deal_num = 5 # how many cards to be deal
            if len(self.flop) > 0:
                for i in range(3):
                    known_cards.append(self.flop[i])
                deal_num = 2
            if self.turn != None:
                known_cards.append(self.turn)
                deal_num = 1
            if self.river != None:
                known_cards.append(self.river)
                deal_num = 0

            deck = Deck()
            # kick the cards in known_cards
            cards_left = []
            for card in deck.cards:
                good_flag = True
                for i in range(len(known_cards)):
                    known_card = known_cards[i]
                    if card.value == known_card.value and card.suit == known_card.suit:
                        good_flag = False
                        break
                if good_flag:
                    cards_left.append(card)
            
            # deal cards num need to deal
            if deal_num == 2:
                # 'accurate' solution, but takes too long
                for i in range(len(cards_left)-1):
                    for j in range(i+1, len(cards_left)):
                        case_num += 1
                        my_all_cards = [self.hand[0],self.hand[1], \
                                        self.flop[0],self.flop[1],self.flop[2], \
                                        cards_left[i],cards_left[j]]
                        op_all_cards = [oc[0],oc[1], \
                                        self.flop[0],self.flop[1],self.flop[2], \
                                        cards_left[i],cards_left[j]]
                        my_evaluate = Cards7Evaluate(my_all_cards)
                        op_evaluate = Cards7Evaluate(op_all_cards)
                        list_cards = [my_evaluate.best_hand[0], op_evaluate.best_hand[0]]
                        best_hand, best_idx = compare.best_hand(list_cards)
                        if len(best_idx) == 2:
                            i_win_num += 0.5
                        else:
                            if best_idx[0] == 0: # I win
                                i_win_num += 1
            if deal_num == 1:
                for i in range(len(cards_left)):
                    case_num += 1
                    my_all_cards = [self.hand[0],self.hand[1], \
                                    self.flop[0],self.flop[1],self.flop[2], \
                                    cards_left[i],self.turn]
                    op_all_cards = [oc[0],oc[1], \
                                    self.flop[0],self.flop[1],self.flop[2], \
                                    cards_left[i],self.turn]
                    my_evaluate = Cards7Evaluate(my_all_cards)
                    op_evaluate = Cards7Evaluate(op_all_cards)
                    list_cards = [my_evaluate.best_hand[0], op_evaluate.best_hand[0]]
                    best_hand, best_idx = compare.best_hand(list_cards)
                    if len(best_idx) == 2:
                        i_win_num += 0.5
                    else:
                        if best_idx[0] == 0: # I win
                            i_win_num += 1
            if deal_num == 0:
                case_num += 1
                my_all_cards = [self.hand[0],self.hand[1], \
                                self.flop[0],self.flop[1],self.flop[2], \
                                self.river,self.turn]
                op_all_cards = [oc[0],oc[1], \
                                self.flop[0],self.flop[1],self.flop[2], \
                                self.river,self.turn]
                my_evaluate = Cards7Evaluate(my_all_cards)
                op_evaluate = Cards7Evaluate(op_all_cards)
                list_cards = [my_evaluate.best_hand[0], op_evaluate.best_hand[0]]
                best_hand, best_idx = compare.best_hand(list_cards)
                if len(best_idx) == 2:
                    i_win_num += 0.5
                else:
                    if best_idx[0] == 0: # I win
                        i_win_num += 1
        if case_num > 0:
            return float(i_win_num/case_num)
        else:
            return 0

    def preflop_action_should_take(self):
        print("Bot have :")
        for card in self.hand:
            card.show()

        power = self.my_hand_card_power()

        val1 = self.hand[0].value
        val2 = self.hand[1].value
        if val1 == 1:
            val1 = 14
        if val2 == 1:
            val2 = 14

        if power == 0:
            if self.chips_to_call == 0:
                rd = np.random.rand()
                if rd < 0.7: # 70 percent just check
                    return [1, 0]
                else: # raise if have big
                    if val1 > 11 or val2 > 11:
                        raise_pow = np.random.randint(low=4, high=6, size=1)
                        return [2, raise_pow[0]*self.bb]
                    else:
                        return [1, 0]
            else:
                call_pow = self.chips_to_call / self.bb
                if call_pow > 4:
                    return [0, 0] # fold
                elif call_pow > 2:
                    rd = np.random.rand()
                    if rd < 0.2: # 20 percent call
                        return [1, self.chips_to_call]
                    else:
                        return [0, 0] # fold
                else:
                    return [1, self.chips_to_call] # call min raise 
        elif power == 1:
            if self.chips_to_call == 0:
                rd = np.random.rand()
                if rd < 0.5: # 50 percent just check
                    return [1, 0]
                else: # raise if have big
                    if val1 > 11 or val2 > 11:
                        raise_pow = np.random.randint(low=4, high=6, size=1)
                        return [2, raise_pow[0]*self.bb]
                    else:
                        return [1, 0]
            else:
                call_pow = self.chips_to_call / self.bb
                if call_pow > 8:
                    if val1 > 12 or val2 > 12:
                        return [1, self.chips_to_call]
                    else:
                        return [0, 0] # fold
                elif call_pow > 5:
                    rd = np.random.rand()
                    if rd < 0.2: # 20 percent call
                        return [1, self.chips_to_call]
                    else:
                        if val1 > 11 or val2 > 11:
                            return [1, self.chips_to_call]
                        else:
                            return [0, 0] # fold
                else:
                    return [1, self.chips_to_call] # call
        elif power == 2:
            if self.chips_to_call == 0:
                rd = np.random.rand()
                if rd < 0.3: # 30 percent just check
                    return [1, 0]
                else: # raise if have big
                    if val1 > 11 or val2 > 11:
                        raise_pow = np.random.randint(low=4, high=6, size=1)
                        return [2, raise_pow[0]*self.bb]
                    else:
                        return [1, 0]
            else:
                call_pow = self.chips_to_call / self.bb
                if call_pow > 12:
                    if val1 > 12 or val2 > 12:
                        return [1, self.chips_to_call]
                    else:
                        return [0, 0] # fold
                elif call_pow > 8:
                    rd = np.random.rand()
                    if rd < 0.2: # 20 percent call
                        return [1, self.chips_to_call]
                    else:
                        if val1 > 11 or val2 > 11:
                            return [1, self.chips_to_call]
                        else:
                            return [0, 0] # fold
                else:
                    return [1, self.chips_to_call] # call
        elif power == 3:
            call_pow = self.chips_to_call / self.bb
            if call_pow < 4:
                rd = np.random.rand()
                if rd < 0.1: # 10 percent just call
                    return [1, self.chips_to_call]
                else:
                    raise_pow = np.random.randint(low=4, high=6, size=1)
                    return [2, raise_pow[0]*self.bb] # raise
            else:
                if call_pow < 12:
                    if val1 > 11 or val2 > 11:
                        return [2, self.min_raise] # raise
                    else:
                        return [1, self.chips_to_call] # call
                else:
                    return [1, self.chips_to_call] # call
        elif power == 4:
            last_log = self.game_log[0][-1]
            pot = last_log.pot
            if self.chips_to_call == 0:
                raise_pow = np.random.randint(low=4, high=6, size=1)
                return [2, raise_pow[0]*self.bb]
            elif self.chips_to_call > 20*self.bb:
                return [1, self.chips_to_call] # call
            elif self.chips_to_call > 10*self.bb:
                rd = np.random.rand()
                if rd < 0.4: # 40 percent just call
                    return [1, self.chips_to_call]
                else:
                    return [2, max(2*self.min_raise, int(0.8*pot))] # raise
            else:
                rd = np.random.rand()
                if rd < 0.1: # 10 percent just call
                    return [1, self.chips_to_call]
                else:
                    return [2, max(2*self.min_raise, int(0.8*pot))] # raise
        elif power == 5:
            if self.chips <= self.chips_to_call:
                return [1, self.chips_to_call] # call
            last_log = self.game_log[0][-1]
            pot = last_log.pot
            opponent_chip = last_log.chip_left
            if self.chips_to_call == 0:
                raise_pow = np.random.randint(low=4, high=6, size=1)
                return [2, raise_pow[0]*self.bb]
            elif self.chips_to_call > 10*self.bb and self.chips_to_call < 20*self.bb: 
                rd = np.random.rand()
                if rd < 0.3: # 30 percent just call
                    return [1, self.chips_to_call]
                else:
                    bet = min(2*self.min_raise, int(5*pot), opponent_chip)
                    if bet <= self.chips_to_call:
                        return [1, self.chips_to_call] # call
                    else:
                        return [2, bet] # raise
            else: # raise
                bet = min(2*self.min_raise, int(5*pot), opponent_chip)
                if bet <= self.chips_to_call:
                    return [1, self.chips_to_call] # call
                else:
                    return [2, bet] # raise

        else: # error happen, suppose not happen! just fold
            return [0, 0] # fold

    def flop_action_should_take(self):
        opponent_hand_power, opponent_range, my_range, i_open = self.preflop_analyze()
        ev = Classification()
        card5 = [self.hand[0],self.hand[1],self.flop[0],self.flop[1],self.flop[2]]
        my_current_power = ev.classify(card5)
        win_rate = self.flop_approximate_win_rate(my_current_power, ev)
        ic(win_rate)

        if self.afo[0] == self.my_name: # I take action first
            if self.chips_to_call == 0: # First action
                if i_open: # I open in preflop, consider if c-bet
                    num_my_range = 0
                    num_opponent_range = 0
                    for i in range(3):
                        card = self.flop[i]
                        if card.value in my_range:
                            num_my_range += 1
                        if card.value in opponent_range:
                            num_opponent_range += 1
                    current_pot = self.game_log[0][-1].pot
                    if num_my_range >= num_opponent_range: # c-bet, estimate a bet value
                        return [2, int(0.35*current_pot)]
                    else: # 50 percent c-bet
                        rd = np.random.rand()
                        if rd > 0.5:
                            return [2, int(0.3*current_pot)]
                        else:
                            return [1, self.chips_to_call]
                else: # I didn't open, just check
                    return [1, self.chips_to_call]
            else: # I action, opponent raise, now my turn, consider call or fold
                if i_open: # I open in preflop
                    if my_current_power > 2: # got someting better than two pairs just call
                        return [1, self.chips_to_call]
                    else:
                        num_my_range = 0
                        num_opponent_range = 0
                        for i in range(3):
                            card = self.flop[i]
                            if card.value in my_range:
                                num_my_range += 1
                            if card.value in opponent_range:
                                num_opponent_range += 1
                        if num_my_range < num_opponent_range: # 80 percent fold
                            rd = np.random.rand()
                            if rd > 0.8:
                                return [0, 0]
                            else:
                                return [1, self.chips_to_call]
                        else: # just call since I open in preflop
                            return [1, self.chips_to_call]
                else: # I didn't open, check my situation
                    if my_current_power > 1: # got someting better than one pair just call
                        return [1, self.chips_to_call]
                    else: # calculate win pob and compare with chip to call
                        current_pot = self.game_log[1][-1].pot
                        odds = self.chips_to_call / (self.chips_to_call + current_pot)
                        # win_rate = self.get_win_rate(opponent_hands)
                        win_rate = self.flop_approximate_win_rate(my_current_power, ev)
                        if win_rate > odds:
                            return [1, self.chips_to_call] # call
                        else:
                            return [0, 0] # fold
        else: # opponent take action first
            if self.chips_to_call == 0: # opponent check
                if i_open: # I open in preflop, consider if c-bet
                    num_my_range = 0
                    num_opponent_range = 0
                    for i in range(3):
                        card = self.flop[i]
                        if card.value in my_range:
                            num_my_range += 1
                        if card.value in opponent_range:
                            num_opponent_range += 1
                    current_pot = self.game_log[1][-1].pot
                    if num_my_range >= num_opponent_range: # c-bet, estimate a bet value
                        return [2, int(0.35*current_pot)]
                    else: # 50 percent c-bet
                        rd = np.random.rand()
                        if rd > 0.5:
                            return [2, int(0.3*current_pot)]
                        else:
                            return [1, self.chips_to_call]
                else: # I didn't open, if got some thing good, 50 percent donk
                    if my_current_power > 1: # got someting better than one pair
                        rd = np.random.rand()
                        if rd > 0.5:
                            current_pot = self.game_log[1][-1].pot
                            return [2, int(0.3*current_pot)]
                        else:
                            return [1, self.chips_to_call]
                    else: # check
                        return [1, self.chips_to_call]
            else: # opponent raise
                if i_open: # I open in preflop, and opponent donk
                    if my_current_power > 2: # got someting better than two pairs, 3-bet
                        current_pot = self.game_log[1][-1].pot
                        return [2, int(0.9*current_pot)]
                    else:
                        num_my_range = 0
                        num_opponent_range = 0
                        for i in range(3):
                            card = self.flop[i]
                            if card.value in my_range:
                                num_my_range += 1
                            if card.value in opponent_range:
                                num_opponent_range += 1
                        if num_my_range < num_opponent_range: # 80 percent fold
                            rd = np.random.rand()
                            if rd > 0.8:
                                return [0, 0]
                            else:
                                return [1, self.chips_to_call]
                        else: # just call since I open in preflop
                            return [1, self.chips_to_call]
                else: # I didn't open, consider call or fold
                    if my_current_power > 1: # got someting better than one pair just call
                        return [1, self.chips_to_call]
                    else: # calculate win pob and compare with chip to call
                        current_pot = self.game_log[1][-1].pot
                        odds = self.chips_to_call / (self.chips_to_call + current_pot)
                        # win_rate = self.get_win_rate(opponent_hands)
                        win_rate = self.flop_approximate_win_rate(my_current_power, ev)
                        if win_rate > odds:
                            return [1, self.chips_to_call] # call
                        else:
                            return [0, 0] # fold

    def turn_action_should_take(self):
        opponent_hand_power, opponent_range, my_range, i_open = self.preflop_analyze()
        opponent_hands = self.opponent_hand_card_pool(opponent_hand_power)
        win_rate = self.get_win_rate(opponent_hands)
        ic(win_rate)
        return [1, self.chips_to_call]

    def river_action_should_take(self):
        opponent_hand_power, opponent_range, my_range, i_open = self.preflop_analyze()
        opponent_hands = self.opponent_hand_card_pool(opponent_hand_power)
        win_rate = self.get_win_rate(opponent_hands)
        ic(win_rate)
        return [1, self.chips_to_call]

    def action_should_take(self):
        if len(self.flop) == 0: # Preflop
            for i in range(2):
                if self.hand[i].value == 14:
                    self.hand[i].value = 1
            return self.preflop_action_should_take()
        elif self.turn == None: # Flop
            for i in range(2):
                if self.hand[i].value == 14:
                    self.hand[i].value = 1
            for i in range(3):
                if self.flop[i].value == 14:
                    self.flop[i].value = 1
            return self.flop_action_should_take()
        elif self.river == None: # Turn
            for i in range(2):
                if self.hand[i].value == 14:
                    self.hand[i].value = 1
            for i in range(3):
                if self.flop[i].value == 14:
                    self.flop[i].value = 1
            if self.turn.value == 14:
                    self.turn.value = 1
            return self.turn_action_should_take()
        else:                     # River
            for i in range(2):
                if self.hand[i].value == 14:
                    self.hand[i].value = 1
            for i in range(3):
                if self.flop[i].value == 14:
                    self.flop[i].value = 1
            if self.turn.value == 14:
                    self.turn.value = 1
            if self.river.value == 14:
                    self.river.value = 1
            return self.river_action_should_take()