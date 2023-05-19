from typing import Dict

from common.redis import Cache
from common.user_api import UserAPI


class OrderService:
    cache = Cache()
    user_api = UserAPI()

    async def get_user_id_by_cpf(self, cpf: str) -> int:
        id_user_api = await self.cache.get_cache(cpf)

        if not id_user_api:
            user_api_data = self.user_api.filter_user_by_cpf(cpf)
            id_user_api = self._get_id_user_api(user_api_data)
            if id_user_api:
                await self.cache.create_cache(cpf, id_user_api)

        return id_user_api

    def _get_id_user_api(self, user_api: Dict) -> int:
        if not user_api:
            return
        if user_api['count'] == 0:
            return

        return user_api['results'][0]['id']

    def is_valid_search_user_id(self, data: Dict) -> bool:
        if not data.get('cpf'):
            return False

        if data.get('user_id'):
            return False

        return True
