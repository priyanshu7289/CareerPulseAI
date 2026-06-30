"""
scraper/job_scraper.py
Collects job postings from public listings using requests + BeautifulSoup,
with Selenium fallback for JS-rendered pages (LinkedIn, Glassdoor).

NOTE: Always respect each site's robots.txt and Terms of Service.
Add delays between requests and use official APIs where available
(e.g. Naukri/Indeed publisher APIs) for production use.
"""

import time
import random
import logging
from dataclasses import dataclass, asdict
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


@dataclass
class JobPosting:
    job_title: str
    company_name: str
    city: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    experience_min: Optional[float] = None
    experience_max: Optional[float] = None
    skills: Optional[List[str]] = None
    employment_type: Optional[str] = None
    education: Optional[str] = None
    posted_date: Optional[str] = None
    source_portal: str = "Unknown"
    job_description: Optional[str] = None


class BaseScraper:
    """Common scraping utilities shared across portal-specific scrapers."""

    def __init__(self, delay_range=(1.5, 3.5)):
        self.delay_range = delay_range
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def _polite_sleep(self):
        time.sleep(random.uniform(*self.delay_range))

    def fetch(self, url: str) -> Optional[BeautifulSoup]:
        try:
            resp = self.session.get(url, timeout=15)
            resp.raise_for_status()
            self._polite_sleep()
            return BeautifulSoup(resp.text, "html.parser")
        except requests.RequestException as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            return None


class GenericJobBoardScraper(BaseScraper):
    """
    Generic scraper template — adapt selectors to the specific portal's
    HTML structure. Designed to be subclassed per source (Naukri, Indeed, etc.)
    """

    SOURCE_NAME = "Generic"

    def search(self, keyword: str, location: str = "", pages: int = 1) -> List[JobPosting]:
        results: List[JobPosting] = []
        for page in range(1, pages + 1):
            url = self.build_search_url(keyword, location, page)
            soup = self.fetch(url)
            if soup is None:
                continue
            cards = self.extract_job_cards(soup)
            logger.info(f"[{self.SOURCE_NAME}] Page {page}: found {len(cards)} listings")
            results.extend(cards)
        return results

    def build_search_url(self, keyword: str, location: str, page: int) -> str:
        """Override in subclass — construct the portal's search URL."""
        raise NotImplementedError

    def extract_job_cards(self, soup: BeautifulSoup) -> List[JobPosting]:
        """Override in subclass — parse listing cards into JobPosting objects."""
        raise NotImplementedError


class NaukriScraper(GenericJobBoardScraper):
    SOURCE_NAME = "Naukri"

    def build_search_url(self, keyword: str, location: str, page: int) -> str:
        kw = keyword.replace(" ", "-").lower()
        loc = location.replace(" ", "-").lower()
        return f"https://www.naukri.com/{kw}-jobs-in-{loc}-{page}" if loc else f"https://www.naukri.com/{kw}-jobs-{page}"

    def extract_job_cards(self, soup: BeautifulSoup) -> List[JobPosting]:
        jobs = []
        for card in soup.select("article.jobTuple"):
            try:
                title = card.select_one(".title").get_text(strip=True)
                company = card.select_one(".companyInfo .subTitle")
                company = company.get_text(strip=True) if company else "Unknown"
                location_el = card.select_one(".locationsContainer")
                city = location_el.get_text(strip=True) if location_el else None
                exp_el = card.select_one(".expwdth")
                skills_el = card.select(".tagsContainer .tag")
                skills = [s.get_text(strip=True) for s in skills_el] if skills_el else []

                jobs.append(JobPosting(
                    job_title=title,
                    company_name=company,
                    city=city,
                    skills=skills,
                    source_portal=self.SOURCE_NAME,
                ))
            except (AttributeError, TypeError):
                continue
        return jobs


def scrape_all_sources(keyword: str, location: str = "", pages_per_source: int = 2) -> List[dict]:
    """
    Orchestrates scraping across all configured sources and returns a flat
    list of dicts ready to load into the raw dataset / staging table.
    """
    scrapers = [NaukriScraper()]
    all_jobs: List[JobPosting] = []

    for scraper in scrapers:
        try:
            jobs = scraper.search(keyword, location, pages=pages_per_source)
            all_jobs.extend(jobs)
        except NotImplementedError:
            logger.warning(f"{scraper.SOURCE_NAME} scraper not fully implemented yet — skipping.")
        except Exception as e:
            logger.error(f"Error scraping {scraper.SOURCE_NAME}: {e}")

    return [asdict(j) for j in all_jobs]


if __name__ == "__main__":
    results = scrape_all_sources(keyword="data analyst", location="bangalore", pages_per_source=1)
    logger.info(f"Total jobs collected: {len(results)}")
    for r in results[:5]:
        print(r)
