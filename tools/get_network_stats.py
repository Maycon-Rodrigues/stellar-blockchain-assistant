from agno.tools.decorator import tool
from stellar_sdk import Server
import os


@tool()
def get_network_stats() -> dict:
    """
    Retrieves current Stellar network statistics and status.
    Shows fee stats, recent ledger information, and network activity.
    
    Returns:
        Dict with network statistics
    """
    try:
        horizon_url = os.getenv("STELLAR_HORIZON_URL", "https://horizon.stellar.org")
        server = Server(horizon_url)
        
        # Get fee stats
        fee_stats = server.fee_stats().call()
        
        # Get latest ledger
        ledgers = server.ledgers().order(desc=True).limit(1).call()
        latest_ledger = ledgers["_embedded"]["records"][0]
        
        return {
            "latest_ledger": {
                "sequence": latest_ledger["sequence"],
                "closed_at": latest_ledger["closed_at"],
                "successful_transactions": latest_ledger.get("successful_transaction_count", 0),
                "failed_transactions": latest_ledger.get("failed_transaction_count", 0),
                "operations": latest_ledger["operation_count"],
                "total_coins": latest_ledger["total_coins"],
                "protocol_version": latest_ledger["protocol_version"]
            },
            "fee_stats": {
                "last_ledger_base_fee": fee_stats["last_ledger_base_fee"],
                "ledger_capacity_usage": fee_stats.get("ledger_capacity_usage", "N/A"),
                "fee_charged_min": fee_stats["fee_charged"]["min"],
                "fee_charged_mode": fee_stats["fee_charged"]["mode"],
                "fee_charged_p50": fee_stats["fee_charged"]["p50"],
                "fee_charged_p95": fee_stats["fee_charged"]["p95"],
                "fee_charged_p99": fee_stats["fee_charged"]["p99"],
                "max_fee_p50": fee_stats["max_fee"]["p50"],
                "max_fee_p95": fee_stats["max_fee"]["p95"]
            },
            "base_reserve": latest_ledger.get("base_reserve_in_stroops", "N/A")
        }
    except Exception as e:
        return {"error": f"Error fetching network stats: {str(e)}"}
