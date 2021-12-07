from utils import solution_timing
import numpy as np


def objective_value(locations, alignment, fuel_function):
    """
    Fuel required  to align crabs from current positions
    :param locations Iterable[int]: Where crabs are
    :param alignment int: where they are going
    :param fuel_function callable: how much fuel it costs to move that many units
    :return: How much it costs to get there
    """
    return np.sum(fuel_function(np.abs(locations-alignment)))


def problem_1(locations):
    """
    Find optimal crab position then find fuel to get there
    aka: \min_x \sum_i \abs(h_i-x)
    aka: integer median
    """
    fuel_function = lambda x: x
    return objective_value(locations, np.median(locations), fuel_function)


def problem_2(locations):
    """
    Find optimal crab position then find fuel to get there
    Fuel function is \sum_i i which is f(n) = n(n+1)
    aka: \min_x \sum_i f(\abs(h_i-x))
        \note{for h_i-x, and h_i-x+1 of the same sign we can drop abs to get
        = \min_x \frac{(h_i-x)(h_i-x+1)}{2}
        = \min_x h_i^2 + x_i^2 -2h_ix + h_i -x
    aka: nearly the mean (2-norm) so we fake it and evaluate twice to verify
    """
    fuel_function = lambda x: x*(x+1)/2
    above_alignment = np.floor(np.mean(locations))
    below_alignment = np.ceil(np.mean(locations))
    above_value = objective_value(locations, above_alignment, fuel_function)
    below_value = objective_value(locations, below_alignment, fuel_function)
    return min(above_value, below_value)


if __name__ == "__main__":
    crab_locations = np.loadtxt("input.txt", delimiter=',', dtype=np.int16)

    with solution_timing("Problem 1"):
        print(problem_1(crab_locations))

    with solution_timing("Problem 2"):
        print(problem_2(crab_locations))
