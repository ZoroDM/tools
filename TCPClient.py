import asyncore
import sys
import struct
import argparse

# 协议说明
# # 客户端请求：
# # |2Bytes req id |  4Bytes PacketLen | 4Byte ReqDataLenFromServer | Req Padding data |
# # req id ----- 客户端请求的id
# # PacketLen ---- 客户端请求报文总长( ReqDataLenFromServer  + Req Padding data )
# # ReqDataLenFromServer  ----- 要请求的服务器返回的数据量
# # Req Padding data  --- 客户端填充的无意义数据，满足 PacketLen
# # 服务器响应：
# # |2Bytes rsp id| 4Bytes PacketLen | rsp data|
# # rsp id ----- 返回客户端请求的id
# # PacketLen ---- 服务器返回的数据长度 len(rsp data)
# # rsp data ----- 服务器返回的填充数据
# 客户端请求报文说明
    ## |2Bytes packet id|4Bytes packetLen| 4Byte dataSizeFromServer| packetLen-4 size Padding data|
# 协议响应报文说明
    ## |2Bytes packet id|4Bytes paketLen| packetLen Bytes response data|
#-------------------------------------------------------------------------------------------------
# 可配置的参数信息
## 服务器信息
#dst_addr = "uc20.yealink.com"
#dst_port = 23457

#ali
dst_addr = "106.14.179.245"
dst_port = 23457

## 一次请求服务器返回的数据部分大小
req_data_size = 1024*1024
## 请求的次数限制
req_count_limit = 1000
## 发起的请求报文中数据部分大小
req_packet_size = 48
## 调试开关
### 是否打印请求报文详细码流(默认关闭)
print_req_packet_detail = False
### 是否打印响应报文详细码流(默认关闭)
print_rsp_packet_detail = False
### 是否开启请求并发(默认关闭)(暂不支持)
req_concurrency = False

#-------------------------------------------------------------------------------------------------
# 不可配置的参数信息
# 请求的报文id
req_packet_id = 0
# 响应的报文id
rsp_packet_id = 0

def print_packet(desc, packet_data):
    print(desc)
    if (not packet_data):
        return

    for i in range(0, len(packet_data)):
        if i%16 == 0:
            if i>0:
                print("") #报文换行
            print("\t ", end="") #报文缩进
        print('%02x' % packet_data[i], " ",end="") #报文输出不换行
    print("\n")

def encode_request(dataSizeFromServer, paddingDataSize, print_detail=False):
    global req_packet_id
    paddingData = ([i%16 for i in range(0,int(paddingDataSize))])
    req_packet_id = req_packet_id + 1
    packet_len = 4+paddingDataSize
    req_packet = struct.pack("!HII{}s".format(paddingDataSize), req_packet_id , packet_len, dataSizeFromServer, bytes(paddingData))
  
    if print_detail:
        print_packet("request packet [id:{0}] [len:{1} bytes] [will_req_data:{2} bytes]".format(req_packet_id,packet_len,dataSizeFromServer), req_packet)
    else:
        print_packet("request packet [id:{0}] [len:{1} bytes] [will_req_data:{2} bytes]".format(req_packet_id,packet_len,dataSizeFromServer),bytes())

    return req_packet

def decode_response(packet_data, print_detail=False):
    # return (packet_id, total_size, sharding_len)
    rsp_packet = struct.pack("!{0}s".format(len(packet_data)),packet_data)
    decode_packet = struct.unpack("!HI",rsp_packet[0:6])
    
    id = decode_packet[0]
    rsp_data_len = decode_packet[1]
    total_size = len(packet_data)
    if print_detail:
        print_packet("response packet [id:{0}] [rsp_head:{1} + rsp_will_return_data:{2} bytes] [this_sharding_size:{3} bytes]".format(id, 6, rsp_data_len, total_size), packet_data)
    else:
        print_packet("response packet [id:{0}] [rsp_head:{1} + rsp_will_return_data:{2} bytes] [this_sharding_size:{3} bytes]".format(id, 6, rsp_data_len, total_size), bytes())
    return (id, total_size)


class TCPEchoClient(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.connect( (host, port) )
        self.req_count = 0
        self.rsp_count = 0
        self.recv_len = 0

    def handle_connect(self):
        print("\nStart [req_count_limit:{0}] [per_req_packet_size:{1} bytes] [per_req_will_get_data_size:{2} ytes]... \n".format(
             req_count_limit, req_packet_size, req_data_size))
        self.handle_write()

    def handle_close(self):
        print("\nFinish [req_count:{0}] [rsp_count:{1}]!!! \n".format(self.req_count, self.rsp_count))
        self.close()

    def handle_read(self):
        global rsp_packet_id
        packet_rsp = self.recv(8192)
        if not len(packet_rsp):
            self.handle_close()
        
        if self.req_count == self.rsp_count + 1:
            packet_head = decode_response(packet_rsp, print_rsp_packet_detail)
            rsp_packet_id = packet_head[0]
            if rsp_packet_id == req_packet_id:
                self.rsp_count = self.rsp_count + 1

        self.recv_len += len(packet_rsp)
        print("\t recv_len:[{0}] rsp_count[{1}] req_count[{2}] rsp_id:[{3}] req_id[{4}]".format(self.recv_len,
         self.rsp_count, self.req_count, rsp_packet_id, req_packet_id))

        if not self.is_finish():
            self.handle_write()
        else:
            self.handle_close()

    def is_continue_write(self):
        return (not self.is_finish()) and self.rsp_count == self.req_count and (self.recv_len == 0 or self.recv_len - 6 >= req_data_size)

    def is_finish(self):
        return self.req_count >= req_count_limit and self.recv_len - 6 >= req_data_size

    def clear_recv(self):
        #print("Clear recv ...")
        self.recv_len = 0

    def writable(self):
        return self.is_continue_write()

    def handle_write(self):
        if self.is_continue_write():
            self.buffer = encode_request(req_data_size, req_packet_size-4, print_req_packet_detail) 
            self.send(self.buffer)
            self.req_count = self.req_count + 1
            self.clear_recv()
            

if __name__ == "__main__":
    if len(sys.argv) == 3:
        dst_addr = sys.argv[1]
        dst_port = int(sys.argv[2])
    client = TCPEchoClient(dst_addr, dst_port)
    asyncore.loop()