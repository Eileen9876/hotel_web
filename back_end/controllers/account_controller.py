from flask import request

from controllers import app
from module.account import AccountService
from controllers.decorator import err_catch


@app.route("/register", methods=["POST"])
@err_catch
def register_route():
    """註冊"""
    data = request.get_json()
    return AccountService.register(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        type=data["type"],
    )


@app.route("/login", methods=["POST"])
@err_catch
def login_route():
    """登入"""
    data = request.get_json()
    return AccountService.login(
        email=data["email"],
        password=data["password"],
    )
