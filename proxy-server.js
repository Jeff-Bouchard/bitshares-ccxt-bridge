import express from 'express';
import cors from 'cors';
import fetch from 'node-fetch';

const app = express();
const PORT = 3001;
const XBTS_API = 'https://cmc.xbts.io/v2';

// Enable CORS for all routes
app.use(cors());

// Proxy endpoint
app.get('/api/tickers/:pair', async (req, res) => {
    try {
        const response = await fetch(`${XBTS_API}/tickers/${req.params.pair}`, {
            headers: {
                'Accept': 'application/json'
            }
        });
        const data = await response.json();
        res.json(data);
    } catch (error) {
        console.error('Proxy error:', error);
        res.status(500).json({ error: 'Failed to fetch data from XBTS API' });
    }
});

app.listen(PORT, () => {
    console.log(`Proxy server running on http://localhost:${PORT}`);
});
