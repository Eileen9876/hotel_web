USE Hotel;

CREATE TABLE bookRecord (
  bookId char(8) PRIMARY KEY,
  roomId char(2) NOT NULL,
  name NVARCHAR(50) NOT NULL,
  email NVARCHAR(100) NOT NULL,
  arrDate DATE NOT NULL,
  depDate DATE NOT NULL,
  people INT NOT NULL,
  roomType VARCHAR(10) NOT NULL
);

CREATE TABLE storeInfo (
  storeId char(8) PRIMARY KEY,
  storeName NVARCHAR(50) NOT NULL,
  address NVARCHAR(255) NOT NULL,
  phone NVARCHAR(20) NOT NULL,
  officeURL NVARCHAR(2048),
  googleMapURL NVARCHAR(2048),
  info NVARCHAR(2048)
);

CREATE TABLE storePageViews (
  storeId char(8) NOT NULL,
  clickTime DATETIME NOT NULL
);