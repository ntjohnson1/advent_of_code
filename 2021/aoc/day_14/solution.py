from utils import solution_timing
import numpy as np
from string import ascii_uppercase as letters

# If we matches two integers where pairwise differences were all unique then
# identifying patterns flattens to a single vector difference and comparison
# maybe future thought
LETTER_MAPPING = dict(zip(letters, range(len(letters))))
NULL_IDX = len(letters) + 1


def parse_file(a_file):

    with open(a_file, 'r') as f:
        initial_string = f.readline().rstrip()
        f.readline()
        rest_of_strings = f.read()

    for a_letter in letters:
        initial_string = initial_string.replace(a_letter, str(LETTER_MAPPING[a_letter])+',')
        rest_of_strings = rest_of_strings.replace(a_letter, str(LETTER_MAPPING[a_letter])+',')

    rest_of_strings = rest_of_strings.replace(' -> ', '')
    rest_of_strings = rest_of_strings.replace(',\n', ',')

    sequence = np.fromstring(initial_string, sep=',', dtype=np.int32)
    instructions = np.fromstring(rest_of_strings, sep=',', dtype=np.int32)
    instructions = instructions.reshape((-1, 3))

    return sequence, instructions


def apply_instructions(a_sequence, instructions):
    max_length = 2*len(a_sequence) - 1
    new_sequence = np.full((max_length, ), fill_value=NULL_IDX)
    new_sequence[::2] = a_sequence
    for sequence_idx in range(len(a_sequence)-1):
        first_char_match = instructions[:, 0] == a_sequence[sequence_idx]
        second_char_match = instructions[:, 1] == a_sequence[sequence_idx+1]
        valid_pattern_match = first_char_match & second_char_match
        if np.any(valid_pattern_match):
            assert np.sum(valid_pattern_match) < 2, "I don't think duplicate insertions are ok"
            new_sequence[sequence_idx*2 + 1] = instructions[valid_pattern_match, 2]
    non_nulls = new_sequence != NULL_IDX
    return new_sequence[non_nulls]


def problem_1(a_sequence, instructions):
    updated_sequence = a_sequence.copy()
    for i in range(10):
        updated_sequence = apply_instructions(updated_sequence, instructions)
    _, counts = np.unique(updated_sequence, return_counts=True)
    return np.max(counts) - np.min(counts)


def update_counts(pairs, instructions):
    observed_instructions = instructions[pairs[instructions[:, 0], instructions[:, 1]] > 0]
    updated_pairs = pairs.copy()

    # Certain pattern replacements yield duplicate updates and that indexing was
    # not working this morning.
    for old_first, old_end, new_middle in observed_instructions:
        updated_pairs[old_first, new_middle] += pairs[old_first, old_end]
        updated_pairs[new_middle, old_end] += pairs[old_first, old_end]
        updated_pairs[old_first, old_end] -= pairs[old_first, old_end]

    return updated_pairs


def problem_2(a_sequence, instructions):
    """
    Tracks the counts in a matrix accessed via [first_char, second_char]
    for all pair counts
    """
    used_chars = np.unique(instructions)
    pair_counts = np.zeros((len(LETTER_MAPPING), len(LETTER_MAPPING)))

    # Initialize counts
    for sequence_idx in range(len(a_sequence) - 1):
        first_char = a_sequence[sequence_idx]
        second_char = a_sequence[sequence_idx+1]
        pair_counts[first_char, second_char] += 1

    for i in range(40):
        pair_counts = update_counts(pair_counts, instructions)

    char_totals = np.sum(pair_counts, axis=1)
    char_totals[a_sequence[-1]] += 1
    return np.max(char_totals) - np.min(char_totals[used_chars])


if __name__ == "__main__":
    input_file = "input.txt"
    sequence, instructions = parse_file(input_file)
    with solution_timing("Problem 1"):
        print(problem_1(sequence, instructions))
    with solution_timing("Problem 2"):
        print(problem_2(sequence, instructions))
