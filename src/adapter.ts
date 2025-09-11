import { getSummary, getTicker, getOrderBook, getTrades, getMarketHistory } from './marketdata-xbts.js';
import { xbtsTickerFromSymbol, symbolFromXbtsTicker } from './symbols.js';
import { Signer } from './signer-btsdex.js';

export class BitSharesCCXT {
  id = 'bitshares-dex';
  name = 'BitShares DEX (CCXT bridge)';
  signer = new Signer();
  marketsCache: any[] = [];

  async describe() {
    const summary = await getSummary();
    this.marketsCache = Object.entries(summary.tickers).map(([k, v]: any) => ({
      id: k,
      symbol: symbolFromXbtsTicker(k),
      base: v.base_symbol,
      quote: v.quote_symbol,
      active: v.isFrozen === 0,
      type: 'spot',
      spot: true
    }));
    return { id: this.id, name: this.name };
  }

  async fetchMarkets() {
    if (!this.marketsCache.length) await this.describe();
    return this.marketsCache;
  }

  async fetchTicker(symbol: string) {
    const t = await getTicker(xbtsTickerFromSymbol(symbol));
    const k = Object.keys(t)[0];
    const v = t[k];
    return {
      symbol,
      last: parseFloat(v.last),
      bid: parseFloat(v.buy),
      ask: parseFloat(v.sell),
      baseVolume: parseFloat(v.base_volume),
      quoteVolume: parseFloat(v.quote_volume),
      percentage: parseFloat(v.change),
      timestamp: v.timestamp ? v.timestamp * 1000 : Date.now(),
      info: v
    };
  }

  async fetchOrderBook(symbol: string, limit = 50) {
    const ob = await getOrderBook(xbtsTickerFromSymbol(symbol), limit);
    return {
      symbol,
      timestamp: ob.timestamp * 1000,
      bids: ob.bids.map((b: any) => [parseFloat(b.price), parseFloat(b.quote)]),
      asks: ob.asks.map((a: any) => [parseFloat(a.price), parseFloat(a.quote)]),
      info: ob
    };
  }

  async fetchTrades(symbol: string, since?: number, limit = 100) {
    const raw = await getTrades(xbtsTickerFromSymbol(symbol), limit);
    return raw
      .map((t: any) => ({
        id: String(t.trade_id),
        symbol,
        timestamp: t.timestamp * 1000,
        datetime: new Date(t.timestamp * 1000).toISOString(),
        price: parseFloat(t.price),
        amount: parseFloat(t.quote_volume),
        side: t.type === 'sell' ? 'sell' : 'buy',
        info: t
      }))
      .filter(x => !since || x.timestamp >= since);
  }

  async fetchOHLCV(symbol: string) {
    const raw = await getMarketHistory(xbtsTickerFromSymbol(symbol));
    return raw.map((c: any) => [
      Date.parse(c.date),
      parseFloat(c.open_price),
      parseFloat(c.high_price),
      parseFloat(c.low_price),
      parseFloat(c.close_price),
      parseFloat(c.base_volume)
    ]);
  }

  async login(account: string, keyOrPassword: string, isPassword = false, node?: string) {
    await this.signer.connect(node);
    await this.signer.login(account, keyOrPassword, isPassword);
  }

  async fetchBalance() {
    return this.signer.balances();
  }

  async createOrder(symbol: string, type: 'limit', side: 'buy'|'sell', amount: number, price: number, params?: any) {
    if (type !== 'limit') throw new Error('Only limit orders supported');
    return this.signer.createLimitOrder(symbol, side, amount, price, params);
  }

  async cancelOrder(id: string) {
    return this.signer.cancelOrder(id);
  }

  async fetchOpenOrders() {
    return this.signer.openOrders();
  }
}
