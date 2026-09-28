import os
APP_NAME="NETX"
VERSION="0.4.0"
MAX_RESULTS=12
REQUEST_TIMEOUT=15
MAX_WORKERS=6
MIN_CONTENT_LENGTH=120
SUMMARY_SENTENCES=3
CACHE_HOURS=24
DATABASE_FILE=os.path.join("data","netx.db")
JSON_REPORT=os.path.join("reports","report.json")
HTML_REPORT=os.path.join("reports","report.html")
USER_AGENT="NETX/0.4 (+research-engine)"
