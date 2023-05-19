import requests
from django.conf import settings
from rest_framework import status


class UserAPI:
    headers = None

    def setup(self) -> None:
        if self.headers != None:
            return

        response = requests.post(
            f'{settings.USER_API_URL}token/',
            data=settings.USER_API_AUTHENTICATION
        )

        if response.status_code != status.HTTP_200_OK:
            return
        
        token = response.json()['token']
        self.headers = {
            'Authorization': f'Token {token}',
        }

    def filter_user_by_cpf(self, cpf) -> dict:
        try:
            self.setup()
            response = requests.get(f'{settings.USER_API_URL}user/?cpf={cpf}', headers=self.headers)
            if response.status_code != status.HTTP_200_OK:
                print(f"Problems do conect User Api response: {response}")
                return
            return response.json()
        except:
            return None
