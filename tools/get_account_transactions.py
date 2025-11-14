from agno.tools.decorator import tool
from stellar_sdk import Server
import os


@tool()
def get_account_transactions(account_id: str, limit: int = 10) -> dict:
    """
    Retrieves the transaction history for a Stellar account.
    
    Args:
        account_id: Public address of the account
        limit: Maximum number of transactions to return (default: 10, max: 200)
    
    Returns:
        Dict with list of transactions and metadata
    """
    try:
        horizon_url = os.getenv("STELLAR_HORIZON_URL", "https://horizon.stellar.org")
        server = Server(horizon_url)
        
        transactions = server.transactions().for_account(account_id).limit(min(limit, 200)).order(desc=True).call()
        
        tx_list = []
        for tx in transactions["_embedded"]["records"]:
            tx_list.append({
                "hash": tx["hash"],
                "ledger": tx["ledger"],
                "created_at": tx["created_at"],
                "source_account": tx["source_account"],
                "fee_charged": tx["fee_charged"],
                "operation_count": tx["operation_count"],
                "successful": tx["successful"],
                "memo_type": tx.get("memo_type", "none"),
                "memo": tx.get("memo", "")
            })
        
        return {
            "account_id": account_id,
            "total_returned": len(tx_list),
            "transactions": tx_list
        }
    except Exception as e:
        return {"error": f"Error fetching transactions: {str(e)}"}
