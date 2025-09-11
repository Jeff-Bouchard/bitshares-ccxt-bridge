export type Pair = { base: string; quote: string };

export function parseSymbol(symbol: string): Pair {
  const [base, quote] = symbol.split('/');
  if (!base || !quote) throw new Error(`Invalid symbol: ${symbol}`);
  return { base: base.trim(), quote: quote.trim() };
}

export function xbtsTickerFromSymbol(symbol: string) {
  const { base, quote } = parseSymbol(symbol);
  return `${base}_${quote}`;
}

export function symbolFromXbtsTicker(t: string) {
  const [base, quote] = t.split('_');
  return `${base}/${quote}`;
}
