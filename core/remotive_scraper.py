import requests
from typing import List
from db.models import JobPosting
from utils.logger import logger


class RemotiveScraper:
    """
    Fetch real remote jobs using public API
    """

    API_URL = "https://remotive.com/api/remote-jobs"

    def fetch_jobs(self) -> List[JobPosting]:
        logger.info("Fetching REAL jobs from Remotive API...")

        response = requests.get(self.API_URL)

        if response.status_code != 200:
            logger.error("Failed to fetch jobs from API")
            return []

        data = response.json()

        jobs: List[JobPosting] = []

        for job in data["jobs"][:80]:   # limit 80 jobs

            title = job.get("title", "")
            company = job.get("company_name", "")
            location = job.get("candidate_required_location", "Remote")
            description = job.get("description", "")

            job_obj = JobPosting(
                title=title,
                company=company,
                location=location,
                description=description,
                source="RemotiveAPI"
            )

            jobs.append(job_obj)

        logger.info(f"Jobs fetched from API: {len(jobs)}")
        return jobs
