import requests
from bs4 import BeautifulSoup
from typing import List
from db.models import JobPosting
from utils.logger import logger


class WeWorkScraper:
    """
    Scrapes real jobs from WeWorkRemotely
    """

    URL = "https://weworkremotely.com/remote-jobs/search?term=python"

    def fetch_jobs(self) -> List[JobPosting]:
        logger.info("Fetching REAL jobs from WeWorkRemotely...")

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(self.URL, headers=headers)

        if response.status_code != 200:
            logger.error("Failed to fetch jobs")
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        jobs: List[JobPosting] = []

        listings = soup.find_all("li", class_="feature")

        for job in listings:

            title_tag = job.find("span", class_="title")
            company_tag = job.find("span", class_="company")
            region_tag = job.find("span", class_="region")

            if not title_tag or not company_tag:
                continue

            title = title_tag.text.strip()
            company = company_tag.text.strip()
            location = region_tag.text.strip() if region_tag else "Remote"
            description = job.text.strip()

            job_obj = JobPosting(
                title=title,
                company=company,
                location=location,
                description=description,
                source="WeWorkRemotely"
            )

            jobs.append(job_obj)

        logger.info(f"Jobs fetched: {len(jobs)}")
        return jobs
