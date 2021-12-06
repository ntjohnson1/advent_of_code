from utils import solution_timing
import numpy as np

DAYS_TO_SPAWN = 6
MATURITY_DAYS = 2
TOT_DAY = 80


def increment_day(fish_list):
    reset_idx = np.where(fish_list == 0)[0]
    fish_list -= 1
    fish_list[reset_idx] = DAYS_TO_SPAWN
    new_fish = np.full(len(reset_idx), DAYS_TO_SPAWN + MATURITY_DAYS, dtype=np.int16)
    fish_list = np.append(fish_list, new_fish)
    return fish_list


def growth_of_fish_parents(parents, num_days):
    full_spawns = num_days//(DAYS_TO_SPAWN+1)
    remaining_days = num_days - (full_spawns*(DAYS_TO_SPAWN+1))
    remainder = np.sum((parents - remaining_days) < 0)
    return (full_spawns)*len(parents) + remainder


def problem_1(initial_fish):
    """
    Kept slow method for sanity checking part 2
    """
    fish = initial_fish
    for _ in range(TOT_DAY):
        fish = increment_day(fish)
    return len(fish)


def problem_2(initial_fish):
    remaining_days = 256-1
    # First Fish
    total_fish = np.uint64(len(initial_fish))
    # First generation growth
    total_fish += growth_of_fish_parents(initial_fish, remaining_days)
    num_new_gen = np.zeros((9,), np.uint32)
    num_new_gen[8] = 1
    while remaining_days > 0:
        remaining_days -= 1
        new_gens_today = num_new_gen[0]

        if new_gens_today == 0:
            num_new_gen = np.roll(num_new_gen, -1)
        else:
            generation_count = growth_of_fish_parents(initial_fish, remaining_days)
            total_fish += new_gens_today * generation_count

            num_new_gen[0] = 0
            num_new_gen = np.roll(num_new_gen, -1)
            num_new_gen[-3] += new_gens_today
            num_new_gen[-1] += new_gens_today

    return total_fish


if __name__ == "__main__":
    fish = np.loadtxt("input.txt", delimiter=',', dtype=np.int16)

    with solution_timing("Problem 1"):
        print(problem_1(fish))
    with solution_timing("Problem 2"):
        print(problem_2(fish))
