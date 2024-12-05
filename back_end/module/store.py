import json
import qrcode
import io
import base64

from module.database import DbUtil
import module.utils as utils


class StoreService:

    @staticmethod
    def add_store_merchant(
        account_id: str,
        name: str,
        address: str,
        phone: str,
        office_url: str,
        google_map_url: str,
        intro: str,
        image: str,
    ):
        """新增商店訊息"""

        store_id = utils.generate_id36()

        StoreUtil.insert_store_table(
            table="store_record",
            store_id=store_id,
            store_name=name,
            store_address=address,
            store_phone=phone,
            store_intro=intro,
            office_url=office_url,
            google_map_url=google_map_url,
            account_id=account_id,
        )

        StoreUtil.insert_image(
            table="store_image_record", store_id=store_id, image=image
        )

    @staticmethod
    def get_store_traveler() -> dict:
        """從資料表 store 中取得商店資料

        Returns:
            dict:
            商店資訊(非詳細資訊):
                {
                    商店識別碼: {
                        "store_id": 商店識別碼str,
                        "store_name": 店名str,
                        "store_intro": 商店描述str,
                        "store_image": 商店圖片str
                    },
                }
        """
        column = ["store_id", "store_name", "store_intro"]

        query = f"""
            SELECT {", ".join(column)}
            FROM store;
        """
        store_info_list = DbUtil.execute_fetch_all(query)

        # 取得商店圖片
        store_image_list = StoreUtil.get_image(table="store_image")

        result = {}
        for store in store_info_list:
            id = store[0]
            result[id] = {col: store[idx] for idx, col in enumerate(column)}
            result[id]["store_image"] = store_image_list[id]

        return result

    @staticmethod
    def get_store_admin(page_idx: int) -> dict:
        """從資料表 store_record 中取得未審核商店

        Args:
            page_idx (int): 分頁索引

        Returns:
            dict:
            商店資訊(非詳細資訊):
                {
                    商店識別碼: {
                        "store_id": 商店識別碼str,
                        "store_name": 店名str
                    },
                }
        """

        page_size = 10  # 每頁顯示最大筆數

        offset = (page_idx - 1) * page_size  # 第幾頁

        column = ["store_id", "store_name"]

        query = f"""
            SELECT {", ".join(column)}
            FROM store_record
            WHERE review_status = 'PENDING'
            LIMIT {page_size} OFFSET {offset};
        """

        store_info_list = DbUtil.execute_fetch_all(query)

        result = {}
        for store in store_info_list:
            id = store[0]
            result[id] = {col: store[idx] for idx, col in enumerate(column)}

        return result

    @staticmethod
    def get_store_merchant(account_id: str, page_idx: int) -> dict:
        """從資料表 store_record 中，根據帳號取得對應商店

        Args:
            page_idx (int): 分頁索引

        Returns:
            dict:
            商店資訊(非詳細資訊):
                {
                    商店識別碼: {
                        "store_id": 商店識別碼str,
                        "store_name": 店名str,
                        "review_status": 審核狀態 ex 'PENDING', 'APPROVED', 'REJECTED'
                    },
                }
        """

        page_size = 10  # 每頁顯示最大筆數

        offset = (page_idx - 1) * page_size  # 第幾頁

        column = ["store_id", "store_name", "review_status"]

        query = f"""
            SELECT {", ".join(column)}
            FROM store_record
            WHERE account_id = %s
            LIMIT {page_size} OFFSET {offset};
        """

        store_info_list = DbUtil.execute_fetch_all(query, (account_id,))

        result = {}
        for store in store_info_list:
            id = store[0]
            result[id] = {col: store[idx] for idx, col in enumerate(column)}

        return result

    @staticmethod
    def get_store_detailed_traveler(store_id: str) -> dict:
        """取得指定商店的詳細資訊

        Returns:
            dict:
            回傳指定商店的詳細資訊:
                {
                    "store_name": 店名str
                    "store_address": 地址str
                    "store_phone": 電話str
                    "store_intro": 商店描述str
                    "office_url": 官方網站網址str
                    "google_map_url": google地圖網址
                    "image": {
                        "store_image": 商店圖片(MIME編碼)str
                        "office_url": 官網qrcode(MIME編碼)str
                        "google_map_url": google地圖網址qrcode(MIME編碼)str
                    }
                }
        """
        column = [
            "store_name",
            "store_address",
            "store_phone",
            "store_intro",
            "office_url",
            "google_map_url",
        ]

        query = f"""
            SELECT {", ".join(column)}
            FROM store
            WHERE store_id = %s
            LIMIT 1;
        """

        # 取得商店訊息
        store_info = DbUtil.execute_fetch_one(query, (store_id,))

        # 取得圖片資料
        store_image = StoreUtil.get_image(table="store_image", store_id=store_id)

        # 設置回傳值
        result = {}
        result["image"] = {}

        for idx, col in enumerate(column):
            result[col] = store_info[idx]

            if col == "office_url" or col == "google_map_url":
                result["image"][col] = StoreUtil.generate_qrcode(store_info[idx])

        result["image"]["store_image"] = store_image[store_id]

        return result

    @staticmethod
    def get_store_detailed_merchant(store_id: str) -> dict:
        """取得指定商店的詳細資訊

        Returns:
            dict:
            回傳指定商店的詳細資訊:
                {
                    "store_name": 店名str
                    "store_address": 地址str
                    "store_phone": 電話str
                    "store_intro": 商店描述str
                    "office_url": 官方網站網址str
                    "google_map_url": google地圖網址
                    "review_status": 審核狀態str ex.'PENDING', 'APPROVED', 'REJECTED'
                    "image": {
                        "store_image": 商店圖片(MIME編碼)str
                    }
                }
        """
        column = [
            "store_name",
            "store_address",
            "store_phone",
            "store_intro",
            "office_url",
            "google_map_url",
            "review_status",
        ]

        query = f"""
            SELECT {", ".join(column)}
            FROM store_record
            WHERE store_id = %s
            LIMIT 1;
        """

        # 取得商店訊息
        store_info = DbUtil.execute_fetch_one(query, (store_id,))

        # 取得圖片資料
        store_image = StoreUtil.get_image(table="store_image_record", store_id=store_id)

        # 設置回傳值
        result = {col: store_info[idx] for idx, col in enumerate(column)}
        result["image"] = {"store_image": store_image[store_id]}

        return result

    @staticmethod
    def update_store_merchant(
        account_id: str, store_id: str, update_data: dict
    ) -> bool:
        """更新指定商店的資訊

        更新資料表 store_record 中的商店資料，並將審核狀態更改為 "PENDNIG"。

        Args:
            id (str): 指定的商店編號
            data (dict): 要更新的資料，
                        格式 { 要更改的欄位: 更新後的值 }，
                        範例 { "store_phone": '0912345678' }

        Returns:
            bool: 執行成功回傳True否則回傳False。
        """

        # 驗證account_id是否正確
        if StoreUtil.verify_account(account_id, store_id) == False:
            return False

        # 商店圖片更新
        if "image" in update_data:
            StoreUtil.update_image(
                table="store_image_record",
                store_id=store_id,
                image=update_data["image"],
            )

            update_data.pop("image")

        # 商店資訊更新
        StoreUtil.update_store_table("store_record", store_id, update_data)

        # 更新審核狀態為 `PENDING`
        StoreUtil.set_review_status(store_id, "PENDING")

        return True

    @staticmethod
    def approved_store(store_id: str):
        """商店通過審核

        更新商店的審核狀態為 "APPROVED"（已審核），
        假如該筆資料已存在於 `store` 資料表，則更新，否則新增該筆資料。

        Args:
            store_id (str): 要審核的商店唯一識別碼。
        """

        # 設置審核狀態
        StoreUtil.set_review_status(store_id, "APPROVED")

        # 確認資料是否已存在，用於決定是要「更新」資料還是「新增」資料
        is_exist = StoreUtil.is_store_exist("store", store_id)

        if is_exist:
            StoreUtil.update_approved_store(store_id)
        else:
            StoreUtil.insert_approved_store(store_id)

    @staticmethod
    def rejected_store(store_id: str):
        """商店審核退回"""

        StoreUtil.set_review_status(store_id, "REJECTED")

    @staticmethod
    def record_store_page_views(store_id: str):
        """記錄頁面瀏覽次數"""

        query = """
            INSERT INTO store_view (store_id, view_time) 
            VALUES (%s, NOW());
        """

        DbUtil.execute(query, (store_id,))

    @staticmethod
    def get_store_page_views(store_id: str) -> list:
        """取得今年每個月的瀏覽次數

        該函式會查詢資料庫，統計指定商店在今年每個月的瀏覽次數，返回一個包含 12 個元素的列表，
        對應 1 到 12 月的瀏覽次數（若某月無數據則為 0）。

        Args:
            id (str): 商店編號，對應資料庫的 `store_id` 欄位

        Returns:
            dict: 長度為 12 的列表，分別對應 1 到 12 月的瀏覽次數。

        Example:
            >>> # 假設商店編號為 '12345'
            >>> get_page_views("12345")
            [5, 12, 8, 0, 0, 3, 7, 10, 0, 0, 0, 0]
        """
        query = """
            SELECT MONTH(view_time) AS month, COUNT(*) AS cnt
            FROM store_view
            WHERE store_id = %s
                AND YEAR(view_time) = YEAR(CURDATE())
            GROUP BY YEAR(view_time), MONTH(view_time)
            ORDER BY MONTH(view_time);
        """

        db_data = DbUtil.execute_fetch_all(query, (store_id,))

        result = [0] * 12
        for data in db_data:
            result[data[0] - 1] = data[1]  # data[0]: 月份，data[1]: 次數

        return result

    @staticmethod
    def favorite_store(account_id: str, store_id: str):
        """收藏商店

        新增一筆收藏紀錄到 store_favorite_record，並更新或新增收藏狀態到 store_favorite
        """

        # 新增一筆收藏紀錄到 store_favorite_record
        StoreUtil.insert_favorite_store(
            table="store_favorite_record",
            store_id=store_id,
            account_id=account_id,
            fav_status=True,
        )

        # 更新或新增收藏狀態到 store_favorite
        is_exist = StoreUtil.is_favorite_exist(
            table="store_favorite",
            store_id=store_id,
            account_id=account_id,
        )

        if is_exist:
            StoreUtil.update_favorite_store(
                table="store_favorite",
                store_id=store_id,
                account_id=account_id,
                fav_status=True,
            )
        else:
            StoreUtil.insert_favorite_store(
                table="store_favorite",
                store_id=store_id,
                account_id=account_id,
                fav_status=True,
            )

    @staticmethod
    def cancel_favorite_store(account_id: str, store_id: str):
        """取消收藏商店

        新增一筆收藏紀錄到 store_favorite_record，並更新收藏狀態到 store_favorite
        """

        # 新增一筆收藏紀錄到 store_favorite_record
        StoreUtil.insert_favorite_store(
            table="store_favorite_record",
            store_id=store_id,
            account_id=account_id,
            fav_status=False,
        )

        # 更新收藏狀態到 store_favorite
        StoreUtil.update_favorite_store(
            table="store_favorite",
            store_id=store_id,
            account_id=account_id,
            fav_status=False,
        )

    @staticmethod
    def get_favorite_store_traveler(account_id: str) -> dict:
        """根據 store_favorite 從資料表 store 中取得收藏商店

        Returns:
            dict:
            商店資訊(非詳細資訊):
                {
                    商店識別碼: {
                        "store_id": 商店識別碼str,
                        "store_name": 店名str,
                        "store_intro": 商店描述str,
                        "store_image": 商店圖片str
                    },
                }
        """

        column = ["store_id", "store_name", "store_intro"]

        query = f"""
            SELECT {", ".join(f"store.{col} AS {col}" for col in column)}
            FROM store_favorite
            INNER JOIN store 
            ON store_favorite.store_id = store.store_id 
            WHERE store_favorite.account_id = %s AND store_favorite.fav_status = TRUE;
        """

        store_list = DbUtil.execute_fetch_all(query, (account_id,))

        # 取得商店圖片
        store_image_list = StoreUtil.get_image(table="store_image")

        result = {}
        for store in store_list:
            id = store[0]
            result[id] = {col: store[idx] for idx, col in enumerate(column)}
            result[id]["store_image"] = store_image_list[id]

        return result

    @staticmethod
    def get_favorite_store_id_traveler(account_id: str) -> list:
        """根據 store_favorite 從資料表 store 中取得收藏商店

        Returns:
            list: [商店識別碼,]
        """

        query = """
            SELECT store_id
            FROM store_favorite
            WHERE account_id = %s AND fav_status = TRUE;
        """

        result = DbUtil.execute_fetch_one(query, (account_id,))

        if result:
            return list(result)
        else:
            return []

    @staticmethod
    def get_total_favorites(store_id: str) -> int:
        """取得總收藏數"""

        query = """
            SELECT COUNT(*) AS cnt
            FROM store_favorite
            WHERE store_id = %s AND fav_status = TRUE;
        """

        db_data = DbUtil.execute_fetch_one(query, (store_id,))

        if db_data:
            return db_data[0]
        else:
            return 0

    @staticmethod
    def get_favorite_statistics(store_id: str) -> list:
        """取得今年每個月的收藏數

        該函式會查詢資料庫，統計指定商店在今年每個月的「收藏」與「取消收藏」次數，並相減取得當月總收藏數。
        返回一個包含 12 個元素的列表，對應 1 到 12 月的收藏數（若某月無數據則為 0）。

        Args:
            id (str): 商店編號，對應資料庫的 `store_id` 欄位

        Returns:
            dict: 長度為 12 的列表，分別對應 1 到 12 月的收藏數。

        Example:
            >>> # 假設商店編號為 '12345'
            >>> get_favorite_statistic("12345")
            [5, 12, 8, 0, 0, 3, 7, 10, 0, 0, 0, 0]
        """

        query = """
            SELECT
                MONTH(fav_time) AS month, 
                SUM(CASE WHEN fav_status = TRUE THEN 1 ELSE 0 END) AS favorites,
                SUM(CASE WHEN fav_status = FALSE THEN 1 ELSE 0 END) AS unfavorites
            FROM store_favorite_record
            WHERE store_id = %s
                AND YEAR(fav_time) = YEAR(CURDATE())
            GROUP BY YEAR(fav_time), MONTH(fav_time)
            ORDER BY MONTH(fav_time);
        """

        db_data = DbUtil.execute_fetch_all(query, (store_id,))

        result = [0] * 12
        for data in db_data:
            # data[0]: 月份，data[1]: 收藏數，data[2]: 取消收藏數
            result[data[0] - 1] = data[1] - data[2]

        return result


class StoreUtil:
    @staticmethod
    def set_review_status(store_id: str, status: str):
        """更新審核狀態

        更新 `store` 資料表的 `review_status` 欄位。
        """
        query = f"""
            UPDATE store_record
            SET review_status = '{status}'
            WHERE store_id = %s;
        """

        DbUtil.execute(query, (store_id,))

    @staticmethod
    def is_store_exist(table: str, store_id: str) -> bool:
        """指定的商店資料是否存在於指定表單中"""

        query = f"""
            SELECT EXISTS(
                SELECT 1 
                FROM {table}
                WHERE store_id = %s
            );
        """

        result = DbUtil.execute_fetch_one(query, (store_id,))

        return bool(result[0])

    @staticmethod
    def is_favorite_exist(table: str, store_id: str, account_id: str) -> bool:
        """是否曾經收藏過商店"""

        query = f"""
            SELECT EXISTS(
                SELECT 1 
                FROM {table}
                WHERE store_id = %s AND account_id = %s
            );
        """

        result = DbUtil.execute_fetch_one(query, (store_id, account_id))

        return bool(result[0])

    @staticmethod
    def insert_favorite_store(
        table: str, store_id: str, account_id: str, fav_status: bool
    ):
        """新增收藏商店"""

        query = f"""
            INSERT INTO {table} (store_id, account_id, fav_status) 
            VALUES (%s, %s, %s);
        """

        DbUtil.execute(query, (store_id, account_id, fav_status))

    @staticmethod
    def update_favorite_store(
        table: str, store_id: str, account_id: str, fav_status: bool
    ):
        """取消收藏商店"""

        query = f"""
            UPDATE {table}
            SET fav_status = %s
            WHERE store_id = %s AND account_id = %s;
        """

        DbUtil.execute(query, (fav_status, store_id, account_id))

    @staticmethod
    def insert_approved_store(store_id: str):
        """新增已審核商店資料。

        此方法會根據提供的 `store_id`，將 `store_record` 表中的商店資料新增至 `store` 表，
        與 `store_image_record` 表中的商店資料新增至 `store_image` 表。
        """

        # 新增至 `store` 表

        column = [
            "store_id",
            "store_name",
            "store_address",
            "store_phone",
            "office_url",
            "google_map_url",
            "store_intro",
            "account_id",
        ]

        query = f"""
            INSERT INTO store ({", ".join(column)})
            SELECT {", ".join(column)}
            FROM store_record
            WHERE store_id = %s;
        """

        DbUtil.execute(query, (store_id,))

        # 新增至 `store_image` 表

        query = """
            INSERT INTO store_image (store_id, store_image)
            SELECT store_id, store_image
            FROM store_image_record
            WHERE store_image_record.store_id = %s;
        """

        DbUtil.execute(query, (store_id,))

    @staticmethod
    def update_approved_store(store_id: str):
        """更新已審核商店資料。

        此方法會根據提供的 `store_id`，將 `store_record` 表中的商店資料更新至 `store` 表，
        與 `store_image_record` 表中的商店資料更新至 `store_image` 表。
        """

        # 更新 `store` 表

        column = [
            "store_id",
            "store_name",
            "store_address",
            "store_phone",
            "office_url",
            "google_map_url",
            "store_intro",
            "account_id",
        ]

        query = f"""
            UPDATE store
            JOIN store_record ON store.store_id = store_record.store_id
            SET 
                {", ".join([f"store.{col} = store_record.{col}" for col in column])}
            WHERE store.store_id = %s;
        """

        DbUtil.execute(query, (store_id,))

        # 更新 `store_image` 表

        query = """
            UPDATE store_image
            JOIN store_image_record ON store_image.store_id = store_image_record.store_id
            SET store_image.store_image = store_image_record.store_image
            WHERE store_image.store_id = %s;
        """

        DbUtil.execute(query, (store_id,))

    @staticmethod
    def update_store_table(table: str, store_id: str, data: dict):
        """更新資料庫中的商店表格資料

        Args:
            id (str): 指定的商店編號
            data (dict): 要更新的資料，
                        格式 { 要更改的欄位: 更新後的值 }，
                        範例 { "phone": '0912345678' }

        """

        clause = []
        for col in data.keys():
            clause.append(col + " = '%s'" % data[col])

        query = f"UPDATE {table} SET {','.join(clause)} WHERE store_id = %s;"

        DbUtil.execute(query, (store_id,))

    @staticmethod
    def insert_store_table(
        table: str,
        store_id: str,
        store_name: str,
        store_address: str,
        store_phone: str,
        store_intro: str,
        office_url: str,
        google_map_url: str,
        account_id: str,
    ):
        column = [
            "store_id",
            "store_name",
            "store_address",
            "store_phone",
            "store_intro",
            "office_url",
            "google_map_url",
            "account_id",
        ]

        query = f"""
            INSERT INTO {table} ({", ".join(column)})
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """

        values = (
            store_id,
            store_name,
            store_address,
            store_phone,
            store_intro,
            office_url,
            google_map_url,
            account_id,
        )

        DbUtil.execute(query, values)

    @staticmethod
    def update_image(table: str, store_id: str, image: str):
        """更新商店或qrcode圖片"""

        query = f"""
            UPDATE {table}
            SET store_image = %s
            WHERE store_id = %s;
        """

        DbUtil.execute(query, (image, store_id))

    @staticmethod
    def insert_image(table: str, store_id: str, image: str):
        """儲存商店圖片"""

        query = f"""
            INSERT INTO {table} (store_id, store_image) 
            VALUES (%s, %s);
        """

        DbUtil.execute(query, (store_id, image))

    @staticmethod
    def get_image(table: str, store_id: str | None = None) -> dict:
        """取得商店圖片

        Args:
            store_id (str | None, optional): 預設為 None
                - None: 提取所有商店圖片
                - str: 提取指定商店圖片

        Returns:
            dict:
            - 指定商店:
                {
                    商店識別碼: 商店圖片(MIME編碼)str
                }
            - 無指定商店:
                {
                    商店識別碼: 商店圖片(MIME編碼)str,
                    商店識別碼2: 商店圖片2(MIME編碼)str,
                }
        """

        result = {}

        if not store_id:  # 提取全部
            query = f"""
                SELECT store_id, store_image
                FROM {table};
            """

            db_data = DbUtil.execute_fetch_all(query)

            for data in db_data:
                result[data[0]] = data[1]  # data[0]: store_id, data[1]: store_image

        else:  # 提取特定
            query = f"""
                SELECT store_image
                FROM {table}
                WHERE store_id = %s;
            """

            db_data = DbUtil.execute_fetch_all(query, (store_id,))

            result[store_id] = db_data[0]

        return result

    @staticmethod
    def verify_account(account_id: str, store_id: str) -> bool:
        """驗證帳號識別碼是否正確"""

        QUERY = """
            SELECT COUNT(*) AS is_valid
            FROM store_record
            WHERE store_id = %s
            AND account_id = %s;
        """

        result = DbUtil.execute_fetch_one(QUERY, (store_id, account_id))

        is_valid = (
            result[0] if result else 0
        )  # 確保 result 是數字類型（防止意外返回空值）

        return is_valid > 0

    @staticmethod
    def generate_qrcode(url: str) -> str:
        """
        將網址轉換為 QRCode，再轉成 MIME 格式的字符串

        Args:
            url (str): 要轉換為 QRCode 的網址

        Returns:
            str: QRCode 圖像的 MIME 格式
        """
        image = qrcode.make(url)

        # 將圖像轉換為字符流
        image_bytes = io.BytesIO()
        image.save(image_bytes)
        image_bytes.seek(0)

        # 轉成 Base64 字符串
        encoded_str = base64.b64encode(image_bytes.read()).decode()

        # 獲取 MIME 格式
        mime_str = "data:image/png;base64," + encoded_str

        return mime_str
