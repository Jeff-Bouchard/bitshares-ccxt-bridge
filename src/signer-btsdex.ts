import BitShares from 'btsdex';
import { parseSymbol } from './symbols.js';

export class Signer {
  private accountName!: string;
  private connected = false;
  private acc: any | null = null;

  async connect(node?: string) {
    if (!this.connected) {
      await (node ? BitShares.connect(node) : BitShares.connect());
      this.connected = true;
    }
  }

  async login(accountName: string, wifOrPassword: string, isPassword = false) {
    await this.connect();
    this.accountName = accountName;
    this.acc = isPassword
      ? await BitShares.login(accountName, wifOrPassword)
      : new (BitShares as any)(accountName, wifOrPassword);
    return this.acc;
  }

  async balances() {
    const iam = await (BitShares as any).accounts[this.accountName];
    return iam.balances;
  }

  async createLimitOrder(
    symbol: string,
    side: 'buy' | 'sell',
    amount: number,
    price: number,
    params?: { fillOrKill?: boolean; expire?: string }
  ) {
    const { base, quote } = parseSymbol(symbol);
    if (side === 'buy') {
      return this.acc.buy(quote, base, amount, price, params?.fillOrKill ?? false, params?.expire);
    }
    return this.acc.sell(base, quote, amount, price, params?.fillOrKill ?? false, params?.expire);
  }

  async cancelOrder(orderId: string) {
    return this.acc.cancelOrder(orderId);
  }

  async openOrders() {
    const iam = await (BitShares as any).accounts[this.accountName];
    const full = await (BitShares as any).db.get_full_accounts([iam.id], false);
    return full[0][1].limit_orders;
  }
}
