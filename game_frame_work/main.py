from player import Player
from game import Game

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