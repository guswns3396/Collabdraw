import unittest
from canvas_board import CanvasBoard


class TestCanvasBoard(unittest.TestCase):
    def test_init(self):
        imagedata = {
            'width': 3,
            'height': 2,
            # Flatten 3x2 array with RGBA values
            'data': [0 for i in range(24)]
        }

        canvas_board = CanvasBoard(imagedata)

        self.assertEqual(canvas_board.width, 3)
        self.assertEqual(canvas_board.height, 2)
        self.assertEqual(canvas_board.data, [0 for i in range(24)])

    def test_init_invalid_imagedata_raises_value_error(self):
        imagedata = {'width': 3, 'height': 2, 'data': [0, 0]}

        with self.assertRaises(ValueError):
            CanvasBoard(imagedata)

    def test_get_pixel_for_coordinate_returns_tuple_of_rgba(self):
        red = 1
        green = 2
        blue = 3
        alpha = 4
        imagedata = {
            'width': 1,
            'height': 1,
            'data': [red, green, blue, alpha]
        }
        canvas_board = CanvasBoard(imagedata)

        rgba = canvas_board.get_pixel_for_coordinate(0, 0)

        self.assertEqual(rgba[CanvasBoard.RED], red)
        self.assertEqual(rgba[CanvasBoard.GREEN], green)
        self.assertEqual(rgba[CanvasBoard.BLUE], blue)
        self.assertEqual(rgba[CanvasBoard.ALPHA], alpha)

    def test_get_pixel_for_coordinate_invalid_coordinate_raises_value_error(
            self):
        imagedata = {'width': 1, 'height': 1, 'data': [0, 0, 0, 0]}
        canvas_board= CanvasBoard(imagedata)

        with self.assertRaises(ValueError):
            canvas_board.get_pixel_for_coordinate(100, 100)


if __name__ == '__main__':
    unittest.main()
