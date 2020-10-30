import traceback
import socket
from datetime import datetime
from threading import Thread
import os
import datetime
from typing import Iterable, List

from WSGIApplication import WSGIApplication


class ServerThread(Thread):
    DOCUMENT_ROOT = "src"
    CONTENT_TYPE_MAP = {
        "html": "text/html",
        "htm": "text/html",
        "txt": "text/plain",
        "css": "text/css",
        "js": "application/javascript",
        "png": "image/png",
        "jpg": "image/jpg",
        "jpeg": "image/jpg",
        "gif": "image/gif",
    }

    response_line: str
    response_headers: List[tuple]

    def __init__(self, client_socket: socket):
        super().__init__()
        self.socket = client_socket

    def run(self):
        print("Worker: 処理開始")
        # noinspection PyBroadException
        try:
            # クライアントから受け取ったメッセージを代入（4096は受け取れるバイト数）
            msg_from_client = self.socket.recv(4096)
            # 受け取ったメッセージをファイルに書き込む
            with open("server_recv.txt", "wb") as f:
                f.write(msg_from_client)

            # リクエストメソッド
            status_line = msg_from_client.decode().split("\r\n")[0]
            request_method: str = msg_from_client.decode().split("\r\n")[0].split(" ")[0]
            # 要求されたファイルのパス
            path: str = msg_from_client.decode().split("\r\n")[0].split(" ")[1]
            headers = msg_from_client.decode().split("\r\n")[:-2]
            body = msg_from_client.decode().split("\r\n")[-1]
            print(body)

            extend: str = path.rsplit(".", maxsplit=1)[1].split("?")[0]
            normalized_path = os.path.normpath(path)  # パスの正規化
            requested_file_path = self.DOCUMENT_ROOT + normalized_path
            # ファイルがなければ404エラーを返す
            # is_exists = os.path.exists(requested_file_path)
            # if is_exists:

            # envを作る
            env = self._make_env(headers, body)

            # start_responseを作る
            def start_response(response_line: str, response_headers: List[tuple]):
                """start_responseが呼ばれたときに、response_lineとheadersの情報をWSGIサーバーが受け取って保持できるようにする"""
                self.response_line = response_line  # ステータスコード
                self.response_headers = response_headers  # レスポンスヘッダ

            body_bytes_list: Iterable[bytes] = WSGIApplication().application(env, start_response)

            # body_bytes_listをもとにレスポンスを作る
            output_bytes = b""
            self.response_headers.append(('Content-type', f'{self._get_content_type(extend)}'))
            print(self.response_headers)
            output_bytes += self._get_response_header()  # レスポンスヘッダ
            output_bytes += "\r\n".encode()  # 改行
            output_bytes += self._get_response_body(body_bytes_list)  # レスポンスボディ

            self.socket.send(output_bytes)

        except Exception:
            print("Worker: " + traceback.format_exc())

        finally:
            self.socket.close()
            print("Worker: 通信を終了しました")

    def _get_content_type(self, ext: str):
        if ext == "" or ext not in self.CONTENT_TYPE_MAP:
            return "application/octet-stream"
        return self.CONTENT_TYPE_MAP[ext]

    def _get_response_header(self) -> bytes:
        """start_responseがコールされた結果をもとに、レスポンスヘッダーを取得する"""
        # ex) "HTTP/1.1 200 OK"
        status_line = "HTTP/1.1 " + self.response_line + "\r\n"

        # ex)
        # self.response_headers = [("key1", "value1"), ("key2, value2")]
        # header_text_list = ["key1: value1", "key2: value2"]
        # header_text = "key1: value1\r\n key2: value2"
        header_text_list = (": ".join(response_header) for response_header in self.response_headers)  # ジェネレータ
        header_text = "\r\n".join(header_text_list) + "\r\n"

        header = b""
        header += status_line.encode()
        header += header_text.encode()
        return header

    @staticmethod
    def _get_response_body(body_bytes_list: Iterable[bytes]) -> bytes:
        """レスポンスボディを取得する"""
        return b"".join(body_bytes_list)

    @staticmethod
    def _get_date() -> str:
        return datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

    @staticmethod
    def _make_env(headers, body):
        for i, header in enumerate(headers):
            if i == 0:
                status_line = header
                path = status_line.split(" ")[1]
                env = {
                    "REQUEST_METHOD": status_line.split(" ")[0],
                    "PATH_INFO": path,
                    "QUERY_STRING": path.split('?')[1] if len(path.split('?')) > 1 else "",
                    "CONTENT_TYPE": '',
                    "CONTENT_LENGTH": '',
                    "SERVER_NAME": 'Nao/0.1',
                    "SERVER_PROTOCOL": 'protocol',
                }
            elif "Content-Type" in header:
                env = {
                    "CONTENT_TYPE": header.split(" ")[1],
                }
            elif "Content-Length" in header:
                env = {
                    "CONTENT_LENGTH": header.split(" ")[1],
                }
            elif "Query-String" in header:
                env = {
                    "QUERY_STRING": header.split(" ")[1],
                }
            else:
                key = 'HTTP_' + header.split(": ")[0].replace("-", "_").upper()
                env[key] = header.split(": ")[1]
        # env["wsgi.input"] =
        return env
