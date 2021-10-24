import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

class SimpleGUI(object):
    def __init__(self):
        self.cards_img_path = os.path.abspath(os.getcwd()) + '/card_png/'
        print(self.cards_img_path)
    
    def clear_display(self):
        for i in range(10):
            plt.subplot(2, 5, i+1)
            plt.clf()
            plt.pause(0.01)

    def display_hand(self, hand):
        for i in range(2):
            suit = hand[i].suit
            value = hand[i].value
            card_path = self.cards_img_path + suit + '/' + str(value) + '.png'
            img = mpimg.imread(card_path)
            plt.subplot(2, 5, i+1)
            plt.imshow(img)
            plt.axis('off')
            plt.pause(0.05)

    def display_flop(self, flop):
        for i in range(3):
            suit = flop[i].suit
            value = flop[i].value
            card_path = self.cards_img_path + suit + '/' + str(value) + '.png'
            img = mpimg.imread(card_path)
            plt.subplot(2, 5, i+6)
            plt.imshow(img)
            plt.axis('off')
            plt.pause(0.05)

    def display_turn(self, turn):
        suit = turn.suit
        value = turn.value
        card_path = self.cards_img_path + suit + '/' + str(value) + '.png'
        img = mpimg.imread(card_path)
        plt.subplot(2, 5, 9)
        plt.imshow(img)
        plt.axis('off')
        plt.pause(0.05)

    def display_river(self, river):
        suit = river.suit
        value = river.value
        card_path = self.cards_img_path + suit + '/' + str(value) + '.png'
        img = mpimg.imread(card_path)
        plt.subplot(2, 5, 10)
        plt.imshow(img)
        plt.axis('off')
        plt.pause(0.05)

    
