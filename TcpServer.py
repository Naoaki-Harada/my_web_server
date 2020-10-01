import socket


class TCPServer:
    def main(self):
        # create an INET(IPv4), STREAMing socket socketのインスタンスを生成
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host, and a well-known port 8080番ポート向けにきた通信を受け取る設定
        server_socket.bind(("localhost", 8080))
        # become a server socket 待ち受けモードになる
        server_socket.listen(1)

        print("クライアント接続を待ちます。")
        (client_socket, address) = server_socket.accept()
        print("クライアント接続")

        # クライアントから受け取ったメッセージを代入（4096は受け取れるバイト数）
        msg_from_client = client_socket.recv(4096)

        # 受け取ったメッセージをファイルに書き込む
        with open("server_recv.txt", "wb") as f:
            f.write(msg_from_client)

        # 送り返す用のメッセージをファイルから読み込む
        with open("server_send.txt", "rb") as f:
            msg_to_client = f.read()

        # メッセージを送り返す
        client_socket.send(msg_to_client)

        client_socket.close()
        print("通信を終了しました")


if __name__ == '__main__':
    TCPServer().main()
