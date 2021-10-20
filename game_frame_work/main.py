from player import Player
from game import Game

if __name__ == '__main__': 
    ## Game setting
    sb = 1
    bb = 2
    max_player_num = 8
    game = Game(sb, bb, max_player_num)

    ## Init players
    ai_player1 = Player("bot", 500, 'call')
    human_player = Player("lyw", 500, 'human')

    ## Player join game
    ai_player1.join_game_application()
    human_player.join_game_application()
    game.host_player(ai_player1)
    game.host_player(human_player)

    ## Start 1 game
    print("Now Game Begin!")
    game.start_1_game()