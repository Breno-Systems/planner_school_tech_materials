import streamlit as st
import pandas as pd
from datetime import time

#Header

st.title("Controle de Carrinhos")

day_order = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]

df = pd.DataFrame(columns=[
    "Dia",
    "Horário de Retirada",
    "Horário de Entrega",
    "Carrinho",
    "Professor",
    "Turma"
]) 

if "reservas" not in st.session_state:
    st.session_state.reservas = df

turmas = ["6º A", "6º B", "6º C", "7º A", "7º B", "7º C", "8º A", "8º B", "8º C", "9º A", "9º B", "9º C"]

dias = {
    "SEG": "Segunda-feira",
    "TER": "Terça-feira",
    "QUA": "Quarta-feira",
    "QUI": "Quinta-feira",
    "SEX": "Sexta-feira"
}

professor = st.text_input('Professor')
turma = st.selectbox('Turma', turmas)
dia = st.selectbox('Dia da Semana', dias.values())

if turma.startswith(("7º", "8º")):
    carrinho = st.selectbox('Carrinho', [1, 3])
else:
    carrinho = st.selectbox('Carrinho', [2])

hora_retirada = st.time_input('Horário de Retirada', value=time(7, 0), step=300)
hora_entrega = st.time_input('Horário de Entrega', value=time(7, 45), step=300)

if st.button("Salvar"):

    conflito = (st.session_state.reservas["Dia"] == dia) & (st.session_state.reservas["Carrinho"] == carrinho) & (st.session_state.reservas["Horário de Retirada"] == hora_retirada)

    if professor == "":
        st.warning('Erro: Campo "Professor" está vazio')

    elif conflito.any():
        st.warning('Erro: Carrinho já reservado nesse horário')
    
    else:
        nova_linha = {
            "Dia": dia,
            "Horário de Retirada": hora_retirada,
            "Horário de Entrega": hora_entrega,
            "Carrinho": carrinho,
            "Professor": professor,
            "Turma": turma
        }
        linha_df = pd.DataFrame([nova_linha])
        st.session_state.reservas = pd.concat([st.session_state.reservas, linha_df], ignore_index=True)


if not st.session_state.reservas.empty:
    reservas = st.session_state.reservas.copy()
    reservas["Dia"] = pd.Categorical(reservas["Dia"], categories=day_order, ordered=True)
    reservas = reservas.sort_values(["Dia", "Horário de Retirada", "Turma"]).reset_index(drop=True)
    st.subheader("Tabela de Reservas")
    st.dataframe(reservas, hide_index=True)