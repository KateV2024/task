import pytest
import os
from pymongo import MongoClient
from playwright.sync_api import sync_playwright


BASE_URL = "http://localhost:3000"
BACKEND_URL = "http://localhost:5000/api/records"
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGODB_URL = f"mongodb://{MONGO_HOST}:27017/myapp"
DATABASE_NAME = "myapp"
COLLECTION_NAME = "My_records"


@pytest.fixture(params=["en", "ru"], scope="function")
def locale(request):
    return request.param

@pytest.fixture(scope="function")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        yield page
        context.close()
        browser.close()


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def backend_url():
    return BACKEND_URL


@pytest.fixture(scope="session")
def mongo_url():
    return MONGODB_URL

@pytest.fixture(scope="session")
def db_connection():
    client = MongoClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    yield db
    client.close()

@pytest.fixture(scope='function')
def db_collection(db_connection):
    return db_connection[COLLECTION_NAME]
