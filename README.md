# AI-Powered Predictive Maintenance System with Real-Time Dashboard

## Overview
This project predicts machine failure probability using sensor data such as temperature, vibration, pressure, humidity, and runtime hours.

## Features
- FastAPI backend
- Machine learning model
- React dashboard
- SQLite prediction logs
- Failure probability and status alerts

## Tech Stack
- Python
- FastAPI
- Scikit-learn
- React
- SQLite

## Folder Structure
- `backend/` → API + ML model
- `frontend/` → dashboard UI
- `docs/` → report, presentation
- `images/` → screenshots and diagrams

## How to Run

### Backend
```bash
cd backend
pip install -r requirements.txt
python model/train_model.py
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
