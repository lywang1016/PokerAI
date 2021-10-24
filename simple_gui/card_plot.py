import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

class SimpleGUI(object):
    def __init__(self):
        self.cards_img_path = os.path.abspath(os.getcwd()) + '/card_png/'
        print(self.cards_img_path)

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

    


# if __name__ == '__main__': 
#     suit = 'Spades'
#     value = 7

#     cards_img_path = os.path.abspath(os.getcwd()) + '/card_png/'
#     # card_path = cards_img_path + suit + '/' + str(value) + '.png'
#     card_path1 = cards_img_path + suit + '/' + str(1) + '.png'
#     card_path2 = cards_img_path + suit + '/' + str(2) + '.png'
#     card_path3 = cards_img_path + suit + '/' + str(3) + '.png'
#     card_path4 = cards_img_path + suit + '/' + str(4) + '.png'
#     card_path5 = cards_img_path + suit + '/' + str(5) + '.png'

#     img1 = mpimg.imread(card_path1)
#     img2 = mpimg.imread(card_path2)
#     img3 = mpimg.imread(card_path3)
#     img4 = mpimg.imread(card_path4)
#     img5 = mpimg.imread(card_path5)
#     im_list = [img1, img2, img3, img4, img5]

    
#     # plt.subplot(1, 5, 1)
#     # plt.imshow(img1)
#     # plt.axis('off')
#     # plt.subplot(1, 5, 2)
#     # plt.imshow(img2)
#     # plt.axis('off')
#     # plt.subplot(1, 5, 3)
#     # plt.imshow(img3)
#     # plt.axis('off')
#     # plt.subplot(1, 5, 4)
#     # plt.imshow(img4)
#     # plt.axis('off')
#     # plt.subplot(1, 5, 5)
#     # plt.imshow(img5)
#     # plt.axis('off')
#     for i in range(5):
#         input("Pick actions: 0 for fold, 1 for call, 2 for raise: ")
#         plt.subplot(1, 5, i+1)
#         plt.imshow(im_list[i])
#         plt.axis('off')
#         plt.pause(0.05)

#     # plt.show()

#     # img = mpimg.imread(card_path)
#     # imgplot = plt.imshow(img)
#     # plt.show()

# # plt.axis([0, 10, 0, 1])

# # for i in range(10):
# #     y = np.random.random()
# #     plt.scatter(i, y)
# #     plt.pause(0.05)

# # plt.show()