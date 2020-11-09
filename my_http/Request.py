from dataclasses import dataclass


@dataclass
class Request:
    headers: dict
    POST: dict
    GET: dict

    @staticmethod
    def from_env(env: dict) -> "Request":
        """
        WSGIインターフェースのenvからリクエストクラスを生成するファクトリーメソッド
        """
        Request.headers = env
        Request.POST = env
        Request.GET = env
        raise NotImplementedError