from csp import CSP


class SudokuCSP:

    def __init__(self, filename) -> None:
        """
        Instantiate a CSP representing the Sudoku board found in the text
        file named 'filename'.
        """
        self.csp = CSP()
        self.solution = None
        board = list(map(lambda x: x.strip(), open(filename, 'r')))
        for row in range(9):
            for col in range(9):
                if board[row][col] == '0':
                    self.csp.add_variable(
                        f'{row}-{col}', list(map(str, range(1, 10))))
                else:
                    self.csp.add_variable(f'{row}-{col}', [board[row][col]])
        for row in range(9):
            self.csp.add_all_different_constraint(
                [f'{row}-{col}' for col in range(9)])
        for col in range(9):
            self.csp.add_all_different_constraint(
                [f'{row}-{col}' for row in range(9)])
        for box_row in range(3):
            for box_col in range(3):
                cells = []
                for row in range(box_row * 3, (box_row + 1) * 3):
                    for col in range(box_col * 3, (box_col + 1) * 3):
                        cells.append(f'{row}-{col}')
                self.csp.add_all_different_constraint(cells)

    def solve(self):
        if self.solution is not None:
            print('Board is already solved')
            return
        self.solution = self.csp.backtracking_search()

    def print_solution(self):
        """
        Convert the representation of a Sudoku solution as returned from
        the method CSP.backtracking_search(), into a human readable
        representation.
        """
        if self.solution is None:
            print("Board isn't solved yet")
            return
        print('+-------+-------+-------+')
        for row in range(9):
            for col in range(9):
                if col in [0, 3, 6]:
                    print('| ', end='')
                print(self.solution[f'{row}-{col}'][0], end=' ')
                if col == 8:
                    print('| ', end='')
            print('')
            if row == 2 or row == 5:
                print('|-------+-------+-------|')
        print('+-------+-------+-------+')
        print(
            f'number of "backtrack()" calls: {self.csp.counter_backtrack_calls}')
        print(
            f'number of "backtrack()" fails: {self.csp.counter_backtrack_fails}')
