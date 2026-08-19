#!/bin/bash
echo "Starting STRATA API..."
cd /workspaces/businessdev-agent/strata-api
python3 -m uvicorn server:app --host 0.0.0.0 --port 8000 &
echo "Starting STRATA OS..."
cd /workspaces/businessdev-agent/strata-os
npm run dev -- --host 0.0.0.0 --port 5173 &
