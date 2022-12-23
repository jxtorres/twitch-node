const express = require('express');
const app = express();

app.get('/', (req, res) => {
  console.log("hello my world");
  res.send('Hello World!');
});

exports.handler = (event, context, callback) => {
  // Create an HTTP request and response object from the event and context
  const req = event.httpMethod ? event : {
    httpMethod: event.method,
    headers: event.headers,
    queryStringParameters: event.queryStringParameters,
    path: event.path,
    body: event.body
  };
  const res = {
    setHeader: (name, value) => {
      context.headers[name] = value;
    },
    send: (body) => {
      context.body = body;
    }
  };

  // Invoke the express app with the request and response objects
  app(req, res, (err) => {
    if (err) {
      return callback(err);
    }
    callback(null, {
      statusCode: context.statusCode,
      headers: context.headers,
      body: context.body
    });
  });
};
