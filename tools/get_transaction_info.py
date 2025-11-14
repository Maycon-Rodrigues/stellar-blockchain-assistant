from agno.tools.decorator import tool
from stellar_sdk import Server
import os


@tool()
def get_transaction_info(transaction_hash: str) -> dict:
    """
    Retrieves detailed information about a specific transaction by its hash.
    
    Args:
        transaction_hash: Transaction hash (64 hexadecimal characters)
    
    Returns:
        Dict with detailed transaction information
    """
    try:
        horizon_url = os.getenv("STELLAR_HORIZON_URL", "https://horizon.stellar.org")
        server = Server(horizon_url)
        
        tx = server.transactions().transaction(transaction_hash).call()
        
        return {
            "hash": tx["hash"],
            "ledger": tx["ledger"],
            "created_at": tx["created_at"],
            "source_account": tx["source_account"],
            "fee_charged": tx["fee_charged"],
            "max_fee": tx["max_fee"],
            "operation_count": tx["operation_count"],
            "successful": tx["successful"],
            "memo_type": tx.get("memo_type", "none"),
            "memo": tx.get("memo", ""),
            "signatures": len(tx.get("signatures", []))
        }
    except Exception as e:
        return {"error": f"Erro ao buscar informações da transação: {str(e)}"}
