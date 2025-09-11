import express from 'express';
import dotenv from 'dotenv';
import { BitSharesCCXT } from '../adapter.js';

dotenv.config();
const app = express();
app.use(express.json());

const ex = new BitSharesCCXT();

app.get('/markets', async (_req, res) => {
  res.json(await ex.fetchMarkets());
});

app.get('/ticker', async (req, res) => {
  const { symbol } = req.query;
  if (!symbol) return res.status(400).json({ error: 'symbol required' });
  res.json(await ex.fetchTicker(String(symbol)));
});

const port = process.env.PORT || 8787;
app.listen(port, () => {
  console.log(`BitShares CCXT REST API running on port ${port}`);
});
