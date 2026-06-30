from scoring.aesthetic.balance import BalanceScorer
from scoring.aesthetic.equilibrium import EquilibriumScorer
from scoring.aesthetic.symmetry import SymmetryMode, SymmetryScorer
from scoring.axis_align import AxisAlignScorer
from scoring.gestalt_principles.proximity import ProximityScorer
from scoring.min_touch_target_size import MinTouchTargetSizeScorer
from scoring.text.golden_ratio_text_size import GoldenRatioTextSizeScorer
from scoring.text.min_font_size import MinFontSizeScorer
from ui.blueprint import BlueprintContainer
from ui.components.text import Text, TextConfig
from ui.enums import TextType

footer = BlueprintContainer(
    label="Footer",
    elements=[
        (
            Text,
            {
                "text": "Impressum",
                "label": "Imprint Text",
                "config": TextConfig(is_touch_target=True, text_type=TextType.FOOTNOTE),
            },
        ),
        (
            Text,
            {
                "text": "Datenschutz",
                "label": "Dataprivacy Text",
                "config": TextConfig(is_touch_target=True, text_type=TextType.FOOTNOTE),
            },
        ),
        (
            Text,
            {
                "text": "AGB",
                "label": "TaC Text",
                "config": TextConfig(is_touch_target=True, text_type=TextType.FOOTNOTE),
            },
        ),
    ],
    scorers=[
        (MinTouchTargetSizeScorer(), 1.0),
        (SymmetryScorer(SymmetryMode.RADIAL), 1.0),
        (BalanceScorer(), 1.0),
        (EquilibriumScorer(), 1.0),
        (GoldenRatioTextSizeScorer(), 1.0),
        (ProximityScorer([["Imprint Text", "Dataprivacy Text", "TaC Text"]]), 1.0),
        (AxisAlignScorer(), 1.0),
        (MinFontSizeScorer(), 1.0),
    ],
)
