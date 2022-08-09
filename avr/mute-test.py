import wifi
import socketpool
import time

HOST = "192.168.1.119"
PORT = 23

buffer = bytearray(1024)

pool = socketpool.SocketPool(wifi.radio)
s = pool.socket(pool.AF_INET, pool.SOCK_STREAM)

s.connect((HOST, PORT))
print("Connected!")

# zone2_check = s.send(b"Z2MU?\n")
# mute_off = s.send(b"Z2MUOFF\n")
# print("Message sent: query Zone 2 Power Status")
# bytes_rec = s.recv_into(buffer)
# msg_str = bytearray.decode(buffer)
# print("Msg received")
# print("Type: ",type(msg_str), msg_str)
# print("Done")


def mute_check():
    z2_mute_check = s.send(b"Z2MU?\n")
    bytes_rec = s.recv_into(buffer)
    mute_response = bytearray.decode(buffer)
    print("Msg received")
    print("Type: ", mute_response)


def mute_toggle():
    s.send(b"Z2MU?\n")
    s.recv_into(buffer)
    mute_response = bytearray.decode(buffer)
    print("Type: ", type(mute_response), mute_response)
    print("Length: ", len(mute_response), mute_response[:7])
    if mute_response[:7] is 'Z2MUOFF':

        s.send(b'Z2MUON\n')
        print("Mute on")
    else:
        print("Hello")
        s.send(b"Z2MUOFF\n")
        print(mute_response is "Z2MUOFF")
        print("Mute off")
        pass


mute_toggle()
