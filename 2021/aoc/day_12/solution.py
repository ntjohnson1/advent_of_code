from utils import solution_timing
import numpy as np


def matrix_dfs(T, big_caves, partial_path, end_idx):
    all_paths = []

    # Next step
    next_caves = np.where(T[:, partial_path[-1]])[0]

    # stopping conditions
    at_end = partial_path[-1] == end_idx
    dead_end = len(next_caves) == 0

    if at_end:
        return [partial_path]
    elif dead_end:
        return [None]

    # Update downstream transition matrix
    old_row = T[partial_path[-1], :].copy()
    if partial_path[-1] not in big_caves:
        T[partial_path[-1], :] = 0

    for a_cave in next_caves:
        next_path = partial_path + [a_cave]
        all_paths.extend(matrix_dfs(T, big_caves, next_path, end_idx))

    # Reset Transition matrix for consistency
    T[partial_path[-1], :] = old_row

    return all_paths


if __name__ == "__main__":
    input_file = "input.txt"
    starting_locations = []
    ending_locations = []
    with open(input_file, 'r') as f:
        for line in f:
            a_start, an_end = line.rstrip().split('-')
            starting_locations.append(a_start)
            ending_locations.append(an_end)

    unique_locations = set(starting_locations+ending_locations)
    num_unique = len(unique_locations)
    index_mapping = dict(zip(unique_locations, range(num_unique)))

    T = np.zeros((num_unique, num_unique))
    for a_start, an_end in zip(starting_locations, ending_locations):
        start_idx = index_mapping[a_start]
        ending_idx = index_mapping[an_end]
        T[ending_idx, start_idx] = 1
        T[start_idx, ending_idx] = 1
    T[:, index_mapping['end']] = 0
    T[index_mapping['start'], :] = 0
    partial_path = [index_mapping['start']]
    big_caves = {index_mapping[a_location] for a_location in unique_locations if a_location.isupper()}


    all_paths = matrix_dfs(T, big_caves, partial_path, index_mapping['end'])
    all_valid_paths = [a_path for a_path in all_paths if a_path is not None]
    print(len(all_valid_paths))
