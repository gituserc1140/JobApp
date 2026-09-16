from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "careeros.db"
STATUSES = ["saved", "applied", "interview", "assessment", "offer", "rejected"]


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                company TEXT,
                location TEXT,
                salary REAL,
                url TEXT,
                source TEXT,
                description TEXT,
                date_saved TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                job_title TEXT NOT NULL,
                status TEXT NOT NULL,
                notes TEXT,
                date_created TEXT NOT NULL
            )
            """
        )


def save_job(job: dict[str, Any]) -> None:
    now = datetime.now(timezone.utc).isoformat()
    with _conn() as conn:
        conn.execute(
            """
            INSERT INTO jobs (id, title, company, location, salary, url, source, description, date_saved)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title=excluded.title,
                company=excluded.company,
                location=excluded.location,
                salary=excluded.salary,
                url=excluded.url,
                source=excluded.source,
                description=excluded.description
            """,
            (
                str(job.get("id", "")),
                job.get("title", "Untitled"),
                job.get("company", "Unknown"),
                job.get("location", "Unknown"),
                job.get("salary"),
                job.get("url", ""),
                job.get("source", ""),
                job.get("description", ""),
                now,
            ),
        )


def list_saved_jobs(limit: int = 200) -> list[dict[str, Any]]:
    with _conn() as conn:
        rows = conn.execute(
            """
            SELECT id, title, company, location, salary, url, source, description, date_saved
            FROM jobs
            ORDER BY date_saved DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


def add_application(company: str, job_title: str, status: str, notes: str = "") -> None:
    clean_status = status if status in STATUSES else "saved"
    with _conn() as conn:
        conn.execute(
            """
            INSERT INTO applications (company, job_title, status, notes, date_created)
            VALUES (?, ?, ?, ?, ?)
            """,
            (company, job_title, clean_status, notes, datetime.now(timezone.utc).isoformat()),
        )


def update_status(app_id: int, status: str) -> None:
    if status not in STATUSES:
        return
    with _conn() as conn:
        conn.execute("UPDATE applications SET status = ? WHERE id = ?", (status, app_id))


def list_applications(limit: int = 500) -> list[dict[str, Any]]:
    with _conn() as conn:
        rows = conn.execute(
            """
            SELECT id, company, job_title, status, notes, date_created
            FROM applications
            ORDER BY date_created DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


def get_application_stats() -> dict[str, int]:
    stats = {k: 0 for k in ["total", *STATUSES]}
    with _conn() as conn:
        total = conn.execute("SELECT COUNT(*) AS c FROM applications").fetchone()["c"]
        stats["total"] = int(total)
        rows = conn.execute(
            "SELECT status, COUNT(*) AS c FROM applications GROUP BY status"
        ).fetchall()
    for row in rows:
        if row["status"] in stats:
            stats[row["status"]] = int(row["c"])
    return stats
