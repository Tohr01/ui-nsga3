from numpy import random


def normal_distribution_mutate(
    *,
    value: float,
    mutation_rate: float,
    i_max: float,
    i_min: float = 0,
    mutation_range_factor: float = 6,
) -> float:
    """
    Will mutate a value using a normal distribution by calculating:
    sigma = (i_max - i_min) / mutation_range_factor
    new_value = value + N(0, sigma) with probability mutation_rate
    Note: New Value may be outside of [i_min, i_max]
    :param value: Value to mutate
    :param mutation_rate: Mutation rate
    :param i_max: Interval maximum value
    :param i_min: Interval minimum value
    :param mutation_range_factor: Factor to determine mutation range
    :return: Mutated value
    """
    if random.random() > mutation_rate:
        return value

    sigma = (i_max - i_min) / mutation_range_factor
    return value + random.normal(0, sigma)
