from agno.tools.decorator import tool
from stellar_sdk import Server
import os


@tool()
def search_assets(asset_code: str = None, asset_issuer: str = None, limit: int = 20) -> dict:
    """
    Searches for assets on the Stellar network. Can search by asset code, issuer, or both.
    Useful for finding assets like USDC, BTC, or other tokens.
    
    Args:
        asset_code: Asset code to search for (e.g., "USDC", "BTC")
        asset_issuer: Specific issuer address to filter by (optional)
        limit: Maximum number of results (default: 20, max: 200)
    
    Returns:
        Dict with list of matching assets and their statistics
    """
    try:
        horizon_url = os.getenv("STELLAR_HORIZON_URL", "https://horizon.stellar.org")
        server = Server(horizon_url)
        
        builder = server.assets()
        
        if asset_code:
            builder = builder.for_code(asset_code)
        if asset_issuer:
            builder = builder.for_issuer(asset_issuer)
        
        assets = builder.limit(min(limit, 200)).order(desc=False).call()
        
        assets_list = []
        for asset in assets["_embedded"]["records"]:
            assets_list.append({
                "asset_code": asset["asset_code"],
                "asset_issuer": asset["asset_issuer"],
                "num_accounts": asset["num_accounts"],
                "num_claimable_balances": asset.get("num_claimable_balances", 0),
                "num_liquidity_pools": asset.get("num_liquidity_pools", 0),
                "amount": asset["amount"],
                "flags": {
                    "auth_required": asset["flags"]["auth_required"],
                    "auth_revocable": asset["flags"]["auth_revocable"],
                    "auth_immutable": asset["flags"]["auth_immutable"]
                }
            })
        
        return {
            "search_code": asset_code,
            "search_issuer": asset_issuer,
            "total_found": len(assets_list),
            "assets": assets_list
        }
    except Exception as e:
        return {"error": f"Error searching assets: {str(e)}"}
