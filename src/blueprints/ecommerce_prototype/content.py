from scoring.aesthetic.balance import BalanceScorer
from scoring.aesthetic.equilibrium import EquilibriumScorer
from scoring.aesthetic.symmetry import SymmetryScorer
from scoring.axis_align import Axis, AxisAlignScorer
from scoring.element_order import ElementOrderScorer, OrderDirection
from scoring.gestalt_principles.proximity import ProximityScorer
from scoring.min_touch_target_size import MinTouchTargetSizeScorer
from scoring.screen_space_utilize import ScreenSpaceUtilizationScorer
from scoring.text.golden_ratio_text_size import GoldenRatioTextSizeScorer
from scoring.text.min_font_size import MinFontSizeScorer
from ui.blueprint import BlueprintContainer
from ui.components.aspect_image import AspectImage
from ui.components.cover_image import CoverImage
from ui.components.padding_button import PaddingButton, PaddingButtonConfig
from ui.components.singleline_text import SingleLineText, SingleLineTextConfig
from ui.enums import TextType
from ui.util import img_path_to_aspect_ratio, multiline_text_to_html

#
# Product details
#

start_img_path = "assets/stars.png"

product_description_text = multiline_text_to_html("""Über die Schuhe:
• Gefederte Sohle für optimalen Komfort und Dämpfung bei jedem Schritt
• Atmungsaktives Obermaterial aus hochwertigem Mesh für maximale Belüftung
• Robuste Laufsohne aus rutschfestem Gummiverbundsstoff
• Sportliches Blabla bla
• Lorem ipsum dolor sit amet, consectetur adipiscing elit.""")

product_details = BlueprintContainer(
    label="Product Details",
    elements=[
        (
            SingleLineText,
            {
                "label": "Headline",
                "text": "AirSportX - Limited Edition",
                "config": SingleLineTextConfig(text_type=TextType.HEADER),
            },
        ),
        (
            AspectImage,
            {
                "label": "Stars",
                "img_path": start_img_path,
                "aspect_ratio": img_path_to_aspect_ratio(start_img_path),
            },
        ),
        (
            SingleLineText,
            {
                "label": "Product Description",
                "text": product_description_text,
                "config": SingleLineTextConfig(text_type=TextType.PARAGRAPH),
            },
        ),
        (
            SingleLineText,
            {
                "label": "Price",
                "text": "129,99€",
                "config": SingleLineTextConfig(text_type=TextType.SUBHEADER),
            },
        ),
        (
            PaddingButton,
            {
                "label": "Buy Button",
                "text": "In den Warenkorb",
                "background_color_hex": "#2ecc71",
                "text_color_hex": "#000000",
                "config": PaddingButtonConfig(
                    is_touch_target=True, text_type=TextType.PARAGRAPH
                ),
            },
        ),
    ],
    scorers=[
        (
            ElementOrderScorer(
                ["Headline", "Stars", "Price", "Buy Button", "Product Description"],
                OrderDirection.Y,
            ),
            1.0,
        ),
        (
            ProximityScorer(
                [["Headline", "Stars", "Price"], ["Buy Button", "Product Description"]]
            ),
            1.0,
        ),
        (GoldenRatioTextSizeScorer(), 1.0),
        (AxisAlignScorer(Axis.X), 1.0),
        (MinTouchTargetSizeScorer(), 1.0),
        (MinFontSizeScorer(), 1.0),
        (EquilibriumScorer(), 1.0),
    ],
)

#
# Content
#
content = BlueprintContainer(
    label="Content",
    elements=[
        (
            CoverImage,
            {
                "img_path": "assets/sneaker.jpg",
                "label": "Product_Image",
            },
        ),
        product_details,
    ],
    scorers=[
        (SymmetryScorer(), 1.0),
        (BalanceScorer(), 1.0),
        (ScreenSpaceUtilizationScorer(), 2.0),
        (
            ElementOrderScorer(
                element_order_labels=["Product_Image", "Product_Details"]
            ),
            1.0,
        ),
    ],
)
