import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER','root')}:"
        f"{quote_plus(os.getenv('DB_PASSWORD',''))}@"
        f"{os.getenv('DB_HOST', 'localhost')}/"
        f"{os.getenv('DB_NAME', 'biblioteca')}?charset=utf8mb4"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False