const express = require('express');
const cors = require('cors');
const app = express();
app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
  res.send('NexaVideo API READY - Made by Nazeer Gujjar');
});

// Naye working cobalt instances
const INSTANCES = [
  'https://co.wuk.sh/api/json',
  'https://api.co.eepy.rip/api/json',
  'https://cobalt.api.timelessnesses.me/api/json'
];

async function getCobaltData(url) {
  for (const instance of INSTANCES) {
    try {
      const r = await fetch(instance, {
        method: 'POST',
        headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url, vQuality: '720' })
      });
      const data = await r.json();
      if (data.url || data.status === 'stream' || data.status === 'redirect') return data;
    } catch (e) {}
  }
  throw new Error('All instances failed');
}

app.get('/info', async (req, res) => {
  const url = req.query.url;
  if (!url) return res.json({ error: 'url missing ?url=...' });
  try {
    const data = await getCobaltData(url);
    res.json(data);
  } catch (e) {
    res.json({ error: e.message });
  }
});

app.get('/download', async (req, res) => {
  const url = req.query.url;
  if (!url) return res.status(400).send('url missing');
  try {
    const data = await getCobaltData(url);
    if (data.url) return res.redirect(data.url);
    res.json(data);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

module.exports = app;
