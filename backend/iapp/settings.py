import secrets

from pydantic import AnyHttpUrl, BaseSettings
from sqlalchemy.engine.url import URL

from .utils.config import DBConfig


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8days
    # SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl

    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: int = 3306

    DEFAULT_DB_RECORD_REFRESH_SECS: int = 30 * 60

    DISABLE_AUTH: bool = False

    @property
    def MYSQL_DATABASE_URI(self) -> str:
        dialect_driver = 'mysql'
        url = URL(
            dialect_driver,
            self.DB_USERNAME,
            self.DB_PASSWORD,
            self.DB_HOST,
            self.DB_PORT,
            self.DB_NAME,
            query={
                'charset': 'utf8mb4',
                # 'timezone': 'utc',
            }
        )
        return url
        #return f'mysql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4'


settings = Settings(
    SERVER_HOST='http://127.0.0.0.1',
    DB_USERNAME=DBConfig.MYSQL_USER,
    DB_PASSWORD=DBConfig.MYSQL_PASSWORD,
    DB_HOST=DBConfig.DB_HOST,
    DB_PORT=int(DBConfig.DB_PORT),
    DB_NAME=DBConfig.MYSQL_DATABASE,
    DISABLE_AUTH=True,
)
