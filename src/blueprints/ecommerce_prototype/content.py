from scoring.aesthetic.balance import BalanceScorer
from scoring.aesthetic.equilibrium import EquilibriumScorer
from scoring.aesthetic.symmetry import SymmetryScorer
from scoring.axis_align import AxisAlignScorer
from scoring.element_order import ElementOrderScorer
from scoring.enums import Axis
from scoring.gestalt_principles.proximity import ProximityScorer
from scoring.min_touch_target_size import MinTouchTargetSizeScorer
from scoring.screen_space_utilize import ScreenSpaceUtilizationScorer
from scoring.text.golden_ratio_text_size import GoldenRatioTextSizeScorer
from scoring.text.min_font_size import MinFontSizeScorer
from ui.blueprint import BlueprintContainer
from ui.components.aspect_image import AspectImage
from ui.components.cover_image import CoverImage
from ui.components.padding_button import PaddingButton, PaddingButtonConfig
from ui.components.text import Text, TextConfig
from ui.enums import TextType
from ui.util import img_path_to_aspect_ratio, multiline_text_to_html

#
# Product details
#

stars_img_path = "assets/stars.png"

product_description_text = multiline_text_to_html("""Produktdetails:
• Optimaler Komfort durch die verbesserte AirSportPLUS Dämpfung
• Atmungsaktives Obermaterial aus hochwertigem Mesh
• Hoher Grip der Laufsohle auf verschiedenen Terrains
• Dynamisches Abrollen dank Xtrack Außensohle, ideal auf langen Distanzen
• Farben: Cloud White Green / Carbon Orange""")

product_details = BlueprintContainer(
    label="Product_Details",
    elements=[
        (
            Text,
            {
                "label": "Headline",
                "text": "AirSportX - Limited Edition",
                "config": TextConfig(text_type=TextType.HEADER),
            },
        ),
        (
            AspectImage,
            {
                "label": "Stars",
                "img_path": stars_img_path,
                "aspect_ratio": img_path_to_aspect_ratio(stars_img_path),
            },
        ),
        (
            Text,
            {
                "label": "Product Description",
                "text": product_description_text,
                "config": TextConfig(text_type=TextType.PARAGRAPH),
            },
        ),
        (
            Text,
            {
                "label": "Price",
                "text": "129,99€",
                "config": TextConfig(text_type=TextType.SUBHEADER),
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
                Axis.Y,
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
        # BlueprintContainer(label="Product_Details", elements=[], scorers=[]),
        product_details,
    ],
    scorers=[
        (SymmetryScorer(), 1.0),
        (BalanceScorer(), 1.0),
        (ScreenSpaceUtilizationScorer(), 1.0),
        (
            ElementOrderScorer(
                element_order_labels=["Product_Image", "Product_Details"]
            ),
            1.0,
        ),
    ],
)
