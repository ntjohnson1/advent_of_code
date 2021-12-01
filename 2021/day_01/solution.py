import numpy as np

def part_1():
    """
    Count the number of times the measurement increase from one step to the next
    :return: num_increases
    """
    measurements = np.loadtxt("input.txt")
    num_increases = np.sum(measurements[1:]>measurements[:-1])
    return num_increases

def part_2(window_size=3):
    """
    Count the number of time the sliding window sum increases
    :return: num_increases
    """
    measurements = np.loadtxt("input.txt")
    # Ensure initial copy
    window_sums = np.array(measurements[:-window_size+1])
    for i in range(1, window_size):
        tail_offset = len(window_sums) + i
        window_sums += measurements[i:tail_offset]
    num_increases = np.sum(window_sums[1:] > window_sums[:-1])
    return num_increases

if __name__=="__main__":
    print(f"Part 1 Answer is: {part_1()}")
    print(f"Part 2 Answer is: {part_2()}")