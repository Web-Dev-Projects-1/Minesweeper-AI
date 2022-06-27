import time
import random
import win32api, win32con
import util


class Mouse:
    def __init__(self, first_block_x, first_block_y):
        self.util_obj = util.Util(first_block_x, first_block_y)

    def click_block(self, x, y):
        x_coor, y_coor = self.util_obj.find_block_coor(x, y)
        win32api.SetCursorPos((x_coor, y_coor))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    def flag_block(self, x, y):
        x_coor, y_coor = self.util_obj.find_block_coor(x, y)
        win32api.SetCursorPos((x_coor, y_coor))
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
        time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

    def random_click(self, board):
        uncliked_indices = []
        for i in range(0, board.shape[0]):
            for j in range(0, board.shape[1]):
                if board[i, j] == -1:
                    uncliked_indices.append([i, j])
        random_index = random.choice(uncliked_indices)
        self.click_block(random_index[1], random_index[0])
    
    def first_click(self, board):
        random_i = random.choice([0, board.shape[0] - 1])
        random_j = random.choice([0, board.shape[1] - 1])
        self.click_block(random_j, random_i)
    
    def click_reset(self, logo_location, y):
        time.sleep(0.5)
        win32api.SetCursorPos((logo_location[0] + 15 + int((y / 2)) * 20, logo_location[1] + 93))
        # beginner x + 71
        # advanced x + 290
        # offset = 15 px
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        time.sleep(0.5)