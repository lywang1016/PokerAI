from deckofcards import Card, Deck

class Evaluation(object):
    def __init__(self, cards7):
        self.cards = cards7
        self.all_possible = []
        self.max_power = 0
        self.max_power_hands = []
        self.best_hand = []
        self.build_all_possible()

    def build_all_possible(self):
        if len(self.cards) == 7:
            for i in range(6):
                for j in range(i+1, 7):
                    temp = []
                    for k in range(7):
                        if k != i and k != j:
                            temp.append(self.cards[k])
                    self.all_possible.append(temp)

    def get_best_hand(self):
        self.get_max_power_hands()

        nums = len(self.max_power_hands)
        self.best_hand = self.max_power_hands[0]
        # if nums > 1:
        #     if self.max_power == 8:
        #         for i in range(1, nums):
        #             self.best_hand = flush_and_straight_compare(self.best_hand, self.max_power_hands[i])
        #     if self.max_power == 7:
        #         for i in range(1, nums):
        #             self.best_hand = four_of_a_kind_compare(self.best_hand, self.max_power_hands[i])
        #     if self.max_power == 6:
        #         for i in range(1, nums):
        #             self.best_hand = full_house_compare(self.best_hand, self.max_power_hands[i])
        #     if self.max_power == 5:
        #         for i in range(1, nums):
        #             self.best_hand = flush_compare(self.best_hand, self.max_power_hands[i])
        #     if self.max_power == 4:
        #         for i in range(1, nums):
        #             self.best_hand = straight_compare(self.best_hand, self.max_power_hands[i])
        #     if self.max_power == 3:
        #         for i in range(1, nums):
        #             self.best_hand = three_of_a_kind_compare(self.best_hand, self.max_power_hands[i])
        #     if self.max_power == 2:
        #         for i in range(1, nums):
        #             self.best_hand = two_pairs_compare(self.best_hand, self.max_power_hands[i])
        #     if self.max_power == 1:
        #         for i in range(1, nums):
        #             self.best_hand = one_pair_compare(self.best_hand, self.max_power_hands[i])
        #     if self.max_power == 0:
        #         for i in range(1, nums):
        #             self.best_hand = high_card_compare(self.best_hand, self.max_power_hands[i])
    
    def get_max_power_hands(self):
        power_dict = {8:[], 7:[], 6:[], 5:[], 4:[], 3:[], 2:[], 1:[], 0:[]}
        for test in self.all_possible:
            four_of_a_kind = self.if_four_of_a_kind(test)
            full_house = self.if_full_house(test)
            flush = self.if_flush(test)
            straight = self.if_straight(test)
            three_of_a_kind = self.if_three_of_a_kind(test)
            two_pairs = self.if_two_pairs(test)
            one_pair = self.if_one_pair(test)
            if flush and straight:
                power_dict[8].append(test)
            elif four_of_a_kind:
                power_dict[7].append(test)
            elif full_house:
                power_dict[6].append(test)
            elif flush:
                power_dict[5].append(test)
            elif straight:
                power_dict[4].append(test)
            elif three_of_a_kind:
                power_dict[3].append(test)
            elif two_pairs:
                power_dict[2].append(test)
            elif one_pair:
                power_dict[1].append(test)
            else:
                power_dict[0].append(test)

        max_power = 0
        for power in range(8, 0, -1):
            if len(power_dict[power]) > 0:
                max_power = power
                break
        
        self.max_power = max_power
        self.max_power_hands = power_dict[max_power]

        for hand in self.max_power_hands:
            self.hand_sort(hand)

    def hand_sort(self, cards5):
        for i in range(4):
            for j in range(i+1, 5):
                if cards5[i].value > cards5[j].value:
                    cards5[i], cards5[j] = cards5[j], cards5[i]

    def if_four_of_a_kind(self, cards5):
        values = {}
        for card in cards5:
            if card.value not in values:
                values[card.value] = 1
            else:
                values[card.value] += 1
        if len(values) == 2:
            for key in values:
                if values[key] == 1 or values[key] == 4:
                    return True
                else:
                    return False
        else:
            return False

    def if_full_house(self, cards5):
        values = {}
        for card in cards5:
            if card.value not in values:
                values[card.value] = 1
            else:
                values[card.value] += 1
        if len(values) == 2:
            for key in values:
                if values[key] == 2 or values[key] == 3:
                    return True
                else:
                    return False
        else:
            return False

    def if_flush(self, cards5):
        card = cards5[0]
        suit = card.suit
        for i in range(1, 5):
            card = cards5[i]
            if suit != card.suit:
                return False
        return True

    def if_straight(self, cards5):
        values = []
        for card in cards5:
           values.append(card.value) 
        values.sort()
        init_value = values[0]
        if init_value == 1:
            if values[1] == 2 and values[2] == 3 and values[3] == 4 and values[4] == 5:
                return True
            elif values[1] == 10 and values[2] == 11 and values[3] == 12 and values[4] == 13:
                return True
            else:
                return False
        else:
            for i in range(1, 5):
                if values[i] - values[i-1] != 1:
                    return False
            return True

    def if_three_of_a_kind(self, cards5):
        values = {}
        for card in cards5:
            if card.value not in values:
                values[card.value] = 1
            else:
                values[card.value] += 1
        if len(values) == 3:
            nums = []
            for key in values:
                nums.append(values[key])
            nums.sort()
            if nums == [1, 1, 3]:
                return True
            else:
                return False
        else:
            return False

    def if_two_pairs(self, cards5):
        values = {}
        for card in cards5:
            if card.value not in values:
                values[card.value] = 1
            else:
                values[card.value] += 1
        if len(values) == 3:
            nums = []
            for key in values:
                nums.append(values[key])
            nums.sort()
            if nums == [1, 2, 2]:
                return True
            else:
                return False
        else:
            return False

    def if_one_pair(self, cards5):
        values = {}
        for card in cards5:
            if card.value not in values:
                values[card.value] = 1
            else:
                values[card.value] += 1
        if len(values) == 4:
            nums = []
            for key in values:
                nums.append(values[key])
            nums.sort()
            if nums == [1, 1, 1, 2]:
                return True
            else:
                return False
        else:
            return False



    
if __name__ == '__main__': 
    # myDeck = Deck()
    # myDeck.shuffle()

    cards = []
    
    # card = myDeck.draw()
    card = Card('Clubs', 7)
    card.show()
    cards.append(card)
    # card = myDeck.draw()
    card = Card('Diamonds', 7)
    card.show()
    cards.append(card)
    # card = myDeck.draw()
    card = Card('Hearts', 5)
    card.show()
    cards.append(card)
    # card = myDeck.draw()
    card = Card('Diamonds', 6)
    card.show()
    cards.append(card)
    # card = myDeck.draw()
    card = Card('Hearts', 7)
    card.show()
    cards.append(card)
    # card = myDeck.draw()
    card = Card('Hearts', 1)
    card.show()
    cards.append(card)
    # card = myDeck.draw()
    card = Card('Hearts', 2)
    card.show()
    cards.append(card)

    evaluate = Evaluation(cards)
    # print(evaluate.if_flush(evaluate.cards))
    # print(evaluate.if_straight(evaluate.cards))
    # print(evaluate.if_three_of_a_kind(evaluate.cards))
    # print(len(evaluate.all_possible))
    evaluate.get_best_hand()
    # for hand in evaluate.max_power_hands:
    #     print("--------------------------")
    #     for card in hand:
    #         card.show()
