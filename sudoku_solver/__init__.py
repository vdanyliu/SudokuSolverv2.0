import logging
import sys

import numpy as np
from math import sqrt

from custom_dlx import DLX


class SudokuSolver:
    def __init__(self, source, dev=False):
        """

        :param source: [(0, 0, 0, .... 0), (0, 0, ....)...]
        """
        self.__init_logger(dev)
        self.size = len(source)
        self.sqrt_size = sqrt(self.size)
        self.matrix = self.__generate_coating_matrix()
        self.sudoku = source
        self.__optimize_coating_matrix()
        self.DLX = DLX(self.matrix, dev=True)

    def __generate_coating_matrix(self):
        # TODO Комменты
        size_sqr = self.size ** 2
        size_cube = self.size ** 3
        matrix = np.zeros((size_cube, 4 * size_sqr), dtype=bool)
        for x in range(size_cube):
            matrix[x][0 * size_sqr + x % size_sqr] = True
            matrix[x][1 * size_sqr + x % self.size + (x // size_sqr) * self.size] = True
            matrix[x][2 * size_sqr + x // self.size] = True
            num = x // size_sqr
            place = x % size_sqr
            col = place % self.size
            line = place // self.size
            foo = int((self.sqrt_size * (line // self.sqrt_size) + col // self.sqrt_size) + num * self.size)
            matrix[x][3 * size_sqr + foo] = True
        # logging.debug(np.ndarray.astype(matrix, dtype=int))
        return matrix

    @staticmethod
    def __init_logger(developer_mode: bool):
        np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)
        log_level = logging.INFO
        if developer_mode:
            log_level = logging.DEBUG
        logging.basicConfig(filename='sudoku.log', level=log_level, filemode='w',
                            format='%(asctime)s %(levelname)s\n %(message)s', datefmt='%H:%M:%S')

    def get_next_solution(self):
        return 0

    def __optimize_coating_matrix(self):
        del_list_of_rows = self.__sudoku_conditions_in_matrix_rows()
        del_list_of_affected_col = self.__get_list_of_affected_col_by_rows(del_list_of_rows)
        del_list_of_affected_rows = self.__get_list_of_affected_rows_by_cols(del_list_of_affected_col)+del_list_of_rows
        for x in del_list_of_affected_rows:
            self.matrix[x].fill(False)
        self.matrix = np.delete(self.matrix, del_list_of_affected_col, 1)
        # logging.debug(np.ndarray.astype(self.matrix, dtype=int))

    def __sudoku_conditions_in_matrix_rows(self):
        data = []
        size_sqr = self.size ** 2
        for x, string in enumerate(self.sudoku):
            for y, num in enumerate(string):
                if num:
                    num -= 1
                    data.append(num * size_sqr + x * self.size + y)
        logging.debug(data)
        return data

    def __get_list_of_affected_col_by_rows(self, rows):
        data = []
        for row in rows:
            for y, val in enumerate(self.matrix[row]):
                if val:
                    data.append(y)
        if data != list(dict.fromkeys(data)):
            raise Exception("Invalid SOURCE data")
        return data

    def __get_list_of_affected_rows_by_cols(self, cols):
        data = []
        matrix = self.matrix.transpose()
        for col in cols:
            for x, val in enumerate(matrix[col]):
                if val:
                    data.append(x)
        return data
