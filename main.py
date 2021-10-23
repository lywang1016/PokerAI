from game_frame_work.player import Player
from game_frame_work.game import Game
from policy_of_ai.naive_policy_wly import AlwaysCall, AlwaysFold, AlwaysRaise, Human

if __name__ == '__main__': 
    ## Game setting
    sb = 1
    bb = 2
    max_player_num = 8
    game = Game(sb, bb, max_player_num)

    ## Init Strategies
    fold_strategy = AlwaysFold()
    call_strategy = AlwaysCall()
    raise_strategy = AlwaysRaise()
    human_strategy = Human()

    ## Init players
    ai_player1 = Player("bot1", 50000, fold_strategy)
    ai_player2 = Player("bot2", 50000, call_strategy)
    ai_player3 = Player("bot3", 50000, raise_strategy)
    human_player = Player("lyw", 500, human_strategy)

    ## Player join game
    ai_player1.join_game_application()
    ai_player2.join_game_application()
    ai_player3.join_game_application()
    human_player.join_game_application()
    game.host_player(ai_player1)
    game.host_player(ai_player2)
    game.host_player(ai_player3)
    game.host_player(human_player)

    ## Start 1 game
    print("Now Game Begin!")
    game.start_1_game()

    ## Start 100 game
    # for i in range(100):
    #     game.start_1_game()
    ai_player1.show_chips()
    ai_player2.show_chips()
    ai_player3.show_chips()
    human_player.show_chips()