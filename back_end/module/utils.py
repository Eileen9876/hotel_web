"""
放置全局可用的小功能函式
"""

import traceback
import random
import io
import qrcode
import base64
import uuid


def print_exception():
    traceback.print_exc()


def split_string_by_delimiter(input_string: str | None, delimiter: str) -> list:
    """
    Splits a string by a specified delimiter.
    Returns None if the input string is empty or the delimiter is invalid.

    Args:
        input_string (str): The string to split.
        delimiter (str): The delimiter to split the string by.

    Returns:
        list: A list of substrings, or None if the input is invalid.
    """
    if not input_string or not delimiter:
        return None
    return input_string.split(delimiter)


def get_value_or_none_from_list(target_list: list, index: int) -> any:
    """
    Safely retrieves the value at a specific index in a list.
    Returns None if the index is out of bounds.

    Args:
        target_list (list): The list to retrieve the value from.
        index (int): The index of the value to retrieve.

    Returns:
        any: The value at the specified index, or None if the index is out of bounds.
    """
    if index < 0 or index >= len(target_list):
        return None
    return target_list[index]


def get_first_or_none(target_list: list) -> any:
    """返回列表中的第一個元素，如果列表為空，則返回 None。

    該函式會檢查列表 `data` 是否為空，若不為空則返回列表的第一個元素，
    否則返回 None。

    Args:
        data (list): 要處理的列表。

    Returns:
        any: 列表中的第一個元素，若列表為空則返回 None。

    Example:
        >>> get_first_item_or_none([1, 2, 3])
        1
        >>> get_first_item_or_none([])
        None
    """
    return None if len(target_list) == 0 else target_list[0]


def get_or_add_index(L: list, value: str) -> int:
    """確保值存在於列表中，並返回其索引。

    該函式會尋找指定的值在列表中的索引。若值不存在，則將其追加至列表末端，並返回追加後的索引。

    Args:
        L (list): 要操作的列表。
        value (str): 要尋找的值。

    Returns:
        int: 值在列表中的索引（若值被追加，則返回其新索引）。

    Example:
        >>> my_list = ["apple", "banana"]
        >>> get_or_add_index(my_list, "banana")
        1
        >>> get_or_add_index(my_list, "cherry")
        2
        >>> my_list
        ["apple", "banana", "cherry"]
    """

    if value not in L:
        L.append(value)

    return L.index(value)


def get_random_int(size: int) -> int:
    """取得亂數值。

    Args:
        size (int): 位數

    Returns:
        int: 亂數值
    """
    result = ""
    for _ in range(size):
        result += str(random.randint(0, 9))
    return result


def url_to_qrcode_mime(url: str) -> str:
    """
    將網址轉換為 QRCode，並將生成的圖像轉換為 MIME 格式的 Base64 字符串。

    該函式會使用 `qrcode` 库生成 QRCode 圖像，然後將圖像轉換為字節流，
    最後將字節流進行 Base64 編碼，生成 MIME 格式的字符串。

    Args:
        url (str): 要轉換為 QRCode 的網址。

    Returns:
        str: QRCode 圖像的 MIME 格式字符串，包含 Base64 編碼的圖像數據。

    Example:
        >>> url_to_qrcode_mime("https://example.com")
        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgA...'
    """
    # 使用 qrcode 库生成 QRCode 圖像
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


def generate_id36() -> str:
    """建立36字元的識別碼"""
    return str(uuid.uuid4())


def has_common_elements(list1: list, list2: list) -> bool:
    """比對兩個陣列中是否有相同元素"""
    duplicates = list(set(list1) & set(list2))
    return bool(duplicates)
