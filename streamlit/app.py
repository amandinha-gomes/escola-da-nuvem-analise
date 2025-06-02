# import streamlit as st
# import pandas as pd
# import altair as alt

# # **1. Chame o st.set_page_config primeiro**
# st.set_page_config(
#     page_title="Projeto Extensor - Escola da Nuvem",
#     page_icon="📊",
#     layout="wide"
# )

# # Função para carregar os dados
# @st.cache_data
# def load_data():
#     df = pd.read_csv('alunos_pii_none.csv')


#     return df

# # Função para agrupar escolaridade
# def group_escolaridade(df):
#     grupos = {
#         'Pós-graduação': ['Pós graduação', 'MBA', 'Mestrado', 'Pós-graduação'],
#         'Ensino Superior': ['Superior Completo', 'Graduação'],
#         'Ensino Médio': ['Ensino Médio Completo'],
#         'Ensino Fundamental': ['Ensino Fundamental Completo', 'Fundamental'],
#         'Outros': ['Outro', 'Não Especificado']
#     }
#     for nova, antigas in grupos.items():
#         df['Escolaridade'] = df['Escolaridade'].replace(antigas, nova)
#     return df

# # Gráfico com Altair
# def plot_escolaridade(df):
#     df = group_escolaridade(df)
#     contagem = df['Escolaridade'].value_counts(normalize=True) * 100
#     df_plot = contagem.reset_index()
#     df_plot.columns = ['Escolaridade', 'Porcentagem']

#     chart = alt.Chart(df_plot).mark_bar().encode(
#         x=alt.X('Escolaridade:N', sort='-y'),
#         y=alt.Y('Porcentagem:Q'),
#         tooltip=['Escolaridade', alt.Tooltip('Porcentagem:Q', format='.2f')]
#     ).properties(
#         width=600,
#         height=400,
#         title="Distribuição por Nível de Escolaridade"
#     )

#     st.altair_chart(chart, use_container_width=True)
#     df_plot['Porcentagem'] = df_plot['Porcentagem'].map(lambda x: f"{x:.2f}%")
#     st.dataframe(df_plot)

# # Página inicial
# def pagina_inicio():
#     st.title("📘 Projeto Extensor - Escola da Nuvem")
#     st.write("Bem-vindo à plataforma de análise dos dados da Escola da Nuvem.")
#     with st.expander("📊 Visualizar gráfico de escolaridade"):
#         df = load_data()
#         plot_escolaridade(df)
#     if st.button("Ir para página de alunos"):
#         st.session_state.pagina = "Alunos"
#         st.experimental_rerun()

# # Página de análise de alunos
# def pagina_alunos():
#     st.title("👨‍🎓 Análise de Alunos")
#     st.write("Explore o perfil dos alunos e distribuições.")
#     df = load_data()
#     plot_escolaridade(df)

# # # Sidebar de navegação
# # # st.sidebar.image("img/logo.png", width=80)

# st.sidebar.header("Navegação")
# opcao = st.sidebar.selectbox("Escolha uma página", ["Início", "Alunos"])

# # Renderização condicional
# if opcao == "Início":
#     pagina_inicio()
# else:
#     pagina_alunos()


# # import streamlit as st
# # import pandas as pd
# # import altair as alt

# # # Configurações da página
# # st.set_page_config(
# #     page_title="Projeto Extensor - Escola da Nuvem",
# #     page_icon="📊",
# #     layout="wide"
# # )

# # # Função para carregar os dados
# # @st.cache_data
# # def load_data():
# #     df = pd.read_csv('alunos_pii_none.csv', engine='openpyxl')
# #     return df

# # # Função para agrupar escolaridade
# # def group_escolaridade(df):
# #     grupos = {
# #         'Pós-graduação': ['Pós graduação', 'MBA', 'Mestrado', 'Pós-graduação'],
# #         'Ensino Superior': ['Superior Completo', 'Graduação'],
# #         'Ensino Médio': ['Ensino Médio Completo'],
# #         'Ensino Fundamental': ['Ensino Fundamental Completo', 'Fundamental'],
# #         'Outros': ['Outro', 'Não Especificado']
# #     }
# #     for nova, antigas in grupos.items():
# #         df['Escolaridade'] = df['Escolaridade'].replace(antigas, nova)
# #     return df

# # # Função para plotar o gráfico de Escolaridade com Altair
# # def plot_escolaridade(df):
# #     df = group_escolaridade(df)
# #     contagem = df['Escolaridade'].value_counts(normalize=True) * 100
# #     df_plot = contagem.reset_index()
# #     df_plot.columns = ['Escolaridade', 'Porcentagem']

# #     chart = alt.Chart(df_plot).mark_bar().encode(
# #         x=alt.X('Escolaridade:N', sort='-y'),
# #         y=alt.Y('Porcentagem:Q'),
# #         tooltip=['Escolaridade', alt.Tooltip('Porcentagem:Q', format='.2f')]
# #     ).properties(
# #         width=600,
# #         height=400,
# #         title="Distribuição por Nível de Escolaridade"
# #     )

# #     st.altair_chart(chart, use_container_width=True)
# #     df_plot['Porcentagem'] = df_plot['Porcentagem'].map(lambda x: f"{x:.2f}%")
# #     st.dataframe(df_plot)

# # # Página de Matrículas
# # def pagina_matricula():
# #     st.title("📑 Análise de Matrículas")
# #     st.write("""
# #     Vamos explorar as **matrículas** realizadas na Escola da Nuvem ao longo dos anos.
# #     Utilizaremos gráficos dinâmicos e filtros para explorar os dados de maneira interativa.
# #     """)

# #     # Filtro interativo para o ano
# #     ano = st.selectbox("Escolha o ano", ['2023', '2022', '2021', '2020'])
    
# #     # Filtro interativo para o curso
# #     curso = st.selectbox("Escolha o curso", ['Curso A', 'Curso B', 'Curso C'])
    
# #     df = load_data()  # Carregar os dados
# #     df = df[df['Ano'] == int(ano)]  # Filtrar pelo ano

# #     # Mostrar o total de matrículas por curso
# #     matriculas_por_curso = df[df['Curso'] == curso].shape[0]
# #     st.write(f"Total de matrículas para o curso {curso} em {ano}: {matriculas_por_curso}")
    
# #     # Exibir gráfico de matrícula por curso
# #     matriculas_df = df['Curso'].value_counts().reset_index()
# #     matriculas_df.columns = ['Curso', 'Total de Matrículas']
    
# #     chart = alt.Chart(matriculas_df).mark_bar().encode(
# #         x=alt.X('Curso:N', sort='-y', title="Cursos"),
# #         y=alt.Y('Total de Matrículas:Q', title="Número de Matrículas"),
# #         tooltip=['Curso', 'Total de Matrículas']
# #     ).properties(
# #         width=600,
# #         height=400,
# #         title="Distribuição de Matrículas por Curso"
# #     )
    
# #     st.altair_chart(chart, use_container_width=True)

# # # Página de Processo Seletivo
# # def pagina_processo_seletivo():
# #     st.title("📋 Análise do Processo Seletivo")
# #     st.write("""
# #     Nessa página, você pode explorar os dados dos candidatos que participaram do **processo seletivo** da Escola da Nuvem.
# #     Utilize os filtros abaixo para visualizar o desempenho dos candidatos.
# #     """)

# #     # Filtro interativo para nota de corte
# #     nota_corte = st.slider("Selecione a nota de corte", 0, 10, 7)
    
# #     # Filtro interativo para faixa etária
# #     faixa_etaria = st.selectbox("Escolha a faixa etária", ['18-25', '26-35', '36-45', '46+'])
    
# #     df = load_data()  # Carregar os dados
# #     df = df[df['Nota'] >= nota_corte]  # Filtrar por nota de corte
# #     df = df[df['Faixa Etaria'] == faixa_etaria]  # Filtrar por faixa etária
    
# #     # Mostrar o número de candidatos aprovados
# #     aprovados = df[df['Status'] == 'Aprovado'].shape[0]
# #     reprovados = df[df['Status'] == 'Reprovado'].shape[0]
# #     st.write(f"Total de candidatos aprovados: {aprovados}")
# #     st.write(f"Total de candidatos reprovados: {reprovados}")
    
# #     # Exibir gráfico de desempenho
# #     desempenho_df = df.groupby('Status')['Nota'].mean().reset_index()
    
# #     chart = alt.Chart(desempenho_df).mark_bar().encode(
# #         x=alt.X('Status:N', title="Status"),
# #         y=alt.Y('Nota:Q', title="Média das Notas"),
# #         color='Status:N',
# #         tooltip=['Status', 'Nota']
# #     ).properties(
# #         width=600,
# #         height=400,
# #         title="Desempenho dos Candidatos por Status"
# #     )

# #     st.altair_chart(chart, use_container_width=True)

# # # Mapeamento das páginas
# # page_names_to_funcs = {
# #     "Matrículas": pagina_matricula,
# #     "Processo Seletivo": pagina_processo_seletivo
# # }

# # # Sidebar de navegação
# # # st.sidebar.image("img/logo.png", width=80)
# # st.sidebar.header("Navegação")
# # opcao = st.sidebar.selectbox("Escolha uma visualização", page_names_to_funcs.keys())

# # # Renderização condicional
# # page_names_to_funcs[opcao]()

# # ----------------------------------------------------------------------------------------------------------

import streamlit as st
import pandas as pd
import altair as alt

# Configurações da página
st.set_page_config(
    page_title="Projeto Extensor - Escola da Nuvem",
    page_icon="📊",
    layout="wide"
)

# Função para carregar os dados
@st.cache_data
def load_data():
    # Agora usamos read_csv para carregar o arquivo CSV
    df = pd.read_csv('projeto_integrador/alunos_pii_none.csv', engine='python', sep=';', on_bad_lines='skip')  # Certifique-se de que o caminho do arquivo está correto
    return df

# Função para agrupar escolaridade
def group_escolaridade(df):
    grupos = {
        'Pós-graduação': ['Pós graduação', 'MBA', 'Mestrado', 'Pós-graduação'],
        'Ensino Superior': ['Superior Completo', 'Graduação'],
        'Ensino Médio': ['Ensino Médio Completo'],
        'Ensino Fundamental': ['Ensino Fundamental Completo', 'Fundamental'],
        'Outros': ['Outro', 'Não Especificado']
    }
    for nova, antigas in grupos.items():
        df['Escolaridade'] = df['Escolaridade'].replace(antigas, nova)
    return df

# Função para plotar o gráfico de Escolaridade com Altair
def plot_escolaridade(df):
    df = group_escolaridade(df)
    contagem = df['Escolaridade'].value_counts(normalize=True) * 100
    df_plot = contagem.reset_index()
    df_plot.columns = ['Escolaridade', 'Porcentagem']

    chart = alt.Chart(df_plot).mark_bar().encode(
        x=alt.X('Escolaridade:N', sort='-y'),
        y=alt.Y('Porcentagem:Q'),
        tooltip=['Escolaridade', alt.Tooltip('Porcentagem:Q', format='.2f')]
    ).properties(
        width=600,
        height=400,
        title="Distribuição por Nível de Escolaridade"
    )

    st.altair_chart(chart, use_container_width=True)
    df_plot['Porcentagem'] = df_plot['Porcentagem'].map(lambda x: f"{x:.2f}%")
    st.dataframe(df_plot)

# Página de Matrículas
def pagina_matricula():
    st.title("📑 Análise de Matrículas")
    st.write("""
    Vamos explorar as **matrículas** realizadas na Escola da Nuvem ao longo dos anos.
    Utilizaremos gráficos dinâmicos e filtros para explorar os dados de maneira interativa.
    """)

    # Filtro interativo para o ano
    ano = st.selectbox("Escolha o ano", ['2023', '2022', '2021', '2020'])
    
    # Filtro interativo para o curso
    curso = st.selectbox("Escolha o curso", ['Curso A', 'Curso B', 'Curso C'])
    
    df = load_data()  # Carregar os dados
    # df = df[df['Ano'] == int(ano)]  # Filtrar pelo ano

    # Mostrar o total de matrículas por curso
    # matriculas_por_curso = df[df['Curso'] == curso].shape[0]
    # st.write(f"Total de matrículas para o curso {curso} em {ano}: {matriculas_por_curso}")
    
    # # Exibir gráfico de matrícula por curso
    # matriculas_df = df['Curso'].value_counts().reset_index()
    # matriculas_df.columns = ['Curso', 'Total de Matrículas']
    
    # chart = alt.Chart(matriculas_df).mark_bar().encode(
    #     x=alt.X('Curso:N', sort='-y', title="Cursos"),
    #     y=alt.Y('Total de Matrículas:Q', title="Número de Matrículas"),
    #     tooltip=['Curso', 'Total de Matrículas']
    # ).properties(
    #     width=600,

    #     height=400,
    #     title="Distribuição de Matrículas por Curso"
    # )
    
    # st.altair_chart(chart, use_container_width=True)
    

# Página de Processo Seletivo
def pagina_processo_seletivo():
    st.title("📋 Análise do Processo Seletivo")
    st.write("""
    Nessa página, você pode explorar os dados dos candidatos que participaram do **processo seletivo** da Escola da Nuvem.
    Utilize os filtros abaixo para visualizar o desempenho dos candidatos.
    """)

    # Filtro interativo para nota de corte
    nota_corte = st.slider("Selecione a nota de corte", 0, 10, 7)
    
    # Filtro interativo para faixa etária
    faixa_etaria = st.selectbox("Escolha a faixa etária", ['18-25', '26-35', '36-45', '46+'])
    
    df = load_data()  # Carregar os dados
    df = df[df['Nota'] >= nota_corte]  # Filtrar por nota de corte
    df = df[df['Faixa Etaria'] == faixa_etaria]  # Filtrar por faixa etária
    
    # Mostrar o número de candidatos aprovados
    aprovados = df[df['Status'] == 'Aprovado'].shape[0]
    reprovados = df[df['Status'] == 'Reprovado'].shape[0]
    st.write(f"Total de candidatos aprovados: {aprovados}")
    st.write(f"Total de candidatos reprovados: {reprovados}")
    
    # Exibir gráfico de desempenho
    desempenho_df = df.groupby('Status')['Nota'].mean().reset_index()
    
    chart = alt.Chart(desempenho_df).mark_bar().encode(
        x=alt.X('Status:N', title="Status"),
        y=alt.Y('Nota:Q', title="Média das Notas"),
        color='Status:N',
        tooltip=['Status', 'Nota']
    ).properties(
        width=600,
        height=400,
        title="Desempenho dos Candidatos por Status"
    )

    st.altair_chart(chart, use_container_width=True)

# Mapeamento das páginas
page_names_to_funcs = {
    "Matrículas": pagina_matricula,
    "Processo Seletivo": pagina_processo_seletivo
}

# Sidebar de navegação
# st.sidebar.image("img/logo.png", width=80)
st.sidebar.header("Navegação")
opcao = st.sidebar.selectbox("Escolha uma visualização", page_names_to_funcs.keys())

# Renderização condicional
page_names_to_funcs[opcao]()


import requests
import pandas as pd

# Link compartilhado do Google Drive
url = "https://colab.research.google.com/drive/1RgPLD2Wik5tUy3PavdKzQEATp6g2poP5?usp=sharing"  # Substitua "FILE_ID" pelo ID do seu arquivo

# Baixando o arquivo diretamente
r = requests.get(url)
with open("alunos_pii_none.csv", "wb") as f:
    f.write(r.content)

# Carregando os dados do arquivo CSV
df = pd.read_csv("alunos_pii_none.csv")


import streamlit as st
import pandas as pd
import requests

# Função para baixar o arquivo CSV do Google Drive
def download_file_from_google_drive(url, filename):
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)

# Função para carregar os dados CSV
@st.cache_data
def load_data():
    file_url = "https://colab.research.google.com/drive/1RgPLD2Wik5tUy3PavdKzQEATp6g2poP5?usp=sharing"  # Substitua pelo ID do seu arquivo
    file_path = "alunos_pii_none.csv"
    
    # Baixando o arquivo do Google Drive
    download_file_from_google_drive(file_path)
    
    # Carregar os dados do CSV
    df = pd.read_csv(file_path)
    return df

# Função para mostrar a Situação de Emprego Atual
def situacao_emprego(df):
    situacao_emprego = df['Situação de Emprego Atual'].value_counts()
    st.write("### Situação de Emprego Atual dos Alunos:")
    st.write(situacao_emprego)

# Função para a página inicial
def pagina_inicio():
    st.title("Projeto Escola da Nuvem")
    st.write("Analisando dados de matrículas, escolaridade e situação de emprego atual.")
    
    # Carregar os dados
    df = load_data()

    # Exibir a Situação de Emprego Atual
    situacao_emprego(df)

# Página principal de navegação
def main():
    pagina_inicio()

if __name__ == "__main__":
    main()

