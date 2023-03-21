import random
import re

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        #create board
        self.board = self.make_new_board()
        self.assign_values()

        #initialise set to keep track of locations already dug
        #save (row,col) tuples into this set
        self.dug = set()

    def make_new_board(self):
        #construct a new board based on dim_size and num_bombs
        #use a list of lists
        board = [[None for i in range(self.dim_size)] for j in range(self.dim_size)]

        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            row = random.randint(0,self.dim_size-1)
            col = random.randint(0,self.dim_size-1)
            if board[row][col] == "*":
                continue
            else:
                board[row][col] = "*"
                bombs_planted += 1
        return board

    def assign_values(self):
        #after planting bombs, assign numbers 0-8 to empty spaces to denote how many bombs are around it
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == "*":
                    continue
                count = 0
                for a in range(max(0,r-1),min(self.dim_size,r+2)):
                    for b in range(max(0,c-1),min(self.dim_size,c+2)):
                            if self.board[a][b] == "*":
                                count += 1
                self.board[r][c] = count

    def dig(self, row, col):
        self.dug.add((row,col))
        if self.board[row][col] == "*":
            return False
        elif self.board[row][col] > 0:
            return True
        for a in range(max(0,row-1),min(self.dim_size,row+2)):
            for b in range(max(0,col-1),min(self.dim_size,col+2)):
                if (a,b) in self.dug:
                    continue
                self.dig(a,b)
        return True

    def __str__(self):
        # this is a magic function where if you call print on this object,
        # it'll print out what this function returns!
        # return a string that shows the board to the player

        # first let's create a new array that represents what the user would see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-' * str_len + '\n' + string_rep + '-' * str_len

        return string_rep


def play(dim_size = 10, num_bombs = 10):
    #1: create board and plant bombs
    board = Board(dim_size, num_bombs)
    #2: show user board, ask where they want to dig for bombs
    #3a: if location is bomb, show game over message
    #3b: if location is not a bomb, dig recursively until each square is at least next to a bomb
    #4: repeat 2-3 until there are no more places to dig
    safe = True
    while len(board.dug) < board.dim_size** 2 - num_bombs:
        print(" ")
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col:"))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col>=board.dim_size:
            print("Invalid location. Try again.")
            continue
        safe = board.dig(row,col)
        if not safe:
            break
    if safe:
        print("")
        print("Congratulations! you beat the game!")
        print(board)
    else:
        print("")
        print("Sorry. game over...")
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == "__main__":
    play()

