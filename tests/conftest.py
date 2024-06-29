import os
import sys

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(PROJECT_PATH, "src")
sys.path.append(SOURCE_PATH)


import pytest


@pytest.fixture(scope="session")
def settings():
    from common.settings import settings

    return settings
