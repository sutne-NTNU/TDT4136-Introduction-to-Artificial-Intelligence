from sudoku import SudokuCSP


if __name__ == '__main__':
    boards = ['easy.txt', 'medium.txt', 'hard.txt', 'veryhard.txt']
    for board in boards:
        sudoku = SudokuCSP(f'boards/{board}')
        sudoku.solve()
        print(f'\nSolved: "{board}"')
        sudoku.print_solution()
