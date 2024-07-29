# 飯店網站

## 使用
檔案下載後，輸入指令 `docker-compose up --build`，即啟動服務。
啟動服務後，會在本地端自動建立 data 資料夾用於儲存備份檔案，該資料夾內有三個資料夾 roomUseDate、storeInfo、sql_backup。

roomUseDate 用於儲存各個房間無法使用的日期。

storeInfo 儲存周邊商家相關圖片（mime 格式），包含店面圖片、Qrcode圖片。

sql_backup 資料庫備份檔。

要使用備份後的資料，請先在本地建立 data 資料夾，並將檔案放置對應的資料夾中，再啟動服務即可。
