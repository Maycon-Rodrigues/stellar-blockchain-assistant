# Stellar Blockchain Assistant

An AI-powered assistant that helps you interact with the Stellar blockchain using natural language. Built with the Agno framework and Stellar SDK, it allows you to query account information, check balances, view transactions, and explore the Stellar network without needing to know technical API details.

Available in two interfaces:
- **CLI Mode**: Terminal-based interactive agent
- **Web UI**: Beautiful Streamlit web interface with chat interface

## Features

- **Natural Language Queries**: Ask questions about the Stellar blockchain in plain language
- **Comprehensive Account Information**: Balances, transactions, payments, operations, effects, offers, and trades
- **Transaction Details**: Look up specific transactions by hash
- **Network Statistics**: Current network status, fees, and ledger information
- **DEX Integration**: View active offers and trade history
- **AI-Powered**: Uses LLMs to understand your questions and format responses clearly
- **Agentic Memory**: Maintains context across conversations
- **Multi-Model Support**: Choose between OpenAI (GPT-4o, GPT-4o-mini) or Google (Gemini 2.0, Gemini 1.5)

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Clone the repository
git clone <repository-url>
cd onchain_analyst

# Install dependencies
uv sync
```

## Environment Variables

Create a `.env` file in the project root:

```env
# Stellar Horizon API endpoint
STELLAR_HORIZON_URL=https://horizon.stellar.org  # For mainnet
# STELLAR_HORIZON_URL=https://horizon-testnet.stellar.org  # For testnet

# LLM API keys
# For Google Gemini:
GOOGLE_API_KEY=your_key_here
# For OpenAI:
OPENAI_API_KEY=your_key_here
```

**Note for Streamlit Web UI**: You can provide API keys directly in the web interface sidebar, no `.env` file required!

## Usage

### Option 1: Web Interface (Streamlit)

Launch the beautiful web interface with chat functionality:

```bash
uv run streamlit run app_streamlit.py
```

This will open a web browser with:
- 💬 **Interactive chat interface** with message history
- ⚙️ **Model configuration sidebar** - choose between OpenAI or Google models
- 🔑 **API Key input** - paste your key directly in the UI (no .env needed)
- 📊 **Rich markdown responses** with formatted data
- 🗑️ **Clear conversation** button to start fresh

### Option 2: Terminal CLI

Run the command-line interface:

```bash
uv run agent.py
```

### Example Queries

Ask questions in natural language:

```
You: What is the balance of account GAHK7EEG2WWHVKDNT4CEQFZGKF2LGDSW2IVM4S5DP42RBW3K6BTODB4A?

You: How many transactions has account GXXX... made?

You: Show me the last 10 payments for that account

You: Does the account have any active offers on the DEX?

You: What trades has this account completed?

You: Search for the USDC asset

You: What are the current network statistics?

You: Tell me about the most recent ledger
```

Exit with `/quit` or `/q`.

## Available Tools (12 Total)

### Account Queries (7 tools)

#### get_account_info
Retrieves complete account information including:
- Account ID and sequence number
- All asset balances (XLM and custom assets)
- Thresholds and flags
- Number of signers

#### get_account_transactions
Gets transaction history for an account. **Use this to count transactions!**
- Transaction hashes
- Fees charged
- Operation counts
- Success/failure status

#### get_account_payments
Fetches payment-specific operations:
- Regular payments
- Account creation operations
- Account merge operations

#### get_account_operations
Lists all operations performed by an account.

#### get_account_effects
Shows state changes (effects) from operations:
- Balance changes (credits/debits)
- Trustline additions/removals
- Account creation effects

#### get_account_offers
Gets active orders on the Stellar DEX:
- Selling/buying assets
- Amounts and prices
- Offer IDs

#### get_account_trades
Retrieves completed trade history:
- Trade pairs
- Amounts exchanged
- Prices
- Trade timestamps

### Asset Queries (2 tools)

#### get_asset_info
Queries specific asset by code and issuer:
- Total supply
- Number of holders
- Asset flags

#### search_assets
Searches for assets by code (e.g., "USDC", "BTC"):
- Multiple issuer results
- Statistics for each
- Authorization flags

### Transaction Queries (1 tool)

#### get_transaction_info
Gets detailed information about a specific transaction by hash:
- Ledger number
- Fee charged
- Operation count
- Memo and signatures

### Network Queries (2 tools)

#### get_ledger_info
Retrieves information about ledgers:
- Current or specific ledger by sequence
- Transaction and operation counts
- Network fees and reserves
- Protocol version

#### get_network_stats
Gets current network statistics:
- Latest ledger info
- Fee statistics (min, mode, p50, p95, p99)
- Network capacity usage
- Base reserve

## Architecture

The application consists of:

1. **Agent System (agent.py)**: Core interactive agent using Agno framework with SQLite-backed memory for context retention.

2. **Tools Layer (tools/)**: 12 specialized tools for querying the Stellar blockchain organized by category:
   - **Account tools** (7): Complete account analysis
   - **Asset tools** (2): Asset search and information
   - **Transaction tools** (1): Transaction lookup
   - **Network tools** (2): Ledger and network statistics

3. **Configuration**:
   - `config/agent_config.py`: Agent role and detailed instructions
   - `config/model_config.py`: LLM model selection

All tools use the Stellar SDK to communicate with the Horizon API.

## Requirements

- Python >= 3.13
- Dependencies managed by `uv` (see `pyproject.toml`)
- API Key from OpenAI or Google (for LLM access)

## Streamlit Web UI Features

The web interface (`app_streamlit.py`) provides:

### 🎨 User Interface
- Clean, responsive chat interface
- Real-time streaming responses
- Message history preservation
- Markdown formatting for structured data

### ⚙️ Configuration Options
- **Provider Selection**: Choose between OpenAI or Google
- **Model Selection**: 
  - OpenAI: GPT-4o, GPT-4o-mini, GPT-4-turbo, GPT-3.5-turbo
  - Google: Gemini 2.0 Flash, Gemini 1.5 Pro, Gemini 1.5 Flash
- **API Key Input**: Secure password field for your API key
- **Clear Conversation**: Reset chat history anytime


