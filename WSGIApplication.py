from typing import Callable, List
import os


import datetime

DOCUMENT_ROOT = "src"


class WSGIApplication:

    @staticmethod
    def application(env: dict, start_response: Callable[[str, List[tuple]], None]):
        method = env["REQUEST_METHOD"]
        path = env["PATH_INFO"]

        # start_responseを一度だけコールする
        # 固定で200 OKにする
        # Content-typeはWSGIサーバ側で編集するので空のリストにする
        start_response('200 OK', [('Server', 'Nao/0.1'),
                                  ('Connection', 'Close')])

        if '/now' in path:
            body = f'<h1>{datetime.datetime.now()}</h1>'
            return [body.encode()]
        elif '/headers' in path:
            body = [f'{x}: {env[x]}<br>'.encode() for x in env]
            return body
        else:
            # レスポンスボディを返す
            # ex) '<h1>METHOD: POST, PATH: /index.html</h1>'
            normalized_path = os.path.normpath(path)  # パスの正規化
            requested_file_path = DOCUMENT_ROOT + normalized_path
            with open(requested_file_path, "rb") as f:
                body = f.read()
            return [body]
