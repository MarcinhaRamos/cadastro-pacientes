import streamlit as st
import pandas as pd
from datetime import datetime


COLUNAS = [
    "timestamp",
    "nome",
    "idade",
    "convenio",
    "prioridade",
    "motivo"
]


# Configuração da página
st.set_page_config(
    page_title="Cadastro de Pacientes",
    page_icon="🏥",
    layout="centered"
)


# Título
st.title("🏥 Cadastro de Pacientes")
st.write("Preencha os dados abaixo para cadastrar um paciente.")


# Cria a lista de pacientes na sessão
if "pacientes" not in st.session_state:
    st.session_state.pacientes = pd.DataFrame(
        columns=COLUNAS
    )


# Formulário
with st.form("cadastro"):

    nome = st.text_input(
        "Nome do paciente",
        placeholder="Digite o nome completo"
    )

    idade = st.number_input(
        "Idade",
        min_value=0,
        max_value=120,
        step=1
    )

    convenio = st.selectbox(
        "Convênio",
        [
            "Particular",
            "Unimed",
            "Bradesco Saúde",
            "SulAmérica",
            "Outro"
        ]
    )

    prioridade = st.slider(
        "Prioridade do atendimento",
        min_value=1,
        max_value=5,
        value=1
    )

    motivo = st.text_area(
        "Motivo da consulta / observações",
        placeholder="Digite o motivo da consulta ou outras observações"
    )

    enviado = st.form_submit_button("Cadastrar")


# Quando o botão Cadastrar for pressionado
if enviado:

    if not nome.strip():

        st.error("Informe o nome do paciente.")

    else:

        nova_linha = {
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "nome": nome,
            "idade": idade,
            "convenio": convenio,
            "prioridade": prioridade,
            "motivo": motivo
        }

        novo_paciente = pd.DataFrame(
            [nova_linha]
        )

        st.session_state.pacientes = pd.concat(
            [
                st.session_state.pacientes,
                novo_paciente
            ],
            ignore_index=True
        )

        st.success(
            "Paciente cadastrado com sucesso!"
        )


# Mostra os pacientes cadastrados
if not st.session_state.pacientes.empty:

    st.subheader(
        "Últimos pacientes cadastrados"
    )

    st.dataframe(
        st.session_state.pacientes.tail(5),
        use_container_width=True,
        hide_index=True
    )


    # Cria o arquivo CSV para download
    csv = st.session_state.pacientes.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        label="📥 Baixar CSV",
        data=csv,
        file_name="pacientes.csv",
        mime="text/csv"
    )
    