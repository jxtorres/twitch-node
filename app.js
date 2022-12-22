const express = require('express');
const app = express();

app.get('/', (req, res) => {
  console.log("hello my world");
  res.send('Hello World!');
});

module.exports.handler = app;
