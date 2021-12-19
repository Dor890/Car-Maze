#################################################################
# FILE : car.py
# WRITER : Dor Messica, dor.messica, 318391877
# EXERCISE : intro2cse ex9 2020
# DESCRIPTION: The file contains the class Car of the game "Rush Hour"
#################################################################

class Car:
    """
    Add class used to represent a car in "rush hour" game.
    """
    VERTICAL = 0
    HORIZONTAL = 1
    MOVEMENT = 'cause the car to move '
    WIN = 'cause the car to win the game'
    INVALID_DIRECTION = 'the car can not go that way'
    UP = 'u'
    DOWN = 'd'
    RIGHT = 'r'
    LEFT = 'l'

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object.
        :param name: A string representing the car's name.
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col)
         location.
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL).
        """
        self.__name = name
        self.__length = length
        self.__location = location
        self.__orientation = orientation
        self.__FIRST_POSITION = self.car_coordinates()[0]
        self.__LAST_POSITION = self.car_coordinates()[-1]

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        row_loc, col_loc = self.__location
        coordinates = [self.__location]
        for i in range(1, self.__length):
            if self.__orientation == Car.HORIZONTAL:
                coordinates.append((row_loc, col_loc + i))
            else: # car is placed vertically
                coordinates.append((row_loc + i, col_loc))
        return coordinates

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements
         permitted by this car.
        """
        result = {}
        if self.__orientation == Car.HORIZONTAL:
            result[Car.LEFT] = Car.MOVEMENT + 'left'
            result[Car.RIGHT] = Car.MOVEMENT + 'right'
        if self.__orientation == Car.VERTICAL:
            result[Car.UP] = Car.MOVEMENT + 'up'
            result[Car.DOWN] = Car.MOVEMENT + 'down'
        return result

    def movement_requirements(self, movekey):
        """
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this
         move to be legal.
        """
        if movekey in self.possible_moves().keys():
            if movekey == Car.RIGHT:
                return [(self.__LAST_POSITION[0], self.__LAST_POSITION[1] + 1)]
            elif movekey == Car.LEFT:
                return [(self.__FIRST_POSITION[0], self.__FIRST_POSITION[1] - 1)]
            elif movekey == Car.UP:
                return [(self.__FIRST_POSITION[0] - 1, self.__FIRST_POSITION[1])]
            elif movekey == Car.DOWN:
                return [(self.__LAST_POSITION[0] + 1, self.__LAST_POSITION[1])]
        print(Car.INVALID_DIRECTION)

    def move(self, movekey):
        """
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if movekey not in self.possible_moves().keys():
            return False
        new_location = list(self.__location)
        if self.__orientation == Car.HORIZONTAL:
            if movekey == Car.RIGHT:
                new_location[1] += 1
            if movekey == Car.LEFT:
                new_location[1] -= 1
        else:  # orientation is vertically
            if movekey == Car.DOWN:
                new_location[0] += 1
            if movekey == Car.UP:
                new_location[0] -= 1
        self.__location = tuple(new_location)
        self.__FIRST_POSITION = self.car_coordinates()[0]
        self.__LAST_POSITION = self.car_coordinates()[-1]
        return True

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name
