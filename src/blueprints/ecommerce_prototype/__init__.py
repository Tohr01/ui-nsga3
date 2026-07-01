from blueprints.ecommerce_prototype.content import content
from blueprints.ecommerce_prototype.footer import footer
from blueprints.ecommerce_prototype.header import header
from scoring.footer import FooterScorer
from scoring.header import HeaderScorer
from scoring.screen_space_utilize import ScreenSpaceUtilizationScorer
from ui.blueprint import BlueprintContainer, RootBlueprint

interface_blueprint = RootBlueprint(
    width_px=1920,
    height_px=1080,
    label="Baselayout",
    elements=[
        # BlueprintContainer(label="Header", elements=[], scorers=[]),
        # BlueprintContainer(label="Content", elements=[], scorers=[]),
        # BlueprintContainer(label="Footer", elements=[], scorers=[]),
        header,
        content,
        footer,
    ],
    scorers=[
        (HeaderScorer(), 1.0),
        (FooterScorer(), 1.0),
        (ScreenSpaceUtilizationScorer(), 1.0),
    ],
)
