from dataclasses import dataclass
from typing import Optional


@dataclass
class JobPosting:
    title: str
    company: str
    location: str
    description: str
    experience: Optional[str] = None
    salary: Optional[str] = None
    source: Optional[str] = None
    apply_link: str = None
