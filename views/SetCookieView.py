from my_http.Request import Request
from my_http.Response import Response, HTTP_STATUS
from views.BaseView import BaseView


class SetCookieView(BaseView):
    @staticmethod
    def get(request: Request) -> Response:
        """
        :return: Cookieを設定して返す
        """
        # cookies = request.cookies
        return Response(status=HTTP_STATUS.OK, body=b"Cookie", headers={"Set-Cookie": "hogehogehogehoge"})
        # return Response(status=HTTP_STATUS.OK, body=b"Cookie", cookies={"key": "value"})
