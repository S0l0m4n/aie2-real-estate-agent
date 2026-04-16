"""
This is the FastAPI server application that presents the /predict route for
predicting the house price given the input data.
"""

from fastapi import Body, FastAPI, HTTPException
from typing import Annotated

from app import ml_model as model
from app.schemas import HouseFeatures, PredictedPrice

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
            "neighborhood": "CollgCr",
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
