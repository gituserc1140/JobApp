from __future__ import annotations

from typing import Any

import requests

BASE_URL = "https://remotive.com/api/remote-jobs"


def search_jobs(keyword: str = "", location: str = "", limit: int = 50) -> list[dict[str, Any]]:
    params = {}
    if keyword:
        params["search"] = keyword

    response = requests.get(BASE_URL, params=params, timeout=12)
    response.raise_for_status()
    jobs = response.json().get("jobs", [])

    results = []
    for job in jobs[:limit]:
        candidate = {
            "id": f"remotive-{job.get('id')}",
            "title": job.get("title", ""),
            "company": job.get("company_name", ""),
            "location": job.get("candidate_required_location", "Remote"),
            "salary": None,
            "url": job.get("url", ""),
            "source": "Remotive",
            "description": job.get("description", ""),
            "remote": True,
            "category": job.get("category", ""),
        }
        if location and location.lower() not in (candidate["location"] or "").lower():
            continue
        results.append(candidate)
    return results
