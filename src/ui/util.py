import base64
from io import BytesIO
from pathlib import Path
from typing import Union

import PIL.Image as Image


def img_path_to_base64_str(img_path: Union[str, Path]) -> str:
    """
    Open image using Pillow, save as webp, return b64 string
    :param img_path: Path to the image file
    :return: Base64 string of the image
    """
    with Image.open(img_path) as img:
        buffered = BytesIO()
        img.save(buffered, format="webp")
        return (
            f"data:image/webp;base64,{base64.b64encode(buffered.getvalue()).decode()}"
        )


def img_path_to_aspect_ratio(img_path: Union[str, Path]) -> float:
    """
    Open image using Pillow and return aspect ratio (width / height)
    :param img_path: Path to the image file
    :return: Aspect ratio of the image
    """
    with Image.open(img_path) as img:
        return img.width / img.height


def multiline_text_to_html(text: str) -> str:
    """
    Convert multiline text to HTML by replacing \\n with <br>
    :param text: Multiline text with \\n as line breaks
    :return: HTML string with <br> as line breaks
    """
    return text.replace("\n", "<br>")
