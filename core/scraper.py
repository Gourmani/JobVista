from abc import ABC, abstractmethod
from typing import List
from db.models import JobPosting


class BaseScraper(ABC):
    """
    Base class for all job scrapers
    """

    @abstractmethod
    def fetch_jobs(self) -> List[JobPosting]:
        pass
