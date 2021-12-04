import numpy as np


def string_binary_converter(string):
    return np.fromiter(string.decode("utf-8"), dtype=int)


def vector_binary_converter(vector):
    return vector.dot(2 ** np.arange(vector.size)[::-1])


def problem_1(numbers):
    num_digits = len(numbers)
    sum_digits = np.sum(numbers, axis=0)
    gamma_binary = sum_digits > (num_digits//2)
    epsilon_binary = ~gamma_binary
    gamma = vector_binary_converter(gamma_binary)
    epsilon = vector_binary_converter(epsilon_binary)
    return gamma*epsilon


def problem_2(numbers):
    num_digits = len(numbers)
    oxygen_mask = np.ones((num_digits,), np.bool)
    co2_mask = np.ones((num_digits,), np.bool)
    current_index = 0
    max_index = len(numbers[0])
    while current_index < max_index:
        # These sum checks are wasted computation
        if np.sum(oxygen_mask) > 1:
            oxygen_mask = apply_filter(oxygen_mask, current_index, numbers, oxygen_criteria)

        if np.sum(co2_mask) > 1:
            co2_mask = apply_filter(co2_mask, current_index, numbers, co2_criteria)
        current_index += 1
    oxygen_binary = numbers[oxygen_mask]
    co2_binary = numbers[co2_mask]
    oxygen = vector_binary_converter(oxygen_binary)
    co2 = vector_binary_converter(co2_binary)
    return oxygen*co2


def oxygen_criteria(remaining_numbers, total_numbers):
    return remaining_numbers >= (total_numbers/2)


def co2_criteria(remaining_numbers, total_numbers):
    # This should just be ~oxygen_criteria
    return remaining_numbers < (total_numbers/2)


def apply_filter(mask, index, numbers, criteria):
    sum_digits = np.sum(numbers[mask, index], axis=0)
    # These sum checks are wasted computation
    num_digits = np.sum(mask)
    filter_value = criteria(sum_digits, num_digits)
    additional_mask = numbers[mask, index] == filter_value
    # Each step we only consider true values in the mask
    # the new mask is only for the subset
    mask[mask] = additional_mask
    return mask


if __name__ == "__main__":
    # Binary vectors
    numbers = np.loadtxt("input.txt", converters={0: string_binary_converter})

    print(f"Problem 1: {problem_1(numbers)}")
    print(f"Problem 2: {problem_2(numbers)}")
