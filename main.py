import streamlit as st
from utils import *

    # Configuração da página
st.set_page_config(page_title="Controle de Carrinhos", page_icon="🛒", layout="centered")

    # Inicializa o estado de autenticação
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""

    # Inicializa a conexão com o Neon
conn = st.connection("postgresql", type="sql")

if __name__ == "__main__":
    if not st.session_state.authenticated:
        login(conn)
    else:
        app_principal(conn)