from deckofcards import Card, Deck

class Player(object):
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = []
        self.flop = []
        self.turn = None
        self.river = None
        self.all_cards = []

    def say_hello(self):
        print("Hi my name is " + self.name)
        return self.name

    def show_hand(self):
        print("My hand cards are:")
        for card in self.hand:
            card.show()
        return self.hand
    
    def show_chips(self):
        print("I have " + str(self.chips) + " chips")
        return self.chips

    def get_1_card(self, card):
        if len(self.hand) < 2:
            self.hand.append(card)
            self.all_cards.append(card)

    def get_flop(self, cards):
        self.flop = cards
        for card in cards:
            self.all_cards.append(card)

    def get_turn(self, card):
        self.turn = card
        self.all_cards.append(card)
    
    def get_river(self, card):
        self.river = card
        self.all_cards.append(card)

    # def action_fold(self):
    #     self.hand = []
    
    # def action_check(self):
    #     self.chips = self.chips

    # def action_call(self, chip_num):
    #     self.chips -= chip_num

    # def action_raise(self, chip_num):
    #     self.chips -= chip_num

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