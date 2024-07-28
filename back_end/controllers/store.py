from flask import request

from controllers import app
from module import store


@app.route('/save_store_info', methods=['POST'])
def save_store_info_route():
    '''
    儲存店家資料
    '''
    data = request.get_json()
    return store.Save_StoreInfo(data)


@app.route('/get_store_info/<string:type>', methods=['POST'])
def get_store_info_route(type):
    '''
    取得店家資料
    '''
    data = request.get_json() 
    if type == 'Specific': # 取得特定店家訊息
        return store.Get_SpecificStoreInfo(data["storeId"], list(data["colName"]))    
    if type == 'All': # 取得所有店家訊息
        return store.Get_AllStoreInfo(list(data["colName"]))
    return {"status": "error", "content": "類型錯誤，類型選項：Specific、All"}


@app.route('/update_store_info', methods=['POST'])
def update_store_info_route():
    '''
    更新店家資料
    '''
    data = request.get_json()
    return store.Update_StoreInfo(data["storeId"], data)


@app.route('/record_page_views/<string:storeId>', methods=['GET'])
def record_page_views_route(storeId):
    '''
    記錄瀏覽次數
    '''
    return store.Record_PageViews(storeId)


@app.route('/get_page_views/<string:storeId>', methods=['GET'])
def get_page_views_route(storeId):
    '''
    取得瀏覽次數
    '''
    return store.Get_PageViews(storeId)