from src.game import Game
from src.players.bad_IA import BAD_IA
from src.players.good_IA import GOOD_IA

import numpy as np
import matplotlib.pyplot as plt
import time
from multiprocessing import Pool, cpu_count

t = time.time()

N = 10
nb_games = [10, 100, 1000, 10000]

win1 = np.zeros((N, len(nb_games)))
draw = np.zeros((N, len(nb_games)))

if __name__ == '__main__':

    depth_tree = 4

    bad_IA = BAD_IA()
    good_IA = GOOD_IA(depth_tree)

    game = Game(good_IA, bad_IA, False)

    list_numbers = []

    def callback(result):
        list_numbers.append(result)

    for i in range(len(nb_games)):

        pool = Pool(processes=(cpu_count()))
        for j in range(N):

            for _ in range(nb_games[i]):
                pool.apply_async(game.run, args=(), callback=callback)

        pool.close()
        pool.join()

        for f in range(N):
            if f == 0:
                new_list = list_numbers[:(f + 1) * nb_games[i] + 1]
            if f == N - 1:
                new_list = list_numbers[f * nb_games[i]:]
                win1[f][i] = 100 * (new_list.count(1) / nb_games[i])
                draw[f][i] = 100 * (new_list.count(0) / nb_games[i])
            else:
                new_list = list_numbers[f * nb_games[i] + 1 : (f + 1) * nb_games[i] + 1]
                win1[f][i] = 100 * (new_list.count(1) / nb_games[i])
                draw[f][i] = 100 * (new_list.count(0) / nb_games[i])

        list_numbers = []

    print("wins = {}".format(win1))
    print("draws = {}".format(draw))

    win1_mean = np.mean(win1, axis=0)
    draw_mean = np.mean(draw, axis=0)

    print("win mean = {}".format(win1_mean))
    print("draw mean = {}".format(draw_mean))

    elapsed = time.time() - t
    print("Time elapsed : {}".format(elapsed))

    plt.figure()
    for i in range(len(nb_games)):
        plt.scatter(np.full(N, nb_games[i]), win1[:,i], c = 'blue', s = 10)
        plt.scatter(np.full(N, nb_games[i]), draw[:,i], c = 'red', s = 10)
        plt.scatter(nb_games[i], win1_mean[i], c = 'blue', marker = 'x', s = 50)
        plt.scatter(nb_games[i], draw_mean[i], c = 'red', marker = 'x', s = 50)

    plt.legend(['Victoire joueur 1', 'Ex-aequo', 'Moyenne victoire joueur 1', 'Moyenne ex-aequo'], loc=5)
    plt.xlabel('Nombre de parties')
    plt.ylabel('Probabilite en %')
    plt.xscale("log")
    plt.ylim((-10,100))
    plt.savefig('war_IA_graph.pdf')
    plt.show()