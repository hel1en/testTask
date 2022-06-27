import pathlib
import yaml

from testTask.models.config import ConfigFile, DbConfig

BASE_DIR = pathlib.Path(__file__).parent
config_path = BASE_DIR / 'config.yml'

__all__ = ['config']


def __get_config(path) -> ConfigFile:
    with open(path) as f:
        c = yaml.safe_load(f)

    return c


config = __get_config(config_path)
