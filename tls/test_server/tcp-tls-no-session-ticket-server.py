import socket
import ssl
import packet
import time

class server_ssl:
    def build_listen(self):
        CA_FILE = "ca.crt"
        KEY_FILE = "server.key"
        CERT_FILE = "server.crt"
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
        context.load_verify_locations(CA_FILE)
        #context.verify_mode = ssl.CERT_REQUIRED
        context.options |= ssl.OP_NO_TICKET

        # 监听端口
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            # 将socket打包成SSL socket
            with context.wrap_socket(sock, server_side=True) as ssock:
                ssock.bind(('0.0.0.0', 23456))
                ssock.listen(5)
                while True:
                    # 接收客户端连接
                    client_socket, addr = ssock.accept()
                    # 接收客户端信息
                    print(f"receive msg from client: {addr}")
                    
                    while True:
                        recv_data_len = 0
                        packet_head = None
                        req_packet = client_socket.recv(1024)
                        if not packet_head:
                            packet_head = packet.decode_client_request(req_packet)
                        
                        req_id = packet_head[0]
                        req_packet_len = packet_head[1]
                        req_data_len = packet_head[2]
                        recv_data_len = len(req_packet) - packet.client_req_packet_head_size
                        while recv_data_len < req_packet_len:
                            req_packet = client_socket.recv(1024)
                            recv_data_len += len(req_packet)
                            print(f"\t req_len:[{recv_data_len}] req_id:[{req_id}]")
                            if packet.print_client_req_packet_detail:
                                packet.print_packet("", req_packet)

                        rsp_data = bytes(req_data_len)
                        rsp_packet = packet.encode_server_response(rsp_data)
                        time.sleep(1)
                        client_socket.send(rsp_packet)

                    client_socket.close()


if __name__ == "__main__":
    server = server_ssl()
    server.build_listen()
