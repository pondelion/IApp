from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from ..settings import settings
from ..models.sqlalchemy.base import Base
from ..models.sqlalchemy.twitter import *
from ..utils.logger import Logger


if not database_exists(settings.MYSQL_DATABASE_URI):
    Logger.i('rdb', f'Database not found. Creating database : {settings.MYSQL_DATABASE_URI}')
    create_database(settings.MYSQL_DATABASE_URI)

engine = create_engine(
    settings.MYSQL_DATABASE_URI,
    convert_unicode=True,
    pool_pre_ping=True
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = Session()
print(engine.table_names())


def init_rdb(recreate_table: bool = False) -> None:
    if recreate_table:
        drop_tables()
    Base.metadata.create_all(engine)


def show_tables() -> None:
    print(engine.table_names())


def drop_tables() -> None:
    Base.metadata.drop_all(engine)


def delete_all_tables() -> None:
    pass
