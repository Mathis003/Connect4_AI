from src.players.bad_IA import BAD_IA
from src.players.good_IA import GOOD_IA
from src.players.player import Player
from src.game import Game


if __name__ == "__main__":

    depth_tree = 5

    bad_IA = BAD_IA()
    good_IA = GOOD_IA(depth_tree)
    player = Player()

    game1 = Game(player, good_IA, True)
    game2 = Game(player, bad_IA, True)
    game3 = Game(bad_IA, good_IA, True)

    game1.run()
    game2.run()
    game3.run()