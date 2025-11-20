#!/bin/bash

# Test API script for AI-Translate
# Usage: ./scripts/test_api.sh

API_URL="http://localhost:8000"
SAMPLE_FILE="sample_files/sample_audio.mp3"

echo "🧪 Testing AI-Translate API"
echo "================================"

# Test health
echo -e "\n1️⃣ Health Check:"
curl -s -X GET "$API_URL/api/health" | python -m json.tool

# Test upload (if sample file exists)
if [ -f "$SAMPLE_FILE" ]; then
    echo -e "\n2️⃣ Uploading file: $SAMPLE_FILE"
    RESPONSE=$(curl -s -X POST \
        -F "file=@$SAMPLE_FILE" \
        -F "target_lang=en" \
        "$API_URL/api/upload")
    
    echo "$RESPONSE" | python -m json.tool
    
    # Extract job ID
    JOB_ID=$(echo "$RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['job_id'])" 2>/dev/null)
    
    if [ ! -z "$JOB_ID" ]; then
        echo -e "\n3️⃣ Polling for results (Job ID: $JOB_ID):"
        
        for i in {1..30}; do
            echo "Attempt $i/30..."
            curl -s -X GET "$API_URL/api/result/$JOB_ID" | python -m json.tool
            sleep 2
        done
    fi
else
    echo "⚠️ Sample file not found. Skipping upload test."
    echo "📝 Available test: PUT SAMPLE FILES IN sample_files/"
fi

# List all jobs
echo -e "\n4️⃣ All Jobs:"
curl -s -X GET "$API_URL/api/jobs" | python -m json.tool

echo -e "\n✅ Tests completed"
