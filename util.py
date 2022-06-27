# minesweeper X = block size 20px
# minesweeper.online standard = 694, 400 (for beginner and intermediate) and 653, 400 (for advanced) block size 30 px for 24 setting
class Util:
    def __init__(self, x, y):
        self.FIRST_BLOCK_X = x
        self.FIRST_BLOCK_Y = y

    def find_block_coor(self, x, y):
        x_coor = self.FIRST_BLOCK_X + x * 20
        y_coor = self.FIRST_BLOCK_Y + y * 20
        return x_coor, y_coor