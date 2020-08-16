import threading
import copy

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

    def __init__(self, imagedata):
        """Parses a JSON of ImageData."""

        self.width = copy.deepcopy(imagedata['width'])
        self.height = copy.deepcopy(imagedata['height'])
        self.data = copy.deepcopy(imagedata['data'])
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

    def toDict(self):
        boardDict = {
            'width': self.width,
            'height': self.height,
            'data': self.data
        }
        return boardDict
