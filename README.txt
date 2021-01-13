This is a python implementation of Blackjack that is built using python version 3.7.4

Please note, this project is still in development, but does have enough functionality for it to be played.

Currently, there is only one player and the dealer. The player can enter their total balance at the beginning of the game and how much they would like to bet. The player has the ability to only hit or stand and can continue to play until they choose to finish or they run out of money, at which point, the game notifies them and terminates.

Functionality to be added includes: 
-Allowing up to 7 players in total (including the dealer)
-Splitting pairs
-Doubling down

Brief Explanation of Files:

main: Contains a loop that runs the game by calling the appropriate functions from the config module

config: Contains most of the logic for setting up and running each round of the game

card: Represents the card objects to be used in the game deck
	
player: Contains an abstract class to represent a player of the Blackjack game. Two classes (Dealer and Gambler) inherit from this class.

RoundResult: Contains an enumeration that is used to let the main function know the result of each round.