from pathlib import Path

BASE_LOGGER_NAME = "ui-nsga3"

# Reference direction settings
# Max number of objectives for which to use Das-Dennis reference directions (instead of energy-based reference directions)
MAX_OBJECTIVES_DAS_DENNIS = 4

# Text settings
MIN_FONT_SIZE_PX = 2
DEFAULT_FONT_FAMILY = "Arial"

# Directory paths
OUTPUT_DIR = Path("output")
HTML_OUTPUT_DIR = OUTPUT_DIR / "html"
OPTIMIZATION_RESULTS_DIR = OUTPUT_DIR / "optimization_results"
