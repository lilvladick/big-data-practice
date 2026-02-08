import streamlit as st
from utils.session_state import SessionState
from utils.api_client import APIClient

st.title("Настройки")

client = APIClient()
client.set_token(SessionState.get_token())

tab_update, tab_delete = st.tabs(["Обновить себя", "Удалить себя"])


with tab_update:
    st.subheader("Обновление своих данных")
    with st.form("update_self_form"):
        new_fn   = st.text_input("Новое имя", key="up_fn")
        new_ln   = st.text_input("Новая фамилия", key="up_ln")
        new_pt   = st.text_input("Новое отчество", key="up_pt")
        new_email= st.text_input("Новый email", key="up_email")
        is_active= st.selectbox("Статус активности", [None, True, False], key="up_active")
        new_pwd  = st.text_input("Новый пароль (если нужно)", type="password", key="up_pwd")
        submitted= st.form_submit_button("Обновить")

    if submitted:
        payload = {}
        if new_fn:    payload["first_name"] = new_fn
        if new_ln:    payload["last_name"]  = new_ln
        if new_pt:    payload["patronymic"] = new_pt
        if new_email: payload["email"]      = new_email
        if is_active is not None: payload["is_active"] = is_active
        if new_pwd:   payload["password"]   = new_pwd

        if not payload:
            st.warning("Измените хотя бы одно поле")
        else:
            try:
                result = client.update_current_user(payload)
                st.success("Данные обновлены")
                if result:
                    st.json(result)
            except Exception as e:
                st.error(f"Ошибка обновления: {e}")

with tab_delete:
    st.subheader("Удаление аккаунта")
    st.warning("Действие **необратимо**.")
    confirm = st.checkbox("Я понимаю, что аккаунт будет удалён навсегда")
    if st.button("Удалить мой аккаунт", type="primary", disabled=not confirm):
        try:
            client.delete_current_user()
            st.success("Аккаунт удалён")
            SessionState.logout()
            st.rerun()
        except Exception as e:
            st.error(f"Ошибка удаления: {e}")