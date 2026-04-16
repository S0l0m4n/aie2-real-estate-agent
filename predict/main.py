"""
This is the FastAPI server application that presents the /predict route for
predicting the house price given the input data.
"""

from enum import Enum
from typing import Annotated

from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel, Field

from . import ml_model as model

# --- PYDANTIC TYPES ---


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


# --- FASTAPI APP ---

app = FastAPI(title="AI Real Estate Agent API")


@app.on_event("startup")
def startup():
    try:
        model.load_model()
    except FileNotFoundError as e:
        # Allow the server to start without the model — /predict will return 503
        print(f"WARNING: {e}")


# Sanity health check
@app.get("/health")
def health():
    """
    A simple heath check, should return "ok" when run.
    """
    return {"status": "ok"}


EXAMPLES = {
    "new_2_story": {
        "summary": "New 2-story house",
        "value": {
            "bedrooms": 3,
            "central_air": True,
            "has_garage": False,
            "lot_area": 8450,
            "ms_sub_class": 60,
            "neighborhood": "Collgr",
            "overall_qual": 7,
            "total_rooms": 8,
            "year_built": 2003,
        },
    },
    "old_2_story": {
        "summary": "Old 2-story house",
        "value": {
            "bedrooms": 3,
            "central_air": True,
            "has_garage": False,
            "lot_area": 9600,
            "ms_sub_class": 70,
            "neighborhood": "OldTown",
            "overall_qual": 7,
            "total_rooms": 6,
            "year_built": 1925,
        },
    },
}


# POST: Predict house price
@app.post("/predict", response_model=PredictedPrice)
def predict(input_features: Annotated[HouseFeatures, Body(openapi_examples=EXAMPLES)]):
    """
    Predict the house price based on the input features.
    """
    if model._model is None:
        raise HTTPException(status_code=503, detail="Model not loaded.")

    # Map API field names to the column names the model was trained on
    features = {
        "BedroomAbvGr": input_features.bedrooms,
        "CentralAir": int(input_features.central_air),
        "HasGarage": int(input_features.has_garage),
        "LotArea": input_features.lot_area,
        "MSSubClass": input_features.ms_sub_class.value,
        "Neighborhood": input_features.neighborhood.value,
        "OverallQual": input_features.overall_qual,
        "TotRmsAbvGrd": input_features.total_rooms,
        "YearBuilt": input_features.year_built,
    }

    y = model.predict(features)
    return PredictedPrice(predicted_price=round(y / 1000) * 1000)
