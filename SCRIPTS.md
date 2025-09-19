# BitShares CCXT Bridge - Scripts Documentation

## Overview

This document describes all available management scripts and their usage. These scripts are designed to make the BitShares CCXT Bridge easy to use for both technical and non-technical users.

## Installation Scripts

### `install.sh`

**Purpose**: Automated installation and configuration wizard

**Usage**:
```bash
./install.sh
```

**What it does**:
- Checks and installs Node.js 20+ if needed (Linux/macOS)
- Installs all project dependencies via `npm install`
- Builds the TypeScript project
- Runs interactive configuration wizard
- Validates user inputs (account names, private keys)
- Creates secure `.env` configuration file
- Tests the setup to ensure everything works

**Supported Platforms**:
- Ubuntu/Debian (apt-get)
- CentOS/RHEL/Fedora (yum/dnf)
- macOS (Homebrew)
- Windows (manual Node.js installation required)

**Configuration Prompts**:
1. BitShares Node URL (default: `wss://node.xbts.io/ws`)
2. BitShares Account Name (validated format)
3. BitShares Private Key (WIF format validation)
4. Server Port (default: 8787)
5. XBTS API URL (default: `https://cmc.xbts.io/v2`)

**Security Features**:
- Private key format validation
- Account name format validation
- Secure file permissions on `.env` (chmod 600)
- Connection testing before completion

## Management Scripts

### `start.sh`

**Purpose**: Start the BitShares CCXT Bridge server

**Usage**:
```bash
./start.sh
```

**What it does**:
- Checks for existing `.env` configuration
- Builds project if `dist/` directory missing
- Detects port conflicts and offers to resolve them
- Starts the server with proper environment
- Displays server information and available endpoints

**Output Example**:
```
[INFO] Starting BitShares CCXT Bridge...
[INFO] Server will run on http://localhost:8787

Available endpoints:
  • GET http://localhost:8787/markets
  • GET http://localhost:8787/ticker?symbol=BTS/USDT

Press Ctrl+C to stop the server
Or run ./stop.sh from another terminal
```

### `stop.sh`

**Purpose**: Stop the BitShares CCXT Bridge server

**Usage**:
```bash
./stop.sh
```

**What it does**:
- Reads port from `.env` file (default: 8787)
- Finds all processes using the port
- Gracefully terminates processes with SIGTERM
- Force kills remaining processes if needed
- Confirms successful shutdown

**Output Example**:
```
[INFO] Stopping BitShares CCXT Bridge on port 8787...
[INFO] Stopped process 12345
[INFO] ✓ Server stopped successfully
```

### `logs.sh`

**Purpose**: View server logs and process information

**Usage**:
```bash
./logs.sh
```

**What it does**:
- Checks if server is running
- Shows process information (PID, status)
- Displays recent log activity using journalctl (if available)
- Falls back to process information if journalctl unavailable

**Output Example**:
```
================================
  BitShares CCXT Bridge Logs
================================

[INFO] Server is running on port 8787 (PID: 12345)

Recent server activity:
Press Ctrl+C to stop viewing logs
```

## Testing Scripts

### `test-api.sh`

**Purpose**: Comprehensive API endpoint testing

**Usage**:
```bash
./test-api.sh
```

**What it does**:
- Verifies server is running
- Tests all major API endpoints
- Displays formatted responses with error handling
- Shows response previews (truncated for readability)
- Provides troubleshooting suggestions

**Endpoints Tested**:
- `/markets` - All available markets
- `/ticker?symbol=BTS/USDT` - BTS/USDT ticker
- `/ticker?symbol=BTS/CNY` - BTS/CNY ticker

**Output Format**:
```
================================
  BitShares CCXT Bridge Test
================================

[INFO] Server is running on http://localhost:8787

Testing: Get all available markets
URL: http://localhost:8787/markets

[INFO] ✓ Success!
Response preview:
[{"id":"BTS_USDT","symbol":"BTS/USDT",...}]
... (response truncated)

----------------------------------------
```

### `test-pairs.sh`

**Purpose**: Test specific BitShares trading pairs

**Usage**:
```bash
./test-pairs.sh
```

**What it does**:
- Tests your specific BitShares tokens
- Shows live price data (last, bid, ask)
- Identifies inactive pairs (no trading activity)
- Provides clean, formatted output

**Pairs Tested**:
- BTS/NESS, BTS/SCH, BTS/NCH
- BTC/NESS, BTC/SCH, BTC/NCH
- ETH/NESS, ETH/SCH
- STH/NESS, STH/SCH
- BTS/USDT (reference)

**Output Example**:
```
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

## Utility Scripts

### `scripts/kill-port.js`

**Purpose**: Kill processes using a specific port (used internally)

**Usage**: Called automatically by `npm start` and management scripts

**What it does**:
- Finds processes using the configured port
- Terminates them to prevent conflicts
- Used as a prestart hook in package.json

## Script Dependencies

### Required Tools

**All Scripts**:
- `bash` shell
- `curl` for API testing
- `lsof` for port checking (Linux/macOS)

**Installation Script**:
- `node` and `npm` (installed automatically if missing)
- Package managers: `apt-get`, `yum`, `dnf`, or `brew`

**Optional Tools**:
- `jq` for JSON formatting (graceful fallback if missing)
- `journalctl` for log viewing (Linux systemd systems)

### Platform Compatibility

| Script | Linux | macOS | Windows (Git Bash) |
|--------|-------|-------|-------------------|
| `install.sh` | ✅ | ✅ | ⚠️ (manual Node.js) |
| `start.sh` | ✅ | ✅ | ✅ |
| `stop.sh` | ✅ | ✅ | ✅ |
| `logs.sh` | ✅ | ✅ | ⚠️ (limited) |
| `test-api.sh` | ✅ | ✅ | ✅ |
| `test-pairs.sh` | ✅ | ✅ | ✅ |

## Error Handling

### Common Issues and Solutions

**Permission Denied**:
```bash
chmod +x *.sh
```

**Port Already in Use**:
```bash
./stop.sh
./start.sh
```

**Node.js Not Found**:
- Run `./install.sh` to install automatically
- Or install manually from nodejs.org

**API Not Responding**:
```bash
./test-api.sh  # Diagnose issues
./logs.sh      # Check for errors
```

### Script Exit Codes

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 1 | General error |
| 127 | Command not found |

## Customization

### Environment Variables

Scripts read configuration from `.env`:
- `PORT` - Server port (default: 8787)
- `BTS_NODE` - BitShares node URL
- `BTS_ACCOUNT` - Account name
- `BTS_WIF` - Private key

### Modifying Scripts

**Adding New Test Pairs**:
Edit `test-pairs.sh` and add:
```bash
test_pair "YOUR_TOKEN/BTS"
```

**Changing Default Port**:
Edit `.env` file:
```
PORT=9999
```

**Custom Node Installation**:
Modify `install.sh` function `install_nodejs()` for your platform.

## Integration with Other Tools

### PM2 Process Manager

```bash
# Start with PM2
pm2 start dist/rest/server.js --name bitshares-bridge

# Use scripts for testing
./test-api.sh
```

### Docker

```bash
# Build and run
docker build -t bitshares-bridge .
docker run -d --env-file .env -p 8787:8787 bitshares-bridge

# Test from host
./test-api.sh
```

### Systemd Service

```bash
# Install as service
sudo systemctl enable bitshares-bridge
sudo systemctl start bitshares-bridge

# Test service
./test-api.sh
```

## Development Workflow

### Typical Development Session

```bash
# Initial setup
./install.sh

# Development cycle
./start.sh          # Start server
./test-pairs.sh     # Test functionality
# Make code changes
npm run build       # Rebuild
./stop.sh           # Stop server
./start.sh          # Restart with changes
```

### Debugging

```bash
# Check server status
./logs.sh

# Test specific endpoints
curl "http://localhost:8787/ticker?symbol=BTS/NESS"

# Full API test
./test-api.sh
```

## Security Considerations

### Script Security

- Scripts validate input parameters
- Private keys are handled securely
- File permissions are set appropriately
- No sensitive data in process arguments

### Best Practices

1. **Keep scripts updated** - Pull latest versions regularly
2. **Review before running** - Understand what each script does
3. **Secure .env file** - Never commit to version control
4. **Use dedicated accounts** - Don't use main BitShares account
5. **Monitor logs** - Check `./logs.sh` regularly

## Contributing

### Adding New Scripts

1. Follow existing naming convention
2. Include proper error handling
3. Add documentation to this file
4. Test on multiple platforms
5. Use consistent output formatting

### Script Standards

- Use `#!/bin/bash` shebang
- Include `set -e` for error handling
- Use colored output functions
- Provide helpful error messages
- Include usage examples

---

**Need help with scripts? Run `./test-api.sh` to diagnose issues or check the main README.md for troubleshooting.**
