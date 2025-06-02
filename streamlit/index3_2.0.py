import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from rapidfuzz import fuzz

# --- Carregamento de dados ---
@st.cache_data
def load_data():
    df = pd.read_csv('alunos_pii_none.csv', delimiter=';', header=None, on_bad_lines='skip')
    return df

@st.cache_data
def load_excel_data():
    df = pd.read_excel('matriculas_modificada.xlsx', sheet_name='Planilha2')
    return df

@st.cache_data
def df_processos():
    return pd.read_excel('processos_seletivos_pii_none.xlsx')


# --- Categorias e sinônimos ---
categorias = {
    'Indisponibilidade de datas e horários': [
        'não tenho disponibilidade nesse horário',
        'indisponibilidade de tempo',
        'horário',
        'não tenho disponibilidade',
        'horário noturno indisponível',
        'trabalho durante a noite',
        'os dias não são compativel',
        'não consigo particitar todas as segundas',
        'só tenho terça-feira livre, não posso na segunda-feira',
        'por enquanto não posso fazer aulas as segundas à noite',
        'o motivo é porque nas segundas tenho aulas de inglês das 19h até 20h',
        'não conseguiria ver as aulas por conta que faço faculdade no turno da tarde/noite',
        'infelizmente eu trabalho das 22:30 às 6:02. seria impossível comparecer às aulas',
        'não consigo estar presente no horário',
        'no momento, não consigo estar presente em todos os dias das aulas ao vivo',
        'infelizmente nao consigo dispor desse tempo durante 4 dias x 16 semanas',
        'tenho compromissos nas quartas Feiras apartir das 19:00.',
        'Dias da aula não conciliam com  o trabalho',
        'As terças a noite já tenho compromisso neste ano e mudar agora me atrapalha',
        'Consegui uma bolsa gratuita na ProZ de programação que tem aulas on line justamente na segunda e na quarta feira.\nNão posso perder essa oportunidade. Posso ficar com o curso de terça e quinta na escola da nuvem?',
        'Dias alternados pois trabalho em alguns dias específicos \n\nSe for dias estabelecidos \n\nExemplo\n\nSegunda quarta sexta tranquilo em.faze',
        'estou com uma agente cheia ate outubro'
    ],
    'Iniciar pelos fundamentos': [
        'quero começar pelo fundamentos aws',
        'gostaria de começar pelo básico, para ter uma boa base',
        'desejo o fundamental no momento',
        'gostaria de participar do fundamentos aws',
        'prefiro a turma de fundamentos',
        'poís quero o de aws',
        'queria fazer o iniciante mesmo',
        'agora tenho mais interesse em tirar o certificado básico para a minha carreira de desenvolvedor',
        'quero aprender do começo, tenho pouca experiência',
        'não tenho certeza se conseguiria acompanhar o restante da turma, prefiro começar com o básico e me habituar com os conceitos',
        'quero realizar o primeiro curso para conseguir a certificação inicial',
        'desejo iniciar no curso básico para garantir um maior aprendizado',
        'eu fico lisonjeado que eu possa ter recebido essa proposta pro nível mais avançado, mas eu mesmo acredito que meu conhecimento ainda não está nesse nível, e por isso, pretendo começar do início',
        'o que eu respondi no formulário foi conhecimento que adquiri através de problemas que apareceu na minha vida, eu me sinto mais confortável em fazer o curso do zero'
    ],
    'Não possui conhecimentos básicos': [
        'porque ainda não tenho conhecimentos basicos',
        'porque não sinto que tenho conhecimento avançado para poder fazer um curso mais avançado',
        'não acho que tenho os conhecimentos mínimos necessários ainda.',
        'desejo ver os conteúdos do início para fixar os conhecimentos e posteriormente partir para o mais avançado, e não pular as etapas necessárias e básicas.',
        'acredito que não estou pronto para um curso intermediário',
        'tenho conhecimentos muito superficiais na área',
        'sendo uma turma avançada, não serei tao capaz de acompanhar',
        'prefiro começar do iniciante. tem muitas coisa que não vi ainda',
        'tenho a dúvida se irei conseguir acompanhar o nível da turma, estou a 7 anos fora da área de informática',
    ],
    'Foco em outra trilha de aprendizado': [
        'focar em uma trilha já planejada por mim',
        'não conseguiria focar em aws que está se aprofundando e em ms900 ao mesmo tempo',
        'estarei focado no curso aws practitioner',
        'procurando me especializar somente na aws'
    ],
    'Não possui interesse no curso': [
        'não é do meu interesse',
        'obrigado',
        'contato por e-mail'
    ],
    'Perda do prazo':[
        'o prazo para inicio do curso já passou\nData de início:  12 de Julho de 2023. '
    ]
}

# --- Função para padronizar motivos ---
def padronizar_motivos(motivo):
    print(motivo)
    if not isinstance(motivo, str):
        return motivo

    melhor_categoria = None
    melhor_score = 0

    for categoria, sinonimos in categorias.items():
        for sinonimo in sinonimos:
            score = fuzz.partial_ratio(motivo.lower(), sinonimo.lower())
            if score > melhor_score:
                melhor_categoria = categoria
                melhor_score = score

    return melhor_categoria if melhor_score >= 60 else motivo

# --- Funções das páginas ---
# def pagina_inicio():
#     st.title("Projeto Integrador - Escola da Nuvem")
#     st.write("Bem-vindo à plataforma de análise dos dados da Escola da Nuvem.")
#     st.info("Use o menu lateral para navegar entre as análises disponíveis.")
#     if st.button("Ir para página de alunos"):
#         st.session_state.pagina = "Alunos"
#         st.experimental_rerun()

def pagina_inicio():
    # st.set_page_config(page_title="Análise Escola da Nuvem", layout="wide")
    st.title("📊 Painel de Análise - Escola da Nuvem")
    st.markdown("""
        <h4 style='font-size:18px;'>Este painel interativo apresenta uma análise completa dos dados dos alunos da Escola da Nuvem,
        com foco em indicadores de desempenho, empregabilidade, estágios e motivos de evasão. Acompanhe a jornada dos estudantes e descubra
        oportunidades de melhoria e destaque.</h4>
    """, unsafe_allow_html=True)

    # Carregando dados
    df_excel = load_excel_data()
    total_alunos = df_excel.shape[0]
    aprovados = df_excel[df_excel['Estagio'].str.lower() == 'aprovado'].shape[0]
    reprovados = df_excel[df_excel['Estagio'].str.lower() == 'reprovado'].shape[0]
    # empregados = df_excel[df_excel['Empregado'].astype(str).str.lower() == 'sim'].shape[0]
    
    # Exibindo métricas principais
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Alunos", total_alunos)
    col2.metric("Aprovados", aprovados)
    col3.metric("Reprovados", reprovados)
    # col4.metric("Com Emprego", empregados)

    # Gráfico de distribuição
    st.markdown("### Distribuição Geral dos Estágios")
    estagios = df_excel['Estagio'].astype(str).str.lower().str.strip()
    estagios = estagios.replace({
        'desistãªncia': 'desistencia',
        'desistência': 'desistencia',
        'desistiu': 'desistencia',
        'sem interesse': 'desistencia',
        'nan': 'desconhecido',
    })
    estagios = estagios.fillna('desconhecido')
    status_counts = estagios.value_counts()

    fig, ax = plt.subplots(figsize=(6, 4))
    status_counts.plot(kind='bar', color='mediumseagreen', ax=ax)
    ax.set_title('Situação dos Alunos')
    ax.set_ylabel('Quantidade')
    ax.set_xlabel('Estágio')
    st.pyplot(fig)

    st.info("Use o menu lateral para explorar análises detalhadas por categoria.")


def pagina_alunos():
    st.title("👨‍🎓 Análise de Alunos")
    st.write("Explore o perfil dos alunos.")
    df = load_data()
    st.dataframe(df)

def pagina_empregabilidade():
    st.title("💼 Análise de Empregabilidade")
    st.markdown(
        "<h4 style='font-size:20px;'>Taxa de aprovação conforme criação de ações de empregabilidade</h4>",
        unsafe_allow_html=True
    )

    df = load_excel_data()
    df['Estagio'] = df['Estagio'].astype(str).str.lower().str.strip()
    df['Criar Empregabilidade'] = df['Criar Empregabilidade'].astype(str).str.lower().str.strip()

    aprovados = df[df['Estagio'] == 'aprovado']['Criar Empregabilidade'].value_counts()
    total = df['Criar Empregabilidade'].value_counts()
    taxa = (aprovados / total * 100).dropna()

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(
        taxa.values,
        labels=taxa.index,
        autopct='%1.1f%%',
        colors=sns.color_palette('autumn', len(taxa)),
        startangle=90,
        textprops={'fontsize': 10}
    )
    ax.axis('equal')
    ax.set_title('Taxa de Aprovação (%)', fontsize=8)
    st.pyplot(fig)
    # sns.barplot(x=taxa.index, y=taxa.values, hue=taxa.index, palette='autumn', legend=False)
    # plt.ylabel('Taxa de Aprovação (%)')
    # plt.ylim(0, 100)
    # plt.tight_layout()
    

def pagina_evasao():
    st.title("🚪 Análise de Evasão")
    st.write("Explore os dados de evasão escolar.")
    df = load_data()
    st.dataframe(df)

def pagina_reprovacao():
    st.title("❌ Análise de Reprovação")
    st.write("Explore os dados de reprovação dos alunos.")
    df = load_data()
    st.dataframe(df)

def pagina_estagios():
    st.title("📈 Análise de Estágios")
    st.markdown(
        "<h4 style='font-size:20px;'>Distribuição dos alunos por estágio (aprovado, reprovado, desistência, etc.)</h4>",
        unsafe_allow_html=True
    )
    df = load_excel_data()
    df['Estagio'] = df['Estagio'].astype(str).str.strip().str.lower()
    df['Estagio'] = df['Estagio'].replace({
        'desistãªncia': 'desistencia',
        'desistência': 'desistencia',
        'desistiu': 'desistencia',
        'sem interesse': 'desistencia',
        'desistência.': 'desistencia',
        'nan': 'desconhecido',
    })
    df['Estagio'] = df['Estagio'].fillna('desconhecido')
    status_counts = df['Estagio'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Quantidade']
    plt.figure(figsize=(8, 5))
    sns.barplot(data=status_counts, x='Status', y='Quantidade', hue='Status', palette='Set2', legend=False)
    plt.title('Estágio dos Alunos (Padronizado)')
    plt.ylabel('Quantidade')
    plt.xlabel('Status')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

def processo_seletivo():
    
    st.title("📉 Motivos de Recusa dos Cursos Ofertados")
    st.markdown(
        "<h4 style='font-size:20px;'>Nesta seção, analisamos os principais motivos relatados pelos candidatos para recusarem os cursos ofertados. Essa análise ajuda a compreender os desafios enfrentados pelos alunos em potencial.</h4>",
        unsafe_allow_html=True
    )
    
    df = df_processos()

        # Padroniza os motivos
    df['Motivo Recusa Curso Ofertado'] = df['Motivo Recusa Curso Ofertado'].map(padronizar_motivos)
    contagem = df['Motivo Recusa Curso Ofertado'].value_counts()
    print(contagem)
    fig, ax = plt.subplots(figsize=(10, 6))
    contagem.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title('Principais Motivos de Recusa dos Cursos Ofertados')
    ax.set_xlabel('Motivo de Recusa')
    ax.set_ylabel('Quantidade de Candidatos')
    for i, v in enumerate(contagem):
        ax.text(i, v + 0.2, str(v), ha='center', va='bottom', fontsize=8)
        
    st.pyplot(fig)

# --- Configuração da página e navegação ---
st.set_page_config(page_title="Análise Escola da Nuvem", layout="wide")

st.sidebar.header("Navegação")
opcao = st.sidebar.selectbox(
    "Escolha uma página",
    ["Início", "Alunos", "Empregabilidade", "Evasão", "Reprovação", "Estágios", "Processo Seletivo"]
)

if opcao == "Início":
    pagina_inicio()
elif opcao == "Alunos":
    pagina_alunos()
elif opcao == "Empregabilidade":
    pagina_empregabilidade()
elif opcao == "Evasão":
    pagina_evasao()
elif opcao == "Reprovação":
    pagina_reprovacao()
elif opcao == "Estágios":
    pagina_estagios()
elif opcao == "Processo Seletivo":
    processo_seletivo()
