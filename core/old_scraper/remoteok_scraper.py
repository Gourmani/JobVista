import requests
from bs4 import BeautifulSoup
from typing import List
from db.models import JobPosting
from utils.logger import logger


class RemoteOKScraper:
    """
    Scrapes real jobs from RemoteOK API page
    """

    URL = "https://remoteok.com/remote-dev+python-jobs"

    def fetch_jobs(self) -> List[JobPosting]:
        logger.info("Fetching REAL jobs from RemoteOK...")

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(self.URL, headers=headers)

        if response.status_code != 200:
            logger.error("Failed to fetch RemoteOK")
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        job_rows = soup.select("tr.job")

        jobs: List[JobPosting] = []

        for job in job_rows:

            title_tag = job.select_one("h2")
            company_tag = job.select_one("h3")
            location_tag = job.select_one(".location")

            if not title_tag or not company_tag:
                continue

            title = title_tag.get_text(strip=True)
            company = company_tag.get_text(strip=True)
            location = location_tag.get_text(strip=True) if location_tag else "Remote"

            description = job.get_text(" ", strip=True)

            job_obj = JobPosting(
                title=title,
                company=company,
                location=location,
                description=description,
                source="RemoteOK"
            )

            jobs.append(job_obj)

        logger.info(f"RemoteOK Jobs fetched: {len(jobs)}")
        return jobs
