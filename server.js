const express = require('express');
const cors = require('cors');
const app = express();
app.use(cors());

app.get('/', (req,res) => res.send('NexaVideo API LIVE - Nazeer Gujjar'));

// Invidious API - Ye Vercel pe block hai, Render pe 100% chalta hai
app.get('/info', async (req,res) => {
  const url = req.query.url;
  if(!url) return res.json({error:'url missing'});

  const id = url.match(/(?:v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/)?.[1];
  if(!id) return res.json({error:'Invalid URL'});

  try {
    // Invidious instance
    const r = await fetch(`https://inv.nadeko.net/api/v1/videos/${id}`);
    const data = await r.json();

    res.json({
      title: data.title,
      thumbnail: data.videoThumbnails?.[0]?.url,
      duration: data.lengthSeconds,
      formats: data.formatStreams, // direct download links!
      best: data.formatStreams?.[0]?.url
    });
  } catch(e) {
    res.json({error: e.message});
  }
});

app.get('/download', async (req,res) => {
  const url = req.query.url;
  const id = url.match(/(?:v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/)?.[1];
  try {
    const r = await fetch(`https://inv.nadeko.net/api/v1/videos/${id}`);
    const data = await r.json();
    if(data.formatStreams?.[0]?.url) return res.redirect(data.formatStreams[0].url);
    res.json(data);
  } catch(e) { res.json({error:e.message}); }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log('Running on', PORT));
