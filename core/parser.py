import requests
from bs4 import BeautifulSoup
from typing import List
from db.models import JobPosting
from utils.logger import logger


class StaticJobScraper:
    """
    Scrapes jobs from a static demo job website
    """

    URL = "https://realpython.github.io/fake-jobs/"

    def fetch_jobs(self) -> List[JobPosting]:
        logger.info("Fetching jobs from static site...")

        response = requests.get(self.URL)

        if response.status_code != 200:
            logger.error("Failed to fetch website")
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        job_cards = soup.find_all("div", class_="card-content")

        jobs: List[JobPosting] = []

        for job in job_cards:
            title = job.find("h2", class_="title").text.strip()
            company = job.find("h3", class_="company").text.strip()
            location = job.find("p", class_="location").text.strip()
            description = job.text.strip()

            job_obj = JobPosting(
                title=title,
                company=company,
                location=location,
                description=description,
                source="StaticDemoSite"
            )

            jobs.append(job_obj)

        logger.info(f"Total jobs fetched: {len(jobs)}")
        return jobs
