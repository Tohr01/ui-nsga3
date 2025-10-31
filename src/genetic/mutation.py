from numpy import random


def normal_distribution_mutate(
    *,
    value: float,
    mutation_rate: float,
    i_min: float = 0,
    i_max: float = 1,
    mutation_range_factor: float = 8,
) -> float:
    """
    Will mutate a value using a normal distribution by calculating:
    sigma = (i_max - i_min) / mutation_range_factor
    new_value = value + N(0, sigma) with probability mutation_rate
    :param value: Value to mutate
    :param mutation_rate: Mutation rate
    :param i_min: Interval minimum value
    :param i_max: Interval maximum value
    :param mutation_range_factor: Factor to determine mutation range
    :return: Mutated value
    """
    if random.random() > mutation_rate:
        return value

    sigma = (i_max - i_min) / mutation_range_factor
    return value + random.normal(0, sigma)
