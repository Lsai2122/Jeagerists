const express = require('express');
const translatte = require('translatte');
const app = express();
const port = 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.send('Hello from KrishiKavach!');
});

app.post('/chat', async (req, res) => {
  const { message, lang } = req.body;

  if (!message || !lang) {
    return res.status(400).json({ error: 'Both message and lang are required.' });
  }

  try {
    const translated = await translatte(message, { 
      to: lang,
      agents: [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
      ]
    });
    res.json({ reply: translated.text });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Translation failed.' });
  }
});

app.listen(port, () => {
  console.log(`KrishiKavach backend listening at http://localhost:${port}`);
});