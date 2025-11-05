import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
import requests
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.agents import create_openai_tools_agent, AgentExecutor

# Carrega variáveis de ambiente
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

if not openai_api_key:
    raise ValueError("Chave da OpenAI API não encontrada. Verifique seu arquivo .env.")
if not tavily_api_key:
    raise ValueError("Chave da Tavily API não encontrada. Verifique seu arquivo .env.")

# Inicializa o LLM (GPT-3.5 Turbo)
llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    model_name="gpt-3.5-turbo",
    temperature=0  # Respostas mais determinísticas para agentes
)

# Ferramenta 1: Busca cotação de criptomoeda via CoinGecko
@tool
def buscar_cotacao_cripto(nome_cripto: str) -> str:
    """
    Busca a cotação atual de uma criptomoeda em USD.
    Exemplo: 'bitcoin', 'ethereum'.
    """
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={nome_cripto.lower()}&vs_currencies=usd"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if nome_cripto.lower() in data and 'usd' in data[nome_cripto.lower()]:
            preco = data[nome_cripto.lower()]['usd']
            return f"A cotação atual de {nome_cripto.capitalize()} é ${preco:,.2f} USD."
        else:
            return f"Não foi possível encontrar a cotação em USD para {nome_cripto}."
    except Exception as e:
        return f"Erro ao buscar cotação de {nome_cripto}: {e}"

# Ferramenta 2: Busca notícias recentes via Tavily Search
@tool
def buscar_noticias_recentes_tavily(topico_da_pesquisa: str, numero_maximo_de_resultados: int = 3) -> str:
    """
    Busca notícias recentes sobre um tópico usando a Tavily Search API.
    """
    try:
        search_tool_instance = TavilySearchResults(max_results=numero_maximo_de_resultados)
        results = search_tool_instance.invoke(input=topico_da_pesquisa)

        if not results:
            return f"Nenhuma notícia recente encontrada para '{topico_da_pesquisa}'."

        formatted_output = f"Principais notícias sobre '{topico_da_pesquisa}':\n\n"
        if not isinstance(results, list):
            results = [results]

        for i, res_item in enumerate(results):
            title = res_item.get('title', 'N/A')
            url = res_item.get('url', 'N/A')
            content_preview = (res_item.get('content', '')[:250] + "...") if res_item.get('content') else 'N/A'
            formatted_output += f"{i+1}. {title}\n   URL: {url}\n   Preview: {content_preview}\n\n"

        return formatted_output.strip()
    except Exception as e:
        return f"Erro ao buscar notícias sobre '{topico_da_pesquisa}': {e}"

# Lista de ferramentas disponíveis para o agente
tools = [buscar_cotacao_cripto, buscar_noticias_recentes_tavily]

# Carrega prompt pré-definido do LangChain Hub (otimizado para OpenAI Tools)
prompt = hub.pull("hwchase17/openai-tools-agent")

# Cria o agente com LLM, ferramentas e prompt
agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)

# Cria o executor do agente (com modo verbose para depuração)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Exemplo de uso
input_usuario = "Qual a cotação atual do Bitcoin e quais as principais notícias sobre ele nas últimas 24 horas?"

print(f"Executando agente com input: '{input_usuario}'\n")
response = agent_executor.invoke({"input": input_usuario})

print("\n\n--------------------------------------------------")
print("Conteúdo da Resposta Final do Agente:")
print("--------------------------------------------------")
print(response["output"])
