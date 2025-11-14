from agno.tools.decorator import tool
from stellar_sdk import Server
import os


@tool()
def get_account_effects(account_id: str, limit: int = 10) -> dict:
    """
    Retrieves the effects (state changes) for a Stellar account's operations.
    Effects show the actual changes that happened (like balance changes, trustline additions, etc).
    
    Args:
        account_id: Public address of the account
        limit: Maximum number of effects to return (default: 10, max: 200)
    
    Returns:
        Dict with list of effects
    """
    try:
        horizon_url = os.getenv("STELLAR_HORIZON_URL", "https://horizon.stellar.org")
        server = Server(horizon_url)
        
        effects = server.effects().for_account(account_id).limit(min(limit, 200)).order(desc=True).call()
        
        effects_list = []
        for effect in effects["_embedded"]["records"]:
            effect_info = {
                "type": effect["type"],
                "created_at": effect["created_at"],
            }
            
            # Add type-specific information
            if effect["type"] in ["account_credited", "account_debited"]:
                effect_info.update({
                    "asset_type": effect.get("asset_type", "native"),
                    "asset_code": effect.get("asset_code", "XLM"),
                    "amount": effect.get("amount", "0")
                })
            elif effect["type"] == "account_created":
                effect_info.update({
                    "starting_balance": effect.get("starting_balance", "0")
                })
            elif effect["type"] in ["trustline_created", "trustline_removed", "trustline_updated"]:
                effect_info.update({
                    "asset_type": effect.get("asset_type"),
                    "asset_code": effect.get("asset_code"),
                    "limit": effect.get("limit", "N/A")
                })
            
            effects_list.append(effect_info)
        
        return {
            "account_id": account_id,
            "total_returned": len(effects_list),
            "effects": effects_list
        }
    except Exception as e:
        return {"error": f"Error fetching effects: {str(e)}"}
