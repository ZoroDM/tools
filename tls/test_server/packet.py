import struct

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

# -----------------------------------
# 可配置参数
## 调试开关
### 是否打印请求报文详细码流(默认关闭)
print_client_req_packet_detail = False
### 是否打印响应报文详细码流(默认关闭)
print_server_rsp_packet_detail = False
### 是否开启请求并发(默认关闭)(暂不支持)
req_concurrency = False

# -----------------------------------
# 不可配置参数
# 客户端请求的报文id
client_req_packet_id = 0
# 客户端请求的报文头部长度
client_req_packet_head_size = 6
# 服务器响应的报文id
server_rsp_packet_id = 0
# 服务器响应报文的头部长度
server_rsp_packet_head_size = 6



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

def encode_client_request(dataSizeFromServer, paddingDataSize, print_detail=print_client_req_packet_detail):
    global client_req_packet_id
    paddingData = ([i%16 for i in range(0,int(paddingDataSize))])
    client_req_packet_id = client_req_packet_id + 1
    packet_len = 4+paddingDataSize
    req_packet = struct.pack("!HII{}s".format(paddingDataSize), client_req_packet_id , packet_len, dataSizeFromServer, bytes(paddingData))
  
    print_packet_data = bytes()
    if print_detail:
        print_packet_data = req_packet
    
    print_packet(f"request packet [id:{client_req_packet_id}] [len:{packet_len} bytes] [will_req_data:{dataSizeFromServer} bytes]", print_packet_data)

    return req_packet

def decode_client_request(packet_data, print_detail=print_client_req_packet_detail):
    req_packet = struct.pack(f"!{len(packet_data)}s", bytes(packet_data))
    decode_packet = struct.unpack("!HII", req_packet[0:10])

    id = decode_packet[0]
    req_packet_len = decode_packet[1]
    req_data_len = decode_packet[2]

    print_packet_data = bytes()
    if print_detail:
        print_packet_data = packet_data

    print_packet(f"request packet [id:{id}] [packet_len:{req_packet_len} bytes] [req_data_len:{req_data_len} bytes].", print_packet_data)
    return (id, req_packet_len, req_data_len)

def encode_server_response(rsp_data, print_detail = print_server_rsp_packet_detail):
    global server_rsp_packet_id
    server_rsp_packet_id += 1
    rsp_data_len = len(rsp_data)
    rsp_packet = struct.pack(f"!HI{rsp_data_len}s", server_rsp_packet_id, rsp_data_len, rsp_data)

    print_rsp_data = bytes()
    if print_detail:
        print_rsp_data = rsp_packet
    
    print_packet(f"response packet [id:{server_rsp_packet_id}] [rsp_data_len:{rsp_data_len} bytes].", print_rsp_data)

    return rsp_packet

def decode_server_response(packet_data, print_detail=print_server_rsp_packet_detail):
    rsp_packet = struct.pack("!{0}s".format(len(packet_data)),packet_data)
    decode_packet = struct.unpack("!HI",rsp_packet[0:6])
    
    id = decode_packet[0]
    rsp_data_len = decode_packet[1]
    total_size = len(packet_data)

    print_packet_data = bytes()
    if print_detail:
        print_packet_data = packet_data

    print_packet(f"response packet [id:{id}] [rsp_head:{6} + rsp_will_return_data:{rsp_data_len} bytes] [this_sharding_size:{total_size} bytes].", print_packet_data)
    
    return (id, rsp_data_len)