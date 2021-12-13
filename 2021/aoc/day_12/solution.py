from utils import solution_timing
import numpy as np


def matrix_dfs(T, big_caves, partial_path, end_idx, small_caves_seen, all_small_caves, observed_duplicate):
    all_paths = []
    T = T.copy()
    small_caves_seen = small_caves_seen.copy()

    # Next step
    next_caves = np.where(T[:, partial_path[-1]])[0]

    # stopping conditions
    at_end = partial_path[-1] == end_idx
    dead_end = (len(next_caves) == 0)

    if at_end:
        return [partial_path]
    elif dead_end:
        return [None]

    # Update downstream transition matrix
    old_row = T[partial_path[-1], :].copy()
    if partial_path[-1] not in big_caves:
        if partial_path[-1] in small_caves_seen:
            if not observed_duplicate:
                # Nothing should transition to observed small cave
                T[list(small_caves_seen), :] = 0
                # Treat every cave moving forward as already observed
                small_caves_seen = all_small_caves
                observed_duplicate = True
            else:
                T[partial_path[-1], :] = 0
            next_caves = np.where(T[:, partial_path[-1]])[0]
        else:
            small_caves_seen.add(partial_path[-1])

    for a_cave in next_caves:
        next_path = partial_path + [a_cave]
        all_paths.extend(matrix_dfs(T, big_caves, next_path, end_idx, small_caves_seen, all_small_caves, observed_duplicate))

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
    big_caves.add(index_mapping['start'])
    small_caves = {index_mapping[a_location] for a_location in unique_locations if a_location.islower()}
    small_caves -= {index_mapping['start'], index_mapping['end']}

    with solution_timing("Problem 1"):
        all_paths = matrix_dfs(T, big_caves, partial_path, index_mapping['end'], small_caves, small_caves, True)
        all_valid_paths = [a_path for a_path in all_paths if a_path is not None]
        print(len(all_valid_paths))

    with solution_timing("Problem 2"):
        all_paths = matrix_dfs(T, big_caves, partial_path, index_mapping['end'], set(), small_caves, False)
        all_valid_paths = [a_path for a_path in all_paths if a_path is not None]
        print(len(all_valid_paths))
