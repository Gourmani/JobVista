import json
from collections import Counter
from typing import List, Dict
from db.models import JobPosting
from utils.logger import logger


class SkillExtractor:

    def __init__(self, skill_file: str = "data/seed_skills.json"):
        with open(skill_file, "r") as f:
            self.skills = json.load(f)

        logger.info("Skill extractor initialized")

    def extract_skills_from_jobs(self, jobs: List[JobPosting]) -> Dict[str, int]:
        """
        Count skill demand from job descriptions
        """
        skill_counter = Counter()

        for job in jobs:
            description = job.description.lower()

            for skill in self.skills:
                if skill in description:
                    skill_counter[skill] += 1

        return dict(skill_counter)
