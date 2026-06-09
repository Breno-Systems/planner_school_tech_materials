import streamlit as st
from utils import *

    # Configuração da página
st.set_page_config(page_title="Controle de Carrinhos", page_icon="🛒", layout="centered")

    # Inicializa o estado de autenticação
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.role = ""

if __name__ == "__main__":
    if not st.session_state.authenticated:
        login()
    elif st.session_state.role == "Administrador":
        app_admin()
    elif st.session_state.role == "Professor":
        app_professor()
    elif st.session_state.role == "Aluno":
        app_aluno()