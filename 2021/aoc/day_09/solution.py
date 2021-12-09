from utils import solution_timing
import numpy as np


def lazy_converter(a_line):
    return np.fromiter(a_line.decode("utf-8"), dtype=np.int16)


def get_low_points(floor_heights):
    is_low_point = np.ones(floor_heights.shape, dtype=np.bool)

    is_low_point[:-1, :] &= floor_heights[:-1, :] < floor_heights[1:,:]
    is_low_point[1:, :] &= floor_heights[1:, :] < floor_heights[:-1, :]
    is_low_point[:, :-1] &= floor_heights[:, :-1] < floor_heights[:, 1:]
    is_low_point[:, 1:] &= floor_heights[:, 1:] < floor_heights[:, :-1]
    return is_low_point


def problem_1(floor_heights):
    low_points = get_low_points(floor_heights)
    return np.sum(floor_heights[low_points]) + len(floor_heights[low_points])


def update_direction(floor_map, direction):
    """
    If there is an unassigned square in the direction assign it to its neighbors value
    """
    offset = 1
    full_slice = slice(0, None)
    increment_slice = slice(offset, None)
    stationary_slice = slice(0, -offset)

    # 3.6 has no match, so use if else to determine slices based on direction
    if direction == "right":
        slice_shift = (full_slice, increment_slice)
        slice_current = (full_slice, stationary_slice)
    elif direction == "left":
        slice_shift = (full_slice, stationary_slice)
        slice_current = (full_slice, increment_slice)
    elif direction == "up":
        slice_shift = (stationary_slice, full_slice)
        slice_current = (increment_slice, full_slice)
    elif direction == "down":
        slice_shift = (increment_slice, full_slice)
        slice_current = (stationary_slice, full_slice)
    else:
        raise ValueError(f"Bad direction: {direction}")

    direction_is_unassigned = floor_map[slice_shift] == -1
    neighbor_is_assigned = floor_map[slice_current] >= 0
    update_idx = direction_is_unassigned & neighbor_is_assigned

    floor_map[slice_shift][update_idx] = floor_map[slice_current][update_idx]
    return floor_map


def problem_2(floor_heights):
    low_points = get_low_points(floor_heights)
    # -1 means unassigned basin
    # -2 means boundary
    # positive integer is the basin assigned
    basin_map = np.full(floor_heights.shape, -1, dtype=np.int16)
    basin_map[floor_heights == 9] = -2
    basin_map[low_points] = np.arange(np.sum(low_points))

    # Propagate basin indices throughout the whole map
    remaining_changes = True
    while remaining_changes:
        basin_map = update_direction(basin_map, "up")
        basin_map = update_direction(basin_map, "down")
        basin_map = update_direction(basin_map, "left")
        if -1 not in basin_map:  # Every point assigned but boundaries
            remaining_changes = False

    valid_basins = basin_map[basin_map != -2]
    values, counts = np.unique(valid_basins, return_counts=True)
    return np.prod(np.sort(counts)[-3:])


if __name__ == "__main__":
    input_file = "input.txt"
    floor_heights = np.loadtxt(input_file, converters={0: lazy_converter}, dtype=np.int16)
    with solution_timing("Problem 1"):
        print(problem_1(floor_heights))
    with solution_timing("Problem 2"):  # Takes 10x longer than problem 1
        print(problem_2(floor_heights))
