import requests
from typing import Optional, Dict, Any


class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.token: Optional[str] = None

    def set_token(self, token: str):
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def clear_token(self):
        self.token = None
        self.session.headers.pop("Authorization", None)

    def _handle_response(self, response: requests.Response) -> Any:
        if response.status_code == 401:
            raise requests.HTTPError("Необходима авторизация")
        if response.status_code == 404:
            raise requests.HTTPError("Ресурс не найден")
        if response.status_code >= 400:
            try:
                error_json = response.json()
                error_detail = error_json.get("detail") or error_json
            except Exception:
                error_detail = response.text
            raise requests.HTTPError(f"Ошибка {response.status_code}: {error_detail}")
        try:
            return response.json()
        except ValueError:
            return response.text

    def login(self, email: str, password: str) -> Dict[str, Any]:
        url = f"{self.base_url}/auth/login"
        payload = {"email": email, "password": password}
        resp = self.session.post(url, json=payload)
        return self._handle_response(resp)

    # create_user should follow UserCreate: first_name, last_name, patronymic?, email, password
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/users/"
        resp = self.session.post(url, json=user_data)
        return self._handle_response(resp)

    def update_current_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/users/update"
        resp = self.session.put(url, json=user_data)
        return self._handle_response(resp)

    def delete_current_user(self) -> Dict[str, Any]:
        url = f"{self.base_url}/users/delete"
        resp = self.session.delete(url)
        return self._handle_response(resp)

    def get_univariate_analysis(self, column: str) -> Dict[str, Any]:
        url = f"{self.base_url}/univariate/{column}"
        resp = self.session.get(url)
        return self._handle_response(resp)

    def get_categorical_analysis(self, column: str) -> Dict[str, Any]:
        url = f"{self.base_url}/univariate/categorial/{column}"
        resp = self.session.get(url)
        return self._handle_response(resp)

    def say_hello(self) -> Dict[str, Any]:
        url = f"{self.base_url}/data/say_hello"
        resp = self.session.get(url)
        return self._handle_response(resp)