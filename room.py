class Room:
    def __init__(self, room_id, board):
        self.__id = room_id
        self.__board = board
        self.__headcount = 0

    def get_id(self):
        return self.__id

    def get_board(self):
        return self.__board

    def get_headcount(self):
        return self.__headcount

    def increment(self):
        self.__headcount += 1

    def decrement(self):
        self.__headcount -= 1
