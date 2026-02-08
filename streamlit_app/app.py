import streamlit as st
from utils.session_state import SessionState
from utils.api_client import APIClient


SessionState.initialize()

if "auth_view" not in st.session_state:
    st.session_state.auth_view = "login"


def registration_form(client: APIClient):
    st.header("Регистрация")
    with st.form("register_form", clear_on_submit=False):
        first_name  = st.text_input("Имя")
        last_name   = st.text_input("Фамилия")
        patronymic  = st.text_input("Отчество (необязательно)")
        email       = st.text_input("Email")
        password    = st.text_input("Пароль", type="password")
        submitted   = st.form_submit_button("Зарегистрироваться")

    if submitted:
        if not all([first_name, last_name, email, password]):
            st.error("Заполните обязательные поля: имя, фамилия, email, пароль")
            return

        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
        }
        if patronymic.strip():
            payload["patronymic"] = patronymic.strip()

        try:
            client.create_user(payload)
            st.success("Регистрация прошла успешно")
            st.info("Теперь можете войти")
            st.session_state.auth_view = "login"
            st.rerun()
        except Exception as e:
            st.error(f"Ошибка регистрации: {e}")


def login_form(client: APIClient):
    st.header("Вход")
    with st.form("login_form", clear_on_submit=False):
        email     = st.text_input("Email")
        password  = st.text_input("Пароль", type="password")
        submitted = st.form_submit_button("Войти")

    if submitted:
        if not (email and password):
            st.error("Введите email и пароль")
            return

        try:
            result = client.login(email=email, password=password)
            token = result.get("access_token") or result.get("token")
            if not token:
                st.error("Сервер не вернул токен")
                return

            SessionState.set_authenticated(token)
            st.success("Вход выполнен")
            st.rerun()
        except Exception as e:
            st.error(f"Ошибка входа: {str(e)}")

if not SessionState.is_authenticated():
    st.set_page_config(page_title="Авторизация", layout="centered")

    client = APIClient()

    tab_login, tab_reg = st.tabs(["Вход", "Регистрация"])

    with tab_login:
        login_form(client)

    with tab_reg:
        registration_form(client)

    with st.expander("Отладочная информация"):
        st.caption(f"API base URL: {client.base_url}")

else:
    st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")

    with st.sidebar:
        if st.button("Выйти", type="primary"):
            SessionState.logout()
            st.rerun()
