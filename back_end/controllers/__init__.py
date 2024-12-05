from flask import Flask
from flask_cors import CORS

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="static",
    template_folder="templates",
)

CORS(app)

# 引入要使用的路由檔案，需在設置 app 變數後，
# 否則會出現 name 'app' is not defined 的錯誤。
from controllers import account_controller, book_controller, store_controller


# 測試用
@app.route("/")
def test():
    return "connect success"
