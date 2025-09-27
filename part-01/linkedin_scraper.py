import logging
import os
import json

from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters

# Change root logger level (default is WARN)
logging.basicConfig(level=logging.INFO)

# Fired once for each successfully processed job
def on_data(data: EventData):
    print('[ON_DATA]', data.title, data.company, data.company_link, data.date, data.date_text, data.link, data.insights,
          len(data.description))
    with open(f"jobs/job-{data.job_id}.json", "w") as f:
        f.write(json.dumps(data._asdict()))

# Fired once for each page (25 jobs)
def on_metrics(metrics: EventMetrics):
    print('[ON_METRICS]', str(metrics))

def on_error(error):
    print('[ON_ERROR]', error)

def on_end():
    print('[ON_END]')

scraper = LinkedinScraper(
    chrome_executable_path=None,  # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver)
    chrome_binary_location=None,  # Custom path to Chrome/Chromium binary (e.g. /foo/bar/chrome-mac/Chromium.app/Contents/MacOS/Chromium)
    chrome_options=None,  # Custom Chrome options here
    headless=False,  # Overrides headless mode only if chrome_options is None
    max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
    slow_mo=1.5,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
    page_load_timeout=40  # Page load timeout (in seconds)
)

# Add event listeners
scraper.on(Events.DATA, on_data)
scraper.on(Events.ERROR, on_error)
scraper.on(Events.END, on_end)

queries = [
    Query(
        # query='Software',
        options=QueryOptions(
            locations=['Israel'],
            apply_link=True,  # Try to extract apply link (easy applies are skipped). If set to True, scraping is slower because an additional page must be navigated. Default to False.
            skip_promoted_jobs=False,  # Skip promoted jobs. Default to False.
            page_offset=2,  # How many pages to skip
            limit=12000,
        )
    ),
]

os.environ["LI_AT_COOKIE"] = "..."
scraper.run(queries)