import os

from dotenv import load_dotenv

load_dotenv()

user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')
db_name = os.getenv('DB_NAME')

test_user = os.getenv('POSTGRES_USER')
test_password = os.getenv('POSTGRES_PASSWORD')
test_host = os.getenv('TEST_HOST')
test_port = os.getenv('TEST_PORT')
test_db_name = os.getenv('TEST_DB_NAME')


class Config:
    url_for_engine = f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}'
    url = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
    echo = False

    test_url_for_engine = f'postgresql+asyncpg://{test_user}:{test_password}@{test_host}:{test_port}/{test_db_name}'
    test_url = f'postgresql://{test_user}:{test_password}@{test_host}:{test_port}/{test_db_name}'
    test_echo = False


settings = Config()
