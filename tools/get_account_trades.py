from agno.tools.decorator import tool
from stellar_sdk import Server
import os


@tool()
def get_account_trades(account_id: str, limit: int = 10) -> dict:
    """
    Retrieves the trade history for a Stellar account on the DEX.
    Shows completed buy/sell trades the account has executed.
    
    Args:
        account_id: Public address of the account
        limit: Maximum number of trades to return (default: 10, max: 200)
    
    Returns:
        Dict with list of trades
    """
    try:
        horizon_url = os.getenv("STELLAR_HORIZON_URL", "https://horizon.stellar.org")
        server = Server(horizon_url)
        
        trades = server.trades().for_account(account_id).limit(min(limit, 200)).order(desc=True).call()
        
        trades_list = []
        for trade in trades["_embedded"]["records"]:
            base_asset = trade["base_asset_type"]
            counter_asset = trade["counter_asset_type"]
            
            base = "XLM" if base_asset == "native" else trade.get("base_asset_code", "Unknown")
            counter = "XLM" if counter_asset == "native" else trade.get("counter_asset_code", "Unknown")
            
            trades_list.append({
                "id": trade["id"],
                "ledger_close_time": trade["ledger_close_time"],
                "base_asset": base,
                "counter_asset": counter,
                "base_amount": trade["base_amount"],
                "counter_amount": trade["counter_amount"],
                "price": trade["price"]["n"] + "/" + trade["price"]["d"],
                "trade_type": trade.get("trade_type", "orderbook")
            })
        
        return {
            "account_id": account_id,
            "total_returned": len(trades_list),
            "trades": trades_list
        }
    except Exception as e:
        return {"error": f"Error fetching trades: {str(e)}"}
