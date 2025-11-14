from agno.tools.decorator import tool
from stellar_sdk import Server
import os


@tool()
def fetch_transactions(limit: int = 10) -> dict:
    """
    Busca as transações mais recentes da rede Stellar.
    """
    horizon_url = os.getenv("STELLAR_HORIZON_URL", "https://horizon.stellar.org")
    server = Server(horizon_url)
    txs = server.transactions().order(desc=True).limit(limit).call()

    transactions = []
    for record in txs["_embedded"]["records"]:
        transactions.append(
            {
                "id": record["id"],
                "source_account": record["source_account"],
                "created_at": record["created_at"],
                "fee_charged": record["fee_charged"],
                "operation_count": record["operation_count"],
            }
        )

    return {"transactions": transactions}
