import time
import numpy as np
import keyboard
import pyautogui
import win32api
import mouse
import board
import AI


# 0 = BEGINNER, 1 = INTERMEDIATE, 2 = EXPERT
diff = 1
x, y = 0, 0

# determining the size of the grid based on difficulty
if diff == 0:
    x, y = 8, 8
elif diff == 1:
    x, y = 16, 16
else:
    x = 16
    y = 30

# finding the location of the minesweeper window
logo_location = pyautogui.locateOnScreen("minesweeper_logo.png")
FIRST_BLOCK_X = logo_location[0] + 24
FIRST_BLOCK_Y = logo_location[1] + 135

# starting the classes
mouse_obj = mouse.Mouse(FIRST_BLOCK_X, FIRST_BLOCK_Y)
board_obj = board.Board(x, y, FIRST_BLOCK_X, FIRST_BLOCK_Y)

losses = 0
wins = 0
times = []
games = 5
# running five games and displaying the statistics (winrate, time)
for k in range(games):
    print("Game", k + 1)
    # press q to interrupt AI
    if keyboard.is_pressed("q"):
        break
    start = time.time()
    wins_current = wins
    for cycle in range(75):
        # updating the board
        board_arr, lost = board_obj.fill_board()
        if cycle == 0:
            mouse_obj.first_click(board_arr)
            continue
        # determining if the game is lost
        if lost:
            losses += 1
            break
        # determining if the game is won
        if not np.isin(-1, board_arr):
            wins += 1
            break
        if keyboard.is_pressed("q"):
            break
        board_for_ai = np.copy(board_arr)
        ai_obj = AI.AI(board_for_ai, diff)
        prob_board = ai_obj.generate_prob_board()
        clicked = False
        # flagging and clicking based on the AI's output
        for i in range(0, prob_board.shape[0]):
            for j in range(0, prob_board.shape[1]):
                if (prob_board[i, j] == -2 and board_arr[i, j] != -2):
                    mouse_obj.flag_block(j, i)
                elif (prob_board[i, j] == 10):
                    clicked = True
                    mouse_obj.click_block(j, i)
        # making a random click if AI has not chosen a block to click
        if not clicked:
            mouse_obj.random_click(board_arr)
        win32api.SetCursorPos((logo_location[0], logo_location[1]))
    if wins > wins_current:
        times.append(time.time() - start)
    mouse_obj.click_reset(logo_location, y)

print("Wins = %d/%d" % (wins, games))
print("Accuracy = %d%%" % ((wins / games) * 100))
if times:    
    print("Average time per game = %.2f" % (np.mean(times)))