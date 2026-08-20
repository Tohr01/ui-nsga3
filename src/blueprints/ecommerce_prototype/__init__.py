from blueprints.ecommerce_prototype.content import content
from blueprints.ecommerce_prototype.footer import footer
from blueprints.ecommerce_prototype.header import header
from scoring.constraints.min_size import MinSizeScorer
from scoring.constraints.padding import PaddingScorer
from scoring.footer import FooterScorer
from scoring.header import HeaderScorer
from scoring.screen_space_utilize import ScreenSpaceUtilizationScorer
from ui.blueprint import RootBlueprint

interface_blueprint = RootBlueprint(
    width_px=1920,
    height_px=1080,
    label="Baselayout",
    elements=[
        header,
        content,
        footer,
    ],
    scorers=[
        (HeaderScorer(), 1.0),
        (FooterScorer(), 1.0),
        (ScreenSpaceUtilizationScorer(), 1.0),
    ],
    global_constraints=[
        PaddingScorer(padding=0.01),
        MinSizeScorer(min_width=0.0, min_height=0.0),
    ],
)
