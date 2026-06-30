import io
import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

app = FastAPI()

# Load model and feature names
model = joblib.load("house_model.joblib")
features = joblib.load("house_features.joblib")


# Input Schema
class HouseFeatures(BaseModel):
    MedInc: float = Field(gt=0, description="Median income of the neighbourhood")
    HouseAge: float = Field(ge=0, description="Average age of houses in the block")
    AveRooms: float = Field(gt=0, description="Average number of rooms per house")
    AveBedrms: float = Field(gt=0, description="Average number of bedrooms per house")
    Population: float = Field(gt=0, description="Total population of the block")
    AveOccup: float = Field(gt=0, description="Average number of people per household")
    Latitude: float = Field(ge=32, le=42, description="Latitude")
    Longitude: float = Field(ge=-125, le=-114, description="Longitude")


# Home
@app.get("/")
def home():
    return {
        "message": "California House Prediction API",
        "status": "running",
        "endpoint": "Send POST request to /predict"
    }


# Health Check
@app.get("/health")
def health():
    return {
        "status": "running",
        "model": "RandomForestRegressor",
        "features": features,
        "avg_error": "$39,000"
    }


# Single Prediction
@app.post("/predict")
def predict(house: HouseFeatures):
    try:
        input_data = pd.DataFrame([{
            "MedInc": house.MedInc,
            "HouseAge": house.HouseAge,
            "AveRooms": house.AveRooms,
            "AveBedrms": house.AveBedrms,
            "Population": house.Population,
            "AveOccup": house.AveOccup,
            "Latitude": house.Latitude,
            "Longitude": house.Longitude
        }])

        prediction = model.predict(input_data)[0]
        price_usd = prediction * 100000

        return {
            "predicted_price": f"${price_usd:,.0f}",
            "predicted_price_short": f"${prediction:.2f} hundred thousands",
            "confidence_range": f"${price_usd - 39000:,.0f} to ${price_usd + 39000:,.0f}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


# Bulk Prediction using CSV
@app.post("/predict-file")
async def predict_file(file: UploadFile = File(...)):

    # Validate file extension
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV file only."
        )

    try:
        # Read uploaded CSV
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        # Required columns
        required_columns = [
            "MedInc",
            "HouseAge",
            "AveRooms",
            "AveBedrms",
            "Population",
            "AveOccup",
            "Latitude",
            "Longitude"
        ]

        # Check missing columns
        missing_columns = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Missing columns: {missing_columns}"
            )

        # Check empty file
        if len(df) == 0:
            raise HTTPException(
                status_code=400,
                detail="The uploaded CSV has no data."
            )

        # Make predictions
        predictions = model.predict(df[required_columns])

        # Add prediction columns
        df["PredictedPrice"] = predictions * 100000

        df["PredictedPrice"] = df["PredictedPrice"].apply(
            lambda x: f"${x:,.0f}"
        )

        # Convert dataframe to CSV
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)

        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=predictions.csv"
            }
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )