# Binance Futures Testnet Trading Bot

A command-line Python application that places **Market** and **Limit** orders on the
[Binance Futures Testnet (USDT-M)](https://testnet.binancefuture.com).

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance REST API wrapper (signs & sends requests)
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Shared logger setup
├── cli.py                 # CLI entry point (argparse)
├── logs/                  # Auto-created; contains trading_bot.log
├── .env.example           # Template for credentials
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Get Demo/Testnet API credentials

1. Go to <https://demo.binance.com> and log in.
2. Navigate to **API Management** → **Create API** → **HMAC**.
3. Make sure **Enable Futures** is checked under API restrictions.
4. Copy your **API Key** and **Secret Key**.

### 2. Clone & install dependencies

```bash
git clone https://github.com/YOUR_USERNAME/trading-bot.git
cd trading_bot
pip install -r requirements.txt
```

### 3. Set environment variables

**Linux / macOS / Git Bash (Windows):**
```bash
export BINANCE_API_KEY="your_api_key_here"
export BINANCE_API_SECRET="your_api_secret_here"
```

**Windows CMD:**
```cmd
set BINANCE_API_KEY=your_api_key_here
set BINANCE_API_SECRET=your_api_secret_here
```

**Windows PowerShell:**
```powershell
$env:BINANCE_API_KEY="your_api_key_here"
$env:BINANCE_API_SECRET="your_api_secret_here"
```

Alternatively, copy `.env.example` to `.env`, fill in your credentials, and load it:
```bash
cp .env.example .env
# edit .env, then:
export $(cat .env | xargs)   # Linux/macOS
```

---

## How to Run

All commands are run from inside the `trading_bot/` directory.

### Place a Market BUY order
```bash
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01
```

### Place a Market SELL order
```bash
python cli.py --symbol ETHUSDT --side SELL --order-type MARKET --quantity 0.1
```

### Place a Limit BUY order
```bash
python cli.py --symbol BTCUSDT --side BUY --order-type LIMIT --quantity 0.01 --price 80000
```

### Place a Limit SELL order
```bash
python cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.01 --price 120000
```

### Show help
```bash
python cli.py --help
```

---

## Sample Output

```
╔══════════════ ORDER REQUEST ══════════════╗
  Symbol     : BTCUSDT
  Side       : BUY
  Order Type : MARKET
  Quantity   : 0.01
╚═══════════════════════════════════════════╝

╔══════════════ ORDER RESPONSE ═════════════╗
  Order ID     : 3158563829
  Status       : FILLED
  Executed Qty : 0.01
  Avg Price    : 96450.30
  Symbol       : BTCUSDT
  Client OID   : web_abc123
╚═══════════════════════════════════════════╝

✅  Order placed successfully!
```

---

## Logging

All activity is written to `logs/trading_bot.log`.  
The log captures:
- Every API request (parameters, endpoint)
- Every API response (status, orderId, executedQty)
- Validation warnings
- Errors and exceptions with full tracebacks

Console output shows INFO-level and above; the file captures DEBUG-level and above.

---

## Assumptions

- Only **USDT-M Futures** (perpetual contracts) on the testnet are targeted.
- Limit orders use `timeInForce=GTC` (Good Till Cancelled) by default.
- Credentials are supplied via environment variables (not hardcoded).
- No third-party SDK is required — only the `requests` library is used for HTTP calls.
- Quantity precision must match the symbol's rules on the testnet
  (e.g., BTCUSDT minimum quantity is 0.001 BTC).

---

## Requirements

- Python 3.10+
- `requests==2.32.3`
