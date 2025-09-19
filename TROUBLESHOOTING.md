# BitShares CCXT Bridge - Troubleshooting Guide

## Quick Diagnostics

Run these commands to quickly diagnose issues:

```bash
./test-api.sh       # Test all API endpoints
./test-pairs.sh     # Test your specific pairs
./logs.sh           # View server logs
cat .env            # Check configuration
```

## Common Issues

### 1. Server Won't Start

#### Error: `EADDRINUSE: address already in use`

**Cause**: Port 8787 is already being used by another process.

**Solutions**:
```bash
# Stop existing server
./stop.sh

# Or kill all processes on port 8787
lsof -ti:8787 | xargs kill -9

# Then restart
./start.sh
```

#### Error: `Node.js not found`

**Cause**: Node.js is not installed or wrong version.

**Solutions**:
```bash
# Check Node.js version (needs 20+)
node --version

# Install via installer
./install.sh

# Or install manually
# Ubuntu/Debian:
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# macOS:
brew install node@20
```

#### Error: `Cannot find module`

**Cause**: Dependencies not installed or project not built.

**Solutions**:
```bash
# Install dependencies
npm install

# Build project
npm run build

# Start server
./start.sh
```

### 2. API Returns Errors

#### Error: `symbol required`

**Cause**: Missing symbol parameter in API request.

**Solution**:
```bash
# Wrong:
curl "http://localhost:8787/ticker"

# Correct:
curl "http://localhost:8787/ticker?symbol=BTS/USDT"
```

#### Error: `500 Internal Server Error`

**Cause**: Server-side error, often configuration related.

**Diagnostics**:
```bash
# Check server logs
./logs.sh

# Check configuration
cat .env

# Test with known working pair
curl "http://localhost:8787/ticker?symbol=BTS/USDT"
```

#### Error: Connection refused / No response

**Cause**: Server is not running or wrong port.

**Solutions**:
```bash
# Check if server is running
./test-api.sh

# Start server if not running
./start.sh

# Check correct port in .env
grep PORT .env
```

### 3. Trading Issues

#### Error: `Authentication required`

**Cause**: Not logged in for trading endpoints.

**Solutions**:
```bash
# Login via API
curl -X POST "http://localhost:8787/login" \
  -H "Content-Type: application/json" \
  -d '{
    "account": "your-account",
    "keyOrPassword": "5YourPrivateKey...",
    "isPassword": false
  }'

# Or ensure .env has correct credentials
cat .env | grep BTS_
```

#### Error: `Invalid private key`

**Cause**: Wrong private key format or invalid key.

**Solutions**:
```bash
# Check key format (should start with '5' and be ~51 characters)
echo $BTS_WIF | wc -c

# Verify key in BitShares wallet
# Re-run installer to update key
./install.sh
```

#### Error: `Insufficient balance`

**Cause**: Not enough funds in account.

**Solutions**:
```bash
# Check balance
curl "http://localhost:8787/balance"

# Check public balance
curl "http://localhost:8787/balancePublic?account=your-account"

# Fund your account via BitShares DEX
```

### 4. Installation Issues

#### Error: `Permission denied`

**Cause**: Scripts don't have execute permissions.

**Solution**:
```bash
chmod +x *.sh
./install.sh
```

#### Error: `Package manager not found`

**Cause**: Unsupported Linux distribution.

**Solutions**:
```bash
# Install Node.js manually
wget https://nodejs.org/dist/v20.x.x/node-v20.x.x-linux-x64.tar.xz
tar -xf node-v20.x.x-linux-x64.tar.xz
sudo mv node-v20.x.x-linux-x64 /opt/nodejs
echo 'export PATH=/opt/nodejs/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Then continue with installation
npm install
npm run build
```

#### Error: `Network timeout during installation`

**Cause**: Slow or unreliable internet connection.

**Solutions**:
```bash
# Increase npm timeout
npm config set timeout 60000

# Use different registry
npm config set registry https://registry.npmjs.org/

# Retry installation
npm install
```

### 5. Configuration Issues

#### Error: `Invalid account name format`

**Cause**: BitShares account name doesn't meet requirements.

**Requirements**:
- 3-63 characters long
- Lowercase letters, numbers, dots, hyphens only
- Must start and end with letter or number

**Examples**:
```bash
# Valid:
myaccount123
test-account
user.name

# Invalid:
ab                    # too short
MyAccount            # uppercase
-invalid             # starts with hyphen
account_name         # underscore not allowed
```

#### Error: `Connection to BitShares node failed`

**Cause**: BitShares node is unreachable or wrong URL.

**Solutions**:
```bash
# Test node connectivity
curl -s "wss://node.xbts.io/ws" || echo "Node unreachable"

# Try alternative nodes in .env:
BTS_NODE=wss://api.bts.mobi/ws
# or
BTS_NODE=wss://btsws.roelandp.nl/ws

# Restart server
./stop.sh && ./start.sh
```

### 6. Performance Issues

#### Issue: Slow API responses

**Causes**: Network latency, rate limiting, server overload.

**Solutions**:
```bash
# Test response times
time curl "http://localhost:8787/ticker?symbol=BTS/USDT"

# Check server resources
top | grep node

# Restart server
./stop.sh && ./start.sh

# Consider caching for high-frequency requests
```

#### Issue: High memory usage

**Cause**: Memory leaks or large market data cache.

**Solutions**:
```bash
# Monitor memory usage
ps aux | grep node

# Restart server periodically
./stop.sh && ./start.sh

# Consider using PM2 for automatic restarts
npm install -g pm2
pm2 start dist/rest/server.js --name bitshares-bridge --max-memory-restart 500M
```

## Platform-Specific Issues

### Windows (Git Bash/WSL)

#### Issue: Scripts don't run

**Solutions**:
```bash
# Ensure using Git Bash or WSL
# Convert line endings if needed
dos2unix *.sh

# Make executable
chmod +x *.sh
```

#### Issue: `lsof` command not found

**Solution**:
```bash
# Use netstat instead (modify stop.sh if needed)
netstat -ano | findstr :8787
```

### macOS

#### Issue: `brew` command not found

**Solution**:
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Then install Node.js
brew install node@20
```

### Linux

#### Issue: `curl` not installed

**Solution**:
```bash
# Ubuntu/Debian:
sudo apt-get install curl

# CentOS/RHEL:
sudo yum install curl
```

## Advanced Troubleshooting

### Debug Mode

Enable detailed logging:

```bash
# Set debug environment
export DEBUG=*
./start.sh

# Or modify .env
echo "DEBUG=*" >> .env
```

### Network Diagnostics

```bash
# Test BitShares node connectivity
curl -v "https://api.bitshares.ws/"

# Test XBTS API
curl -v "https://cmc.xbts.io/v2/summary"

# Check DNS resolution
nslookup node.xbts.io
```

### Database Issues

If using persistent storage:

```bash
# Clear cache/database
rm -rf data/ cache/

# Restart with fresh state
./stop.sh && ./start.sh
```

### Log Analysis

```bash
# View detailed logs
./logs.sh

# Search for specific errors
./logs.sh | grep -i error

# Monitor real-time logs
tail -f logs/server.log  # if logging to file
```

## Getting Help

### Before Asking for Help

1. **Run diagnostics**:
   ```bash
   ./test-api.sh
   ./test-pairs.sh
   ./logs.sh
   ```

2. **Check configuration**:
   ```bash
   cat .env
   node --version
   npm --version
   ```

3. **Try basic fixes**:
   ```bash
   ./stop.sh && ./start.sh
   npm run build
   ```

### Information to Include

When reporting issues, include:

- Operating system and version
- Node.js version (`node --version`)
- Output from `./test-api.sh`
- Relevant log entries from `./logs.sh`
- Your `.env` configuration (remove private key)
- Exact error messages
- Steps to reproduce the issue

### Support Channels

1. **Documentation**: README.md, API.md, SCRIPTS.md
2. **Self-diagnosis**: `./test-api.sh`, `./logs.sh`
3. **GitHub Issues**: Report bugs and feature requests
4. **Community**: BitShares community forums

## Prevention

### Regular Maintenance

```bash
# Weekly health check
./test-pairs.sh

# Monthly updates
git pull
npm update
npm run build
./stop.sh && ./start.sh
```

### Monitoring

```bash
# Set up monitoring script
cat > monitor.sh << 'EOF'
#!/bin/bash
if ! curl -s http://localhost:8787/markets > /dev/null; then
    echo "$(date): Server down, restarting..." >> monitor.log
    ./stop.sh && ./start.sh
fi
EOF

chmod +x monitor.sh

# Run every 5 minutes via cron
echo "*/5 * * * * /path/to/bitshares-ccxt-bridge/monitor.sh" | crontab -
```

### Backup

```bash
# Backup configuration
cp .env .env.backup

# Backup custom modifications
git stash  # if using git
```

---

**Still having issues? Run `./test-api.sh` and `./logs.sh` to gather diagnostic information, then check the main README.md or report the issue with the collected information.**
