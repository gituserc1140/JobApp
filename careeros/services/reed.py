from __future__ import annotations

import base64
import os
from typing import Any

import requests


def search_jobs(
    keyword: str = "",
    location: str = "",
    min_salary: int | None = None,
    remote: bool = False,
) -> list[dict[str, Any]]:
    api_key = os.getenv("REED_API_KEY", "").strip()
    if not api_key:
        return []

    basic = base64.b64encode((api_key + ":").encode("utf-8")).decode("utf-8")
    headers = {"Authorization": "Basic " + basic}
    params: dict[str, Any] = {
        "keywords": keyword,
        "locationName": location,
        "resultsToTake": 50,
    }
    if min_salary:
        params["minimumSalary"] = min_salary

    response = requests.get("https://www.reed.co.uk/api/1.0/search", params=params, headers=headers, timeout=12)
    response.raise_for_status()
    jobs = response.json().get("results", [])

    out: list[dict[str, Any]] = []
    for job in jobs:
        title = job.get("jobTitle", "")
        location_text = job.get("locationName", "")
        description = job.get("jobDescription", "")
        is_remote = "remote" in f"{title} {location_text} {description}".lower()
        if remote and not is_remote:
            continue
        out.append(
            {
                "id": f"reed-{job.get('jobId')}",
                "title": title,
                "company": job.get("employerName", "Unknown"),
                "location": location_text,
                "salary": job.get("minimumSalary") or job.get("maximumSalary"),
                "url": job.get("jobUrl", ""),
                "source": "Reed",
                "description": description,
                "remote": is_remote,
            }
        )
    return out
