# BitShares CCXT Bridge - API Documentation

## Overview

The BitShares CCXT Bridge provides a comprehensive REST API and programmatic interface for interacting with the BitShares decentralized exchange. This document covers all available endpoints, parameters, and response formats.

## Base URL

```
http://localhost:8787
```

## Authentication

Most market data endpoints are public and require no authentication. Trading endpoints require account login via the `/login` endpoint or by configuring credentials in the `.env` file.

## Response Format

All API responses are in JSON format. Successful responses return the requested data, while errors return an object with an `error` field:

```json
{
  "error": "Error message description"
}
```

## Market Data Endpoints

### GET /describe

Returns exchange information and initializes the market cache.

**Response:**
```json
{
  "id": "bitshares-dex",
  "name": "BitShares DEX (CCXT bridge)"
}
```

### GET /markets

Returns all available trading pairs with metadata.

**Response:**
```json
[
  {
    "id": "BTS_USDT",
    "symbol": "BTS/USDT",
    "base": "BTS",
    "quote": "USDT",
    "active": true,
    "type": "spot",
    "spot": true,
    "precision": {
      "price": 8,
      "amount": 8
    },
    "limits": {
      "amount": { "min": null, "max": null },
      "price": { "min": null, "max": null },
      "cost": { "min": null, "max": null }
    }
  }
]
```

### GET /ticker

Returns price ticker for a specific trading pair.

**Parameters:**
- `symbol` (required): Trading pair symbol (e.g., "BTS/USDT")

**Example:**
```http
GET /ticker?symbol=BTS/USDT
```

**Response:**
```json
{
  "symbol": "BTS/USDT",
  "last": 730.40467672,
  "bid": 720.0,
  "ask": 738.4075986,
  "baseVolume": 31222.61175,
  "quoteVolume": 42.865474,
  "percentage": 0.5,
  "timestamp": 1758153085000,
  "info": {
    "base_id": 463,
    "quote_id": 825,
    "base_symbol": "BTS",
    "quote_symbol": "USDT",
    "last": "730.40467672",
    "sell": "738.40759860",
    "buy": "720.00000000",
    "base_volume": "31222.61175",
    "quote_volume": "42.865474",
    "change": "0.5",
    "type": "spot",
    "isFrozen": 0,
    "url": "https://ex.xbts.io/market/XBTSX.USDT_BTS",
    "timestamp": 1758153085
  }
}
```

### GET /orderbook

Returns order book (bids and asks) for a trading pair.

**Parameters:**
- `symbol` (required): Trading pair symbol
- `limit` (optional): Number of orders to return (default: 50)

**Example:**
```http
GET /orderbook?symbol=BTS/USDT&limit=20
```

**Response:**
```json
{
  "symbol": "BTS/USDT",
  "timestamp": 1758153085000,
  "bids": [
    [720.0, 100.5],
    [719.5, 50.25]
  ],
  "asks": [
    [738.41, 75.0],
    [739.0, 25.5]
  ],
  "info": {
    "timestamp": 1758153085,
    "bids": [...],
    "asks": [...]
  }
}
```

### GET /trades

Returns recent trade history for a trading pair.

**Parameters:**
- `symbol` (required): Trading pair symbol
- `since` (optional): Timestamp to fetch trades from
- `limit` (optional): Number of trades to return (default: 100)

**Example:**
```http
GET /trades?symbol=BTS/USDT&limit=50
```

**Response:**
```json
[
  {
    "id": "12345",
    "symbol": "BTS/USDT",
    "timestamp": 1758153085000,
    "datetime": "2025-09-17T23:58:05.000Z",
    "price": 730.40467672,
    "amount": 10.5,
    "side": "buy",
    "info": {
      "trade_id": 12345,
      "timestamp": 1758153085,
      "price": "730.40467672",
      "quote_volume": "10.5",
      "type": "buy"
    }
  }
]
```

### GET /ohlcv

Returns OHLCV (candlestick) data for a trading pair.

**Parameters:**
- `symbol` (required): Trading pair symbol
- `timeframe` (optional): Time interval (currently ignored by backend)

**Example:**
```http
GET /ohlcv?symbol=BTS/USDT&timeframe=1h
```

**Response:**
```json
[
  [1758153085000, 720.0, 740.0, 715.0, 738.41, 1250.5],
  [1758149485000, 715.0, 725.0, 710.0, 720.0, 980.25]
]
```

Each array contains: `[timestamp, open, high, low, close, volume]`

### GET /currencies

Returns all available currencies with metadata (CCXT compliance).

**Response:**
```json
{
  "BTS": {
    "id": "BTS",
    "code": "BTS",
    "name": "BTS",
    "active": true,
    "precision": 8,
    "limits": {
      "amount": {"min": null, "max": null},
      "withdraw": {"min": null, "max": null}
    },
    "info": {}
  },
  "NESS": {
    "id": "NESS",
    "code": "NESS",
    "name": "NESS",
    "active": true,
    "precision": 8,
    "limits": {
      "amount": {"min": null, "max": null},
      "withdraw": {"min": null, "max": null}
    },
    "info": {}
  }
}
```

### GET /tradingFees

Returns trading fee structure (CCXT compliance).

**Response:**
```json
{
  "trading": {
    "maker": 0.001,
    "taker": 0.001,
    "percentage": true,
    "tierBased": false
  },
  "funding": {
    "withdraw": {},
    "deposit": {}
  }
}
```

### GET /tradingLimits

Returns trading limits for all or specific symbols (CCXT compliance).

**Parameters:**
- `symbols` (optional): Comma-separated list of symbols to get limits for

**Example:**
```http
GET /tradingLimits?symbols=BTS/USDT,BTS/CNY
```

**Response:**
```json
{
  "BTS/USDT": {
    "amount": {"min": 1e-8, "max": 1000000000},
    "price": {"min": 1e-8, "max": 1000000000},
    "cost": {"min": 1e-8}
  },
  "BTS/CNY": {
    "amount": {"min": 1e-8, "max": 1000000000},
    "price": {"min": 1e-8, "max": 1000000000},
    "cost": {"min": 1e-8}
  }
}
```

## Trading Endpoints

### POST /login

Authenticate with your BitShares account for trading operations.

**Request Body:**
```json
{
  "account": "your-account-name",
  "keyOrPassword": "5YourPrivateKeyHere...",
  "isPassword": false,
  "node": "wss://node.xbts.io/ws"
}
```

**Parameters:**
- `account` (required): BitShares account name
- `keyOrPassword` (required): Private key (WIF format) or password
- `isPassword` (optional): Set to true if using password instead of private key
- `node` (optional): BitShares node WebSocket URL

**Response:**
```json
{
  "ok": true
}
```

### GET /balance

Returns account balances (requires login).

**Response:**
```json
{
  "BTS": {
    "free": 1000.0,
    "used": 100.0,
    "total": 1100.0
  },
  "USDT": {
    "free": 500.0,
    "used": 0.0,
    "total": 500.0
  }
}
```

### GET /balancePublic

Returns public balance for any BitShares account (no login required).

**Parameters:**
- `account` (required): BitShares account name to query

**Example:**
```http
GET /balancePublic?account=some-account
```

**Response:**
```json
{
  "BTS": {
    "free": 1000.0,
    "used": 0.0,
    "total": 1000.0
  }
}
```

### POST /order

Create a new limit order (requires login).

**Request Body:**
```json
{
  "symbol": "BTS/USDT",
  "type": "limit",
  "side": "buy",
  "amount": 100.0,
  "price": 700.0,
  "params": {}
}
```

**Parameters:**
- `symbol` (required): Trading pair symbol
- `type` (required): Order type (currently only "limit" supported)
- `side` (required): "buy" or "sell"
- `amount` (required): Order amount in base currency
- `price` (required): Order price
- `params` (optional): Additional order parameters

**Response:**
```json
{
  "id": "order-id-12345",
  "symbol": "BTS/USDT",
  "type": "limit",
  "side": "buy",
  "amount": 100.0,
  "price": 700.0,
  "status": "open",
  "timestamp": 1758153085000
}
```

### DELETE /order

Cancel an existing order (requires login).

**Parameters:**
- `id` (required): Order ID to cancel

**Example:**
```http
DELETE /order?id=order-id-12345
```

**Response:**
```json
{
  "id": "order-id-12345",
  "status": "canceled"
}
```

### GET /openOrders

Returns all open orders for the authenticated account (requires login).

**Parameters:**
- `symbol` (optional): Filter by trading pair
- `since` (optional): Filter orders after timestamp
- `limit` (optional): Maximum number of orders to return

**Example:**
```http
GET /openOrders?symbol=BTS/USDT&limit=10
```

**Response:**
```json
[
  {
    "id": "order-id-12345",
    "symbol": "BTS/USDT",
    "type": "limit",
    "side": "buy",
    "amount": 100.0,
    "price": 700.0,
    "filled": 0,
    "remaining": 100.0,
    "status": "open",
    "timestamp": 1758153085000,
    "datetime": "2025-01-15T10:30:00.000Z"
  }
]
```

### GET /order/:id

Returns details for a specific order by ID (CCXT compliance).

**Parameters:**
- `id` (required): Order ID in URL path
- `symbol` (optional): Trading pair symbol

**Example:**
```http
GET /order/1.7.12345?symbol=BTS/USDT
```

**Response:**
```json
{
  "id": "1.7.12345",
  "symbol": "BTS/USDT",
  "type": "limit",
  "side": "buy",
  "amount": 100.0,
  "price": 700.0,
  "filled": 0,
  "remaining": 100.0,
  "status": "open",
  "timestamp": 1758153085000,
  "datetime": "2025-01-15T10:30:00.000Z"
}
```

### GET /orders

Returns order history for the authenticated account (CCXT compliance).

**Parameters:**
- `symbol` (optional): Filter by trading pair
- `since` (optional): Filter orders after timestamp
- `limit` (optional): Maximum number of orders to return

**Example:**
```http
GET /orders?symbol=BTS/USDT&limit=50
```

**Response:**
```json
[
  {
    "id": "order-id-12345",
    "symbol": "BTS/USDT",
    "type": "limit",
    "side": "buy",
    "amount": 100.0,
    "price": 700.0,
    "filled": 50.0,
    "remaining": 50.0,
    "status": "open",
    "timestamp": 1758153085000,
    "datetime": "2025-01-15T10:30:00.000Z"
  }
]
```

### GET /myTrades

Returns trade history for the authenticated account (CCXT compliance).

**Parameters:**
- `symbol` (optional): Filter by trading pair
- `since` (optional): Filter trades after timestamp
- `limit` (optional): Maximum number of trades to return

**Example:**
```http
GET /myTrades?symbol=BTS/USDT&limit=100
```

**Response:**
```json
[
  {
    "id": "trade-id-67890",
    "symbol": "BTS/USDT",
    "side": "buy",
    "amount": 50.0,
    "price": 700.0,
    "cost": 35000.0,
    "fee": {"currency": "BTS", "cost": 0.05},
    "timestamp": 1758153085000,
    "datetime": "2025-01-15T10:30:00.000Z"
  }
]
```

### PUT /order/:id

Edit an existing order (CCXT compliance). Note: BitShares doesn't support direct order editing, so this cancels the original order and creates a new one.

**Parameters:**
- `id` (required): Order ID in URL path

**Request Body:**
```json
{
  "symbol": "BTS/USDT",
  "type": "limit",
  "side": "buy",
  "amount": 150.0,
  "price": 720.0,
  "params": {}
}
```

**Response:**
```json
{
  "id": "new-order-id-54321",
  "symbol": "BTS/USDT",
  "type": "limit",
  "side": "buy",
  "amount": 150.0,
  "price": 720.0,
  "status": "open",
  "timestamp": 1758153085000
}
```

## Error Codes

| HTTP Status | Error Type | Description |
|-------------|------------|-------------|
| 400 | Bad Request | Missing required parameters |
| 401 | Unauthorized | Authentication required |
| 404 | Not Found | Endpoint or resource not found |
| 500 | Internal Server Error | Server-side error |

## Rate Limits

The API uses the XBTS market data service, which has its own rate limits. For high-frequency applications, consider implementing caching or using WebSocket connections for real-time data.

## WebSocket Support

Currently, the bridge uses HTTP polling for market data. WebSocket support for real-time updates is planned for future versions.

## CCXT Compatibility

The API is designed to be compatible with the CCXT library structure. You can use standard CCXT methods when using the programmatic interface:

```javascript
const exchange = new BitSharesCCXT();
await exchange.loadMarkets();
const ticker = await exchange.fetchTicker('BTS/USDT');
const orderbook = await exchange.fetchOrderBook('BTS/USDT');
```

## Supported Trading Pairs

The bridge supports all trading pairs available on the XBTS exchange. Popular pairs include:

**Major Pairs:**
- BTS/USDT, BTS/USD, BTS/CNY, BTS/RUB
- BTC/USDT, ETH/USDT, LTC/USDT

**Custom Tokens:**
- BTS/NESS, BTS/SCH, BTS/NCH
- BTC/NESS, BTC/SCH, BTC/NCH
- ETH/NESS, ETH/SCH
- STH/NESS, STH/SCH

Use the `/markets` endpoint to get the complete list of available pairs.

## Testing

Use the provided testing scripts to verify API functionality:

```bash
./test-api.sh       # Test all endpoints
./test-pairs.sh     # Test specific trading pairs
```

## Examples

### Market Data Example

```bash
# Get all markets
curl "http://localhost:8787/markets"

# Get BTS/USDT ticker
curl "http://localhost:8787/ticker?symbol=BTS/USDT"

# Get order book
curl "http://localhost:8787/orderbook?symbol=BTS/USDT&limit=10"

# Get recent trades
curl "http://localhost:8787/trades?symbol=BTS/USDT&limit=20"
```

### Trading Example

```bash
# Login
curl -X POST "http://localhost:8787/login" \
  -H "Content-Type: application/json" \
  -d '{
    "account": "your-account",
    "keyOrPassword": "5YourPrivateKey...",
    "isPassword": false
  }'

# Check balance
curl "http://localhost:8787/balance"

# Place buy order
curl -X POST "http://localhost:8787/order" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTS/USDT",
    "type": "limit",
    "side": "buy",
    "amount": 100,
    "price": 700
  }'

# Check open orders
curl "http://localhost:8787/openOrders"
```

## Security Considerations

1. **Private Keys**: Never expose private keys in URLs or logs
2. **HTTPS**: Use HTTPS in production environments
3. **Rate Limiting**: Implement client-side rate limiting to avoid API abuse
4. **Input Validation**: Always validate input parameters
5. **Error Handling**: Implement proper error handling for network issues

## Support

For API support and bug reports:
- Check the main README.md for troubleshooting
- Use `./test-api.sh` to diagnose issues
- Review server logs with `./logs.sh`
- Report issues on the project repository
