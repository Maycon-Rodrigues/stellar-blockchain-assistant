from agno.tools.decorator import tool
from stellar_sdk import Server
import os


@tool()
def get_account_info(account_id: str) -> dict:
    """
    Retrieves complete information about a Stellar account, including balances for all assets.
    
    Args:
        account_id: Public address of the account (starts with G)
    
    Returns:
        Dict with account information including balances, signers, thresholds, etc.
    """
    try:
        horizon_url = os.getenv("STELLAR_HORIZON_URL", "https://horizon.stellar.org")
        server = Server(horizon_url)
        
        account = server.accounts().account_id(account_id).call()
        
        balances_info = []
        for balance in account["balances"]:
            if balance["asset_type"] == "native":
                balances_info.append({
                    "asset": "XLM (Lumens)",
                    "balance": balance["balance"],
                    "buying_liabilities": balance.get("buying_liabilities", "0"),
                    "selling_liabilities": balance.get("selling_liabilities", "0")
                })
            elif balance["asset_type"] == "liquidity_pool_shares":
                balances_info.append({
                    "type": "Liquidity Pool Share",
                    "balance": balance["balance"],
                    "liquidity_pool_id": balance.get("liquidity_pool_id", "")
                })
            else:
                balances_info.append({
                    "asset": f"{balance['asset_code']} (issuer: {balance['asset_issuer'][:8]}...)",
                    "balance": balance["balance"],
                    "limit": balance.get("limit", "N/A"),
                    "is_authorized": balance.get("is_authorized", False)
                })
        
        return {
            "account_id": account["account_id"],
            "sequence": account["sequence"],
            "subentry_count": account["subentry_count"],
            "home_domain": account.get("home_domain", ""),
            "balances": balances_info,
            "thresholds": account["thresholds"],
            "flags": account["flags"],
            "num_signers": len(account["signers"]),
            "num_sponsoring": account.get("num_sponsoring", 0),
            "num_sponsored": account.get("num_sponsored", 0)
        }
    except Exception as e:
        return {"error": f"Erro ao buscar informações da conta: {str(e)}"}
