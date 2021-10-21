from game_frame_work.deckofcards import Deck

class Classification(object):
    def __init__(self):
        self.power_info = {0:"High card",
                           1:"One pair",
                           2:"Two pairs",
                           3:"Three of a kind",
                           4:"Straight",
                           5:"Flush",
                           6:"Full house",
                           7:"Four of a kind",
                           8:"Flush and straight"}

    def classify(self, test):
        four_of_a_kind = self.if_four_of_a_kind(test)
        full_house = self.if_full_house(test)
        flush = self.if_flush(test)
        straight = self.if_straight(test)
        three_of_a_kind = self.if_three_of_a_kind(test)
        two_pairs = self.if_two_pairs(test)
        one_pair = self.if_one_pair(test)
        if flush and straight:
            return 8
        elif four_of_a_kind:
            return 7
        elif full_house:
            return 6
        elif flush:
            return 5
        elif straight:
            return 4
        elif three_of_a_kind:
            return 3
        elif two_pairs:
            return 2
        elif one_pair:
            return 1
        else:
            return 0

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

class CompareHands(object):
    def __init__(self):
        self.classifier = Classification()

    def best_hand(self, hand_list):
        if len(hand_list) < 2:
            return hand_list

        res = [hand_list[0]]
        res_idx = [0]
        for i in range(1, len(hand_list)):
            better = self.better_hand(res[0], hand_list[i])
            if len(better) == 1:
                if better[0] == hand_list[i]:
                    res = [hand_list[i]]
                    res_idx = [i]
            else:
                if hand_list[i] in better:
                    res.append(hand_list[i])
                    res_idx.append(i)

        return res, res_idx

    def better_hand(self, hand1, hand2):
        power1 = self.classifier.classify(hand1)
        power2 = self.classifier.classify(hand2)
        if power1 > power2:
            return [hand1]
        elif power2 > power1:
            return [hand2]
        else:
            if power1 == 0:
                return self.high_card_compare(hand1, hand2)
            if power1 == 1:
                return self.one_pair_compare(hand1, hand2)
            if power1 == 2:
                return self.two_pairs_compare(hand1, hand2)
            if power1 == 3:
                return self.three_of_a_kind_compare(hand1, hand2)
            if power1 == 4:
                return self.straight_compare(hand1, hand2)
            if power1 == 5:
                return self.flush_compare(hand1, hand2)
            if power1 == 6:
                return self.full_house_compare(hand1, hand2)
            if power1 == 7:
                return self.four_of_a_kind_compare(hand1, hand2)
            if power1 == 8:
                return self.flush_and_straight_compare(hand1, hand2)
        return []


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

class Cards7Evaluate(object):
    def __init__(self, cards7):
        self.cards = cards7
        self.all_possible = []
        self.build_all_possible()
        self.compare = CompareHands()
        self.best_hand, self.best_idx = self.compare.best_hand(self.all_possible)
        self.max_power = -1
        self.max_power_str = ""
        if len(self.best_hand) > 0:
            self.max_power = self.compare.classifier.classify(self.best_hand[0])
            self.max_power_str = self.compare.classifier.power_info[self.max_power]

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

    
if __name__ == '__main__': 
    # ## Test 1: Test Classification Class
    # cards = []
    # card = Card('Spades', 5)
    # card.show()
    # cards.append(card)
    # card = Card('Spades', 4)
    # card.show()
    # cards.append(card)
    # card = Card('Hearts', 3)
    # card.show()
    # cards.append(card)
    # card = Card('Spades', 1)
    # card.show()
    # cards.append(card)
    # card = Card('Hearts', 2)
    # card.show()
    # cards.append(card)

    # classifier = Classification()
    # print(classifier.power_info[classifier.classify(cards)])



    # ## Test 2: Test CompareHands Class
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

    # hand_list = [cards2, cards1, cards2, cards1, cards2]
    # compare = CompareHands()
    # best_hand = compare.best_hand(hand_list)
    # for i in range(len(best_hand)):
    #     hand = best_hand[i]
    #     print("----------No. " + str(i+1) + " hand----------")
    #     for card in hand:
    #         card.show()





    ## Test 3: Test Cards7Evaluate Class
    myDeck = Deck()
    myDeck.shuffle()
    cards = []
    for i in range(7):
        card = myDeck.draw()
        card.show()
        cards.append(card)

    evaluate = Cards7Evaluate(cards)
    print("Card power is: " + evaluate.max_power_str)
    print("Best hand is:")
    for cards in evaluate.best_hand:
        print("!!!!!!!!!!!!!!!!!!!!!!!")
        for card in cards:
            card.show()
    

    