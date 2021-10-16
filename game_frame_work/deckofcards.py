import random

class Card(object):
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val
        
    def show(self):
        if self.value == 1:
            val = "Ace"
        elif self.value == 11:
            val = "Jack"
        elif self.value == 12:
            val = "Queen"
        elif self.value == 13:
            val = "King"
        else:
            val = self.value

        print("{} of {}".format(val, self.suit)) 


class Deck(object):
    def __init__(self):
        self.cards = []
        self.build()

    # Display all cards in the deck
    def show(self):
        for card in self.cards:
            card.show()

    # Generate 52 cards
    def build(self):
        self.cards = []
        for suit in ['Hearts', 'Clubs', 'Diamonds', 'Spades']:
            for val in range(1,14):
                self.cards.append(Card(suit, val))

    # Shuffle the deck
    def shuffle(self):
        random.shuffle(self.cards)

    # Return the top card
    def draw(self):
        return self.cards.pop()


if __name__ == '__main__':   
    # card = Card('Spades', 12)
    # card.show()
    myDeck = Deck()
    # myDeck.shuffle()
    myDeck.show()

    print('----------------')
    card = myDeck.draw()
    card.show()
    print('----------------')
    myDeck.show()