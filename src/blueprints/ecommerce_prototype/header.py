from scoring.aesthetic.symmetry import SymmetryMode, SymmetryScorer
from scoring.axis_align import AxisAlignScorer
from scoring.element_order import ElementOrderScorer
from scoring.gestalt_principles.proximity import ProximityScorer
from scoring.max_icon_size import MaxIconSizeScorer
from scoring.min_touch_target_size import MinTouchTargetSizeScorer
from scoring.text.golden_ratio_text_size import GoldenRatioTextSizeScorer
from scoring.text.min_font_size import MinFontSizeScorer
from ui.blueprint import BlueprintContainer
from ui.components.aspect_image import AspectImage, AspectImageConfig
from ui.components.text import Text, TextConfig
from ui.enums import ImageType
from ui.util import img_path_to_aspect_ratio

#
# Header
#
logo_img_path = "assets/logo.png"
shopping_cart_img_path = "assets/shopping-cart.png"
search_img_path = "assets/search.png"
header = BlueprintContainer(
    label="Header",
    elements=[
        (
            AspectImage,
            {
                "img_path": logo_img_path,
                "label": "Logo",
                "aspect_ratio": img_path_to_aspect_ratio(logo_img_path),
                "config": AspectImageConfig(is_touch_target=True),
            },
        ),
        (
            Text,
            {
                "text": "Kategorien",
                "label": "Categories Text",
                "config": TextConfig(is_touch_target=True),
            },
        ),
        (
            Text,
            {
                "text": "Angebote",
                "label": "Offers Text",
                "config": TextConfig(is_touch_target=True),
            },
        ),
        (
            AspectImage,
            {
                "img_path": search_img_path,
                "label": "Search Icon",
                "aspect_ratio": img_path_to_aspect_ratio(search_img_path),
                "config": AspectImageConfig(
                    is_touch_target=True, image_type=ImageType.ICON
                ),
            },
        ),
        (
            AspectImage,
            {
                "img_path": shopping_cart_img_path,
                "label": "Shopping Cart Icon",
                "aspect_ratio": img_path_to_aspect_ratio(shopping_cart_img_path),
                "config": AspectImageConfig(
                    is_touch_target=True, image_type=ImageType.ICON
                ),
            },
        ),
    ],
    scorers=[
        (
            ProximityScorer(
                [
                    ["Categories Text", "Offers Text"],
                    ["Search Icon", "Shopping Cart Icon"],
                ]
            ),
            1.0,
        ),
        (
            ElementOrderScorer(
                [
                    "Logo",
                    "Categories Text",
                    "Offers Text",
                    "Search Icon",
                    "Shopping Cart Icon",
                ]
            ),
            1.0,
        ),
        (MinTouchTargetSizeScorer(), 1.0),
        (MaxIconSizeScorer(), 1.0),
        (GoldenRatioTextSizeScorer(), 1.0),
        (AxisAlignScorer(), 1.0),
        (SymmetryScorer(SymmetryMode.RADIAL), 1.0),
        (MinFontSizeScorer(), 1.0),
    ],
)
