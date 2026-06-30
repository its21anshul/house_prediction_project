# 🏠 California House Price Prediction API

A production-ready **Machine Learning REST API** built using **FastAPI** and **Scikit-Learn** to predict California house prices. The project supports both **single-house prediction** and **bulk prediction using CSV files**. The API loads a trained Random Forest model and exposes endpoints for real-time inference. :contentReference[oaicite:0]{index=0}

---

## 🚀 Features

- Predict house price for a single house
- Bulk prediction using CSV upload
- FastAPI automatic Swagger documentation
- Input validation using Pydantic
- Health check endpoint
- Returns downloadable prediction CSV
- Trained Random Forest Regression model
- Feature names stored separately using Joblib

---

## 📂 Project Structure

```text
house_prediction_api/
│
├── main.py                  # FastAPI application
├── train.py                 # Model training script
├── explore.py               # Dataset exploration
├── house_model.joblib       # Trained ML model
├── house_features.joblib    # Feature names
├── predictions.csv          # Sample output
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

- Python 3.12
- FastAPI
- Scikit-Learn
- Pandas
- Joblib
- Uvicorn
- Pydantic

---

## 📊 Dataset

This project uses the **California Housing Dataset** available in Scikit-Learn.

Features:

- MedInc
- HouseAge
- AveRooms
- AveBedrms
- Population
- AveOccup
- Latitude
- Longitude

Target:

- Median House Value

The dataset is loaded from Scikit-Learn and converted into a Pandas DataFrame before training. :contentReference[oaicite:1]{index=1}

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/california-house-price-api.git
```

Move into the project

```bash
cd california-house-price-api
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🧠 Train the Model

Run

```bash
python train.py
```

This creates

- house_model.joblib
- house_features.joblib

---

# ▶️ Run the API

```bash
uvicorn main:app --reload
```

Server

```
http://127.0.0.1:8000
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# 📌 API Endpoints

## Home

```
GET /
```

Returns API status.

---

## Health Check

```
GET /health
```

Returns

- API status
- Model name
- Features
- Average prediction error

---

## Single Prediction

```
POST /predict
```

Example Request

```json
{
  "MedInc": 8.3252,
  "HouseAge": 41,
  "AveRooms": 6.984,
  "AveBedrms": 1.023,
  "Population": 322,
  "AveOccup": 2.555,
  "Latitude": 37.88,
  "Longitude": -122.23
}
```

Example Response

```json
{
  "predicted_price": "$452,000",
  "predicted_price_short": "$4.52 hundred thousands",
  "confidence_range": "$413,000 to $491,000"
}
```

---

## Bulk Prediction

```
POST /predict-file
```

Upload a CSV file containing these columns:

| Column |
|----------|
| MedInc |
| HouseAge |
| AveRooms |
| AveBedrms |
| Population |
| AveOccup |
| Latitude |
| Longitude |

Returns

```
predictions.csv
```

with an additional column:

```
PredictedPrice
```

The API validates file type, required columns, and empty uploads before generating predictions. :contentReference[oaicite:2]{index=2}

---

# 📷 Swagger UI

FastAPI automatically generates interactive API documentation.

```
http://127.0.0.1:8000/docs
```

---

# 🧪 Model Information

Algorithm

```
Random Forest Regressor
```

Problem Type

```
Regression
```

Framework

```
Scikit-Learn
```

---

# 📈 Future Improvements

- Docker support
- Model versioning
- Authentication (JWT)
- Cloud deployment (Render/AWS/Azure)
- CI/CD with GitHub Actions
- Logging and monitoring
- Model retraining pipeline

---

# 👨‍💻 Author

**Anshul Yadav**

Machine Learning & AI Enthusiast

---

# ⭐ If you found this project helpful

Please consider giving it a ⭐ on GitHub.
