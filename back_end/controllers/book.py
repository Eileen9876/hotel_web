from flask import request

from controllers import app
from module import book

'''
新增訂房資訊
'''
@app.route('/save_book_info', methods=['POST'])
def save_book_info_route():
    data = request.get_json()

    # 確認是否有空房
    roomId = book.Check_RoomAvailable(
        data["arrDate"], 
        data["depDate"], 
        data["roomType"]
    )

    if roomId == "error":
        return {"status": "error", "content": "該時段已客滿"}
    
    # 儲存訂房資訊
    data["roomId"] = roomId

    return book.Save_BookInfo(data)

'''
取得資料庫中的訂房紀錄（依條件提取）
'''
@app.route('/get_book_info', methods=['POST'])
def get_book_info_route():
    data = request.get_json() 

    return book.Get_BookInfo(data["name"], 
                             data["startDate"], 
                             data["endDate"], 
                             data["pageIdx"])

