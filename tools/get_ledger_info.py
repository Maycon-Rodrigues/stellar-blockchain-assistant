from agno.tools.decorator import tool
from stellar_sdk import Server
import os


@tool()
def get_ledger_info(ledger_sequence: int = None) -> dict:
    """
    Retrieves information about a specific ledger or the most recent one.
    
    Args:
        ledger_sequence: Ledger sequence number (optional, if not provided returns the most recent)
    
    Returns:
        Dict with ledger information
    """
    try:
        horizon_url = os.getenv("STELLAR_HORIZON_URL", "https://horizon.stellar.org")
        server = Server(horizon_url)
        
        if ledger_sequence:
            ledger = server.ledgers().ledger(ledger_sequence).call()
        else:
            ledgers = server.ledgers().order(desc=True).limit(1).call()
            ledger = ledgers["_embedded"]["records"][0]
        
        return {
            "sequence": ledger["sequence"],
            "hash": ledger["hash"],
            "closed_at": ledger["closed_at"],
            "successful_transaction_count": ledger.get("successful_transaction_count", 0),
            "failed_transaction_count": ledger.get("failed_transaction_count", 0),
            "operation_count": ledger["operation_count"],
            "total_coins": ledger["total_coins"],
            "fee_pool": ledger["fee_pool"],
            "base_fee_in_stroops": ledger["base_fee_in_stroops"],
            "base_reserve_in_stroops": ledger["base_reserve_in_stroops"],
            "protocol_version": ledger["protocol_version"]
        }
    except Exception as e:
        return {"error": f"Erro ao buscar informações do ledger: {str(e)}"}
