from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from typing import Optional
from app.scraper import scrape_jobs


app = FastAPI(title="Job Scraper API")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse(os.path.join("static", "job_scraper_ui.html"))

@app.get("/jobs")
def get_jobs(
    tag: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    min_salary: Optional[int] = Query(None),
    max_salary: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    limit:  int = Query(10, ge=1, le=100),
):
    
    jobs = scrape_jobs()
    filtered = []

    for job in jobs:
        #filter by tag
        if tag and tag.lower() not in [t.lower() for t in job.get("tags", [])]:
            continue
        
        #filter by location
        if location and location.lower() not in (job.get("location") or "").lower():
            continue

        #filter by keyword in title or company name
        if keyword:
            if keyword.lower() not in (job.get("title") or "").lower() and \
                keyword.lower() not in (job.get("company") or "").lower() and \
                keyword.lower() not in (job.get("description") or "").lower():
                continue
    
        #filter by salary
        job_min = job.get("salary-min")
        job_max = job.get("salary-max")

        if min_salary and (not job_min or job_min < min_salary):
            continue
        if max_salary and (not job_max or job_max > max_salary):
            continue

        filtered.append(job)
    
    #paginate
    start = (page - 1) * limit
    end = start + limit
    paginated = filtered[start:end]


    return {
        "page": page,
        "limit": limit,
        "total_results": len(filtered),
        "results": paginated,
    }