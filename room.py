class Room:
    def __init__(self, board):
        self.__board = board
        self.__headcount = 0

    def get_board(self):
        return self.__board

    def get_headcount(self):
        return self.__headcount

    def increment(self):
        self.__headcount += 1

    def decrement(self):
        self.__headcount -= 1

    @staticmethod
    def create_room(board):
        return Room(board)
