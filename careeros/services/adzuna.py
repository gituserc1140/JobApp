from __future__ import annotations

import os
from typing import Any

import requests


def search_jobs(
    keyword: str = "",
    location: str = "",
    min_salary: int | None = None,
    remote: bool = False,
    page: int = 1,
    country: str = "gb",
) -> list[dict[str, Any]]:
    app_id = os.getenv("ADZUNA_APP_ID", "").strip()
    app_key = os.getenv("ADZUNA_APP_KEY", "").strip()
    if not app_id or not app_key:
        return []

    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"
    params: dict[str, Any] = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": 30,
        "what": keyword,
        "where": location,
        "content-type": "application/json",
    }
    if min_salary:
        params["salary_min"] = min_salary

    response = requests.get(url, params=params, timeout=12)
    response.raise_for_status()
    jobs = response.json().get("results", [])

    out = []
    for job in jobs:
        location_name = (job.get("location") or {}).get("display_name", "")
        title = job.get("title", "")
        description = job.get("description", "")
        is_remote = "remote" in f"{title} {description} {location_name}".lower()
        if remote and not is_remote:
            continue
        out.append(
            {
                "id": f"adzuna-{job.get('id')}",
                "title": title,
                "company": (job.get("company") or {}).get("display_name", "Unknown"),
                "location": location_name or "Unknown",
                "salary": job.get("salary_min") or job.get("salary_max"),
                "url": job.get("redirect_url", ""),
                "source": "Adzuna",
                "description": description,
                "remote": is_remote,
            }
        )
    return out
