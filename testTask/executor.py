from abc import ABC, abstractmethod
from typing import List, Dict, Tuple

from testTask.exceptions.exployee import EmployeeNotFount
from testTask.models.employee import Employee
from testTask.repository.repository import DatabaseInterface
from testTask.repository import postgres


class ExecutorInterface(ABC):

    @staticmethod
    @abstractmethod
    async def exec(*args, **kwargs):
        pass

    @classmethod
    def _result_to_employee_dict(cls, result: Tuple) -> Dict:
        employee: Dict = {
            key: value
            for key, value in zip(Employee.__match_args__, result)
        }
        return employee


class GetOneEmployee(ExecutorInterface):

    @classmethod
    async def exec(cls, database: DatabaseInterface, employee_uid: int,
                   *args, **kwargs) -> Dict:
        command: Tuple = postgres.GetOneEmployee(employee_uid=employee_uid)
        result: List[Tuple] = await database.execute(command)
        if result:
            return cls._result_to_employee_dict(result=result[0])

        raise EmployeeNotFount


class GetManyEmployees(ExecutorInterface):

    @classmethod
    async def exec(cls, database: DatabaseInterface, limit: int, offset: int,
                   *args, **kwargs) -> List[Dict]:
        command: Tuple = postgres.GetManyEmployees(limit=limit, offset=offset)
        employees: List[Dict] = []
        result: List[Tuple] = await database.execute(command)
        if result:
            employees.extend([cls._result_to_employee_dict(r) for r in result])
        return employees


class UpdateEmployee(ExecutorInterface):

    @classmethod
    async def exec(cls, database: DatabaseInterface, employee: Dict,
                   *args, **kwargs) -> Dict:
        command: Tuple = postgres.UpdateEmployee(employee=employee)
        result = await database.execute(command)
        if result:
            return cls._result_to_employee_dict(result[0])

        raise EmployeeNotFount


class CreateEmployee(ExecutorInterface):

    @staticmethod
    async def exec(database: DatabaseInterface, employee: Dict,
                   *args, **kwargs) -> int:
        command: Tuple = postgres.CreateEmployee(employee=employee)
        result = await database.execute(command)
        return result[0][0]


class DeleteEmployee(ExecutorInterface):
    @staticmethod
    async def exec(database: DatabaseInterface, employee_uid: int,
                   *args, **kwargs) -> None:
        command: Tuple = postgres.DeleteEmployee(uid=employee_uid)
        await database.execute(command)


class GetPosition(ExecutorInterface):

    @staticmethod
    async def exec(database: DatabaseInterface, position_id: int,
                   *args, **kwargs) -> str:
        command = postgres.GetPosition(position_id=position_id)
        result = await database.execute(command)
        if result:
            return result[0][0]
