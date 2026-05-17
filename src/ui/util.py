import base64
from io import BytesIO
from pathlib import Path
from typing import Union

import PIL.Image as Image


def img_path_to_base64_str(img_path: Union[str, Path]) -> str:
    with Image.open(img_path) as img:
        buffered = BytesIO()
        # TODO: Maybe change to JPEG
        img.save(buffered, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"
