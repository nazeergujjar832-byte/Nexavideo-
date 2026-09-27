const express = require('express');
const cors = require('cors');
const app = express();
app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
  res.send('NexaVideo API READY - Made by Nazeer Gujjar');
});

app.get('/info', async (req, res) => {
  const url = req.query.url;
  if (!url) return res.json({ error: 'url missing ?url=link' });
  
  try {
    const response = await fetch('https://api.cobalt.tools/api/json', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        url: url,
        vQuality: '720',
        filenamePattern: 'basic'
      })
    });
    const data = await response.json();
    res.json(data);
  } catch (e) {
    res.json({ error: e.message });
  }
});

app.get('/download', async (req, res) => {
  const url = req.query.url;
  if (!url) return res.status(400).send('url missing');
  
  try {
    const response = await fetch('https://api.cobalt.tools/api/json', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url: url, vQuality: '720' })
    });
    const data = await response.json();
    
    if(data.url) {
      // Direct download link mil gaya
      return res.redirect(data.url);
    } else {
      res.json(data);
    }
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

module.exports = app;
