from typing import Optional
import streamlit as st


class SessionState:
    @staticmethod
    def initialize():
        if 'token' not in st.session_state:
            st.session_state.token = None
        if 'is_authenticated' not in st.session_state:
            st.session_state.is_authenticated = False

    @staticmethod
    def set_authenticated(token: str):
        st.session_state.token = token
        st.session_state.is_authenticated = True

    @staticmethod
    def logout():
        st.session_state.token = None
        st.session_state.is_authenticated = False

    @staticmethod
    def get_token() -> Optional[str]:
        return st.session_state.token

    @staticmethod
    def is_authenticated() -> bool:
        return st.session_state.is_authenticated