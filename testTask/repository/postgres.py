from typing import Dict, List, Tuple

from loguru import logger
from psycopg import AsyncConnection

from testTask.repository.repository import DatabaseInterface, SQLCommand

import psycopg


class Postgres(DatabaseInterface):
    conn: AsyncConnection

    async def connect(self, *args, **kwargs):
        self.conn: AsyncConnection = await psycopg.AsyncConnection.connect(
            dbname=self.config_file.database,
            host=self.config_file.host,
            port=self.config_file.port,
            user=self.config_file.user,
            password=self.config_file.password
        )
        await self.conn.set_autocommit(True)

    async def disconnect(self, *args, **kwargs):
        await self.conn.close()

    async def execute(self, command: Tuple) -> List[Tuple] | List:
        result = []
        async with self.conn.cursor() as cur:
            await cur.execute(query=command[0], params=command[1])
            try:
                async for record in cur:
                    result.append(record)

            except Exception as e:
                logger.error(e)

            finally:
                return result


class CreateEmployee(SQLCommand):

    @classmethod
    def _init_command(cls, employee: Dict, *args, **kwargs):
        command = """
        INSERT INTO users 
        (name, salary, start_work_from, boss, position_key)
        values (%s, %s, %s, %s, %s) RETURNING id;
        """
        args = tuple(employee.values())
        cls.args_for_execute = (command, args,)

    def __new__(cls, *args, **kwargs):
        return super(CreateEmployee, cls).__new__(cls, *args, **kwargs)


class GetOneEmployee(SQLCommand):

    @classmethod
    def _init_command(cls, employee_uid: int, *args, **kwargs):
        command = f"SELECT * FROM users WHERE id = %s"
        args = (employee_uid,)
        cls.args_for_execute = (command, args, )

    def __new__(cls, *args, **kwargs):
        return super(GetOneEmployee, cls).__new__(cls, *args, **kwargs)


class GetManyEmployees(SQLCommand):

    @classmethod
    def _init_command(cls, limit: int, offset: int, *args, **kwargs):
        command: str = "SELECT * FROM USERS LIMIT %s OFFSET %s"
        args = (limit, offset)
        cls.args_for_execute = (command, args, )

    def __new__(cls, *args, **kwargs):
        return super(GetManyEmployees, cls).__new__(cls, *args, **kwargs)


class UpdateEmployee(SQLCommand):

    @classmethod
    def _init_command(cls, employee: Dict, *args, **kwargs):
        uid = employee.pop('uid')
        rows_to_update = ", ".join([f"{key}= %s" for key in employee.keys()])
        command = f"""
                    UPDATE users SET {rows_to_update} 
                    WHERE id=%s RETURNING *;
                    """
        args = (*employee.values(), uid,)
        cls.args_for_execute = (command, args,)

    def __new__(cls, *args, **kwargs):
        return super(UpdateEmployee, cls).__new__(cls, *args, **kwargs)


class DeleteEmployee(SQLCommand):

    @classmethod
    def _init_command(cls, uid: int, *args, **kwargs):
        command = "DELETE FROM users WHERE id=%s"
        args = (uid,)
        cls.args_for_execute = (command, args,)

    def __new__(cls, *args, **kwargs):
        return super(DeleteEmployee, cls).__new__(cls, *args, **kwargs)


class GetPosition(SQLCommand):

    @classmethod
    def _init_command(cls, position_id: int, *args, **kwargs):
        command = f"SELECT name FROM positions WHERE id=%s"
        args = (position_id,)
        cls.args_for_execute = (command, args)

    def __new__(cls, *args, **kwargs):
        return super(GetPosition, cls).__new__(cls, *args, **kwargs)
