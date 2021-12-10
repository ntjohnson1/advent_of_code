from utils import solution_timing
import numpy as np
import io
from itertools import repeat

NUM_SEGMENTS = 7
NUM_DIGITS = 14


def lazy_converter(a_column):
    print(a_column)
    return np.fromiter(a_column.decode("utf-8"), dtype=np.int16)


def segment_to_digit(a_vector):
    one = tuple([1, 1, 1, 0, 1, 1, 1])
    two = tuple([0, 0, 1, 0, 0, 1, 0])
    three = tuple([1, 0, 1, 1, 1, 0, 1])
    four = tuple([0, 1, 1, 1, 0, 1, 0])
    five = tuple([1, 1, 0, 1, 0, 1, 1])
    six = tuple([1, 1, 0, 1, 1, 1, 1])
    seven = tuple([1, 0, 1, 0, 0, 1, 0])
    eight = tuple([1, 1, 1, 1, 1, 1, 1])
    nine = tuple([1, 1, 1, 1, 0, 1, 1])
    mapping = {
        one: '1',
        two: '2',
        three: '3',
        four: '4',
        five: '5',
        six: '6',
        seven: '7',
        eight: '8',
        nine: '9',
    }
    return mapping[a_vector]


def problem_1(segments):
    outputs_segments = segments[:, 11:]

    return np.sum(outputs_segments < 9999) + np.sum(outputs_segments > 999999)


def problem_2(file_bytes):
    file_bytes = file_bytes.splitlines()
    num_observations = len(file_bytes)
    segment_tensor = np.zeros((NUM_SEGMENTS, NUM_DIGITS, num_observations))
    for i, observation_set in enumerate(file_bytes):
        the_digits = observation_set.split()
        for j, a_digit in enumerate(the_digits):
            segment_idx = np.fromiter(a_digit.decode('utf-8'), dtype=np.uint16) - 1
            segment_tensor[segment_idx, j, i] = 1
    segment_counts = np.sum(segment_tensor[:, :10, :], axis=1)
    four_segments = np.sum(segment_tensor[:, :10, :], axis=0) == 4
    np.repeat()
    four_counts = segment_tensor[:, :10, :]

    a_idx = np.where((segment_counts == 8)) #& (segment_counts - four_counts == 8))
    b_idx = np.where(segment_counts == 6)
    #c_idx = np.where((segment_counts == 8) #& (segment_counts - four_counts == 7))
    d_idx = np.where((segment_counts == 7) )#& (segment_counts - four_counts == 6))
    e_idx = np.where(segment_counts == 4)
    f_idx = np.where(segment_counts == 9)
    #g_idx = np.where((segment_counts == 7) & (segment_counts - four_counts == 7))

    print(segment_counts)
    #print(segment_counts-four_counts)
    #for an_idx in [a_idx, b_idx, c_idx, d_idx, e_idx, f_idx, g_idx]:
    for an_idx in [a_idx, b_idx, d_idx, e_idx, f_idx,]:
        print((an_idx[0].shape))
    #segment_permutation = np.hstack([a_idx, b_idx, c_idx, d_idx, e_idx, f_idx, g_idx])
    #print(segment_permutation.shape)
    #segment_tensor =
    #for _ in range(num_observations):
    #    segment_tensor[:,10:,:]


if __name__ == "__main__":
    input_file = 'small.txt'
    with open(input_file, 'rb') as f:
        unparsed_bytes = f.read().replace(b'|', b'')
    unparsed_bytes = unparsed_bytes.replace(b'a', b'1')
    unparsed_bytes = unparsed_bytes.replace(b'b', b'2')
    unparsed_bytes = unparsed_bytes.replace(b'c', b'3')
    unparsed_bytes = unparsed_bytes.replace(b'd', b'4')
    unparsed_bytes = unparsed_bytes.replace(b'e', b'5')
    unparsed_bytes = unparsed_bytes.replace(b'f', b'6')
    unparsed_bytes = unparsed_bytes.replace(b'g', b'7')
    # (x1,y1,x2,y2)
    segments = np.genfromtxt(io.BytesIO(unparsed_bytes), delimiter=" ", dtype=np.uint32)
    with solution_timing("Problem 1"):
        print(problem_1(segments))
    with solution_timing("Problem 2"):
        print(problem_2(unparsed_bytes))