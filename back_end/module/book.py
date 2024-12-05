from datetime import datetime, timedelta
import json

from module.const import ErrCode
from module.database import DbUtil
from module.utils import generate_id36, has_common_elements


class BookService:
    @staticmethod
    def booking(
        account_id: str,
        room_type: str,
        check_in_date: str,
        check_out_date: str,
    ) -> int:
        """訂房

        Args:
            account_id (str): 帳戶識別碼
            room_type (str): 房型，包含'single', 'double', 'quad'
            check_in_date (str): 入住日期，格式為 'YYYY-MM-DD'
            check_out_date (str): 退房日期，格式為 'YYYY-MM-DD'

        Returns:
            int: 執行結果
                - 成功: 0
                - 失敗: 301 (無可用房間)
        """

        # 取得房號
        room_number = BookManager.get_available_room_number(
            check_in_date,
            check_out_date,
            room_type,
        )

        if room_number == None:
            return ErrCode.FULLY_BOOKED

        # 新增訂房資訊
        BookManager.add_booking_info(
            check_in_date,
            check_out_date,
            account_id,
            room_number,
            room_type,
        )

        return 0


class BookManager:
    ROOM_USAGE_DATE_FILE = "data/room_usage_date.json"

    @staticmethod
    def add_booking_info(
        check_in_date: str,
        check_out_date: str,
        account_id: str,
        room_number: str,
        room_type: str,
    ):
        """新增訂房資訊"""
        # 新增指定房號的使用日期
        BookManager.__add_room_usage_dates(
            check_in_date, check_out_date, room_type, room_number
        )

        # 訂房編號設置
        reserve_id = generate_id36()

        # 儲存至資料庫
        BookManager.__insert_to_database(
            reserve_id,
            check_in_date,
            check_out_date,
            account_id,
            room_number,
            room_type,
        )

    @staticmethod
    def get_booking_info_traveler(
        account_id: str, start_date: str, end_date: str, page_idx: int
    ) -> list:
        """獲取訂房資訊

        Args:
            account_id (str): 帳號識別碼。
            start_date (str): 開始日期。
            end_date (str): 結束日期。
            page_idx (int): 分頁索引。

        Returns:
            list:
            >>> [
            >>>     {
            >>>         "reserve_id": 訂房識別碼str
            >>>         "check_in_date": 入住日str, 格式為 'YYYY-MM-DD'
            >>>         "check_out_date": 退房日str, 格式為 'YYYY-MM-DD'
            >>>         "room_number": 房號str
            >>>         "room_type": 房型str
            >>>     },
            >>> ]
        """

        column = [
            "reserve_id",
            "check_in_date",
            "check_out_date",
            "room_number",
            "room_type",
        ]  # 欄位名稱

        page_size = 10  # 每頁顯示最大筆數

        offset = (page_idx - 1) * page_size  # 第幾頁

        where_sql = BookManager.__generate_booking_select_condition(
            start_date=start_date, end_date=end_date, account_id=account_id
        )

        query = f"""
            SELECT 
                reservation.reserve_id AS reserve_id, 
                DATE_FORMAT(reservation.check_in_date, '%Y-%m-%d') AS check_in_date, 
                DATE_FORMAT(reservation.check_out_date, '%Y-%m-%d') AS check_out_date, 
                reservation.room_number AS room_number, 
                reservation.room_type AS room_type, 
                account.account_name AS account_name,
                account.account_email AS account_email
            FROM reservation
            INNER JOIN account
            ON reservation.account_id = account.account_id
            {where_sql}
            LIMIT {page_size} OFFSET {offset};
        """

        # 資料庫連線查詢
        db_data = DbUtil.execute_fetch_all(query)

        # 處理結果
        result = []
        for db_data_ in db_data:
            result.append({col: db_data_[i] for i, col in enumerate(column)})

        return result

    @staticmethod
    def get_booking_info_admin(
        name: str, start_date: str, end_date: str, page_idx: int
    ) -> list:
        """獲取訂房資訊

        Args:
            name (str): 旅客姓名。
            start_date (str): 開始日期。
            end_date (str): 結束日期。
            page_idx (int): 分頁索引。

        Returns:
            list:
            [
                {
                    "reserve_id": 訂房識別碼str
                    "check_in_date": 入住日str, 格式為 'YYYY-MM-DD'
                    "check_out_date": 退房日str, 格式為 'YYYY-MM-DD'
                    "room_number": 房號str
                    "room_type": 房型str
                    "account_name": 帳號姓名str
                    "account_email": 帳號信箱str
                }
            ]
        """

        column = [
            "reserve_id",
            "check_in_date",
            "check_out_date",
            "room_number",
            "room_type",
            "account_name",
            "account_email",
        ]  # 欄位名稱

        page_size = 10  # 每頁顯示最大筆數

        offset = (page_idx - 1) * page_size  # 第幾頁

        where_sql = BookManager.__generate_booking_select_condition(
            start_date=start_date, end_date=end_date, account_name=name
        )

        query = f"""
            SELECT 
                reservation.reserve_id AS reserve_id, 
                DATE_FORMAT(reservation.check_in_date, '%Y-%m-%d') AS check_in_date, 
                DATE_FORMAT(reservation.check_out_date, '%Y-%m-%d') AS check_out_date, 
                reservation.room_number AS room_number, 
                reservation.room_type AS room_type, 
                account.account_name AS account_name,
                account.account_email AS account_email
            FROM reservation
            INNER JOIN account 
            ON reservation.account_id = account.account_id
            {where_sql}
            LIMIT {page_size} OFFSET {offset};
        """

        # 資料庫連線查詢
        db_data = DbUtil.execute_fetch_all(query)

        # 處理結果
        result = []
        for db_data_ in db_data:
            result.append({col: db_data_[i] for i, col in enumerate(column)})

        return result

    @staticmethod
    def get_available_room_number(
        check_in_date: str, check_out_date: str, room_type: str
    ) -> str | None:
        """取得房號

        Returns:
            str: 有空房回傳房號，無空房回傳None
        """

        # 取得使用日期
        booking_dates = BookManager.__get_booking_dates(check_in_date, check_out_date)

        # 確認是否有空房
        with open(BookManager.ROOM_USAGE_DATE_FILE) as file:
            room_unable_dates = json.load(file)

        for room_number in room_unable_dates[room_type]:
            # 提取該房間會被使用的日子
            unable_dates = room_unable_dates[room_type][room_number]

            # 確認房間在這段時間內是否有人使用
            is_room_available = has_common_elements(unable_dates, booking_dates)

            if is_room_available == False:
                return room_number

        return None

    @staticmethod
    def __insert_to_database(
        reserve_id: str,
        check_in_date: str,
        check_out_date: str,
        account_id: str,
        room_number: str,
        room_type: str,
    ):
        query = """
            INSERT INTO reservation (
                reserve_id, 
                check_in_date, 
                check_out_date, 
                account_id, 
                room_number, 
                room_type
            ) VALUES (
                %s, %s, %s, %s, %s, %s 
            );
        """

        DbUtil.execute(
            query,
            (
                reserve_id,
                check_in_date,
                check_out_date,
                account_id,
                room_number,
                room_type,
            ),
        )

    @staticmethod
    def __add_room_usage_dates(
        check_in_date: str, check_out_date: str, room_type: str, room_number: str
    ):
        """新增指定房號的使用日期

        取得入住期間的所有日期，並儲存至 room_usage_date.json 檔案中。
        """

        # 取得入住期間的所有日期
        booking_dates = BookManager.__get_booking_dates(check_in_date, check_out_date)

        # 將日期記錄在檔案中
        with open(BookManager.ROOM_USAGE_DATE_FILE, "r+") as file:
            room_unable_date = json.load(file)

            room_unable_date[room_type][room_number].extend(booking_dates)

            file.seek(0)

            json.dump(room_unable_date, file)

            file.truncate()  # 確保文件不含多餘內容

    @staticmethod
    def __get_booking_dates(check_in_date: str, check_out_date: str) -> list:
        """取得入住期間的所有日期"""

        start_date = datetime.strptime(check_in_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(check_out_date, "%Y-%m-%d").date()

        use_dates = [str(start_date)]
        date = start_date
        while date != end_date:
            date += timedelta(days=1)
            use_dates.append(str(date))

        return use_dates

    @staticmethod
    def __generate_booking_select_condition(
        start_date: str | None = None,
        end_date: str | None = None,
        account_name: str | None = None,
        account_id: str | None = None,
    ) -> str:
        """根據參數建立條件式，用來提取訂房資訊

        Returns:
            str: WHERE 條件式
        """

        if not start_date and end_date:
            start_date = end_date
        elif start_date and not end_date:
            end_date = start_date

        # 條件設置
        cdn_list = []

        if start_date:
            cdn_list.append(f"reservation.check_in_date <= '{start_date}'")
            cdn_list.append(f"reservation.check_out_date >= '{end_date}'")

        if account_name:
            cdn_list.append(f"account.account_name = '{account_name}'")

        if account_id:
            cdn_list.append(f"reservation.account_id = '{account_id}'")

        # 查詢語句設置
        return "WHERE " + " AND ".join(cdn_list) if cdn_list else ""
