"""
cli.py — Entry point for the Binance Futures Testnet Trading Bot.

Usage examples:
    python cli.py --symbol BTCUSDT --side BUY  --order-type MARKET --quantity 0.01
    python cli.py --symbol BTCUSDT --side SELL --order-type LIMIT  --quantity 0.01 --price 95000
"""

import argparse
import sys

from bot.client import BinanceFuturesClient
from bot.logging_config import setup_logger
from bot.orders import place_order
from bot.validators import validate_inputs

logger = setup_logger("cli")


def _print_summary(symbol: str, side: str, order_type: str, quantity: float, price: float | None) -> None:
    print("\n╔══════════════ ORDER REQUEST ══════════════╗")
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Order Type : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price is not None:
        print(f"  Price      : {price}")
    print("╚═══════════════════════════════════════════╝\n")


def _print_response(response: dict) -> None:
    print("╔══════════════ ORDER RESPONSE ═════════════╗")
    print(f"  Order ID     : {response.get('orderId', 'N/A')}")
    print(f"  Status       : {response.get('status', 'N/A')}")
    print(f"  Executed Qty : {response.get('executedQty', 'N/A')}")
    avg = response.get("avgPrice") or response.get("price", "N/A")
    print(f"  Avg Price    : {avg}")
    print(f"  Symbol       : {response.get('symbol', 'N/A')}")
    print(f"  Client OID   : {response.get('clientOrderId', 'N/A')}")
    print("╚═══════════════════════════════════════════╝\n")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Place orders on Binance Futures Testnet (USDT-M).",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--symbol", required=True,
        help="Trading pair symbol, e.g. BTCUSDT",
    )
    parser.add_argument(
        "--side", required=True,
        help="Order side: BUY or SELL",
    )
    parser.add_argument(
        "--order-type", required=True, dest="order_type",
        help="Order type: MARKET or LIMIT",
    )
    parser.add_argument(
        "--quantity", required=True,
        help="Order quantity, e.g. 0.01",
    )
    parser.add_argument(
        "--price", required=False, default=None,
        help="Limit price (required for LIMIT orders), e.g. 95000",
    )
    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    logger.info(
        "CLI invoked | symbol=%s side=%s type=%s qty=%s price=%s",
        args.symbol, args.side, args.order_type, args.quantity, args.price,
    )

    try:
        # 1. Validate inputs
        symbol, side, order_type, quantity, price = validate_inputs(
            args.symbol, args.side, args.order_type, args.quantity, args.price
        )

        # 2. Print request summary
        _print_summary(symbol, side, order_type, quantity, price)

        # 3. Initialise client
        client = BinanceFuturesClient()

        # 4. Place order
        response = place_order(client, symbol, side, order_type, quantity, price)

        # 5. Print response
        _print_response(response)
        print("✅  Order placed successfully!")
        logger.info("Session complete — order placed successfully.")

    except ValueError as exc:
        print(f"\n❌  Validation error: {exc}\n")
        logger.warning("Validation error: %s", exc)
        sys.exit(1)

    except EnvironmentError as exc:
        print(f"\n❌  Configuration error: {exc}\n")
        logger.error("Configuration error: %s", exc)
        sys.exit(1)

    except RuntimeError as exc:
        print(f"\n❌  API error: {exc}\n")
        logger.error("API error: %s", exc)
        sys.exit(1)

    except Exception as exc:
        print(f"\n❌  Unexpected error: {exc}\n")
        logger.exception("Unexpected error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
