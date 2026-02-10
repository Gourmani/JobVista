import sqlite3
from typing import List
from db.models import JobPosting
from utils.logger import logger


class JobDatabase:

    def __init__(self, db_name: str = "jobs.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            description TEXT,
            experience TEXT,
            salary TEXT,
            source TEXT,
            apply_link TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()
        logger.info("Database table ensured")

    def insert_jobs(self, jobs: List[JobPosting]):
        query = """
        INSERT INTO jobs (title, company, location, description, experience, salary, source, apply_link)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        job_data = [
            (
                job.title,
                job.company,
                job.location,
                job.description,
                job.experience,
                job.salary,
                job.source,
                job.apply_link
            )
            for job in jobs
        ]

        self.conn.executemany(query, job_data)
        self.conn.commit()
        logger.info(f"{len(jobs)} jobs inserted into database")

    def fetch_all_jobs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM jobs")
        return cursor.fetchall()

    def clear_jobs(self):
        """
        Delete all old jobs before inserting fresh jobs
        """
        query = "DELETE FROM jobs"
        self.conn.execute(query)
        self.conn.commit()
        logger.info("Old jobs cleared from database")
