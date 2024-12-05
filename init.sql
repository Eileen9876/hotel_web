USE Hotel;

CREATE TABLE account (
  account_id CHAR(36) PRIMARY KEY,
  account_name VARCHAR(50) NOT NULL,
  account_email VARCHAR(100) NOT NULL,
  account_password VARCHAR(255) NOT NULL,
  UNIQUE(account_email),
  account_type VARCHAR(10) NOT NULL CHECK (account_type IN ('MERCHANT', 'TRAVELER'))
);

CREATE TABLE reservation (
  reserve_id CHAR(36) PRIMARY KEY,
  check_in_date DATE NOT NULL,
  check_out_date DATE NOT NULL,
  account_id CHAR(36) NOT NULL,
  room_number CHAR(3) NOT NULL,
  room_type VARCHAR(10) NOT NULL,
  FOREIGN KEY(account_id) REFERENCES account(account_id) ON DELETE CASCADE
);

CREATE TABLE store_record (
  store_id CHAR(36) PRIMARY KEY,
  store_name NVARCHAR(50) NOT NULL,
  store_address NVARCHAR(255) NOT NULL,
  store_phone NVARCHAR(20) NOT NULL,
  store_intro NVARCHAR(2048),
  office_url NVARCHAR(2048),
  google_map_url NVARCHAR(2048),
  account_id CHAR(36) NOT NULL,
  review_status VARCHAR(10) DEFAULT 'PENDING' NOT NULL CHECK (
    review_status IN ('PENDING', 'APPROVED', 'REJECTED')
  ),
  UNIQUE(store_phone),
  FOREIGN KEY(account_id) REFERENCES account(account_id) ON DELETE CASCADE
);

CREATE TABLE store (
  store_id CHAR(36) PRIMARY KEY,
  store_name NVARCHAR(50) NOT NULL,
  store_address NVARCHAR(255) NOT NULL,
  store_phone NVARCHAR(20) NOT NULL,
  store_intro NVARCHAR(2048),
  office_url NVARCHAR(2048),
  google_map_url NVARCHAR(2048),
  account_id CHAR(36) NOT NULL,
  UNIQUE(store_phone),
  FOREIGN KEY(account_id) REFERENCES account(account_id) ON DELETE CASCADE,
  FOREIGN KEY(store_id) REFERENCES store_record(store_id) ON DELETE CASCADE
);

CREATE TABLE store_image_record (
  store_id CHAR(36) PRIMARY KEY,
  store_image LONGTEXT NOT NULL,
  FOREIGN KEY(store_id) REFERENCES store_record(store_id) ON DELETE CASCADE
);

CREATE TABLE store_image (
  store_id CHAR(36) PRIMARY KEY,
  store_image LONGTEXT NOT NULL,
  FOREIGN KEY(store_id) REFERENCES store(store_id) ON DELETE CASCADE
);

CREATE TABLE store_view (
  store_id CHAR(36) NOT NULL,
  view_time DATETIME NOT NULL,
  FOREIGN KEY(store_id) REFERENCES store(store_id) ON DELETE CASCADE
);

CREATE TABLE store_favorite_record (
  store_id CHAR(36) NOT NULL,
  account_id CHAR(36) NOT NULL,
  fav_status BOOLEAN NOT NULL,
  fav_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(store_id) REFERENCES store(store_id) ON DELETE CASCADE,
  FOREIGN KEY(account_id) REFERENCES account(account_id) ON DELETE CASCADE
);

CREATE TABLE store_favorite (
  store_id CHAR(36) NOT NULL,
  account_id CHAR(36) NOT NULL,
  fav_status BOOLEAN NOT NULL,
  UNIQUE(store_id, account_id),
  FOREIGN KEY(store_id) REFERENCES store(store_id) ON DELETE CASCADE,
  FOREIGN KEY(account_id) REFERENCES account(account_id) ON DELETE CASCADE
);