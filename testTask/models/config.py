from dataclasses import dataclass


@dataclass
class DbConfig:
    database: str
    user: str
    password: str
    host: str
    port: int


@dataclass
class ConfigFile:
    pg: DbConfig
