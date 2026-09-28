const express = require('express');
const cors = require('cors');
const app = express();
app.use(cors()); app.use(express.json());
let videos=[];

app.post('/api/auth/login', (req,res)=> res.json({token:'demo-token', user:{id:1, username:req.body.username}}));
app.post('/api/auth/register', (req,res)=> res.json({token:'demo-token'}));
app.post('/api/auth/refresh', (req,res)=> res.json({token:'demo-token-refreshed'}));
app.get('/api/feed', (req,res)=> res.json(videos));
app.get('/api/shorts', (req,res)=> res.json(videos));
app.post('/api/videos/upload', (req,res)=>{ const v={id:Date.now(),...req.body, likes:0}; videos.push(v); res.json(v); });
app.post('/api/social/like', (req,res)=> res.json({ok:true}));
app.post('/api/social/follow', (req,res)=> res.json({ok:true}));
app.post('/api/comments', (req,res)=> res.json({id:Date.now(), text:req.body.text}));
app.get('/api/inbox', (req,res)=> res.json([]));
app.get('/api/notifications', (req,res)=> res.json([]));
app.get('/api/profile/:id', (req,res)=> res.json({id:req.params.id, earnings:0}));
app.get('/api/creator/ledger', (req,res)=> res.json({balance:1200, history:[]}));
app.get('/api/search', (req,res)=> res.json(videos));
app.post('/api/reports', (req,res)=> res.json({ok:true}));
app.get('/health', (req,res)=> res.json({status:'ok', features:14}));

app.listen(3000, ()=>console.log('NexaVideo API running on 3000'));
