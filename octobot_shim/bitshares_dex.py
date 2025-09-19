import os
import time
import requests
import ccxt


class bitshares_dex(ccxt.Exchange):
    """
    OctoBot/CCXT-compatible shim that forwards CCXT calls to the local
    BitShares bridge REST API started by this repo (src/rest/server.ts).

    Default REST base URL: http://localhost:8787
    Override with env BITSHARES_CCXT_BRIDGE_URL or with exchange option `baseUrl`.
    """

    def describe(self):
        base = super().describe()
        return self.deep_extend(base, {
            'id': 'bitshares-dex',
            'name': 'BitShares DEX (via local CCXT bridge)',
            'countries': ['XBS'],
            'rateLimit': 200,
            'pro': False,
            'has': {
                'fetchMarkets': True,
                'fetchTicker': True,
                'fetchOrderBook': True,
                'fetchTrades': True,
                'fetchOHLCV': True,
                'fetchBalance': True,
                'createOrder': True,
                'cancelOrder': True,
                'fetchOpenOrders': True,
                # Shim-only convenience: will auto-login using apiKey/secret or options
                'signIn': True,
            },
            'timeframes': {
                # The backend currently returns 1h candles via fetchOHLCV();
                # extend when more granularities are added.
                '1h': '1h',
            },
            'urls': {
                'api': self._base_url(),
            },
            'options': {
                'baseUrl': self._base_url(),
                # Optional auth options: if provided, shim will auto sign-in on first private call
                # 'account': 'your-bts-account',
                # 'keyOrPassword': 'your-active-key-or-password',
                # 'isPassword': False,
                # 'node': 'wss://node.xbts.io/ws',
            }
        })

    # --------------- Helpers ---------------
    def _base_url(self):
        return self.options.get('baseUrl') or os.environ.get('BITSHARES_CCXT_BRIDGE_URL', 'http://localhost:8787')

    def _get(self, path, params=None):
        url = f"{self._base_url()}{path}"
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        return r.json()

    def _post(self, path, data=None):
        url = f"{self._base_url()}{path}"
        r = requests.post(url, json=data or {}, timeout=30)
        r.raise_for_status()
        return r.json()

    def _delete(self, path, params=None):
        url = f"{self._base_url()}{path}"
        r = requests.delete(url, params=params or {}, timeout=20)
        r.raise_for_status()
        return r.json()

    # Manage login state
    _logged_in = False

    def _ensure_logged_in(self):
        """
        Ensure we've authenticated to the bridge before making private calls.
        Credential precedence:
        1) options.account / options.keyOrPassword / options.isPassword / options.node
        2) self.apiKey (as account) and self.secret (as key/password)
        3) env BTS_ACCOUNT / BTS_WIF / BTS_IS_PASSWORD / BTS_NODE
        """
        if self._logged_in:
            return

        # From options
        account = self.safe_value(self.options, 'account')
        key_or_password = self.safe_value(self.options, 'keyOrPassword')
        is_password = self.safe_value(self.options, 'isPassword')
        node = self.safe_value(self.options, 'node')

        # Fallback to CCXT standard credentials
        if account is None and getattr(self, 'apiKey', None):
            account = self.apiKey
        if key_or_password is None and getattr(self, 'secret', None):
            key_or_password = self.secret
        if is_password is None and os.environ.get('BTS_IS_PASSWORD') is not None:
            is_password = os.environ.get('BTS_IS_PASSWORD', 'false').lower() in ['1', 'true', 'yes']

        # Fallback to env vars
        if account is None:
            account = os.environ.get('BTS_ACCOUNT')
        if key_or_password is None:
            key_or_password = os.environ.get('BTS_WIF')
        if is_password is None:
            is_password = os.environ.get('BTS_IS_PASSWORD', 'false').lower() in ['1', 'true', 'yes']
        if node is None:
            node = os.environ.get('BTS_NODE')

        if not account or not key_or_password:
            # Defer login; private calls will fail server-side if not configured
            return

        self.sign_in(account, key_or_password, bool(is_password), node)
        self._logged_in = True

    # --------------- CCXT surface ---------------
    def fetch_markets(self, params={}):
        return self._get('/markets')

    def fetch_ticker(self, symbol, params={}):
        return self._get('/ticker', { 'symbol': symbol, **params })

    def fetch_order_book(self, symbol, limit=None, params={}):
        p = { 'symbol': symbol, **params }
        if limit is not None:
            p['limit'] = int(limit)
        return self._get('/orderbook', p)

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        p = { 'symbol': symbol, **params }
        if since is not None:
            p['since'] = int(since)
        if limit is not None:
            p['limit'] = int(limit)
        return self._get('/trades', p)

    def fetch_ohlcv(self, symbol, timeframe='1h', since=None, limit=None, params={}):
        # Backend returns raw OHLCV list: [timestamp, O, H, L, C, V]
        # Timeframe selection is not yet exposed; when added, pass it through here.
        data = self._get('/ohlcv', { 'symbol': symbol, **params })
        if since is not None:
            data = [c for c in data if c[0] >= int(since)]
        if limit is not None:
            data = data[-int(limit):]
        return data

    # ---- Account/auth ----
    def sign_in(self, account: str, key_or_password: str, is_password: bool = False, node: str | None = None):
        body = {
            'account': account,
            'keyOrPassword': key_or_password,
            'isPassword': bool(is_password),
            'node': node,
        }
        return self._post('/login', body)

    def fetch_balance(self, params={}):
        # Try private path first
        if self._logged_in is False:
            # Attempt auto-login (may be skipped if no creds)
            self._ensure_logged_in()
        if self._logged_in:
            raw = self._get('/balance')
            return self._unify_balance(raw)
        # Fallback to public balance by account
        account = (
            self.safe_value(params, 'account')
            or self.safe_value(self.options, 'account')
            or getattr(self, 'apiKey', None)
            or os.environ.get('BTS_ACCOUNT')
        )
        if not account:
            raise ccxt.ArgumentsRequired('bitshares_dex.fetch_balance requires credentials or params.account for public balance')
        raw = self._get('/balancePublic', { 'account': account })
        return self._unify_balance(raw)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        # Symbol filtering can be added client-side if needed
        self._ensure_logged_in()
        return self._get('/openOrders', params)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type != 'limit':
            raise ccxt.NotSupported('Only limit orders are supported by BitShares DEX bridge')
        body = {
            'symbol': symbol,
            'type': type,
            'side': side,
            'amount': amount,
            'price': price,
            'params': params,
        }
        self._ensure_logged_in()
        return self._post('/order', body)

    def cancel_order(self, id, symbol=None, params={}):
        self._ensure_logged_in()
        return self._delete('/order', { 'id': id, **params })

    # --------------- Unifiers ---------------
    def _unify_balance(self, raw):
        """
        Convert various possible BitShares balance payloads to CCXT unified format.
        Returns a dict like:
        {
          'info': raw,
          'free': { 'BTS': 1.23, ... },
          'used': { 'BTS': 0.0, ... },
          'total': { 'BTS': 1.23, ... }
        }
        If we cannot distinguish free/used, we put the total in both free and total and 0 in used.
        """
        result = {
            'info': raw,
            'free': {},
            'used': {},
            'total': {},
        }

        def add(cur, total=None, free=None, used=None):
            if cur is None:
                return
            cur = str(cur)
            if total is None and free is not None and used is not None:
                total = float(free) + float(used)
            if free is None and total is not None and used is not None:
                free = float(total) - float(used)
            if used is None and total is not None and free is not None:
                used = float(total) - float(free)
            # Last resort: if only total known
            if free is None and total is not None and used is None:
                free = float(total)
                used = 0.0
            # Normalize to floats
            if total is not None:
                total = float(total)
            if free is not None:
                free = float(free)
            if used is not None:
                used = float(used)
            if total is None and free is None and used is None:
                return
            result['total'][cur] = total if total is not None else (free + used if free is not None and used is not None else 0.0)
            result['free'][cur] = free if free is not None else (total - used if total is not None and used is not None else 0.0)
            result['used'][cur] = used if used is not None else (total - free if total is not None and free is not None else 0.0)

        # Case 1: raw already CCXT-like
        if isinstance(raw, dict) and ('free' in raw or 'total' in raw):
            # Try to preserve as-is but ensure numeric types
            for part in ['free', 'used', 'total']:
                if part in raw and isinstance(raw[part], dict):
                    for k, v in raw[part].items():
                        try:
                            result[part][k] = float(v)
                        except Exception:
                            pass
            result['info'] = raw.get('info', raw)
            return result

        # Case 2: list of objects (typical from BitShares libs)
        if isinstance(raw, list):
            for item in raw:
                if not isinstance(item, dict):
                    continue
                symbol = item.get('symbol') or item.get('asset') or item.get('currency') or item.get('name')
                total = item.get('total') or item.get('amount') or item.get('balance') or item.get('value')
                free = item.get('free') or item.get('available')
                used = item.get('used') or item.get('locked') or item.get('hold')
                add(symbol, total=total, free=free, used=used)
            return result

        # Case 3: dict mapping currency->amount
        if isinstance(raw, dict):
            for k, v in raw.items():
                # Skip non-currency keys
                if k in ['info', 'success', 'status']:
                    continue
                add(k, total=v)
            return result

        # Fallback: unknown structure
        return result


# Quick manual test (optional): run this file directly
if __name__ == '__main__':
    ex = bitshares_dex({ 'options': { 'baseUrl': os.environ.get('BITSHARES_CCXT_BRIDGE_URL', 'http://localhost:8787') } })
    print('describe:', ex.describe())
    mkts = ex.fetch_markets()
    print('markets:', len(mkts))
    sym = 'NESS/BTS'
    print('ticker:', ex.fetch_ticker(sym))
    print('orderbook bids:', len(ex.fetch_order_book(sym, limit=10)['bids']))
    print('trades sample:', ex.fetch_trades(sym, limit=3))
    print('ohlcv sample:', ex.fetch_ohlcv(sym, limit=2))
