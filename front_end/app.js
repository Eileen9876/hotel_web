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

//------------------------- 旅客相關 API -------------------------//

app.get("/traveler/index", (req, res) => {
  res.sendFile(__dirname + "/views/traveler/index.html");
});

app.get("/traveler/book", (req, res) => {
  res.sendFile(__dirname + "/views/traveler/book.html");
});

app.get("/traveler/storeDetailed", (req, res) => {
  res.sendFile(__dirname + "/views/traveler/storeDetailed.html");
});

//-----------------------------------------------------------//
//----------------------- 商家相關 API -----------------------//

app.get("/merchant/index", (req, res) => {
  res.sendFile(__dirname + "/views/merchant/index.html");
});

app.get("/merchant/storeDetailed", (req, res) => {
  res.sendFile(__dirname + "/views/merchant/storeDetailed.html");
});

app.get("/merchant/addStore", (req, res) => {
  res.sendFile(__dirname + "/views/merchant/addStore.html");
});

//-----------------------------------------------------------//
//---------------------- 管理員相關 API ----------------------//

app.get("/admin/index", (req, res) => {
  res.sendFile(__dirname + "/views/admin/index.html");
});

app.get("/admin/storeDetailed", (req, res) => {
  res.sendFile(__dirname + "/views/admin/storeDetailed.html");
});

//-----------------------------------------------------------//
//-----------------------------------------------------------//

app.get("/index", (req, res) => {
  res.sendFile(__dirname + "/views/index.html");
});

app.get("/login", (req, res) => {
  res.sendFile(__dirname + "/views/login.html");
});

app.get("/register", (req, res) => {
  res.sendFile(__dirname + "/views/register.html");
});

app.get("/storeDetailed", (req, res) => {
  res.sendFile(__dirname + "/views/storeDetailed.html");
});

//-----------------------------------------------------------//
//-----------------------------------------------------------//

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
  console.log('Running on http://127.0.0.1:3000/index');
  console.log('Running on http://127.0.0.1:3000/admin/index');
});