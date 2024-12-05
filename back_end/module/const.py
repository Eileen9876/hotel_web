from dotenv import load_dotenv
import os

# 載入 .env 文件中的變數
load_dotenv()

# 資料庫連線資訊
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# 使用 JWT 建立 Token 所需的金鑰
JWT_KEY = os.getenv("JWT_KEY")

# token 有效時間
TOKEN_VALID_HOURS = 1


class ErrCode:
    TOKEN_EXPIRE = 101  # token 過期
    TOKEN_INVALID = 102  # token 無效
    TOKEN_NONE = 103  # 無 token

    EMAIL_INVALID = 201  # email不符合格式
    PWD_INVALID = 202  # 密碼不符合規定
    PWD_WRONG = 203  # 密碼錯誤
    ACCOUNT_NOT_EXIST = 204  # 帳號不存在
    ACCOUNT_ID_ERROR = 205  # 帳號識別碼錯誤

    FULLY_BOOKED = 301  # 該時段已客滿

    UNKNOWN = 999  # 不明錯誤
