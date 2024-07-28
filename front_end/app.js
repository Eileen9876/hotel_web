const express = require('express');
const cookieParser = require("cookie-parser");
const http = require("http");
const bodyParser = require('body-parser');

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.use(cookieParser());

//載入位於 public 目錄中的靜態檔案
app.use(express.static('public'));
app.use(express.static('views'));

app.use(express.static('node_modules'));

//------------------------- 前台API -------------------------//

app.get("/index", (req, res) => {
  res.sendFile(__dirname + "/views/front/index.html");
});

app.get("/book", (req, res) => {
  res.sendFile(__dirname + "/views/front/book.html");
});

app.get("/storeDetailed", (req, res) => {
  res.sendFile(__dirname + "/views/front/storeDetailed.html");
});

//-----------------------------------------------------------//
//------------------------- 後台API -------------------------//

app.get("/control/index", (req, res) => {
  res.sendFile(__dirname + "/views/back/index.html");
});

app.get("/control/storeDetailed", (req, res) => {
  res.sendFile(__dirname + "/views/back/storeDetailed.html");
});

app.get("/control/addStore", (req, res) => {
  res.sendFile(__dirname + "/views/back/addStore.html");
});

//-----------------------------------------------------------//
//-----------------------------------------------------------//

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
  console.log('Running on http://127.0.0.1:3000/index');
  console.log('Running on http://127.0.0.1:3000/control/index');
});