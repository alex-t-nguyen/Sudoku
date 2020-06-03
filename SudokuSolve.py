
# Adjacency list board
import pygame
import random
from StartMenuDesign import redraw_loading_screen
pygame.font.init()

board2 = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]
board = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
]


def check_board(bo, counter):
    empty_pos = find_empty(bo)

    # If no more empty positions -> board is solved
    if not empty_pos:
        return True
    # Else get coord of empty position
    else:
        (row, col) = empty_pos

    for i in range(1, 10):
        if is_valid_value(bo, i, (row, col)):
            bo[row][col] = i
            if find_empty(bo) is None:
                counter[0] += 1
                break
            elif check_board(bo, counter):
                return True
    bo[row][col] = 0


def fill_board(bo):
    number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    empty_pos = find_empty(bo)

    # If no more empty positions -> board is solved
    if not empty_pos:
        return True
    # Else get coord of empty position
    else:
        (row, col) = empty_pos

    # Loop through all possible values and insert into position until valid
    random.shuffle(number_list)
    for i in number_list:
        # If value is valid in position -> insert value and continue solving board
        if is_valid_value(bo, i, (row, col)):
            bo[row][col] = i

            # If board reaches end -> puzzle is solved -> return True
            if fill_board(bo):
                return True
            # If no possible number works in position -> reset position to 0 and backtrack to previous position
            else:
                bo[row][col] = 0

    # If board was not solvable b/c wrong answer -> return False
    return False


def is_valid_value(bo, num, pos):
    """ Checks if inputted value is a possible valid answer or not """
    # Check column for same number
    for rows in range(len(bo)):
        if bo[rows][pos[1]] == num and pos[0] != rows:
            return False

    # Check row for same number
    for cols in range(len(bo[pos[0]])):
        if bo[pos[0]][cols] == num and pos[1] != cols:
            return False

    # Check box for same number
    box_row = pos[0] // 3    # "//" -> Floor division b/c "/" returns decimal
    box_col = pos[1] // 3

    for rows in range(box_row * 3, box_row * 3 + 3):
        for cols in range(box_col * 3, box_col * 3 + 3):
            if bo[rows][cols] == num and (rows, cols) != pos:
                return False

    # Passed all checks -> number is valid
    return True


def print_board(bo):
    for rows in range(len(bo)):
        if rows % 3 == 0 and rows != 0:
            print("- - - - - - - - - - -")
        for cols in range(len(bo)):
            if cols % 3 == 0 and cols != 0:
                print(" | ", end="")

            if cols == 8:   # If last position on board -> just print number and newline
                print(bo[rows][cols])
            elif cols == 2 or cols == 5:
                print(bo[rows][cols], end="")
            else:   # If not last position on board -> print number, space and no newline
                print(str(bo[rows][cols]) + " ", end="")


def find_empty(bo):
    for rows in range(len(bo)):
        for cols in range(len(bo[rows])):
            if bo[rows][cols] == 0:
                return (rows, cols)  # return row, col tuple of empty space
    return None


def generate_board(bo, attempts_remove):
    # First generate a fully solved board
    fill_board(bo)

    while attempts_remove > 0:
        redraw_loading_screen()
        counter = [0]
        # Choose random cell on board
        x = random.randint(0, len(bo) - 1)
        y = random.randint(0, len(bo[0]) - 1)
        while bo[x][y] == 0:
            x = random.randint(0, len(bo) - 1)
            y = random.randint(0, len(bo[0]) - 1)

        # Save number in case it cannot be removed
        backup = bo[x][y]
        # Remove number at randomly generated position
        bo[x][y] = 0

        check_board(bo, counter)
        # If number at position could not be removed -> put back number and decrease number of attempts left to remove a cell
        if counter[0] != 1:
            bo[x][y] = backup
            attempts_remove -= 1
        print(attempts_remove)
    return bo


def main():
    attempts_remove = 40
    print_board(board)
    # solve_board(board)
    generate_board(board, attempts_remove)
    print()
    print_board(board)


if __name__ == '__main__':
    main()


#solve_board(board)
#print_board(board)
