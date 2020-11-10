from my_http.Request import Request
from my_http.Response import Response, HTTP_STATUS


class ParametersView:
    def get_response(self, request: Request) -> Response:
        """
        /parameters のパスにきたリクエストに対して、適切なレスポンスを生成して返す
        :param request:
        :return:
        """
        if request.method == "GET":
            return self._get(request)
        elif request.method == "POST":
            return self._post(request)
        else:
            return Response(status=HTTP_STATUS.METHOD_NOT_ALLOWED)

    @staticmethod
    def _get(request: Request) -> Response:
        """
        リクエストメソッドがGETだった時の処理
        """
        return Response(status=HTTP_STATUS.OK, body=str(request.GET).encode())

    @staticmethod
    def _post(request: Request) -> Response:
        """
        リクエストメソッドがPOSTだった時の処理
        """
        return Response(status=HTTP_STATUS.OK, body=str(request.POST).encode())
