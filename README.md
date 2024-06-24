# Game-Of-Life

## :zap: About
This is a very basic, limited simulation of Conway's Game of Life (or just Life, if you please) made using Python and Pygame. I built it to test some patterns I found online (some interesting ones have been added for demonstration purposes). 

These are the simple rules of the Game of Life:
- Any live cell with fewer than two live neighbours dies, as if by underpopulation.
- Any live cell with two or three live neighbours lives on to the next generation.
- Any live cell with more than three live neighbours dies, as if by overpopulation.
- Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

The simulation is very basic and limited. For example, the proper Game of Life is infinite, but this simulation is limited. If cells reach the edge, they don't go on, rather they become squares, die, etcetera.

## :desktop_computer: How to run locally
Just clone the repository on your machine, and run `main.py`. You might need to install a few packages, like `pygame`.

## :grey_question: Controls
- You can draw patterns (left click) or erase them (right click)
- You can use the pre-loaded patterns with keys `0` to `9`.
- Press `<SPACE>` to pause or unpause.
- Press `c` to clear the current grid.
- Press `r` to print the currently alive cells (if you wish to create new patterns)
- If you want to use a bigger or smaller base grid, just change `CELL_SIZE` in the source code.
- If you want to change the colours, FPS, number of generations, etc. you can do so in the source code.