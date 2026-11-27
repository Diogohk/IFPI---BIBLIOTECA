import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Em desenvolvimento, permite executar o projeto sem configurar o .env.
    # Em produção, SECRET_KEY deve ser definida por variável de ambiente.
    SECRET_KEY = os.getenv("SECRET_KEY") or "chave-apenas-para-desenvolvimento-biblioteca-ifpi"

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:"
        f"{quote_plus(os.getenv('DB_PASSWORD', ''))}@"
        f"{os.getenv('DB_HOST', 'localhost')}/"
        f"{os.getenv('DB_NAME', 'biblioteca')}?charset=utf8mb4"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY", "").strip()
