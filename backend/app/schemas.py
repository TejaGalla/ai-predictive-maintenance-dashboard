from pydantic import BaseModel, Field


class SensorInput(BaseModel):
    temperature: float = Field(..., ge=0, le=200)
    vibration: float = Field(..., ge=0, le=100)
    pressure: float = Field(..., ge=0, le=300)
    humidity: float = Field(..., ge=0, le=100)
    runtime_hours: float = Field(..., ge=0)


class PredictionResponse(BaseModel):
    failure_probability: float
    status: str
    message: str
