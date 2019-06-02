import socket
import ssl
import packet

# 可配置的参数信息
## 服务器信息
dst_addr = "192.168.1.12"
dst_port = 5678

## 一次请求服务器返回的数据部分大小
req_data_size = 1024
## 请求的次数限制
req_count_limit = 1000
## 发起的请求报文中数据部分大小
req_packet_size = 48

class client_ssl:
    def send_request(self,):
        CA_FILE = "ca.crt"
        KEY_FILE = "client.key"
        CERT_FILE = "client.crt"

        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.check_hostname = False
        context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
        context.load_verify_locations(CA_FILE)
        context.verify_mode = ssl.CERT_REQUIRED
        
        # 与服务端建立socket连接
        with socket.socket() as sock:
            # 将socket打包成SSL socket
            with context.wrap_socket(sock, server_side=False) as ssock:
                ssock.connect(('192.168.1.12', 4567))
                i = 0
                while True:
                    # 向服务端发送信息
                    if i > req_count_limit:
                        break

                    msg = packet.encode_client_request(req_data_size, req_packet_size)
                    ssock.send(msg)
                    # 接收服务端返回的信息

                    recv_len = 0
                    while True:
                        packet_head = None
                        if recv_len >= req_data_size:
                            break

                        msg = ssock.recv(8192)
                        if not len(msg):
                            break

                        if not packet_head:
                           packet_head = packet.decode_server_response(msg)
                           if len(msg) < packet.server_rsp_packet_head_size:
                               break
                           recv_len = len(msg) - packet.server_rsp_packet_head_size

                        else:
                            recv_len += len(msg)
                            print("\t recv_len:[{0}] rsp_count[{1}] req_count[{2}] rsp_id:[{3}] req_id[{4}]".format(recv_len,
                                i, i, packet_head[0], packet.req_packet_id))
                            if packet.print_server_rsp_packet_detail:
                                packet.print_packet("", msg)
                ssock.close()

if __name__ == "__main__":
    client = client_ssl()
    client.send_request()
