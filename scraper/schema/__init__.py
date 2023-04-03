from typing import Optional

from pydantic import Field
from pydantic.dataclasses import dataclass
from pydantic import BaseModel


class ScrapedCode(BaseModel):
    """The scraped codes of a given algorithm"""

    code: str = Field(
        default="", description="The code of the algorithm in a certain language"
    )
    comments: str = Field(default="", description="The first few comments in the code")


class ScrapedAlgorithm(BaseModel):
    """The final result of the scraping operations, an extracted algorithm with its attributes"""

    name: str = Field(default="", description="The name of the scraped algorithm")
    time_complexity: Optional[str] = Field(
        default="", description="The time complexity of the scraped algorithm"
    )
    trustable_time_complexity: bool = Field(
        default=True,
        description="If the given time complexity used a trustable extraction method",
    )
    space_complexity: Optional[str] = Field(
        default="", description="The space complexity of the algorithm"
    )
    trustable_space_complexity: bool = Field(
        default=True,
        description="If the given space complexity used a trustable extraction method",
    )
    url: str = Field(default="", description="The space complexity of the algorithm")
    codes: dict[str, ScrapedCode] = Field(
        default=dict(), description="The algorithm implementations"
    )

    def to_representation(self):
        ...
