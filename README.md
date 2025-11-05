# Agente de IA para Consulta de Criptomoedas e Notícias
Descrição do Projeto
Este projeto implementa um agente de IA autônomo utilizando a biblioteca LangChain, integrado com o modelo de linguagem GPT-3.5 Turbo da OpenAI. O agente é capaz de processar consultas do usuário, planejando e executando ações para responder perguntas complexas. Especificamente, ele inclui ferramentas para:

Buscar a cotação atual de criptomoedas (usando a API do CoinGecko).
Buscar notícias recentes sobre tópicos específicos (usando a API do Tavily Search).

O agente segue o paradigma ReAct (Reason + Act), onde raciocina sobre os passos necessários, chama ferramentas quando preciso e compila uma resposta final. Isso permite respostas dinâmicas e precisas, como consultar a cotação do Bitcoin e listar notícias recentes sobre ele.
Exemplo de uso: O agente processa entradas como "Qual a cotação atual do Bitcoin e quais as principais notícias sobre ele nas últimas 24 horas?" e retorna resultados formatados.
Requisitos

Python 3.8 ou superior.
Chaves API:

OpenAI API Key (para o LLM).
Tavily API Key (para busca de notícias).


Bibliotecas necessárias (instale via pip):
textpip install langchain langchain-openai langchain-community python-dotenv requests tavily-python


Instalação

Clone o repositório ou copie o código para um arquivo agente_cripto.py.
Crie um arquivo .env na raiz do projeto com as chaves API:
textOPENAI_API_KEY=sk-sua-chave-openai-aqui
TAVILY_API_KEY=tvly-sua-chave-tavily-aqui

Instale as dependências listadas acima.
Execute o script para testar.

Como Usar

Rode o script no terminal:
textpython agente_cripto.py

O exemplo padrão executa uma consulta sobre Bitcoin. Modifique input_usuario para testar outras consultas.


Personalização:

Adicione mais ferramentas editando a lista tools.
Altere o modelo LLM em ChatOpenAI (ex.: use "gpt-4o" para melhor desempenho, se disponível).
Para depuração, mantenha verbose=True no AgentExecutor para ver o raciocínio interno do agente.


Exemplo de Saída:
textExecutando agente com input: 'Qual a cotação atual do Bitcoin e quais as principais notícias sobre ele nas últimas 24 horas?'

> Entering new AgentExecutor chain...
[Raciocínio e chamadas de ferramentas aqui...]

--------------------------------------------------
Conteúdo da Resposta Final do Agente:
--------------------------------------------------
A cotação atual de Bitcoin é $72,345.67 USD. Aqui estão as principais notícias recentes sobre Bitcoin:
1. Título: Bitcoin sobe 5% após eleições nos EUA...
URL: https://exemplo.com/noticia
Preview: Conteúdo resumido...


Estrutura do Código

Configuração: Carrega variáveis de ambiente e inicializa o LLM.
Ferramentas:

buscar_cotacao_cripto: Consulta API CoinGecko para preços em USD.
buscar_noticias_recentes_tavily: Usa Tavily para buscar e formatar notícias (máximo 3 resultados por padrão).


Agente e Executor: Cria o agente com prompt do LangChain Hub e executa com verbose para logs.
Exemplo de Uso: Uma consulta hardcoded; expanda para um loop interativo se desejar.

Limitações e Melhorias

Limitações:

Requer chaves API válidas (planos pagos para uso intensivo).
Ferramentas limitadas a cripto e notícias; expanda com mais @tool.
Erros em APIs externas (ex.: rate limits) são capturados, mas podem falhar.


Melhorias Sugeridas:

Integre memória para conversas persistentes (use ConversationChain).
Adicione suporte a mais criptomoedas ou tópicos.
Use modelos locais (ex.: via Ollama) para evitar custos de API.
Implemente uma interface web (ex.: com Streamlit ou Flask).



Contribuições
Sinta-se à vontade para fork e contribuir! Abra issues para bugs ou sugestões.
Licença
MIT License – Use livremente, com atribuição ao código original.
Data: Novembro 2025
