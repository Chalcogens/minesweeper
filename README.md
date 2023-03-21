# minesweeper

A simple python implementation of a 2D minesweeper game.

You can input the dimensions of the board (will be a n by n square board) and number of bombs in the board (must be less than n**2)

To open a location, type in the index of the row followed by the column (zero-indexed) in the format row,column. If there are no bombs in adjacent and directly diagonal tiles, the game digs recursively to open all adjacent non-mined and non-bomb containing cells. 

Adapted from "12 Beginner Python Projects - Coding Course" by freeCodeCamp.org
