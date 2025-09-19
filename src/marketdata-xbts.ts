import axios from 'axios';

const BASE = process.env.XBTS_API || 'https://cmc.xbts.io/v2';

export async function getSummary() {
  return (await axios.get(`${BASE}/summary`)).data;
}

export async function getTicker(pair: string) {
  return (await axios.get(`${BASE}/tickers/${pair}`)).data;
}

export async function getOrderBook(pair: string, depth = 50) {
  return (await axios.get(`${BASE}/orderbook/${pair}`, { params: { depth } })).data;
}

export async function getTrades(pair: string, limit = 100) {
  return (await axios.get(`${BASE}/trades/${pair}`, { params: { limit } })).data;
}

// Accept optional timeframe parameter; currently ignored by backend but forwarded for future support
export async function getMarketHistory(pair: string, timeframe?: string) {
  return (await axios.get(`${BASE}/history/market/${pair}`, { params: timeframe ? { timeframe } : undefined })).data;
}
