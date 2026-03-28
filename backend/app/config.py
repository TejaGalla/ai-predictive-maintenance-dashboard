import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Predictive Maintenance API")
ALERT_THRESHOLD = float(os.getenv("ALERT_THRESHOLD", "0.70"))
DATABASE_URL = "sqlite:///./maintenance.db"
MODEL_PATH = "model/predictive_model.pkl"
