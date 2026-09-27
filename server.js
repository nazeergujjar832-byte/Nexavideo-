const express = require('express');
const cors = require('cors');
const app = express();
app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
  res.send('NexaVideo API READY - Made by Nazeer Gujjar');
});

function getVideoId(url) {
  try {
    const u = new URL(url);
    if (u.hostname.includes('youtu.be')) return u.pathname.slice(1);
    if (u.searchParams.get('v')) return u.searchParams.get('v');
    const parts = u.pathname.split('/');
    return parts.pop();
  } catch { return null; }
}

const PIPED_INSTANCES = [
  'https://pipedapi.kavin.rocks',
  'https://api.piped.privacy.com.de',
  'https://pipedapi.adminforge.de'
];

app.get('/info', async (req, res) => {
  const url = req.query.url;
  if (!url) return res.json({ error: 'url missing?url=' });

  const videoId = getVideoId(url);
  if (!videoId) return res.json({ error: 'Invalid YouTube URL' });

  for (const instance of PIPED_INSTANCES) {
    try {
      const r = await fetch(`${instance}/streams/${videoId}`);
      const data = await r.json();
      if (data.title) {
        return res.json({
          title: data.title,
          thumbnail: data.thumbnailUrl,
          duration: data.duration,
          uploader: data.uploader,
          videoStreams: data.videoStreams?.slice(0,5),
          audioStreams: data.audioStreams?.slice(0,3),
          // direct download links
          bestUrl: data.videoStreams?.[0]?.url,
          downloadLinks: data.videoStreams
        });
      }
    } catch (e) {}
  }
  res.json({ error: 'All Piped instances failed, try again' });
});

app.get('/download', async (req, res) => {
  const url = req.query.url;
  const videoId = getVideoId(url);
  if (!videoId) return res.status(400).send('Invalid URL');

  try {
    const r = await fetch(`https://pipedapi.kavin.rocks/streams/${videoId}`);
    const data = await r.json();
    if(data.videoStreams && data.videoStreams[0]) {
      return res.redirect(data.videoStreams[0].url);
    }
    res.json(data);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

module.exports = app;
