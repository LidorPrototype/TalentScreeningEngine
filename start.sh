#!/bin/bash

# Start FastAPI and Streamlit in parallel
echo "Starting FastAPI..."
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 &

echo "Starting Streamlit UI..."
streamlit run frontend/app.py --server.port 8501 --server.enableCORS false
