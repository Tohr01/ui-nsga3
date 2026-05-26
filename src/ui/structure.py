import uuid
from dataclasses import dataclass, field
from typing import Type

import PIL.Image as Image

from scoring.aesthetic.balance import BalanceScorer
from scoring.aesthetic.equilibrium import EquilibriumScorer
from scoring.aesthetic.symmetry import SymmetryMode, SymmetryScorer
from scoring.axis_align import AxisAlignScorer
from scoring.content import ContentScorer
from scoring.element_order import ElementOrderScorer
from scoring.footer import FooterScorer
from scoring.gestalt_principles.proximity import ProximityScorer
from scoring.header import HeaderScorer
from scoring.max_icon_size import MaxIconSizeScorer
from scoring.min_touch_target_size import MinTouchTargetSizeScorer
from scoring.scorer import Scorer
from scoring.screen_space_utilize import ScreenSpaceUtilizationScorer
from scoring.text.same_text_size import SameTextSizeScorer
from ui.components.aspect_image import AspectImage, AspectImageConfig, ImageType
from ui.components.cover_image import CoverImage
from ui.components.placeholder_container import PlaceholderContainer
from ui.components.singleline_text import SingleLineText, SingleLineTextConfig
from ui.container import Container
from ui.element import UIElement


@dataclass(kw_only=True, frozen=True)
class BlueprintContainer:
    label: str
    blueprint_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    elements: list["BlueprintContainer" | tuple[Type[UIElement], dict]]
    scorers: list[tuple[Scorer, float]]

    flattend_elements: list[tuple[Type[UIElement], dict]] = field(init=False)

    def __post_init__(self):
        """
        Will flatten the elements list by replacing any BlueprintContainer with a PlaceholderContainer and keeping the other elements as they are.
        The flatted_elements array will have the the following format:
        If the element is a BlueprintContainer:
        (PlaceholderContainer, {"label": element.label, "blueprint_id": BlueprintContainer.blueprint_id})
        If the element is a tuple of (UIElement type, args):
        (UIElement type, init args)
        """
        flattend_elements = []
        for element in self.elements:
            if isinstance(element, BlueprintContainer):
                flattend_elements.append(
                    (
                        PlaceholderContainer,
                        {"label": element.label, "blueprint_id": element.blueprint_id},
                    )
                )
            else:
                flattend_elements.append(element)
        # Bypass frozen
        object.__setattr__(self, "flattend_elements", flattend_elements)

    def get_new_container(self, width_px: float, height_px: float) -> Container:
        """
        Returns a new Container instance based on the blueprint with the given dimensions.
        """
        return Container(
            blueprint_id=self.blueprint_id,
            width_px=width_px,
            height_px=height_px,
            label=self.label,
            elements=[
                element_type(**element_args)
                for element_type, element_args in self.flattend_elements
            ],
        )


@dataclass(kw_only=True, frozen=True)
class RootBlueprint(BlueprintContainer):
    width_px: float
    height_px: float
    label: str = "Interface Root"


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
        (SymmetryScorer(SymmetryMode.RADIAL), 0.5),
    ],
)

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


footer = BlueprintContainer(
    label="Footer",
    elements=[
        (
            SingleLineText,
            {
                "text": "Impressum",
                "label": "Imprint Text",
                "config": SingleLineTextConfig(is_touch_target=True),
            },
        ),
        (
            SingleLineText,
            {
                "text": "Datenschutz",
                "label": "Dataprivacy Text",
                "config": SingleLineTextConfig(is_touch_target=True),
            },
        ),
        (
            SingleLineText,
            {
                "text": "AGB",
                "label": "TaC Text",
                "config": SingleLineTextConfig(is_touch_target=True),
            },
        ),
    ],
    scorers=[
        (MinTouchTargetSizeScorer(), 1.0),
        (SymmetryScorer(SymmetryMode.RADIAL), 0.5),
        (BalanceScorer(), 1.0),
        (EquilibriumScorer(), 1.0),
        (SameTextSizeScorer(), 1.0),
        (ProximityScorer([["Imprint Text", "Dataprivacy Text", "TaC Text"]]), 1.0),
        (AxisAlignScorer(), 1.0),
    ],
)

# TODO: Move to seperate location
interface_blueprint = RootBlueprint(
    width_px=1920,
    height_px=1080,
    label="Interface",
    elements=[
        header,
        # BlueprintContainer(label="Content", elements=[], scorers=[]),
        # BlueprintContainer(label="Footer", elements=[], scorers=[]),
        content,
        footer,
    ],
    scorers=[(HeaderScorer(), 1.0), (FooterScorer(), 1.0), (ContentScorer(), 1.0)],
)
