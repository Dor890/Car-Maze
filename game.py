#################################################################
# FILE : game.py
# WRITER : Dor Messica, dor.messica, 318391877
# EXERCISE : intro2cse ex9 2020
# DESCRIPTION: The file contains the class Game and the running functionality
#              of the game "Rush Hour"
#################################################################

import board
import car
import helper
import sys

class Game:
    """
    Add class used to run the game "rush hour".
    """
    PUT_MESSAGE = "Choose name and direction (n,d). To quit type '!': "
    WIN_MSG = 'Congratulation, you have won the game!'
    INVALID_GAME_VALUES = 'The game received invalid car initial values'
    PUT_INVALID = 'You have entered an invalid input.'
    NAMES = 'YBOGWR'
    DIRECTIONS = 'udrl'
    ABORT_GAME = '!'
    COMMA = ','
    EMPTY = '_'
    WIN_ROW = 3
    WIN_COL = 7

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.__board = board

    def input_validator(self, move):
        """
        :param move: the input received from the user in the format 'n,d':
        name = car's name, d = direction to move the car.
        :return: a boolean value if the input received is valid.
        """
        if len(move) != 3 or move[0] not in Game.NAMES or move[2] not in\
                Game.DIRECTIONS or move[1] != Game.COMMA:
            print(Game.PUT_INVALID)
            return False
        return True

    def __single_turn(self):
        """
        The function runs one round of the game:
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.
        :return: a boolean value if the game should be continued.
        """
        if self.__board.cell_content((Game.WIN_ROW, Game.WIN_COL)):
            print(Game.WIN_MSG)
            return False
        print(self.__board)
        move = input(Game.PUT_MESSAGE)
        while not self.input_validator(move) or\
                not self.__board.move_car(move[0], move[2]):
            if move == Game.ABORT_GAME:
                return False
            move = input(Game.PUT_MESSAGE)
        return True

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        while True:
            if not self.__single_turn():
                break


def init_validator(name, length, direction):
    """
    Checks the initial values of a car according to the game laws.
    :param direction: the direction of the car (vertical(0) or horizontal(1)).
    :param length: the length of the car (int).
    :param name:  the name of the car (string).
    :return: a boolean value if the initial values are valid.
    """
    if len(name) == 1 and name in Game.NAMES and \
            1 < length < 5 and (direction == 1 or direction == 0):
        return True
    return False


def init_cars(board):
    """
    Updates the board object with all valid cars.
    :param board: a board object.
    :return: the updated board object.
    """
    CARS_DICT = helper.load_json(sys.argv[1])
    for key in CARS_DICT.keys():
        values = CARS_DICT[key]
        if not check_dict(key, values):
            continue
        length = values[0]
        location = tuple(values[1])
        direction = values[2]
        if init_validator(key, length, direction):
            new_car = car.Car(key, length, location, direction)
            board.add_car(new_car)
        else:
            print(Game.INVALID_GAME_VALUES)
    return board


def check_dict(key, values):
    """
    Checks if all parameters of the JSON dictionary are valid.
    :param key: a key in the dictionary.
    :param values: the value if the key as a list.
    :return: a boolean value if all parameters are valid according to the game.
    """
    if len(values) != 3 or type(values[0]) != int or\
            type(values[1]) != list or len(values[1]) != 2 or\
            type(values[1][0]) != int or type(values[1][1]) != int or\
            type(values[2]) != int or type(key) != str:
        return False
    return True


def main():
    game_board = board.Board()
    updated_board = init_cars(game_board)
    game = Game(updated_board)
    print(game_board.possible_moves())
    game.play()


if __name__ == "__main__":
    main()
