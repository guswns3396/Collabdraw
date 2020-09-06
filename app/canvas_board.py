import threading
import copy

HEIGHT = 500
WIDTH = 500

class CanvasBoard:
    """Represents the image data of the canvas board.

    Attributes:
        width (int): The width of the board.
        height (int): The height of the board.
        data (list): An Uint8ClampedArray of RGBA data ranging from 0 to 255.
    """

    RED = 0
    GREEN = 1
    BLUE = 2
    ALPHA = 3

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [0 for i in range(4 * width * height)]
        self.lock = threading.Lock()

        if len(self.data) != self.width * self.height * 4:
            raise ValueError(
                'Nonmatching image metadata: Expected data length - {}, Actual data length - {}'
                .format(self.width * self.height, len(self.data)))

    def get_pixel_for_coordinate(self, row, col):
        """Returns a tuple of RGBA values at the given coordinate of the canvas board."""

        if row < 0 or col < 0 or row >= self.height or col >= self.width:
            raise ValueError(
                'Invalid coordinate: Row - {}, Col - {}, Height - {}, Width - {}'
                .format(row, col, self.height, self.width))
        start_ind = row * (self.width * 4) + col * 4
        return tuple(self.data[start_ind:start_ind + 4])

    def update_board(self, diffs: list):
        self.lock.acquire()
        for diff in diffs:
            self.data[diff['coord']] = diff['val']
        self.lock.release()

    def to_dict(self):
        boardDict = {
            'width': copy.deepcopy(self.width),
            'height': copy.deepcopy(self.height),
            'data': copy.deepcopy(self.data)
        }
        return boardDict

    @staticmethod
    def create_board(width, height):
        return CanvasBoard(width, height)
