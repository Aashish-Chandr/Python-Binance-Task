from bot.logging_config import setup_logger

logger = setup_logger("validators")

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_inputs(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: str | None,
) -> tuple[str, str, str, float, float | None]:
    """
    Validate and normalise all CLI inputs.

    Returns:
        (symbol, side, order_type, quantity, price)

    Raises:
        ValueError: on any invalid input.
    """
    # --- symbol ---
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string, e.g. BTCUSDT.")
    symbol = symbol.strip().upper()

    # --- side ---
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValueError(f"Side must be one of {sorted(VALID_SIDES)}. Got: '{side}'.")

    # --- order type ---
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(
            f"Order type must be one of {sorted(VALID_ORDER_TYPES)}. Got: '{order_type}'."
        )

    # --- quantity ---
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError()
    except (ValueError, TypeError):
        raise ValueError("Quantity must be a positive number, e.g. 0.01.")

    # --- price (required only for LIMIT) ---
    parsed_price: float | None = None
    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders (use --price).")
        try:
            parsed_price = float(price)
            if parsed_price <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            raise ValueError("Price must be a positive number, e.g. 30000.50.")

    logger.debug(
        "Validation passed | symbol=%s side=%s type=%s qty=%s price=%s",
        symbol, side, order_type, qty, parsed_price,
    )
    return symbol, side, order_type, qty, parsed_price
