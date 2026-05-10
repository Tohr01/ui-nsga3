from pathlib import Path

BASE_LOGGER_NAME = "ui-nsga3"

# Reference direction settings
# Max number of objectives for which to use Das-Dennis reference directions (instead of energy-based reference directions)
MAX_OBJECTIVES_DAS_DENNIS = 4

# Text settings
MIN_FONT_SIZE_PX = 2
DEFAULT_FONT_FAMILY = "Arial"

# Rendering settings
OUTPUT_DIR = Path("output")
