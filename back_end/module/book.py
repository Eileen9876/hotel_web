from datetime import datetime, timedelta
import json
import random
import traceback
import module.envvar as ENVVAR
from module.database import DbHandler

dbHandler = DbHandler(
    ENVVAR.DB_HOST,
    ENVVAR.DB_PORT,
    ENVVAR.DB_USER,
    ENVVAR.DB_PASSWORD,
    'Hotel'
)

def Save_BookInfo(data: dict) -> dict:
    '''
    儲存訂房資訊

    Returns:
        dict: 回傳執行結果，
             成功回傳 {"status": "ok", "content": ""}，
             失敗回傳 {"status": "error", "content": str(ex)} 
    '''
    try:
        # 新增指定房號的使用日期
        with open('data/roomUseDate.json', 'r') as file: 
            room_unable_date = json.load(file)

        arr_date = datetime.strptime(data["arrDate"], '%Y-%m-%d').date()
        dep_date = datetime.strptime(data["depDate"], '%Y-%m-%d').date()

        room_unable_date[data["roomType"]][data["roomId"]].append(str(arr_date))
        date = arr_date
        while date != dep_date:
            date += timedelta(days=1)
            room_unable_date[data["roomType"]][data["roomId"]].append(str(date))

        with open('data/roomUseDate.json', 'w') as file: 
            json.dump(room_unable_date, file)
        
        # 訂房編號設置
        bookId = __Get_RandomInt(8)
        data["bookId"] = bookId

        # 儲存至資料庫
        dbHandler.Insert("bookRecord", data)

        return {"status": "ok", "content": ""}
    
    except Exception as ex:
        __Handle_Exception()
        
        return {"status": "error", "content": str(ex)}


def Check_RoomAvailable(arrDate: str, depDate: str, roomType: str) -> str:
    '''
    確認是否有空房，有空房則回傳房號

    Returns:
        str: 有空房回傳房號，無空房回傳"error"
    '''
    # 列出使用日期
    arr_date = datetime.strptime(arrDate, '%Y-%m-%d').date()
    dep_date = datetime.strptime(depDate, '%Y-%m-%d').date()

    use_date = [str(arr_date)]
    date = arr_date
    while date != dep_date:
        date += timedelta(days=1)
        use_date.append(str(date))

    # 確認是否有空房
    with open('data/roomUseDate.json') as file: 
        room_unable_date = json.load(file)

    for roomId in room_unable_date[roomType]:
        dates = room_unable_date[roomType][roomId] # 提取該房間會被使用的日子

        # 確認預定日期是否有人使用
        able = True
        for date in use_date: 
            if date in dates: # 該日期房間已有人使用
                able = False
                break

        if able:
            return roomId

    return "error"


def Get_BookInfo(name: str, startDate: str, endDate: str, pageIdx: int) -> dict:
    try: 
        # 初始值設置
        colName = ["bookId", "roomId", "roomType", "name", "email", "arrDate", "depDate", "people"]
        
        pageSize = 10

        offset = (pageIdx-1) * pageSize

        if not startDate and endDate: startDate = endDate
        elif startDate and not endDate: endDate = startDate

        # 條件設置
        cdn_list = []

        if startDate: 
            cdn_list.append(f"arrDate <= '{startDate}'")
            cdn_list.append(f"depDate >= '{endDate}'")

        if name:
            cdn_list.append(f"name = '{name}'")

        # 查詢語句設置
        condition = "WHERE " + " AND ".join(cdn_list) if cdn_list else ""
        columns = ["bookId", "roomId", "roomType", "name", "email", 
                   "DATE_FORMAT(arrDate, '%Y-%m-%d') AS arrDate", 
                   "DATE_FORMAT(depDate, '%Y-%m-%d') AS depDate", "people"]

        query = f"""
            SELECT {", ".join(columns)} 
            FROM bookRecord
            {condition}
            ORDER BY arrDate DESC
            LIMIT {pageSize} OFFSET {offset};
        """

        # 資料庫連線查詢
        dbHandler.Connect()

        dbData = dbHandler.ExecuteQuery_Return(query)

        # 處理結果
        result = []
        for dbData_ in dbData:
            result.append({col: dbData_[i] for i, col in enumerate(colName)})

        return {"status": "ok", "content": result}

    except Exception as ex:
        __Handle_Exception()

        return {"status": "error", "content": str(ex)}
    
    
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

def __Handle_Exception():
    traceback.print_exc()