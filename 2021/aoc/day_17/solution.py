from utils import solution_timing
import numpy as np
from itertools import product

# For v_x-t+1>=0, x position is
# p_t = p_0 + v_xt - 1/2 (t-1)*t

# y position is
# p_t = p_0 + v_yt - 1/2(t-1)*t
# peak height is
# when v_y = t-1

def find_min_t(min_x, max_x):
    """
    This should come from the minimum v_x
    to land in region. This is the maximum t where x
    changes but minimum value for best height
    """
    # The furthest distance traveled for the projectile
    # in x is when v_x=t
    candidate_x_times = np.arange(259)
    candidate_x_positions = 0.5*candidate_x_times**2
    valid_x = (candidate_x_positions >= min_x) & (candidate_x_positions <= max_x)
    print(np.where(valid_x))


def find_final_positions_x(max_x):
    # TODO this is ALMOST the same as final_y, update to reduce duplication
    # similar to y, anything faster than max_x immediately overshoots on first step
    candidate_x_velocities = np.arange(1, max_x+1)
    # Here we treat our velocities as candidate times as well (introduces need for negative)
    final_positions = np.outer(candidate_x_velocities, candidate_x_velocities) - 0.5 * (
            candidate_x_velocities * (candidate_x_velocities - 1))
    # the upper triangle is equal to the diagonal since the velocity is 0
    for i in range(len(final_positions)):
        final_positions[i, i + 1:] = final_positions[i, i]
    return final_positions


def find_final_positions_y_negative(min_y):
    """
    Returns matrix of shape (time_steps, integer_velocities)
    Time steps are relative to when y_Vel becomes negative
    """
    # We know we throw up, so at height_0 our velocity is flipped
    # find which speeds thrown straight down land in the region
    # anything faster than min_t when negative will be past the region
    candidate_y_velocities = np.arange(-1, min_y-1, -1)
    # Here we treat our velocities as candidate times as well (introduces need for negative)
    final_positions = -np.outer(candidate_y_velocities, candidate_y_velocities) - 0.5 * (
                candidate_y_velocities * (candidate_y_velocities + 1))
    return final_positions


def find_max_y(min_y, max_y):
    """
    We expect y to hit it's peak height then fall straight down.
    """
    final_positions = find_final_positions_y_negative(min_y)
    valid_y = (final_positions >= min_y) & (final_positions <= max_y)
    max_valid = np.max(np.where(valid_y)[0])
    init_vel = max_valid
    max_y = init_vel**2 - 0.5*(init_vel*(init_vel-1))
    return max_y


def problem_1(inputs):
    return find_max_y(*inputs[1])


def problem_2(inputs):
    min_x, max_x = inputs[0]
    min_y, max_y = inputs[1]
    fx = find_final_positions_x(max_x)
    fy = find_final_positions_y_negative(min_y)
    valid_x = (fx <= max_x) & (fx >= min_x)
    valid_y = (fy <= max_y) & (fy >= min_y)
    total_valid = 0
    valid_pairs = []
    for i in range(min(len(fx), len(fy))):
        # For negative initial y
        total_valid += np.sum(valid_x[:, i]) * np.sum(valid_y[:, i])
        if np.any(valid_x[:, i]) and np.any(valid_y[:, i]):
            x_velocities = np.where(valid_x[:, i])[0]+1
            y_velocities = -(np.where(valid_y[:, i])[0]+1)
            valid_pairs.extend(list(product(x_velocities, y_velocities)))

    return (len(set(valid_pairs)))

if __name__=="__main__":
    # Input is short don't bother parsing
    #real_input = [(235, 259), (-118, -62)]
    real_input = [(20, 30), (-10, -5)]

    print(problem_1(real_input))
    print(problem_2(real_input))
