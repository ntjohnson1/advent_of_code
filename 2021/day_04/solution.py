import numpy as np

ROW_COUNT_IDX = 0
COL_COUNT_IDX = 1


def find_winning_board(numbers, boards, board_counts, found_board_sum):
    number_announced = -1
    for a_number in numbers:
        number_announced += 1
        found_board, found_row, found_column = np.where(boards == a_number)
        board_counts[found_board, found_row, ROW_COUNT_IDX] += 1
        board_counts[found_board, found_column, COL_COUNT_IDX] += 1
        found_board_sum[found_board] += a_number
        if np.any(board_counts == 5):
            finished_boards, _, _ = np.where(board_counts == 5)
            finished_boards = np.unique(finished_boards)
            return number_announced, finished_boards


def problem_1(numbers, boards):
    # Keep track of number of elements called per board
    # Board, index, row or column
    board_counts = np.zeros((len(boards), 5, 2), np.uint8)
    # Found board sum
    found_board_sum = np.zeros((len(boards), ))
    numbers_idx, winner_idx = find_winning_board(numbers, boards, board_counts, found_board_sum)
    board_sum = np.sum(boards[winner_idx, :, :])
    return numbers[numbers_idx] * (board_sum - found_board_sum[winner_idx])


def problem_2(numbers, boards):
    # Keep track of number of elements called per board
    # Board, index, row or column
    board_counts = np.zeros((len(boards), 5, 2), np.uint8)
    # Found board sum
    found_board_sum = np.zeros((len(boards), ))
    previous_score = 0
    total_winners = 0
    for i in range(len(boards)):
        numbers_idx, winner_idx = find_winning_board(numbers, boards, board_counts, found_board_sum)
        total_winners += len(set(winner_idx))
        if total_winners == 100:
            board_sum = np.sum(boards[winner_idx, :, :])
            return numbers[numbers_idx] * (board_sum - found_board_sum[winner_idx])
        # Continue the game without the winner
        # I think slicing or masking wouldn't require new memory use but
        # required more book keeping
        boards = np.delete(boards, winner_idx, axis=0)
        board_counts = np.delete(board_counts, winner_idx, axis=0)
        found_board_sum = np.delete(found_board_sum, winner_idx)
        numbers = numbers[numbers_idx+1:]


if __name__ == "__main__":
    input_file = 'input.txt'
    with open(input_file) as f:
        first_line = f.readline()
    bingo_numbers = np.fromstring(first_line, sep=',', dtype=np.uint8)
    bingo_boards = np.genfromtxt(input_file, skip_header=1, dtype=np.uint8).reshape([-1, 5, 5])

    print(f"Problem 1: {problem_1(bingo_numbers, bingo_boards)}")
    print(f"Problem 2: {problem_2(bingo_numbers, bingo_boards)}")
