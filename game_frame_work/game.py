from deckofcards import Card, Deck
from evaluation import Evaluation
from player import Player
from croupier import Croupier

class ActionLog(object):
    def __init__(self, name, action, chip_bet, chip_left, pot):
        self.name = name
        self.action = action
        self.chip_bet = chip_bet
        self.chip_left = chip_left
        self.pot = pot
    
    def print_log(self):
        if self.action == "call" or self.action == "raise":
            print(self.name + " " + self.action + " " + str(self.chip_bet))
        else:
            print(self.name + " " + self.action)


if __name__ == '__main__': 
    ## Game setting
    sb = 1
    bb = 2
    max_player_num = 8

    ## Pot
    pot = 0

    ## Init players
    ai_player = Player("bot", 500, 1)
    human_player = Player("lyw", 500, 0)
    player_list = []
    player_list.append(ai_player)
    player_list.append(human_player)
    for player in player_list:
        player.set_game_size([sb, bb])

    def search_player(name):
        for player in player_list:
            if player.name == name:
                return player
        return None

    def get_round_bets(player_list):
        round_bet = []
        for player in player_list:
            round_bet.append(player.round_bet) 
        return round_bet

    ## Init croupier
    croupier = Croupier()

    ## Host players
    croupier.open_table(max_player_num) # open a table
    for player in player_list:  # player apply to join game
        player.join_game_application()
    for player in player_list:  # player sit down
        if player.join == 1:
            croupier.add_player(player)

    ## Start game
    print("Now Game Begin!")
    # while ai_player.chips > bb and human_player.chips > bb:
    pot = 0
    log_before_flop = []
    log_flop = []
    log_turn = []
    log_river = []
    winner_get = False

    # deal hand cards
    player_cards, bfo, afo = croupier.deal_hand_cards()
    if len(afo) == 2:
        sb_player = search_player(afo[1])
        pot += sb_player.set_your_position(0)
        sb_log = ActionLog(afo[1], "small blind", sb, sb_player.chips, pot)
        bb_player = search_player(afo[0])
        pot += bb_player.set_your_position(1)
        bb_log = ActionLog(afo[0], "big blind", bb, bb_player.chips, pot)
        log_before_flop.append(sb_log)
        log_before_flop.append(bb_log)
    else:
        for i in range(len(afo)):
            player = search_player(afo[i])
            pot += player.set_your_position(i)
            if i == 0:
                sb_log = ActionLog(afo[0], "small blind", sb, player.chips, pot)
                log_before_flop.append(sb_log)
            if i == 1:
                bb_log = ActionLog(afo[1], "big blind", bb, player.chips, pot)
                log_before_flop.append(bb_log)

    for name in player_cards:
        cards = player_cards[name]
        player = search_player(name)
        player.get_1_card(cards[0])
        player.get_1_card(cards[1])
    # ai_player.print_player_info()
    # human_player.print_player_info()
    
    # ask actions
    action_idx = 0
    while True:
        # check players left
        active_num = 0
        active_name = ' '
        for player in player_list:
            if player.status == 1:
                active_name = player.name
                active_num += 1
        if active_num == 1: # game over
            winner = search_player(active_name)
            winner.win_pot(pot)
            winner_get = True
            break

        # check round bets same
        round_bets = get_round_bets(player_list)
        round_bets.sort()
        if round_bets[0] == round_bets[-1]:
            break
        
        round_bet_target = round_bets[-1]
        player = search_player(bfo[action_idx])
        if player.status == 1: # player still active
            chips_to_call = round_bet_target - player.round_bet
            for i in range(len(log_before_flop)-1, -1, -1):
                log_his = log_before_flop[i]
                if log_his.action == "raise" or log_his.action == "big blind":
                    last_raise = log_his.chip_bet
                    break
            min_raise = last_raise*2
            action = player.your_action(chips_to_call, min_raise)
            pot += action[1]
            if action[0] == 0: # someone fold
                log = ActionLog(bfo[action_idx], "fold", 0, player.chips, pot)
                log_before_flop.append(log)
            if action[0] == 1: 
                if action[1] == 0: # someone check
                    log = ActionLog(bfo[action_idx], "check", 0, player.chips, pot)
                    log_before_flop.append(log)
                if action[1] > 0: # someone call
                    log = ActionLog(bfo[action_idx], "call", action[1], player.chips, pot)
                    log_before_flop.append(log)
            if action[0] == 2: # someone raise
                log = ActionLog(bfo[action_idx], "raise", action[1], player.chips, pot)
                log_before_flop.append(log)

            action_idx += 1
            if action_idx == len(player_list):
                action_idx = 0

    
    # for log in log_before_flop:
    #     log.print_log()
    # print("pot has: " + str(pot))
    






        
    