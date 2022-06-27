import functools

import aiohttp_jinja2
import jinja2
from aiohttp.web import Application
from aiohttp import web

from testTask.repository.repository import DatabaseInterface
from testTask import handler


class App(Application):

    def __init__(self, database: DatabaseInterface, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database: DatabaseInterface = database
        self.init_routing()
        self.setup_jinja()
        self.on_startup.append(database.connect)
        self.on_cleanup.append(database.disconnect)

    def setup_jinja(self):
        aiohttp_jinja2.setup(self,
                             loader=jinja2.FileSystemLoader(
                                 'testTask/templates'))

    def init_routing(self):
        create_employee = handler.CreateEmployee()
        get_employee = handler.GetEmployee()
        get_employees = handler.GetEmployees()
        update_employee = handler.UpdateEmployee()
        delete_employee = handler.DeleteEmployee()
        base_page = handler.BasePage()
        routes = [
            web.get(base_page.path, base_page.handle),
            web.post(create_employee.path,
                     functools.partial(create_employee.handle,
                                       database=self.database)),
            web.get(get_employees.path,
                    functools.partial(get_employees.handle,
                                      database=self.database)),
            web.get(get_employee.path,
                    functools.partial(get_employee.handle,
                                      database=self.database)),
            web.patch(update_employee.path,
                      functools.partial(update_employee.handle,
                                        database=self.database)),
            web.delete(delete_employee.path,
                       functools.partial(delete_employee.handle,
                                         database=self.database)),
            web.static("/static", "testTask/static")
        ]
        self.add_routes(routes=routes)

