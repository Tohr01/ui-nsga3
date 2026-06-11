import PIL.Image as Image

from scoring.aesthetic.symmetry import SymmetryMode, SymmetryScorer
from scoring.axis_align import AxisAlignScorer
from scoring.element_order import ElementOrderScorer
from scoring.gestalt_principles.proximity import ProximityScorer
from scoring.max_icon_size import MaxIconSizeScorer
from scoring.min_touch_target_size import MinTouchTargetSizeScorer
from scoring.text.same_text_size import SameTextSizeScorer
from ui.blueprint import BlueprintContainer
from ui.components.aspect_image import AspectImage, AspectImageConfig, ImageType
from ui.components.singleline_text import SingleLineText, SingleLineTextConfig

#
# Header
#
logo_img = Image.open("assets/logo.png")
logo_img_aspect_ratio = logo_img.width / logo_img.height
shopping_cart_img = Image.open("assets/shopping-cart.png")
shopping_cart_img_aspect_ratio = shopping_cart_img.width / shopping_cart_img.height
search_img = Image.open("assets/search.png")
search_img_aspect_ratio = search_img.width / search_img.height
user_img = Image.open("assets/user.png")
user_img_aspect_ratio = user_img.width / user_img.height
header = BlueprintContainer(
    label="Header",
    elements=[
        (
            AspectImage,
            {
                "img_path": "assets/logo.png",
                "label": "Logo",
                "aspect_ratio": logo_img_aspect_ratio,
                "config": AspectImageConfig(is_touch_target=True),
            },
        ),
        (
            SingleLineText,
            {
                "text": "Kategorien",
                "label": "Categories Text",
                "config": SingleLineTextConfig(is_touch_target=True),
            },
        ),
        (
            SingleLineText,
            {
                "text": "Angebote",
                "label": "Offers Text",
                "config": SingleLineTextConfig(is_touch_target=True),
            },
        ),
        (
            AspectImage,
            {
                "img_path": "assets/search.png",
                "label": "Search Icon",
                "aspect_ratio": search_img_aspect_ratio,
                "config": AspectImageConfig(
                    is_touch_target=True, image_type=ImageType.ICON
                ),
            },
        ),
        (
            AspectImage,
            {
                "img_path": "assets/shopping-cart.png",
                "label": "Shopping Cart Icon",
                "aspect_ratio": shopping_cart_img_aspect_ratio,
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
            1.5,
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
        (SameTextSizeScorer(), 1.0),
        (AxisAlignScorer(), 2.0),
        (SymmetryScorer(SymmetryMode.RADIAL), 1.5),
    ],
)
