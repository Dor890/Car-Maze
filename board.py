#################################################################
# FILE : board.py
# WRITER : Dor Messica, dor.messica, 318391877
# EXERCISE : intro2cse ex9 2020
# DESCRIPTION: The file contains the class Board of the game "Rush Hour"
#################################################################

class Board:
    """
    A class used to represent a game board of the game "rush hour".
    """
    __ROWS = __COLUMNS = 7
    FIRST_LINE = 0
    LAST_LINE = __ROWS - 1
    TARGET_LOC = (3, 7)
    TARGET_IDX = 28
    EXIT_ROW = TARGET_LOC[0]
    EMPTY = '_'
    BLANK = ' '
    MOVEMENT = 'cause the car arrive spot '
    CAR_NOT_FOUND = 'car was not found in the board'
    UP = 'u'
    DOWN = 'd'
    RIGHT = 'r'
    LEFT = 'l'

    def __init__(self):
        """
        A constructor for a board object.
        Attributes:
            __cars - dictionary with car names as keys and car objects as
             values.
            __board - nested list contains the game board.
        """
        self.__board = []
        for i in range(Board.__ROWS):
            self.__board.append([])
            for j in range(Board.__COLUMNS):
                self.__board[i].append(Board.EMPTY)
            if i == Board.EXIT_ROW:
                self.__board[i].append(Board.EMPTY)
        self.__cars = {}

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        str = ''
        for i in range(Board.__ROWS):
            for j in range(Board.__COLUMNS):
                name = self.cell_content((i, j))
                if name:
                    str += self.__board[i][j].get_name() + Board.BLANK
                else:  # empty space
                    str += Board.EMPTY + Board.BLANK
            if i == Board.EXIT_ROW:  # for 7 rows board
                str += Board.EMPTY
            str += '\n'
        return str

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        cell_list = [(i, j) for i in range(len(self.__board))
                     for j in range(len(self.__board[0]))]
        cell_list.insert(Board.TARGET_IDX, Board.TARGET_LOC)
        return cell_list

    def moves_helper(self, car):
        """
        Receives a car and returns a dictionary with all possible moves of the
        car.
        :param car: a car object.
        :return: a dictionary with all possible moves of the car as keys and
        a small description as the value.
        """
        FIRST = car.car_coordinates()[0]
        LAST = car.car_coordinates()[-1]
        result = {}
        if Board.LEFT in car.possible_moves():
            if FIRST[1] != self.FIRST_LINE and self.no_crash(car, Board.LEFT):
                result[Board.LEFT] = self.MOVEMENT + str((FIRST[0], LAST[1]-1))
        if Board.RIGHT in car.possible_moves():
            if LAST[1] != self.LAST_LINE and self.no_crash(car, Board.RIGHT):
                result[car.RIGHT] = self.MOVEMENT + str((FIRST[0], FIRST[1]+1))
            if LAST == (3, 6):
                result[Board.RIGHT] = self.MOVEMENT + str(Board.TARGET_LOC)
        if Board.UP in car.possible_moves():
            if FIRST[0] != self.FIRST_LINE and self.no_crash(car, Board.UP):
                result[Board.UP] = self.MOVEMENT + str((FIRST[0]-1, FIRST[1]))
        if Board.DOWN in car.possible_moves():
            if LAST[0] != self.LAST_LINE and self.no_crash(car, Board.DOWN):
                result[Board.DOWN] = self.MOVEMENT + str((FIRST[0]+1,
                                                          FIRST[1]))
        return result

    def no_crash(self, car, movekey):
        """
        Checks if the car will crush another one if will be moved in the given
        direction.
        :param car: a car object.
        :param movekey: direction to move the car.
        :return: a boolean value if there is going to be a crash with another
        car.
        """
        next_pos = car.movement_requirements(movekey)[0]
        if self.__board[next_pos[0]][next_pos[1]] == Board.EMPTY:
            return True
        return False

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        lst = []
        for car in self.__cars.values():
            car_moves = self.moves_helper(car)
            for key in car_moves:
                lst.append((car.get_name(), key, car_moves[key]))
        return lst

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be
         filled for victory.
        :return: (row,col) of goal location
        """
        return Board.TARGET_LOC  # for a 7 rows game

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        if coordinate in self.cell_list():
            if self.__board[coordinate[0]][coordinate[1]] != Board.EMPTY:
                return self.__board[coordinate[0]][coordinate[1]].get_name()

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        for i in car.car_coordinates():
            if self.cell_content(i):  # if car exists there
                return False
            if i not in self.cell_list():  # if coordinates are in range
                return False
        if car.get_name() in self.__cars.keys():  # if name already exists
            return False
        for i in car.car_coordinates():
            self.__board[i[0]][i[1]] = car
        self.__cars[car.get_name()] = car
        return True

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        if name not in self.__cars.keys():
            print(Board.CAR_NOT_FOUND)
            return False
        for i in range(Board.__ROWS):
            for j in range(Board.__COLUMNS):
                if self.cell_content((i, j)) == name:
                    row, col, car = i, j, self.__board[i][j]
                    if movekey not in self.moves_helper(car):
                        print(car.INVALID_DIRECTION)
                        return False
                    car.move(movekey)
                    self.update_car(car, movekey, row, col)
                    return True
        return False

    def update_car(self, car, movekey, row, col):
        """
        Updates the car's new location in the board.
        :param car: a car object.
        :param movekey: direction to move the car.
        :param row: the current row.
        :param col: the current column.
        """
        length = len(car.car_coordinates())
        if movekey == Board.RIGHT:
            self.__board[row][col] = Board.EMPTY
            self.__board[row][col+length] = car
        if movekey == Board.LEFT:
            self.__board[row][col+length-1] = Board.EMPTY
            self.__board[row][col-1] = car
        if movekey == Board.DOWN:
            self.__board[row][col] = Board.EMPTY
            self.__board[row+length][col] = car
        if movekey == Board.UP:
            self.__board[row+length-1][col] = Board.EMPTY
            self.__board[row-1][col] = car
