"""
Test configuration for Surooh Academy
"""
import pytest
import asyncio
from httpx import AsyncClient
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def client():
    """Create an async test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def sample_project_data():
    """Sample project data for testing."""
    return {
        "project_name": "Test Academy Bot",
        "industry": "Education",
        "target_audience": "Students and Teachers",
        "core_objectives": [
            "Provide educational support",
            "Answer academic questions",
            "Guide learning paths"
        ],
        "key_features": [
            "Q&A assistance",
            "Study material recommendations",
            "Progress tracking"
        ],
        "technical_requirements": [
            "Multilingual support",
            "Integration with LMS",
            "Real-time responses"
        ],
        "budget_range": "10000-50000",
        "timeline": "3-6 months",
        "success_metrics": [
            "User engagement rate > 80%",
            "Response accuracy > 95%",
            "User satisfaction > 4.5/5"
        ]
    }

@pytest.fixture
def bot_training_data():
    """Sample bot training data."""
    return {
        "bot_type": "educational",
        "training_content": "This is educational content for training the bot.",
        "learning_objectives": ["Understand concepts", "Provide accurate answers"],
        "complexity_level": "intermediate"
    }