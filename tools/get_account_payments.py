from agno.tools.decorator import tool
from stellar_sdk import Server
import os


@tool()
def get_account_payments(account_id: str, limit: int = 10) -> dict:
    """
    Retrieves the latest payment transactions for a Stellar account.
    
    Args:
        account_id: Public address of the account
        limit: Maximum number of payments to return (default: 10, max: 200)
    
    Returns:
        Dict with list of recent payments
    """
    try:
        horizon_url = os.getenv("STELLAR_HORIZON_URL", "https://horizon.stellar.org")
        server = Server(horizon_url)
        
        payments = server.payments().for_account(account_id).limit(min(limit, 200)).order(desc=True).call()
        
        payments_list = []
        for payment in payments["_embedded"]["records"]:
            payment_info = {
                "id": payment["id"],
                "type": payment["type"],
                "created_at": payment["created_at"],
                "transaction_hash": payment["transaction_hash"]
            }
            
            if payment["type"] == "payment":
                payment_info.update({
                    "from": payment.get("from", "N/A"),
                    "to": payment.get("to", "N/A"),
                    "asset_type": payment.get("asset_type", "native"),
                    "asset_code": payment.get("asset_code", "XLM"),
                    "amount": payment.get("amount", "0")
                })
            elif payment["type"] == "create_account":
                payment_info.update({
                    "funder": payment.get("funder", "N/A"),
                    "account": payment.get("account", "N/A"),
                    "starting_balance": payment.get("starting_balance", "0")
                })
            elif payment["type"] == "account_merge":
                payment_info.update({
                    "account": payment.get("account", "N/A"),
                    "into": payment.get("into", "N/A")
                })
            
            payments_list.append(payment_info)
        
        return {
            "account_id": account_id,
            "total_returned": len(payments_list),
            "payments": payments_list
        }
    except Exception as e:
        return {"error": f"Erro ao buscar pagamentos: {str(e)}"}
