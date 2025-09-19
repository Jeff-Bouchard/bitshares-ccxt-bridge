import os
import sys
import json
import time

# Ensure local shim can be imported
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import ccxt  # type: ignore
from octobot_shim.bitshares_dex import bitshares_dex

# Register into ccxt namespace for convenience (optional)
ccxt.bitshares_dex = bitshares_dex

BASE_URL = os.environ.get('BITSHARES_CCXT_BRIDGE_URL', 'http://localhost:8787')
VERBOSE = ('--verbose' in sys.argv) or (os.environ.get('VERBOSE', '0').lower() in ['1', 'true', 'yes'])

def vprint(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)


def assert_keys(obj, keys, name):
    missing = [k for k in keys if k not in obj]
    if missing:
        raise AssertionError(f"{name} missing keys: {missing}")


def pass_msg(label, extra=None):
    print(f"PASS: {label}" + (f" -> {extra}" if extra is not None else ""))


def fail_msg(label, err):
    print(f"FAIL: {label}: {err}")


def main():
    # Accept first CLI arg as public-balance account if provided and not an option
    cli_account = None
    for arg in sys.argv[1:]:
        if not arg.startswith('-'):
            cli_account = arg
            break

    ex = bitshares_dex({
        'options': {
            'baseUrl': BASE_URL,
            # Auto-login will use apiKey/secret or env BTS_* if provided
        },
        # You can also pass credentials here for sign-in:
        # 'apiKey': os.environ.get('BTS_ACCOUNT'),
        # 'secret': os.environ.get('BTS_WIF'),
    })

    print('Using API base URL:', BASE_URL)
    if cli_account:
        print('Public balance account (CLI):', cli_account)
    elif os.environ.get('PUBLIC_BALANCE_ACCOUNT'):
        print('Public balance account (ENV PUBLIC_BALANCE_ACCOUNT):', os.environ.get('PUBLIC_BALANCE_ACCOUNT'))
    elif os.environ.get('BTS_ACCOUNT'):
        print('Public balance account (ENV BTS_ACCOUNT):', os.environ.get('BTS_ACCOUNT'))

    # 1) describe()
    try:
        d = ex.describe()
        assert d['id'] == 'bitshares-dex'
        vprint('describe():', json.dumps(d, indent=2))
        pass_msg('describe() id')
    except Exception as e:
        return fail_msg('describe()', e)

    # 2) fetch_markets()
    try:
        mkts = ex.fetch_markets()
        assert isinstance(mkts, list) and len(mkts) > 0
        m0 = mkts[0]
        assert_keys(m0, ['id', 'symbol', 'base', 'quote', 'active'], 'market object')
        vprint('markets sample:', json.dumps(mkts[:2], indent=2))
        pass_msg('fetch_markets()', len(mkts))
    except Exception as e:
        return fail_msg('fetch_markets()', e)

    # Pick a symbol that exists (from markets)
    sym = mkts[0]['symbol']

    # 3) fetch_ticker(symbol)
    try:
        t = ex.fetch_ticker(sym)
        assert_keys(t, ['symbol', 'last', 'bid', 'ask', 'baseVolume', 'quoteVolume', 'timestamp', 'info'], 'ticker')
        assert t['symbol'] == sym
        vprint('ticker full:', json.dumps(t, indent=2))
        pass_msg('fetch_ticker()', json.dumps({k: t[k] for k in ['last', 'bid', 'ask']}))
    except Exception as e:
        return fail_msg('fetch_ticker()', e)

    # 4) fetch_order_book(symbol)
    try:
        ob = ex.fetch_order_book(sym, limit=10)
        assert_keys(ob, ['symbol', 'timestamp', 'bids', 'asks', 'info'], 'orderbook')
        assert isinstance(ob['bids'], list) and isinstance(ob['asks'], list)
        vprint('orderbook bids sample:', ob['bids'][:3])
        vprint('orderbook asks sample:', ob['asks'][:3])
        pass_msg('fetch_order_book()', f"bids={len(ob['bids'])} asks={len(ob['asks'])}")
    except Exception as e:
        return fail_msg('fetch_order_book()', e)

    # 5) fetch_trades(symbol)
    try:
        trades = ex.fetch_trades(sym, limit=5)
        assert isinstance(trades, list)
        if trades:
            tt = trades[0]
            assert_keys(tt, ['id', 'symbol', 'timestamp', 'datetime', 'price', 'amount', 'side', 'info'], 'trade')
        vprint('trades sample:', json.dumps(trades[:2], indent=2))
        pass_msg('fetch_trades()', len(trades))
    except Exception as e:
        return fail_msg('fetch_trades()', e)

    # 6) fetch_ohlcv(symbol)
    try:
        ohlcv = ex.fetch_ohlcv(sym, limit=3)
        assert isinstance(ohlcv, list)
        if ohlcv:
            c = ohlcv[0]
            assert isinstance(c, list) and len(c) == 6
        vprint('ohlcv sample:', ohlcv[:2])
        pass_msg('fetch_ohlcv()', len(ohlcv))
    except Exception as e:
        return fail_msg('fetch_ohlcv()', e)

    # 7) fetch_balance()
    # Try private first; if credentials not available, attempt public balance using an account name.
    try:
        bal = None
        try:
            bal = ex.fetch_balance()
        except Exception as e1:
            # Accept first CLI arg as account as well
            cli_acct = sys.argv[1] if len(sys.argv) > 1 else None
            acct = os.environ.get('BTS_ACCOUNT') or os.environ.get('PUBLIC_BALANCE_ACCOUNT') or cli_acct
            if acct:
                bal = ex.fetch_balance({'account': acct})
            else:
                raise e1
        assert isinstance(bal, dict)
        assert_keys(bal, ['info', 'free', 'used', 'total'], 'balance')
        vprint('balance total currencies:', list(bal['total'].items())[:5])
        pass_msg('fetch_balance()', f"currencies={len(bal['total'])}")
    except Exception as e:
        print('WARN: fetch_balance() skipped or failed (provide BTS_ACCOUNT or PUBLIC_BALANCE_ACCOUNT to test public balance):', e)

    print('\nAll checks attempted. See PASS/FAIL above.')


if __name__ == '__main__':
    main()
