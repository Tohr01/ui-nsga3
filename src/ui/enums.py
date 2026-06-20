from enum import StrEnum


# NOTE: When adding or removing, update GoldenRatioTextSizeScorer roles
class TextType(StrEnum):
    HEADER = "header"
    SUBHEADER = "subheader"
    PARAGRAPH = "paragraph"
    FOOTNOTE = "footnote"
    OTHER = "other"
