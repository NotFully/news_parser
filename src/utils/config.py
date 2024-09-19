import os
from dotenv import load_dotenv

load_dotenv()

BOT_KEY = os.getenv('BOT_KEY')
LOG_TOKEN = os.getenv('LOG_TOKEN')
PASSWORD = os.getenv('PASSWORD')

host = os.getenv('MYSQL_HOST')
port = int(os.getenv('MYSQL_PORT'))
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
dbname = os.getenv('MYSQL_DBNAME')

