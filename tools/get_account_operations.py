from agno.tools.decorator import tool
from stellar_sdk import Server
import os


@tool()
def get_account_operations(account_id: str, limit: int = 10) -> dict:
    """
    Retrieves the latest operations performed by a Stellar account.
    
    Args:
        account_id: Public address of the account
        limit: Maximum number of operations to return (default: 10, max: 200)
    
    Returns:
        Dict with list of recent operations
    """
    try:
        horizon_url = os.getenv("STELLAR_HORIZON_URL", "https://horizon.stellar.org")
        server = Server(horizon_url)
        
        operations = server.operations().for_account(account_id).limit(min(limit, 200)).order(desc=True).call()
        
        operations_list = []
        for op in operations["_embedded"]["records"]:
            op_info = {
                "id": op["id"],
                "type": op["type"],
                "created_at": op["created_at"],
                "transaction_hash": op["transaction_hash"],
                "source_account": op.get("source_account", "N/A")
            }
            
            operations_list.append(op_info)
        
        return {
            "account_id": account_id,
            "total_returned": len(operations_list),
            "operations": operations_list
        }
    except Exception as e:
        return {"error": f"Erro ao buscar operações: {str(e)}"}
