from agno.tools.decorator import tool


@tool()
def analyze_transactions(transactions: list[dict]) -> str:
    """
    Analyse the transactions and identify potential anomalies.
    """
    if not transactions:
        return "Nenhuma transação recente encontrada."

    avg_fee = sum(int(tx["fee_charged"]) for tx in transactions) / len(transactions)
    max_fee_tx = max(transactions, key=lambda t: int(t["fee_charged"]))

    report = (
        f"📊 Análise das últimas {len(transactions)} transações:\n"
        f"• Média de fee: {avg_fee}\n"
        f"• Maior fee: {max_fee_tx['fee_charged']} (tx {max_fee_tx['id'][:6]}...)\n"
        f"• Transações totais: {len(transactions)}"
    )

    return report
