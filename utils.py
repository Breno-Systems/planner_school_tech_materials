import streamlit as st
import pandas as pd
from datetime import time
from sqlalchemy import text
from time import sleep

def login(conn):
    st.title("Login")
    login = st.text_input("Nome de Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        query = text("SELECT 1 FROM users WHERE user_login = :login AND user_password = :senha LIMIT 1;")
        with conn.session as session:
            result = session.execute(query, {"login": login, "senha": senha}).fetchone()
            if result:
                st.session_state.authenticated = True

                query = text("SELECT username FROM users WHERE user_login = :login LIMIT 1")
                user_name = session.execute(query, {"login": login}).fetchone()[0]

                st.session_state.username = user_name
                st.success("Login bem-sucedido!")
                sleep(1.5)
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")


def app_principal(conn):

    st.title("Controle de Carrinhos")

        # Variáveis de ordenação e opções
    day_order = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]
    turmas = ["6º A", "6º B", "6º C", "7º A", "7º B", "7º C", "8º A", "8º B", "8º C", "9º A", "9º B", "9º C"]
    dias = {"SEG": "Segunda-feira", "TER": "Terça-feira", "QUA": "Quarta-feira", "QUI": "Quinta-feira", "SEX": "Sexta-feira"}

        # Formulário de Entrada de Dados
    professor = st.text_input('Professor')
    turma = st.selectbox('Turma', turmas)
    dia = st.selectbox('Dia da Semana', list(dias.values()))

    if turma.startswith(("7º", "8º")):
        carrinho = st.selectbox('Carrinho', [1, 3])
    else:
        carrinho = st.selectbox('Carrinho', [2])

    hora_retirada = st.time_input('Horário de Retirada', value=time(7, 0), step=300)
    hora_entrega = st.time_input('Horário de Entrega', value=time(7, 45), step=300)

    # Lógica para Salvar
    if st.button("Salvar"):
        if professor.strip() == "":
            st.warning('Erro: Campo "Professor" está vazio')
        else:
            # Caso de conflito   
            query_conflito = text("""
                SELECT 1 FROM reservas 
                WHERE dia = :dia 
                AND carrinho = :carrinho 
                AND horario_retirada = :hora_retirada
                LIMIT 1;
            """)
            
            with conn.session as session:
                conflito_existe = session.execute(
                    query_conflito, 
                    {"dia": dia, "carrinho": carrinho, "hora_retirada": hora_retirada}
                ).fetchone()

            if conflito_existe:
                st.warning('Erro: Carrinho já reservado nesse horário!')
            else:
                # INSERT: Envelopado com text()
                query_insert = text("""
                    INSERT INTO reservas (dia, horario_retirada, horario_entrega, carrinho, professor, turma)
                    VALUES (:dia, :hora_retirada, :hora_entrega, :carrinho, :professor, :turma);
                """)
                with conn.session as session:
                    session.execute(
                        query_insert,
                        {
                            "dia": dia,
                            "hora_retirada": hora_retirada,
                            "hora_entrega": hora_entrega,
                            "carrinho": carrinho,
                            "professor": professor,
                            "turma": turma
                        }
                    )
                    session.commit()
                st.success("Reserva salva com sucesso!")
                st.rerun()

    # Exibição dos Dados (SELECT)
    try:
        # Usamos conn.session para rodar a query com text() de forma segura
        query_select = text("SELECT dia, horario_retirada, horario_entrega, carrinho, professor, turma FROM reservas;")
        
        with conn.session as session:
            result = session.execute(query_select)
            # Transforma o resultado do banco em um DataFrame do Pandas
            df_reservas = pd.DataFrame(result.fetchall(), columns=result.keys())
        
        if not df_reservas.empty:
            # Ajusta os nomes das colunas para visualização
            df_reservas.columns = ["Dia", "Horário de Retirada", "Horário de Entrega", "Carrinho", "Professor", "Turma"]
            
            # Ordenação inteligente pelos dias da semana
            df_reservas["Dia"] = pd.Categorical(df_reservas["Dia"], categories=day_order, ordered=True)
            df_reservas = df_reservas.sort_values(["Dia", "Horário de Retirada", "Turma"]).reset_index(drop=True)
            
            st.subheader("Tabela de Reservas")
            st.dataframe(df_reservas, hide_index=True)
        else:
            st.info("Nenhuma reserva cadastrada ainda.")
            
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
