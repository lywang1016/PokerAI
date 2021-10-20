from deckofcards import Card, Deck

class Evaluation(object):
    def __init__(self, cards7):
        self.cards = cards7
        self.all_possible = []
        self.max_power = 0
        self.max_power_hands = []
        self.best_hand = []
        self.build_all_possible()
        self.power_info = {0:"High card",
                           1:"One pair",
                           2:"Two pairs",
                           3:"Three of a kind",
                           4:"Straight",
                           5:"Flush",
                           6:"Full house",
                           7:"Four of a kind",
                           8:"Flush and straight"}

    def build_all_possible(self):
        if self.cards != None:
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
        self.best_hand = [self.max_power_hands[0]]
        if nums > 1:
            if self.max_power == 8:
                for i in range(1, nums):
                    temp = self.flush_and_straight_compare(self.best_hand[0], self.max_power_hands[i]) 
                    if len(temp) == 1:
                        self.best_hand = temp
                    else:
                        self.best_hand.append(self.max_power_hands[i])
            if self.max_power == 7:
                for i in range(1, nums):
                    temp = self.four_of_a_kind_compare(self.best_hand[0], self.max_power_hands[i])
                    if len(temp) == 1:
                        self.best_hand = temp
                    else:
                        self.best_hand.append(self.max_power_hands[i])
            if self.max_power == 6:
                for i in range(1, nums):
                    temp = self.full_house_compare(self.best_hand[0], self.max_power_hands[i])
                    if len(temp) == 1:
                        self.best_hand = temp
                    else:
                        self.best_hand.append(self.max_power_hands[i])
            if self.max_power == 5:
                for i in range(1, nums):
                    temp = self.flush_compare(self.best_hand[0], self.max_power_hands[i])
                    if len(temp) == 1:
                        self.best_hand = temp
                    else:
                        self.best_hand.append(self.max_power_hands[i])
            if self.max_power == 4:
                for i in range(1, nums):
                    temp = self.straight_compare(self.best_hand[0], self.max_power_hands[i])
                    if len(temp) == 1:
                        self.best_hand = temp
                    else:
                        self.best_hand.append(self.max_power_hands[i])
            if self.max_power == 3:
                for i in range(1, nums):
                    temp = self.three_of_a_kind_compare(self.best_hand[0], self.max_power_hands[i])
                    if len(temp) == 1:
                        self.best_hand = temp
                    else:
                        self.best_hand.append(self.max_power_hands[i])
            if self.max_power == 2:
                for i in range(1, nums):
                    temp = self.two_pairs_compare(self.best_hand[0], self.max_power_hands[i])
                    if len(temp) == 1:
                        self.best_hand = temp
                    else:
                        self.best_hand.append(self.max_power_hands[i])
            if self.max_power == 1:
                for i in range(1, nums):
                    temp = self.one_pair_compare(self.best_hand[0], self.max_power_hands[i])
                    if len(temp) == 1:
                        self.best_hand = temp
                    else:
                        self.best_hand.append(self.max_power_hands[i])
            if self.max_power == 0:
                for i in range(1, nums):
                    temp = self.high_card_compare(self.best_hand[0], self.max_power_hands[i])
                    if len(temp) == 1:
                        self.best_hand = temp
                    else:
                        self.best_hand.append(self.max_power_hands[i])
    
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
        for i in range(5):
            if cards5[0].value == 1:
                cards5[0].value = 14
                Ace_card = cards5.pop(0)
                cards5.append(Ace_card)

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

    def high_card_compare(self, hand1, hand2):
        self.hand_sort(hand1)
        self.hand_sort(hand2)
        for i in range(4, -1, -1):
            card1 = hand1[i]
            card2 = hand2[i]
            if card1.value > card2.value:
                return [hand1]
            if card1.value < card2.value:
                return [hand2]
        return [hand1, hand2]

    def one_pair_compare(self, hand1, hand2):
        self.hand_sort(hand1)
        self.hand_sort(hand2)

        def find_pair(hand):
            for i in range(1, 5):
                if hand[i].value == hand[i-1].value:
                    return [i-1, i]
            return []
        
        pair_idxs1 = find_pair(hand1)
        pair_idxs2 = find_pair(hand2)

        if hand1[pair_idxs1[0]].value > hand2[pair_idxs2[0]].value:
            return [hand1]
        if hand1[pair_idxs1[0]].value < hand2[pair_idxs2[0]].value:
            return [hand2]
        
        hand1_left = []
        hand2_left = []
        for i in range(5):
            if i not in pair_idxs1:
                hand1_left.append(hand1[i])
            if i not in pair_idxs2:
                hand2_left.append(hand2[i])
        for i in range(2, -1, -1):
            card1 = hand1_left[i]
            card2 = hand2_left[i]
            if card1.value > card2.value:
                return [hand1]
            if card1.value < card2.value:
                return [hand2]
        return [hand1, hand2]

    def two_pairs_compare(self, hand1, hand2):
        self.hand_sort(hand1)
        self.hand_sort(hand2)

        def find_pairs(hand):
            res = []
            for i in range(1, 5):
                if hand[i].value == hand[i-1].value:
                    res.append([i-1, i]) 
            return res
        
        pair_idxs1 = find_pairs(hand1)
        pair_idxs2 = find_pairs(hand2)

        if hand1[pair_idxs1[1][0]].value > hand2[pair_idxs2[1][0]].value:
            return [hand1]
        if hand1[pair_idxs1[1][0]].value < hand2[pair_idxs2[1][0]].value:
            return [hand2]

        if hand1[pair_idxs1[0][0]].value > hand2[pair_idxs2[0][0]].value:
            return [hand1]
        if hand1[pair_idxs1[0][0]].value < hand2[pair_idxs2[0][0]].value:
            return [hand2]

        hand1_used_idx = []
        hand2_used_idx = []
        for i in range(2):
            for j in range(2):
                hand1_used_idx.append(pair_idxs1[i][j])
                hand2_used_idx.append(pair_idxs2[i][j])
        for i in range(5):
            if i not in hand1_used_idx:
                card1 = hand1[i]
            if i not in hand2_used_idx:
                card2 = hand2[i]
        if card1.value > card2.value:
            return [hand1]
        if card1.value < card2.value:
            return [hand2]
        return [hand1, hand2]

    def three_of_a_kind_compare(self, hand1, hand2):
        self.hand_sort(hand1)
        self.hand_sort(hand2)

        def find_three(hand):
            for i in range(2, 5):
                if hand[i].value == hand[i-1].value and hand[i-1].value == hand[i-2].value:
                    return [i-2, i-1, i]
            return []
        
        three_idxs1 = find_three(hand1)
        three_idxs2 = find_three(hand2)

        if hand1[three_idxs1[0]].value > hand2[three_idxs2[0]].value:
            return [hand1]
        if hand1[three_idxs1[0]].value < hand2[three_idxs2[0]].value:
            return [hand2]
        
        hand1_left = []
        hand2_left = []
        for i in range(5):
            if i not in three_idxs1:
                hand1_left.append(hand1[i])
            if i not in three_idxs2:
                hand2_left.append(hand2[i])
        for i in range(1, -1, -1):
            card1 = hand1_left[i]
            card2 = hand2_left[i]
            if card1.value > card2.value:
                return [hand1]
            if card1.value < card2.value:
                return [hand2]
        return [hand1, hand2]

    def straight_compare(self, hand1, hand2):
        self.hand_sort(hand1)
        self.hand_sort(hand2)

        last1 = hand1[4]
        last2 = hand2[4]
        max1 = last1.value
        max2 = last2.value

        if max1 == 14:
            if hand1[3].value != 13:
                max1 = 5
        if max2 == 14:
            if hand2[3].value != 13:
                max2 = 5

        if max1 > max2:
            return [hand1]
        else:
            return [hand2]

    def flush_compare(self, hand1, hand2):
        return self.high_card_compare(hand1, hand2)

    def full_house_compare(self, hand1, hand2):
        return self.three_of_a_kind_compare(hand1, hand2)

    def four_of_a_kind_compare(self, hand1, hand2):
        self.hand_sort(hand1)
        self.hand_sort(hand2)
        
        def find_four(hand):
            for i in range(3, 5):
                if hand[i].value == hand[i-1].value and hand[i-1].value == hand[i-2].value and hand[i-2].value == hand[i-3].value:
                    return [i-3, i-2, i-1, i]
            return []
        
        four_idxs1 = find_four(hand1)
        four_idxs2 = find_four(hand2)

        if hand1[four_idxs1[0]].value > hand2[four_idxs2[0]].value:
            return [hand1]
        if hand1[four_idxs1[0]].value < hand2[four_idxs2[0]].value:
            return [hand2]

        for i in range(5):
            if i not in four_idxs1:
                card1 = hand1[i]
            if i not in four_idxs2:
                card2 = hand2[i]
        if card1.value > card2.value:
            return [hand1]
        if card1.value < card2.value:
            return [hand2]
        return [hand1, hand2]

    def flush_and_straight_compare(self, hand1, hand2):
        return self.straight_compare(hand1, hand2)

    
if __name__ == '__main__': 
    cards = []
    
    card = Card('Spades', 8)
    card.show()
    cards.append(card)
    card = Card('Spades', 11)
    card.show()
    cards.append(card)
    card = Card('Hearts', 13)
    card.show()
    cards.append(card)
    card = Card('Spades', 1)
    card.show()
    cards.append(card)
    card = Card('Hearts', 1)
    card.show()
    cards.append(card)

    evaluate = Evaluation(None)
    print(evaluate.if_one_pair(cards))

    myDeck = Deck()
    myDeck.shuffle()

    cards = []
    
    card = myDeck.draw()
    # card = Card('Clubs', 7)
    card.show()
    cards.append(card)
    card = myDeck.draw()
    # card = Card('Diamonds', 7)
    card.show()
    cards.append(card)
    card = myDeck.draw()
    # card = Card('Hearts', 10)
    card.show()
    cards.append(card)
    card = myDeck.draw()
    # card = Card('Hearts', 11)
    card.show()
    cards.append(card)
    card = myDeck.draw()
    # card = Card('Hearts', 12)
    card.show()
    cards.append(card)
    card = myDeck.draw()
    # card = Card('Hearts', 13)
    card.show()
    cards.append(card)
    card = myDeck.draw()
    # card = Card('Hearts', 1)
    card.show()
    cards.append(card)

    evaluate = Evaluation(cards)
    evaluate.get_best_hand()
    print("--------------------------")
    print("Card power is: " + evaluate.power_info[evaluate.max_power])
    print("Best hand is:")
    for cards in evaluate.best_hand:
        print("!!!!!!!!!!!!!!!!!!!!!!!")
        for card in cards:
            card.show()
    

    # print("-----------Hand 1---------------")
    # cards1 = []
    # card = Card('Clubs', 8)
    # card.show()
    # cards1.append(card)
    # card = Card('Diamonds', 8)
    # card.show()
    # cards1.append(card)
    # card = Card('Spades', 8)
    # card.show()
    # cards1.append(card)
    # card = Card('Hearts', 8)
    # card.show()
    # cards1.append(card)
    # card = Card('Diamonds', 9)
    # card.show()
    # cards1.append(card)
    # print("-----------Hand 2---------------")
    # cards2 = []
    # card = Card('Clubs', 8)
    # card.show()
    # cards2.append(card)
    # card = Card('Diamonds', 8)
    # card.show()
    # cards2.append(card)
    # card = Card('Spades', 8)
    # card.show()
    # cards2.append(card)
    # card = Card('Hearts', 8)
    # card.show()
    # cards2.append(card)
    # card = Card('Diamonds', 12)
    # card.show()
    # cards2.append(card)

    # # better = evaluate.high_card_compare(cards1, cards2)
    # # better = evaluate.one_pair_compare(cards1, cards2)
    # # better = evaluate.two_pairs_compare(cards1, cards2)
    # # better = evaluate.three_of_a_kind_compare(cards1, cards2)
    # # better = evaluate.straight_compare(cards1, cards2)
    # # better = evaluate.full_house_compare(cards1, cards2)
    # better = evaluate.four_of_a_kind_compare(cards1, cards2)
    # print("--------------------------")
    # for card in better:
    #     card.show()