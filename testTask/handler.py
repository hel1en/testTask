from abc import ABC, abstractmethod
from typing import Dict, List

import aiohttp_jinja2
from aiohttp import web
from aiohttp.abc import Request
from aiohttp.web_response import Response, json_response
from loguru import logger

from testTask.enums import CodeStatus
from testTask.exceptions.exployee import EmployeeNotFount
from testTask.models.employee import Employee
from testTask.repository.repository import DatabaseInterface
from testTask.serializer import Serializer
from testTask import executor

routes = web.RouteTableDef()


class HandlerInterface(ABC):
    _path: str

    @property
    def path(self) -> str:
        return self._path

    @abstractmethod
    async def handle(self, *args, **kwargs) -> Response:
        pass


class GetEmployee(HandlerInterface):
    _path = '/api/employees/{uid}'
    _headers = {"Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Methods": 'DELETE',
                "Access-Control-Allow-Headers": "X-Client-Header",
                "Access-Control-Max-Age": "3600"}

    async def handle(self, r: Request,
                     database: DatabaseInterface) -> Response:
        response: Dict = {}
        status: int = CodeStatus.GET.value
        user_id: Employee.uid = Serializer.get_user_uid_field_from_url(r)
        try:
            employee: Dict = await executor.GetOneEmployee.exec(
                employee_uid=user_id, database=database)
            response = employee

        except EmployeeNotFount:
            response = {"Err": "Employee UID is not corrected"}
            status = CodeStatus.CLIENT_ERR.value

        except Exception as e:
            logger.exception(e)
            response = {"Err": str(e)}
            status = CodeStatus.SERVER_ERR.value

        finally:
            return json_response(response, status=status,
                                 headers=self._headers)


class GetEmployees(HandlerInterface):
    _path = '/api/employees'
    _headers = {"Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Methods": 'DELETE',
                "Access-Control-Allow-Headers": "X-Client-Header",
                "Access-Control-Max-Age": "3600"}

    async def handle(self, r: Request,
                     database: DatabaseInterface) -> Response:
        response: List[Dict] | Dict = []
        status: int = CodeStatus.GET.value
        body: Dict = await Serializer.read_body(r)
        try:
            employees: List[Dict] = await executor.GetManyEmployees.exec(
                limit=Serializer.get_limit_field_from_body(body),
                offset=Serializer.get_offset_field_from_body(body),
                database=database
            )
            response = employees

        except Exception as e:
            status = CodeStatus.SERVER_ERR.value
            response = {"Err": str(e)}

        finally:
            return json_response(response, status=status,
                                 headers=self._headers)


class DeleteEmployee(HandlerInterface):
    _path = '/api/employees/{uid}'
    _headers = {"Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Methods": 'DELETE',
                "Access-Control-Allow-Headers": "X-Client-Header",
                "Access-Control-Max-Age": "3600"}

    async def handle(self, r: Request,
                     database: DatabaseInterface) -> Response:
        response: Dict = {}
        status: int = CodeStatus.DELETE.value
        user_uid: Employee.uid = Serializer.get_user_uid_field_from_url(r)
        try:
            await executor.DeleteEmployee.exec(
                employee_uid=user_uid,
                database=database)

        except EmployeeNotFount:
            response = {"Err": ""}
            status = CodeStatus.CLIENT_ERR.value

        finally:
            return json_response(response, status=status,
                                 headers=self._headers)


class UpdateEmployee(HandlerInterface):
    _path = '/api/employees/{uid}'
    _headers = {"Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Methods": 'DELETE',
                "Access-Control-Allow-Headers": "X-Client-Header",
                "Access-Control-Max-Age": "3600"}

    async def handle(self, r: Request,
                     database: DatabaseInterface) -> Response:
        response: Dict = {}
        status: int = CodeStatus.PATCH.value
        body = await Serializer.read_body(r)
        try:
            new_employee: Dict = Serializer.get_employee_data_from_body(body)
            new_employee['uid'] = Serializer.get_user_uid_field_from_url(r)
            updated_employee: Dict = await executor.UpdateEmployee.exec(
                employee=new_employee,
                database=database
            )

            response = updated_employee

        except Exception as e:
            logger.error(e)
            response = {"Err": str(e)}
            status = CodeStatus.SERVER_ERR.value

        finally:
            return json_response(response, status=status,
                                 headers=self._headers)


class CreateEmployee(HandlerInterface):
    _path = '/api/employees/new'

    async def handle(self, r: Request,
                     database: DatabaseInterface) -> Response:
        body = await Serializer.read_post_data(r)
        response: Dict = {}
        status: int = CodeStatus.CREATE.value
        try:
            employee: dict = Serializer.get_employee_data_from_body(body)

            employee_uid: Employee.uid = await executor.CreateEmployee.exec(
                employee=employee,
                database=database
            )
            response = {"uid": employee_uid}

        except KeyError as e:
            logger.error(e)
            response = {"Err": str(e)}
            status = CodeStatus.CLIENT_ERR.value

        except Exception as e:
            logger.exception(e)
            response = {"Err": str(e)}
            status = CodeStatus.SERVER_ERR.value

        finally:
            return json_response(response, status=status)


class BasePage(HandlerInterface):
    _path = '/'

    @aiohttp_jinja2.template('index.html')
    async def handle(self, r: Request) -> Dict:
        pass

