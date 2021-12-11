from utils import solution_timing
import numpy as np


def lazy_converter(a_column):
    return np.fromiter(a_column.decode("utf-8"), dtype=np.int16)


def infect_neighbors(previous_flashers, levels):
    """
    If you previously infected neighbors you are no longer infectious.
    If you are newly infectious add 1 to you neighbors in all directions.
    """
    new_flashers = (levels>9) & (~previous_flashers)

    offset = 1
    increment_slice = slice(offset, None)
    stationary_slice = slice(0, -offset)
    full_slice = slice(0, None)

    # For a second day too lazy to get the permutation setup for this
    # Down, up, left, right
    levels[increment_slice, full_slice][new_flashers[stationary_slice, full_slice]] += 1
    levels[stationary_slice, full_slice][new_flashers[increment_slice, full_slice]] += 1
    levels[full_slice, increment_slice][new_flashers[full_slice, stationary_slice]] += 1
    levels[full_slice, stationary_slice][new_flashers[full_slice, increment_slice]] += 1
    # Diagonals
    levels[increment_slice, increment_slice][new_flashers[stationary_slice, stationary_slice]] += 1
    levels[stationary_slice, stationary_slice][new_flashers[increment_slice, increment_slice]] += 1
    levels[increment_slice, stationary_slice][new_flashers[stationary_slice, increment_slice]] += 1
    levels[stationary_slice, increment_slice][new_flashers[increment_slice, stationary_slice]] += 1


    return new_flashers, levels


def perform_round(levels):
    """
    General infection model propagation.
    Iterate one round at a time
    """
    levels += 1
    all_flashers = np.zeros(levels.shape, dtype=np.bool)
    new_flashers, levels = infect_neighbors(all_flashers, levels)
    all_flashers = all_flashers | new_flashers
    while np.any(new_flashers):
        new_flashers, levels = infect_neighbors(all_flashers, levels)
        all_flashers = all_flashers | new_flashers

    levels[all_flashers] = 0

    return np.sum(all_flashers), levels


def problem_1(levels):
    total_flash = 0
    num_rounds = 100
    for _ in range(num_rounds):
        num_flashes, levels = perform_round(levels)
        total_flash += num_flashes
    return total_flash


def problem_2(levels):
    num_rounds = 0
    num_flashes = 0
    while np.sum(num_flashes) < levels.size:
        num_flashes, levels = perform_round(levels)
        num_rounds += 1
    return num_rounds


if __name__ == "__main__":
    input_file = "input.txt"
    octopus_levels = np.loadtxt(input_file, converters={0:lazy_converter}, dtype=np.int16)
    with solution_timing("Problem 1"):
        print(problem_1(octopus_levels))
    with solution_timing("Problem 2"):
        # Uses updates from problem 1
        # alternatively could copy inputs to be independent
        print(100 + problem_2(octopus_levels))