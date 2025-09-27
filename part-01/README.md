# חיפוש עבודה באמצעות סוכנים חכמים - חלק 1

![intro-01.png](../docs/intro-01.png)

לכל אחד יש היום איזושהי דוגמה מגניבה איך סוכני AI חכמים מכינים להם קפה בבוקר, שואבים את הבית ומקפלים את הכביסה. גם אני רציתי כזה, אז החלטתי לנסות ולייצר לי צוות של סוכנים חכמים שימצאו לי עבודה חדשה.

לא, אני לא מחפש כרגע עבודה (אבל תמיד פתוח לרעיונות מעניינים).

המטרה היא ליצור סוכני AI שישתמשו במודלי שפה גדולים (LLM) בכדי למצוא לי משרה שתואמת להגדרות שהם קיבלו.

## קצירת משרות
לצורך הפרוייקט הזה הייתי זקוק לאוסף משרות שהסוכנים יוכלו לבדוק. החלטתי לגרד משרות מלינקדאין בעיקר בגלל שהן באנגלית (לא רציתי כרגע להתעמק ביכולות של LLM בשפת הקודש), יחסית מובנות ויש הרבה כאלו.

לצורך כך נעזרתי בספריה המופלאה: linkedin-jobs-scraper

בכמה שורות קוד פשוטות הצלחתי לאסוף מספר רב של משרות מוצעות בישראל מלינקדאין. בכוונה לא הגדרתי שום סינון נוסף פרט לישראל, כדי לראות איך הסוכנים יתמודדו עם הקריטריונים שלי בהמשך.

זה הקוד ששימש לאיסוף המשרות:

```python
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
```

קיבלתי אוסף של קבצי json, אחד לכל משרה, במבנה הכללי הזה:
```json
{
  "query": "",
  "location": "Israel",
  "job_id": "3264944914",
  "job_index": 5,
  "link": "https://www.linkedin.com/jobs/view/3264944914/?trk=flagship3_search_srp_jobs",
  "apply_link": "",
  "title": "Senior/Staff/Lead Architect - Build & Release Infrastructure with verification",
  "company": "Canonical",
  "company_link": "",
  "company_img_link": "https://media.licdn.com/dms/image/v2/C560BAQEbIYAkAURcYw/company-logo_100_100/company-logo_100_100/0/1650566107463/canonical_logo?e=1748476800&v=beta&t=VLzi_hxTcoSWKAPt9u-QNRfYLAQ2bKgtVVjn_aB4tyE",
  "place": "EMEA (Remote)",
  "description": "About the job",
  "description_html": "<div class=\"jobs-box--fadein jobs-box--full-width jobs-box--with-cta-large jobs-description\n        \n        \n        \n         jobs-description--reformatted\n        \n         job-details-module\">\n\n<!---->\n      <article class=\"jobs-description__container\n          \">\n        <div class=\"jobs-description__content jobs-description-content\n            \">\n          <div class=\"jobs-box__html-content\n              WFEGoUwjHEXqljyYwJHjVwufRmllLdVrCRU\n              t-14 t-normal\n              jobs-description-content__text--stretch\" id=\"job-details\" tabindex=\"-1\">\n            <h2 class=\"text-heading-large\">\n              About the job\n            </h2>\n\n<!---->            <div class=\"mt4\">\n<!----><!---->            </div>\n          </div>\n          <div class=\"jobs-description__details\">\n              \n    \n  <div role=\"presentation\" aria-busy=\"true\" alt=\"Loading the job description\">\n    \n        \n    <div class=\"scaffold-skeleton-container scaffold-skeleton-container--size-full  job-description-skeleton__text-container\">\n      \n          \n    <div class=\"scaffold-skeleton-container scaffold-skeleton-container--size-full \">\n      \n            \n    <div class=\"scaffold-skeleton-text scaffold-skeleton--shimmer\n        scaffold-skeleton-text--align-left\n        scaffold-skeleton-text--size-small\"></div>\n  \n          \n    </div>\n  \n\n          \n    <div class=\"scaffold-skeleton-container scaffold-skeleton-container--size-full scaffold-skeleton-container--medium\">\n      \n            \n    <div class=\"scaffold-skeleton-text scaffold-skeleton--shimmer\n        scaffold-skeleton-text--align-left\n        scaffold-skeleton-text--size-full\"></div>\n  \n            \n    <div class=\"scaffold-skeleton-text scaffold-skeleton--shimmer\n        scaffold-skeleton-text--align-left\n        scaffold-skeleton-text--size-large\"></div>\n  \n          \n    </div>\n  \n\n          \n    <div class=\"scaffold-skeleton-container scaffold-skeleton-container--size-full scaffold-skeleton-container--medium\">\n      \n            \n    <div class=\"scaffold-skeleton-text scaffold-skeleton--shimmer\n        scaffold-skeleton-text--align-left\n        scaffold-skeleton-text--size-large\"></div>\n  \n            \n    <div class=\"scaffold-skeleton-text scaffold-skeleton--shimmer\n        scaffold-skeleton-text--align-left\n        scaffold-skeleton-text--size-full\"></div>\n  \n            \n    <div class=\"scaffold-skeleton-text scaffold-skeleton--shimmer\n        scaffold-skeleton-text--align-left\n        scaffold-skeleton-text--size-medium\"></div>\n  \n          \n    </div>\n  \n        \n    </div>\n  \n        \n    <div class=\"scaffold-skeleton-container scaffold-skeleton-container--size-full  job-description-skeleton__text-container\">\n      \n          \n    <div class=\"scaffold-skeleton-container scaffold-skeleton-container--size-full \">\n      \n            \n    <div class=\"scaffold-skeleton-text scaffold-skeleton--shimmer\n        scaffold-skeleton-text--align-left\n        scaffold-skeleton-text--size-small\"></div>\n  \n          \n    </div>\n  \n\n          \n    <div class=\"scaffold-skeleton-container scaffold-skeleton-container--size-full scaffold-skeleton-container--medium\">\n      \n            \n    <div class=\"scaffold-skeleton-text scaffold-skeleton--shimmer\n        scaffold-skeleton-text--align-left\n        scaffold-skeleton-text--size-full\"></div>\n  \n            \n    <div class=\"scaffold-skeleton-text scaffold-skeleton--shimmer\n        scaffold-skeleton-text--align-left\n        scaffold-skeleton-text--size-large\"></div>\n  \n          \n    </div>\n  \n\n          \n    <div class=\"scaffold-skeleton-container scaffold-skeleton-container--size-full scaffold-skeleton-container--medium\">\n      \n            \n    <div class=\"scaffold-skeleton-text scaffold-skeleton--shimmer\n        scaffold-skeleton-text--align-left\n        scaffold-skeleton-text--size-large\"></div>\n  \n            \n    <div class=\"scaffold-skeleton-text scaffold-skeleton--shimmer\n        scaffold-skeleton-text--align-left\n        scaffold-skeleton-text--size-full\"></div>\n  \n            \n    <div class=\"scaffold-skeleton-text scaffold-skeleton--shimmer\n        scaffold-skeleton-text--align-left\n        scaffold-skeleton-text--size-medium\"></div>\n  \n          \n    </div>\n  \n        \n    </div>\n  \n        \n    <div class=\"scaffold-skeleton-container scaffold-skeleton-container--size-full  job-description-skeleton__text-container\">\n      \n          \n    <div class=\"scaffold-skeleton-container scaffold-skeleton-container--size-full \">\n      \n            \n    <div class=\"scaffold-skeleton-text scaffold-skeleton--shimmer\n        scaffold-skeleton-text--align-left\n        scaffold-skeleton-text--size-small\"></div>\n  \n          \n    </div>\n  \n\n          \n    <div class=\"scaffold-skeleton-container scaffold-skeleton-container--size-full scaffold-skeleton-container--medium\">\n      \n            \n    <div class=\"scaffold-skeleton-text scaffold-skeleton--shimmer\n        scaffold-skeleton-text--align-left\n        scaffold-skeleton-text--size-full\"></div>\n  \n            \n    <div class=\"scaffold-skeleton-text scaffold-skeleton--shimmer\n        scaffold-skeleton-text--align-left\n        scaffold-skeleton-text--size-large\"></div>\n  \n          \n    </div>\n  \n\n          \n    <div class=\"scaffold-skeleton-container scaffold-skeleton-container--size-full scaffold-skeleton-container--medium\">\n      \n            \n    <div class=\"scaffold-skeleton-text scaffold-skeleton--shimmer\n        scaffold-skeleton-text--align-left\n        scaffold-skeleton-text--size-large\"></div>\n  \n            \n    <div class=\"scaffold-skeleton-text scaffold-skeleton--shimmer\n        scaffold-skeleton-text--align-left\n        scaffold-skeleton-text--size-full\"></div>\n  \n            \n    <div class=\"scaffold-skeleton-text scaffold-skeleton--shimmer\n        scaffold-skeleton-text--align-left\n        scaffold-skeleton-text--size-medium\"></div>\n  \n          \n    </div>\n  \n        \n    </div>\n  \n    \n  </div>\n\n  \n          </div>\n        </div>\n      </article>\n<!---->    </div>",
  "date": "",
  "date_text": "",
  "insights": [],
  "skills": null
}
```

אספתי כמה מאות משרות, שלצורכי הפרוייקט הזה נראה לי מספק למדי (אבל אם אתם שוקלים להקים חברת השמה משלכם – צריך להשקיע הרבה יותר – לאסוף עוד משרות, מעוד מקורות וכו').

## הכנת קורות החיים
לצורך ההמשך לקחתי את קורות החיים שלי, שהיו בפורמט וורד, וביקשתי מצ'ט גי.פי.טי. להמיר לי אותם לקובץ MD (מרקדאון).

כעת יש לנו את כל הנתונים הבסיסיים להמשך העבודה וליצירת הסוכנים.

תמונת השער יוצרה באמצעות AI באתר tensor.art