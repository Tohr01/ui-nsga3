from constants import CANVAS_HEIGHT_NORM, CANVAS_WIDTH_NORM


def horizontal_canvas_norm_to_pct(value: float) -> float:
    """
    Convert a horizontal relative canvas value to a percentage.
    :param value: Horizontal relative canvas value
    :return: Percentage value
    """
    return (value / CANVAS_WIDTH_NORM) * 100


def vertical_canvas_norm_to_pct(value: float) -> float:
    """
    Convert a vertical relative canvas value to a percentage.
    :param value: Vertical relative canvas value
    :return: Percentage value
    """
    return (value / CANVAS_HEIGHT_NORM) * 100
