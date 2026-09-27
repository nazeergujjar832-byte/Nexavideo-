const express = require('express');
const cors = require('cors');
const ytdl = require('@distube/ytdl-core');

const app = express();
app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
  res.send('NexaVideo API Chal Rahi Hai - Made by Nazeer Gujjar - READY!');
});

app.get('/info', async (req, res) => {
  try {
    const url = req.query.url;
    if (!url) return res.json({ error: 'URL do?url=...' });

    const info = await ytdl.getInfo(url);
    res.json({
      title: info.videoDetails.title,
      thumbnail: info.videoDetails.thumbnails[0].url,
      formats: info.formats.map(f => ({
        quality: f.qualityLabel,
        url: f.url
      })).slice(0,5)
    });
  } catch (e) {
    res.json({ error: e.message });
  }
});

app.get('/download', async (req, res) => {
  try {
    const url = req.query.url;
    if (!ytdl.validateURL(url)) return res.status(400).send('Invalid URL');

    const info = await ytdl.getInfo(url);
    const title = info.videoDetails.title.replace(/[^a-zA-Z0-9]/g, '_');

    res.header('Content-Disposition', `attachment; filename="${title}.mp4"`);
    ytdl(url, { quality: 'highest' }).pipe(res);
  } catch (e) {
    res.status(500).send(e.message);
  }
});

module.exports = app;
