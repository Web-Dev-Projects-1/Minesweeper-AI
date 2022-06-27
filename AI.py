import numpy as np
from itertools import product


class AI:
    def __init__(self, board, diff):
        self.board = board
        self.number_blocks_dict = {}
        self.long_depth = 3
        # long depth decreased to improve speed on expert
        if diff == 2:
            self.long_depth -= 1
        self.square_depth = 1

    def generate_prob_board(self):
        for i in range(0, self.board.shape[0]):
            for j in range(0, self.board.shape[1]):
                if (self.board[i, j] in range(1, 9)):
                    self.number_blocks_dict[(i, j)] = []
        # FIRST CYCLE - naive, to clear obvious ones
        for number_block in self.number_blocks_dict:
            self.flag_around(number_block[0], number_block[1])
        for number_block in self.number_blocks_dict:
            self.safe_around(number_block[0], number_block[1])
        # SECOND CYCLE - probability based, more powerful
        # creating a dictinary that contains the number blocks as key and indexes of surrounding hidden blocks
        for number_block in self.number_blocks_dict:
            self.number_blocks_dict[number_block], _ = self.find_hidden_and_flags(number_block[0], number_block[1])
        for number_block in self.number_blocks_dict:
            if self.number_blocks_dict[number_block]:
                # generating a long block around each number block
                block_around, min_i, min_j = self.long_block_around(number_block)
                # generating a probability around the block
                self.generate_prob_block(block_around, min_i, min_j)
                # generating a square block around each number block
                block_around, min_i, min_j = self.square_block_around(number_block)
                # generating a probability around the block
                self.generate_prob_block(block_around, min_i, min_j)
        # THIRD CYCLE - naive again
        for number_block in self.number_blocks_dict:
            self.flag_around(number_block[0], number_block[1])
        for number_block in self.number_blocks_dict:
            self.safe_around(number_block[0], number_block[1])
        return self.board

    # HARD CODED RULES SECTION
    def flag_around(self, i, j):
        block_num = self.board[i, j]
        hidden_blocks, flag_blocks = self.find_hidden_and_flags(i, j)
        if (len(hidden_blocks) + len(flag_blocks) == block_num):
            for hidden_block in hidden_blocks:
                self.board[hidden_block[0], hidden_block[1]] = -2      # marking blocks as bombs

    def safe_around(self, i, j):
        block_num = self.board[i, j]
        hidden_blocks, flag_blocks = self.find_hidden_and_flags(i, j)
        if (len(flag_blocks) == block_num):
            if hidden_blocks:
                for hidden_block in hidden_blocks:
                    self.board[hidden_block[0], hidden_block[1]] = 10  # marking blocks as safe

    # finding hidden blocks and flagged blocks around the number blocks
    def find_hidden_and_flags(self, i, j):
        hidden_blocks = []
        flag_blocks = []
        for i_inner in range(i - 1, i + 2):
            for j_inner in range(j - 1, j + 2):
                if (i_inner in range(0, self.board.shape[0]) and j_inner in range(0, self.board.shape[1])):
                    if (self.board[i_inner, j_inner] == -1):
                        hidden_blocks.append([i_inner, j_inner])
                    if (self.board[i_inner, j_inner] == -2):
                        flag_blocks.append([i_inner, j_inner])
        return hidden_blocks, flag_blocks
    
    # PROBABILITY SECTION
    def long_block_around(self, number_block):
        hidden_blocks = self.number_blocks_dict[number_block]
        hidden_by_i = sorted(hidden_blocks, key = lambda x: x[0])
        hidden_by_j = sorted(hidden_blocks, key = lambda x: x[1])
        min_i, max_i = min(hidden_by_i[0][0], number_block[0]), max(hidden_by_i[-1][0], number_block[0])
        min_j, max_j = min(hidden_by_j[0][1], number_block[1]), max(hidden_by_j[-1][1], number_block[1])
        # hidden blocks to the left of number
        if (number_block[1] > hidden_by_j[0][1] and number_block[1] > hidden_by_j[-1][1]):
            min_i, max_i = hidden_by_j[0][0], hidden_by_j[-1][0]
            min_j, max_j = hidden_by_j[0][1], number_block[1]
            for _ in range(self.long_depth):
                if min_i != 0:
                    if (self.board[min_i - 1][min_j] in range(-2, 0) and self.board[min_i - 1][max_j] in range(1, 9)):
                        min_i -= 1
            if min_i != 0:
                min_i -= 1
            for _ in range(self.long_depth):
                if max_i != self.board.shape[0] - 1:
                    if (self.board[min_i + 1][min_j] in range(-2, 0) and self.board[min_i + 1][max_j] in range(1, 9)):
                        max_i += 1
            if max_i != self.board.shape[0] - 1:
                max_i += 1
        # hidden blocks to the right of number
        elif (number_block[1] < hidden_by_j[0][1] and number_block[1] < hidden_by_j[-1][1]):
            min_i, max_i = hidden_by_j[0][0], hidden_by_j[-1][0]
            min_j, max_j = number_block[1], hidden_by_j[0][1]
            for _ in range(self.long_depth):
                if min_i != 0:
                    if (self.board[min_i - 1][min_j] in range(1, 9) and self.board[min_i - 1][max_j] in range(-2, 0)):
                        min_i -= 1
            if min_i != 0:
                min_i -= 1
            for _ in range(self.long_depth):
                if max_i != self.board.shape[0] - 1:
                    if (self.board[min_i + 1][min_j] in range(1, 9) and self.board[min_i + 1][max_j] in range(-2, 0)):
                        max_i += 1
            if max_i != self.board.shape[0] - 1:
                max_i += 1
        # hidden blocks below the number
        elif (number_block[0] > hidden_by_i[0][0] and number_block[0] > hidden_by_i[-1][0]):
            min_i, max_i = hidden_by_j[0][0], number_block[0]
            min_j, max_j = hidden_by_i[0][1], hidden_by_i[-1][1]
            for _ in range(self.long_depth):
                if min_j != 0:
                    if (self.board[min_i][min_j - 1] in range(-2, 0) and self.board[max_i][min_j - 1] in range(1, 9)):
                        min_j -= 1
            if min_j != 0:
                min_j -= 1
            for _ in range(self.long_depth):
                if max_j != self.board.shape[1] - 1:
                    if (self.board[min_i + 1][min_j] in range(-2, 0) and self.board[min_i + 1][max_j] in range(1, 9)):
                        max_j += 1
            if max_j != self.board.shape[1] - 1:
                max_j += 1
        # hidden blocks above the number
        elif (number_block[0] < hidden_by_i[0][0] and number_block[0] < hidden_by_i[-1][0]):
            min_i, max_i = number_block[0], hidden_by_j[0][0]
            min_j, max_j = hidden_by_i[0][1], hidden_by_i[-1][1]
            for _ in range(self.long_depth):
                if min_j != 0:
                    if (self.board[min_i][min_j - 1] in range(1, 9) and self.board[max_i][min_j - 1] in range(-2, 0)):
                        min_j -= 1
            if min_j != 0:
                min_j -= 1
            for _ in range(self.long_depth):
                if max_j != self.board.shape[1] - 1:
                    if (self.board[min_i + 1][min_j] in range(1, 9) and self.board[min_i + 1][max_j] in range(-2, 0)):
                        max_j += 1
            if max_j != self.board.shape[1] - 1:
                max_j += 1
        # taking the block
        block_around = np.copy(self.board[min_i:max_i + 1, min_j:max_j + 1])
        block_around = self.preprocess_block(block_around, min_i, min_j)
        return block_around, min_i, min_j
    
    def square_block_around(self, number_block):
        hidden_blocks = self.number_blocks_dict[number_block]
        hidden_by_i = sorted(hidden_blocks, key = lambda x: x[0])
        hidden_by_j = sorted(hidden_blocks, key = lambda x: x[1])
        min_i, max_i = min(hidden_by_i[0][0], number_block[0]), max(hidden_by_i[-1][0], number_block[0])
        min_j, max_j = min(hidden_by_j[0][1], number_block[1]), max(hidden_by_j[-1][1], number_block[1])
        # widening the block according to the depth
        for _ in range(self.square_depth):
            if min_i != 0:
                min_i -= 1
            if min_j != 0:
                min_j -= 1
            if max_i != self.board.shape[0] - 1:
                max_i += 1
            if max_j != self.board.shape[1] - 1:
                max_j += 1
        # taking the block
        block_around = np.copy(self.board[min_i:max_i + 1, min_j:max_j + 1])
        block_around = self.preprocess_block(block_around, min_i, min_j)
        return block_around, min_i, min_j 

    def preprocess_block(self, block_around, min_i, min_j):
        hidden_blocks = []
        number_blocks = []
        # finding hidden and number blocks
        for i in range(0, block_around.shape[0]):
            for j in range(0, block_around.shape[1]):
                if block_around[i, j] == -1:
                    hidden_blocks.append([i, j])
                elif block_around[i, j] in range(1, 9):
                    number_blocks.append([i, j])
        # removing wrong number blocks
        for number_block in number_blocks:
            i, j = number_block[0], number_block[1]
            remove_number = False
            for i_inner in range(i - 1, i + 2):
                for j_inner in range(j - 1, j + 2):
                    if (min_i + i_inner in range(0, self.board.shape[0]) 
                    and min_j + j_inner in range(0, self.board.shape[1])):
                        if (self.board[min_i + i_inner, min_j + j_inner] == -1):
                            if (i_inner < 0 or i_inner > block_around.shape[0] - 1 or j_inner < 0 or j_inner > block_around.shape[1] - 1):
                                remove_number = True
                        elif (self.board[min_i + i_inner, min_j + j_inner] == -2):
                            if (i_inner < 0 or i_inner > block_around.shape[0] - 1 or j_inner < 0 or j_inner > block_around.shape[1] - 1):
                                block_around[i, j] -= 1
            if remove_number:
                block_around[i, j] = -5          # value of -5 for blocks to ignore
        # removing wrong hidden blocks
        for hidden_block in hidden_blocks:
            i, j = hidden_block[0], hidden_block[1]
            remove_hidden = True
            for i_inner in range(i - 1, i + 2):
                for j_inner in range(j - 1, j + 2):
                    if (i_inner in range(0, block_around.shape[0]) and j_inner in range(0, block_around.shape[1])):
                        if (block_around[i_inner, j_inner] in range(1, 9)):
                            remove_hidden = False
            if remove_hidden:
                block_around[i, j] = -5          # value of -5 for blocks to ignore
        return block_around

    def generate_prob_block(self, block_around, min_i, min_j):
        arr = np.copy(block_around)
        arr = arr.astype(float)
        hidden_blocks = []
        number_blocks = []
        # finding the indexes of number and hidden blocks
        for i in range(0, arr.shape[0]):
            for j in range(0, arr.shape[1]):
                if (arr[i, j] in range(0, 9)):
                    number_blocks.append([i, j])
                elif (arr[i, j] == -1):
                    hidden_blocks.append([i, j])
        if len(number_blocks) == 1:
            return
        arrangements = []
        # generating all combinations of bomb positions in hidden blocks
        combs_list = list(product([-2, -1], repeat = len(hidden_blocks)))
        # inserting those arrangements into the matrices
        for i in range(0, len(combs_list)):
            comb_arr = np.copy(arr)
            for j in range(0, len(combs_list[i])):
                comb_arr[hidden_blocks[j][0], hidden_blocks[j][1]] = combs_list[i][j]
            arrangements.append(comb_arr)
        # generating the numbers on number blocks in those matrices
        for arrangement in arrangements:
            for number in number_blocks:
                bombs = 0
                i, j = number[0], number[1]
                for i_inner in range(i - 1, i + 2):
                    for j_inner in range(j - 1, j + 2):
                        if (i_inner in range(0, arrangement.shape[0]) and j_inner in range(0, arrangement.shape[1])):
                            if (arrangement[i_inner, j_inner] == -2):
                                bombs += 1
                arrangement[i, j] = bombs
        # finding the correct arrangements, aka the ones where the numbers on number blocks correspond to our situation
        right_arrangements = []
        for arrangement in arrangements:
            wrong = False
            for number in number_blocks:
                if arrangement[number[0], number[1]] != arr[number[0], number[1]]:
                    wrong = True
            if not wrong:
                right_arrangements.append(arrangement)
        # creating the matrix to store bomb probabilities
        prob_matrix = np.copy(arr)
        for index in hidden_blocks:
            prob_matrix[index[0], index[1]] = 0
        # counting the number of times each hidden block contained a bomb in each possible arrangement
        for right_arrangement in right_arrangements:
            for index in hidden_blocks:
                if (right_arrangement[index[0], index[1]] == -2):
                    prob_matrix[index[0], index[1]] += 1
        # inserting the obtained info in the board matrix
        for index in hidden_blocks:
            arr[index[0], index[1]] = prob_matrix[index[0], index[1]] / len(right_arrangements)
            if arr[index[0], index[1]] == 0:
                # 100% not a bomb = value of 10
                self.board[min_i + index[0], min_j + index[1]] = 10
            elif arr[index[0], index[1]] == 1:
                # 100% a bomb = value of -2
                self.board[min_i + index[0], min_j + index[1]] = -2