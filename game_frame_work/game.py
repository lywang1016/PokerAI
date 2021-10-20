from evaluation import CompareHands
from player import Player, ActionLog
from croupier import Croupier

class Game(object):
    def __init__(self, sb, bb, max_player_num):
        self.sb = sb
        self.bb = bb
        self.max_player_num = max_player_num
        self.pot = 0
        self.all_logs = {}
        self.game_num = 0
        self.log = []
        self.log_before_flop = []
        self.log_flop = []
        self.log_turn = []
        self.log_river = []
        self.bfo = []
        self.afo = []
        self.winner_get = False
        self.player_list = []
        self.croupier = Croupier()
        self.croupier.open_table(max_player_num) # open a table

    def host_player(self, player):
        if player not in self.player_list:
            self.player_list.append(player)
            self.croupier.add_player(player)
            player.set_game_size([self.sb, self.bb])

    def kick_player(self, player):
        if player in self.player_list:
            self.player_list.remove(player)
            self.croupier.drop_player(player)

    def search_player(self, name):
        for player in self.player_list:
            if player.name == name:
                return player
        return None

    def get_round_bets(self):
        round_bet = []
        for player in self.player_list:
            if player.status == 1:
                round_bet.append(player.round_bet) 
        return round_bet

    def broadcast_log(self):
        for player in self.player_list:
            player.get_log(self.log)

    def start_1_game(self):
        self.pot = 0
        self.game_num += 1
        self.log_before_flop = []
        self.log_flop = []
        self.log_turn = []
        self.log_river = []
        self.bfo = []
        self.afo = []
        self.winner_get = False
        self.log = [self.log_before_flop, 
               self.log_flop,
               self.log_turn,
               self.log_river]

        self.deal_hand_cards()
        self.before_flop_actions()
        if not self.winner_get:
            self.flop()
            self.after_flop_actions('flop')
            if not self.winner_get:
                self.turn()
                self.after_flop_actions('turn')
                if not self.winner_get:
                    self.river()
                    self.after_flop_actions('river')
                    if not self.winner_get:
                        candidates_name = []
                        candidates_hand = []
                        candidates_cards = []
                        for player in self.player_list:
                            if player.status == 1:
                                candidates_hand.append(player.show_hand())
                                candidates_name.append(player.name)
                                candidates_cards.append(player.show_best_hand())
                        compare = CompareHands()
                        best_hand = compare.best_hand(candidates_cards)
                        num_winner = len(best_hand)
                        pot_win = int(self.pot/num_winner)
                        for win_cards in best_hand:
                            for i in range(len(candidates_cards)):
                                if win_cards == candidates_cards[i]:
                                    winner = self.search_player(candidates_name[i])
                                    winner.win_pot(pot_win)

        # save log
        self.all_logs[self.game_num] = self.log
        # players return cards
        for player in self.player_list:
            player.return_cards()


    def deal_hand_cards(self):
        print("------------Deal hand cards--------------")
        player_cards, self.bfo, self.afo = self.croupier.deal_hand_cards()
        if len(self.afo) == 2:
            sb_player = self.search_player(self.afo[1])
            self.pot += sb_player.set_your_position(0)
            sb_log = ActionLog(self.afo[1], "small blind", self.sb, sb_player.chips, self.pot)
            self.log_before_flop.append(sb_log)
            self.broadcast_log()
            bb_player = self.search_player(self.afo[0])
            self.pot += bb_player.set_your_position(1)
            bb_log = ActionLog(self.afo[0], "big blind", self.bb, bb_player.chips, self.pot)
            self.log_before_flop.append(bb_log)
            self.broadcast_log()
        else:
            for i in range(len(self.afo)):
                player = self.search_player(self.afo[i])
                self.pot += player.set_your_position(i)
                if i == 0:
                    sb_log = ActionLog(self.afo[0], "small blind", self.sb, player.chips, self.pot)
                    self.log_before_flop.append(sb_log)
                    self.broadcast_log()
                if i == 1:
                    bb_log = ActionLog(self.afo[1], "big blind", self.bb, player.chips, self.pot)
                    self.log_before_flop.append(bb_log)
                    self.broadcast_log()

        for name in player_cards:
            cards = player_cards[name]
            player = self.search_player(name)
            player.get_1_card(cards[0])
            player.get_1_card(cards[1])

    def before_flop_actions(self):
        print("------------Before flop actions--------------")
        action_idx = 0
        while True:
            # check players left
            active_num = 0
            active_name = ' '
            for player in self.player_list:
                if player.status == 1:
                    active_name = player.name
                    active_num += 1
            if active_num == 1: # game over
                winner = self.search_player(active_name)
                winner.win_pot(self.pot)
                self.winner_get = True
                break

            # check round bets same
            round_bets = self.get_round_bets()
            round_bets.sort()
            if round_bets[0] == round_bets[-1]:
                break
            
            round_bet_target = round_bets[-1]
            player = self.search_player(self.bfo[action_idx])
            if player.status == 1: # player still active
                chips_to_call = round_bet_target - player.round_bet
                for i in range(len(self.log_before_flop)-1, -1, -1):
                    log_his = self.log_before_flop[i]
                    if log_his.action == "raise" or log_his.action == "big blind":
                        last_raise = log_his.chip_bet
                        break
                min_raise = last_raise*2
                action = player.your_action(chips_to_call, min_raise)
                self.pot += action[1]
                if action[0] == 0: # someone fold
                    log = ActionLog(self.bfo[action_idx], "fold", 0, player.chips, self.pot)
                    self.log_before_flop.append(log)
                    self.broadcast_log()
                if action[0] == 1: 
                    if action[1] == 0: # someone check
                        log = ActionLog(self.bfo[action_idx], "check", 0, player.chips, self.pot)
                        self.log_before_flop.append(log)
                        self.broadcast_log()
                    if action[1] > 0: # someone call
                        log = ActionLog(self.bfo[action_idx], "call", action[1], player.chips, self.pot)
                        self.log_before_flop.append(log)
                        self.broadcast_log()
                if action[0] == 2: # someone raise
                    log = ActionLog(self.bfo[action_idx], "raise", action[1], player.chips, self.pot)
                    self.log_before_flop.append(log)
                    self.broadcast_log()

            action_idx += 1
            if action_idx == len(self.player_list):
                action_idx = 0
    
    def flop(self):
        print("------------Deal flop cards--------------")
        flop_cards = self.croupier.deal_flop() 
        # print("\tFlop cards are:")
        for card in flop_cards:
            card.show()
        for player in self.player_list:
            if player.status == 1:
                player.get_flop(flop_cards)

    def turn(self):
        print("------------Deal turn cards--------------")
        turn_card = self.croupier.deal_turn() 
        # print("\tTurn cards is:")
        turn_card.show()
        for player in self.player_list:
            if player.status == 1:
                player.get_turn(turn_card)

    def river(self):
        print("------------Deal river cards--------------")
        river_card = self.croupier.deal_river() 
        # print("\tRiver cards is:")
        river_card.show()
        for player in self.player_list:
            if player.status == 1:
                player.get_river(river_card)

    def after_flop_actions(self, stage):
        if stage == "flop":
            print("------------Flop actions--------------")
        if stage == "turn":
            print("------------Turn actions--------------")
        if stage == "river":
            print("------------River actions--------------")

        chips_to_call = 0 
        min_raise = self.bb
        action_idx = -2

        for i in range(len(self.afo)):
            name = self.afo[i]
            player = self.search_player(name)
            if player.status == 1:
                action = player.your_action(chips_to_call, min_raise)
                self.pot += action[1]
                if action[0] == 0: # someone fold
                    log = ActionLog(name, "fold", 0, player.chips, self.pot)
                    if stage == "flop":
                        self.log_flop.append(log)
                    if stage == "turn":
                        self.log_turn.append(log)
                    if stage == "river":
                        self.log_river.append(log)
                    self.broadcast_log()
                    # check players left
                    active_num = 0
                    active_name = ' '
                    for player in self.player_list:
                        if player.status == 1:
                            active_name = player.name
                            active_num += 1
                    if active_num == 1: # game over
                        winner = self.search_player(active_name)
                        winner.win_pot(self.pot)
                        self.winner_get = True
                        break
                if action[0] == 1: 
                    if action[1] == 0: # someone check
                        log = ActionLog(name, "check", 0, player.chips, self.pot)
                        if stage == "flop":
                            self.log_flop.append(log)
                        if stage == "turn":
                            self.log_turn.append(log)
                        if stage == "river":
                            self.log_river.append(log)
                        self.broadcast_log()
                    if action[1] > 0: # someone call
                        log = ActionLog(name, "call", action[1], player.chips, self.pot)
                        if stage == "flop":
                            self.log_flop.append(log)
                        if stage == "turn":
                            self.log_turn.append(log)
                        if stage == "river":
                            self.log_river.append(log)
                        self.broadcast_log()
                if action[0] == 2: # someone raise
                    log = ActionLog(name, "raise", action[1], player.chips, self.pot)
                    if stage == "flop":
                        self.log_flop.append(log)
                    if stage == "turn":
                        self.log_turn.append(log)
                    if stage == "river":
                        self.log_river.append(log)
                    self.broadcast_log()
                    action_idx = i+1
                    break
                
        while action_idx >= 0:
            if action_idx == len(self.player_list):
                action_idx = 0

            # check players left
            active_num = 0
            active_name = ' '
            for player in self.player_list:
                if player.status == 1:
                    active_name = player.name
                    active_num += 1
            if active_num == 1: # game over
                winner = self.search_player(active_name)
                winner.win_pot(self.pot)
                self.winner_get = True
                break

            # check round bets same
            round_bets = self.get_round_bets()
            round_bets.sort()
            if round_bets[0] == round_bets[-1]:
                break
            
            round_bet_target = round_bets[-1]
            player = self.search_player(self.afo[action_idx])
            if player.status == 1: # player still active
                chips_to_call = round_bet_target - player.round_bet
                if stage == "flop":
                    for i in range(len(self.log_flop)-1, -1, -1):
                        log_his = self.log_flop[i]
                        if log_his.action == "raise":
                            last_raise = log_his.chip_bet
                            break
                if stage == "turn":
                    for i in range(len(self.log_turn)-1, -1, -1):
                        log_his = self.log_turn[i]
                        if log_his.action == "raise":
                            last_raise = log_his.chip_bet
                            break
                if stage == "river":
                    for i in range(len(self.log_river)-1, -1, -1):
                        log_his = self.log_river[i]
                        if log_his.action == "raise":
                            last_raise = log_his.chip_bet
                            break
                min_raise = last_raise*2
                action = player.your_action(chips_to_call, min_raise)
                self.pot += action[1]
                if action[0] == 0: # someone fold
                    log = ActionLog(self.afo[action_idx], "fold", 0, player.chips, self.pot)
                    if stage == "flop":
                        self.log_flop.append(log)
                    if stage == "turn":
                        self.log_turn.append(log)
                    if stage == "river":
                        self.log_river.append(log)
                    self.broadcast_log()
                if action[0] == 1: 
                    if action[1] == 0: # someone check
                        log = ActionLog(self.afo[action_idx], "check", 0, player.chips, self.pot)
                        if stage == "flop":
                            self.log_flop.append(log)
                        if stage == "turn":
                            self.log_turn.append(log)
                        if stage == "river":
                            self.log_river.append(log)
                        self.broadcast_log()
                    if action[1] > 0: # someone call
                        log = ActionLog(self.afo[action_idx], "call", action[1], player.chips, self.pot)
                        if stage == "flop":
                            self.log_flop.append(log)
                        if stage == "turn":
                            self.log_turn.append(log)
                        if stage == "river":
                            self.log_river.append(log)
                        self.broadcast_log()
                if action[0] == 2: # someone raise
                    log = ActionLog(self.afo[action_idx], "raise", action[1], player.chips, self.pot)
                    if stage == "flop":
                        self.log_flop.append(log)
                    if stage == "turn":
                        self.log_turn.append(log)
                    if stage == "river":
                        self.log_river.append(log)
                    self.broadcast_log()

            action_idx += 1

                


    
    




        
    