#!/bin/bash

# Run AI-Translate locally or with Docker

if [ "$1" = "docker" ]; then
    echo "🐳 Starting with Docker Compose..."
    docker-compose up --build
elif [ "$1" = "local" ]; then
    echo "🚀 Starting locally..."
    
    # Start backend
    echo "Starting Backend..."
    uvicorn app.main:app --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    
    sleep 2
    
    # Start frontend
    echo "Starting Frontend..."
    streamlit run frontend/app.py --server.port=8501 &
    FRONTEND_PID=$!
    
    echo "Backend running on http://localhost:8000"
    echo "Frontend running on http://localhost:8501"
    echo "Press Ctrl+C to stop"
    
    wait
else
    echo "Usage: ./scripts/run.sh [docker|local]"
    echo ""
    echo "Examples:"
    echo "  ./scripts/run.sh docker   # Run with Docker Compose"
    echo "  ./scripts/run.sh local    # Run locally"
fi
