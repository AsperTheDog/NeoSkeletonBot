import secrets
import os


class SessionManager:
    _codes = {}
    _cookies = {}

    @staticmethod
    def setCookie(cookie, value):
        SessionManager._cookies[cookie] = value

    @staticmethod
    def setCode(code, value):
        SessionManager._codes[code] = value

    @staticmethod
    def get(cookie, code=None):
        if code in SessionManager._codes:
            return SessionManager._codes.pop(code)
        else:
            return SessionManager._cookies.get(cookie)

    @staticmethod
    def checkCookie(cookie):
        if cookie in SessionManager._cookies:
            return cookie
        return secrets.token_urlsafe(32)

    @staticmethod
    def existsCookie(cookie):
        return cookie in SessionManager._cookies
