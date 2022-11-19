import numpy as np
import matplotlib.pyplot as plt
import connect4
import time

t = time.time()

N = 10  # Nb repetitions
nb_games = [10, 100, 1000, 10000]
# Array with the percentage of success for player 1 for [10, 100, 1000, 10000] games, N times each
win1 = np.zeros((N, len(nb_games)))
# Array with the percentage of draws for player 1 for [10, 100, 1000, 10000] games, N times each
draw = np.zeros((N, len(nb_games)))

##################################
### START : To do for students ###
##################################

def play_n_games(n):
    """
    Simulate n games of Puissance4 with the help of the method "connect4.run_game()".
    :param n: number of games to simulate
    :return: a list of two numbers => The first one is the number of games win by the player 1
                                      and the second one is the number of game with draw as end.
    """
    number0, number1 = 0, 0
    for i in range(n):
        number = connect4.run_game()
        if number == 1:
            number1 += 1
        elif number == 0:
            number0 += 1

    return [number1, number0]

# Complete the two arrays
for i in range(len(nb_games) - 3):
    for j in range(N):
        number_of_repetition = nb_games[i]
        list_numbers = play_n_games(number_of_repetition)
        number_wins_by_player1, number_draw_games = list_numbers[0], list_numbers[1]
        # Update the arrays with the percentage
        win1[j][i] = 100 * (number_wins_by_player1 / number_of_repetition)
        draw[j][i] = 100 * (number_draw_games / number_of_repetition)


################################
### END : To do for students ###
################################

# Computes and prints the mean for each [10, 100, 1000, 10000]
win1_mean = np.mean(win1, axis=0)
draw_mean = np.mean(draw, axis=0)
print("win mean = {}".format(win1_mean))
print("draw mean = {}".format(draw_mean))
elapsed = time.time() - t
print('Elapsed time: ', elapsed)

# Plot the results in the required format.
# Please do not modify

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
plt.show()

plt.savefig('MCplot.png', format='png')