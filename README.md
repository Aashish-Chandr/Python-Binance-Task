<div align="center">

<!-- Animated Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=Binance%20Futures%20Trading%20Bot&fontSize=40&fontColor=fff&animation=twinkling&fontAlignY=35&desc=Python%20%7C%20REST%20API%20%7C%20HMAC%20Auth%20%7C%20CLI&descAlignY=55&descSize=18" width="100%"/>

<!-- Badges -->
<p>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Binance-Futures%20Testnet-F0B90B?style=for-the-badge&logo=binance&logoColor=black"/>
  <img src="https://img.shields.io/badge/API-REST%20%2B%20HMAC-00C853?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Auth-SHA256%20Signature-E91E63?style=for-the-badge&logo=letsencrypt&logoColor=white"/>
  <img src="https://img.shields.io/badge/Interface-CLI-607D8B?style=for-the-badge&logo=windowsterminal&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge"/>
</p>

<p>
  <img src="https://img.shields.io/badge/Orders-Market%20%26%20Limit-orange?style=flat-square"/>
  <img src="https://img.shields.io/badge/Logging-Full%20Audit%20Trail-green?style=flat-square"/>
  <img src="https://img.shields.io/badge/Validation-Input%20Guards-red?style=flat-square"/>
  <img src="https://img.shields.io/badge/No%20SDK-Raw%20HTTP%20Requests-blueviolet?style=flat-square"/>
</p>

> **A production-grade command-line trading bot** that interfaces directly with the Binance Futures Testnet REST API using raw HTTP requests, HMAC-SHA256 authentication, and clean modular Python architecture — built without any official SDK.

</div>

---

## 📌 Table of Contents

- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [⚙️ Setup & Installation](#️-setup--installation)
- [🚀 How to Run](#-how-to-run)
- [📟 Sample Output](#-sample-output)
- [📋 Logging](#-logging)
- [🛡️ Input Validation](#️-input-validation)
- [📐 Design Decisions](#-design-decisions)
- [🧰 Tech Stack](#-tech-stack)
- [📁 File Reference](#-file-reference)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📈 **Market Orders** | Instant execution at current market price |
| 📊 **Limit Orders** | Price-controlled GTC orders with precision targeting |
| 🔐 **HMAC-SHA256 Auth** | Manually implemented signature generation — no SDK dependency |
| 🧩 **Modular Architecture** | Clean separation: client, orders, validators, logging |
| 🖥️ **CLI Interface** | Ergonomic `argparse`-powered command-line tool |
| 📝 **Full Logging** | Dual-output: console (INFO+) and rotating file (DEBUG+) |
| ✅ **Input Validation** | Pre-flight checks before any API call is made |
| 🔒 **Env-Based Credentials** | Zero hardcoded secrets; `.env` / shell variable support |

---

## 🏗️ Architecture

```
trading_bot/
├── bot/
│   ├── __init__.py           # Package init
│   ├── client.py             # 🔑 Binance REST API wrapper (HMAC signing, HTTP requests)
│   ├── orders.py             # 📦 Order placement logic (MARKET / LIMIT)
│   ├── validators.py         # 🛡️  Input validation (symbol, side, quantity, price)
│   └── logging_config.py     # 📋 Shared logger (console + file handlers)
├── cli.py                    # 🖥️  CLI entry point (argparse)
├── logs/                     # 📂 Auto-created; stores trading_bot.log
├── .env.example              # 🔒 Template for environment credentials
├── .gitignore
├── requirements.txt
└── README.md
```

### 🔄 Request Lifecycle

```
CLI Input (argparse)
       │
       ▼
  validators.py ──── ❌ Fail fast on bad input
       │
       ▼
   orders.py ──────── Constructs order payload
       │
       ▼
   client.py ──────── Signs request (HMAC-SHA256)
                │          └─► Appends timestamp + signature
                ▼
    Binance Futures Testnet REST API
                │
                ▼
       Response Parsed & Logged
                │
                ▼
       Pretty-printed to Console ✅
```

---

## ⚙️ Setup & Installation

### Step 1 — Get Testnet API Credentials

1. Visit [https://demo.binance.com](https://demo.binance.com) and log in
2. Go to **API Management** → **Create API** → **HMAC**
3. ✅ Enable **Futures** under API restrictions
4. Copy your **API Key** and **Secret Key**

---

### Step 2 — Clone & Install

```bash
git clone https://github.com/Aashish-Chandr/Python-Binance-Task.git
cd Python-Binance-Task
pip install -r requirements.txt
```

> **Requirements:** Python 3.10+ · `requests==2.32.3`

---

### Step 3 — Configure Credentials

**Option A — Shell export (recommended for dev):**

```bash
# Linux / macOS / Git Bash
export BINANCE_API_KEY="your_api_key_here"
export BINANCE_API_SECRET="your_api_secret_here"
```

```cmd
:: Windows CMD
set BINANCE_API_KEY=your_api_key_here
set BINANCE_API_SECRET=your_api_secret_here
```

```powershell
# Windows PowerShell
$env:BINANCE_API_KEY="your_api_key_here"
$env:BINANCE_API_SECRET="your_api_secret_here"
```

**Option B — `.env` file:**

```bash
cp .env.example .env
# Edit .env with your credentials, then:
export $(cat .env | xargs)   # Linux / macOS
```

---

## 🚀 How to Run

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

### Show all CLI options
```bash
python cli.py --help
```

| Argument | Required | Description |
|---|---|---|
| `--symbol` | ✅ | Trading pair, e.g. `BTCUSDT` |
| `--side` | ✅ | `BUY` or `SELL` |
| `--order-type` | ✅ | `MARKET` or `LIMIT` |
| `--quantity` | ✅ | Quantity to trade |
| `--price` | ⚠️ LIMIT only | Target limit price |

---

## 📟 Sample Output

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

## 📋 Logging

All activity is written to `logs/trading_bot.log`, automatically created on first run.

```
[2025-01-15 14:23:01] INFO  - Placing MARKET BUY order for BTCUSDT, qty=0.01
[2025-01-15 14:23:01] DEBUG - POST /fapi/v1/order | params: {symbol: BTCUSDT, side: BUY, ...}
[2025-01-15 14:23:02] DEBUG - Response 200: {orderId: 3158563829, status: FILLED, avgPrice: 96450.30}
[2025-01-15 14:23:02] INFO  - Order placed successfully. OrderId: 3158563829
```

| Log Level | Output |
|---|---|
| `DEBUG` | Full request params, API response body → **file only** |
| `INFO` | Order summary, status, success/failure → **console + file** |
| `WARNING` | Validation issues caught pre-flight → **console + file** |
| `ERROR` | API errors, exceptions with full traceback → **console + file** |

---

## 🛡️ Input Validation

Before any API call is made, `validators.py` performs pre-flight checks:

- ✅ Symbol format — uppercase, non-empty, matches expected pattern
- ✅ Side — must be exactly `BUY` or `SELL`
- ✅ Order type — must be `MARKET` or `LIMIT`
- ✅ Quantity — must be a positive number above minimum lot size
- ✅ Price — required and positive for LIMIT orders; rejected for MARKET orders
- ✅ Credentials — environment variables must be set before any request

Validation failures raise clear, descriptive errors **before** any network call is made.

---

## 📐 Design Decisions

| Decision | Rationale |
|---|---|
| **No official SDK** | Direct REST + HMAC implementation demonstrates deep API understanding |
| **`requests` only** | Minimal external dependency footprint |
| **`timeInForce=GTC`** | Industry-standard default for limit orders |
| **USDT-M Futures only** | Scope-bound to perpetual contracts on testnet |
| **Env vars for secrets** | Follows 12-factor app methodology; zero hardcoded credentials |
| **Modular package layout** | Each concern (`client`, `orders`, `validators`, `logging`) is isolated for testability |
| **Dual-level logging** | Console for operator awareness; file for full audit trail and debugging |

---

## 🧰 Tech Stack

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Requests-HTTP%20Library-20232A?style=for-the-badge&logo=python&logoColor=61DAFB"/>
  <img src="https://img.shields.io/badge/HMAC--SHA256-Security-red?style=for-the-badge&logo=letsencrypt&logoColor=white"/>
  <img src="https://img.shields.io/badge/argparse-CLI-607D8B?style=for-the-badge&logo=gnubash&logoColor=white"/>
  <img src="https://img.shields.io/badge/logging-Audit%20Trail-4CAF50?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Binance%20API-F0B90B?style=for-the-badge&logo=binance&logoColor=black"/>
</p>

---

## 📁 File Reference

| File | Purpose |
|---|---|
| `cli.py` | Entry point; parses CLI args via `argparse` and calls order functions |
| `bot/client.py` | Signs requests (HMAC-SHA256), manages API base URL, sends HTTP calls |
| `bot/orders.py` | Constructs and dispatches MARKET / LIMIT order payloads |
| `bot/validators.py` | Pre-flight input validation; raises descriptive errors early |
| `bot/logging_config.py` | Configures shared logger with console + rotating file handlers |
| `.env.example` | Template for API key/secret environment variables |
| `requirements.txt` | Pinned dependencies (`requests==2.32.3`) |

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer" width="100%"/>

**Built with Python · No SDK · Pure REST + HMAC**

*Aashish Chandr — [GitHub](https://github.com/Aashish-Chandr)*

</div>
