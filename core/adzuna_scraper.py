import requests
import os
from dotenv import load_dotenv
from typing import List
from db.models import JobPosting
from utils.logger import logger

load_dotenv()  # load .env file


class AdzunaScraper:

    APP_ID = os.getenv("ADZUNA_APP_ID")
    APP_KEY = os.getenv("ADZUNA_APP_KEY")


    BASE_URL = "https://api.adzuna.com/v1/api/jobs/in/search/{}"

    def fetch_jobs(self, keyword="software developer") -> List[JobPosting]:
        logger.info(f"Fetching INDIA jobs for: {keyword}")

        jobs: List[JobPosting] = []

        page = 1

        while True:

            url = f"{self.BASE_URL.format(page)}?app_id={self.APP_ID}&app_key={self.APP_KEY}&results_per_page=50&what={keyword}"

            response = requests.get(url)

            if response.status_code != 200:
                break

            data = response.json()
            results = data.get("results", [])

            if not results:
                break

            for job in results:

                title = job.get("title", "")
                company = job.get("company", {}).get("display_name", "")
                location = job.get("location", {}).get("display_name", "India")
                description = job.get("description", "")
                apply_link = job.get("redirect_url", "")

                job_obj = JobPosting(
                    title=title,
                    company=company,
                    location=location,
                    description=description,
                    source="AdzunaIndia",
                    apply_link=apply_link
                )

                jobs.append(job_obj)

            page += 1

            if page > 5:   # safety limit (~250 jobs)
                break

        logger.info(f"Total jobs fetched: {len(jobs)}")
        return jobs
