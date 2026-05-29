from blueprints.ecommerce_prototype.content import content
from blueprints.ecommerce_prototype.footer import footer
from blueprints.ecommerce_prototype.header import header
from scoring.content import ContentScorer
from scoring.footer import FooterScorer
from scoring.header import HeaderScorer
from ui.blueprint import RootBlueprint

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
