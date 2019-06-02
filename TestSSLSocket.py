import socket
import ssl

def test1():
    hostname = 'www.python.org'
    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            print (ssock.version())

def test2():
    hostname = 'www.python.org'
    # PROTOCOL_TLS_CLINET requires valid cert chain and hostname
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations('path/to/cabundle.pem')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            print(ssock.version())

if __name__ == '__main__':
    test1()
    test2()