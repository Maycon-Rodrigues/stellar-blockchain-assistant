from agno.tools.decorator import tool
from stellar_sdk import Server
import os


@tool()
def get_account_offers(account_id: str, limit: int = 20) -> dict:
    """
    Retrieves the active offers (open orders) on the Stellar DEX for an account.
    Shows what assets the account is currently trying to buy or sell.
    
    Args:
        account_id: Public address of the account
        limit: Maximum number of offers to return (default: 20, max: 200)
    
    Returns:
        Dict with list of active offers
    """
    try:
        horizon_url = os.getenv("STELLAR_HORIZON_URL", "https://horizon.stellar.org")
        server = Server(horizon_url)
        
        offers = server.offers().for_account(account_id).limit(min(limit, 200)).call()
        
        offers_list = []
        for offer in offers["_embedded"]["records"]:
            selling = offer["selling"]
            buying = offer["buying"]
            
            selling_asset = "XLM" if selling["asset_type"] == "native" else f"{selling['asset_code']}"
            buying_asset = "XLM" if buying["asset_type"] == "native" else f"{buying['asset_code']}"
            
            offers_list.append({
                "id": offer["id"],
                "selling": selling_asset,
                "buying": buying_asset,
                "amount": offer["amount"],
                "price": offer["price"],
                "last_modified": offer.get("last_modified_time", "N/A")
            })
        
        return {
            "account_id": account_id,
            "total_offers": len(offers_list),
            "offers": offers_list
        }
    except Exception as e:
        return {"error": f"Error fetching offers: {str(e)}"}
