from testTask.app import App
from testTask.settings.settings import config
from aiohttp import web
from testTask.repository.repository import DatabaseInterface
from testTask.repository.postgres import Postgres


if __name__ == '__main__':
    db: DatabaseInterface = Postgres(config['pg'])
    app = App(database=db)
    web.run_app(app)
