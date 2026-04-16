"""
Pydantic data models
"""

from enum import Enum

from pydantic import BaseModel, Field

class MSSubClass(int, Enum):
    ONE_STORY_NEW = 20
    ONE_STORY_OLD = 30
    ONE_N_HALF_STORY = 50
    TWO_STORY_NEW = 60
    TWO_STORY_OLD = 70
    MULTI_LEVEL = 80
    DUPLEX = 90
    ONE_STORY_NEW_DEV = 120
    TWO_STORY_NEW_DEV = 160
    OTHER = 190

    # Map missing values to OTHER (when lookup fails)
    @classmethod
    def _missing_(cls, value):
        return cls.OTHER


class Neighborhood(str, Enum):
    BLOOMINGTON_HEIGHTS = "Blmngtn"
    BLUESTEM = "Blueste"
    BRIARDALE = "BrDale"
    BROOKSIDE = "BrkSide"
    CLEAR_CREEK = "ClearCr"
    COLLEGE_CREEK = "CollgCr"
    CRAWFORD = "Crawfor"
    EDWARDS = "Edwards"
    GILBERT = "Gilbert"
    GREEN_HILLS = "GrnHill"
    IOWA_DOT_RAILROAD = "IDOTRR"
    LANDMARK = "Landmrk"
    MEADOW_VILLAGE = "MeadowV"
    MITCHELL = "Mitchel"
    NORTH_AMES = "Names"
    NORTHRIDGE = "NoRidge"
    NORTHPARK_VILLA = "NPkVill"
    NORTHRIDGE_HEIGHTS = "NridgHt"
    NORTHWEST_AMES = "NWAmes"
    OLD_TOWN = "OldTown"
    IOWA_STATE_UNIVERSITY = "SWISU"
    SAWYER = "Sawyer"
    SAWYER_WEST = "SawyerW"
    SOMERSET = "Somerst"
    STONE_BROOK = "StoneBr"
    TIMBERLAND = "Timber"
    VEENKER = "Veenker"


class HouseFeatures(BaseModel):
    bedrooms: int = Field(ge=0)
    central_air: bool
    has_garage: bool
    lot_area: int
    ms_sub_class: MSSubClass = MSSubClass.ONE_STORY_NEW
    neighborhood: Neighborhood = Neighborhood.NORTH_AMES
    overall_qual: int = Field(ge=1, le=10)
    total_rooms: int = Field(ge=0)
    year_built: int = 1970


class PredictedPrice(BaseModel):
    predicted_price: int


