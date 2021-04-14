This is a python implementation of Blackjack that is built using python version 3.7.4

It still needs to be checked over for some bugs, but it is mostly functional. Code cleanup also has to be done. It is currently configured to give the player 2 sixes from the deck to trigger the option to split and the player is then dealt a four to trigger the option to double down on the first hand.

The player can enter their total balance at the beginning of the game and how much they would like to bet. The player has the ability to hit, stand, split their hand, or double down (if eligible for the last two options) and can continue to play until they choose to finish or they run out of money, at which point, the game notifies them and terminates.

Brief Explanation of Files:

main: Contains a loop that runs the game by calling the appropriate functions from the config module

config: Contains most of the logic for setting up and running each round of the game

card: Represents the card objects to be used in the game deck

hand: Represents the player's hand and keeps track of the total of that hand, along with the number of aces being used with a value of 11. Also used to represent the dealer since they only have a hand of cards and have no bets or money balance to keep track of.

player: Represents the player (you). Holds the player's hand of cards as a 'hand' object along with their balance, bets, and whether or not they split.
	
deck: Represents the actual game deck that cards are dealt from. Currently configured to give the player two sixes to trigger the option of splitting their hand and then deals a four to the player to allow for a double down on one of those split hands. This has only been done for testing purposes.

RoundResult: Contains an enumeration that is used to let the main function know the result of each round.