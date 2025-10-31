import numpy as np


def intermediate_recombination(
    v1: float, v2: float, beta_interval_extention: float = 0.25
) -> float:
    """
    Perform intermediate recombination between two values.
    Will sample a beta value from the uniform distribution in the interval
    [-beta_interval_extention, 1 + beta_interval_extention] and compute the new value as:
    v1 * beta + v2 * (1 - beta)
    :param v1: First value
    :param v2: Second value
    :param beta_interval_extention: Extension factor for the recombination interval
    :return: New value after recombination
    """
    beta = np.random.uniform(-beta_interval_extention, 1 + beta_interval_extention)
    return v1 * beta + v2 * (1 - beta)
