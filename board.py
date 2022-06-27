import numpy as np
import pyautogui
import util


class Board:
    def __init__(self, x, y, first_block_x, first_block_y):
        self.board_arr = np.zeros((x, y))
        self.util_obj = util.Util(first_block_x, first_block_y)

    # -3 = exploded mine, -2 = flag, -1 = uncovered, 0 = empty
    def block_class(self, color1, color2, color3, color4, color5):
        if (color5[0] in range(230, 256)):
            return -3
        elif (color3[0] == 0 and color3[1] == 0 and color3[2] == 0):
            return -2
        elif (color1[2] in range(230, 256)):
            return 1
        elif (color1[0] in range(0, 10) and color1[1] in range(115, 145) and color1[2] in range(115, 145)):
            return 6
        elif (color4[0] in range(0, 10) and color4[1] in range(0, 10) and color4[2] in range(0, 10)):
            return 7
        elif (color1[0] in range(115, 145) and color1[1] in range(115, 145) and color1[2] in range(115, 145)):
            return 8
        elif (color1[1] in range(115, 140)):
            return 2
        elif (color1[0] in range(230, 256)):
            return 3
        elif (color1[2] in range(115, 140)):
            return 4
        elif (color1[0] in range(115, 145)):
            return 5
        elif (color1[0] in range(180, 210)):
            if (color2 in range(240, 256)):
                return -1
            else:
                return 0

    def fill_board(self):
        lost = False
        image = pyautogui.screenshot()
        image = np.array(image)
        for i in range(0, self.board_arr.shape[0]):
            for j in range(0, self.board_arr.shape[1]):
                x_coor, y_coor = self.util_obj.find_block_coor(j, i)
                color1 = image[y_coor, x_coor]
                color2 = image[y_coor, x_coor - 10, 0]
                color3 = image[y_coor + 4, x_coor]
                color4 = image[y_coor - 4, x_coor]
                color5 = image[y_coor + 9, x_coor + 9]
                num = self.block_class(color1, color2, color3, color4, color5)
                if num == -3:
                    lost = True
                self.board_arr[i, j] = num
        return self.board_arr, lost