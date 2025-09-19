import axios from 'axios';
const BASE = process.env.XBTS_API || 'https://cmc.xbts.io/v2';
export async function getSummary() {
    return (await axios.get(`${BASE}/summary`)).data;
}
export async function getTicker(pair) {
    return (await axios.get(`${BASE}/tickers/${pair}`)).data;
}
export async function getOrderBook(pair, depth = 50) {
    return (await axios.get(`${BASE}/orderbook/${pair}`, { params: { depth } })).data;
}
export async function getTrades(pair, limit = 100) {
    return (await axios.get(`${BASE}/trades/${pair}`, { params: { limit } })).data;
}
// Accept optional timeframe parameter; currently ignored by backend but forwarded for future support
export async function getMarketHistory(pair, timeframe) {
    return (await axios.get(`${BASE}/history/market/${pair}`, { params: timeframe ? { timeframe } : undefined })).data;
}
