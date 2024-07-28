from datetime import datetime
import io
import qrcode
import base64
import random
import json
import traceback

import module.envvar as ENVVAR
from module.database import DbHandler, Condition

dbHandler = DbHandler(
    ENVVAR.DB_HOST,
    ENVVAR.DB_PORT,
    ENVVAR.DB_USER,
    ENVVAR.DB_PASSWORD,
    'Hotel'
)

def Save_StoreInfo(data: dict) -> dict:
    '''
    儲存商店訊息

    Returns:
        dict: 執行錯誤回傳 {"status": "error", "content": str(ex)}，
              執行成功回傳 {"status": "ok", "content": ""}
    '''
    try: 
        # 設置商店編號
        storeId = __Get_RandomInt(8)
        data["storeId"] = storeId

        # 儲存影像至本地端 data/storeInfo.json 檔案
        # storeImage 轉成 MIME 格式儲存
        # officeURL 與 googleMapURL 轉成二維碼，並轉成 MIME 格式儲存
        with open('data/storeInfo.json', 'r+') as file: 
            imageData = json.load(file)

            imageData[storeId] = {
                "storeImage": data["storeImage"],
                "officeURL": __Url_To_QrcodeMime(data["officeURL"]),
                "googleMapURL": __Url_To_QrcodeMime(data["googleMapURL"])
            }

            file.seek(0) # 指針移至文件開頭，以覆蓋內容
            json.dump(imageData, file)
            file.truncate() # 截斷文件

            data.pop("storeImage")

        # 儲存資料至資料庫
        dbHandler.Insert("storeInfo", data)

        return {"status": "ok", "content": ""} 
    
    except Exception as ex:
        __Handle_Exception()

        return {"status": "error", "content": str(ex)} 


def Get_AllStoreInfo(colName: list) -> dict:
    '''
    取得每間商店的資訊

    Args:
        colName (list): 要取得的資訊

    Returns:
        dict: 執行錯誤回傳 {"status": "error", "content": str(ex)}，
              執行成功回傳 {"status": "ok", "content": result}
              result 範例 
    '''
    try: 
        # 取得資料
        imageData = {}
        if "image" in colName:
            colName.pop(colName.index("image"))
            imageData = __Get_Image()
            
        dbData = dbHandler.Select("storeInfo", colName)
        
        # 資料處理
        primary_key_idx = colName.index("storeId")
        result = {}
        for dbData_ in dbData:
            result[dbData_[primary_key_idx]] = {
                col: dbData_[i] for i, col in enumerate(colName)
            }

        if imageData:
            for id in imageData.keys():
                result[id]["image"] = imageData[id]

        return {"status": "ok", "content": result}
    
    except Exception as ex:
        __Handle_Exception()
        
        return {"status": "error", "content": str(ex)} 


def Get_SpecificStoreInfo(id: str, colName: list) -> dict:
    '''
    取得指定商店的資訊

    Args:
        id (str): 指定的商店編號
        colName (list): 要取得的資訊
    '''
    try: 

        # 取得本地影像
        imageData = {}
        if "image" in colName:
            colName.pop(colName.index("image"))
            imageData = __Get_Image(id)

        # 取得資料庫資料
        cdn = Condition()
        cdn.Append("storeId", id)

        dbData = dbHandler.SelectWhere("storeInfo", colName, cdn.Create())

        # 處理資料
        result = {
            col: dbData[0][i] for i, col in enumerate(colName)
        }

        # 處理影像資料
        if imageData:
            result["image"] = imageData

        return {"status": "ok", "content": result}

    except Exception as ex:
        __Handle_Exception()

        return {"status": "error", "content": str(ex)} 


def Update_StoreInfo(id: str, data: dict) -> dict:
    '''
    更新指定商店的資訊

    Args:
        id (str): 指定的商店編號
        data (dict): 要更新的資料，
                     格式 { 要更改的欄位: 更新後的值 }，
                     範例 { "people": 5 }
    
    Returns:
        dict: 回傳執行結果，
             成功回傳 {"status": "ok", "content": ""}，
             失敗回傳 {"status": "error", "content": str(ex)}     
    '''
    try: 
        # 更新本地資料
        if "storeImage" in data or "officeURL" in data  or "googleMapURL" in data :
            with open('data/storeInfo.json', 'r+') as file: 
                imageData = json.load(file)

                if "storeImage" in data : 
                    imageData[id]["storeImage"] = data["storeImage"]
                    data.pop("storeImage")

                if "officeURL" in data : 
                    imageData[id]["officeURL"] = __Url_To_QrcodeMime(data["officeURL"])       

                if "googleMapURLL" in data : 
                    imageData[id]["googleMapURL"] = __Url_To_QrcodeMime(data["googleMapURL"])

                file.seek(0) # 指針移至文件開頭，以覆蓋內容
                json.dump(imageData, file)
                file.truncate() # 截斷文件


        # 更新資料庫資料
        cdn = Condition()
        cdn.Append("storeId", id)

        dbHandler.Update("storeInfo", data, cdn.Create())

        return {"status": "ok", "content": ""} 
    
    except Exception as ex:
        __Handle_Exception()

        return {"status": "error", "content": str(ex)} 


def Record_PageViews(id: str) -> str:
    '''
    紀錄

    Args:
        id (str): 商店編號
    '''
    try: 
        data = {
            "storeId": id,
            "clickTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        dbHandler.Insert("storePageViews", data)
        return "ok"

    except Exception as ex:
        __Handle_Exception()
        return "error"
  

def Get_PageViews(id: str) -> dict:
    '''
    取得今年的瀏覽次數，以月計算。

    Args:
        id (str): 商店編號

    Returns:
        dict: 
    '''
    try:
        query = """
            SELECT MONTH(clickTime) AS month, COUNT(*) AS cnt
            FROM storePageViews
            WHERE storeId = %s
                AND YEAR(clickTime) = YEAR(CURDATE())
            GROUP BY YEAR(clickTime), MONTH(clickTime)
            ORDER BY MONTH(clickTime);
        """
            
        dbData = dbHandler.ExecuteQuery_Return(query, (id,)) 

        result = [0] * 12
        for data in dbData:
            result[data[0]-1] = data[1] # data[0]: 月份，data[1]: 次數

        return {"status": "ok", "content": result}

    except Exception as ex:
        __Handle_Exception()

        return {"status": "error", "content": str(ex)}  


def __Url_To_QrcodeMime(url: str) -> str:
    '''
    將轉換網址為 QRCode，再轉成 MIME 格式的字符串

    Args:
        url (str): 要轉換為 QRCode 的網址
    
    Returns:
        str: QRCode 圖像的 MIME 格式
    '''
    image = qrcode.make(url)

    # 將圖像轉換為字符流
    image_bytes = io.BytesIO()
    image.save(image_bytes)
    image_bytes.seek(0)

    # 轉成 Base64 字符串
    encoded_str = base64.b64encode(image_bytes.read()).decode()

    # 獲取 MIME 格式
    mime_str = 'data:image/png;base64,' + encoded_str
    
    return mime_str


def __Get_Image(id: str = "") -> dict:
    result = {}

    with open('data/storeInfo.json', 'r') as file: 
        imageData = json.load(file)
        
    if id == "": # 提取全部
        result = imageData

    else: # 提取特定
        result = imageData[id]

    return result


def __Get_RandomInt(size: int) -> int:
    '''
    取得亂數值

    Args:
        size (int): 位數
    
    Returns:
        int: 亂數值
    '''
    result = ""
    for i in range(size):
        result += str(random.randint(0, 9))
    return result


def __Find_Index(L: list, value: str) -> int:
    '''
    尋找值在列表中的索引。假如值不存在於列表中，則將值添加於列表末端
    
    Args:
        L (list): 列表
        value (str): 要尋找的值

    Returns:
        int: 值在列表中的索引
    '''

    if value not in L:
        L.append(value)
    
    return L.index(value)

def __Handle_Exception():
    traceback.print_exc()