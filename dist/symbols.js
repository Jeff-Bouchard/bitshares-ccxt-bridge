export function parseSymbol(symbol) {
    const [base, quote] = symbol.split('/');
    if (!base || !quote)
        throw new Error(`Invalid symbol: ${symbol}`);
    return { base: base.trim(), quote: quote.trim() };
}
export function xbtsTickerFromSymbol(symbol) {
    const { base, quote } = parseSymbol(symbol);
    return `${base}_${quote}`;
}
export function symbolFromXbtsTicker(t) {
    const [base, quote] = t.split('_');
    return `${base}/${quote}`;
}
