# Auto-register the BitShares DEX shim into ccxt namespace on package import
from .bitshares_dex import bitshares_dex  # noqa: F401

try:
    import ccxt  # type: ignore
    # Register so users can reference ccxt.bitshares_dex
    ccxt.bitshares_dex = bitshares_dex  # type: ignore[attr-defined]
except Exception:
    # ccxt not installed or registration failed; consumers can still import class directly
    pass
