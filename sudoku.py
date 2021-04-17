import pygame as pg
from pygame import *

pg.init()
height = 900
width = 900
display = [width, height]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BROWN = (165, 42, 42)
GREEN = (0, 128, 0)
window = pg.display.set_mode(display)
pg.font.init()
font = pg.font.SysFont("Helvetica", 75)
"""board = the entire board, 9x9 board"""
board = [["" for i in range(9)] for j in range(9)]
"""boxes[i] = each box, boxes[i][j] each row within the box, boxes[i][j][k] = each element within each box"""
boxes = []
"""boxAssign is a way of converting the row and column of the mouse into the box, so it can be used for boxes."""
boxAssign = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]


# TODO: create a chess with sudoku game, don't know the rules, brother says the goal of the game is to stalemate,
#  not too sure about that idea


def createBoxes(grid):
    boxesDuplicate = [[["" for i in range(3)] for j in range(3)] for k in range(9)]
    for i in range(9):
        for j in range(9):
            if grid[i][j] != "":
                boxCount = boxAssign[j // 3][i // 3]
                boxesDuplicate[boxCount][i % 3][j % 3] = grid[i][j]
    return boxesDuplicate


""" check whether number is allowed, used for user input AND for algorithm"""


def checkRow(grid, numberAttempt, columnCheck):
    for i in range(9):
        if grid[i][columnCheck] == numberAttempt:
            return False
    return True


def checkColumn(grid, numberAttempt, rowCheck):
    for i in range(9):
        if grid[rowCheck][i] == numberAttempt:
            return False
    return True


def checkBox(box, numberAttempt, rowCheck, columnCheck):
    boxNumber = boxAssign[columnCheck // 3][rowCheck // 3]
    for i in range(3):
        for j in range(3):
            if box[boxNumber][i][j] == numberAttempt:
                return False
    return True


def checkGrid(grid):
    global board
    for i in range(9):
        for j in range(9):
            if grid[i][j] == "":
                return False
    board = grid
    return True


def backTrack(grid):
    global board
    rowChange = ""
    columnChange = ""
    stop = False
    for i in range(9):
        for j in range(9):
            if grid[j][i] == "":
                rowChange = i
                columnChange = j
                for k in range(1, 10):
                    boxesDuplicate = createBoxes(grid)
                    if checkRow(grid, k, i) and checkColumn(grid, k, j) and checkBox(boxesDuplicate, k, j, i):
                        grid[j][i] = k
                        board = grid
                        Game()
                        if checkGrid(grid):
                            return True
                        else:
                            if backTrack(grid):
                                return True
                stop = True
                break
        if stop:
            break
    if rowChange != "":
        grid[columnChange][rowChange] = ""


class Game():
    def __init__(self):
        window.fill(WHITE)
        global boxes
        """Draw vertical lines make each third one thicker"""
        for i in range(9):
            thick = 1
            if i % 3 == 0:
                thick = 2
            pg.draw.line(window, BLACK, ((i * 100), 0), ((i * 100), height), thick)
        """Draw horizontal lines make each third one thicker"""
        for i in range(9):
            thick = 1
            if i % 3 == 0:
                thick = 2
            pg.draw.line(window, BLACK, (0, (i * 100)), (width, (i * 100)), thick)
        """Display text on the window"""

        for i in range(9):
            for j in range(9):
                if board[i][j] != "":
                    img = font.render(str(board[i][j]), True, BLACK)
                    window.blit(img, (i * 100 + 30, j * 100))
        boxes = createBoxes(board)
        pg.display.update()


Game()

row = -1
column = -1
while True:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if row != -1 and 49 <= event.key <= 57:
                """ASCII values are used for event.key, so subtracting 48 makes it the number pressed"""
                numberPressed = event.key - 48
                if checkRow(board, numberPressed, column) and checkColumn(board, numberPressed, row) and checkBox(boxes, numberPressed, row,
                                                                                                    column):
                    board[row][column] = numberPressed
                """make user have to press on a square again to get user input"""
                row, column = -1, -1
            """if the user presses the space key, than the algorithm starts working"""
            if event.key == 32:
                fakeBoard = board
                backTrack(fakeBoard)
            if event.key == 8:
                board[row][column] = ""

        """if user presses exit button"""
        if event.type == QUIT:
            pg.quit()
            break
        elif event.type == MOUSEBUTTONDOWN:
            """get position of mouse, and then make this where the user wants to edit"""
            pos = pg.mouse.get_pos()
            row = pos[0] // 100
            column = pos[1] // 100
    Game()