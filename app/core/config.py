import os

from dotenv import load_dotenv

load_dotenv()

user = os.getenv("USER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
db_name = os.getenv("DB_NAME")

test_user = os.getenv("TEST_USER")
test_password = os.getenv("TEST_PASSWORD")
test_host = os.getenv("TEST_HOST")
test_port = os.getenv("TEST_PORT")
test_db_name = os.getenv("TEST_DB_NAME")


class Config:
    url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"
    echo = False

    test_url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"
    test_echo = False


settings = Config()
