from functools import wraps

import mysql.connector as connector
from module.const import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD


class DbUtil:
    def print_query_and_result(callback):
        @wraps(callback)
        def decorator(query: str, params=()):
            if params == ():
                print("query: ", query)
            else:
                print("query: ", query % params)

            result = callback(query, params)

            if result:
                print("result: ", result)

            return result

        return decorator

    @staticmethod
    def connect():
        return connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database="Hotel",
        )

    @staticmethod
    @print_query_and_result
    def execute(query: str, params=()):
        db = DbUtil.connect()
        cursor = db.cursor()

        try:
            cursor.execute(query, params)
            db.commit()

        except Exception as ex:
            raise ex

        finally:
            cursor.close()
            db.close()

    @staticmethod
    @print_query_and_result
    def execute_fetch_all(query: str, params=()):
        db = DbUtil.connect()
        cursor = db.cursor()

        try:
            cursor.execute(query, params)
            data = cursor.fetchall()

        except Exception as ex:
            raise ex

        finally:
            cursor.close()
            db.close()

        return data

    @staticmethod
    @print_query_and_result
    def execute_fetch_one(query: str, params=()):
        db = DbUtil.connect()
        cursor = db.cursor()

        try:
            cursor.execute(query, params)
            data = cursor.fetchone()

        except Exception as ex:
            raise ex

        finally:
            cursor.close()
            db.close()

        return data
