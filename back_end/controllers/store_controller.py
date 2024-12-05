from flask import request

from controllers import app
from controllers.decorator import verify_token, err_catch
from module.store import StoreService
from module.const import ErrCode


@app.route("/add_store_merchant", methods=["POST"])
@verify_token
@err_catch
def add_store_merchant_route(account_id):
    """
    儲存商店資料
    """

    data = request.get_json()

    StoreService.add_store_merchant(
        account_id=account_id,
        name=data["name"],
        address=data["address"],
        phone=data["phone"],
        office_url=data["office_url"],
        google_map_url=data["google_map_url"],
        intro=data["intro"],
        image=data["image"],
    )

    return {"status": "ok"}


@app.route("/get_store_traveler", methods=["GET"])
@err_catch
def get_store_traveler_route():
    """
    取得審核已通過商店
    """

    result = StoreService.get_store_traveler()

    return {"status": "ok", "content": result}


@app.route("/get_store_admin/<int:page_idx>", methods=["GET"])
@err_catch
def get_store_admin_route(page_idx):
    """
    取得待審核商店
    """

    result = StoreService.get_store_admin(page_idx)

    return {"status": "ok", "content": result}


@app.route("/get_store_merchant/<int:page_idx>", methods=["GET"])
@verify_token
@err_catch
def get_store_merchant_route(account_id, page_idx):
    """
    根據帳號取得由其管理的商店
    """

    result = StoreService.get_store_merchant(account_id, page_idx)

    return {"status": "ok", "content": result}


@app.route("/get_store_detailed_traveler", methods=["POST"])
def get_store_detailed_traveler_route():
    """
    取得商店詳細資料
    """

    data = request.get_json()

    result = StoreService.get_store_detailed_traveler(store_id=data["store_id"])

    return {"status": "ok", "content": result}


@app.route("/get_store_detailed_merchant", methods=["POST"])
@err_catch
def get_store_detailed_merchant_route():
    """
    取得商店詳細資料
    """

    data = request.get_json()

    result = StoreService.get_store_detailed_merchant(store_id=data["store_id"])

    return {"status": "ok", "content": result}


@app.route("/update_store_merchant", methods=["POST"])
@verify_token
@err_catch
def update_store_merchant_route(account_id):
    """
    更新商店資料
    """

    data = request.get_json()

    isSuccess = StoreService.update_store_merchant(
        account_id=account_id,
        store_id=data["store_id"],
        update_data=data["update_data"],
    )

    if isSuccess:
        return {"status": "ok"}
    else:
        return {"status": "error", "code": ErrCode.ACCOUNT_ID_ERROR}


@app.route("/approved_store", methods=["POST"])
@err_catch
def approved_store_route():
    """
    商店審核通過
    """

    data = request.get_json()

    StoreService.approved_store(store_id=data["store_id"])

    return {"status": "ok"}


@app.route("/rejected_store", methods=["POST"])
@err_catch
def rejected_store_route():
    """
    商店審核不通過
    """

    data = request.get_json()

    StoreService.rejected_store(store_id=data["store_id"])

    return {"status": "ok"}


@app.route("/record_store_page_views", methods=["POST"])
@err_catch
def record_store_page_views_route():
    """
    記錄商店瀏覽次數
    """

    data = request.get_json()

    StoreService.record_store_page_views(store_id=data["store_id"])

    return {"status": "ok"}


@app.route("/get_store_page_views", methods=["POST"])
@err_catch
def get_store_page_views_route():
    """
    取得商店瀏覽次數
    """

    data = request.get_json()

    result = StoreService.get_store_page_views(store_id=data["store_id"])

    return {"status": "ok", "content": result}


@app.route("/favorite_store", methods=["POST"])
@verify_token
@err_catch
def favorite_store_route(account_id):
    """
    收藏商店
    """

    data = request.get_json()

    StoreService.favorite_store(
        account_id=account_id,
        store_id=data["store_id"],
    )

    return {"status": "ok"}


@app.route("/cancel_favorite_store", methods=["POST"])
@verify_token
@err_catch
def cancel_favorite_store_route(account_id):
    """
    取消收藏商店
    """

    data = request.get_json()

    StoreService.cancel_favorite_store(
        account_id=account_id,
        store_id=data["store_id"],
    )

    return {"status": "ok"}


@app.route("/get_favorite_store_traveler", methods=["GET"])
@verify_token
@err_catch
def get_favorite_store_traveler_route(account_id):
    """
    取得收藏商店
    """

    result = StoreService.get_favorite_store_traveler(account_id)

    return {"status": "ok", "content": result}


@app.route("/get_favorite_store_id_traveler", methods=["GET"])
@verify_token
@err_catch
def get_favorite_store_id_traveler_route(account_id):
    """
    取得收藏商店
    """

    result = StoreService.get_favorite_store_id_traveler(account_id)

    return {"status": "ok", "content": result}


@app.route("/get_total_favorites", methods=["POST"])
@err_catch
def get_total_favorites_route():
    """
    取得總收藏數
    """

    data = request.get_json()

    result = StoreService.get_total_favorites(data["store_id"])

    return {"status": "ok", "content": result}


@app.route("/get_favorite_statistics", methods=["POST"])
@err_catch
def get_favorite_statistics_route():
    """
    取得今年每個月的收藏數
    """

    data = request.get_json()

    result = StoreService.get_favorite_statistics(data["store_id"])

    return {"status": "ok", "content": result}
