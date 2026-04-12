import streamlit as st
from groq import Groq

# Configurando a aba do Navegador
st.set_page_config(
    page_title = "DSA AI Coder",
    page_icon = "🤖",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

# Prompt de sistema: define o comportamento, foco e estrutura de resposta da LLM
CUSTOM_PROMPT = """
Você é o "DSA Coder", um assistente de IA especialista em programação, com foco principal em Python. Sua missão é ajudar desenvolvedores iniciantes com dúvidas de programação de forma clara, precisa e útil.

REGRAS DE OPERAÇÃO:
1.  **Foco em Programação**: Responda apenas a perguntas relacionadas a programação, algoritmos, estruturas de dados, bibliotecas e frameworks. Se o usuário perguntar sobre outro assunto, responda educadamente que seu foco é exclusivamente em auxiliar com código.
2.  **Estrutura da Resposta**: Sempre formate suas respostas da seguinte maneira:
    * **Explicação Clara**: Comece com uma explicação conceitual sobre o tópico perguntado. Seja direto e didático.
    * **Exemplo de Código**: Forneça um ou mais blocos de código em Python com a sintaxe correta. O código deve ser bem comentado para explicar as partes importantes.
    * **Detalhes do Código**: Após o bloco de código, descreva em detalhes o que cada parte do código faz, explicando a lógica e as funções utilizadas.
    * **Documentação de Referência**: Ao final, inclua uma seção chamada "📚 Documentação de Referência" com um link direto e relevante para a documentação oficial da Linguagem Python (docs.python.org) ou da biblioteca em questão.
3.  **Clareza e Precisão**: Use uma linguagem clara. Evite jargões desnecessários. Suas respostas devem ser tecnicamente precisas.
"""

# Organização da barra lateral da Interface
with st.sidebar:
    st.title("🤖 DSA AI Coder")
    st.caption("Um Assistente de IA focado em programação Python para ajudar iniciantes.")

    groq_api_key = st.text_input("Insira sua API Key Groq",
        type = "password",
        help = "Obtenha sua chave em https://console.groq.com/keys"
    )

    # Seção de contato do autor
    st.markdown("---")
    st.caption("Desenvolvido para auxiliar em suas dúvidas de programação com Linguagem Python. A IA pode cometer erros. Sempre verifique as respostas.")
    st.markdown("---")
    st.caption("Desenvolvido por **Rafael Marques**.")

    col1, col2 = st.columns(2)

    with col1:
        st.link_button("💼 LinkedIn", "https://www.linkedin.com/in/rafamarques12/")

    with col2:
        st.link_button("🐙 GitHub", "https://github.com/rafamarqsdev24")

st.title("Data Science Academy - DSA AI Coder")
st.subheader("Assistente Pessoal de Programação Python 🐍")
st.caption("Faça sua pergunta sobre a Linguagem Python e obtenha códigos, explicações e referências.")

# Inicializa o histórico de mensagens, caso não tenha 
if "messages" not in st.session_state:
    st.session_state.messages = []

# Renderiza as mensagens na Interface em forma de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

client = None

# Verifica se o cliente forneceu a API Key
if groq_api_key:
    try:
        client = Groq(api_key = groq_api_key)

    except Exception as e:
        st.sidebar.error(f"Erro ao inicializar o cliente Groq: {e}")
        st.stop()

elif st.session_state.messages:
    st.warning("Por favor, insira sua API Key da Groq na barra lateral para continuar.")

# Captura a entrada de prompt do usuário
if prompt := st.chat_input("Qual sua dúvida sobre Python?"):
    if not client: # Interrompe a execução se a API Key não foi fornecida
        st.warning("Por favor, insira sua API Key da Groq na barra lateral para continuar.")
        st.stop()

    # Armazena as mensagens no estado da sessão    
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Exibe a mensagem do usuário no chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Empacota a mensagem do usuário para enviar a LLM e gerar a resposta final
    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for msg in st.session_state.messages:
        messages_for_api.append(msg)

    # Envia o histórico de mensagens à API do Groq e exibe a resposta na Interface
    with st.chat_message("assistant"):
        with st.spinner("Analisando sua pergunta..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages = messages_for_api,
                    model = "openai/gpt-oss-20b",
                    temperature = 0.7,
                    max_tokens = 2048,
                )

                # Filtra as informações buscadas pela LLM, evitando metadados
                dsa_ai_resposta = chat_completion.choices[0].message.content
                st.markdown(dsa_ai_resposta)
                st.session_state.messages.append({"role": "assistant", "content": dsa_ai_resposta})

            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API do Groq: {e}")

# Créditos a Data Science Academy
st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <hr>
        <p>DSA AI Coder - Parte Integrante do Curso Gratuito Fundamentos de Linguagem Python da Data Science Academy</p>
    </div>
    """,
    unsafe_allow_html = True
)