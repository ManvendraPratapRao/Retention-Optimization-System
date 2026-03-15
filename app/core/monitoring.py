import sqlite3
import json
import os
from datetime import datetime
from app.core.logger import logger

# Determine the DB path, favoring the environment variable (for Docker persistence)
DB_PATH = os.getenv("MONITORING_DB_PATH")
if not DB_PATH:
    # Fallback to project root for local development
    DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "monitoring.db")

class Monitor:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite database for monitoring."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    features TEXT,
                    p_churn REAL,
                    risk_segment TEXT,
                    expected_gain REAL,
                    decision TEXT
                )
            """)
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize monitoring DB: {e}")

    def log_prediction(self, features, prediction_result, business_metrics):
        """Log a single prediction event."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Extract core metrics
            p_churn = prediction_result.get("p_churn")
            segment = prediction_result.get("segment")
            gain = business_metrics.get("expected_gain")
            decision = business_metrics.get("decision")
            
            # Serialize features to JSON
            features_json = json.dumps(features)
            
            cursor.execute("""
                INSERT INTO predictions (features, p_churn, risk_segment, expected_gain, decision)
                VALUES (?, ?, ?, ?, ?)
            """, (features_json, p_churn, segment, gain, decision))
            
            conn.commit()
            conn.close()
            logger.info(f"Logged prediction to monitoring DB (p_churn={p_churn:.2f})")
        except sqlite3.Error as e:
            logger.error(f"Failed to log prediction: {e}")

# Global monitor instance
monitor = Monitor()
