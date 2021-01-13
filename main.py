from config import config, run_round, new_round
from player import Gambler, Dealer
from roundResult import RoundResult

'''
The file the Blackjack game will run from. This file will call the appropriate functions from config
for the game to continuously run until the player chooses to stop or their balance goes to zero.
'''

print("Welcome to Blackjack!")
# Obtain the list that contains the dealer and player. Note that the dealer is always first in the list.
players = config()

while True:
	round = run_round(players[0], players[1])

	# Check if player has chosen to finish playing
	if round == RoundResult.FINISH:
		print("Thank you for playing!")
		print("Your total is: ${}".format(players[1].balance))
		break
	# Check if player has chosen to start a new round.
	elif round == RoundResult.NEW_ROUND:
		new_round(players[0], players[1])
	# Player lost all their money
	else:
		print("You have no money left.")
		print("Thank you for playing.")
		break