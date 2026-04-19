def styles_dict_to_str(styles_dict: dict) -> str:
    """
    Convert a dictionary of CSS styles to a string that can be used in an HTML style attribute.
    :param styles_dict: A dictionary where keys are CSS property names and values are the corresponding CSS values.
    """
    return "; ".join(f"{key}: {value}" for key, value in styles_dict.items())


def attributes_dict_to_str(attributes_dict: dict) -> str:
    """
    Convert a dictionary of HTML attributes to a string that can be used in an HTML element.
    :param attributes_dict: A dictionary where keys are attribute names and values are the corresponding attribute values.
    """
    return " ".join(f'{key}="{value}"' for key, value in attributes_dict.items())
