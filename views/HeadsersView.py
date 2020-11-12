from my_http.Request import Request
from my_http.Response import Response, HTTP_STATUS


class HeadersView:
    @staticmethod
    def get_response(request: Request) -> Response:
        """
        /headers のパスにきたリクエストに対して、headerの内容をレスポンスとして返す
        :param request:
        :return:
        """
        return Response(status=HTTP_STATUS.OK, body=str(request.headers).encode())
