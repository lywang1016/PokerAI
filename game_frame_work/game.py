from deckofcards import Card, Deck
from evaluation import Evaluation
from player import Player
from croupier import Croupier

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

    # deal hand cards
    player_cards, bfo, afo = croupier.deal_hand_cards()
    if len(afo) == 2:
        bb_player = search_player(afo[0])
        pot += bb_player.set_your_position(1)
        sb_player = search_player(afo[1])
        pot += sb_player.set_your_position(0)
    else:
        for i in range(len(afo)):
            player = search_player(afo[i])
            pot += player.set_your_position(i)

    for name in player_cards:
        cards = player_cards[name]
        player = search_player(name)
        player.get_1_card(cards[0])
        player.get_1_card(cards[1])
    # ai_player.print_player_info()
    # human_player.print_player_info()
    
    # ask actions
    all_flat = bb
    chips_to_call = sb
    min_raise = sb + bb
    for i in range(len(bfo)):
        player = search_player(bfo[i])
        action = player.your_action(chips_to_call, min_raise)
        # action[0]
        
    