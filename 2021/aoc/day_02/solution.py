from utils import solution_timing
import numpy as np


def direction_converter(direction):
    direction = direction.decode("utf-8")
    if direction == "forward":
        index = 0
    elif direction == "down":
        index = 1
    elif direction == "up":
        index = -1
    else:
        raise ValueError("Something is wrong in parsing")
    return index


def final_postion(movements):
    """
    Nice clean inner product and sum
    """
    horizontal_mask = movements[:, 0] == 0
    vertical_mask = ~horizontal_mask
    horizontal_position = np.sum(movements[horizontal_mask, 1])
    vertical_position = movements[vertical_mask, 0].dot(movements[vertical_mask, 1])
    return horizontal_position, vertical_position


def problem_1(movements):
    return np.prod(final_postion(movements))


def final_postion_2(movements):
    """
    Couldn't figure out the clever indexing to make this work.
    Could expand the scaling to a sparse matrix multiple, but that wasn't
    pretty.
    """
    horizontal_mask = movements[:, 0] == 0
    horizontal_index = np.where(horizontal_mask)[0]
    horizontal_position = np.sum(movements[horizontal_mask, 1])

    vertical_position = 0
    aim_value = 0
    for i in range(len(horizontal_index)-1):
        # Range of aim changes [start, end)
        start = horizontal_index[i] + 1
        end = horizontal_index[i+1]
        if start != end:
            aim_value += movements[range(start, end), 0].dot(movements[range(start, end), 1])
        vertical_position += aim_value * movements[end, 1]

    return horizontal_position, vertical_position


def final_postion_3(movements):
    """
    Got this working with Victor's help
    """
    horizontal_mask = movements[:, 0] == 0
    vertical_mask = ~horizontal_mask
    # Could parse the data this way to start but leaving for backwards compatibility
    # DeltaX,DeltaAim
    deltas = np.zeros(movements.shape)
    deltas[horizontal_mask, 0] = movements[horizontal_mask, 1]
    deltas[vertical_mask, 1] = movements[vertical_mask, 0] * movements[vertical_mask, 1]

    vertical_position = deltas[:,0].dot(np.cumsum(deltas[:,1]))
    horizontal_position = np.sum(deltas[:,0])

    return horizontal_position, vertical_position


def problem_2(movements):
    return np.prod(final_postion_3(movements))


if __name__ == "__main__":
    # direction, magnitude
    # direction: {0: forward, 1: down, -1: up}
    movements = np.loadtxt("input.txt", converters={0:direction_converter}, delimiter=" ")
    with solution_timing("Problem 1"):
        print(problem_1(movements))
    with solution_timing("Problem 2"):
        print(problem_2(movements))
