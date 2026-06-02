import streamlit as st
import pandas as pd
from datetime import time

#Header

st.title("Controle de Carrinhos")

df = pd.DataFrame(columns=[
    "Dia",
    "Horário",
    "Carrinho",
    "Professor",
    "Turma"
])

turmas = ["6º A", "6º B", "6º C", "7º A", "7º B", "7º C", "8º A", "8º B", "8º C", "9º A", "9º B", "9º C"]
turmas_superiores = ["7º A", "7º B", "7º C", "8º A", "8º B", "8º C"]

dias = {
    "SEG": "Segunda-feira",
    "TER": "Terça-feira",
    "QUA": "Quarta-feira",
    "QUI": "Quinta-feira",
    "SEX": "Sexta-feira"
}

professor = st.text_input("Professor")
turma = st.selectbox("Turma", turmas)
dia = st.selectbox(
    "Dia da Semana", dias.values()
)

if turma in turmas_superiores:
    carrinho = st.selectbox("Carrinho", [1, 3])
else:
    carrinho = st.selectbox("Carrinho", [2])

hora_entrega = st.time_input("Horário de Retirada", value=time(7, 0), step=300)
hora_coleta = st.time_input("Horário de Entrega", value=time(7, 45), step=300)