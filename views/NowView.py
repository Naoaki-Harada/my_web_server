from datetime import datetime

from my_http.Response import Response, HTTP_STATUS


class NowView:
    @staticmethod
    def current_time_response() -> Response:
        body_str = f"<html><body><h1>now is {datetime.now()}</h1></body></html>"
        return Response(status=HTTP_STATUS.OK, body=body_str.encode())
