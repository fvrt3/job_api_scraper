#app/scraper.py
import requests


def scrape_jobs():
    print("Scraping jobs...")

    url = "https://remoteok.com/api"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return f"Error fetching jobs: {e}"

    jobs = []
    for job in data[1:]:  # Skip the metadata entry at index 0
        min_salary = job.get("salary_min")
        max_salary = job.get("salary_max")

        if min_salary and max_salary:
            salary = f"${min_salary:,} - ${max_salary:,}"
        elif min_salary:
            salary = f"${min_salary:,}+"
        elif max_salary:
            salary = f"Up to ${max_salary:,}"
        else:
            salary = None

        jobs.append({
            "title": job.get("position"),
            "company": job.get("company"),
            "location": job.get("location"),
            "url": job.get("url"),
            "tags": job.get("tags", []),
            "salary": salary,
            "salary-min": int(min_salary),
            "salary-max": int(max_salary),
            "description": job.get("description")
        })
    
    return jobs