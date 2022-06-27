from typing import Dict

from aiohttp.abc import Request

from testTask.models.employee import Employee


class Serializer:

    @staticmethod
    async def read_body(r: Request) -> Dict:
        return await r.json() if r.can_read_body else {}

    @staticmethod
    async def read_post_data(r: Request) -> Dict:
        return dict(await r.post())

    @staticmethod
    def get_offset_field_from_body(body: Dict) -> int:
        return body.get('offset', 0)

    @staticmethod
    def get_limit_field_from_body(body: Dict) -> int:
        return body.get('limit', 10)

    @staticmethod
    def get_employee_data_from_body(body: Dict) -> Dict:
        employee: Dict = {}
        for key, value in body.items():
            if key in Employee.__match_args__:
                employee[key] = value
        return employee

    @staticmethod
    def get_user_uid_field_from_url(r: Request) -> int:
        user_id: Employee.uid = r.match_info.get('uid', 0)
        return int(user_id)

    @staticmethod
    def convert_dict_to_employee_type(employee: Dict):
        return Employee(**employee)
