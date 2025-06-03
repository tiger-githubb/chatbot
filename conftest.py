"""
Global pytest fixtures and configuration.
This file contains fixtures that are available to all tests.
"""

import os
import pytest

# Set CI marker automatically if CI environment variable is set
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "ci: mark a test as running in a CI environment"
    )
    config.addinivalue_line(
        "markers", "integration: mark a test that requires external services"
    )
    config.addinivalue_line(
        "markers", "telegram: mark a test that requires the Telegram API"
    )
    config.addinivalue_line(
        "markers", "aws: mark a test that requires AWS services"
    )
    
    try:
        # Add CI marker automatically if CI environment variable is set
        if os.environ.get("CI", "").lower() == "true":
            # Don't apply CI marker to all tests, instead skip integration tests
            if not config.option.markexpr:
                config.option.markexpr = "not integration"
            elif "not integration" not in config.option.markexpr:
                config.option.markexpr = f"{config.option.markexpr} and not integration"
    except Exception as e:
        print(f"Warning: Error in pytest_configure: {e}")
        # Continue with default configuration


@pytest.fixture(scope="session")
def is_ci_environment():
    """Check if test is running in CI environment."""
    return os.environ.get("CI", "").lower() == "true"


@pytest.fixture(scope="session")
def skip_if_ci():
    """Skip a test if running in CI environment."""
    if os.environ.get("CI", "").lower() == "true":
        pytest.skip("Test skipped in CI environment")


@pytest.fixture(scope="session")
def skip_if_no_telegram():
    """Skip a test if no Telegram token is available."""
    from src.config import settings
    if not settings.TELEGRAM_BOT_TOKEN or settings.TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN":
        pytest.skip("No Telegram token available")


@pytest.fixture(scope="session")
def skip_if_no_aws():
    """Skip a test if no AWS credentials are available."""
    if not os.environ.get("AWS_ACCESS_KEY_ID") or not os.environ.get("AWS_SECRET_ACCESS_KEY"):
        pytest.skip("No AWS credentials available")
