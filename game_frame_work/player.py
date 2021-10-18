from deckofcards import Card, Deck
from evaluation import Evaluation

class Player(object):
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.flop = []
        self.turn = None
        self.river = None
        self.position = None
        self.sb = 0
        self.bb = 0
        self.pot_size = 0
        self.chips_to_call = 0
        self.min_raise = 0
        self.other_players = []
        self.others_actions = {}
        self.my_actions = []
        self.status = 0
        self.seat_num = -1
        self.join = 0
        self.action_def = {0:"Fold",
                           1:"Check/Call",
                           2:"Raise"}
        self.__hand = []
        self.__all_cards = []

    def join_game_application(self):
        self.say_hello()
        self.show_chips()
        self.join = 1
        return self.name, self.chips
    
    def leave_game_application(self):
        self.join = 0

    def say_hello(self):
        print("Hi my name is " + self.name)
        return self.name

    def show_hand(self):
        print("My hand cards are:")
        for card in self.__hand:
            card.show()
        return self.__hand
    
    def show_chips(self):
        print("I have " + str(self.chips) + " chips")
        return self.chips

    def set_game_size(self, game_size):
        self.sb = game_size[0]
        self.bb = game_size[0]
    
    def set_your_position(self, position):
        self.position = position
        if position == 'SB' or position == 'SBB':
            self.chips -= self.sb
            return self.sb
        if position == 'BB':
            self.chips -= self.bb
            return self.bb
        return 0

    def other_players_info(self, players):
        self.other_players = players
        self.my_actions = []
        self.others_actions = {}
        for player in players:
            if player.position not in self.others_actions:
                self.others_actions[player.position] = []

    def last_others_action(self, position, action, chips):
        self.pot_size += chips
        self.others_actions[position].append([action, chips])

    def win_pot(self):
        self.chips += self.pot_size
        self.pot_size = 0
        self.status = 0

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

        if self.chips_to_call = 0:
            return self.__check()
        else:
            return self.__call()

    def get_1_card(self, card):
        if len(self.__hand) < 2:
            self.__hand.append(card)
            self.__all_cards.append(card)
            self.status = 1

    def get_flop(self, cards):
        self.flop = cards
        for card in cards:
            self.__all_cards.append(card)

    def get_turn(self, card):
        self.turn = card
        self.__all_cards.append(card)
    
    def get_river(self, card):
        self.river = card
        self.__all_cards.append(card)

    def __fold(self):
        self.__hand = []
        self.my_actions.append([0, 0])
        self.status = 0
        return [0, 0]
    
    def __check(self):
        self.my_actions.append([1, 0])
        self.status = 1
        return [1, 0]

    def __call(self):
        self.chips -= self.chips_to_call
        self.my_actions.append([1, self.chips_to_call])
        self.status = 1
        return [1, self.chips_to_call]

    def __raise(self):
        raise_num = self.min_raise
        self.chips -= raise_num
        self.my_actions.append(2, raise_num)
        self.status = 1
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