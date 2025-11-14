import streamlit as st
import os
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.models.google import Gemini

from tools.get_account_info import get_account_info
from tools.get_account_payments import get_account_payments
from tools.get_account_operations import get_account_operations
from tools.get_account_transactions import get_account_transactions
from tools.get_account_effects import get_account_effects
from tools.get_account_offers import get_account_offers
from tools.get_account_trades import get_account_trades
from tools.get_asset_info import get_asset_info
from tools.search_assets import search_assets
from tools.get_transaction_info import get_transaction_info
from tools.get_ledger_info import get_ledger_info
from tools.get_network_stats import get_network_stats
from config.agent_config import AGENT_CONFIG

from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Stellar Blockchain Assistant",
    page_icon="🌟",
    layout="wide",
)

def get_model_instance(provider: str, model_name: str, api_key: str):
    """Create a model instance based on provider and API key"""
    if provider == "OpenAI":
        return OpenAIChat(model_name, api_key=api_key)
    elif provider == "Google":
        return Gemini(model_name, api_key=api_key)
    else:
        raise ValueError(f"Provider {provider} não suportado")

def get_agent(model_instance):
    """Initialize the agent instance"""
    db = SqliteDb(db_file="/tmp/onchain_researcher.db")
    
    agent = Agent(
        model=model_instance,
        name=AGENT_CONFIG["name"],
        description="An AI assistant that helps users interact with the Stellar blockchain using natural language.",
        role=AGENT_CONFIG["role"],
        db=db,
        tools=[
            # Account queries
            get_account_info,
            get_account_transactions,
            get_account_payments,
            get_account_operations,
            get_account_effects,
            get_account_offers,
            get_account_trades,
            # Asset queries
            get_asset_info,
            search_assets,
            # Transaction queries
            get_transaction_info,
            # Ledger and network
            get_ledger_info,
            get_network_stats,
        ],
        instructions=AGENT_CONFIG["instructions"],
        enable_agentic_memory=True,
        add_history_to_context=True,
        markdown=True,
        tool_call_limit=15,
    )
    return agent

def main():
    st.title("🌟 Stellar Blockchain Assistant")
    st.markdown("Faça perguntas sobre a blockchain Stellar em linguagem natural.")
    
    # Developer information in main area (more visible)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 👨‍💻 Desenvolvedor")
        st.markdown("**Maycon Rodrigues**")
    with col2:
        st.markdown("### 🔗 GitHub")
        st.markdown("[Maycon-Rodrigues](https://github.com/Maycon-Rodrigues)")
    with col3:
        st.markdown("### 🌐 Portfolio")
        st.markdown("[mayconrodrigues.com](https://mayconrodrigues.com)")
    
    st.divider()
    
    # Model configuration options
    MODEL_OPTIONS = {
        "OpenAI": {
            "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
            "default": "gpt-4o-mini"
        },
        "Google": {
            "models": ["gemini-2.0-flash-exp", "gemini-1.5-pro", "gemini-1.5-flash"],
            "default": "gemini-2.0-flash-exp"
        },
    }
    
    # Sidebar with configuration
    with st.sidebar:
        st.header("⚙️ Configuração do Modelo")
        
        # Provider selection
        provider = st.selectbox(
            "Provedor LLM",
            options=list(MODEL_OPTIONS.keys()),
            help="Selecione o provedor de IA que deseja usar"
        )
        
        # Model selection based on provider
        model_name = st.selectbox(
            "Modelo",
            options=MODEL_OPTIONS[provider]["models"],
            index=MODEL_OPTIONS[provider]["models"].index(MODEL_OPTIONS[provider]["default"]),
            help="Selecione o modelo específico"
        )
        
        # API Key input
        api_key = st.text_input(
            f"API Key do {provider}",
            type="password",
            help=f"Insira sua chave de API do {provider}. Seus tokens serão usados.",
            placeholder=f"sk-..."
        )
        
        st.divider()
        
        st.header("📚 Exemplos de perguntas")
        st.markdown("""
        - Qual o saldo da conta GXXX...?
        - Mostre os últimos pagamentos dessa conta
        - A conta tem ofertas ativas no DEX?
        - Quais são as estatísticas da rede agora?
        """)
        
        st.divider()
        
        if st.button("🗑️ Limpar conversa", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # Check if API key is provided
    if not api_key:
        st.warning("⚠️ Por favor, insira sua API Key na barra lateral para começar.")
        st.info(f"""
        **Como obter sua API Key do {provider}:**
        
        {"- Acesse: https://platform.openai.com/api-keys" if provider == "OpenAI" else ""}
        {"- Acesse: https://aistudio.google.com/app/apikey" if provider == "Google" else ""}
        - Crie uma nova chave de API
        - Cole a chave no campo acima
        """)
        return
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Digite sua pergunta..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response with streaming
        with st.chat_message("assistant"):
            try:
                # Create model instance with user's API key
                model_instance = get_model_instance(provider, model_name, api_key)
                
                # Get or create agent
                agent = get_agent(model_instance)
                
                # Create placeholder for streaming
                message_placeholder = st.empty()
                full_response = ""
                
                # Stream the response
                for chunk in agent.run(prompt, stream=True):
                    if hasattr(chunk, 'content') and chunk.content:
                        full_response += chunk.content
                        message_placeholder.markdown(full_response + "▌")
                
                # Display final response without cursor
                message_placeholder.markdown(full_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                error_message = f"❌ Erro ao processar sua pergunta: {str(e)}"
                st.error(error_message)
                if "api" in str(e).lower() or "key" in str(e).lower() or "auth" in str(e).lower():
                    st.error("Verifique se sua API Key está correta e ativa.")

if __name__ == "__main__":
    main()
