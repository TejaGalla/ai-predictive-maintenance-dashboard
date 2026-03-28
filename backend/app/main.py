from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import APP_NAME, ALERT_THRESHOLD
from .schemas import SensorInput, PredictionResponse
from .model_utils import predict_failure_probability
from .database import init_db, SessionLocal, PredictionLog
from .alert_utils import build_alert_message

app = FastAPI(title=APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/")
def root():
    return {"message": "Predictive Maintenance API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(data: SensorInput):
    try:
        probability = predict_failure_probability([
            data.temperature,
            data.vibration,
            data.pressure,
            data.humidity,
            data.runtime_hours,
        ])
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}") from e

    if probability >= ALERT_THRESHOLD:
        status = "Critical"
    elif probability >= 0.40:
        status = "Warning"
    else:
        status = "Normal"

    message = build_alert_message(probability, status)

    db = SessionLocal()
    try:
        row = PredictionLog(
            temperature=data.temperature,
            vibration=data.vibration,
            pressure=data.pressure,
            humidity=data.humidity,
            runtime_hours=data.runtime_hours,
            failure_probability=probability,
            status=status,
        )
        db.add(row)
        db.commit()
    finally:
        db.close()

    return PredictionResponse(
        failure_probability=round(probability, 4),
        status=status,
        message=message,
    )


@app.get("/history")
def history():
    db = SessionLocal()
    try:
        rows = db.query(PredictionLog).order_by(PredictionLog.id.desc()).limit(20).all()
        return [
            {
                "id": r.id,
                "temperature": r.temperature,
                "vibration": r.vibration,
                "pressure": r.pressure,
                "humidity": r.humidity,
                "runtime_hours": r.runtime_hours,
                "failure_probability": r.failure_probability,
                "status": r.status,
            }
            for r in rows
        ]
    finally:
        db.close()
