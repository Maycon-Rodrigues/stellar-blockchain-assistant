from agno.tools.decorator import tool
from stellar_sdk import Server
import os


@tool()
def get_asset_info(asset_code: str, asset_issuer: str = None, limit: int = 10) -> dict:
    """
    Retrieves information about assets on the Stellar network.
    
    Args:
        asset_code: Asset code (e.g., USD, BTC, USDC, etc)
        asset_issuer: Address of the asset issuer (optional)
        limit: Maximum number of assets to return
    
    Returns:
        Dict with information about the asset(s)
    """
    try:
        horizon_url = os.getenv("STELLAR_HORIZON_URL", "https://horizon.stellar.org")
        server = Server(horizon_url)
        
        assets_builder = server.assets().for_code(asset_code)
        
        if asset_issuer:
            assets_builder = assets_builder.for_issuer(asset_issuer)
        
        assets = assets_builder.limit(min(limit, 200)).call()
        
        assets_list = []
        for asset in assets["_embedded"]["records"]:
            assets_list.append({
                "asset_type": asset["asset_type"],
                "asset_code": asset["asset_code"],
                "asset_issuer": asset["asset_issuer"],
                "accounts": asset["accounts"]["authorized"],
                "num_claimable_balances": asset.get("num_claimable_balances", 0),
                "amount": asset["amount"],
                "flags": asset["flags"]
            })
        
        return {
            "asset_code": asset_code,
            "total_found": len(assets_list),
            "assets": assets_list
        }
    except Exception as e:
        return {"error": f"Erro ao buscar informações do ativo: {str(e)}"}
