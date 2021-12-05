from utils import solution_timing
import io
import numpy as np

X1_IDX = 0
Y1_IDX = 1
X2_IDX = 2
Y2_IDX = 3
# Could be more selective, but easier to cast all to same
INTEGER_TYPE = np.int16

def get_vent_map(vent_locations):
    x_max = np.max(vent_locations[:, [X1_IDX, X2_IDX]]) + 1
    y_max = np.max(vent_locations[:, [Y1_IDX, Y2_IDX]]) + 1
    vent_map = np.zeros((x_max, y_max), dtype=INTEGER_TYPE)
    for (x1, y1, x2, y2) in vent_locations:
        x_slice = np.linspace(x1, x2, endpoint=True, num=1+np.abs(x2-x1), dtype=INTEGER_TYPE)
        y_slice = np.linspace(y1, y2, endpoint=True, num=1 + np.abs(y2 - y1), dtype=INTEGER_TYPE)
        vent_map[x_slice, y_slice] += 1
    return vent_map


def problem_1(vent_locations):
    horizontal_mask = vent_locations[:, X1_IDX] == vent_locations[:, X2_IDX]
    vertical_mask = vent_locations[:, Y1_IDX] == vent_locations[:, Y2_IDX]
    non_diagonal_mask = horizontal_mask | vertical_mask
    vent_map = get_vent_map(vent_locations[non_diagonal_mask])
    return np.sum(vent_map >= 2)


def problem_2(vent_locations):
    vent_map = get_vent_map(vent_locations)
    return np.sum(vent_map >= 2)


if __name__ == "__main__":
    input_file = 'input.txt'
    with open(input_file, 'rb') as f:
        unparsed_bytes = io.BytesIO(f.read().replace(b'->', b','))
    # (x1,y1,x2,y2)
    locations = np.genfromtxt(unparsed_bytes, delimiter=",", dtype=INTEGER_TYPE)

    with solution_timing("Problem 1"):
        print(problem_1(locations))
    with solution_timing("Problem 2"):
        print(problem_2(locations))
