import wifi
import socketpool

HOST = "192.168.1.119"
PORT = 23

buffer = bytearray(1024)
print("test")


pool = socketpool.SocketPool(wifi.radio)
s = pool.socket(pool.AF_INET, pool.SOCK_STREAM)

s.connect((HOST, PORT))
print("Connected!")
zone2_check = s.send(b"Z2?\n")
print("Message sent")

msg = s.recv_into(buffer)
print("Msg received")
print(msg)

print("Done")