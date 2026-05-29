import PIL.Image as Image

from scoring.aesthetic.balance import BalanceScorer
from scoring.aesthetic.symmetry import SymmetryScorer
from scoring.element_order import ElementOrderScorer
from scoring.screen_space_utilize import ScreenSpaceUtilizationScorer
from ui.blueprint import BlueprintContainer
from ui.components.cover_image import CoverImage

#
# Content
#
product_photo = Image.open("assets/sneaker.jpg")
product_photo_ar = product_photo.width / product_photo.height
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
        BlueprintContainer(label="Product_Details", elements=[], scorers=[]),
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
