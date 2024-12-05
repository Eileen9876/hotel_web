from flask import request
from functools import wraps
import traceback

from module.utils import get_value_or_none_from_list, split_string_by_delimiter
from module.const import ErrCode
from module.account import AccountUtil


def verify_token(callback):
    @wraps(callback)
    def decorator(*args, **kwargs):
        token = None

        # 從請求的 Authorization 標頭中取得 token
        # Authorization 由 Bearer + 空格 + token 組成
        # 取出 Authorization > 使用空格作為分割符切割字串 > 取出 token
        if "Authorization" in request.headers:
            auth = request.headers.get("Authorization")

            auth_split = split_string_by_delimiter(auth, " ")

            token = get_value_or_none_from_list(auth_split, 1)

        # 無 token 則回傳錯誤
        if not token:
            return {"status": "error", "content": ErrCode.TOKEN_NONE}

        # 驗證 token 是否正確，並取得帳號識別碼
        result = AccountUtil.decode_and_validate_token(token)

        if result["status"] == False:
            return {"status": "error", "code": result["code"]}

        return callback(result["id"], *args, **kwargs)

    return decorator


def err_catch(callback):
    @wraps(callback)
    def decorator(*args, **kwargs):
        try:
            return callback(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            return {"status": "error", "code": ErrCode.UNKNOWN}

    return decorator
