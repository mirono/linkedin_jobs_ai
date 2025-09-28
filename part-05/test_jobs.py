import pytest
import jobs
from unittest.mock import patch, mock_open
import json


@pytest.mark.asyncio
async def test_get_jobs():
    """Test the get_jobs function directly"""
    # Call the function
    result = await jobs.get_jobs()

    # Basic assertions that the function returns a string
    assert isinstance(result, str)
    assert "---" in result


@pytest.mark.asyncio
async def test_get_job():
    """Test the get_jobs function directly with a mock file"""
    # Mock job data that would be loaded from the file
    mock_job_data = {
        "job_id": "4065459430",
        "title": "Senior Developer",
        "description": "A great job opportunity",
        "company": "Tech Corp",
        "location": "Remote",
        "link": "https://example.com/job"
    }

    # Create a mock for the open function
    mock_file = mock_open(read_data=json.dumps(mock_job_data))

    # Patch both open and os.path.join to avoid file system dependencies
    with patch("builtins.open", mock_file), \
            patch("os.path.join", return_value="mocked/path/to/job-4065459430.json"):
        # Call the function
        result = await jobs.get_job("4065459430")

        # Basic assertions that the function returns a string
        assert isinstance(result, str)
        expected = ["job_id", "title", "description", "company", "location", "link"]
        assert all(expected_field in result for expected_field in expected)

        # Check that the data matches what we mocked
        result_json = json.loads(result)
        assert result_json["job_id"] == "4065459430"
        assert result_json["title"] == "Senior Developer"
        assert result_json["company"] == "Tech Corp"


@pytest.mark.asyncio
async def test_get_job_fail():
    """Test the get_jobs function directly"""
    # Call the function
    result = await jobs.get_job("notarealid")

    # Basic assertions that the function returns a string
    assert isinstance(result, str)
    assert "could not find job with id notarealid" in result