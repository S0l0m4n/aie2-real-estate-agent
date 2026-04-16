"""
This is the FastAPI server application that presents the /predict route for
predicting the house price given the input data.
"""

from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from . import ml_model as model

# --- PYDANTIC TYPES ---


class MSSubClass(int, Enum):
    pass


class Neighborhood(str, Enum):
    pass


class PredictRequest(BaseModel):
    bedrooms: int
    central_air: bool
    has_garage: bool
    lot_area: int
    ms_sub_class: MSSubClass
    neighborhood: Neighborhood
    overall_qual: int
    total_rooms: int
    year_built: int


class PredictResponse(BaseModel):
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


# POST: Predict house price
@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    """
    Predict the house price based on the input features.
    """
    if model._model is None:
        raise HTTPException(status_code=503, detail="Model not loaded.")
    features = {}
    price = model.predict(features)
    return PredictResponse(predicted_price=round(price / 1000) * 1000)
