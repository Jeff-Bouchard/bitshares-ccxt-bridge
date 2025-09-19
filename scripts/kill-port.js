#!/usr/bin/env node
/*
 Kill any process listening on a given TCP port before starting the server.
 Defaults to process.env.PORT || 8787.
 Works on Windows, macOS, and Linux.
*/
import { execSync } from 'node:child_process';

const PORT = Number(process.env.PORT || 8787);
function log(msg) {
  if (process.env.KILL_PORT_VERBOSE) {
    console.log(`[kill-port] ${msg}`);
  }
}

function killOnWindows(port) {
  try {
    // Prefer PowerShell Stop-Process if available
    const psCmd = `Get-NetTCPConnection -LocalPort ${port} -State Listen -ErrorAction SilentlyContinue | Select-Object -Expand OwningProcess`;
    const cmd = `powershell -NoProfile -Command "${psCmd} | ForEach-Object { Stop-Process -Id $_ -Force }"`;
    execSync(cmd, { stdio: 'ignore' });
    return true;
  } catch (e) {
    // Fallback to netstat + taskkill
    try {
      const out = execSync(`netstat -ano | findstr :${port}` + (process.env.ComSpec ? '' : ' | cat'), { encoding: 'utf8' });
      const lines = out.split(/\r?\n/).filter(Boolean);
      const pids = new Set();
      for (const line of lines) {
        const parts = line.trim().split(/\s+/);
        const pid = parts[parts.length - 1];
        if (pid && /^\d+$/.test(pid)) pids.add(pid);
      }
      for (const pid of pids) {
        try {
          execSync(`taskkill /PID ${pid} /F`, { stdio: 'ignore' });
          log(`Killed PID ${pid} on port ${port}`);
        } catch (_) {}
      }
      return pids.size > 0;
    } catch (_) {
      return false;
    }
  }
}

function killOnUnix(port) {
  try {
    // lsof may not be present on minimal systems; ignore errors
    const out = execSync(`lsof -i :${port} -sTCP:LISTEN -t || true`, { encoding: 'utf8' });
    const pids = out.split(/\s+/).filter(Boolean);
    for (const pid of pids) {
      try {
        execSync(`kill -9 ${pid}`, { stdio: 'ignore' });
        log(`Killed PID ${pid} on port ${port}`);
      } catch (_) {}
    }
    return pids.length > 0;
  } catch (_) {
    // Fallback to fuser if available
    try {
      execSync(`fuser -k ${port}/tcp`, { stdio: 'ignore' });
      return true;
    } catch (_) {
      return false;
    }
  }
}

function main() {
  const platform = process.platform;
  let freed = false;
  if (platform === 'win32') {
    freed = killOnWindows(PORT);
  } else {
    freed = killOnUnix(PORT);
  }
  if (freed) {
    log(`Freed port ${PORT}`);
  } else {
    log(`No listener found on port ${PORT}`);
  }
}

main();
