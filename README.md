# BitShares CCXT Bridge

![version](https://img.shields.io/badge/version-0.2.0-blue.svg)
![Node.js](https://img.shields.io/badge/Node.js-20%2B-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**A production-ready CCXT-compatible adapter for the BitShares DEX with automated installation and management tools.**

This project provides a complete bridge between the BitShares decentralized exchange and the CCXT trading library ecosystem. It includes market data feeds, trading capabilities, and a REST API server with comprehensive tooling for easy deployment.

**🎯 Now with full CCXT compliance and OctoBot integration support!**

## 🚀 Features

- ✅ **Full CCXT Compliance** - Complete implementation of CCXT standard methods
- ✅ **OctoBot Ready** - Seamless integration with OctoBot trading platform
- ✅ **Enhanced Market Data** - Currencies, trading fees, limits, and real-time prices
- ✅ **Advanced Order Management** - Create, cancel, edit orders with full history
- ✅ **Personal Trade History** - Track your trading activity and performance
- ✅ **REST API Server** - 20+ HTTP endpoints for complete integration
- ✅ **One-Click Installation** - Automated setup wizard for non-technical users
- ✅ **Docker Support** - Containerized deployment
- ✅ **Comprehensive Testing** - Built-in CCXT compliance testing tools

## ⚡ One-Liner Quick Start

```bash
git clone https://github.com/your-repo/bitshares-ccxt-bridge.git && cd bitshares-ccxt-bridge && ./install.sh && ./start.sh
```

**Access your bridge at:** `http://localhost:8787`

## 📦 Detailed Installation

### For Non-Technical Users (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-repo/bitshares-ccxt-bridge.git
cd bitshares-ccxt-bridge

# Run the automated installer
./install.sh
```

The installer will:
- Check and install Node.js 20+ if needed
- Install all dependencies automatically
- Guide you through configuration with validation
- Test your setup to ensure everything works

### For Developers

```bash
# Prerequisites: Node.js 20+, npm 9+
npm install
npm run build
cp .env.example .env
# Edit .env with your BitShares credentials
npm start
```

## 🎮 Management Scripts

After installation, use these simple commands:

```bash
./start.sh          # Start the server
./stop.sh           # Stop the server  
./logs.sh           # View server logs
./test-api.sh       # Test all API endpoints
./test-pairs.sh     # Test specific BitShares pairs
```

## ⚙️ Configuration

The installer creates a `.env` file with these settings:

| Variable | Description | Default |
|----------|-------------|---------|
| `BTS_NODE` | BitShares WebSocket endpoint | `wss://node.xbts.io/ws` |
| `BTS_ACCOUNT` | Your BitShares account name | - |
| `BTS_WIF` | Your BitShares active private key | - |
| `XBTS_API` | Market data API endpoint | `https://cmc.xbts.io/v2` |
| `PORT` | REST API server port | `8787` |
| `NODE_ENV` | Environment mode | `production` |

⚠️ **Security Note**: Your private key is stored in the `.env` file. Keep this file secure and never share it.

## 🌐 REST API Reference

### Market Data Endpoints

#### Get All Markets
```http
GET /markets
```
Returns all available trading pairs with metadata.

#### Get Ticker
```http
GET /ticker?symbol=BTS/USDT
```
Returns price ticker for a specific symbol.

**Response:**
```json
{
  "symbol": "BTS/USDT",
  "last": 730.40467672,
  "bid": 720,
  "ask": 738.4075986,
  "baseVolume": 31222.61175,
  "quoteVolume": 42.865474,
  "percentage": 0.5,
  "timestamp": 1758153085000
}
```

#### Get Order Book
```http
GET /orderbook?symbol=BTS/USDT&limit=50
```
Returns order book with bids and asks.

#### Get Recent Trades
```http
GET /trades?symbol=BTS/USDT&limit=100
```
Returns recent trade history.

#### Get OHLCV Data
```http
GET /ohlcv?symbol=BTS/USDT&timeframe=1d
```
Returns candlestick/OHLCV data.

### Trading Endpoints

#### Login
```http
POST /login
Content-Type: application/json

{
  "account": "your-account",
  "keyOrPassword": "your-private-key",
  "isPassword": false,
  "node": "wss://node.xbts.io/ws"
}
```

#### Get Balance
```http
GET /balance
```
Returns your account balances (requires login).

#### Get Public Balance
```http
GET /balancePublic?account=some-account
```
Returns public balance for any account.

#### Create Order
```http
POST /order
Content-Type: application/json

{
  "symbol": "BTS/USDT",
  "type": "limit",
  "side": "buy",
  "amount": 100,
  "price": 700
}
```

#### Cancel Order
```http
DELETE /order?id=order-id
```

#### Get Open Orders
```http
GET /openOrders
```

## 💻 Programmatic Usage

### Basic Example

```typescript
import { BitSharesCCXT } from './dist/adapter.js';

async function main() {
  const exchange = new BitSharesCCXT();
  
  // Initialize and get markets
  await exchange.describe();
  const markets = await exchange.fetchMarkets();
  console.log(`Found ${markets.length} markets`);
  
  // Get ticker
  const ticker = await exchange.fetchTicker('BTS/USDT');
  console.log(`BTS/USDT: ${ticker.last}`);
  
  // Get order book
  const orderbook = await exchange.fetchOrderBook('BTS/USDT', 10);
  console.log(`Best bid: ${orderbook.bids[0][0]}`);
  console.log(`Best ask: ${orderbook.asks[0][0]}`);
}

main().catch(console.error);
```

### Trading Example

```typescript
import { BitSharesCCXT } from './dist/adapter.js';

async function tradingExample() {
  const exchange = new BitSharesCCXT();
  
  // Login to your account
  await exchange.login(
    'your-account-name',
    '5YourPrivateKeyHere...',
    false, // isPassword = false for private key
    'wss://node.xbts.io/ws'
  );
  
  // Check balance
  const balance = await exchange.fetchBalance();
  console.log('Balance:', balance);
  
  // Place a limit buy order
  const order = await exchange.createOrder(
    'BTS/USDT',
    'limit',
    'buy',
    100,    // amount
    700     // price
  );
  console.log('Order placed:', order);
  
  // Check open orders
  const openOrders = await exchange.fetchOpenOrders();
  console.log('Open orders:', openOrders);
  
  // Cancel order if needed
  // await exchange.cancelOrder(order.id);
}

tradingExample().catch(console.error);
```

### Available Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `describe()` | Initialize exchange info | - |
| `fetchMarkets()` | Get all available markets | - |
| `fetchTicker(symbol)` | Get price ticker | symbol |
| `fetchOrderBook(symbol, limit?)` | Get order book | symbol, limit |
| `fetchTrades(symbol, since?, limit?)` | Get trade history | symbol, since, limit |
| `fetchOHLCV(symbol, timeframe?)` | Get candlestick data | symbol, timeframe |
| `login(account, key, isPassword?, node?)` | Login to account | account, key, isPassword, node |
| `fetchBalance()` | Get account balance | - |
| `fetchPublicBalance(account)` | Get public balance | account |
| `createOrder(symbol, type, side, amount, price, params?)` | Place order | symbol, type, side, amount, price, params |
| `cancelOrder(id)` | Cancel order | order id |
| `fetchOpenOrders()` | Get open orders | - |

## 🧪 Testing Your Setup

### Test All Endpoints
```bash
./test-api.sh
```

### Test Specific Pairs
```bash
./test-pairs.sh
```

This tests your specific BitShares tokens:
- BTS/NESS, BTS/SCH, BTS/NCH
- BTC/NESS, BTC/SCH, BTC/NCH  
- ETH/NESS, ETH/SCH
- STH/NESS, STH/SCH

### Manual Testing
```bash
# Test market data
curl "http://localhost:8787/markets"
curl "http://localhost:8787/ticker?symbol=BTS/USDT"

# Test with your tokens
curl "http://localhost:8787/ticker?symbol=BTS/NESS"
curl "http://localhost:8787/ticker?symbol=BTS/SCH"
```

## 🐳 Docker Deployment

```bash
# Build image
docker build -t bitshares-ccxt-bridge .

# Run container
docker run -d \
  --name bitshares-bridge \
  -p 8787:8787 \
  --env-file .env \
  bitshares-ccxt-bridge
```

Or use docker-compose:
```bash
docker-compose up -d
```

## 🔧 Troubleshooting

### Server Won't Start
1. Check if port 8787 is already in use: `./stop.sh`
2. Verify Node.js version: `node --version` (needs 20+)
3. Rebuild project: `npm run build`
4. Check logs: `./logs.sh`

### API Returns Errors
1. Verify server is running: `curl http://localhost:8787/markets`
2. Check configuration: `cat .env`
3. Test with known pairs: `curl "http://localhost:8787/ticker?symbol=BTS/USDT"`
4. Restart server: `./stop.sh && ./start.sh`

### Trading Issues
1. Verify account name and private key in `.env`
2. Check BitShares node connectivity
3. Ensure account has sufficient balance
4. Test with small amounts first

### Common Error Messages

| Error | Solution |
|-------|----------|
| `EADDRINUSE` | Port already in use, run `./stop.sh` |
| `symbol required` | Add `?symbol=BTS/USDT` to URL |
| `Invalid private key` | Check WIF format (starts with '5') |
| `Connection failed` | Check BitShares node URL |

## 📊 Supported Markets

The bridge supports all markets available on the XBTS exchange, including:

**Major Pairs:**
- BTS/USDT, BTS/USD, BTS/CNY
- BTC/USDT, ETH/USDT, LTC/USDT

**Your Custom Tokens:**
- BTS/NESS, BTS/SCH, BTS/NCH
- BTC/NESS, BTC/SCH, BTC/NCH
- ETH/NESS, ETH/SCH
- STH/NESS, STH/SCH

**And many more...** Run `./test-api.sh` to see all available markets.

## 🔒 Security Best Practices

1. **Private Key Security**
   - Store private keys in `.env` file only
   - Set file permissions: `chmod 600 .env`
   - Never commit `.env` to version control
   - Use separate keys for testing and production

2. **Network Security**
   - Run on localhost for development
   - Use HTTPS in production
   - Consider firewall rules for production deployment

3. **Account Security**
   - Use dedicated trading accounts
   - Start with small amounts for testing
   - Monitor account activity regularly

## 🚀 Production Deployment

### Using PM2 (Recommended)
```bash
npm install -g pm2
pm2 start dist/rest/server.js --name bitshares-bridge
pm2 startup
pm2 save
```

### Using systemd
```bash
# Create service file
sudo nano /etc/systemd/system/bitshares-bridge.service

# Add service configuration
[Unit]
Description=BitShares CCXT Bridge
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/bitshares-ccxt-bridge
ExecStart=/usr/bin/node dist/rest/server.js
Restart=always
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable bitshares-bridge
sudo systemctl start bitshares-bridge
```

## 📈 Performance Considerations

- **Rate Limits**: XBTS API has rate limits, implement caching for high-frequency requests
- **WebSocket**: Consider WebSocket connections for real-time data
- **Memory**: Monitor memory usage for long-running processes
- **Logging**: Configure appropriate log levels for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with detailed description

## 📝 Changelog

### Version 0.2.0
- ✅ Added automated installation wizard
- ✅ Added management scripts (start.sh, stop.sh, etc.)
- ✅ Added comprehensive testing tools
- ✅ Added CORS support
- ✅ Improved error handling and validation
- ✅ Added Docker support
- ✅ Enhanced documentation

### Version 0.1.0
- ✅ Initial CCXT adapter implementation
- ✅ Basic REST API server
- ✅ Market data and trading support

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check this README and `QUICK_START.md`
- **Testing**: Use `./test-api.sh` and `./test-pairs.sh`
- **Logs**: Check `./logs.sh` for error messages
- **Issues**: Report bugs and feature requests on GitHub

---

**Ready to start trading on BitShares DEX? Run `./install.sh` and you'll be up and running in minutes!** 🚀
