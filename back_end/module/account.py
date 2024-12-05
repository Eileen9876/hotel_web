from flask_bcrypt import Bcrypt
import re
import datetime
import jwt

from module.utils import generate_id36
from module.database import DbUtil
from module.const import ErrCode, JWT_KEY, TOKEN_VALID_HOURS


class AccountService:

    @staticmethod
    def login(email, password) -> dict:
        """驗證用戶憑據並處理登入邏輯。

        該函式會檢查電子郵件和密碼是否有效，驗證用戶帳戶的存在性及密碼的正確性。
        驗證成功後，返回包含 JWT token 和用戶資訊的結果。

        Returns:
            dict:
                - 成功回傳:
                    {
                        "status": "ok",
                        "content": {
                            "token": token,
                            "name": 用戶名稱,
                            "type": 用戶類型
                        }
                    }

                - 錯誤回傳:
                    {
                        "status": "error",
                        "code": 錯誤代碼
                    }
                    錯誤代碼包括：
                        - EMAIL_INVALID: 電子郵件格式無效。
                        - PWD_INVALID: 密碼格式無效。
                        - ACCOUNT_NOT_EXIST: 用戶帳戶不存在。
                        - PWD_WRONG: 密碼錯誤。

        Example:
            >>> result = login("user@example.com", "password123")s
        """
        if AccountUtil.is_email_valid(email) is False:
            return {"status": "error", "code": ErrCode.EMAIL_INVALID}

        if AccountUtil.is_password_valid(password) is False:
            return {"status": "error", "code": ErrCode.PWD_INVALID}

        account = AccountManager.get_account(email)

        if account is None:
            return {"status": "error", "code": ErrCode.ACCOUNT_NOT_EXIST}

        if AccountUtil.verify_password(account["account_password"], password) is False:
            return {"status": "error", "code": ErrCode.PWD_WRONG}

        token = AccountUtil.generate_token(account["account_id"])

        return {
            "status": "ok",
            "content": {
                "token": token,
                "name": account["account_name"],
                "type": account["account_type"],
            },
        }

    @staticmethod
    def register(name: str, email: str, password: str, type: str) -> dict:
        """用戶註冊

        Returns:
            dict:
                - 成功回傳：
                    {
                        "status": "ok"
                    }
                - 錯誤回傳：
                    {
                        "status": "error",
                        "code": 錯誤代碼
                    }
                    錯誤代碼包括：
                        - EMAIL_INVALID: 電子郵件格式無效。
                        - PWD_INVALID: 密碼格式無效。
        """
        if AccountUtil.is_email_valid(email) is False:
            return {"status": "error", "code": ErrCode.EMAIL_INVALID}

        if AccountUtil.is_password_valid(password) is False:
            return {"status": "error", "code": ErrCode.PWD_INVALID}

        hashed_password = AccountUtil.hash_password(password)

        AccountManager.add_account(name, email, hashed_password, type)

        return {"status": "ok"}


class AccountManager:
    @staticmethod
    def add_account(name: str, email: str, hashed_password: str, type: str):
        """新增帳戶資料

        建立帳戶識別碼並進行儲存。
        """

        # 建立識別碼
        id = generate_id36()

        # SQL 查詢語句
        query = """
            INSERT INTO account (account_id, account_name, account_email, account_password, account_type)
            VALUES (%s, %s, %s, %s, %s);
        """

        # 新增至資料庫
        DbUtil.execute(
            query,
            (
                id,
                name,
                email,
                hashed_password,
                type,
            ),
        )

    @staticmethod
    def get_account(email: str) -> dict | None:
        """根據email從資料庫取得帳戶資料

        Args:
            email (str): 登入使用的帳號

        Returns:
            dict | None:
                - 成功:
                    {
                        "account_id": 帳戶識別碼
                        "account_name": 姓名
                        "account_email": 信箱
                        "account_passsword": 密碼，哈希值
                        "account_type": 帳戶類別，包含 'merchant'、'traveler'
                    }
                - 失敗: None
        """
        # 要提取的欄位
        column = [
            "account_id",
            "account_name",
            "account_email",
            "account_password",
            "account_type",
        ]

        # SQL 查詢語句
        query = f"""
            SELECT {", ".join(column)}
            FROM account
            WHERE account_email = %s
            LIMIT 1;
        """

        # 取值
        data = DbUtil.execute_fetch_one(query, (email,))

        if not data:
            return None

        return {col: data[idx] for idx, col in enumerate(column)}


class AccountUtil:
    bcrypt = Bcrypt()

    @staticmethod
    def generate_token(id: str) -> str:
        expiration = datetime.datetime.now() + datetime.timedelta(
            hours=TOKEN_VALID_HOURS
        )

        token = jwt.encode({"id": id, "exp": expiration}, JWT_KEY, algorithm="HS256")

        return token

    @staticmethod
    def decode_and_validate_token(token: str) -> dict:
        """驗證 JWT token 是否有效，並解碼獲取用戶 ID。

        該函式會使用預定的密鑰來解碼並驗證 JWT，如果驗證成功，會回傳包含用戶 ID 的結果，
        如果 token 過期或無效，則會返回對應的錯誤代碼。

        Args:
            token (str): 用戶端傳遞的 JWT token。

        Returns:
            dict:
                - 若驗證成功，回傳 {"status": True, "id": user_id}
                - 若 token 過期，回傳 {"status": False, "code": TOKEN_EXPIRE}
                - 若 token 無效，回傳 {"status": False, "code": TOKEN_INVALID}

        Example:
            >>> result = verify_token("jwt_token_here")
            >>> if result["status"]:
            >>>     user_id = result["id"]
            >>> else:
            >>>     error_code = result["code"]
        """
        try:
            # 解碼並驗證 JWT
            data = jwt.decode(token, JWT_KEY, algorithms=["HS256"])

            # 取得id
            id = data["id"]

            return {"status": True, "id": id}

        except jwt.ExpiredSignatureError:
            return {"status": False, "code": ErrCode.TOKEN_EXPIRE}

        except jwt.InvalidTokenError:
            return {"status": False, "code": ErrCode.TOKEN_INVALID}

    @staticmethod
    def is_password_valid(password) -> bool:
        """確認密碼是否符合規則，僅包含英文字母（大小寫）和數字"""
        pattern = r"^[A-Za-z0-9]+$"  # 僅包含英文字母（大小寫）和數字
        return bool(re.match(pattern, password))

    @staticmethod
    def is_email_valid(email: str) -> bool:
        """驗證 email 格式是否正確"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def hash_password(password: str) -> str:
        """密碼雜湊"""
        hashed_password = AccountUtil.bcrypt.generate_password_hash(password=password)
        return hashed_password.decode("utf-8")

    @staticmethod
    def verify_password(hashed_password: str, password: str) -> bool:
        """密碼驗證"""
        return AccountUtil.bcrypt.check_password_hash(hashed_password, password)
