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

                query = text("SELECT username, user_role FROM users WHERE user_login = :login LIMIT 1")
                row = session.execute(query, {"login": login}).fetchone()
                
                if row and row[1] in ("Administrador", "Professor", "Aluno"):
                    st.session_state.role = row[1]
                    st.session_state.username = row[0]

                st.success("Login bem-sucedido!")
                sleep(1.5)
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")


def app_admin(conn):

    st.title("Controle de Carrinhos - E.E.  Dom Lúcio Antunes")

        # Variáveis de ordenação e opções
    day_order = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]
    turmas_manha = ["6º A", "6º B", "6º C", "7º A", "7º B", "7º C", "8º A", "8º B", "8º C", "9º A", "9º B", "9º C"]
    turmas_tarde = ["1º A", "1º B", "2º ADM", "2º B", "3º ADM", "3º B"]
    dias = {"SEG": "Segunda-feira", "TER": "Terça-feira", "QUA": "Quarta-feira", "QUI": "Quinta-feira", "SEX": "Sexta-feira"}

        # Formulário de Entrada de Dados
    professor = st.text_input('Professor')
    periodo = st.selectbox('Período', ['Ensino Fundamental II - Manhã', 'Ensino Médio - Tarde'])
    aula = st.selectbox('Aula', ['1ª Aula', '2ª Aula', '3ª Aula', '4ª Aula', '5ª Aula', '6ª Aula', '7ª Aula', '8ª Aula'])
    
    if periodo == 'Ensino Fundamental II - Manhã':
        turma = st.selectbox('Turma', turmas_manha)
    else:
        turma = st.selectbox('Turma', turmas_tarde)
    
    dia = st.selectbox('Dia da Semana', list(dias.values()))

    if turma.startswith(("7º", "8º", "2º B", "3º B", "1º A")): # Verificar depois
        carrinho = st.selectbox('Carrinho', [1, 3])
    else:
        carrinho = st.selectbox('Carrinho', [2])

    

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
                AND periodo = :periodo
                AND aula = :aula
                LIMIT 1;
            """)
            
            with conn.session as session:
                conflito_existe = session.execute(
                    query_conflito, 
                    {"dia": dia, "carrinho": carrinho, "periodo": periodo, "aula": aula}
                ).fetchone()

            if conflito_existe:
                st.warning('Erro: Carrinho já reservado nesse horário!')
            else:
                # INSERT: Envelopado com text()
                query_insert = text("""
                    INSERT INTO reservas (dia, periodo, aula, carrinho, professor, turma)
                    VALUES (:dia, :periodo, :aula, :carrinho, :professor, :turma);
                """)
                with conn.session as session:
                    session.execute(
                        query_insert,
                        {
                            "dia": dia,
                            "periodo": periodo,
                            "aula": aula,
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
        query_select = text("SELECT dia, periodo, aula, carrinho, professor, turma FROM reservas;")
        
        with conn.session as session:
            result = session.execute(query_select)
            # Transforma o resultado do banco em um DataFrame do Pandas
            df_reservas = pd.DataFrame(result.fetchall(), columns=result.keys())
        
        if not df_reservas.empty:
            # Ajusta os nomes das colunas para visualização
            df_reservas.columns = ["Dia", "Período", "Aula", "Carrinho", "Professor", "Turma"]
            
            # Ordenação inteligente pelos dias da semana
            df_reservas["Dia"] = pd.Categorical(df_reservas["Dia"], categories=day_order, ordered=True)
            df_reservas = df_reservas.sort_values(["Dia", "Período", "Aula"]).reset_index(drop=True)
            
            st.subheader("Tabela de Reservas")
            st.dataframe(df_reservas, hide_index=True)
        else:
            st.info("Nenhuma reserva cadastrada ainda.")
            
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")

def app_professor(conn):
    st.title("Área do Professor - Em Desenvolvimento")
    st.info("Esta seção está em desenvolvimento. Por favor, aguarde futuras atualizações.")

def app_aluno(conn):

    st.title("Área do Aluno - Em Desenvolvimento")
    st.info("Esta seção está em desenvolvimento. Por favor, aguarde futuras atualizações.")

    day_order = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]

    # Exibição dos Dados (SELECT)
    try:
        # Usamos conn.session para rodar a query com text() de forma segura
        query_select = text("SELECT dia, periodo, aula, carrinho, professor, turma FROM reservas;")
        
        with conn.session as session:
            result = session.execute(query_select)
            # Transforma o resultado do banco em um DataFrame do Pandas
            df_reservas = pd.DataFrame(result.fetchall(), columns=result.keys())
        
        if not df_reservas.empty:
            # Ajusta os nomes das colunas para visualização
            df_reservas.columns = ["Dia", "Período", "Aula", "Carrinho", "Professor", "Turma"]
            
            # Ordenação inteligente pelos dias da semana
            df_reservas["Dia"] = pd.Categorical(df_reservas["Dia"], categories=day_order, ordered=True)
            df_reservas = df_reservas.sort_values(["Dia", "Período", "Aula"]).reset_index(drop=True)
            
            st.subheader("Tabela de Reservas")
            st.dataframe(df_reservas, hide_index=True)
        else:
            st.info("Nenhuma reserva cadastrada ainda.")
            
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")