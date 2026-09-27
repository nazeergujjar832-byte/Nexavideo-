// NEXA VIDEO - ALL FEATURES IN ONE FILE
// Made by Nazeer Gujjar - Ghakhar Mandi
// Ye file aapke server.js me add karni hai

const express = require('express');
const jwt = require('jsonwebtoken');
const app = express();
app.use(express.json());

// ============ DATABASE (Temporary) ============
let users = [];
let follows = [];
let videos = [];
let musics = [
  { id: 1, name: "Punjabi Beat", url: "https://example.com/beat1.mp3" },
  { id: 2, name: "Funny Sound", url: "https://example.com/funny.mp3" },
  { id: 3, name: "Desi Dhol", url: "https://example.com/dhol.mp3" }
];

// ============ 1. LOGIN / SIGNUP SYSTEM ============
app.post('/api/signup', (req, res) => {
  const { username, password, phone } = req.body;
  users.push({ username, password, phone });
  const token = jwt.sign({ username }, 'NEXA_SECRET_123');
  res.json({ success: true, token, message: "Welcome to NexaVideo Nazeer Bhai!" });
});

app.post('/api/login', (req, res) => {
  const { username, password } = req.body;
  const user = users.find(u => u.username == username && u.password == password);
  if (user) {
    const token = jwt.sign({ username }, 'NEXA_SECRET_123');
    res.json({ success: true, token, user });
  } else {
    res.json({ success: false, message: "Username ya Password ghalat hai" });
  }
});

// ============ 2. FOLLOW / FOLLOWING SYSTEM ============
app.post('/api/follow', (req, res) => {
  const { follower, following } = req.body;
  follows.push({ follower, following });
  res.json({ success: true, message: `${follower} ne ${following} ko follow kiya` });
});

app.get('/api/followers/:username', (req, res) => {
  const count = follows.filter(f => f.following === req.params.username).length;
  const followingCount = follows.filter(f => f.follower === req.params.username).length;
  res.json({ followers: count, following: followingCount });
});

// ============ 3. VIDEO UPLOAD WITH HASHTAG ============
app.post('/api/upload', (req, res) => {
  const { title, videoUrl, username, tags } = req.body; // tags = ["#punjabi", "#funny"]
  const newVideo = { 
    id: videos.length + 1, 
    title, 
    videoUrl, 
    username, 
    tags, 
    likes: 0, 
    comments: [] 
  };
  videos.push(newVideo);
  res.json({ success: true, video: newVideo });
});

// ============ 4. HASHTAG SEARCH ============
app.get('/api/search/:tag', (req, res) => {
  const tag = '#' + req.params.tag;
  const result = videos.filter(v => v.tags && v.tags.includes(tag));
  res.json({ tag, count: result.length, videos: result });
});

app.get('/api/feed', (req, res) => {
  res.json(videos.reverse()); // TikTok jaisi feed
});

// ============ 5. LIKE & COMMENT ============
app.post('/api/like/:id', (req, res) => {
  const video = videos.find(v => v.id == req.params.id);
  if (video) video.likes++;
  res.json({ success: true, likes: video.likes });
});

app.post('/api/comment/:id', (req, res) => {
  const video = videos.find(v => v.id == req.params.id);
  if (video) {
    video.comments.push({ user: req.body.user, text: req.body.text });
  }
  res.json({ success: true, comments: video.comments });
});

// ============ 6. MUSIC SYSTEM ============
app.get('/api/all-music', (req, res) => {
  res.json(musics);
});

// ============ 7. USER PROFILE ============
app.get('/api/profile/:username', (req, res) => {
  const userVideos = videos.filter(v => v.username === req.params.username);
  const followers = follows.filter(f => f.following === req.params.username).length;
  res.json({ 
    username: req.params.username, 
    totalVideos: userVideos.length, 
    followers, 
    videos: userVideos 
  });
});

// ============ SERVER START ============
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`NexaVideo Server Chal Raha Hai Port ${PORT} Par!`);
});
