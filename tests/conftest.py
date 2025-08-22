import pytest
from faker import Faker


@pytest.fixture
def get_faker():
    """Fixture to provide a Faker instance for generating test data."""
    return Faker()
