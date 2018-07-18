import pytest
from pidgin.app import app as pidgin_app

@pytest.fixture
def app():
    return pidgin_app
