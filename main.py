from hand import Hand
from deck import Deck
from config import config, run_round, new_round
from player import Player
from roundResult import RoundResult

'''
The file the Blackjack game will run from. This file will call the appropriate functions from config
for the game to continuously run until the player chooses to stop or their balance goes to zero.
'''

print("Welcome to Blackjack!")
# The dealer can only hit until they reach at least 17 and have no bets or other options, 
# therefore they can just be represented by a hand alone.
dealer = Hand()
player = Player()
game_deck = Deck()
config(player, dealer, game_deck)

while True:
    round = run_round(player, dealer, game_deck)
    # Check if player has chosen to finish playing
    if round == RoundResult.FINISH:
        print("Thank you for playing!")
        print("Your total is: ${}".format(player.balance))
        break
    # Check if player has chosen to start a new round.
    elif round == RoundResult.NEW_ROUND:
        game_deck = Deck() #reset the Deck
        new_round(player, dealer, game_deck)
        # print("Length of player's hand in main: {}".format(len(player.hands))) #Q_DEBUG
    # Player lost all their money
    elif round == RoundResult.ZERO_BALANCE:
        print("You have no money left.")
        print("Thank you for playing.")
        break
    else: 
        print("Error during game")
        break