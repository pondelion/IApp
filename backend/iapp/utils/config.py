import os

import yaml

from .logger import Logger


DEFAULT_AWS_FILEPATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', '..',
    'config/aws.yml'
)
DEFAULT_TWITTER_FILEPATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', '..',
    'config/twitter.yml'
)
DEFAULT_DATALOCATION_FILEPATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', '..',
    'config/data_location.yml'
)
DEFAULT_DEV_FILEPATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', '..',
    'config/dev.yml'
)
DEFAULT_DB_FILEPATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', '..',
    'config/db_local.yml'
)


def _load_aws_config(filepath: str = DEFAULT_AWS_FILEPATH):
    return yaml.safe_load(open(filepath))


def _load_twitter_config(filepath: str = DEFAULT_TWITTER_FILEPATH):
    return yaml.safe_load(open(filepath))


def _load_datalocation_config(filepath: str = DEFAULT_DATALOCATION_FILEPATH):
    return yaml.safe_load(open(filepath))


def _load_dev_config(filepath: str = DEFAULT_DEV_FILEPATH):
    return yaml.safe_load(open(filepath))


def _load_db_config(filepath: str = DEFAULT_DB_FILEPATH):
    return yaml.safe_load(open(filepath))


class _AWSConfig(type):
    try:
        config = _load_aws_config()
        if 'ACCESS_KEY_ID' in config:
            os.environ['AWS_ACCESS_KEY_ID'] = config['ACCESS_KEY_ID']
            Logger.i('Config', f'Setting AWS_ACCESS_KEY_ID to {config["ACCESS_KEY_ID"][:4]}***')
        if 'SECRET_ACCESS_KEY' in config:
            os.environ['AWS_SECRET_ACCESS_KEY'] = config['SECRET_ACCESS_KEY']
            Logger.i('Config', f'Setting AWS_SECRET_ACCESS_KEY to {config["SECRET_ACCESS_KEY"][:4]}***')
        if 'REGION_NAME' in config:
            os.environ['AWS_DEFAULT_REGION'] = config['REGION_NAME']
        if 'ENDPOINT_URL' not in config:
            config['ENDPOINT_URL'] = None
        else:
            Logger.i('Config', f'Setting aws endpoint to {config["ENDPOINT_URL"]}')
    except Exception as e:
        Logger.w('Config', f'Failed to load aws config filr : {e}')
        config = {}

    def __getattr__(cls, key: str):
        if key in cls.config:
            return cls.config[key]
        elif key in os.environ:
            return os.environ[key]
        else:
            err_msg = f'No config value found for {key}, you must specify it in {DEFAULT_AWS_FILEPATH} or environment variable.'
            Logger.e('AWSConfig', f'{err_msg}')
            raise KeyError(f'[AWSConfig] {err_msg}')


class _TwitterConfig(type):
    try:
        config = _load_twitter_config()
    except Exception as e:
        Logger.w('Config', f'Failed to load twitter config filr : {e}')
        config = {}

    def __getattr__(cls, key: str):
        if key in cls.config:
            return cls.config[key]
        elif key in os.environ:
            return os.environ[key]
        else:
            err_msg = f'No config value found for {key}, you must specify it in {DEFAULT_TWITTER_FILEPATH} or environment variable.'
            Logger.e('TwitterConfig', f'{err_msg}')
            raise KeyError(f'[TwitterConfig] {err_msg}')


class _DataLocationConfig(type):
    try:
        config = _load_datalocation_config()
    except Exception as e:
        Logger.w('Config', f'Failed to load data_location config filr : {e}')
        config = {}

    def __getattr__(cls, key: str):
        if key in cls.config:
            return cls.config[key]
        elif key in os.environ:
            return os.environ[key]
        else:
            err_msg = f'No config value found for {key}, you must specify it in {DEFAULT_DATALOCATION_FILEPATH} or environment variable.'
            Logger.e('DataLocationConfig', f'{err_msg}')
            raise KeyError(f'[DataLocationConfig] {err_msg}')


class _DevConfig(type):
    try:
        config = _load_dev_config()
    except Exception as e:
        Logger.w('Config', f'Failed to load dev config filr : {e}')
        config = {}

    def __getattr__(cls, key: str):
        if key in cls.config:
            return cls.config[key]
        elif key in os.environ:
            return os.environ[key]
        else:
            err_msg = f'No config value found for {key}, you must specify it in {DEFAULT_DEV_FILEPATH} or environment variable.'
            Logger.e('DevConfig', f'{err_msg}')
            raise KeyError(f'[DevConfig] {err_msg}')


class _DBConfig(type):
    try:
        config = _load_db_config()
    except Exception as e:
        Logger.w('Config', f'Failed to load db config filr : {e}')
        config = {}

    def __getattr__(cls, key: str):
        if key in cls.config:
            return cls.config[key]
        elif key in os.environ:
            return os.environ[key]
        else:
            err_msg = f'No config value found for {key}, you must specify it in {DEFAULT_DB_FILEPATH} or environment variable.'
            Logger.e('DBConfig', f'{err_msg}')
            raise KeyError(f'[DBConfig] {err_msg}')


class AWSConfig(metaclass=_AWSConfig):
    pass


class TwitterConfig(metaclass=_TwitterConfig):
    pass


class DataLocationConfig(metaclass=_DataLocationConfig):
    pass


class DevConfig(metaclass=_DevConfig):
    pass


class DBConfig(metaclass=_DBConfig):
    pass
