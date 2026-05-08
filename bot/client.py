import os

import requests
from bot.logging_config import setup_logger

logger = setup_logger("client")

TESTNET_BASE_URL = "https://demo-fapi.binance.com"


def get_credentials() -> tuple[str, str]:
    """Read API credentials from environment variables."""
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()

    if not api_key or not api_secret:
        raise EnvironmentError(
            "BINANCE_API_KEY and BINANCE_API_SECRET must be set as environment variables."
        )
    return api_key, api_secret


class BinanceFuturesClient:
    """
    Thin wrapper around the Binance Futures Testnet REST API.
    Uses direct HTTP calls (requests) so no third-party SDK is required.
    """

    def __init__(self) -> None:
        self.api_key, self.api_secret = get_credentials()
        self.base_url = TESTNET_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})
        logger.info("BinanceFuturesClient initialised (testnet: %s)", self.base_url)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _sign(self, params: dict) -> dict:
        """Append a HMAC-SHA256 signature to a parameter dict."""
        import hashlib
        import hmac
        import time

        params["timestamp"] = int(time.time() * 1000)
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _post(self, endpoint: str, params: dict) -> dict:
        """Sign and POST to a Futures endpoint; return parsed JSON."""
        signed = self._sign(params)
        url = f"{self.base_url}{endpoint}"
        logger.debug("POST %s | params=%s", url, {k: v for k, v in signed.items() if k != "signature"})

        response = self.session.post(url, params=signed, timeout=10)
        data = response.json()

        logger.debug("Response [%s]: %s", response.status_code, data)

        if not response.ok:
            code = data.get("code", response.status_code)
            msg = data.get("msg", response.text)
            raise RuntimeError(f"Binance API error {code}: {msg}")

        return data

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: float | None = None,
    ) -> dict:
        """Place a futures order and return the raw API response."""
        params: dict = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        return self._post("/fapi/v1/order", params)
