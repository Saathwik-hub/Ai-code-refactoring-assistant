import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "refactor_ai.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Analysis Reports table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_reports (
        id TEXT PRIMARY KEY,
        filename TEXT NOT NULL,
        language TEXT NOT NULL,
        health_score INTEGER NOT NULL,
        grade TEXT NOT NULL,
        total_issues INTEGER NOT NULL,
        critical_count INTEGER NOT NULL,
        high_count INTEGER NOT NULL,
        medium_count INTEGER NOT NULL,
        low_count INTEGER NOT NULL,
        info_count INTEGER NOT NULL,
        report_data TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    # AI Refactoring History table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS refactoring_history (
        id TEXT PRIMARY KEY,
        filename TEXT NOT NULL,
        language TEXT NOT NULL,
        mode TEXT NOT NULL,
        model_used TEXT NOT NULL,
        original_code TEXT NOT NULL,
        refactored_code TEXT NOT NULL,
        explanations TEXT NOT NULL,
        metrics_before TEXT NOT NULL,
        metrics_after TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def save_analysis_report(report_dict: Dict[str, Any]):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO analysis_reports (
        id, filename, language, health_score, grade, total_issues,
        critical_count, high_count, medium_count, low_count, info_count,
        report_data, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report_dict["id"],
        report_dict["filename"],
        report_dict["language"],
        report_dict["health_score"],
        report_dict["grade"],
        report_dict["total_issues"],
        report_dict.get("critical_count", 0),
        report_dict.get("high_count", 0),
        report_dict.get("medium_count", 0),
        report_dict.get("low_count", 0),
        report_dict.get("info_count", 0),
        json.dumps(report_dict),
        report_dict.get("created_at", datetime.now().isoformat())
    ))
    conn.commit()
    conn.close()

def get_analysis_report(report_id: str) -> Optional[Dict[str, Any]]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT report_data FROM analysis_reports WHERE id = ?", (report_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None

def save_refactoring_session(session_dict: Dict[str, Any]):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO refactoring_history (
        id, filename, language, mode, model_used,
        original_code, refactored_code, explanations,
        metrics_before, metrics_after, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session_dict["id"],
        session_dict["filename"],
        session_dict["language"],
        session_dict["mode"],
        session_dict.get("model_used", "Ollama (Qwen2.5-Coder)"),
        session_dict["original_code"],
        session_dict["refactored_code"],
        json.dumps(session_dict.get("explanations", [])),
        json.dumps(session_dict.get("metrics_before", {})),
        json.dumps(session_dict.get("metrics_after", {})),
        session_dict.get("created_at", datetime.now().isoformat())
    ))
    conn.commit()
    conn.close()

def get_refactoring_history() -> List[Dict[str, Any]]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, filename, language, mode, model_used, created_at
    FROM refactoring_history ORDER BY created_at DESC LIMIT 50
    """)
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        results.append({
            "id": r[0],
            "filename": r[1],
            "language": r[2],
            "mode": r[3],
            "model_used": r[4],
            "created_at": r[5]
        })
    return results

def get_refactoring_session(session_id: str) -> Optional[Dict[str, Any]]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM refactoring_history WHERE id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "filename": row[1],
            "language": row[2],
            "mode": row[3],
            "model_used": row[4],
            "original_code": row[5],
            "refactored_code": row[6],
            "explanations": json.loads(row[7]),
            "metrics_before": json.loads(row[8]),
            "metrics_after": json.loads(row[9]),
            "created_at": row[10]
        }
    return None

# Initialize SQLite tables on import
init_db()
