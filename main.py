from game_frame_work.player import Player
from game_frame_work.game import Game
from policy_of_ai.naive_policy_wly import AlwaysCall, AlwaysFold, AlwaysRaise, Human
import warnings

if __name__ == '__main__':  
    warnings.filterwarnings("ignore")

    ## Game setting
    sb = 1
    bb = 2
    max_player_num = 9
    game = Game(sb, bb, max_player_num)

    ## Init Strategies
    fold_strategy = AlwaysFold()
    call_strategy = AlwaysCall()
    raise_strategy = AlwaysRaise()
    human_strategy = Human()

    ## Init players
    human_player = Player("wly", 0, human_strategy)
    ai_player1 = Player("bot1", 50, fold_strategy)
    ai_player2 = Player("bot2", 50, call_strategy)
    ai_player3 = Player("bot3", 70, raise_strategy)
    ai_player4 = Player("bot4", 30, call_strategy)
    ai_player5 = Player("bot5", 50, raise_strategy)
    ai_player6 = Player("bot6", 50, call_strategy)
    ai_player7 = Player("bot7", 70, raise_strategy)
    ai_player8 = Player("bot8", 30, call_strategy)

    ## Player join game
    game.host_player(human_player)
    game.host_player(ai_player1)
    game.host_player(ai_player2)
    game.host_player(ai_player3)
    game.host_player(ai_player4)
    game.host_player(ai_player5)
    game.host_player(ai_player6)
    game.host_player(ai_player7)
    game.host_player(ai_player8)

    ## Start 1 game
    # game.start_1_game()
    # human_player.show_chips()
    # ai_player1.show_chips()
    # ai_player2.show_chips()
    # ai_player3.show_chips()
    # ai_player4.show_chips()

    ## Start 100 game
    # for i in range(100):
    #     game.start_1_game()
    #     human_player.show_chips()
    #     ai_player1.show_chips()
    #     ai_player2.show_chips()
    #     ai_player3.show_chips()
    #     ai_player4.show_chips()

    ## Continue play game until only 1 player left
    while len(game.player_list) > 1:
        game.start_1_game()
        human_player.show_chips()
        ai_player1.show_chips()
        ai_player2.show_chips()
        ai_player3.show_chips()
        ai_player4.show_chips()
        ai_player5.show_chips()
        ai_player6.show_chips()
        ai_player7.show_chips()
        ai_player8.show_chips()

    