from constants import OUTPUT_DIR


def init_output_dir():
    OUTPUT_DIR.mkdir(exist_ok=True)
    # Clear previous output
    for item in OUTPUT_DIR.iterdir():
        if item.is_dir():
            for subitem in item.iterdir():
                subitem.unlink()
            item.rmdir()
        else:
            item.unlink()
