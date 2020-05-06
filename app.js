require('dotenv').config();

const express = require('express');
const apiRouter = require('./routes/api');
const apiResponse = require('./helpers/apiResponse');
const cors = require('cors');

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// app.use(express.static(path.join(__dirname, 'public')));

//To allow cross-origin requests
app.use(cors());

//Route Prefixes
app.use('/api/', apiRouter);

// throw 404 if URL not found
app.all('*', function (req, res) {
  return apiResponse.notFoundResponse(res, 'Page not found');
});

app.use((err, req, res) => {
  if (err.name == 'UnauthorizedError') {
    return apiResponse.unauthorizedResponse(res, err.message);
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Example app listening on port ${PORT}!`));
