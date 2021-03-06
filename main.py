#!/usr/bin/env python3.8
import logging
import sys
import itertools

from sudoku_solver import SudokuSolver

if __name__ == '__main__':
    sudoku_data = []
    with open(sys.argv[1]) as f:
        lines = f.readlines()
        for line in lines:
            sudoku_data.append(tuple(map(int, (line.split()))))
    test = SudokuSolver(tuple(sudoku_data), dev=True)
    i = 0
    for solve in test.solves():
        print(solve)
        break


