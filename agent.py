from agno.agent import Agent
from agno.db.sqlite import SqliteDb

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
from config.model_config import MODEL_CONFIG

from dotenv import load_dotenv

load_dotenv()

db = SqliteDb(db_file="/tmp/onchain_researcher.db")

agent = Agent(
    model=MODEL_CONFIG["model"],
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
    # Memory configuration (choose ONE):
    # Option 1: Automatic memory (agent decides what to remember)
    enable_agentic_memory=True,
    # Option 2: Manual memory (you control with enable_user_memories)
    # enable_user_memories=True,
    # Add conversation history to context
    add_history_to_context=True,
    markdown=True,
    # Optional: Limit tool calls to prevent loops
    tool_call_limit=15,
)

if __name__ == "__main__":
    print("🌟 Stellar Blockchain Assistant iniciado!")
    print("Faça perguntas sobre a blockchain Stellar em linguagem natural.")
    print("Exemplos:")
    print('  - "Qual o saldo da conta GXXX...?"')
    print('  - "Quantas transações a conta GYYY... fez?"')
    print('  - "Mostre os últimos pagamentos dessa conta"')
    print('  - "A conta tem ofertas ativas no DEX?"')
    print('  - "Me dê detalhes do ledger mais recente"')
    print('  - "Quais são as estatísticas da rede agora?"')
    print("\nDigite /quit ou /q para sair.\n")
    
    try:
        while True:
            user_input = input("You: ")
            if user_input.strip().lower() in ("/quit", "/q"):
                print("👋 Até logo!")
                break
            if not user_input.strip():
                continue
            agent.print_response(user_input, stream=True)
    except (EOFError, KeyboardInterrupt):
        print("\n👋 Encerrando...")
