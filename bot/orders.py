from bot.client import BinanceFuturesClient
from bot.logging_config import setup_logger

logger = setup_logger("orders")


def place_order(
    client: BinanceFuturesClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None = None,
) -> dict:
    """
    Place a market or limit order via the provided client.

    Args:
        client:     Initialised BinanceFuturesClient.
        symbol:     Trading pair, e.g. 'BTCUSDT'.
        side:       'BUY' or 'SELL'.
        order_type: 'MARKET' or 'LIMIT'.
        quantity:   Order size.
        price:      Limit price (required when order_type == 'LIMIT').

    Returns:
        Raw API response dict.

    Raises:
        RuntimeError: on API-level errors.
        requests.RequestException: on network failures.
    """
    logger.info(
        "Placing %s %s order | symbol=%s qty=%s price=%s",
        side, order_type, symbol, quantity, price,
    )

    try:
        response = client.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )
        logger.info(
            "Order accepted | orderId=%s status=%s executedQty=%s avgPrice=%s",
            response.get("orderId"),
            response.get("status"),
            response.get("executedQty"),
            response.get("avgPrice"),
        )
        return response

    except RuntimeError as exc:
        logger.error("API error while placing order: %s", exc)
        raise

    except Exception as exc:
        logger.error("Unexpected error while placing order: %s", exc)
        raise
