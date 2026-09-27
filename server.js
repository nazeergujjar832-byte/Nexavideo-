const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
  res.send('NexaVideo API Chal Rahi Hai - Made by Nazeer Gujjar - READY!');
});

app.get('/download', async (req, res) => {
  res.json({ status: 'API Ready', message: 'Use ?url=YoutubeLink' });
});

module.exports = app;
