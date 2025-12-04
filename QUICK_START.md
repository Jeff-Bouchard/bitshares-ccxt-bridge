## 🚀 BitShares CCXT Bridge - Quick Start Guide

**For Non-Technical Users**

This guide will help you set up and use the BitShares CCXT Bridge in just a few simple steps!

## What You Need

1.  **BitShares Account**: You need a BitShares account with some funds
2.  **Private Key**: Your BitShares ACTIVE private key (starts with "5")
3.  **Computer**: Windows, Mac, or Linux computer

## 📦 One-Click Installation

### Step 1: Run the Installer

```plaintext
chmod +x install.sh
./install.sh
```

The installer will:

*   ✅ Check and install Node.js 20+ if needed
*   ✅ Install all dependencies automatically
*   ✅ Guide you through configuration with validation
*   ✅ Test your setup to ensure everything works

### Step 2: Follow the Setup Wizard

The installer will ask you for:

1.  **BitShares Node** (default `wss://node.xbts.io/ws` is fine for most users)
2.  **Your Account Name** (e.g., "palmpay6669")
3.  **Your Private Key** (your ACTIVE key starting with "5")
4.  **Server Port** (default 8787 is fine)
5.  **Market Data API** (default `https://cmc.xbts.io/v2` is fine)

⚠️ **IMPORTANT**: Your private key will be stored securely in a `.env` file with restricted permissions. Keep this file safe!

## 🎮 Using the Bridge

### Start the Server

```plaintext
./start.sh
```

### Stop the Server

```plaintext
./stop.sh
```

### Test All API Endpoints

```plaintext
./test-api.sh
```

### Test Your Specific Pairs

```plaintext
./test-pairs.sh
```

This tests your BitShares tokens:

*   BTS/NESS, BTS/SCH, BTS/NCH
*   BTC/NESS, BTC/SCH, BTC/NCH
*   ETH/NESS, ETH/SCH
*   STH/NESS, STH/SCH

### View Server Logs

```plaintext
./logs.sh
```

## 🌐 API Endpoints

Once running, you can access:

### Market Data (Public)

*   **All Markets**: `http://localhost:8787/markets`
*   **Price Ticker**: `http://localhost:8787/ticker?symbol=BTS/USDT`
*   **Order Book**: `http://localhost:8787/orderbook?symbol=BTS/USDT`
*   **Recent Trades**: `http://localhost:8787/trades?symbol=BTS/USDT`
*   **OHLCV Data**: `http://localhost:8787/ohlcv?symbol=BTS/USDT`

### Your Custom Coins or Tokens

*   **NESS Price**: `http://localhost:8787/ticker?symbol=BTS/NESS`
*   **SCH Price**: `http://localhost:8787/ticker?symbol=BTS/SCH`
*   **NCH Price**: `http://localhost:8787/ticker?symbol=BTS/NCH`

### Trading (Requires Login)

*   **Account Balance**: `http://localhost:8787/balance`
*   **Public Balance**: `http://localhost:8787/balancePublic?account=some-account`
*   **Open Orders**: `http://localhost:8787/openOrders`

## 🔧 Troubleshooting

### Server Won't Start?

1.  Check if port is busy: `./stop.sh`
2.  Verify Node.js version: `node --version` (needs 20+)
3.  Rebuild project: `npm run build`
4.  Try starting again: `./start.sh`

### API Not Working?

1.  Test server status: `./test-api.sh`
2.  Check server logs: `./logs.sh`
3.  Verify configuration: `cat .env`
4.  Restart server: `./stop.sh &amp;&amp; ./start.sh`

### Configuration Issues?

1.  Re-run installer: `./install.sh`
2.  Choose "yes" when asked to reconfigure
3.  Verify your BitShares account name and private key

### Common Errors

| Error | Solution |
| --- | --- |
| `EADDRINUSE` | Port 8787 is busy, run `./stop.sh` |
| `symbol required` | Add `?symbol=BTS/USDT` to your URL |
| `Invalid private key` | Check your key starts with "5" and is 51 characters |
| `Connection failed` | Check BitShares node URL in `.env` |

## 📊 Testing Your Setup

### Quick Test

```plaintext
# Test if server is running
curl "http://localhost:8787/markets"

# Test your tokens
curl "http://localhost:8787/ticker?symbol=BTS/NESS"
curl "http://localhost:8787/ticker?symbol=BTS/SCH"
```

### Comprehensive Test

```plaintext
./test-pairs.sh
```

Expected output for working pairs:

```plaintext
Testing: BTS/NESS
[INFO] ✓ Last: 0.06666667 | Bid: 0.06666667 | Ask: 0.07999

Testing: BTS/SCH  
[INFO] ✓ Last: 0.00008 | Bid: 0.00006897 | Ask: 0.00008
```

## 📚 What's Next?

### For Traders

*   **Manual Trading**: Use the REST API endpoints
*   **Automated Trading**: Integrate with trading bots
*   **Monitoring**: Set up price alerts using the ticker endpoints

### For Developers

*   **Programmatic Usage**: See `README.md` for code examples
*   **CCXT Integration**: Use as a drop-in CCXT exchange
*   **Custom Applications**: Build on top of the REST API

### Advanced Features

*   **Docker Deployment**: Use `docker-compose up -d`
*   **Production Setup**: See README.md for PM2/systemd configuration
*   **API Documentation**: Check `API.md` for complete endpoint reference

## 🔒 Security Best Practices

1.  **Keep** `**.env**` **file secure** - Never share or commit to version control
2.  **Use dedicated trading accounts** - Don't use your main BitShares account
3.  **Start with small amounts** - Test thoroughly before large trades
4.  **Monitor regularly** - Check your account activity frequently
5.  **Backup your keys** - Store private keys securely offline

## 🆘 Need Help?

### Documentation

1.  **README.md** - Complete technical documentation
2.  **API.md** - Detailed API reference
3.  **This guide** - Quick start instructions

### Diagnostics

1.  **Test scripts**: `./test-api.sh` and `./test-pairs.sh`
2.  **Server logs**: `./logs.sh`
3.  **Configuration**: `cat .env`

### Common Solutions

1.  **Restart everything**: `./stop.sh &amp;&amp; ./start.sh`
2.  **Rebuild project**: `npm run build`
3.  **Reconfigure**: `./install.sh` (choose yes to reconfigure)

## 🎉 Success!

If you see this output from `./test-pairs.sh`, you're ready to go:

```plaintext
================================
  Testing Your BitShares Pairs
================================

[INFO] Server is running on http://localhost:8787

Testing your BitShares pairs:

Testing: BTS/NESS
[INFO] ✓ Last: 0.06666667 | Bid: 0.06666667 | Ask: 0.07999

Testing: BTS/SCH
[INFO] ✓ Last: 0.00008 | Bid: 0.00006897 | Ask: 0.00008

[INFO] Pair testing complete!
```

**You now have a fully functional BitShares CCXT bridge! 🚀**

Start building your trading applications or integrate with existing tools using the REST API endpoints.