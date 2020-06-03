# Sudoku GUI

import pygame

import StartMenuDesign
from SudokuSolve import is_valid_value, fill_board, find_empty, generate_board
import time
pygame.font.init()


class Grid:
    """
    board2 = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
    """
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    def __init__(self, rows, cols, width, height, window):
        self.rows = rows
        self.cols = cols
        # Create cell object at each position on board, storing all into 2d array
        self.cells = [[Cell(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None   # Contains the board with an inputted answer to be checked by system if it is the correct solution
        self.selected = None    # Stores tuple containing (row, col) of selected cell on board
        self.window = window

    def print_board(self):
        for rows in range(self.rows):
            if rows % 3 == 0 and rows != 0:
                print("- - - - - - - - - - -")
            for cols in range(self.cols):
                if cols % 3 == 0 and cols != 0:
                    print(" | ", end="")

                if cols == 8:  # If last position on board -> just print number and newline
                    print(self.board[rows][cols])
                elif cols == 2 or cols == 5:
                    print(self.board[rows][cols], end="")
                else:  # If not last position on board -> print number, space and no newline
                    print(str(self.board[rows][cols]) + " ", end="")

    def update_model(self):
        """ Updates model (if new values are entered onto board) """
        self.model = [[self.cells[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def draw_board(self, window):
        """ Draws grid-lines and cells """
        # Draw grid-lines
        cell_gap = self.width / 9   # Get even division of box width to draw grid-lines
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                line_thickness = 4  # Main dividing lines (3x3)
            else:
                line_thickness = 1  # Individual cell dividing lines (1x1)
            pygame.draw.line(window, (0, 0, 0), (0, int(i * cell_gap)), (self.width, int(i * cell_gap)), line_thickness)
            pygame.draw.line(window, (0, 0, 0), (int(i * cell_gap), 0), (int(i * cell_gap), self.height), line_thickness)

        # Draw cells
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw_cell(window)

    def select_cell(self, row, col):
        """ Selects the cell on the grid (and the cell itself to draw the border) """
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].selected = False

        self.cells[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].set_temp(0)

    def sketch_value(self, value):
        row, col = self.selected
        self.cells[row][col].set_temp(value)

    def check_submitted_value(self, value):
        row, col = self.selected

        # If cell is empty -> input value into cell and update model to contain inputted answer
        if self.cells[row][col].value == 0:
            self.cells[row][col].set_value(value)
            self.update_model()

            if is_valid_value(self.model, value, (row, col)) and fill_board(self.model):
                return True
            else:
                self.cells[row][col].set_value(0)
                self.cells[row][col].set_temp(0)
                self.update_model()
                return False

    def click(self, pos):
        """
        Convert pixel coordinates to index coordinates from mouse click
        :param pos: position in pixels coordinates
        :return: (row, col) of position clicked in cartesian/index coordinates
        """

        # If clicked region is w/in board area
        if pos[0] < self.width and pos[1] < self.height:
            cell_gap = self.width / 9
            x = pos[0] // cell_gap    # Floor division
            y = pos[1] // cell_gap
            return int(y), int(x)
        # If not clicking area w/in board return None
        else:
            return None

    def is_finished(self):
        """ Return True if all cells filled in, False if not """
        # Loop through all cells on board
        for i in range(self.rows):
            for j in range(self.cols):
                # If any cell is not filled in -> return false
                if self.cells[i][j].value == 0:
                    return False
        # If all cells filled in -> return true
        return True

    def show_algorithm(self):
        self.update_model()
        empty_pos = find_empty(self.model)

        # If not empty position found -> end of game
        if not empty_pos:
            return True
        else:
            row, col = empty_pos

        for i in range(1, 10):
            # If value is valid in position -> insert value and continue solving
            if is_valid_value(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cells[row][col].set_value(i)
                self.cells[row][col].draw_change(self.window, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.show_algorithm():
                    return True

                # Reset value to 0 if no answer was possible for cell and back-track
                self.model[row][col] = 0
                self.cells[row][col].set_value(0)
                self.cells[row][col].draw_change(self.window, False)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

        return False

    def set_board(self, board):
        self.board = board


class Cell:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw_cell(self, window):
        font = pygame.font.SysFont("comicsans", 40)

        cell_gap = self.width / 9
        x = self.col * cell_gap
        y = self.row * cell_gap

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, (128, 128, 128))
            window.blit(text, (int(x + 5), int(y + 5)))
        elif not(self.value == 0):
            text = font.render(str(self.value), 1, (0, 0, 0))
            window.blit(text, (int(x + (cell_gap/2 - text.get_width()/2)), int(y + (cell_gap/2 - text.get_height()/2))))

        # Highlight the selected cell with a red border
        if self.selected:
            pygame.draw.rect(window, (255, 0, 0), (int(x), int(y), int(cell_gap), int(cell_gap)), 3)

    def set_value(self, value):
        self.value = value

    def set_temp(self, value):
        self.temp = value

    def draw_change(self, window, valid=True):
        font = pygame.font.SysFont("comicsans", 40)

        cell_gap = self.width / 9
        x = self.col * cell_gap
        y = self.row * cell_gap

        pygame.draw.rect(window, (255, 255, 255), (int(x), int(y), int(cell_gap), int(cell_gap)), 0)

        text = font.render(str(self.value), 1, (0, 0, 0))
        window.blit(text, (int(x + (cell_gap/2 - text.get_width()/2)), int(y + (cell_gap/2 - text.get_height()/2))))

        # If input value is valid -> draw green border
        if valid:
            pygame.draw.rect(window, (0, 255, 0), (int(x), int(y), int(cell_gap), int(cell_gap)), 3)
        # If input value is invalid -> draw red border
        else:
            pygame.draw.rect(window, (255, 0, 0), (int(x), int(y), int(cell_gap), int(cell_gap)), 3)


def redraw_window(window, board, time, strikes):
    window.fill((255, 255, 255))
    font = pygame.font.SysFont("comicsans", 40)
    text = font.render("Time: " + format_time(time), 1, (0, 0, 0))
    window.blit(text, (540 - 160, 560))

    # Tally strikes
    text = font.render("X: " + str(strikes), 1, (255, 0, 0))
    window.blit(text, (20, 560))

    # Draw grid and board
    board.draw_board(window)


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    formatted_time = str(hour) + ":" + str(minute) + ":" + str(sec)
    return formatted_time


def main(attempts_remove):
    window = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    # Make temporary grid with default empty board
    temp = Grid(9, 9, 540, 540, window)
    # Generate a new solvable board
    generate_board(temp.board, attempts_remove)
    # Make new board with the new solvable board
    board = Grid(9, 9, 540, 540, window)
    key = None
    run = True
    start = time.time()
    strikes = 0

    timer = 0
    passed_time = 0
    clock = pygame.time.Clock()

    quit_game = False

    while run:
        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                StartMenuDesign.clear_window()
                StartMenuDesign.redraw_start_window()
                run = False
                quit_game = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cells[i][j].temp != 0:
                        if board.check_submitted_value(board.cells[i][j].temp):
                            print("Correct!")
                        else:
                            print("Incorrect!")
                            strikes += 1

                        key = None

                        if board.is_finished():
                            print("Game Over")
                            run = False

                if event.key == pygame.K_SPACE:
                    if timer == 0:
                        timer = .001
                    # If spacebar was double tapped w/in 0.5 seconds -> solve puzzle w/ algorithm and end game
                    elif timer < 0.5:
                        board.show_algorithm()    # Solve Sudoku w/ algorithm
                        board.print_board()
                        timer = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                clicked = board.click(position)
                if clicked:
                    board.select_cell(clicked[0], clicked[1])
                    key = None

        # Increase timer after spacebar was pressed the first time.
        if timer != 0:
            timer += passed_time
            # Reset after 0.5 seconds
            if timer > 0.5:
                timer = 0

        # passed_time is time in seconds since last tick.
        # Divide by 1000 to convert milliseconds to seconds.
        passed_time = clock.tick(30) / 1000

        if board.selected and key is not None:
            board.sketch_value(key)

        if not quit_game:
            # Draws board on load-up and updates upon inputs
            redraw_window(window, board, play_time, strikes)
            pygame.display.update()

