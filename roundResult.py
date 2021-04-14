from enum import Enum, unique

@unique
class RoundResult(Enum):
    '''
    Used to represent the result of a round, either by player's choice or how the play turns out
    (For ex. if the player loses all their money, ZERO_BALANCE will get returned and the game will end).
    '''
    FINISH = 0
    ZERO_BALANCE = 1
    NEW_ROUND = 2
    CONTINUE = 3
    TWENTY_ONE = 4
    BUST = 5
    STAND = 6
    ERROR = 7