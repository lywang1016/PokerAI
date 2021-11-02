from prettytable import PrettyTable
from icecream import ic
from policy_of_ai.strategy import Strategy
from simple_gui.card_plot import SimpleGUI

class AlwaysFold(Strategy):
    def __init__(self):
        super(AlwaysFold, self).__init__()

    def action_should_take(self):
        return [0, 0]

class AlwaysCall(Strategy):
    def __init__(self):
        super(AlwaysCall, self).__init__()

    def action_should_take(self):
        return [1, self.chips_to_call]

class AlwaysRaise(Strategy):
    def __init__(self):
        super(AlwaysRaise, self).__init__()

    def action_should_take(self):
        if self.chips < self.chips_to_call:
            return [1, self.chips]
        return [2, self.min_raise]

class Human(Strategy):
    def __init__(self):
        super(Human, self).__init__()
        self.display = SimpleGUI()

    def show_hand(self):
        # print(self.my_name + "'s hand cards are:")
        # for card in self.hand:
        #     card.show()
        if len(self.flop) == 0:
            self.display.clear_display()
        self.display.display_hand(self.hand)

    def show_flop(self):
        if len(self.flop) > 0:
            # print("Flop cards are:")
            # for card in self.flop:
            #     card.show()
            self.display.display_flop(self.flop)

    def show_turn(self):
        if self.turn != None:
            # print("Turn card is:")
            # self.turn.show()
            self.display.display_turn(self.turn)

    def show_river(self):
        if self.river != None:
            # print("River card is:")
            # self.river.show()
            self.display.display_river(self.river)

    def show_log_before_flop(self):
        if len(self.game_log[0]) > 0:
            tb = PrettyTable()
            tb.field_names = ["Player Name", "Player Action", "Chip Bet", "Pot Total", "Player Chips Left"]
            print("Log Preflop: ")
            for log in self.game_log[0]:
                tb.add_row([log.name,log.action,log.chip_bet,log.pot,log.chip_left])
            print(tb)

    def show_log_flop(self):
        if len(self.game_log[1]) > 0:
            tb = PrettyTable()
            tb.field_names = ["Player Name", "Player Action", "Chip Bet", "Pot Total", "Player Chips Left"]
            print("Log Flop: ")
            for log in self.game_log[1]:
                tb.add_row([log.name,log.action,log.chip_bet,log.pot,log.chip_left])
            print(tb)

    def show_log_turn(self):
        if len(self.game_log[2]) > 0:
            tb = PrettyTable()
            tb.field_names = ["Player Name", "Player Action", "Chip Bet", "Pot Total", "Player Chips Left"]
            print("Log Turn: ")
            for log in self.game_log[2]:
                tb.add_row([log.name,log.action,log.chip_bet,log.pot,log.chip_left])
            print(tb)
        
    def show_log_river(self):
        if len(self.game_log[3]) > 0:
            tb = PrettyTable()
            tb.field_names = ["Player Name", "Player Action", "Chip Bet", "Pot Total", "Player Chips Left"]
            print("Log River: ")
            for log in self.game_log[3]:
                tb.add_row([log.name,log.action,log.chip_bet,log.pot,log.chip_left])
            print(tb)
    
    def show_chips(self):
        print(self.my_name + " have " + str(self.chips) + " chips")

    def action_should_take(self):
        print('++++++++++++++++++++++++++++++++ Game Logs ++++++++++++++++++++++++++++++++')
        self.show_hand()
        self.show_log_before_flop()
        self.show_flop()
        self.show_log_flop()
        self.show_turn()
        self.show_log_turn()
        self.show_river()
        self.show_log_river()
        self.show_chips()

        if len(self.flop) == 0: # Preflop
            ic("Take Preflop Action!")
        elif self.turn == None: # Flop
            ic("Take Flop Action!")
        elif self.river == None: # Turn
            ic("Take Turn Action!")
        else:                     # River
            ic("Take River Action!")

        if self.chips_to_call == 0:
            action = int(input("Pick actions: 0 for fold, 1 for check, 2 for raise: "))
            if action < 1:
                action = 0
            if action > 1:
                action = 2
        else:
            print(str(self.chips_to_call) + " chips to call." )
            action = int(input("Pick actions: 0 for fold, 1 for call, 2 for raise: "))
            if action < 1:
                action = 0
            if action > 1:
                action = 2
        if action == 0:
            return [0, 0]
        if action == 1:
            return [1, self.chips_to_call]
        if action == 2:
            chips_raise = int(input("Min raise is: " + str(self.min_raise) + " Input chips to raise: "))
            return [2, chips_raise]
