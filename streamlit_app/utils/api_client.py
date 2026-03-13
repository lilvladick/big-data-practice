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

    def _request(self, method: str, path: str, params: Optional[Dict] = None, json: Optional[Dict] = None) -> Any:

        url = f"{self.base_url}{path}"

        response = self.session.request(method=method, url=url, params=params, json=json)

        return self._handle_response(response)

    def _get(self, path: str, params: Optional[Dict] = None):
        return self._request("GET", path, params=params)

    def _post(self, path: str, json: Optional[Dict] = None):
        return self._request("POST", path, json=json)

    def _put(self, path: str, json: Optional[Dict] = None):
        return self._request("PUT", path, json=json)

    def _delete(self, path: str):
        return self._request("DELETE", path)

    @staticmethod
    def _handle_response(response: requests.Response) -> Any:

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

    def login(self, email: str, password: str):

        return self._post("/auth/login", json={"email": email, "password": password})

    def create_user(self, user_data: Dict[str, Any]):
        return self._post("/users/", json=user_data)

    def update_current_user(self, user_data: Dict[str, Any]):
        return self._put("/users/update", json=user_data)

    def delete_current_user(self):
        return self._delete("/users/delete")

    def get_univariate_analysis(self, column: str):
        return self._get(f"/univariate/{column}")

    def get_categorical_analysis(self, column: str):
        return self._get(f"/univariate/categorial/{column}")

    def say_hello(self):
        return self._get("/data/say_hello")

    def knn_classification(self, target_column: str, feature_columns: list, k: int = 5, test_size: float = 0.25):

        params = {
            "feature_columns": feature_columns,
            "k": k,
            "test_size": test_size
        }

        return self._get(f"/multivariate/knn_class/{target_column}", params=params)

    def automl_classification(self, target_column: str, feature_columns: list, test_size: float = 0.25,
                              n_select: int = 5):

        params = {
            "feature_columns": feature_columns,
            "test_size": test_size,
            "n_select": n_select
        }

        return self._get(f"/multivariate/automl/{target_column}", params=params)
