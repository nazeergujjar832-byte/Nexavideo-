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
    if (!url) return res.json({ error: 'url parameter missing' });

    // ANDROID client se YouTube block bypass hota hai
    const info = await ytdl.getInfo(url, {
      playerClients: ['ANDROID', 'IOS', 'WEB']
    });

    const formats = info.formats
      .filter(f => f.hasVideo && f.hasAudio)
      .map(f => ({
        quality: f.qualityLabel,
        itag: f.itag,
        url: f.url
      }));

    res.json({
      title: info.videoDetails.title,
      thumbnail: info.videoDetails.thumbnails.pop().url,
      duration: info.videoDetails.lengthSeconds,
      formats: formats
    });

  } catch (e) {
    console.log(e);
    res.json({ error: e.message + " | Try another video" });
  }
});

app.get('/download', async (req, res) => {
  try {
    const url = req.query.url;
    if (!url) return res.status(400).send('URL missing');

    const info = await ytdl.getInfo(url, { playerClients: ['ANDROID'] });
    const title = info.videoDetails.title.replace(/[^\w\s]/gi, '');

    res.header('Content-Disposition', `attachment; filename="${title}.mp4"`);
    ytdl(url, { 
      quality: 'highest',
      playerClients: ['ANDROID']
    }).pipe(res);

  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

module.exports = app;
