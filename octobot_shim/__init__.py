# Auto-register the BitShares DEX shim into ccxt namespace on package import
from .bitshares_dex import bitshares_dex  # noqa: F401

try:
    import ccxt  # type: ignore
    # Register so users can reference ccxt.bitshares_dex
    ccxt.bitshares_dex = bitshares_dex  # type: ignore[attr-defined]
    # Ensure the exchange id is visible in ccxt.exchanges list for tools that rely on it (like OctoBot)
    try:
        if hasattr(ccxt, "exchanges") and "bitshares_dex" not in getattr(ccxt, "exchanges", []):
            ccxt.exchanges.append("bitshares_dex")  # type: ignore[attr-defined]
    except Exception:
        # exchanges list might be immutable or unavailable in some environments; safe to ignore
        pass

    # Also register into ccxt.async_support, which OctoBot uses for some operations
    try:
        import ccxt.async_support as ccxt_async  # type: ignore
        ccxt_async.bitshares_dex = bitshares_dex  # type: ignore[attr-defined]
        if hasattr(ccxt_async, "exchanges") and "bitshares_dex" not in getattr(ccxt_async, "exchanges", []):
            ccxt_async.exchanges.append("bitshares_dex")  # type: ignore[attr-defined]
    except Exception:
        # async_support may not be available or may have a different API; ignore silently
        pass
except Exception:
    # ccxt not installed or registration failed; consumers can still import class directly
    pass
