from utils import solution_timing
import numpy as np


def parse_file(a_file):
    """
    Parse provided fold definitions
    :param a_file:
    :return: (np.array, np.array) (initial board, folds)
        Initial board is boolean matrix, folds is vector with convention
            +val is x fold -val is y fold
    """
    fold_x = "fold along x="
    fold_y = "fold along y="
    x_indices = []
    y_indices = []
    folds = []
    with open(a_file, 'r') as f:
        for line in f:
            line = line.rstrip()
            is_fold_x = fold_x in line
            is_fold_y = fold_y in line
            if len(line) == 0:
                continue
            elif not is_fold_x and not is_fold_y:
                x_index, y_index = line.split(',')
                x_indices.append(int(x_index))
                y_indices.append(int(y_index))
            elif is_fold_x:
                folds.append(int(line.split(fold_x)[1]))
            elif is_fold_y:
                folds.append(-int(line.split(fold_y)[1]))
            else:
                raise ValueError(f"Bad parse of line: {line}")

    board = np.zeros((max(y_indices)+1, max(x_indices)+1), dtype=np.bool)
    board[y_indices, x_indices] = True

    return board, np.array(folds)


def perform_fold(board, a_fold):
    """
    Originally assumed we always folded in half.
    Currently assumes that folded piece is <= size of stationary piece.
    """
    # Should resolve redundancy here, but didn't
    if a_fold < 0:
        original_board = board[0:-a_fold, :]
        folded_board = np.flipud(board[-a_fold+1:, :])
        non_overlapping_count = original_board.shape[0] - folded_board.shape[0]
        original_board[non_overlapping_count:, :] |= folded_board
    else:
        original_board = board[:, 0:a_fold]
        folded_board = np.fliplr(board[:, a_fold + 1:])
        non_overlapping_count = original_board.shape[1] - folded_board.shape[1]
        original_board[:, non_overlapping_count:] |= folded_board

    return original_board


def problem_1(board, folds):
    return np.sum(perform_fold(board, folds[0]))


def problem_2(board, folds):
    for a_fold in folds:
        board = perform_fold(board, a_fold)
    return board


def generate_viz(final_board):
    """
    I found this quite hard to read and wasn't going to program a decoder
    """
    for a_row in final_board:
        list_col = []
        for a_col in a_row:
            if a_col > 0:
                list_col.append('#')
            else:
                list_col.append('.')
        print(list_col)


if __name__ == "__main__":
    input_file = "input.txt"
    board, folds = parse_file(input_file)

    with solution_timing("Problem 1"):
        print(problem_1(board, folds))
    with solution_timing("Problem 2"):
        final_board = problem_2(board, folds)
        print("See viz")
        generate_viz(final_board)

