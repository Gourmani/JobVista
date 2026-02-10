from core.adzuna_scraper import AdzunaScraper
from db.database import JobDatabase
from core.skill_extractor import SkillExtractor


def main():
    print("\n🚀 JobVista India Backend Pipeline\n")

    # Default domain (used only if running main.py manually)
    keyword = "software developer"

    scraper = AdzunaScraper()
    jobs = scraper.fetch_jobs(keyword)

    print(f"Total jobs fetched: {len(jobs)}")

    if len(jobs) == 0:
        print("No jobs fetched. Exiting.")
        return

    # Store fresh jobs
    db = JobDatabase()
    db.clear_jobs()
    db.insert_jobs(jobs)
    print("Database updated with latest jobs")

    # Skill analysis preview (console)
    skill_engine = SkillExtractor()
    skill_counts = skill_engine.extract_skills_from_jobs(jobs)

    print("\n🔥 Top Skills in Market:\n")

    sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)

    for skill, count in sorted_skills[:10]:
        print(f"{skill.upper()} : {count} jobs")


if __name__ == "__main__":
    main()
