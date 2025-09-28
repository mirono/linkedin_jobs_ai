from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from typing import Optional
import json
import logging
import os

logger = logging.getLogger(__name__)

class Job(BaseModel):
    job_id: Optional[str]
    location: Optional[str]
    title: Optional[str]
    company: Optional[str]
    description: Optional[str]
    link: Optional[str]

# Initialize FastMCP server
mcp = FastMCP("jobs")

# Constants
JOBS_FOLDER = "/Users/miron/Dev/rag/content_creation_01/job_search_agents_01/jobs"
# NWS_API_BASE = "https://api.weather.gov"
# USER_AGENT = "weather-app/1.0"

# async def make_nws_request(url: str) -> dict[str, Any] | None:
#     """Make a request to the NWS API with proper error handling."""
#     headers = {
#         "User-Agent": USER_AGENT,
#         "Accept": "application/geo+json"
#     }
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.get(url, headers=headers, timeout=30.0)
#             response.raise_for_status()
#             return response.json()
#         except Exception:
#             return None
#
# def format_alert(feature: dict) -> str:
#     """Format an alert feature into a readable string."""
#     props = feature["properties"]
#     return f"""
# Event: {props.get('event', 'Unknown')}
# Area: {props.get('areaDesc', 'Unknown')}
# Severity: {props.get('severity', 'Unknown')}
# Description: {props.get('description', 'No description available')}
# Instructions: {props.get('instruction', 'No specific instructions provided')}
# """
#
@mcp.tool()
async def get_jobs() -> str:
    """Get a list of all jobs.
    """
    logger.info("get_jobs tool called")
    job_ids = []
    for file_name in os.listdir(JOBS_FOLDER):
        if file_name.endswith(".json"):
            with open(os.path.join(JOBS_FOLDER, file_name), "r") as file:
                try:
                    job = Job.model_validate(json.load(file))
                    job_ids.append(job.job_id)
                except Exception as e:
                    logger.error(e)
    merged = "\n---\n".join(job_ids)
    return merged

@mcp.tool()
async def get_job(id: str) -> str:
    """Get a job by the job id.

    Args:
        id: the job id
    """
    logger.info(f"get_job tool called with id: {id}")
    file_name = f"job-{id}.json"
    try:
        with open(os.path.join(JOBS_FOLDER, file_name), "r") as file:
            job = Job.model_validate(json.load(file))
            return job.model_dump_json()
    except Exception as e:
        logger.error(e)
        return f"could not find job with id {id}, error {e}"
    # First get the forecast grid endpoint
#     points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
#     points_data = await make_nws_request(points_url)
#
#     if not points_data:
#         return "Unable to fetch forecast data for this location."
#
#     # Get the forecast URL from the points response
#     forecast_url = points_data["properties"]["forecast"]
#     forecast_data = await make_nws_request(forecast_url)
#
#     if not forecast_data:
#         return "Unable to fetch detailed forecast."
#
#     # Format the periods into a readable forecast
#     periods = forecast_data["properties"]["periods"]
#     forecasts = []
#     for period in periods[:5]:  # Only show next 5 periods
#         forecast = f"""
# {period['name']}:
# Temperature: {period['temperature']}°{period['temperatureUnit']}
# Wind: {period['windSpeed']} {period['windDirection']}
# Forecast: {period['detailedForecast']}
# """
#         forecasts.append(forecast)
#
#     return "\n---\n".join(forecasts)


def main():
    # Initialize and run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()