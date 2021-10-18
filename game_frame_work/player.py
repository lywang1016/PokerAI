from deckofcards import Card, Deck
from evaluation import Evaluation

class Player(object):
    def __init__(self, name, chips, is_ai):
        self.name = name
        self.chips = chips
        self.flop = []
        self.turn = None
        self.river = None
        self.position = None
        self.sb = 0
        self.bb = 0
        self.round_bet = 0
        self.chips_to_call = 0
        self.min_raise = 0
        self.status = 0
        self.seat_num = -1
        self.join = 0
        self.is_ai = is_ai
        self.action_def = {0:"Fold",
                           1:"Check/Call",
                           2:"Raise"}
        self.__hand = []
        self.__all_cards = []
    
    def print_player_info(self):
        self.say_hello()
        self.show_chips()
        self.show_hand()
        print(self.name + "'s position is: " + str(self.position))
        print(self.name + "'s seat number is: " + str(self.seat_num))
        print(self.name + "'s status is: " + str(self.status))

    def join_game_application(self):
        self.join = 1
    
    def leave_game_application(self):
        self.join = 0

    def say_hello(self):
        print("Hi my name is " + self.name)
        return self.name

    def show_hand(self):
        print(self.name + "'s hand cards are:")
        for card in self.__hand:
            card.show()
        return self.__hand
    
    def show_chips(self):
        print(self.name + " have " + str(self.chips) + " chips")
        return self.chips

    def set_game_size(self, game_size):
        self.sb = game_size[0]
        self.bb = game_size[1]
    
    def set_your_position(self, position):
        self.position = position
        if position == 0:
            self.chips -= self.sb
            self.round_bet += self.sb
            return self.sb
        if position == 1:
            self.chips -= self.bb
            self.round_bet += self.bb
            return self.bb
        return 0

    def win_pot(self, pot_size):
        self.chips += pot_size
        self.status = 0
        self.round_bet = 0

    def show_best_hand(self):
        if len(self.__all_cards) == 7:
            evaluate = Evaluation(self.__all_cards)
            evaluate.get_best_hand()
            print("My card power is: " + evaluate.power_info[evaluate.max_power])
            print("My best hand is:")
            for card in evaluate.best_hand:
                card.show()
            return evaluate.best_hand
    
    def your_action(self, chips_to_call, min_raise):
        self.chips_to_call = chips_to_call
        self.min_raise = min_raise

        if self.is_ai: # AI player
            if self.chips_to_call == 0:
                return self.__check()
            else:
                return self.__call()
        else: # Human player
            # print("Pick actions: 0 for fold, 1 for check/call, 2 for raise")
            action = int(input("Pick actions: 0 for fold, 1 for check/call, 2 for raise: "))
            if action == 0:
                return self.__fold()
            if action == 1:
                if self.chips_to_call == 0:
                    return self.__check()
                else:
                    return self.__call()
            if action == 2:
                chips_raise = int(input("Min raise is: " + str(self.min_raise) + " Input chips to raise: "))
                return self.__raise(chips_raise)

    def get_1_card(self, card):
        if len(self.__hand) < 2:
            self.__hand.append(card)
            self.__all_cards.append(card)
            self.status = 1

    def get_flop(self, cards):
        self.flop = cards
        self.round_bet = 0
        for card in cards:
            self.__all_cards.append(card)

    def get_turn(self, card):
        self.turn = card
        self.round_bet = 0
        self.__all_cards.append(card)
    
    def get_river(self, card):
        self.river = card
        self.round_bet = 0
        self.__all_cards.append(card)

    def __fold(self):
        self.__hand = []
        self.status = 0
        # print(self.name + " Fold")
        self.round_bet = 0
        return [0, 0]
    
    def __check(self):
        self.status = 1
        # print(self.name + " Check")
        return [1, 0]

    def __call(self):
        if self.chips >= self.chips_to_call:
            self.chips -= self.chips_to_call
            self.status = 1
            # print(self.name + " Call " + str(self.chips_to_call) + " chips")
            self.round_bet += self.chips_to_call
            return [1, self.chips_to_call]
        else:
            call_chips = self.chips
            self.chips = 0
            self.status = 1
            # print(self.name + " Call " + str(call_chips) + " chips")
            self.round_bet += call_chips
            return [1, call_chips]

    def __raise(self, raise_num):
        if raise_num < self.min_raise:
            raise_num = self.min_raise
        if self.chips >= raise_num:
            self.chips -= raise_num
        else:
            raise_num = self.chips
            self.chips = 0
        self.status = 1
        # print(self.name + " Raise " + str(raise_num) + " chips")
        self.round_bet += raise_num
        return [2, raise_num]

if __name__ == '__main__': 
    myDeck = Deck()
    myDeck.shuffle()

    fish_player = Player("Daming", 500)
    fish_player.say_hello()
    fish_player.show_chips()

    card = myDeck.draw()
    fish_player.get_1_card(card)
    card = myDeck.draw()
    fish_player.get_1_card(card)

    fish_player.show_hand()