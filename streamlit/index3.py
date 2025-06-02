import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from rapidfuzz import fuzz
from PIL import Image
import base64

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
    # Aqui use os dados reais lendo do arquivo
    # Se quiser, descomente para ler do arquivo:
    # return pd.read_excel('processos_seletivos_pii_none.xlsx')

    # Exemplo de DataFrame para testes
    data = {
        'Motivo Recusa Curso Ofertado': [
            'não tenho disponibilidade nesse horário',
            'quero começar pelo fundamentos aws',
            'porque ainda não tenho conhecimentos basicos',
            'não é do meu interesse',
            'focar em uma trilha já planejada por mim',
            'obrigado'
        ]
    }
    return pd.DataFrame(data)

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

    st.markdown("### 1. Origem dos Alunos Imigrantes")
    st.markdown("""
    <div style='text-align: justify; font-size: 18px'>
        A imagem abaixo mostra a <strong>origem dos alunos imigrantes</strong> matriculados nos cursos oferecidos pela Escola da Nuvem. 
        Esse dado é relevante porque evidencia a presença de alunos que nasceram fora do Brasil, mas que, atualmente, estão em busca de capacitação profissional na área de tecnologia, contribuindo com a diversidade cultural dentro das turmas.<br><br>
    </div>
    """, unsafe_allow_html=True)

    def get_base64_image(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    image_base64 = get_base64_image("imigrantes.png")

    # Mostrar imagem centralizada
    st.markdown(f"""
        <div style='text-align: center'>
            <img src='data:image/png;base64,{image_base64}' width='600' alt='Origem dos alunos imigrantes'/>
            <p><em>Origem dos alunos imigrantes</em></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 2. Distribuição por Faixa Etária")
    st.markdown("""
    <div style='text-align: justify; font-size: 18px'>
          A distribuição da <strong>faixa etária</strong> dos alunos matriculados fornece informações importantes sobre o perfil etário do público atendido.
    A maioria dos alunos se concentra entre 18 e 29 anos, o que indica uma forte presença de jovens adultos em início de carreira ou em processo de transição profissional.<br><br>
    </div>
    """, unsafe_allow_html=True)

    def get_base64_image(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    image_base64 = get_base64_image("faixa_etaria.png")

    # Mostrar imagem centralizada
    st.markdown(f"""
        <div style='text-align: center'>
            <img src='data:image/png;base64,{image_base64}' width='800' alt='Origem dos alunos imigrantes'/>
            <p><em>Origem dos alunos imigrantes</em></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 3. Média de Idade dos Alunos")
    st.markdown("""
    <div style='text-align: justify; font-size: 18px'>
        A <strong>média de idade por gênero</strong> dos alunos da Escola da Nuvem oferece um panorama sobre o perfil etário de homens, mulheres e pessoas que se identificam com outros gêneros nos cursos oferecidos.<br>
    A análise mostra que a idade média entre os gêneros é relativamente próxima, o que evidencia um equilíbrio geracional. Essa proximidade pode indicar que o acesso às oportunidades de formação em tecnologia está sendo promovido de maneira igualitária, independentemente do gênero.<br><br>
    </div>
    """, unsafe_allow_html=True)

    def get_base64_image(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    image_base64 = get_base64_image("media_idade.png")

    # Mostrar imagem centralizada
    st.markdown(f"""
        <div style='text-align: center'>
            <img src='data:image/png;base64,{image_base64}' width='800' alt='Origem dos alunos imigrantes'/>
            <p><em>Origem dos alunos imigrantes</em></p>
        </div>
        """, unsafe_allow_html=True)
    

    # media_idade_img = Image.open("media_idade.png")
    # st.image(media_idade_img, caption="Média de idade dos alunos", use_column_width=True)

def pagina_empregabilidade():
    st.title("💼 Análise de Empregabilidade")
    st.markdown("""
<div style='text-align: justify; font-size: 18px'>
    A imagem abaixo apresenta a <strong>situação de emprego atual</strong> dos alunos. 
</div>
""", unsafe_allow_html=True)

    st.markdown("### Situação de emprego")
    def get_base64_image(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    image_base64 = get_base64_image("emprego.png")
    st.markdown(f"""
    <div style='text-align: center'>
        <img src='data:image/png;base64,{image_base64}' width='1000'/>
        <p><em>Situação de emprego atual dos alunos da Escola da Nuvem</em></p>
    </div>
    """, unsafe_allow_html=True)

def pagina_desempenho():

    def get_base64_image(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    st.title("📊 Análise de Desempenho")
    st.markdown("""
<div style='text-align: justify; font-size: 18px'>
    Esta seção apresenta uma análise do <strong>desempenho acadêmico</strong> dos alunos da Escola da Nuvem, com base na média geral das notas e no desempenho por disciplina.
    Esses indicadores ajudam a entender o nível de aprendizado dos estudantes, identificar possíveis dificuldades em áreas específicas e orientar ações para melhoria contínua da formação.<br><br>
</div>
""", unsafe_allow_html=True)

    # Média das Notas
    st.markdown("### 1. Média Geral das Notas")
    st.markdown("""
<div style='text-align: justify; font-size: 18px'>
    A imagem abaixo mostra a <strong>média geral de notas</strong> obtidas pelos alunos nos cursos. 
    Essa métrica permite avaliar o desempenho global da turma e a efetividade das trilhas educacionais.<br><br>
</div>
""", unsafe_allow_html=True)

    image_base64 = get_base64_image("media_nota.png")
    st.markdown(f"""
    <div style='text-align: center'>
        <img src='data:image/png;base64,{image_base64}' width='1000'/>
        <p><em>Média geral de desempenho dos alunos</em></p>
    </div>
    """, unsafe_allow_html=True)

    # Notas por Matéria
    st.markdown("### 2. Notas por Matéria")
    st.markdown("""
<div style='text-align: justify; font-size: 18px'>
    O gráfico a seguir apresenta as <strong>notas médias por matéria</strong>, permitindo uma análise detalhada do desempenho em cada área do conhecimento. 
    Esse tipo de análise é importante para identificar disciplinas com maior necessidade de reforço e promover intervenções pedagógicas mais assertivas.<br><br>
</div>
""", unsafe_allow_html=True)

    image_base64 = get_base64_image("nota_materia.png")
    st.markdown(f"""
    <div style='text-align: center'>
        <img src='data:image/png;base64,{image_base64}' width='1000'/>
        <p><em>Desempenho por disciplina</em></p><br><br>
    </div>
    """, unsafe_allow_html=True)

def pagina_estagios():

    def get_base64_image(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    
    st.title("📈 Análise de Estágios")
    st.markdown("""
<div style='text-align: justify; font-size: 18px'>
    Esta seção apresenta uma análise do <strong>Distribuição dos alunos por estágio</strong> (aprovado, reprovado, desistência, etc.<br><br>
</div>
""", unsafe_allow_html=True)

    # Média das Notas
    # st.markdown("### 1. Média Geral das Notas")
    st.markdown("""
<div style='text-align: justify; font-size: 18px'> A imagem abaixo apresenta a distribuição dos alunos de acordo com seu <strong>status acadêmico padronizado</strong>. Essa visualização permite compreender a proporção de concluintes, desistentes, reprovados e alunos em curso, além de casos com status não identificado. Essas informações são essenciais para o monitoramento da trajetória dos estudantes e para o planejamento de ações de permanência e sucesso acadêmico.<br><br> </div>
""", unsafe_allow_html=True)

    image_base64 = get_base64_image("estagio.png")
    st.markdown(f"""
    <div style='text-align: center'>
        <img src='data:image/png;base64,{image_base64}' width='1000'/>
        <p><em>Alunos que foram aprovados, reprovados, desistiram ou estão no estágio</em></p>
    </div>
    """, unsafe_allow_html=True)

    # st.title("📈 Análise de Estágios")
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


    # df['Estagio'] = df['Estagio'].fillna('desconhecido')
    # status_counts = df['Estagio'].value_counts().reset_index()
    # status_counts.columns = ['Status', 'Quantidade']
    # plt.figure(figsize=(8, 5))
    # sns.barplot(data=status_counts, x='Status', y='Quantidade', hue='Status', palette='Set2', legend=False)
    # plt.title('Estágio dos Alunos (Padronizado)')
    # plt.ylabel('Quantidade')
    # plt.xlabel('Status')
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    # st.pyplot(plt)

def processo_seletivo():

    def get_base64_image(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    
    st.title("📉 Motivos de Recusa dos Cursos Ofertados")
    st.markdown(
        "<div style='text-align: justify; font-size: 18px'>Nesta seção, analisamos os principais motivos relatados pelos candidatos para recusarem os cursos ofertados. Essa análise ajuda a compreender os desafios enfrentados pelos alunos em potencial. <br><br></div>",
        unsafe_allow_html=True
    )

    st.markdown("""
<div style='text-align: justify; font-size: 18px'>  A imagem abaixo apresenta os <strong>principais motivos de recusa</strong> dos cursos ofertados pelos candidatos. A identificação dessas razões — como incompatibilidade de datas, ausência de conhecimentos prévios ou falta de interesse — permite compreender as barreiras enfrentadas pelos participantes e aperfeiçoar o desenho das formações. Esses dados são fundamentais para aumentar a adesão e o engajamento nas próximas ofertas educacionais.<br><br> </div>
""", unsafe_allow_html=True)

    image_base64 = get_base64_image("recusa1.1.jpg")
    st.markdown(f"""
    <div style='text-align: center'>
        <img src='data:image/png;base64,{image_base64}' width='1000'/>
        <p><em>Motivos informados pelos candidatos para não participarem dos cursos ofertados</em></p>
    </div>
    """, unsafe_allow_html=True)

    
    # df = df_processos()

    #     # Padroniza os motivos
    # df['Motivo Recusa Curso Ofertado'] = df['Motivo Recusa Curso Ofertado'].map(padronizar_motivos)
    # contagem = df['Motivo Recusa Curso Ofertado'].value_counts()
    # print(contagem)
    # fig, ax = plt.subplots(figsize=(10, 6))
    # contagem.plot(kind='bar', ax=ax, color='skyblue')
    # ax.set_title('Principais Motivos de Recusa dos Cursos Ofertados')
    # ax.set_xlabel('Motivo de Recusa')
    # ax.set_ylabel('Quantidade de Candidatos')
    # for i, v in enumerate(contagem):
    #     ax.text(i, v + 0.2, str(v), ha='center', va='bottom', fontsize=8)
    #     st.pyplot(fig)

# --- Configuração da página e navegação ---
st.set_page_config(page_title="Análise Escola da Nuvem", layout="wide")

st.sidebar.header("Navegação")
opcao = st.sidebar.selectbox(
    "Escolha uma página",
    ["Início", "Alunos", "Empregabilidade", "Desempenho", "Estágios", "Processo Seletivo"]
)

if opcao == "Início":
    pagina_inicio()
elif opcao == "Alunos":
    pagina_alunos()
elif opcao == "Empregabilidade":
    pagina_empregabilidade()
elif opcao == "Desempenho":
    pagina_desempenho()
elif opcao == "Estágios":
    pagina_estagios()
elif opcao == "Processo Seletivo":
    processo_seletivo()
