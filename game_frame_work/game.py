from deckofcards import Card, Deck
from evaluation import Evaluation
from player import Player, ActionLog
from croupier import Croupier

class Game(object):
    def __init__(self, sb, bb, max_player_num):
        self.sb = sb
        self.bb = bb
        self.max_player_num = max_player_num
        self.pot = 0
        self.log = {}
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


    def deal_hand_cards(self):
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
    



if __name__ == '__main__': 
    ## Game setting
    sb = 1
    bb = 2
    max_player_num = 8
    game = Game(sb, bb, max_player_num)

    ## Init players
    ai_player = Player("bot", 500, 1)
    human_player = Player("lyw", 500, 0)
    ai_player.join_game_application()
    human_player.join_game_application()

    ## Player join game
    game.host_player(ai_player)
    game.host_player(human_player)

    ## Start 1 game
    print("Now Game Begin!")
    game.start_1_game()
    
    




        
    