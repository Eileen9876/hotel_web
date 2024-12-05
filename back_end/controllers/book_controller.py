from flask import request

from controllers import app
from controllers.decorator import verify_token, err_catch
from module.book import BookManager, BookService


@app.route("/booking", methods=["POST"])
@verify_token
@err_catch
def booking_route(account_id):
    """新增訂房資訊"""

    data = request.get_json()

    result_code = BookService.booking(
        account_id=account_id,
        room_type=data["room_type"],
        check_in_date=data["check_in_date"],
        check_out_date=data["check_out_date"],
    )

    if result_code == 0:
        return {"status": "ok"}

    return {"status": "error", "code": result_code}


@app.route("/get_booking_info/traveler", methods=["POST"])
@verify_token
@err_catch
def get_booking_info_traveler_route(account_id):
    """取得資料庫中指定的旅客的訂房紀錄（依條件提取）"""

    data = request.get_json()

    booking_info = BookManager.get_booking_info_traveler(
        account_id=account_id,
        start_date=data["start_date"],
        end_date=data["end_date"],
        page_idx=data["page_index"],
    )

    return {"status": "ok", "content": booking_info}


@app.route("/get_booking_info/admin", methods=["POST"])
@err_catch
def get_booking_info_admin_route():
    """取得資料庫中的訂房紀錄（依條件提取）"""

    data = request.get_json()

    booking_info = BookManager.get_booking_info_admin(
        name=data["name"],
        start_date=data["start_date"],
        end_date=data["end_date"],
        page_idx=data["page_index"],
    )

    return {"status": "ok", "content": booking_info}
