#!/usr/bin/env bash
echo "==================================================="
echo "    Launching Dawa Dost (دوا دوست) Web Server"
echo "    Opening at http://127.0.0.1:8080"
echo "==================================================="

python3 backend/server.py || python backend/server.py
