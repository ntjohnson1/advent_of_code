from utils import solution_timing
import numpy as np

MAX_SYMBOLS = 150


def lazy_converter(a_line):
    line_len = len(a_line)
    if line_len > MAX_SYMBOLS:
        raise ValueError(f"Line length {line_len} greater than max symbols {MAX_SYMBOLS}")
    a_line = a_line.replace(b'(', b'-3,')
    a_line = a_line.replace(b')', b'3,')
    a_line = a_line.replace(b'[', b'-57,')
    a_line = a_line.replace(b']', b'57,')
    a_line = a_line.replace(b'{', b'-1197,')
    a_line = a_line.replace(b'}', b'1197,')
    a_line = a_line.replace(b'<', b'-25137,')
    a_line = a_line.replace(b'>', b'25137,')
    parsed_line = np.zeros((MAX_SYMBOLS, ), dtype=np.int32)
    parsed_line[:line_len] = np.fromstring(a_line, sep=',', dtype=np.int32)
    return parsed_line


def problem_1(pattern_arrays):
    """
    We close patterns in the order they were open.
    Trying to use our matrix in place as our LIFO queue for matching.
    """
    num_observations = len(pattern_arrays, )
    # Our contract is that the spaces between forward and backward are zero
    forward_idx = np.ones((num_observations, ), dtype=np.int16)
    backward_idx = np.zeros((num_observations, ), dtype=np.int16)
    first_breaking_pattern = np.zeros((num_observations, ), dtype=np.int16)
    broken_initial_characters = pattern_arrays[np.arange(num_observations), backward_idx] > 0
    first_breaking_pattern[broken_initial_characters] = pattern_arrays[broken_initial_characters, 0]
    not_already_found = ~broken_initial_characters

    i = 0
    while np.any(forward_idx < MAX_SYMBOLS-1):

        if np.any(backward_idx < 0):
            raise ValueError("Sad")

        # Case 0: We've reached our padding zeros
        fwd_slice = np.arange(num_observations), forward_idx
        finished = pattern_arrays[fwd_slice] == 0
        forward_idx[finished] = MAX_SYMBOLS-1

        # Case 1: We've matched a close to our most recent open
        fwd_slice = np.arange(num_observations), forward_idx
        bwd_slice = np.arange(num_observations), backward_idx
        matching_patterns = pattern_arrays[fwd_slice] == -pattern_arrays[bwd_slice]
        if np.any(matching_patterns):
            pattern_arrays, forward_idx, backward_idx = \
                matched_patterns(matching_patterns, pattern_arrays, forward_idx, backward_idx)

        # Case 2: Found a new open symbol
        fwd_slice = np.arange(num_observations), forward_idx
        bwd_slice = np.arange(num_observations), backward_idx
        new_open_mask = (pattern_arrays[fwd_slice] < 0) & (pattern_arrays[bwd_slice] <= 0)
        pattern_arrays, forward_idx, backward_idx = \
            new_open(new_open_mask, pattern_arrays, forward_idx, backward_idx)

        # Case 3: We close something we shouldn't
        fwd_slice = np.arange(num_observations), forward_idx
        bwd_slice = np.arange(num_observations), backward_idx
        matching_patterns = pattern_arrays[fwd_slice] == -pattern_arrays[bwd_slice]
        bad = (pattern_arrays[np.arange(num_observations), forward_idx] > 0) & ~matching_patterns
        bad = bad & not_already_found
        matching_idx = np.where(bad)[0]
        fwd_slice = matching_idx, forward_idx[matching_idx]
        if len(matching_idx) > 0:
            first_breaking_pattern[matching_idx] = pattern_arrays[fwd_slice]
        pattern_arrays, forward_idx, backward_idx = \
            bad_syntax(bad, pattern_arrays, forward_idx, backward_idx)
        not_already_found = not_already_found & ~bad
        i += 1

    return first_breaking_pattern


def bad_syntax(matching_patterns, pattern_arrays, forward_idx, backward_idx):
    """
    The there is a close symbol that doesn't match the most recent open.
    Push forward and backward to the end of the array set to a positive constant to skip further consideration
    """
    matching_idx = np.where(matching_patterns)[0]

    forward_idx[matching_idx] = MAX_SYMBOLS - 1
    backward_idx[matching_idx] = MAX_SYMBOLS - 2

    bwd_slice = np.ix_(matching_idx, backward_idx[matching_idx])
    fwd_slice = np.ix_(matching_idx, forward_idx[matching_idx])
    # This breaks our assumption so now cases shall trigger after
    pattern_arrays[fwd_slice] = -9999
    pattern_arrays[bwd_slice] = 9999

    return pattern_arrays, forward_idx, backward_idx


def new_open(matching_patterns, pattern_arrays, forward_idx, backward_idx):
    """
    We have found a new open symbol. Shuffle it from our unobserved list to our queue
    """
    from itertools import repeat
    matching_idx = np.where(matching_patterns)[0]

    # this swap is probably overkill. An assign then clear is probably easier
    bwd_slice = matching_idx, (backward_idx + 1)[matching_idx]
    fwd_slice = matching_idx, forward_idx[matching_idx]
    pattern_arrays[bwd_slice], pattern_arrays[fwd_slice] = \
            pattern_arrays[fwd_slice], pattern_arrays[bwd_slice]
    # update indices
    forward_idx[matching_idx] += 1
    backward_idx[matching_idx] += 1
    backward_idx[backward_idx == forward_idx] -= 1
    forward_idx[forward_idx >= MAX_SYMBOLS] = MAX_SYMBOLS - 1
    return pattern_arrays, forward_idx, backward_idx


def matched_patterns(matching_patterns, pattern_arrays, forward_idx, backward_idx):
    """
    If we have matched symbols clear them from our matrix and update our indices
    """
    # Mixing logical and boolean indexing confuses things. Logical is the easiest way to reason about it
    # but integer is cleaner to validate
    matching_idx = np.where(matching_patterns)
    pattern_arrays[matching_idx, forward_idx[matching_idx]] = 0
    pattern_arrays[matching_idx, backward_idx[matching_idx]] = 0

    # Update indices
    forward_idx[matching_idx] += 1
    backward_idx[matching_idx] -= 1
    # Lazy check for now
    backward_idx[backward_idx < 0] = 0
    forward_idx[forward_idx >= MAX_SYMBOLS] = MAX_SYMBOLS-1

    return pattern_arrays, forward_idx, backward_idx


def matching_sanity():
    num_observations = 3
    pattern = np.array([
        [0, -1, 1, 0],
        [-1, 1, 0, 0],
        [-1, -2, 0, 0]
    ])
    fwd_idx = np.array([2, 1, 1])
    bwd_idx = np.array([1, 0, 0])
    matching_patterns = pattern[np.arange(num_observations), fwd_idx] == -pattern[
        np.arange(num_observations), bwd_idx]
    pattern_arrays, forward_idx, backward_idx = matched_patterns(matching_patterns, pattern, fwd_idx, bwd_idx)
    assert np.all(forward_idx == np.array([3, 2, 1]))
    assert np.all(backward_idx == np.array([0, 0, 0]))
    assert np.all(pattern_arrays == np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [-1, -2, 0, 0]
    ]))


def open_sanity():
    num_observations = 3
    pattern = np.array([
        [0, -2, 0, -3, 0],
        [-1, -4, 0, 0, 0],
        [-1, 1, 0, 0, 0]
    ])
    fwd_idx = np.array([3, 1, 1])
    bwd_idx = np.array([1, 0, 0])
    fwd_slice = np.arange(num_observations), fwd_idx
    bwd_slice = np.arange(num_observations), bwd_idx
    new_open_mask = (pattern[fwd_slice] < 0) & (pattern[bwd_slice] < 0)
    pattern_arrays, forward_idx, backward_idx = new_open(new_open_mask, pattern, fwd_idx, bwd_idx)
    assert np.all(forward_idx == np.array([4, 2, 1]))
    assert np.all(backward_idx == np.array([2, 1, 0]))
    assert np.all(pattern_arrays == np.array([
        [0, -2, -3, 0, 0],
        [-1, -4, 0, 0, 0],
        [-1, 1, 0, 0, 0]
    ]))


def bad_sanity():
    """
    This requires setting MAX_SYMBOLS global to 5 because I didn't want to plumb it through
    """
    num_observations = 3
    pattern = np.array([
        [0, -2, 0, 3, 0],
        [-1, 4, 0, 0, 0],
        [-1, 1, 0, 0, 0]
    ])
    fwd_idx = np.array([3, 1, 1])
    bwd_idx = np.array([1, 0, 0])
    matching_patterns = pattern[np.arange(num_observations), fwd_idx] == -pattern[
        np.arange(num_observations), bwd_idx]
    bad = (pattern[np.arange(num_observations), fwd_idx] > 0) & ~matching_patterns
    pattern_arrays, forward_idx, backward_idx = bad_syntax(bad, pattern, fwd_idx, bwd_idx)
    assert np.all(forward_idx == np.array([MAX_SYMBOLS-1, MAX_SYMBOLS-1, 1]))
    assert np.all(backward_idx == np.array([MAX_SYMBOLS-2, MAX_SYMBOLS-2, 0]))
    assert np.all(pattern_arrays == np.array([
        [0, -2, 0, 9999, -9999],
        [-1, 4, 0, 9999, -9999],
        [-1, 1, 0, 0, 0]
    ]))


def problem_2(patterns, first_breaking_patterns):
    missing_patterns = np.where(first_breaking_patterns==0)[0]
    patterns[patterns == 9999] = 0
    patterns[patterns == -9999] = 0
    patterns[patterns == -3] = 1
    patterns[patterns == -57] = 2
    patterns[patterns == -1197] = 3
    patterns[patterns == -25137] = 4
    np_score = np.zeros(len(missing_patterns,))
    for score_idx, line_idx in enumerate(missing_patterns):
        non_zero_idx = np.where(patterns[line_idx])[0]
        non_zeros = np.array(patterns[line_idx, non_zero_idx], dtype=np.uint64)
        np_score[score_idx] = np.dot(5**np.arange(len(non_zeros)), non_zeros)

    return np.median(np_score)


if __name__ == "__main__":
    input_file = "input.txt"
    patterns = np.loadtxt(input_file, converters={0: lazy_converter}, delimiter=",", dtype=np.int16)
    with solution_timing("Problem 1"):
        first_breaking_pattern = problem_1(patterns)
        print(np.sum(first_breaking_pattern))
    with solution_timing("Problem 2"):
        print(problem_2(patterns, first_breaking_pattern))
