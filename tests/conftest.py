import os

import pytest

from notebooker.utils import caching
from notebooker.web.config import settings


@pytest.fixture
def bson_library(mongo_server, test_db_name, test_lib_name):
    return mongo_server.api[test_db_name][test_lib_name]


@pytest.fixture
def mongo_host(mongo_server):
    return f"{mongo_server.hostname}:{mongo_server.port}"


@pytest.fixture
def test_db_name(config):
    return config.DATABASE_NAME


@pytest.fixture
def test_lib_name(config):
    return config.RESULT_COLLECTION_NAME

@pytest.fixture
def template_dir(workspace, monkeypatch):
    monkeypatch.setenv("TEMPLATE_DIR", workspace.workspace)
    return workspace.workspace

@pytest.fixture
def output_dir(workspace, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", workspace.workspace)
    return workspace.workspace

@pytest.fixture
def config():
    return settings.DevConfig


@pytest.fixture
def clean_file_cache(monkeypatch, workspace):
    """Set up cache encironment."""
    assert caching.cache is None
    monkeypatch.setenv("CACHE_DIR", workspace.workspace)
    yield
    # purge the cache
    caching.cache = None


@pytest.fixture(autouse=True)
def _unset_notebooker_environ(config):
    """Remove Notebooker values from os.environ after each test."""
    yield
    for attribute in dir(config):
        if attribute.startswith("_"):
            continue
        os.environ.pop(attribute, None)
