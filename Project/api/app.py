from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import os

MODEL_PATH = os.getenv("MODEL_PATH", "biodiversity_model.pkl")
model = joblib.load(MODEL_PATH)

FEATURES = list(getattr(model, "feature_names_in_", []))
if not FEATURES:
    FEATURES = ["HAB", "SPP", "CS", "CP", "CW"]  # fallback

class PredictInput(BaseModel):
    HAB: float = Field(..., ge=0, le=100)
    SPP: float = Field(..., ge=0, le=100)
    CS:  float = Field(..., ge=0, le=100)
    CP:  float = Field(..., ge=0, le=100)
    CW:  float = Field(..., ge=0, le=100)

class PredictOutput(BaseModel):
    prediction: float

app = FastAPI(title="Biodiversity Predictor API")

# CORS — Nginx proxy’t van dezelfde host, dus dit is strikt genomen niet nodig.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # zet je domein in productie
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "features_expected": FEATURES}

@app.post("/predict", response_model=PredictOutput)
def predict(inp: PredictInput):
    try:
        row = {f: getattr(inp, f) for f in FEATURES}
    except AttributeError:
        raise HTTPException(status_code=400, detail=f"Model expects features: {FEATURES}")

    X = pd.DataFrame([row], columns=FEATURES)
    yhat = float(model.predict(X)[0])
    return {"prediction": yhat}
