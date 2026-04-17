"""
This is the FastAPI server application that presents the /predict route for
predicting the house price given the input data.
"""

import json

from fastapi import Body, FastAPI, HTTPException
from typing import Annotated

from app import llm_client
from app import ml_model as model
from app.prompts import EXTRACT_FEATURES_PROMPT
from app.schemas import (
    ExtractedFeatures, HouseDescription, HouseFeatures, PredictedPrice
)

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


# --- ML model prediction ---

EXAMPLES = {
    "new_2_story": {
        "summary": "New 2-story house",
        "value": {
            "bedrooms": 3,
            "central_air": True,
            "has_garage": False,
            "lot_area": 8450,
            "house_type": 60,
            "neighborhood": "CollgCr",
            "overall_quality": 7,
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
            "house_type": 70,
            "neighborhood": "OldTown",
            "overall_quality": 7,
            "total_rooms": 6,
            "year_built": 1925,
        },
    },
}


# POST: Predict house price
@app.post("/predict", response_model=PredictedPrice)
def predict(request: Annotated[HouseFeatures, Body(openapi_examples=EXAMPLES)]):
    """
    Predict the house price based on the input features.
    """
    if model._model is None:
        raise HTTPException(status_code=503, detail="Model not loaded.")

    # Map API field names to the column names the model was trained on
    features = {
        "BedroomAbvGr": request.bedrooms,
        "CentralAir": int(request.central_air),
        "HasGarage": int(request.has_garage),
        "LotArea": request.lot_area,
        "MSSubClass": request.house_type.value,
        "Neighborhood": request.neighborhood.value,
        "OverallQual": request.overall_quality,
        "TotRmsAbvGrd": request.total_rooms,
        "YearBuilt": request.year_built,
    }

    y = model.predict(features)
    return PredictedPrice(price=round(y / 1000) * 1000)


# --- Stage 1 LLM: Feature extraction ---

# POST: Extract house features from description
@app.post("/extract", response_model=ExtractedFeatures)
def extract_features(request: HouseDescription):
    """Extract house features from a natural language property description."""
    response = llm_client.call(request.text, EXTRACT_FEATURES_PROMPT,
                               ExtractedFeatures)
    return ExtractedFeatures.model_validate_json(response)
